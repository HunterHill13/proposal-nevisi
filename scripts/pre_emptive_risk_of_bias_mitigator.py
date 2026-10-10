#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pre_emptive_risk_of_bias_mitigator.py - Pre-emptive Risk of Bias (RoB) Mitigation Engine
Proposal-Nevisi Engine v10.2 (Universal Biomedical Architecture)

Enforces international standards for pre-emptive experimental bias mitigation
based on Cochrane RoB-2 (Clinical/Translational) and SYRCLE (Preclinical Animal/In Vitro):
1. Domain 1: Selection Bias (Random sequence generation & allocation concealment)
2. Domain 2: Performance Bias (Blinded administration & randomized positional layout)
3. Domain 3: Detection Bias (Blinded outcome assessment / masked operator evaluation)
4. Domain 4: Attrition Bias (Pre-hoc exclusion criteria & complete outcome data accounting)
5. Domain 5: Reporting Bias (Pre-registration on OSF/IRCT & selective reporting guard)

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
    def evaluate_selection_bias(cls, sections: Dict[int, str]) -> BiasDomainEvaluation:
        """Domain 1: Selection Bias (Random sequence generation & allocation concealment)."""
        methods_text = f"{sections.get(13, '')} {sections.get(15, '')} {sections.get(22, '')} {sections.get(27, '')}".lower()
        strengths = []
        vulnerabilities = []

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
    def evaluate_performance_bias(cls, sections: Dict[int, str]) -> BiasDomainEvaluation:
        """Domain 2: Performance Bias (Environmental uniformity & random plate/cage placement)."""
        methods_text = f"{sections.get(13, '')} {sections.get(16, '')} {sections.get(20, '')} {sections.get(27, '')}".lower()
        strengths = []
        vulnerabilities = []

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
    def evaluate_detection_bias(cls, sections: Dict[int, str]) -> BiasDomainEvaluation:
        """Domain 3: Detection Bias (Blinded outcome assessment / masked evaluation)."""
        methods_text = f"{sections.get(13, '')} {sections.get(19, '')} {sections.get(20, '')} {sections.get(27, '')}".lower()
        strengths = []
        vulnerabilities = []

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
    def evaluate_attrition_bias(cls, sections: Dict[int, str]) -> BiasDomainEvaluation:
        """Domain 4: Attrition Bias (Pre-hoc exclusion criteria & handling missing data)."""
        s18 = sections.get(18, "").lower()
        s23 = sections.get(23, "").lower()
        strengths = []
        vulnerabilities = []

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
    def evaluate_reporting_bias(cls, sections: Dict[int, str]) -> BiasDomainEvaluation:
        """Domain 5: Reporting Bias (Pre-registration on OSF/IRCT & selective reporting guard)."""
        full_text = " ".join(sections.values()).lower()
        strengths = []
        vulnerabilities = []

        has_prereg = any(t in full_text for t in ["ثبت", "پیش‌ثبت", "osf", "irct", "کد اخلاق", "پژوهشیار", "سامانه", "ثبت پروتکل"])
        s6 = sections.get(6, "")
        has_predefined_aims = len(s6) >= 40 or any(t in s6 for t in ["هدف", "تعیین", "سنجش", "بررسی", "۱"])

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

        return BiasDomainEvaluation(
            domain_id="DOMAIN_5_REPORTING_BIAS",
            domain_title_fa="سوگیری گزارش‌دهی انتخابی نتایج (Reporting Bias)",
            domain_title_en="Reporting Bias: Pre-registration & Selective Outcome Reporting Guard",
            risk_level=risk,
            strengths=strengths,
            vulnerabilities=vulnerabilities,
            remediation_fa="درج تعهد پیش‌ثبت متدولوژی در سامانه مصوب پژوهشیار / OSF جهت ممانعت از سوگیری گزارش انتخابی در بخش ۲۴ الزامی است."
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
        """Conducts full 5-domain Cochrane/SYRCLE Pre-emptive Risk of Bias audit."""
        sections = cls.parse_sections(proposal_input)

        d1 = cls.evaluate_selection_bias(sections)
        d2 = cls.evaluate_performance_bias(sections)
        d3 = cls.evaluate_detection_bias(sections)
        d4 = cls.evaluate_attrition_bias(sections)
        d5 = cls.evaluate_reporting_bias(sections)

        domains = {
            "SELECTION_BIAS": d1,
            "PERFORMANCE_BIAS": d2,
            "DETECTION_BIAS": d3,
            "ATTRITION_BIAS": d4,
            "REPORTING_BIAS": d5
        }

        high_risk = [d.domain_title_fa for d in domains.values() if d.risk_level == "HIGH_RISK"]
        some_concerns = [d.domain_title_fa for d in domains.values() if d.risk_level == "SOME_CONCERNS"]

        if len(high_risk) == 0 and len(some_concerns) <= 1:
            overall_risk = "LOW_RISK"
            is_acceptable = True
            exec_summary = (
                "پروپوزال از حیث مهار سیستماتیک سوگیری‌های آزمایشگاهی (Cochrane RoB-2 / SYRCLE) در رتبه ممتاز (Low Risk of Bias) "
                "قرار دارد. تدابیر تصادفی‌سازی، کورسازی، پنهان‌سازی تخصیص و شفافیت خروج نمونه‌ها به صورت استاندارد لحاظ گردیده است."
            )
        elif len(high_risk) == 0:
            overall_risk = "MODERATE_RISK"
            is_acceptable = True
            exec_summary = (
                f"پروپوزال دارای ریسک سوگیری متوسط (Some Concerns) است. در حوزه‌های ({', '.join(some_concerns)}) "
                "تدابیر کلی پیش‌بینی شده اما برای نیل به استانداردهای تراز اول گرنت‌ها، شفاف‌سازی کورسازی و تخصیص تصادفی توصیه می‌گردد."
            )
        else:
            overall_risk = "HIGH_RISK"
            is_acceptable = False
            exec_summary = (
                f"پروپوزال در حوزه‌های ({', '.join(high_risk)}) دارای ریسک بالای سوگیری (High Risk of Bias) تشخیص داده شد. "
                "تعبیه صریح استانداردهای کورسازی و تصادفی‌سازی پیش از ارسال نهایی طرح الزامی است."
            )

        return RiskOfBiasAuditResult(
            overall_risk=overall_risk,
            is_acceptable=is_acceptable,
            domain_evaluations=domains,
            high_risk_domains=high_risk,
            executive_summary_fa=exec_summary
        )

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


if __name__ == "__main__":
    print("PreEmptiveRiskOfBiasMitigator loaded successfully.")
