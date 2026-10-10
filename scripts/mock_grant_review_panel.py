#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mock_grant_review_panel.py - Multi-Agent Mock Grant Study Section & Inter-Section Semantic Drift Gate
Proposal-Nevisi Engine v10.0 (Universal Biomedical Architecture)

Simulates an authentic academic grant review panel (Mock Study Section) based on
NIH / NIMAD / Pajooheshyar competitive grant scoring rubrics:
1. Reviewer 1 (Scientific Merit & Innovation):
   - Evaluates Problem Statement, Literature Review, Clinical Significance, and Hypotheses.
2. Reviewer 2 (Methodological Rigor, Inter-Section Drift & Biostatistics):
   - Evaluates Replicate Structure, Statistical Models, Sample Size, Controls, and
     enforces Inter-Section Semantic Drift (Aims <-> Variables <-> Assays alignment).
3. Reviewer 3 (Bioethics, Biosafety & Feasibility):
   - Evaluates Ethical codes, Biosafety protocols, Timeline/Gantt realism, and Study limitations.

Scoring Scale: 1.0 (Exceptional) to 9.0 (Poor).
Fundable Threshold: <= 3.5 overall score and zero critical flaws.
Generates MOCK_GRANT_REVIEW_REPORT.md and MOCK_GRANT_REVIEW_REPORT.json.

100% Domain-Agnostic: Zero hardcoded disease or chemical entities.
"""

import os
import re
import json
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple


@dataclass
class ReviewerScore:
    reviewer_id: str
    reviewer_title_fa: str
    reviewer_title_en: str
    domain: str
    score: float  # 1.0 (Exceptional) to 9.0 (Poor)
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    critical_flaws: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "reviewer_id": self.reviewer_id,
            "reviewer_title_fa": self.reviewer_title_fa,
            "reviewer_title_en": self.reviewer_title_en,
            "domain": self.domain,
            "score": round(self.score, 2),
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "critical_flaws": self.critical_flaws,
            "recommendations": self.recommendations
        }


@dataclass
class PanelReviewResult:
    overall_score: float
    funding_verdict: str  # "APPROVED_FUNDABLE" | "REVISION_REQUIRED" | "REJECTED_UNFUNDABLE"
    can_proceed: bool
    reviewer_evaluations: Dict[str, Any]
    inter_section_drift: Dict[str, Any]
    critical_flaws_count: int
    executive_summary_fa: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_score": round(self.overall_score, 2),
            "funding_verdict": self.funding_verdict,
            "can_proceed": self.can_proceed,
            "critical_flaws_count": self.critical_flaws_count,
            "executive_summary_fa": self.executive_summary_fa,
            "inter_section_drift": self.inter_section_drift,
            "reviewer_evaluations": self.reviewer_evaluations
        }


class MockGrantReviewPanel:
    """Multi-Agent Mock Grant Study Section and Scientific Rigor Evaluator."""

    SECTION_CANONICAL_NAMES = {
        1: "موضوع",
        2: "بیان مسئله",
        3: "مرور بر منابع",
        4: "اهمیت وضرورت تحقیق",
        5: "تعریف واژه ها",
        6: "اهداف جزیی",
        7: "اهداف کلی",
        8: "اهداف کاربردی",
        9: "فرضیات و سوالات",
        10: "دستاورد ها",
        11: "جدول متغیر ها",
        12: "جدول زمان بندی و مراحل اجرا",
        13: "روش اجرا",
        14: "نوع مطالعه",
        15: "جامعه مورد مطالعه",
        16: "محل انجام مطالعه",
        17: "معیار های ورود به مطالعه",
        18: "معیار های خروج از مطالعه",
        19: "ابزار های گردآوری اطلاعات",
        20: "تعیین اعتبار ابزار گردآوری",
        21: "تعیین ابزار گردآوری",
        22: "حجم نمونه و روش محاسبه آن",
        23: "روش تجزیه و تحلیل داده",
        24: "ملاحظلات اخلاقی در صورت نیاز",
        25: "نحوه رعایت نکات امنیتی و حفاظت پروژه در صورت نیاز",
        26: "مشکلات و محدودیت ها",
        27: "روش انجام طرح، شیوه اجرایی مراحل طرح و چگونگی جمع آوری اطلاعات",
        28: "منابعی که استفاده شد"
    }

    @classmethod
    def parse_proposal_sections(cls, proposal_input: Any) -> Dict[int, str]:
        """Parses a markdown string or dictionary into a normalized section map."""
        sections_map: Dict[int, str] = {}
        if isinstance(proposal_input, dict):
            # Already mapped by section number or title
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
            sec_body = text[start_pos:end_pos].strip()
            sections_map[sec_num] = sec_body

        # If 14-section proposal, map methodology subsections from Section 13
        if sections_map and max(sections_map.keys()) <= 14:
            s13_text = sections_map.get(13, "")
            for sec_idx in range(15, 28):
                if sec_idx not in sections_map:
                    sections_map[sec_idx] = s13_text
            if 28 not in sections_map and 14 in sections_map:
                sections_map[28] = sections_map[14]

        return sections_map

    # =========================================================================
    # REVIEWER 1: SCIENTIFIC MERIT & INNOVATION
    # =========================================================================

    @classmethod
    def evaluate_reviewer_1_scientific_merit(
        cls,
        sections: Dict[int, str],
        context: Optional[Dict[str, Any]] = None
    ) -> ReviewerScore:
        """Reviewer 1 evaluates Scientific Premise, Literature Synthesis, Innovation, and Hypotheses."""
        score = 1.5
        strengths = []
        weaknesses = []
        critical_flaws = []
        recommendations = []

        # Section 2: Problem Statement
        s2 = sections.get(2, "")
        if len(s2) >= 600:
            strengths.append("بیان مسئله تفصیلی و مستند به مبانی بیولوژیک و اپیدمیولوژیک تدوین شده است.")
        elif len(s2) >= 200:
            weaknesses.append("بیان مسئله نسبتاً کوتاه است و نیازمند تشریح عمیق‌تر شکاف دانش و فوریت علمی می‌باشد.")
            score += 0.8
        else:
            critical_flaws.append("بیان مسئله فاقد عمق علمی کافی است (کمتر از ۲۰۰ کاراکتر).")
            score += 2.0

        # Section 3: Literature Review
        s3 = sections.get(3, "")
        if len(s3) >= 800 and ("[" in s3 or "همکاران" in s3):
            strengths.append("مرور منابع غنی و ساختاریافته با استناد به مطالعات پیشین تنظیم شده است.")
        else:
            weaknesses.append("مرور منابع نیازمند تفکیک دقیق‌تر مطالعات و استنادات درون‌متنی مستقیم است.")
            score += 1.0

        # Section 4: Significance
        s4 = sections.get(4, "")
        if len(s4) >= 300:
            strengths.append("اهمیت و ضرورت پژوهش از جنبه‌های بالینی و راهبردی نظام سلامت به وضوح تبیین شده است.")
        else:
            weaknesses.append("ضرورت و اهمیت تحقیق به صورت کلی بیان شده و دلایل بالینی یا کاربردی شفاف‌تری می‌طلبد.")
            score += 0.5

        # Section 9: Hypotheses
        s9 = sections.get(9, "")
        if "فرضیه" in s9 or "آیا" in s9 or "هم‌افزایی" in s9 or "synerg" in s9.lower():
            strengths.append("فرضیات و سوالات پژوهش آزمون‌پذیر و متناظر با پرسش مرکزی طرح صورت‌بندی شده‌اند.")
        else:
            critical_flaws.append("بخش فرضیات فاقد گزاره‌های دقیق آزمون‌پذیر یا سوالات کمی پژوهش است.")
            score += 1.5

        if critical_flaws:
            recommendations.append("تقویت بیولوژیک بیان مسئله و شفاف‌سازی گزاره‌های فرضیه پیش از ارسال.")

        return ReviewerScore(
            reviewer_id="REVIEWER_1",
            reviewer_title_fa="داور اصالت علمی و نوآوری پژوهشی",
            reviewer_title_en="Scientific Merit, Premise & Innovation Reviewer",
            domain="SCIENTIFIC_MERIT_AND_INNOVATION",
            score=min(9.0, max(1.0, score)),
            strengths=strengths,
            weaknesses=weaknesses,
            critical_flaws=critical_flaws,
            recommendations=recommendations
        )

    # =========================================================================
    # REVIEWER 2: METHODOLOGY, INTER-SECTION DRIFT & BIOSTATISTICS
    # =========================================================================

    @classmethod
    def evaluate_inter_section_drift(cls, sections: Dict[int, str]) -> Dict[str, Any]:
        """Validates 1-to-1 bijection between Specific Aims (Sec 6), Variables (Sec 11), and Methods (Sec 13/27)."""
        aims_text = sections.get(6, "").lower()
        vars_text = sections.get(11, "").lower()
        methods_text = f"{sections.get(13, '')} {sections.get(27, '')}".lower()

        # Extract objective target domains
        DOMAIN_KEYWORDS = {
            "viability_cytotoxicity": ["زیست‌پذیری", "سمیت", "mtt", "زنده‌مانی", "cytotox", "viability", "ic50"],
            "apoptosis_cell_death": ["آپوپتوز", "مرگ سلولی", "کاسپاز", "caspase", "apoptosis", "annexin"],
            "migration_invasion": ["مهاجرت", "تهاجم", "خراش", "scratch", "wound", "migration", "invasion"],
            "synergy_combination": ["هم‌افزایی", "سینرژی", "چو", "تالالی", "ci", "synerg", "combination index"],
            "gene_protein_expression": ["بیان ژن", "پروتئین", "rt-pcr", "pcr", "western", "الایزا", "elisa", "expression"],
            "cell_cycle": ["چرخه سلولی", "cell cycle", "sub-g1", "فاز"]
        }

        detected_aims = []
        for domain, keywords in DOMAIN_KEYWORDS.items():
            if any(k in aims_text for k in keywords):
                detected_aims.append(domain)

        unaligned_aims_in_methods = []
        unaligned_aims_in_variables = []

        for aim in detected_aims:
            kws = DOMAIN_KEYWORDS[aim]
            # Check methods
            has_method = any(k in methods_text for k in kws)
            if not has_method:
                unaligned_aims_in_methods.append(aim)
            # Check variables
            has_variable = any(k in vars_text for k in kws)
            if not has_variable:
                unaligned_aims_in_variables.append(aim)

        drift_detected = (len(unaligned_aims_in_methods) > 0 or len(unaligned_aims_in_variables) > 0)
        
        return {
            "drift_detected": drift_detected,
            "detected_aim_domains": detected_aims,
            "unaligned_aims_in_methods": unaligned_aims_in_methods,
            "unaligned_aims_in_variables": unaligned_aims_in_variables,
            "alignment_score": round(1.0 - (len(unaligned_aims_in_methods) + len(unaligned_aims_in_variables)) / max(len(detected_aims) * 2, 1), 2)
        }

    @classmethod
    def evaluate_reviewer_2_methodology_and_alignment(
        cls,
        sections: Dict[int, str],
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[ReviewerScore, Dict[str, Any]]:
        """Reviewer 2 evaluates Study Design, Inter-Section Drift, Controls, Sample Size, and Biostatistics."""
        score = 1.4
        strengths = []
        weaknesses = []
        critical_flaws = []
        recommendations = []

        # 1. Inter-Section Drift Audit
        drift_res = cls.evaluate_inter_section_drift(sections)
        if drift_res["drift_detected"]:
            for u in drift_res["unaligned_aims_in_methods"]:
                critical_flaws.append(f"INTER_SECTION_DRIFT: هدف اختصاصی '{u}' در روش‌های اجرایی (بخش ۱۳ یا ۲۷) آزمون متناظر ندارد.")
                score += 1.2
            for u in drift_res["unaligned_aims_in_variables"]:
                weaknesses.append(f"INTER_SECTION_DRIFT: هدف اختصاصی '{u}' در جدول متغیرها (بخش ۱۱) فاقد متغیر تعریف‌شده است.")
                score += 0.6
        else:
            strengths.append("تناظر معنایی و یکپارچگی بین اهداف اختصاصی، جدول متغیرها و آزمون‌های آزمایشگاهی ۱۰۰٪ برقرار است.")

        # 2. Controls and Assay Interference (AssayInterferencePolicy)
        methods_text = f"{sections.get(13, '')} {sections.get(27, '')}".lower()
        if "کنترل" in methods_text or "control" in methods_text:
            strengths.append("طراحی کنترل‌های آزمایشگاهی متناسب در متدولوژی لحاظ شده است.")
        else:
            critical_flaws.append("گروه‌های کنترل منفی، حلال یا شاهد در روش اجرا به صورت صریح تعریف نشده‌اند.")
            score += 1.5

        # 3. Section 22: Sample Size
        s22 = sections.get(22, "")
        if ("n=" in s22.lower() or "تکرار" in s22 or "فرمول" in s22 or "توان" in s22) and len(s22) >= 200:
            strengths.append("روش محاسبه حجم نمونه با قید تکرارها و منطق بیومتینیک تشریح گردیده است.")
        else:
            weaknesses.append("بخش حجم نمونه نیازمند ارائه فرمول مشخص و تفکیک تکرارهای بیولوژیک و تکنیکال است.")
            score += 1.0

        # 4. Section 23: Statistical Analysis
        s23 = sections.get(23, "")
        if any(stat in s23.lower() for stat in ["anova", "t-test", "معناداری", "نرمال", "compusyn", "spss", "p-value", "p<"]):
            strengths.append("آزمون‌های آماری، سطح معناداری و نرم‌افزار تحلیلی به درستی تعیین شده‌اند.")
        else:
            critical_flaws.append("روش تجزیه و تحلیل داده فاقد نام آزمون آماری مشخص (مانند ANOVA یا آزمون ناپارامتری) است.")
            score += 1.5

        if critical_flaws:
            recommendations.append("برطرف‌سازی مغایرت‌های بین‌بخشی و تدوین صریح گروه‌های کنترل و آزمون آماری.")

        rev_score = ReviewerScore(
            reviewer_id="REVIEWER_2",
            reviewer_title_fa="داور روش‌شناسی، انطباق بین‌بخشی و بیواستاتیک",
            reviewer_title_en="Methodological Rigor, Inter-Section Drift & Biostatistics Reviewer",
            domain="METHODOLOGY_RIGOR_AND_ALIGNMENT",
            score=min(9.0, max(1.0, score)),
            strengths=strengths,
            weaknesses=weaknesses,
            critical_flaws=critical_flaws,
            recommendations=recommendations
        )
        return rev_score, drift_res

    # =========================================================================
    # REVIEWER 3: BIOETHICS, FEASIBILITY & RESOURCE MANAGEMENT
    # =========================================================================

    @classmethod
    def evaluate_reviewer_3_bioethics_and_feasibility(
        cls,
        sections: Dict[int, str],
        context: Optional[Dict[str, Any]] = None
    ) -> ReviewerScore:
        """Reviewer 3 evaluates Ethical Codes, Biosafety, Feasibility, Schedule and Limitations."""
        score = 1.3
        strengths = []
        weaknesses = []
        critical_flaws = []
        recommendations = []

        # Section 24: Bioethics
        s24 = sections.get(24, "")
        if len(s24) >= 150 and any(eth in s24 for eth in ["اخلاق", "کد", "هلسینکی", "رضایت", "پژوهش", "کمیته", "حیوانات", "پسماند"]):
            strengths.append("ملاحظات اخلاقی متناسب با نوع مطالعه تدوین شده و تعهد به رعایت کدهای اخلاق زیستی قید گردیده است.")
        else:
            weaknesses.append("ملاحظات اخلاقی مختصر است؛ اشاره به اصول کدهای ۳۱ گانه اخلاق زیستی کشور توصیه می‌شود.")
            score += 0.8

        # Section 25: Biosafety & Security
        s25 = sections.get(25, "")
        if len(s25) >= 150:
            strengths.append("نکات ایمنی زیستی، مهار آلودگی و حفاظت فردی و محیطی به درستی مورد توجه قرار گرفته است.")
        else:
            weaknesses.append("پروتکل‌های ایمنی زیستی (Biosafety) و امحای پسماندهای بیولوژیک نیازمند تفصیل بیشتر است.")
            score += 0.5

        # Section 12: Gantt Chart & Schedule
        s12 = sections.get(12, "")
        if "|" in s12 or "ماه" in s12 or "فاز" in s12:
            strengths.append("جدول زمان‌بندی و گانت چارت اجرایی با تفکیک فازهای پژوهش ارائه شده است.")
        else:
            weaknesses.append("جدول زمان‌بندی فاقد فازبندی زمانی مشخص در قالب جدول مدون است.")
            score += 0.7

        # Section 26: Limitations
        s26 = sections.get(26, "")
        if len(s26) >= 100:
            strengths.append("محدودیت‌های فنی و اجرایی پژوهش به صورت واقع‌بینانه فهرست شده‌اند.")
        else:
            weaknesses.append("محدودیت‌های احتمالی پژوهش و راهکارهای مهار آن ذکر نشده است.")
            score += 0.5

        if critical_flaws:
            recommendations.append("افزایش استانداردهای ایمنی زیستی و مستندسازی تعهدات اخلاق پژوهش.")

        return ReviewerScore(
            reviewer_id="REVIEWER_3",
            reviewer_title_fa="داور اخلاق زیستی، ایمنی و امکان‌پذیری اجرایی",
            reviewer_title_en="Bioethics, Biosafety & Feasibility Reviewer",
            domain="BIOETHICS_SAFETY_AND_FEASIBILITY",
            score=min(9.0, max(1.0, score)),
            strengths=strengths,
            weaknesses=weaknesses,
            critical_flaws=critical_flaws,
            recommendations=recommendations
        )

    # =========================================================================
    # MASTER PANEL CONDUCT & SCORING
    # =========================================================================

    @classmethod
    def conduct_panel_review(
        cls,
        proposal_input: Any,
        proposal_context: Optional[Dict[str, Any]] = None
    ) -> PanelReviewResult:
        """Conducts full Mock Study Section review across the 3 specialist reviewer agents."""
        sections = cls.parse_proposal_sections(proposal_input)

        r1 = cls.evaluate_reviewer_1_scientific_merit(sections, proposal_context)
        r2, drift_res = cls.evaluate_reviewer_2_methodology_and_alignment(sections, proposal_context)
        r3 = cls.evaluate_reviewer_3_bioethics_and_feasibility(sections, proposal_context)

        all_critical_flaws = r1.critical_flaws + r2.critical_flaws + r3.critical_flaws
        crit_count = len(all_critical_flaws)

        # Calculate overall score (1.0 to 9.0)
        overall_score = round((r1.score + r2.score + r3.score) / 3.0, 2)

        # Funding Verdict
        if overall_score <= 3.5 and crit_count == 0:
            funding_verdict = "APPROVED_FUNDABLE"
            can_proceed = True
            exec_summary = (
                f"پروپوزال با نمره میانگین داوری {overall_score} از ۹.۰ (رتبه استثنایی و ممتاز) و بدون هیچ‌گونه نقص بحرانی "
                f"توسط هیئت داوری شبیه‌سازی‌شده (Mock Study Section) در اولویت تصویب و اعطای گرنت (Fundable) ارزیابی گردید."
            )
        elif overall_score <= 6.0 or crit_count > 0:
            funding_verdict = "REVISION_REQUIRED"
            can_proceed = False
            exec_summary = (
                f"پروپوزال با نمره داوری {overall_score} از ۹.۰ و تعداد {crit_count} نقص بحرانی در وضعیت نیاز به اصلاح اساسی "
                f"(Revision Required) قرار گرفت. پیش از تصویب و ارسال نهایی، اعمال توصیه‌های اصلاحی هیئت داوری الزامی است."
            )
        else:
            funding_verdict = "REJECTED_UNFUNDABLE"
            can_proceed = False
            exec_summary = (
                f"پروپوزال با نمره داوری {overall_score} از ۹.۰ و نقایص ساختاری اساسی، حائز شرایط تصویب تشخیص داده نشد "
                f"و نیازمند بازطراحی بنیادی متدولوژی و اهداف می‌باشد."
            )

        evaluations = {
            "REVIEWER_1": r1.to_dict(),
            "REVIEWER_2": r2.to_dict(),
            "REVIEWER_3": r3.to_dict()
        }

        return PanelReviewResult(
            overall_score=overall_score,
            funding_verdict=funding_verdict,
            can_proceed=can_proceed,
            reviewer_evaluations=evaluations,
            inter_section_drift=drift_res,
            critical_flaws_count=crit_count,
            executive_summary_fa=exec_summary
        )

    # =========================================================================
    # REPORT GENERATION & PERSISTENCE
    # =========================================================================

    @classmethod
    def generate_markdown_report(cls, result: PanelReviewResult) -> str:
        """Generates formal Markdown report suitable for researchers and review committees."""
        verdict_badge = {
            "APPROVED_FUNDABLE": "✅ تصویب با اولویت ممتاز (Fundable / Approved)",
            "REVISION_REQUIRED": "⚠️ نیازمند بازنگری و اصلاحات (Revision Required)",
            "REJECTED_UNFUNDABLE": "❌ عدم احراز شرایط داوری (Unfundable / Rejected)"
        }.get(result.funding_verdict, result.funding_verdict)

        lines = [
            "# کارنامه رسمی داوری گرنت و ممیزی پروپوزال (Mock Grant Review Summary Report)",
            "",
            f"> **وضعیت ارزیابی هیئت داوران:** {verdict_badge}",
            f"> **نمره نهایی داوری (مقیاس ۱ تا ۹):** `{result.overall_score} / 9.0` (نمره ۱ ممتاز - نمره ۹ ضعیف)",
            f"> **تعداد نقایص بحرانی (Critical Flaws):** `{result.critical_flaws_count}`",
            "",
            "## ۱. خلاصه مدیریتی ارزیابی هیئت داوران (Executive Summary)",
            result.executive_summary_fa,
            "",
            "## ۲. پایش انطباق معنایی بین‌بخشی (Inter-Section Semantic Drift)",
            f"- **وضعیت انطباق:** {'⚠️ انحراف شناسایی شد' if result.inter_section_drift.get('drift_detected') else '✅ ۱۰۰٪ منطبق بدون انحراف'}",
            f"- **شاخص هماهنگی اهداف با متدها:** `{result.inter_section_drift.get('alignment_score', 1.0) * 100}%`",
            f"- **حوزه‌های هدف شناسایی‌شده:** `{result.inter_section_drift.get('detected_aim_domains', [])}`",
        ]

        if result.inter_section_drift.get("unaligned_aims_in_methods"):
            lines.append(f"- **اهداف فاقد آزمون در متدولوژی:** `{result.inter_section_drift['unaligned_aims_in_methods']}`")
        if result.inter_section_drift.get("unaligned_aims_in_variables"):
            lines.append(f"- **اهداف فاقد متغیر در جدول متغیرها:** `{result.inter_section_drift['unaligned_aims_in_variables']}`")

        lines.extend([
            "",
            "## ۳. ارزیابی تفکیکی داوران تخصصی (Individual Reviewer Critiques)",
            ""
        ])

        for r_key, r_eval in result.reviewer_evaluations.items():
            lines.extend([
                f"### {r_eval['reviewer_title_fa']} ({r_eval['reviewer_title_en']})",
                f"- **نمره داوری این حوزه:** `{r_eval['score']} / 9.0`",
                "- **نقاط قوت (Strengths):**"
            ])
            for st in r_eval["strengths"]:
                lines.append(f"  * {st}")
            
            if r_eval["weaknesses"]:
                lines.append("- **نقاط ضعف (Weaknesses):**")
                for w in r_eval["weaknesses"]:
                    lines.append(f"  * {w}")

            if r_eval["critical_flaws"]:
                lines.append("- **نقایص بحرانی (Critical Flaws):**")
                for cf in r_eval["critical_flaws"]:
                    lines.append(f"  * 🔴 {cf}")

            if r_eval["recommendations"]:
                lines.append("- **توصیه‌های اصلاحی (Recommendations):**")
                for rec in r_eval["recommendations"]:
                    lines.append(f"  * 💡 {rec}")
            
            lines.append("")

        return "\n".join(lines)

    @classmethod
    def save_reports(
        cls,
        result: PanelReviewResult,
        output_dir: str = "."
    ) -> Tuple[str, str]:
        """Saves MOCK_GRANT_REVIEW_REPORT.md and MOCK_GRANT_REVIEW_REPORT.json."""
        os.makedirs(output_dir, exist_ok=True)
        md_path = os.path.join(output_dir, "MOCK_GRANT_REVIEW_REPORT.md")
        json_path = os.path.join(output_dir, "MOCK_GRANT_REVIEW_REPORT.json")

        md_content = cls.generate_markdown_report(result)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)

        return md_path, json_path


if __name__ == "__main__":
    print("MockGrantReviewPanel loaded successfully.")
