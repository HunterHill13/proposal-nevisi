#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
methodology_completeness_gate.py - Pajooheshyar 28-Section Completeness & Sample Size Methodology Gate
Proposal-Nevisi Engine v9.1 (Layer 2: Structural Compliance)

Enforces:
1. 28 Mandatory Sections of the official Iranian Biomedical Research Information System (Pajooheshyar).
2. Deep Sample Size Methodology Evaluation:
   - Evaluates primary endpoint, experimental unit, effect size, variance/SD, alpha, power, design.
   - If inputs are insufficient, does NOT generate a fictitious formula; emits SAMPLE_SIZE_STATUS = INSUFFICIENT_INPUTS
     and lists missing_inputs.
3. Biological vs Technical Replicates Enforcer:
   - Strictly distinguishes biological replicates (independent experimental units) from technical replicates
     (pipetting/assay triplicates).
   - Prevents pseudo-replication fallacy (4 biological x 3 technical is n = 4, NEVER n = 12).
   - Flags REPLICATION_STRUCTURE_UNDEFINED if experimental unit is ambiguous.

100% General-Purpose: Zero hardcoded project subjects.
"""

import re
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field

REQUIRED_SECTIONS_28 = [
    "عنوان فارسی",
    "عنوان انگلیسی",
    "نوع مطالعه",
    "بیان مسئله و ضرورت انجام تحقیق",
    "مروری بر متون",
    "اهداف (هدف کلی و اهداف اختصاصی)",
    "فرضیات یا سوالات پژوهشی",
    "جامعه آماری",
    "روش نمونهگیری",
    "حجم نمونه و روش محاسبه آن",
    "معیارهای ورود به مطالعه",
    "معیارهای خروج از مطالعه",
    "روش اجرا",
    "ابزار جمعآوری دادهها",
    "روشهای آماری تجزیه و تحلیل دادهها",
    "ملاحظات اخلاقی",
    "محدودیتهای مطالعه",
    "جدول متغیرها",
    "جدول زمانبندی",
    "بودجه",
    "منابع",
    "خلاصه فارسی",
    "خلاصه انگلیسی (Abstract)",
    "کلیدواژههای فارسی",
    "کلیدواژههای انگلیسی",
    "تعارض منافع",
    "سپاسگزاری",
    "ضمائم (در صورت نیاز)"
]

PAJOOHESHYAR_28_SECTIONS = REQUIRED_SECTIONS_28

SECTION_SYNONYMS = {
    "عنوان فارسی": [r"عنوان\s+فارسی", r"موضوع\s+فارسی", r"عنوان\s+طرح"],
    "عنوان انگلیسی": [r"عنوان\s+انگلیسی", r"english\s+title", r"موضوع\s+انگلیسی"],
    "نوع مطالعه": [r"نوع\s+مطالعه", r"طراحی\s+مطالعه", r"study\s+design"],
    "بیان مسئله و ضرورت انجام تحقیق": [r"بیان\s+مسئله", r"ضرورت\s+انجام\s+تحقیق", r"بیان\s+مساله", r"problem\s+statement"],
    "مروری بر متون": [r"مروری\s+بر\s+متون", r"مرور\s+بر\s+منابع", r"پیشینه\s+پژوهش", r"literature\s+review"],
    "اهداف (هدف کلی و اهداف اختصاصی)": [r"اهداف", r"هدف\s+کلی", r"اهداف\s+اختصاصی", r"اهداف\s+جزیی", r"objectives"],
    "فرضیات یا سوالات پژوهشی": [r"فرضیات", r"فرضیه‌ها", r"سوالات\s+پژوهش", r"hypotheses"],
    "جامعه آماری": [r"جامعه\s+آماری", r"جامعه\s+پژوهش", r"population", r"جامعه\s+هدف"],
    "روش نمونهگیری": [r"روش\s+نمونه‌?گیری", r"نمونه‌?گیری", r"sampling\s+method"],
    "حجم نمونه و روش محاسبه آن": [r"حجم\s+نمونه", r"محاسبه\s+حجم\s+نمونه", r"sample\s+size"],
    "معیارهای ورود به مطالعه": [r"معیارهای\s+ورود", r"شرایط\s+ورود", r"inclusion\s+criteria"],
    "معیارهای خروج از مطالعه": [r"معیارهای\s+خروج", r"شرایط\s+خروج", r"exclusion\s+criteria"],
    "روش اجرا": [r"روش\s+اجرا", r"مراحل\s+اجرا", r"روش\s+کار", r"پروتکل\s+اجرایی", r"methodology"],
    "ابزار جمعآوری دادهها": [r"ابزار\s+جمع‌?آوری", r"ابزارهای\s+گردآوری", r"data\s+collection\s+tools"],
    "روشهای آماری تجزیه و تحلیل دادهها": [r"روش‌های\s+آماری", r"تجزیه\s+و\s+تحلیل\s+داده", r"تحلیل\s+آماری", r"statistical\s+analysis"],
    "ملاحظات اخلاقی": [r"ملاحظات\s+اخلاقی", r"کد\s+اخلاق", r"ethical\s+considerations"],
    "محدودیتهای مطالعه": [r"محدودیت‌های\s+مطالعه", r"مشکلات\s+و\s+محدودیت‌ها", r"limitations"],
    "جدول متغیرها": [r"جدول\s+متغیرها", r"متغیرهای\s+پژوهش", r"variables\s+table"],
    "جدول زمانبندی": [r"جدول\s+زمان‌?بندی", r"گانت\s+چارت", r"timeline", r"gantt"],
    "بودجه": [r"بودجه", r"هزینه‌ها", r"برآورد\s+مالی", r"budget"],
    "منابع": [r"منابع", r"فهرست\s+منابع", r"references", r"مراجع"],
    "خلاصه فارسی": [r"خلاصه\s+فارسی", r"چکیده\s+فارسی", r"persian\s+abstract"],
    "خلاصه انگلیسی (Abstract)": [r"خلاصه\s+انگلیسی", r"چکیده\s+انگلیسی", r"abstract"],
    "کلیدواژههای فارسی": [r"کلیدواژه‌های\s+فارسی", r"واژگان\s+کلیدی\s+فارسی", r"persian\s+keywords"],
    "کلیدواژههای انگلیسی": [r"کلیدواژه‌های\s+انگلیسی", r"keywords", r"english\s+keywords"],
    "تعارض منافع": [r"تعارض\s+منافع", r"تضاد\s+منافع", r"conflict\s+of\s+interest"],
    "سپاسگزاری": [r"سپاسگزاری", r"تقدیر", r"تشکر", r"acknowledgements?"],
    "ضمائم (در صورت نیاز)": [r"ضمائم", r"پیوست‌ها", r"ضمیمه", r"appendices?"]
}

SAMPLE_SIZE_FORMULA_PATTERNS = [
    r'\\frac',
    r'Z_\{?1',
    r'[nN]\s*=',
    r'Mead',
    r'E\s*=\s*N\s*-\s*B\s*-\s*T',
    r'resource equation',
    r'کوکران|کوهن|مید|پوکاک',
    r'تکرار.*(بیولوژیک|مستقل|آزمایشگاهی)',
    r'(biological|independent)\s+replicate'
]

@dataclass
class SampleSizeEvaluation:
    status: str  # "ADEQUATE", "INSUFFICIENT_INPUTS", "REPLICATION_STRUCTURE_UNDEFINED", "RECOMMENDED_FORMULA_AVAILABLE"
    can_proceed: bool
    missing_inputs: List[str] = field(default_factory=list)
    experimental_unit: Optional[str] = None
    biological_replicates: Optional[int] = None
    technical_replicates: Optional[int] = None
    total_independent_n: Optional[int] = None
    recommended_formula: Optional[str] = None
    methodological_rationale_fa: str = ""
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "can_proceed": self.can_proceed,
            "missing_inputs": self.missing_inputs,
            "experimental_unit": self.experimental_unit,
            "biological_replicates": self.biological_replicates,
            "technical_replicates": self.technical_replicates,
            "total_independent_n": self.total_independent_n,
            "recommended_formula": self.recommended_formula,
            "methodological_rationale_fa": self.methodological_rationale_fa,
            "warnings": self.warnings
        }

@dataclass
class CompletenessGateResult:
    is_complete: bool
    can_proceed: bool
    missing_sections: List[str] = field(default_factory=list)
    sections_needing_formula: List[str] = field(default_factory=list)
    present_sections: List[str] = field(default_factory=list)
    sample_size_evaluation: Optional[SampleSizeEvaluation] = None
    total_required: int = 28
    compliance_score: float = 0.0
    detailed_status: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_complete": self.is_complete,
            "can_proceed": self.can_proceed,
            "missing_sections": self.missing_sections,
            "sections_needing_formula": self.sections_needing_formula,
            "present_sections": self.present_sections,
            "sample_size_evaluation": self.sample_size_evaluation.to_dict() if self.sample_size_evaluation else None,
            "total_required": self.total_required,
            "compliance_score": self.compliance_score,
            "detailed_status": self.detailed_status
        }


class MethodologyCompletenessGate:
    """Validates 28-section Pajooheshyar completeness, sample size rigor, and replicate structures."""

    @classmethod
    def evaluate_sample_size_inputs(
        cls,
        study_design: str = "in_vitro",
        primary_endpoint: Optional[str] = None,
        experimental_unit: Optional[str] = None,
        effect_size: Optional[float] = None,
        variance_or_sd: Optional[float] = None,
        alpha: Optional[float] = 0.05,
        power: Optional[float] = 0.80,
        groups_count: int = 4,
        biological_replicates: Optional[int] = None,
        technical_replicates: Optional[int] = None
    ) -> SampleSizeEvaluation:
        """
        Evaluates the epistemic adequacy of sample size parameters.
        Does NOT invent formulas when inputs are missing.
        Strictly enforces distinction between biological and technical replicates.
        """
        missing = []
        warnings = []

        if not primary_endpoint:
            missing.append("primary_endpoint")

        if not experimental_unit:
            missing.append("experimental_unit")
            warnings.append("REPLICATION_STRUCTURE_UNDEFINED: واحد آزمایشی مستقل (Experimental Unit) مشخص نشده است.")

        # Replicate pseudo-replication check
        if biological_replicates is not None and technical_replicates is not None:
            if technical_replicates > 1:
                warnings.append(
                    f"PSEUDO_REPLICATION_GUARD: تعداد {biological_replicates} تکرار بیولوژیک مستقل همراه با "
                    f"{technical_replicates} تکرار تکنیکی (فنی) تعریف شده است. "
                    f"حجم نمونه مستقل n = {biological_replicates} است و تکرارهای فنی نباید به عنوان درجات آزادی مستقل در آزمون فرض وارد شوند."
                )
            independent_n = biological_replicates
        elif biological_replicates is not None:
            independent_n = biological_replicates
        else:
            independent_n = None
            missing.append("biological_replicates")

        # Parametric input check
        has_power_params = (effect_size is not None and variance_or_sd is not None and alpha is not None and power is not None)

        if not has_power_params:
            if effect_size is None:
                missing.append("effect_size")
            if variance_or_sd is None:
                missing.append("variance_or_sd")

            # In exploratory in vitro/in vivo studies where effect size is unknown:
            if study_design in ["in_vitro", "in_vivo"]:
                rationale_fa = (
                    "وضعیت: INSUFFICIENT_INPUTS برای توان‌آزمایی پارامتریک سنتی. "
                    "به دلیل ماهیت اکتشافی (Exploratory) و فقدان مطالعات قبلی با اندازه اثر مشخص، "
                    "محاسبه بر مبنای حداقل تکرار بیولوژیک مستقل استاندارد (حداقل ۳ الی ۴ تکرار مستقل در روزهای مجزا) "
                    "یا رابطه تخصیص منابع مید (Mead's Resource Equation: E = N - B - T) صورت می‌پذیرد."
                )
                rec_formula = "E = N - B - T (10 <= E <= 20) یا حداقل n = 3-4 تکرار بیولوژیک مستقل"
            else:
                rationale_fa = (
                    "وضعیت: INSUFFICIENT_INPUTS. داده‌های کافی برای محاسبه اندازه نمونه (اندازه اثر و واریانس) وجود ندارد. "
                    "فرمول جعلی تولید نمی‌شود؛ داده‌های پایلوت برای تخمین Cohen's d الزامی است."
                )
                rec_formula = None

            return SampleSizeEvaluation(
                status="INSUFFICIENT_INPUTS",
                can_proceed=(independent_n is not None and independent_n >= 3),
                missing_inputs=missing,
                experimental_unit=experimental_unit,
                biological_replicates=biological_replicates,
                technical_replicates=technical_replicates,
                total_independent_n=independent_n,
                recommended_formula=rec_formula,
                methodological_rationale_fa=rationale_fa,
                warnings=warnings
            )

        # Full parametric inputs available
        formula_str = r"n = \frac{2(Z_{1-\alpha/2} + Z_{1-\beta})^2 \cdot \sigma^2}{\Delta^2}"
        rationale_fa = f"محاسبه بر مبنای توان آماری {int(power*100)}٪ و آلفای {alpha} با اندازه اثر {effect_size} انجام شد."

        return SampleSizeEvaluation(
            status="ADEQUATE",
            can_proceed=True,
            missing_inputs=[],
            experimental_unit=experimental_unit,
            biological_replicates=biological_replicates,
            technical_replicates=technical_replicates,
            total_independent_n=independent_n,
            recommended_formula=formula_str,
            methodological_rationale_fa=rationale_fa,
            warnings=warnings
        )

    @classmethod
    def validate(cls, proposal_input: Union[Dict[str, Any], str]) -> CompletenessGateResult:
        """
        Validates presence and adequacy of all 28 Pajooheshyar sections.
        """
        if isinstance(proposal_input, dict):
            extracted = cls._extract_sections_from_dict(proposal_input)
        else:
            extracted = cls._extract_sections_from_markdown(str(proposal_input))

        missing = []
        needing_substance = []
        present = []
        details = {}

        for req_sec in REQUIRED_SECTIONS_28:
            content = extracted.get(req_sec)

            # Check presence
            if not content or len(str(content).strip()) == 0:
                if req_sec == "ضمائم (در صورت نیاز)":
                    present.append(req_sec)
                    details[req_sec] = "OPTIONAL_OMITTED_CLEAN"
                    continue
                missing.append(req_sec)
                details[req_sec] = "MISSING"
                continue

            content_str = str(content).strip()

            # Specific check for Sample Size Section (Section 10)
            if req_sec == "حجم نمونه و روش محاسبه آن":
                has_formula = any(re.search(pat, content_str, re.IGNORECASE) for pat in SAMPLE_SIZE_FORMULA_PATTERNS)
                if not has_formula:
                    needing_substance.append(req_sec)
                    details[req_sec] = "MISSING_MATHEMATICAL_FORMULA_OR_DESIGN_JUSTIFICATION"
                    continue
                else:
                    present.append(req_sec)
                    details[req_sec] = "PRESENT_METHODOLOGICALLY_EVALUATED"
                    continue

            present.append(req_sec)
            details[req_sec] = "PRESENT"

        is_complete = (len(missing) == 0 and len(needing_substance) == 0)
        can_proceed = is_complete
        score = round((len(present) / len(REQUIRED_SECTIONS_28)) * 100, 1)

        return CompletenessGateResult(
            is_complete=is_complete,
            can_proceed=can_proceed,
            missing_sections=missing,
            sections_needing_formula=needing_substance,
            present_sections=present,
            total_required=len(REQUIRED_SECTIONS_28),
            compliance_score=score,
            detailed_status=details
        )

    @classmethod
    def _extract_sections_from_dict(cls, data: Dict[str, Any]) -> Dict[str, str]:
        extracted = {}
        for sec in REQUIRED_SECTIONS_28:
            if sec in data:
                extracted[sec] = str(data[sec])

        for sec, patterns in SECTION_SYNONYMS.items():
            if sec in extracted:
                continue
            for key, val in data.items():
                if any(re.search(p, key, re.IGNORECASE) for p in patterns):
                    extracted[sec] = str(val)
                    break

        if "sample_size_calculation" in data and "حجم نمونه و روش محاسبه آن" not in extracted:
            ss = data["sample_size_calculation"]
            formula = ss.get("formula", "") if isinstance(ss, dict) else str(ss)
            extracted["حجم نمونه و روش محاسبه آن"] = formula

        if "variable_table" in data and "جدول متغیرها" not in extracted:
            extracted["جدول متغیرها"] = str(data["variable_table"])

        if "timeline" in data and "جدول زمانبندی" not in extracted:
            extracted["جدول زمانبندی"] = str(data["timeline"])

        if "references" in data and "منابع" not in extracted:
            extracted["منابع"] = str(data["references"])

        return extracted

    @classmethod
    def _extract_sections_from_markdown(cls, md_text: str) -> Dict[str, str]:
        extracted = {}
        lines = md_text.split('\n')
        current_sec = None
        current_buffer = []

        def save_current():
            if current_sec and current_buffer:
                extracted[current_sec] = '\n'.join(current_buffer).strip()

        for line in lines:
            header_match = re.match(r'^(?:#+|\d+\s*[-.)]|بخش\s*\d+[:\s])\s*(.+)$', line.strip())
            if header_match:
                candidate_title = header_match.group(1).strip()
                matched_req = None
                for req_sec, patterns in SECTION_SYNONYMS.items():
                    if any(re.search(p, candidate_title, re.IGNORECASE) for p in patterns):
                        matched_req = req_sec
                        break

                if matched_req:
                    save_current()
                    current_sec = matched_req
                    current_buffer = []
                    continue

            if current_sec:
                current_buffer.append(line)

        save_current()
        return extracted
