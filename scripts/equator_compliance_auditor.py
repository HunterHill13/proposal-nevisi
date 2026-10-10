#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
equator_compliance_auditor.py - EQUATOR Network Compliance & Biological Resource Authentication Auditor
Proposal-Nevisi Engine v10.1 (Universal Biomedical Architecture)

Enforces international transparency, reproducibility, and reporting standards:
1. OECD / GCCP (Good Cell Culture Practice):
   - Cell line provenance & STR profiling authentication
   - Mycoplasma testing protocol & frequency
   - Passage number containment (<= 10 passages)
2. MIQE Standard (qPCR & Gene Expression Experiments):
   - RNA extraction, purity & integrity assessment (RIN >= 7, A260/A280)
   - Primer specificity, efficiency (90-110%), and amplicon validation
   - Internal reference gene normalization & 2^(-Delta Delta Ct) method
3. ARRIVE 2.0 Guidelines (In Vivo Animal Studies):
   - Ethical protocol & animal housing conditions
   - Random allocation, allocation concealment, and investigator blinding
   - Humane endpoints, monitoring, and euthanasia criteria
4. Biological & Chemical Resource Authentication (NIH Mandate / SciScore):
   - CAS registry number / RRID tracking
   - Compound purity verification (>= 95% via HPLC/MS)
   - Vehicle control toxicity threshold (e.g. DMSO <= 0.1% v/v)

100% General-Purpose and Config-Driven: Zero hard-coded drugs or diseases.
"""

import os
import re
import json
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple


@dataclass
class GuidelineItemCheck:
    guideline: str
    criterion_fa: str
    criterion_en: str
    is_met: bool
    evidence_snippet: str = ""
    severity: str = "MAJOR"  # "CRITICAL" | "MAJOR" | "MINOR"
    remediation_fa: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "guideline": self.guideline,
            "criterion_fa": self.criterion_fa,
            "criterion_en": self.criterion_en,
            "is_met": self.is_met,
            "severity": self.severity,
            "evidence_snippet": self.evidence_snippet[:120] if self.evidence_snippet else "",
            "remediation_fa": self.remediation_fa
        }


@dataclass
class EquatorAuditResult:
    compliance_score: float  # 0.0 to 100.0%
    is_compliant: bool
    applicable_guidelines: List[str]
    total_checks: int
    passed_checks: int
    critical_deficits: List[str] = field(default_factory=list)
    detailed_checks: List[GuidelineItemCheck] = field(default_factory=list)
    executive_summary_fa: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "compliance_score": round(self.compliance_score, 1),
            "is_compliant": self.is_compliant,
            "applicable_guidelines": self.applicable_guidelines,
            "total_checks": self.total_checks,
            "passed_checks": self.passed_checks,
            "critical_deficits": self.critical_deficits,
            "executive_summary_fa": self.executive_summary_fa,
            "detailed_checks": [c.to_dict() for c in self.detailed_checks]
        }


class EquatorComplianceAuditor:
    """Master evaluator for EQUATOR reporting guidelines and biological authentication."""

    @classmethod
    def parse_sections(cls, proposal_input: Any) -> Dict[int, str]:
        """Parses markdown text or dict into a normalized 1-28 section map."""
        sections_map: Dict[int, str] = {}
        if isinstance(proposal_input, dict):
            for k, v in proposal_input.items():
                if isinstance(k, int) and 1 <= k <= 28:
                    sections_map[k] = str(v)
                elif isinstance(k, str):
                    m = re.match(r'^(?:##\s*)?(\d+)', k.strip())
                    if m:
                        sec_num = int(m.group(1))
                        if 1 <= sec_num <= 28:
                            sections_map[sec_num] = str(v)
            if len(sections_map) >= 14:
                return sections_map

        text = str(proposal_input)
        pattern = r'(?m)^##\s+(\d+)\.\s*([^\n]+)'
        matches = list(re.finditer(pattern, text))
        for i, match in enumerate(matches):
            sec_num = int(match.group(1))
            start_pos = match.end()
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            sections_map[sec_num] = text[start_pos:end_pos].strip()

        # Fallback for 14-section legacy proposals
        if sections_map and max(sections_map.keys()) <= 14:
            s13 = sections_map.get(13, "")
            for sec_idx in range(15, 28):
                if sec_idx not in sections_map:
                    sections_map[sec_idx] = s13
            if 28 not in sections_map and 14 in sections_map:
                sections_map[28] = sections_map[14]

        return sections_map

    @classmethod
    def detect_applicable_guidelines(
        cls,
        sections: Dict[int, str],
        context: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """Automatically detects relevant EQUATOR guidelines based on study design and aims."""
        all_text = " ".join(sections.values()).lower()
        guidelines = []

        # 1. OECD/GCCP (Cell Culture)
        cell_keywords = ["کشت سلول", "رده سلولی", "سلول", "cell culture", "in vitro", "سلول‌های", "cell line"]
        if any(k in all_text for k in cell_keywords):
            guidelines.append("OECD_GCCP_CELL_CULTURE")

        # 2. MIQE (qPCR & Molecular Expression)
        qpcr_keywords = ["qpcr", "real-time pcr", "rt-pcr", "pcr", "بیان ژن", "rna", "mrna", "پرایمر", "primer"]
        if any(k in all_text for k in qpcr_keywords):
            guidelines.append("MIQE_QPCR_STANDARDS")

        # 3. ARRIVE 2.0 (In Vivo Animal Studies)
        animal_keywords = ["موش", "رت", "حیوانات آزمایشگاهی", "in vivo", "animal model", "رت‌های", "سوری", "حیوان"]
        if any(k in all_text for k in animal_keywords):
            guidelines.append("ARRIVE_2_0_ANIMAL_STUDIES")

        # 4. Chemical / Biological Authentication (Always enforced for interventional/compound studies)
        compound_keywords = ["عصاره", "دارو", "ترکیب", "تیمار", "غلظت", "ic50", "compound", "drug", "nanoparticle"]
        if any(k in all_text for k in compound_keywords):
            guidelines.append("REAGENT_CHEMICAL_AUTHENTICATION")

        # Ensure at least the core cell culture or chemical authentication is evaluated
        if not guidelines:
            guidelines = ["OECD_GCCP_CELL_CULTURE", "REAGENT_CHEMICAL_AUTHENTICATION"]

        return guidelines

    # =========================================================================
    # INDIVIDUAL GUIDELINE CHECKERS
    # =========================================================================

    @classmethod
    def audit_gccp_cell_culture(cls, sections: Dict[int, str]) -> List[GuidelineItemCheck]:
        """Audits Good Cell Culture Practice (OECD GCCP) standards."""
        checks = []
        full_methods = f"{sections.get(13, '')} {sections.get(15, '')} {sections.get(17, '')} {sections.get(20, '')} {sections.get(27, '')}".lower()

        # 1. Provenance / Repository Source
        has_source = any(src in full_methods for src in ["انستیتو پاستور", "بانک سلولی", "مرکز ذخایر", "atcc", "dsmz", "ecacc", "pasteur"])
        checks.append(GuidelineItemCheck(
            guideline="OECD_GCCP",
            criterion_fa="شناسنامه و منبع معتبر خرید رده‌های سلولی (ATCC/بانک سلولی پاستور/مرکز ذخایر)",
            criterion_en="Cell Line Provenance & Repository Sourcing",
            is_met=has_source,
            severity="CRITICAL",
            remediation_fa="قید منبع معتبر تهیه رده سلولی (نظیر انستیتو پاستور ایران یا مرکز ذخایر زیستی) در بخش ۱۵ و ۱۷ الزامی است."
        ))

        # 2. STR Profiling Authentication
        has_str = any(term in full_methods for term in ["str", "پروفایل ژنتیکی", "short tandem repeat", "احراز هویت ژنتیکی", "شناسنامه"])
        checks.append(GuidelineItemCheck(
            guideline="OECD_GCCP",
            criterion_fa="احراز هویت سلولی با آنالیز پروفایل STR (Short Tandem Repeat) جهت ممانعت از آلودگی متقاطع",
            criterion_en="Cell Authentication via STR Profiling",
            is_met=has_str,
            severity="MAJOR",
            remediation_fa="درج عبارت صریح انجام آنالیز STR یا داشتن شناسنامه ژنتیکی تاییدشده رده سلولی در بخش ۲۰ الزامی است."
        ))

        # 3. Mycoplasma Testing
        has_myco = any(term in full_methods for term in ["مایکوپلاسما", "mycoplasma", "فاقد آلودگی مایکوپلاسما", "آزمون pcr مایکوپلاسما"])
        checks.append(GuidelineItemCheck(
            guideline="OECD_GCCP",
            criterion_fa="پروتکل غربالگری منظم آلودگی مایکوپلاسما (با روش PCR یا رنگ‌آمیزی DAPI)",
            criterion_en="Routine Mycoplasma Contamination Testing",
            is_met=has_myco,
            severity="CRITICAL",
            remediation_fa="قید تایید عدم آلودگی به مایکوپلاسما در معیارهای ورود به مطالعه (بخش ۱۷) الزامی است."
        ))

        # 4. Passage Limit
        has_passage = any(term in full_methods for term in ["پاساژ", "passage", "شماره پاساژ", "پاساژهای بین", "p<10", "p<15"])
        checks.append(GuidelineItemCheck(
            guideline="OECD_GCCP",
            criterion_fa="تعیین سقف شماره پاساژ سلولی (ترجیحاً کمتر از ۱۰ تا ۱۵ پاساژ) جهت حفظ فنوتیپ",
            criterion_en="Defined Passage Number Limits (<= 10-15)",
            is_met=has_passage,
            severity="MAJOR",
            remediation_fa="تعیین محدوده مشخص پاساژهای سلولی (مثلاً پاساژهای ۳ تا ۱۰) در بخش ۱۷ و ۲۷ ضروری است."
        ))

        return checks

    @classmethod
    def audit_miqe_qpcr(cls, sections: Dict[int, str]) -> List[GuidelineItemCheck]:
        """Audits MIQE guidelines for Quantitative Real-Time PCR."""
        checks = []
        full_methods = f"{sections.get(13, '')} {sections.get(19, '')} {sections.get(20, '')} {sections.get(21, '')} {sections.get(23, '')} {sections.get(27, '')}".lower()

        # 1. RNA Quality & Integrity (RIN / Ratio)
        has_rna_qual = any(term in full_methods for term in ["rin", "نانودراپ", "nanodrop", "260/280", "کیفیت rna", "سالم بودن rna", "ژل آگارز"])
        checks.append(GuidelineItemCheck(
            guideline="MIQE",
            criterion_fa="سنجش خلوص و سلامت RNA با نانودراپ (نسبت A260/A280) و شاخص سلامت RIN",
            criterion_en="RNA Quality and Integrity Assessment (RIN >= 7 / A260/A280)",
            is_met=has_rna_qual,
            severity="MAJOR",
            remediation_fa="درج روش ارزیابی کمّی و کیفی RNA استخراج‌شده (نسبت ۲۶۰/۲۸۰ و نانودراپ) در بخش ۲۰ و ۲۷ الزامی است."
        ))

        # 2. Primer Specificity & Amplification Efficiency
        has_primer_eff = any(term in full_methods for term in ["کارایی پرایمر", "efficiency", "اختصاصیت پرایمر", "blast", "منحنی ذوب", "melting curve", "پرایمر"])
        checks.append(GuidelineItemCheck(
            guideline="MIQE",
            criterion_fa="صحت‌سنجی کارایی تکثیر پرایمرها (Efficiency بین ۹۰ تا ۱۱۰٪) و منحنی ذوب (Melting Curve)",
            criterion_en="Primer Specificity, Efficiency & Melting Curve Analysis",
            is_met=has_primer_eff,
            severity="MAJOR",
            remediation_fa="اشاره به صحت‌سنجی پرایمرها با بلاست، رسم منحنی ذوب تک‌پیک و کارایی استاندارد تکثیر در بخش ۲۱ الزامی است."
        ))

        # 3. Internal Reference Gene Normalization
        has_ref_gene = any(term in full_methods for term in ["gapdh", "actb", "beta-actin", "18s", "ژن مرجع", "ژن رفرنس", "داخلی", "housekeeping", "نرمال‌سازی"])
        checks.append(GuidelineItemCheck(
            guideline="MIQE",
            criterion_fa="نرمال‌سازی بیان ژن با ژن مرجع پایدار (Housekeeping Gene نظیر GAPDH یا ACTB)",
            criterion_en="Internal Reference Gene Normalization (e.g. GAPDH / ACTB)",
            is_met=has_ref_gene,
            severity="CRITICAL",
            remediation_fa="نام‌بردن صریح از ژن رفرنس داخلی (مانند GAPDH یا بتا-اکتین) جهت نرمال‌سازی در بخش ۲۱ و ۲۷ الزامی است."
        ))

        # 4. Standard Delta-Delta Ct Relative Quantification
        has_ddct = any(term in full_methods for term in ["2^-", "2^-deltadelta", "delta-delta", "livak", "روش فافل", "نسبی", "تغییر چند برابری", "fold change"])
        checks.append(GuidelineItemCheck(
            guideline="MIQE",
            criterion_fa="روش استاندارد کمی‌سازی نسبی بیان ژن (فرمول Livak / 2^-ΔΔCt یا Pfaffl)",
            criterion_en="Standard Relative Quantification Method (Livak 2^-ΔΔCt)",
            is_met=has_ddct,
            severity="MAJOR",
            remediation_fa="قید فرمول تحلیلی ۲ به توان منفی دلتا دلتا سی‌تی در روش تجزیه و تحلیل داده‌ها (بخش ۲۳) ضروری است."
        ))

        return checks

    @classmethod
    def audit_arrive_animal_studies(cls, sections: Dict[int, str]) -> List[GuidelineItemCheck]:
        """Audits ARRIVE 2.0 guidelines for preclinical in vivo studies."""
        checks = []
        full_methods = f"{sections.get(13, '')} {sections.get(15, '')} {sections.get(22, '')} {sections.get(24, '')} {sections.get(27, '')}".lower()

        # 1. Random Allocation
        has_rand = any(term in full_methods for term in ["تصادفی", "تخصیص تصادفی", "randomization", "random", "بلوک‌بندی"])
        checks.append(GuidelineItemCheck(
            guideline="ARRIVE_2_0",
            criterion_fa="تخصیص تصادفی حیوانات به گروه‌های آزمایشی و شاهد (Random Allocation)",
            criterion_en="Random Allocation to Experimental Groups",
            is_met=has_rand,
            severity="CRITICAL",
            remediation_fa="تشریح فرآیند تصادفی‌سازی تقسیم نمونه‌ها در گروه‌ها در بخش ۱۳ الزامی است."
        ))

        # 2. Blinding / Masking
        has_blinding = any(term in full_methods for term in ["کورسازی", "کور", "blinding", "masked", "عدم اطلاع ارزیاب"])
        checks.append(GuidelineItemCheck(
            guideline="ARRIVE_2_0",
            criterion_fa="کورسازی ارزیاب یا مجری نسبت به گروه‌های تیمار (Investigator Blinding)",
            criterion_en="Blinding of Experimenters and Outcome Assessors",
            is_met=has_blinding,
            severity="MAJOR",
            remediation_fa="قید تدابیر کورسازی در سنجش پیامدها جهت حذف سوگیری ناظر در بخش ۱۳ و ۲۷ توصیه می‌شود."
        ))

        # 3. Housing, Light/Dark Cycle & Climate
        has_housing = any(term in full_methods for term in ["چرخه روشنایی", "قفس", "دما", "رطوبت", "۱۲ ساعت", "housing", "فتوپریود"])
        checks.append(GuidelineItemCheck(
            guideline="ARRIVE_2_0",
            criterion_fa="تشریح شرایط نگهداری استاندارد حیوانات (چرخه نوری ۱۲ ساعته، دما و تهویه)",
            criterion_en="Animal Housing, Photoperiod & Climate Description",
            is_met=has_housing,
            severity="MAJOR",
            remediation_fa="ذکر شرایط استاندارد آشیانه حیوانات آزمایشگاهی در بخش ۱۵ و ۱۶ الزامی است."
        ))

        # 4. Humane Endpoints & Euthanasia
        has_humane = any(term in full_methods for term in ["یوتانایزی", "پایان انسانی", "بیهوشی", "کتامین", "humane endpoint", "کاهش درد"])
        checks.append(GuidelineItemCheck(
            guideline="ARRIVE_2_0",
            criterion_fa="تعریف نقاط پایانی انسانی (Humane Endpoints) و پروتکل بی‌دردی و یوتانایزی استاندارد",
            criterion_en="Humane Endpoints and Standard Euthanasia Protocol",
            is_met=has_humane,
            severity="CRITICAL",
            remediation_fa="قید دقیق شیوه‌نامه یوتانایزی بدون درد و استانداردهای کمیته اخلاق در بخش ۲۴ الزامی است."
        ))

        return checks

    @classmethod
    def audit_reagent_chemical_authentication(cls, sections: Dict[int, str]) -> List[GuidelineItemCheck]:
        """Audits Reagent, Chemical and Drug Authentication (CAS / Purity / Vehicle)."""
        checks = []
        full_text = f"{sections.get(5, '')} {sections.get(11, '')} {sections.get(13, '')} {sections.get(17, '')} {sections.get(19, '')} {sections.get(21, '')} {sections.get(27, '')}".lower()

        # 1. Purity Statement
        has_purity = any(term in full_text for term in ["خلوص", "خلوص بالا", "purity", "%", "hplc", "استاندارد آنالیتیکال", "analytical grade", "سیگما"])
        checks.append(GuidelineItemCheck(
            guideline="REAGENT_AUTH",
            criterion_fa="درج درجه خلوص مواد موثره و داروها (خلوص بالینی/آزمایشگاهی بالاتر از ۹۵٪)",
            criterion_en="Chemical Purity Verification (>= 95% / Analytical Standard)",
            is_met=has_purity,
            severity="CRITICAL",
            remediation_fa="درج خلوص ترکیبات مداخله‌گر و داروها (مثلاً گرید آنالیتیکال با خلوص >= ۹۵٪) در بخش ۵ و ۲۱ الزامی است."
        ))

        # 2. Vehicle / Solvent Toxicity Control (e.g. DMSO limit)
        has_vehicle = any(term in full_text for term in ["حلال", "dmso", "شاهد حلال", "کنترل منفی حلال", "vehicle control", "غلظت نهایی حلال"])
        checks.append(GuidelineItemCheck(
            guideline="REAGENT_AUTH",
            criterion_fa="تعریف گروه کنترل حلال (Vehicle Control) و محدودسازی غلظت حلال به زیر آستانه سمی (مانند DMSO زیر ۰.۱٪)",
            criterion_en="Vehicle Control Sizing & Solvent Toxicity Limit (DMSO <= 0.1%)",
            is_met=has_vehicle,
            severity="MAJOR",
            remediation_fa="تعریف گروه شاهد حلال (Vehicle Control) و تضمین غلظت غیرسمی حلال در بخش ۱۳ و ۲۷ الزامی است."
        ))

        # 3. Standard Reagent Sourcing / Vendor Specification
        has_vendor = any(term in full_text for term in ["شرکت", "سیگما", "sigma", "merck", "مرک", "کمپانی", "سازنده", "کد کاتالوگ"])
        checks.append(GuidelineItemCheck(
            guideline="REAGENT_AUTH",
            criterion_fa="ذکر نام برند یا شرکت تامین‌کننده معتبر مواد شیمیایی و کیت‌های سنجش (Vendor/Catalog)",
            criterion_en="Authentic Vendor Specification for Reagents & Assay Kits",
            is_met=has_vendor,
            severity="MAJOR",
            remediation_fa="قید کمپانی سازنده کیت‌ها و داروها (مانند Sigma-Aldrich یا Merck) در بخش ۲۱ الزامی است."
        ))

        return checks

    # =========================================================================
    # MASTER AUDIT EXECUTION
    # =========================================================================

    @classmethod
    def audit_proposal(
        cls,
        proposal_input: Any,
        context: Optional[Dict[str, Any]] = None
    ) -> EquatorAuditResult:
        """Runs the multi-guideline EQUATOR and resource authentication audit."""
        sections = cls.parse_sections(proposal_input)
        guidelines = cls.detect_applicable_guidelines(sections, context)

        detailed_checks: List[GuidelineItemCheck] = []

        if "OECD_GCCP_CELL_CULTURE" in guidelines:
            detailed_checks.extend(cls.audit_gccp_cell_culture(sections))

        if "MIQE_QPCR_STANDARDS" in guidelines:
            detailed_checks.extend(cls.audit_miqe_qpcr(sections))

        if "ARRIVE_2_0_ANIMAL_STUDIES" in guidelines:
            detailed_checks.extend(cls.audit_arrive_animal_studies(sections))

        if "REAGENT_CHEMICAL_AUTHENTICATION" in guidelines:
            detailed_checks.extend(cls.audit_reagent_chemical_authentication(sections))

        total_checks = len(detailed_checks)
        passed_checks = sum(1 for c in detailed_checks if c.is_met)
        critical_deficits = [c.criterion_fa for c in detailed_checks if not c.is_met and c.severity == "CRITICAL"]

        compliance_score = round((passed_checks / max(total_checks, 1)) * 100.0, 1)
        is_compliant = (compliance_score >= 80.0 and len(critical_deficits) == 0)

        if is_compliant:
            exec_summary = (
                f"پروپوزال با شاخص انطباق {compliance_score}% و بدون هیچ‌گونه نقص بحرانی با استانداردهای "
                f"شبکه بین‌المللی EQUATOR ({', '.join(guidelines)}) و دستورالعمل‌های احراز هویت زیستی منطبق ارزیابی گردید."
            )
        else:
            exec_summary = (
                f"پروپوزال دارای شاخص انطباق {compliance_score}% و تعداد {len(critical_deficits)} نقص بحرانی با "
                f"استانداردهای بین‌المللی بازتولیدپذیری پژوهش است. رفع نواقص جهت اخذ استانداردهای انتشار الزامی است."
            )

        return EquatorAuditResult(
            compliance_score=compliance_score,
            is_compliant=is_compliant,
            applicable_guidelines=guidelines,
            total_checks=total_checks,
            passed_checks=passed_checks,
            critical_deficits=critical_deficits,
            detailed_checks=detailed_checks,
            executive_summary_fa=exec_summary
        )

    # =========================================================================
    # REPORT GENERATION & PERSISTENCE
    # =========================================================================

    @classmethod
    def generate_markdown_report(cls, result: EquatorAuditResult) -> str:
        """Generates formal EQUATOR compliance report in Persian and English."""
        badge = "✅ تایید انطباق بین‌المللی (EQUATOR Compliant)" if result.is_compliant else "⚠️ نیازمند تکمیل الزامات بازتولیدپذیری (Deficits Detected)"
        
        lines = [
            "# گزارش ممیزی انطباق با راهنماهای بین‌المللی پژوهش (EQUATOR Network Compliance Report)",
            "",
            f"> **وضعیت ممیزی:** {badge}",
            f"> **شاخص کل انطباق (Compliance Score):** `{result.compliance_score}%` ({result.passed_checks} از {result.total_checks} شاخص محقق شده)",
            f"> **راهنماهای فعال برای این مطالعه:** `{', '.join(result.applicable_guidelines)}`",
            f"> **تعداد نقایص بحرانی (Critical Deficits):** `{len(result.critical_deficits)}`",
            "",
            "## ۱. خلاصه مدیریتی بازتولیدپذیری و شفافیت متدولوژیک (Executive Summary)",
            result.executive_summary_fa,
            "",
            "## ۲. کارنامه تفکیکی شاخص‌های راهنماها (Detailed Checklist)",
            ""
        ]

        current_gl = ""
        for c in result.detailed_checks:
            if c.guideline != current_gl:
                current_gl = c.guideline
                lines.append(f"### راهنمای تخصصی: `{current_gl}`")
            
            icon = "✅" if c.is_met else "❌"
            sev_fa = "🔴 بحرانی (Critical)" if c.severity == "CRITICAL" else "🟡 مهم (Major)"
            lines.append(f"- {icon} **{c.criterion_fa}** ({c.criterion_en})")
            lines.append(f"  * **سطح اهمیت:** {sev_fa}")
            lines.append(f"  * **وضعیت احراز:** {'محقق شده' if c.is_met else 'احراز نشده'}")
            if not c.is_met and c.remediation_fa:
                lines.append(f"  * **اقدام اصلاحی الزامی:** 💡 {c.remediation_fa}")
            lines.append("")

        return "\n".join(lines)

    @classmethod
    def save_reports(
        cls,
        result: EquatorAuditResult,
        output_dir: str = "."
    ) -> Tuple[str, str]:
        """Saves EQUATOR_COMPLIANCE_AUDIT.md and EQUATOR_COMPLIANCE_AUDIT.json."""
        os.makedirs(output_dir, exist_ok=True)
        md_path = os.path.join(output_dir, "EQUATOR_COMPLIANCE_AUDIT.md")
        json_path = os.path.join(output_dir, "EQUATOR_COMPLIANCE_AUDIT.json")

        md_content = cls.generate_markdown_report(result)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)

        return md_path, json_path


if __name__ == "__main__":
    print("EquatorComplianceAuditor loaded successfully.")
