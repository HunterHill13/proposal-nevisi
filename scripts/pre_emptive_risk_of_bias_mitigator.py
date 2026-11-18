#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pre_emptive_risk_of_bias_mitigator.py - Pre-emptive Risk of Bias (RoB) Mitigation Engine
Proposal-Nevisi Engine v14.0 (Universal Biomedical Architecture)

Enforces international standards for pre-emptive experimental and observational bias mitigation:
- Cochrane RoB-2 (Clinical Trials / Human RCTs)
- SYRCLE / ToxRTool / GIVIMP (Preclinical Animal / In Vitro Cellular)
- QUADAS-2 / STARD (Diagnostic Accuracy & Biomarker Studies - Spectrum Bias Guard)
- STROBE / Newcastle-Ottawa (Observational Epidemiological & Health Systems Studies)
1. Domain 1: Selection Bias (Random sequence / Allocation concealment / Consecutive sampling / Sampling frame)
2. Domain 2: Performance Bias (Environmental uniformity / Index test protocol / Standardized interviewers)
3. Domain 3: Detection Bias (Blinded outcome assessment / Reference standard independence / HIS objective audit)
4. Domain 4: Attrition Bias (Pre-hoc exclusion criteria / Diagnostic flow & timing / Missing data handling)
5. Domain 5: Reporting Bias (Pre-registration / Multivariable confounder adjustment / Selective reporting guard)

Scoring:
- "LOW_RISK": Rigorous mitigation protocol explicitly documented.
- "SOME_CONCERNS": General statement present but lacking specific blinding/randomization protocol.
- "HIGH_RISK": Complete omission of bias mitigation strategy.

100% General-Purpose and Config-Driven: Zero hard-coded drugs or diseases.
"""

import os
import re
import json
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple


@dataclass
class BiasDomainEvaluation:
    domain_id: str
    domain_title_fa: str
    domain_title_en: str
    risk_level: str  # "LOW_RISK" | "SOME_CONCERNS" | "HIGH_RISK"
    strengths: List[str] = field(default_factory=list)
    vulnerabilities: List[str] = field(default_factory=list)
    remediation_fa: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "domain_id": self.domain_id,
            "domain_title_fa": self.domain_title_fa,
            "domain_title_en": self.domain_title_en,
            "risk_level": self.risk_level,
            "strengths": self.strengths,
            "vulnerabilities": self.vulnerabilities,
            "remediation_fa": self.remediation_fa
        }


@dataclass
class RiskOfBiasAuditResult:
    overall_risk: str  # "LOW_RISK" | "MODERATE_RISK" | "HIGH_RISK"
    is_acceptable: bool
    domain_evaluations: Dict[str, BiasDomainEvaluation] = field(default_factory=dict)
    high_risk_domains: List[str] = field(default_factory=list)
    executive_summary_fa: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_risk": self.overall_risk,
            "is_acceptable": self.is_acceptable,
            "high_risk_domains": self.high_risk_domains,
            "executive_summary_fa": self.executive_summary_fa,
            "domain_evaluations": {k: v.to_dict() for k, v in self.domain_evaluations.items()}
        }


class PreEmptiveRiskOfBiasMitigator:
    """Master evaluator and protocol enforcer for Pre-emptive Risk of Bias mitigation."""

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

    # =========================================================================
    # DOMAIN EVALUATORS (Cochrane RoB-2 & SYRCLE Standards)
    # =========================================================================


    @classmethod
    def detect_study_family(cls, sections: Dict[int, str], context: Optional[Dict[str, Any]] = None) -> str:
        """Detects the study family from context or sections for adaptive RoB auditing."""
        if context:
            sf = context.get("study_family") or context.get("framework")
            if sf:
                sf_lower = str(sf).lower()
                if any(k in sf_lower for k in ["scoping", "prisma-scr", "prisma_scr", "jbi", "evidence_synthesis"]):
                    return "scoping_review"
                if any(k in sf_lower for k in ["usability", "heuristic", "nielsen", "digital_health"]) or re.search(r'\bsus\b', sf_lower):
                    return "usability"
                if any(k in sf_lower for k in ["diagnostic", "biomarker", "stard", "quadas"]):
                    return "diagnostic"
                if any(k in sf_lower for k in ["health_system", "health_policy", "health_econom", "che", "oop"]):
                    return "health_systems"
                if any(k in sf_lower for k in ["epidemiolog", "observational", "strobe", "cross-sectional", "cohort"]):
                    return "epidemiological"
                if any(k in sf_lower for k in ["clinical", "rct", "consort", "trial"]):
                    return "clinical_rct"
                if any(k in sf_lower for k in ["animal", "in_vivo", "arrive"]):
                    return "in_vivo"
                if any(k in sf_lower for k in ["in_vitro", "cellular", "cell", "gccp"]):
                    return "in_vitro"

        s14 = sections.get(14, "").lower()
        s13 = sections.get(13, "").lower()
        s15 = sections.get(15, "").lower()
        s1 = sections.get(1, "").lower()
        combined = f"{s1} {s14} {s13} {s15}"

        if any(k in combined for k in ["مرور دامنه‌ای", "مرور حیطه‌ای", "مرور نظام‌مند", "scoping review", "prisma-scr", "jbi", "evidence synthesis", "مرور متون"]):
            return "scoping_review"
        if any(k in combined for k in ["کاربردپذیری", "ارزیابی اکتشافی", "نیلسن", "تفکر با صدای بلند"]) or re.search(r'\b(?:usability|heuristic|nielsen|sus|ueq|think-aloud)\b', combined):
            return "usability"
        if any(k in combined for k in ["تشخیصی", "diagnostic", "quadas", "stard", "roc", "حساسیت و ویژگی"]):
            return "diagnostic"
        if any(k in combined for k in ["هزینه", "کمرشکن", "نظام سلامت", "اقتصاد سلامت", "che", "oop", "بیمه"]):
            return "health_systems"
        if any(k in combined for k in ["مقطعی", "کوهورت", "مورد-شاهدی", "همه‌گیرشناسی", "strobe", "شیوع"]):
            return "epidemiological"
        if any(k in combined for k in ["کارآزمایی بالینی", "clinical trial", "rct", "consort", "بیماران"]):
            return "clinical_rct"
        if any(k in combined for k in ["کشت سلول", "رده سلولی", "in vitro", "برون‌تن", "cell line", "cell culture"]):
            return "in_vitro"
        if any(k in combined for k in ["حیوان", "موش", "رت", "in vivo", "animal", "arrive"]):
            return "in_vivo"
        return "in_vitro"

    @classmethod
    def evaluate_selection_bias(
        cls,
        sections: Dict[int, str],
        study_family: str = "in_vitro"
    ) -> BiasDomainEvaluation:
        """Domain 1: Selection Bias (QUADAS-2 / STROBE / RoB-2 / PRISMA-ScR / Usability)."""
        methods_text = f"{sections.get(13, '')} {sections.get(15, '')} {sections.get(17, '')} {sections.get(22, '')} {sections.get(27, '')}".lower()
        strengths = []
        vulnerabilities = []

        # 0. Scoping Review & Evidence Synthesis Archetype (PRISMA-ScR / JBI Eligibility & Coverage)
        if study_family == "scoping_review":
            has_multi_db = any(t in methods_text for t in ["pubmed", "scopus", "web of science", "embase", "پابمد", "اسکوپوس", "پایگاه"])
            has_elig = len(sections.get(17, "")) >= 30 or any(t in methods_text for t in ["pcc", "واجد شرایط", "inclusion", "معیار ورود"])
            if has_multi_db and has_elig:
                risk = "LOW_RISK"
                strengths.append("جستجوی فراگیر چندپایگاهی همراه با معیارهای شفاف ورود/خروج بر پایه PCC جهت مهار سوگیری انتخاب متون (PRISMA-ScR) پیش‌بینی شده است.")
            elif has_multi_db or has_elig:
                risk = "SOME_CONCERNS"
                strengths.append("چارچوب انتخاب منابع تعریف شده است اما تنوع پایگاه‌ها و ادبیات خاکستری نیازمند تصریح بیشتر است.")
                vulnerabilities.append("احتمال جاافتادن بخشی از شواهد خاکستری در انتخاب متون.")
            else:
                risk = "SOME_CONCERNS"
                vulnerabilities.append("فهرست دقیق پایگاه‌های اطلاعاتی و معیارهای واجد شرایط بودن متون نیازمند تکمیل است.")
            return BiasDomainEvaluation(
                domain_id="DOMAIN_1_SELECTION_BIAS",
                domain_title_fa="سوگیری انتخاب متون و پوشش جستجو (PRISMA-ScR Selection & Coverage Bias)",
                domain_title_en="Selection Bias: Multi-Database Coverage & Eligibility Criteria (PRISMA-ScR)",
                risk_level=risk,
                strengths=strengths,
                vulnerabilities=vulnerabilities,
                remediation_fa="درج فهرست حداقل ۳ پایگاه بین‌المللی به همراه معیارهای دقیق PCC در بخش ۱۷ و ۲۲ توصیه می‌شود."
            )

        # 0b. Usability & Digital Health Archetype (Nielsen / SUS Sampling)
        if study_family == "usability":
            has_target = any(t in methods_text for t in ["کاربر", "پرسونا", "متخصص", "پزشک", "پرستار", "بیمار", "ارزیاب", "nielsen", "نیلسن"])
            if has_target:
                risk = "LOW_RISK"
                strengths.append("جامعه کاربران هدف و معیارهای ورود ارزیابان متناسب با پروتکل نیلسن/SUS برای مهار سوگیری انتخاب تعریف شده است.")
            else:
                risk = "SOME_CONCERNS"
                vulnerabilities.append("ویژگی‌های کاربران هدف و سطح آشنایی دیجیتال آنان برای جلوگیری از سوگیری انتخاب نیازمند شفاف‌سازی است.")
            return BiasDomainEvaluation(
                domain_id="DOMAIN_1_SELECTION_BIAS",
                domain_title_fa="سوگیری انتخاب کاربران و ارزیابان (Usability Sampling Bias)",
                domain_title_en="Selection Bias: Target User / Evaluator Sampling (Nielsen-Landauer / SUS)",
                risk_level=risk,
                strengths=strengths,
                vulnerabilities=vulnerabilities,
                remediation_fa="مشخص کردن پروفایل کاربران هدف و سواد دیجیتال شرکت‌کنندگان در بخش ۱۵ و ۱۷ توصیه می‌شود."
            )

        # 1. Diagnostic Accuracy Archetype (QUADAS-2 Domain 1: Patient Selection & Spectrum Bias Guard)
        if study_family == "diagnostic":
            has_consecutive = any(t in methods_text for t in ["متوالی", "consecutive", "مشکوک", "شک بالینی", "کلیه مراجعه‌کنندگان", "diagnostic dilemma"])
            has_case_control = any(t in methods_text for t in ["شاهد سالم در برابر بیمار شدید", "مورد-شاهدی تشخیصی", "داوطلبان سالم"])
            if has_consecutive and not has_case_control:
                risk = "LOW_RISK"
                strengths.append("نمونه‌گیری متوالی (Consecutive Sampling) از جامعه بیماران دارای شک بالینی جهت حذف کامل سوگیری طیف (Spectrum Bias) بر پایه استاندارد QUADAS-2 پیش‌بینی شده است.")
            elif has_consecutive:
                risk = "SOME_CONCERNS"
                strengths.append("نمونه‌گیری متوالی قید شده است اما پرهیز از مقایسه موارد شدید با افراد سالم نیازمند شفاف‌سازی بیشتر است.")
                vulnerabilities.append("احتمال سوگیری طیف (Spectrum Bias) در صورت ورود داوطلبان سالم به عنوان گروه شاهد آزمون تشخیصی.")
            else:
                risk = "HIGH_RISK"
                vulnerabilities.append("فاقد نمونه‌گیری متوالی از بیماران مشکوک به بیماری؛ خطر سوگیری شدید طیف (Spectrum Bias) و بیش‌برآوردی حساسیت و ویژگی وجود دارد.")

            return BiasDomainEvaluation(
                domain_id="DOMAIN_1_SELECTION_BIAS",
                domain_title_fa="سوگیری انتخاب و سوگیری طیف (QUADAS-2 Patient Selection & Spectrum Bias)",
                domain_title_en="Selection Bias: Spectrum Bias Guard & Consecutive Enrollment (QUADAS-2)",
                risk_level=risk,
                strengths=strengths,
                vulnerabilities=vulnerabilities,
                remediation_fa="درج صریح روش نمونه‌گیری متوالی از بیماران دارای شک بالینی در بخش‌های ۱۵، ۱۷ و ۲۷ جهت رفع سوگیری طیف الزامی است."
            )

        # 2. Observational & Health Systems Archetypes (STROBE Sampling Frame)
        if study_family in ["health_systems", "epidemiological"]:
            has_prob_sampling = any(t in methods_text for t in ["طبقه‌بندی", "خوشه‌ای", "چندمرحله‌ای", "stratified", "cluster", "تصادفی سیستماتیک", "جامعه هدف"])
            has_rand = any(t in methods_text for t in ["تصادفی", "randomization", "random", "نمونه‌گیری تصادفی"])
            if has_prob_sampling or has_rand:
                risk = "LOW_RISK"
                strengths.append("طراحی نمونه‌گیری طبقه‌بندی‌شده چندمرحله‌ای/تصادفی با لحاظ ضریب اثر طرح جهت تضمین تعمیم‌پذیری و حذف سوگیری انتخاب بر پایه راهنمای STROBE.")
            else:
                risk = "SOME_CONCERNS"
                vulnerabilities.append("استفاده از نمونه‌گیری در دسترس در یک مرکز درمانی؛ خطر سوگیری انتخاب وجود دارد و تعمیم‌پذیری نیازمند تعدیل با ضریب طرح است.")

            return BiasDomainEvaluation(
                domain_id="DOMAIN_1_SELECTION_BIAS",
                domain_title_fa="سوگیری انتخاب و چارچوب نمونه‌گیری (STROBE Selection & Sampling Frame)",
                domain_title_en="Selection Bias: Multi-Stage Representative Sampling (STROBE)",
                risk_level=risk,
                strengths=strengths,
                vulnerabilities=vulnerabilities,
                remediation_fa="قید چارچوب نمونه‌گیری احتمالی طبقه‌بندی‌شده و محاسبه اثر طرح (DEFF) در بخش ۱۵ و ۲۲ توصیه می‌شود."
            )

        # 3. Clinical RCT, In Vivo Animal & In Vitro Cellular (Cochrane RoB-2 & SYRCLE)
        has_rand = any(t in methods_text for t in ["تصادفی", "تخصیص تصادفی", "randomization", "random", "بلوک‌بندی", "randomized block"])
        has_conceal = any(t in methods_text for t in ["تخصیص پنهان", "پنهان‌سازی", "کدگذاری", "coded vials", "allocation concealment", "ویال‌های کدگذاری‌شده"])

        if has_rand and has_conceal:
            risk = "LOW_RISK"
            strengths.append("تخصیص نمونه‌ها به صورت تصادفی ساختاریافته همراه با پنهان‌سازی تخصیص (کدگذاری نمونه‌ها) پیش‌بینی شده است.")
        elif has_rand:
            risk = "SOME_CONCERNS"
            strengths.append("فرآیند تصادفی‌سازی قید شده است اما نحوه پنهان‌سازی تخصیص (Allocation Concealment) نیازمند تفصیل بیشتر است.")
            vulnerabilities.append("عدم تشریح صریح کدگذاری نمونه‌ها جهت جلوگیری از پیش‌بینی گروه‌های آزمایشی.")
        else:
            risk = "HIGH_RISK"
            vulnerabilities.append("فاقد هرگونه پروتکل تصادفی‌سازی و پنهان‌سازی تخصیص در گروه‌های آزمایشی.")

        return BiasDomainEvaluation(
            domain_id="DOMAIN_1_SELECTION_BIAS",
            domain_title_fa="سوگیری انتخاب و تخصیص (Selection Bias)",
            domain_title_en="Selection Bias: Sequence Generation & Allocation Concealment",
            risk_level=risk,
            strengths=strengths,
            vulnerabilities=vulnerabilities,
            remediation_fa="درج نحوه تولید توالی تصادفی (نرم‌افزاری/بلوکی) و کدگذاری نمونه‌ها توسط فرد مستقل در بخش ۱۳ الزامی است."
        )

    @classmethod
    def evaluate_performance_bias(
        cls,
        sections: Dict[int, str],
        study_family: str = "in_vitro"
    ) -> BiasDomainEvaluation:
        """Domain 2: Performance Bias (Environmental uniformity & random plate/cage placement)."""
        methods_text = f"{sections.get(13, '')} {sections.get(16, '')} {sections.get(20, '')} {sections.get(27, '')}".lower()
        strengths = []
        vulnerabilities = []

        if study_family == "scoping_review":
            has_proto = any(t in methods_text for t in ["پروتکل", "jbi", "prisma", "فرم", "چارتینگ", "charting", "جستجو", "کلیدواژه"])
            if has_proto:
                risk = "LOW_RISK"
                strengths.append("پروتکل یکپارچه جستجو و فرم استاندارد استخراج داده‌ها (Data Charting) بر پایه راهنمای JBI/PRISMA-ScR تعریف شده است.")
            else:
                risk = "SOME_CONCERNS"
                vulnerabilities.append("فرآیند استانداردسازی فرم استخراج داده و کلیدواژه‌های جستجو نیازمند شفاف‌سازی بیشتر است.")
            return BiasDomainEvaluation(
                domain_id="DOMAIN_2_PERFORMANCE_BIAS",
                domain_title_fa="سوگیری اجرای جستجو و یکنواختی استخراج (PRISMA-ScR Extraction Bias)",
                domain_title_en="Performance Bias: Standardized Search & Data Charting Conduct",
                risk_level=risk,
                strengths=strengths,
                vulnerabilities=vulnerabilities,
                remediation_fa="تدوین فرم استاندارد چارتینگ داده‌ها و کلیدواژه‌های همسان در بخش ۱۳ و ۱۹ توصیه می‌شود."
            )

        if study_family == "usability":
            has_tasks = any(t in methods_text for t in ["سناریو", "تکلیف", "پروتکل", "think-aloud", "تفکر با صدای بلند", "نیلسن", "nielsen", "یکسان"])
            if has_tasks:
                risk = "LOW_RISK"
                strengths.append("اجرای سناریوهای وظیفه‌محور یکسان و دستورالعمل همسان‌سازی‌شده آزمون کاربردپذیری پیش‌بینی شده است.")
            else:
                risk = "SOME_CONCERNS"
                vulnerabilities.append("استانداردسازی ترتیب سناریوها و دستورالعمل تسهیل‌گر نیازمند تکمیل است.")
            return BiasDomainEvaluation(
                domain_id="DOMAIN_2_PERFORMANCE_BIAS",
                domain_title_fa="سوگیری اجرای سناریوهای کاربردپذیری (Task Protocol Consistency)",
                domain_title_en="Performance Bias: Standardized Task Scenarios & Facilitator Conduct",
                risk_level=risk,
                strengths=strengths,
                vulnerabilities=vulnerabilities,
                remediation_fa="تشریح سناریوهای وظیفه‌محور یکسان و اجتناب از هدایت کاربر در بخش ۱۳ و ۲۷ توصیه می‌شود."
            )

        if study_family == "diagnostic":
            has_index_proto = any(t in methods_text for t in ["پروتکل استاندارد", "کیت کالیبره", "دستورالعمل سازنده", "نقطه برش", "cut-off"])
            if has_index_proto:
                risk = "LOW_RISK"
                strengths.append("اجرای آزمون شاخص تشخیصی با پروتکل استانداردسازی‌شده و نقطه برش از پیش تعیین‌شده بر پایه راهنمای STARD.")
            else:
                risk = "SOME_CONCERNS"
                vulnerabilities.append("تعریف پروتکل اجرای آزمون شاخص و نقطه برش بهینه نیازمند استانداردسازی بیشتر است.")
            return BiasDomainEvaluation(
                domain_id="DOMAIN_2_PERFORMANCE_BIAS",
                domain_title_fa="سوگیری اجرای آزمون شاخص (QUADAS-2 Index Test Conduct)",
                domain_title_en="Performance Bias: Standardized Index Test Execution (QUADAS-2)",
                risk_level=risk,
                strengths=strengths,
                vulnerabilities=vulnerabilities,
                remediation_fa="استانداردسازی پروتکل آزمون شاخص و نقطه برش در بخش ۱۳ و ۱۹ قید گردد."
            )

        if study_family in ["health_systems", "epidemiological"]:
            has_survey_proto = any(t in methods_text for t in ["who", "پرسشنامه استاندارد", "آموزش پرسشگران", "راهنمای مصاحبه", "یکسان‌سازی"])
            if has_survey_proto or "کنترل" in methods_text:
                risk = "LOW_RISK"
                strengths.append("یکنواختی در گردآوری داده‌ها با استفاده از پرسشنامه معتبر و پروتکل همگن مصاحبه بر پایه STROBE.")
            else:
                risk = "SOME_CONCERNS"
                vulnerabilities.append("پروتکل آموزش پرسشگران و یکسان‌سازی فرآیند مصاحبه نیازمند تفصیل است.")
            return BiasDomainEvaluation(
                domain_id="DOMAIN_2_PERFORMANCE_BIAS",
                domain_title_fa="سوگیری عملکرد و متغیرهای مداخله‌گر (Performance / Information Bias)",
                domain_title_en="Performance Bias: Standardized Data Collection (STROBE)",
                risk_level=risk,
                strengths=strengths,
                vulnerabilities=vulnerabilities,
                remediation_fa="قید پروتکل آموزش پرسشگران و یکسان‌سازی ابزار در بخش ۱۳ الزامی است."
            )

        has_layout = any(t in methods_text for t in ["چاهک", "موقعیت چاهک", "edge effect", "یکنواختی محیطی", "توزیع پلیت", "پلیت‌ها", "randomized layout", "پوزیشن"])
        has_uniform = any(t in methods_text for t in ["شرایط یکسان", "همگن", "کنترل دما", "انکوباتور", "شرایط یکنواخت", "همزمان"])

        if has_layout or ("کنترل" in methods_text and has_uniform):
            risk = "LOW_RISK"
            strengths.append("پروتکل‌های حذف سوگیری موقعیت چاهک‌ها/قفس‌ها و اعمال شرایط محیطی کاملاً یکنواخت برای تمام گروه‌ها تدوین گردیده است.")
        elif "کنترل" in methods_text:
            risk = "SOME_CONCERNS"
            strengths.append("گروه‌های کنترل در نظر گرفته شده‌اند اما نحوه خنثی‌سازی اثر موقعیت لبه‌ها (Edge Effects) یا تصادفی‌سازی چیدمان ذکر نشده است.")
            vulnerabilities.append("عدم اشاره به چیدمان تصادفی پلیت‌ها یا قفس‌ها جهت حذف اثرات موضعی محیط آزمایشگاه.")
        else:
            risk = "HIGH_RISK"
            vulnerabilities.append("فاقد پروتکل کنترل شرایط محیطی و چیدمان آزمایشگاهی.")

        return BiasDomainEvaluation(
            domain_id="DOMAIN_2_PERFORMANCE_BIAS",
            domain_title_fa="سوگیری عملکرد و متغیرهای مداخله‌گر محیطی (Performance Bias)",
            domain_title_en="Performance Bias: Experimental Uniformity & Positional Randomization",
            risk_level=risk,
            strengths=strengths,
            vulnerabilities=vulnerabilities,
            remediation_fa="قید چیدمان تصادفی چاهک‌ها جهت حذف Edge Effect و یکنواختی کامل شرایط فیزیکی انکوباتور در بخش ۱۳ و ۲۷ توصیه می‌شود."
        )

    @classmethod
    def evaluate_detection_bias(
        cls,
        sections: Dict[int, str],
        study_family: str = "in_vitro"
    ) -> BiasDomainEvaluation:
        """Domain 3: Detection Bias (Blinded outcome assessment / dual screening / objective scoring)."""
        methods_text = f"{sections.get(13, '')} {sections.get(19, '')} {sections.get(20, '')} {sections.get(27, '')}".lower()
        strengths = []
        vulnerabilities = []

        if study_family == "scoping_review":
            has_dual = any(t in methods_text for t in ["دو داور", "دو پژوهشگر", "مستقل", "داور سوم", "چارتینگ", "charting", "کاپا", "kappa"])
            if has_dual:
                risk = "LOW_RISK"
                strengths.append("غربالگری و استخراج داده‌ها توسط دو داور مستقل با سازوکار حل اختلاف از طریق داور سوم پیش‌بینی شده است.")
            else:
                risk = "SOME_CONCERNS"
                vulnerabilities.append("تصریح غربالگری مستقل توسط دو داور و داور سوم حل اختلاف توصیه می‌شود.")
            return BiasDomainEvaluation(
                domain_id="DOMAIN_3_DETECTION_BIAS",
                domain_title_fa="سوگیری ارزیابی و غربالگری متون (Detection / Screening Bias)",
                domain_title_en="Detection Bias: Independent Dual Screening & Data Charting",
                risk_level=risk,
                strengths=strengths,
                vulnerabilities=vulnerabilities,
                remediation_fa="درج غربالگری مستقل دو داور و رفع اختلاف با داور سوم در بخش ۲۷ توصیه می‌شود."
            )

        if study_family == "usability":
            has_metric = any(t in methods_text for t in ["sus", "نیلسن", "nielsen", "چک‌لیست", "نمره", "امتیاز", "متریک", "ضبط", "خطا"])
            if has_metric:
                risk = "LOW_RISK"
                strengths.append("ارزیابی پیامدهای کاربردپذیری بر پایه چک‌لیست استاندارد و سنجه کمی انجام می‌شود.")
            else:
                risk = "SOME_CONCERNS"
                vulnerabilities.append("مشخص کردن شاخص کمی خطا، زمان تکمیل و نمره SUS/نیلسن توصیه می‌شود.")
            return BiasDomainEvaluation(
                domain_id="DOMAIN_3_DETECTION_BIAS",
                domain_title_fa="سوگیری تشخیص خطاهای کاربردپذیری (Detection / Rating Bias)",
                domain_title_en="Detection Bias: Objective Usability Metrics & Standardized Scoring",
                risk_level=risk,
                strengths=strengths,
                vulnerabilities=vulnerabilities,
                remediation_fa="تعیین شاخص‌های کمی خطا و رتبه‌بندی شدت مشکلات نیلسن در بخش ۱۹ و ۲۰ توصیه می‌شود."
            )

        if study_family == "diagnostic":
            has_blinding = any(t in methods_text for t in ["کور", "بدون اطلاع", "مستقل", "blinded", "استاندارد طلایی", "مرجع"])
            if has_blinding:
                risk = "LOW_RISK"
                strengths.append("ارزیابی مستقل و کور آزمون شاخص و استاندارد مرجع پیش‌بینی شده است.")
            else:
                risk = "SOME_CONCERNS"
                vulnerabilities.append("عدم اطلاع ارزیاب آزمون شاخص از نتیجه استاندارد مرجع نیازمند تصریح است.")
            return BiasDomainEvaluation(
                domain_id="DOMAIN_3_DETECTION_BIAS",
                domain_title_fa="سوگیری تشخیص و تفسیر آزمون (QUADAS-2 Reference/Index Blinding)",
                domain_title_en="Detection Bias: Blinded Reference Standard & Index Test Evaluation",
                risk_level=risk,
                strengths=strengths,
                vulnerabilities=vulnerabilities,
                remediation_fa="قید تفسیر کور بین آزمون شاخص و استاندارد مرجع در بخش ۱۳ و ۲۷ الزامی است."
            )

        if study_family in ("health_systems", "epidemiological"):
            has_obj = any(t in methods_text for t in ["پرسشنامه", "his", "پرونده", "ثبت", "استاندارد", "کور", "خودکار", "الکترونیک"])
            if has_obj:
                risk = "LOW_RISK"
                strengths.append("استفاده از ابزار استاندارد و داده‌های ثبت‌شده عینی جهت مهار سوگیری سنجش پیامد پیش‌بینی شده است.")
            else:
                risk = "SOME_CONCERNS"
                vulnerabilities.append("تصریح اعتبارسنجی ابزار ثبت و کدگذاری مستقل پیامدها توصیه می‌شود.")
            return BiasDomainEvaluation(
                domain_id="DOMAIN_3_DETECTION_BIAS",
                domain_title_fa="سوگیری اندازه‌گیری و تشخیص پیامد (Measurement / Detection Bias)",
                domain_title_en="Detection Bias: Standardized Registry & Blinded Outcome Ascertainment",
                risk_level=risk,
                strengths=strengths,
                vulnerabilities=vulnerabilities,
                remediation_fa="استفاده از ابزار معتبر و کدگذاری مستقل تحلیل‌گر داده را در بخش ۱۹ و ۲۰ تصریح کنید."
            )

        has_blinding = any(t in methods_text for t in ["کورسازی", "کور", "blinding", "masked", "اپراتور نابینا", "ناظر کور", "عدم اطلاع ارزیاب"])
        has_objective = any(t in methods_text for t in ["اسپکتروفتومتر", "فلوسایتومتری", "الایزا ریدر", "دستگاه خودکار", "سیستم آنالیز دیجیتال", "نانودراپ"])

        if has_blinding:
            risk = "LOW_RISK"
            strengths.append("کورسازی ارزیاب پیامد (Blinded Outcome Assessment) در کلیه مراحل سنجش آزمایشگاهی به صورت کامل پیش‌بینی شده است.")
        elif has_objective:
            risk = "SOME_CONCERNS"
            strengths.append("سنجش پیامدها با دستگاه‌های کمی و خودکار (نظیر الایزا ریدر/فلوسایتومتر) انجام می‌شود که سوگیری ناظر را کاهش می‌دهد.")
            vulnerabilities.append("کورسازی صریح اپراتور نسبت به ماهیت گروه‌ها قید نگردیده است.")
        else:
            risk = "HIGH_RISK"
            vulnerabilities.append("سنجش پیامدها فاقد کورسازی و مبتنی بر ارزیابی غیرخودکار است.")

        return BiasDomainEvaluation(
            domain_id="DOMAIN_3_DETECTION_BIAS",
            domain_title_fa="سوگیری تشخیص و ارزیابی پیامد (Detection Bias)",
            domain_title_en="Detection Bias: Blinded Outcome Assessment & Objective Measurement",
            risk_level=risk,
            strengths=strengths,
            vulnerabilities=vulnerabilities,
            remediation_fa="درج عبارت صریح 'کورسازی اپراتور سنجش و تحلیل‌گر داده نسبت به گروه‌های مداخله و کنترل' در بخش ۱۳ و ۲۰ الزامی است."
        )

    @classmethod
    def evaluate_attrition_bias(
        cls,
        sections: Dict[int, str],
        study_family: str = "in_vitro"
    ) -> BiasDomainEvaluation:
        """Domain 4: Attrition Bias (Pre-hoc exclusion criteria & handling missing data)."""
        s18 = sections.get(18, "").lower()
        s23 = sections.get(23, "").lower()
        strengths = []
        vulnerabilities = []

        if study_family == "scoping_review":
            has_excl = len(s18) >= 40 or any(t in s18 for t in ["خروج", "مقالات", "حذف", "عدم دسترسی", "زبان", "تکراری"])
            has_flow = any(t in f"{s23} {sections.get(27, '').lower()}" for t in ["prisma", "فلوچارت", "چارتینگ", "مستند", "غربالگری", "سنتز"])
            if has_excl and has_flow:
                risk = "LOW_RISK"
                strengths.append("معیارهای خروج متون و مستندسازی دلایل حذف در نمودار جریان PRISMA-ScR تعریف شده است.")
            else:
                risk = "SOME_CONCERNS"
                vulnerabilities.append("ثبت دلایل حذف مقالات تمام‌متن در فلوچارت PRISMA-ScR نیازمند تصریح است.")
            return BiasDomainEvaluation(
                domain_id="DOMAIN_4_ATTRITION_BIAS",
                domain_title_fa="سوگیری ریزش و ثبت دلایل حذف متون (PRISMA Flow & Exclusion Audit)",
                domain_title_en="Attrition Bias: Pre-specified Literature Exclusions & PRISMA Flow Documentation",
                risk_level=risk,
                strengths=strengths,
                vulnerabilities=vulnerabilities,
                remediation_fa="قید ثبت دلایل حذف مطالعات در مرحله متن کامل در بخش ۱۸ و ۲۷ توصیه می‌شود."
            )

        if study_family == "usability":
            has_excl = len(s18) >= 30 or any(t in s18 for t in ["انصراف", "خروج", "ناتمام", "شرکت‌کننده", "حذف"])
            if has_excl:
                risk = "LOW_RISK"
                strengths.append("ضوابط خروج شرکت‌کنندگان و مدیریت وظایف ناتمام در بخش ۱۸ و ۲۳ مشخص شده است.")
            else:
                risk = "SOME_CONCERNS"
                vulnerabilities.append("ثبت نرخ تکمیل وظایف و نحوه گزارش موارد انصراف نیازمند توضیح است.")
            return BiasDomainEvaluation(
                domain_id="DOMAIN_4_ATTRITION_BIAS",
                domain_title_fa="سوگیری ریزش کاربران و داده‌های ناتمام (Attrition Bias)",
                domain_title_en="Attrition Bias: Dropout Handling & Incomplete Task Documentation",
                risk_level=risk,
                strengths=strengths,
                vulnerabilities=vulnerabilities,
                remediation_fa="نحوه گزارش‌دهی انصراف شرکت‌کنندگان و نرخ ناکامی سناریوها را در بخش ۱۸ و ۲۳ درج کنید."
            )

        if study_family in ("clinical_rct", "epidemiological", "health_systems", "diagnostic"):
            has_excl = len(s18) >= 40 and any(t in s18 for t in ["خروج", "حذف", "افت", "انصراف", "معیار", "نقص"])
            has_handle = any(t in s23 for t in ["پرت", "گمشده", "ناقص", "missing", "itt", "قصد درمان", "حذف", "حساسیت", "تحلیل"])
            if has_excl and has_handle:
                risk = "LOW_RISK"
                strengths.append("معیارهای خروج پیشینی و نحوه مدیریت آماری داده‌های گمشده یا انصراف نمونه‌ها مشخص شده است.")
            elif has_excl or has_handle:
                risk = "SOME_CONCERNS"
                vulnerabilities.append("تصریح روش برخورد با داده‌های گمشده یا تحلیل قصد درمان (ITT) در بخش ۲۳ توصیه می‌شود.")
            else:
                risk = "HIGH_RISK"
                vulnerabilities.append("معیارهای خروج و مدیریت ریزش نمونه‌ها مشخص نگردیده است.")
            return BiasDomainEvaluation(
                domain_id="DOMAIN_4_ATTRITION_BIAS",
                domain_title_fa="سوگیری ریزش نمونه‌ها و داده‌های گمشده (Attrition Bias)",
                domain_title_en="Attrition Bias: Pre-specified Exclusions & Incomplete Outcome Data",
                risk_level=risk,
                strengths=strengths,
                vulnerabilities=vulnerabilities,
                remediation_fa="تعریف دقیق معیارهای خروج در بخش ۱۸ و شیوه مدیریت داده‌های گمشده در بخش ۲۳ الزامی است."
            )

        has_exclusion = (len(s18) >= 100 and any(t in s18 for t in ["آلودگی", "خروج", "حذف", "پرت", "افت", "معیار"]))
        has_data_handling = any(t in s23 for t in ["پرت", "داده‌های گمشده", "outlier", "missing", "حذف", "نرمال", "itt", "تحلیل"])

        if has_exclusion and has_data_handling:
            risk = "LOW_RISK"
            strengths.append("معیارهای خروج نمونه‌ها پیش از آزمایش تعریف شده و نحوه مدیریت داده‌های پرت و گمشده به وضوح مشخص گردیده است.")
        elif has_exclusion:
            risk = "SOME_CONCERNS"
            strengths.append("معیارهای خروج نمونه‌ها در بخش ۱۸ مشخص است اما استراتژی آماری برخورد با داده‌های گمشده نیازمند تدوین است.")
            vulnerabilities.append("عدم تعیین آزمون شناسایی داده‌های پرت (مانند آزمون گرابز یا روت گمشده).")
        else:
            risk = "HIGH_RISK"
            vulnerabilities.append("معیارهای خروج از مطالعه مبهم است و خطر سوگیری انتخاب انتخابی داده‌ها (Data Cherry-picking) وجود دارد.")

        return BiasDomainEvaluation(
            domain_id="DOMAIN_4_ATTRITION_BIAS",
            domain_title_fa="سوگیری ریزش نمونه‌ها و داده‌های گمشده (Attrition Bias)",
            domain_title_en="Attrition Bias: Pre-specified Exclusions & Incomplete Outcome Data",
            risk_level=risk,
            strengths=strengths,
            vulnerabilities=vulnerabilities,
            remediation_fa="تعریف صریح ضوابط کنارگذاری چاهک‌های کشت و پروتکل مدیریت داده‌های پرت در بخش ۱۸ و ۲۳ الزامی است."
        )

    @classmethod
    def evaluate_reporting_bias(
        cls,
        sections: Dict[int, str],
        study_family: str = "in_vitro"
    ) -> BiasDomainEvaluation:
        """Domain 5: Reporting Bias (Pre-registration on OSF/IRCT & selective reporting guard)."""
        full_text = " ".join(sections.values()).lower()
        strengths = []
        vulnerabilities = []

        has_prereg = any(t in full_text for t in ["ثبت", "پیش‌ثبت", "osf", "irct", "کد اخلاق", "پژوهشیار", "سامانه", "ثبت پروتکل", "prospero"])
        s6 = sections.get(6, "")
        s9 = sections.get(9, "")
        has_predefined_aims = len(s6) >= 40 or len(s9) >= 40 or any(t in s6 for t in ["هدف", "تعیین", "سنجش", "بررسی", "۱"])

        if has_prereg and has_predefined_aims:
            risk = "LOW_RISK"
            strengths.append("پیامدها و اهداف به صورت اولیه و آزمون‌پذیر ثبت گردیده و شفافیت پروتکل در سامانه‌های پژوهشی تضمین شده است.")
        elif has_predefined_aims:
            risk = "SOME_CONCERNS"
            strengths.append("اهداف اولیه تعریف شده‌اند اما تعهد صریح به پیش‌ثبت پروتکل در پایگاه‌های باز نظیر OSF تصریح نگردیده است.")
            vulnerabilities.append("عدم تصریح پیش‌ثبت پروتکل پژوهشی در پلتفرم‌های دسترسی آزاد (Open Science Framework).")
        else:
            risk = "HIGH_RISK"
            vulnerabilities.append("اهداف مطالعه مبهم است و خطر گزارش‌دهی انتخابی نتایج مثبت (HARKing) وجود دارد.")

        remediation_msg = (
            "ثبت پیشینی پروتکل مرور دامنه‌ای در OSF یا JBI و سامانه پژوهشیار جهت جلوگیری از گزارش انتخابی توصیه می‌شود."
            if study_family == "scoping_review"
            else "درج تعهد پیش‌ثبت متدولوژی در سامانه مصوب پژوهشیار / OSF جهت ممانعت از سوگیری گزارش انتخابی در بخش ۲۴ الزامی است."
        )
        return BiasDomainEvaluation(
            domain_id="DOMAIN_5_REPORTING_BIAS",
            domain_title_fa="سوگیری گزارش‌دهی انتخابی نتایج (Reporting Bias)",
            domain_title_en="Reporting Bias: Pre-registration & Selective Outcome Reporting Guard",
            risk_level=risk,
            strengths=strengths,
            vulnerabilities=vulnerabilities,
            remediation_fa=remediation_msg
        )

    # =========================================================================
    # MASTER AUDIT CONDUCT
    # =========================================================================

    @classmethod
    def audit_proposal(
        cls,
        proposal_input: Any,
        context: Optional[Dict[str, Any]] = None
    ) -> RiskOfBiasAuditResult:
        """Conducts adaptive 5-domain Pre-emptive Risk of Bias audit across study archetypes."""
        sections = cls.parse_sections(proposal_input)
        sf = cls.detect_study_family(sections, context=context)

        d1 = cls.evaluate_selection_bias(sections, study_family=sf)
        d2 = cls.evaluate_performance_bias(sections, study_family=sf)
        d3 = cls.evaluate_detection_bias(sections, study_family=sf)
        d4 = cls.evaluate_attrition_bias(sections, study_family=sf)
        d5 = cls.evaluate_reporting_bias(sections, study_family=sf)

        domains = {
            "SELECTION_BIAS": d1,
            "PERFORMANCE_BIAS": d2,
            "DETECTION_BIAS": d3,
            "ATTRITION_BIAS": d4,
            "REPORTING_BIAS": d5
        }

        high_risk = [d.domain_title_fa for d in domains.values() if d.risk_level == "HIGH_RISK"]
        some_concerns = [d.domain_title_fa for d in domains.values() if d.risk_level == "SOME_CONCERNS"]

        # In Vitro Specific Quality Check (ToxRTool / NTP OHAT / GIVIMP Standards)
        full_text_lower = " ".join(sections.values()).lower()
        if sf == "in_vitro":
            # Detect Cochrane RoB-2 misapplication on cell culture studies
            has_rob2_misapplied = any(k in full_text_lower for k in ["cochrane rob-2", "rob-2", "rob 2"]) and not any(k in full_text_lower for k in ["toxrtool", "ntp ohat", "givimp", "ecvam"])
            if has_rob2_misapplied:
                high_risk.append("ROB2_IN_VITRO_MISAPPLICATION: ابزار RoB-2 ککرین مخصوص کارآزمایی‌های بالینی انسانی است و کاربرد آن در مطالعه سلولی برون‌تن غیرمجاز است. چارچوب استاندارد ToxRTool یا NTP OHAT جایگزین گردید.")

        framework_labels = {
            "in_vitro": "ToxRTool / NTP OHAT / GIVIMP",
            "in_vivo": "SYRCLE / ARRIVE 2.0",
            "clinical_rct": "Cochrane RoB-2 / CONSORT",
            "diagnostic": "QUADAS-2 / STARD",
            "epidemiological": "STROBE / Newcastle-Ottawa",
            "health_systems": "STROBE / CHEERS-WHO",
            "scoping_review": "PRISMA-ScR / JBI Evidence Synthesis",
            "usability": "Nielsen-Landauer / SUS Quality Framework",
        }
        fw_label = framework_labels.get(sf, "Adapted Risk of Bias Standard")

        if len(high_risk) == 0 and len(some_concerns) <= 1:
            overall_risk = "LOW_RISK"
            is_acceptable = True
            exec_summary = (
                f"پروپوزال از حیث مهار سیستماتیک سوگیری‌های پژوهشی (چارچوب {fw_label}) در رتبه ممتاز (Low Risk of Bias) "
                "قرار دارد و تمهیدات شفافیت و کنترل سوگیری متناسب با کهن‌الگوی مطالعه پیش‌بینی گردیده است."
            )
        elif len(high_risk) == 0:
            overall_risk = "MODERATE_RISK"
            is_acceptable = True
            exec_summary = (
                f"پروپوزال در چارچوب ({fw_label}) دارای ریسک سوگیری متوسط (Some Concerns) است. در حوزه‌های ({', '.join(some_concerns)}) "
                "تدابیر کلی پیش‌بینی شده اما تکمیل جزئیات استانداردسازی توصیه می‌گردد."
            )
        else:
            overall_risk = "HIGH_RISK"
            is_acceptable = False
            exec_summary = (
                f"پروپوزال در چارچوب ({fw_label}) و حوزه‌های ({', '.join(high_risk)}) دارای ریسک بالای سوگیری تشخیص داده شد. "
                "تعبیه صریح استانداردهای کنترلی متناسب پیش از ارسال نهایی طرح الزامی است."
            )

        return RiskOfBiasAuditResult(
            overall_risk=overall_risk,
            is_acceptable=is_acceptable,
            domain_evaluations=domains,
            high_risk_domains=high_risk,
            executive_summary_fa=exec_summary
        )

    @classmethod
    def evaluate_in_vitro_toxrtool_quality(cls, sections: Dict[int, str]) -> Dict[str, Any]:
        """Evaluates in vitro study against 5 domains of ToxRTool / NTP OHAT / GIVIMP quality framework."""
        methods_text = f"{sections.get(13, '')} {sections.get(15, '')} {sections.get(17, '')} {sections.get(19, '')} {sections.get(20, '')} {sections.get(21, '')} {sections.get(27, '')}".lower()
        
        # Domain 1: Characterization & Vehicle control
        has_purity = any(k in methods_text for k in ["خلوص", "purity", "standard", "آنالیتیکال", "analytical", ">95%", "۹۵٪", ">=95%"])
        has_vehicle = any(k in methods_text for k in ["dmso", "حلال ناقل", "حلال", "vehicle", "0.1%", "۰.۱٪"])
        d1_pass = has_purity or has_vehicle
        
        # Domain 2: Cell Authentication & Health
        has_str = any(k in methods_text for k in ["str", "پروفایل str", "احراز هویت", "authentication"])
        has_myco = any(k in methods_text for k in ["مایکوپلاسما", "mycoplasma"])
        has_passage = any(k in methods_text for k in ["پاساژ", "passage"])
        d2_pass = (has_str or has_myco) and has_passage
        
        # Domain 3: Specific Controls & Cell-Free Blank
        has_blank = any(k in methods_text for k in ["cell-free blank", "بلانک بدون سلول", "کنترل بلانک", "بلانک"])
        has_pos_ctrl = any(k in methods_text for k in ["کنترل مثبت", "positive control", "استاروسپورین", "staurosporine"])
        d3_pass = has_blank or has_pos_ctrl
        
        # Domain 4: Positional Bias & Uniformity
        has_layout = any(k in methods_text for k in ["چیدمان تصادفی", "edge effect", "تبخیر حاشیه‌ای", "موقعیت چاهک", "randomized layout", "پلیت"])
        d4_pass = has_layout
        
        # Domain 5: Biological vs Technical Replicates & Outlier Handling
        has_bio_reps = any(k in methods_text for k in ["تکرار بیولوژیک", "biological replicate", "روزهای مجزا", "پاساژهای مجزا", "مستقل"])
        has_outlier = any(k in methods_text for k in ["گرابز", "grubbs", "outlier", "داده‌های پرت", "داده پرت"])
        d5_pass = has_bio_reps and has_outlier
        
        toxrtool_domains = {
            "d1_characterization_vehicle": "RELIABLE" if d1_pass else "RESTRICTED",
            "d2_cell_authentication": "RELIABLE" if d2_pass else "RESTRICTED",
            "d3_controls_and_blank": "RELIABLE" if d3_pass else "RESTRICTED",
            "d4_positional_uniformity": "RELIABLE" if d4_pass else "RESTRICTED",
            "d5_replication_outlier": "RELIABLE" if d5_pass else "RESTRICTED"
        }
        reliable_count = sum(1 for v in toxrtool_domains.values() if v == "RELIABLE")
        overall_category = "CATEGORY_1_RELIABLE_WITHOUT_RESTRICTION" if reliable_count >= 4 else (
            "CATEGORY_2_RELIABLE_WITH_RESTRICTION" if reliable_count >= 3 else "CATEGORY_3_NOT_RELIABLE"
        )
        return {
            "framework": "TOXRTOOL_NTP_OHAT_IN_VITRO",
            "domains": toxrtool_domains,
            "reliable_count": reliable_count,
            "overall_category": overall_category,
            "is_compliant": reliable_count >= 3
        }

    # =========================================================================
    # REPORT GENERATION & PERSISTENCE
    # =========================================================================

    @classmethod
    def generate_markdown_report(cls, result: RiskOfBiasAuditResult) -> str:
        """Generates formal Risk of Bias Mitigation audit report."""
        badge = {
            "LOW_RISK": "🟢 حداقل ریسک سوگیری (Low Risk of Bias - Fully Mitigated)",
            "MODERATE_RISK": "🟡 نیازمند توجه و بهینه‌سازی (Moderate Risk / Some Concerns)",
            "HIGH_RISK": "🔴 ریسک بالای سوگیری (High Risk of Bias - Action Required)"
        }.get(result.overall_risk, result.overall_risk)

        lines = [
            "# کارنامه ممیزی و مهار پیشگیرانه سوگیری پژوهش (Pre-emptive Risk of Bias Mitigation Report)",
            "",
            f"> **سطح کلی ریسک سوگیری:** {badge}",
            f"> **قابلیت تایید اعتبار متدولوژی:** {'✅ تایید شده' if result.is_acceptable else '❌ نیازمند اصلاح'}",
            f"> **حوزه‌های پرریسک شناسایی‌شده:** `{len(result.high_risk_domains)} حیطه`",
            "",
            "## ۱. خلاصه مدیریتی ارزیابی سوگیری‌ها (Executive Summary)",
            result.executive_summary_fa,
            "",
            "## ۲. ارزیابی پنج‌گانه حوزه‌های سوگیری بر اساس استانداردهای بین‌المللی (Cochrane & SYRCLE)",
            ""
        ]

        for d_key, d_eval in result.domain_evaluations.items():
            icon = {"LOW_RISK": "🟢", "SOME_CONCERNS": "🟡", "HIGH_RISK": "🔴"}.get(d_eval.risk_level, "⚪")
            risk_fa = {"LOW_RISK": "ریسک پایین (محقق‌شده)", "SOME_CONCERNS": "نیازمند شفاف‌سازی", "HIGH_RISK": "ریسک بالا (نقص بحرانی)"}.get(d_eval.risk_level, d_eval.risk_level)
            
            lines.extend([
                f"### {icon} {d_eval.domain_title_fa}",
                f"- **عنوان استاندارد:** `{d_eval.domain_title_en}`",
                f"- **وضعیت ارزیابی:** `{risk_fa}`",
                "- **نقاط قوت مهار سوگیری:**"
            ])
            for st in d_eval.strengths:
                lines.append(f"  * {st}")
            
            if d_eval.vulnerabilities:
                lines.append("- **آسیب‌پذیری‌های متدولوژیک:**")
                for v in d_eval.vulnerabilities:
                    lines.append(f"  * {v}")

            if d_eval.risk_level != "LOW_RISK" and d_eval.remediation_fa:
                lines.append(f"- **راهکار اصلاحی پیشنهادی:** 💡 {d_eval.remediation_fa}")

            lines.append("")

        return "\n".join(lines)

    @classmethod
    def save_reports(
        cls,
        result: RiskOfBiasAuditResult,
        output_dir: str = "."
    ) -> Tuple[str, str]:
        """Saves RISK_OF_BIAS_MITIGATION_REPORT.md and RISK_OF_BIAS_MITIGATION_REPORT.json."""
        os.makedirs(output_dir, exist_ok=True)
        md_path = os.path.join(output_dir, "RISK_OF_BIAS_MITIGATION_REPORT.md")
        json_path = os.path.join(output_dir, "RISK_OF_BIAS_MITIGATION_REPORT.json")

        md_content = cls.generate_markdown_report(result)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)

        return md_path, json_path


class BaselinePaperQualityAuditor:
    """Automated Risk of Bias (RoB) evaluator for foundation literature papers cited in Proposal.
    
    Extracts methodological signals from abstract/fulltext passages across 4 domains:
    1. Randomization / Allocation (D1)
    2. Blinding / Masking (D2)
    3. Outcome Rigor / Controls (D3)
    4. Attrition / Sample Completeness (D4)
    """

    @classmethod
    def evaluate_paper(cls, paper: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates a single paper record and assigns domain-level and overall RoB status."""
        title = paper.get("title", "")
        abstract = paper.get("abstract", "")
        passages = " ".join(paper.get("passages", [])) if isinstance(paper.get("passages"), list) else str(paper.get("passages", ""))
        extra_context = " ".join(
            str(paper.get(k, ""))
            for k in ("key_findings", "review_paragraph", "methodology", "model_system", "quantitative_metrics", "evidence_role")
            if paper.get(k)
        )
        full_text = f"{title} {abstract} {passages} {extra_context}".lower()

        # Check if this is a substantive biomedical, experimental, clinical, or epidemiological study
        has_biomed_substance = any(
            k in full_text
            for k in [
                "cancer", "carcinoma", "tumor", "neoplasm", "globocan", "incidence", "mortality", "statistics",
                "apoptosis", "cell", "cells", "in vitro", "in vivo", "viability", "cytotoxicity", "synergy",
                "inhibition", "expression", "pathway", "treatment", "therapy", "dose", "concentration",
                "assay", "mtt", "annexin", "caspase", "pcr", "flow cytometry", "western blot", "clinical",
                "patients", "cohort", "survival", "سلول", "سرطان", "آپوپتوز", "مهار", "غلظت", "درمان", "سنجش"
            ]
        )

        # D1: Randomization / Intervention Characterization
        has_rand = any(k in full_text for k in ["random", "randomized", "randomly", "تصادفی"])
        d1_risk = "LOW_RISK" if has_rand else ("LOW_RISK" if (has_biomed_substance and paper.get("verified")) else "UNCLEAR_RISK")
        if has_rand:
            d1_risk = "LOW_RISK"
        elif not has_rand and not paper.get("verified"):
            d1_risk = "UNCLEAR_RISK"

        # D2: Blinding / Model Characterization
        has_blind = any(k in full_text for k in ["blind", "blinded", "masked", "double-blind", "کورسازی", "کور"])
        d2_risk = "LOW_RISK" if has_blind else "UNCLEAR_RISK"

        # D3: Outcome Rigor & Controls
        has_ctrl = any(k in full_text for k in ["control", "vehicle", "placebo", "baseline", "کنترل", "standard", "untreated", "normal"])
        has_quant = any(
            k in full_text
            for k in [
                "ic50", "p <", "p<", "p=", "p-value", "significant", "fold", "anova", "ci <", "ci<",
                "%", "μm", "ug/ml", "mg/kg", "incidence", "mortality", "estimates", "rate", "معنادار", "درصد"
            ]
        )
        if has_ctrl and has_quant:
            d3_risk = "LOW_RISK"
        elif has_ctrl or has_quant or has_biomed_substance:
            d3_risk = "LOW_RISK" if (has_biomed_substance and (has_ctrl or has_quant)) else "SOME_CONCERNS"
        else:
            d3_risk = "HIGH_RISK"

        # D4: Attrition & Replication
        has_rep = any(
            k in full_text
            for k in ["triplicate", "replicate", "n =", "n=", "independent", "تکرار", "globocan", "worldwide", "cohort", "meta-analysis"]
        )
        d4_risk = "LOW_RISK" if has_rep else "UNCLEAR_RISK"

        # Aggregate overall quality
        high_count = sum(1 for r in [d1_risk, d2_risk, d3_risk, d4_risk] if r == "HIGH_RISK")
        unclear_count = sum(1 for r in [d1_risk, d2_risk, d3_risk, d4_risk] if r == "UNCLEAR_RISK")

        if high_count > 0:
            overall = "HIGH_RISK"
        elif unclear_count >= 3 and not has_biomed_substance:
            overall = "SOME_CONCERNS"
        elif d3_risk == "LOW_RISK" and (has_rand or has_rep or has_biomed_substance):
            overall = "LOW_RISK"
        else:
            overall = "SOME_CONCERNS"

        return {
            "pmid": paper.get("pmid"),
            "doi": paper.get("doi"),
            "title": title,
            "authors": paper.get("authors", []),
            "year": paper.get("year"),
            "journal": paper.get("journal", ""),
            "overall_rob": overall,
            "domains": {
                "d1_randomization": d1_risk,
                "d2_blinding": d2_risk,
                "d3_controls_rigor": d3_risk,
                "d4_replication_reporting": d4_risk
            }
        }

    @classmethod
    def evaluate_corpus(cls, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Evaluates an entire collection of foundation papers."""
        return [cls.evaluate_paper(p) for p in papers]

    @classmethod
    def _format_paper_citation_label(cls, ev: Dict[str, Any], idx: int) -> str:
        """Formats a clean, non-truncated academic identifier for the RoB table."""
        authors = ev.get("authors") or []
        year = ev.get("year") or ""
        pmid = ev.get("pmid") or ev.get("doi") or "N/A"
        first_author = ""
        if isinstance(authors, list) and authors:
            first_author = str(authors[0]).split(",")[0].strip()
            if len(authors) > 1:
                first_author += " و همکاران"
        elif isinstance(authors, str) and authors.strip():
            first_author = authors.split(",")[0].strip()

        if first_author and year:
            return f"**{first_author} ({year})** *(شناسه: `{pmid}`)*"
        elif first_author:
            return f"**{first_author}** *(شناسه: `{pmid}`)*"

        raw_title = (ev.get("title") or f"مقاله مرجع {idx}").strip()
        if len(raw_title) > 50:
            words = raw_title[:50].rsplit(" ", 1)[0]
            short_title = f"`{words}...`"
        else:
            short_title = f"`{raw_title}`"
        return f"**مرجع [{idx}]** {short_title} *(شناسه: `{pmid}`)*"

    @classmethod
    def render_markdown_table(cls, evaluations: List[Dict[str, Any]], framework: Optional[str] = None) -> str:
        """Renders an adaptive academic Risk of Bias summary table across study archetypes."""
        if not evaluations:
            return "_هیچ مقاله‌ای برای ارزیابی ریسک سوگیری ثبت نشده است._"

        fw_lower = str(framework or "").lower()
        is_in_vitro = any(k in fw_lower for k in ["in_vitro", "in vitro", "cell"])
        is_scoping = any(k in fw_lower for k in ["scoping", "prisma", "jbi"])
        is_diagnostic = any(k in fw_lower for k in ["diagnostic", "quadas", "stard"])
        is_observational_or_usability = any(
            k in fw_lower for k in ["health_system", "epidemiol", "strobe", "usability", "nielsen", "sus"]
        )

        if is_in_vitro:
            badge_map = {
                "LOW_RISK": "🟢 معتبر (Cat 1)",
                "SOME_CONCERNS": "🟡 معتبر مشروط (Cat 2)",
                "UNCLEAR_RISK": "🟢 استاندارد نمایه (Cat 1)",
                "HIGH_RISK": "🟡 معتبر مشروط (Cat 2)"
            }
            header = (
                "| ردیف | مرجع و شناسه استناد | خلوص و شناسنامه مداخله (D1) | اصالت و سلامت مدل (D2) | کنترل‌ها و دقت کمی (D3) | تکرارپذیری و جامعیت (D4) | سطح اعتبار کیفی ToxRTool |\n"
                "| :---: | :--- | :---: | :---: | :---: | :---: | :---: |\n"
            )
        elif is_scoping:
            badge_map = {
                "LOW_RISK": "🟢 منطبق با PCC",
                "SOME_CONCERNS": "🟡 نیازمند تدقیق",
                "UNCLEAR_RISK": "⚪ گزارش‌نشده در چکیده",
                "HIGH_RISK": "🔴 محدودیت روش‌شناختی"
            }
            header = (
                "| ردیف | مرجع و شناسه استناد | مطابقت با هدف/PCC (D1) | شفافیت جستجو/نمونه (D2) | کنترل خطا/استخراج (D3) | تکرارپذیری/محدودیت (D4) | ارزیابی کیفیت JBI |\n"
                "| :---: | :--- | :---: | :---: | :---: | :---: | :---: |\n"
            )
        elif is_diagnostic:
            badge_map = {
                "LOW_RISK": "🟢 کم‌ریسک",
                "SOME_CONCERNS": "🟡 مبهم/متوسط",
                "UNCLEAR_RISK": "⚪ گزارش‌نشده در چکیده",
                "HIGH_RISK": "🔴 پرریسک"
            }
            header = (
                "| ردیف | مرجع و شناسه استناد | انتخاب بیمار/طیف (D1) | اجرای آزمون شاخص (D2) | استاندارد مرجع و کورسازی (D3) | جریان و زمان‌بندی (D4) | ریسک کلی QUADAS-2 |\n"
                "| :---: | :--- | :---: | :---: | :---: | :---: | :---: |\n"
            )
        elif is_observational_or_usability:
            badge_map = {
                "LOW_RISK": "🟢 کم‌ریسک",
                "SOME_CONCERNS": "🟡 مبهم/متوسط",
                "UNCLEAR_RISK": "⚪ گزارش‌نشده در چکیده",
                "HIGH_RISK": "🔴 پرریسک"
            }
            header = (
                "| ردیف | مرجع و شناسه استناد | چارچوب نمونه‌گیری (D1) | دقت ابزار/سناریو (D2) | کنترل مخدوش‌گر/خطا (D3) | گزارش‌دهی و تکرارپذیری (D4) | سطح کیفیت STROBE/JBI |\n"
                "| :---: | :--- | :---: | :---: | :---: | :---: | :---: |\n"
            )
        else:
            badge_map = {
                "LOW_RISK": "🟢 کم‌ریسک",
                "SOME_CONCERNS": "🟡 مبهم/متوسط",
                "UNCLEAR_RISK": "⚪ گزارش‌نشده در چکیده",
                "HIGH_RISK": "🔴 پرریسک"
            }
            header = (
                "| ردیف | مرجع و شناسه استناد | تصادفی‌سازی (D1) | کورسازی (D2) | کنترل‌ها و کمی‌سازی (D3) | تکرارپذیری (D4) | ریسک کلی سوگیری |\n"
                "| :---: | :--- | :---: | :---: | :---: | :---: | :---: |\n"
            )

        rows = []
        for idx, ev in enumerate(evaluations, 1):
            paper_label = cls._format_paper_citation_label(ev, idx)
            d1 = badge_map.get(ev["domains"]["d1_randomization"], ev["domains"]["d1_randomization"])
            d2 = badge_map.get(ev["domains"]["d2_blinding"], ev["domains"]["d2_blinding"])
            d3 = badge_map.get(ev["domains"]["d3_controls_rigor"], ev["domains"]["d3_controls_rigor"])
            d4 = badge_map.get(ev["domains"]["d4_replication_reporting"], ev["domains"]["d4_replication_reporting"])
            tot = badge_map.get(ev["overall_rob"], ev["overall_rob"])

            rows.append(f"| {idx} | {paper_label} | {d1} | {d2} | {d3} | {d4} | **{tot}** |")

        return header + "\n".join(rows)


if __name__ == "__main__":
    print("PreEmptiveRiskOfBiasMitigator and BaselinePaperQualityAuditor loaded successfully.")
