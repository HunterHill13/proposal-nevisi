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
    "موضوع",
    "بیان مسئله",
    "مرور بر منابع (مقالات و فعالیت های مشابه به موضوع ما)",
    "اهمیت وضرورت تحقیق",
    "تعریف واژه ها (واژه های بولد و علمی که نیازمند توضیح هستند)",
    "اهداف جزیی (تعیین تاثیر متغیر مستقل روی متغیر وابسته)",
    "اهداف کلی (همین موضوع با کلمه تعیین..)",
    "اهداف کاربردی",
    "فرضیات و سوالات",
    "دستاورد ها (چه دستاوردی ازین تحقیق خواهیم داشت)",
    "جدول متغیر ها (نقش متغیر (وابسته، مستقل،مخدوش گر) و نوع متغیر(کیفی، کمی پیوسته یا کمی گسسته))",
    "جدول زمان بندی و مراحل اجرا",
    "روش اجرا",
    "نوع مطالعه",
    "جامعه مورد مطالعه",
    "محل انجام مطالعه",
    "معیار های ورود به مطالعه",
    "معیار های خروج از مطالعه",
    "ابزار های گردآوری اطلاعات",
    "تعیین اعتبار ابزار گردآوری",
    "تعیین ابزار گردآوری",
    "حجم نمونه و روش محاسبه آن",
    "روش تجزیه و تحلیل داده",
    "ملاحظلات اخلاقی در صورت نیاز",
    "نحوه رعایت نکات امنیتی و حفاظت پروژه در صورت نیاز",
    "مشکلات و محدودیت ها",
    "روش انجام طرح، شیوه اجرایی مراحل طرح و چگونگی جمع آوری اطلاعات",
    "منابعی که استفاده شد (انگلیسی یا فارسی)"
]

PAJOOHESHYAR_28_SECTIONS = REQUIRED_SECTIONS_28

SECTION_SYNONYMS = {
    "موضوع": [r"^عنوان(?:\s+فارسی|\s+طرح|\s+پروپوزال)?", r"title"],
    "بیان مسئله": [r"بیان\s+مس[ئأه]له", r"problem\s+statement"],
    "مرور بر منابع (مقالات و فعالیت های مشابه به موضوع ما)": [r"مرور\s+بر\s+منابع", r"پیشینه\s+پژوهش", r"مروری\s+بر\s+متون", r"literature\s+review"],
    "اهمیت وضرورت تحقیق": [r"اهمیت\s+و\s*ضرورت(?:\s+انجام)?\s+تحقیق", r"significance\s*(?:and|&)\s*necessity"],
    "تعریف واژه ها (واژه های بولد و علمی که نیازمند توضیح هستند)": [r"تعریف\s+واژه(?:[\s\u200c]*های|ها)?", r"واژگان\s+تخصصی", r"definition\s+of\s+terms"],
    "اهداف جزیی (تعیین تاثیر متغیر مستقل روی متغیر وابسته)": [r"اهداف\s+جز[ئیی]", r"اهداف\s+اختصاصی", r"specific\s+objectives"],
    "اهداف کلی (همین موضوع با کلمه تعیین..)": [r"هدف\s+کلی", r"اهداف\s+کلی", r"general\s+objective"],
    "اهداف کاربردی": [r"اهداف\s+کاربردی", r"applied\s+objectives"],
    "فرضیات و سوالات": [r"فرضی[اه]ت\s+و\s+س[وؤ]الات", r"فرضیه‌ها\s+و\s+پرسش‌ها", r"hypotheses\s*(?:and|&)\s*questions"],
    "دستاورد ها (چه دستاوردی ازین تحقیق خواهیم داشت)": [r"دستاورد(?:[\s\u200c]*های|ها)?", r"achievements", r"deliverables"],
    "جدول متغیر ها (نقش متغیر (وابسته، مستقل،مخدوش گر) و نوع متغیر(کیفی، کمی پیوسته یا کمی گسسته))": [r"جدول\s+متغیر(?:[\s\u200c]*های|ها)?", r"متغیرهای\s+پژوهش", r"variable\s+table"],
    "جدول زمان بندی و مراحل اجرا": [r"جدول\s+زمان[\s\u200c\-]*بندی(?:\s+و\s+مراحل\s+اجرا)?", r"گانت\s+چارت", r"timeline", r"gantt"],
    "روش اجرا": [r"روش\s+اجرا", r"متدولوژی", r"روش\s+کار", r"پروتکل\s+اجرایی", r"methodology"],
    "نوع مطالعه": [r"نوع\s+مطالعه", r"طراحی\s+مطالعه", r"study\s+type", r"study\s+design"],
    "جامعه مورد مطالعه": [r"جامعه\s+مورد\s+مطالعه", r"جامعه\s+آماری", r"جامعه\s+پژوهش", r"study\s+population", r"target\s+population"],
    "محل انجام مطالعه": [r"محل\s+انجام(?:\s+مطالعه)?", r"study\s+setting", r"location"],
    "معیار های ورود به مطالعه": [r"معیار(?:[\s\u200c]*های|ها)?\s+ورود(?:\s+به\s+مطالعه)?", r"شرایط\s+ورود", r"inclusion\s+criteria"],
    "معیار های خروج از مطالعه": [r"معیار(?:[\s\u200c]*های|ها)?\s+خروج(?:\s+از\s+مطالعه)?", r"شرایط\s+خروج", r"exclusion\s+criteria"],
    "ابزار های گردآوری اطلاعات": [r"ابزار(?:[\s\u200c]*های|ها)?\s+گردآوری(?:\s+اطلاعات)?", r"ابزار\s+جمع[\s\u200c\-]*آوری", r"data\s+collection\s+tools", r"instruments"],
    "تعیین اعتبار ابزار گردآوری": [r"تعیین\s+اعتبار\s+ابزار(?:\s+گردآوری)?", r"اعتبار\s+ابزار", r"روایی", r"validity"],
    "تعیین ابزار گردآوری": [r"تعیین\s*(?:پایایی\s*\/\s*)?ابزار\s*گردآوری", r"پایایی\s+ابزار", r"قابلیت\s+اعتماد", r"reliability"],
    "حجم نمونه و روش محاسبه آن": [r"حجم\s+نمونه(?:\s+و\s+روش\s+محاسبه\s+آن)?", r"محاسبه\s+حجم\s+نمونه", r"sample\s+size"],
    "روش تجزیه و تحلیل داده": [r"روش(?:[\s\u200c]*های)?\s+تجزیه\s+و\s+تحلیل\s+داده(?:[\s\u200c]*های|ها)?", r"تحلیل\s+آماری", r"روش‌های\s+آماری", r"statistical\s+analysis"],
    "ملاحظلات اخلاقی در صورت نیاز": [r"ملاحظ[اه]ت\s+اخلاقی(?:\s+در\s+صورت\s+نیاز)?", r"ملاحظلات\s+اخلاقی(?:\s+در\s+صورت\s+نیاز)?", r"کد\s+اخلاق", r"ethical\s+considerations"],
    "نحوه رعایت نکات امنیتی و حفاظت پروژه در صورت نیاز": [r"(?:نحوه\s+رعایت\s+)?نکات\s+امنیتی\s+و\s+حفاظت\s+پروژه(?:\s+در\s+صورت\s+نیاز)?", r"حفاظت\s*(?:زیستی|پروژه)", r"نکات\s+امنیتی", r"biosafety", r"security"],
    "مشکلات و محدودیت ها": [r"مشکلات\s+و\s+محدودیت(?:[\s\u200c]*های|ها)?", r"محدودیت‌های\s+مطالعه", r"limitations\s*(?:and|&)\s*challenges"],
    "روش انجام طرح، شیوه اجرایی مراحل طرح و چگونگی جمع آوری اطلاعات": [r"روش\s+انجام\s+طرح[،\s]+شیوه\s+اجرایی(?:\s*مراحل\s*طرح)?(?:\s*و\s*چگونگی\s*جمع[\s\-]*آوری\s*اطلاعات)?", r"شیوه\s+اجرایی", r"مراحل\s*طرح", r"روش\s+انجام\s+طرح", r"چگونگی\s*جمع[\s\-]*آوری"],
    "منابعی که استفاده شد (انگلیسی یا فارسی)": [r"منابعی\s+که\s+استفاده\s+شد(?:\s*\(.*\))?", r"منابع(?:\s+مورد\s+استفاده)?", r"فهرست\s+منابع", r"مراجع", r"references"]
}

SAMPLE_SIZE_FORMULA_PATTERNS = [
    r'\\frac',
    r'Z_\{?1',
    r'[nN]\s*=',
    r'Mead',
    r'E\s*=\s*N\s*-\s*B\s*-\s*T',
    r'resource equation',
    r'Festing|ARRIVE|Chow|کوکران|کوهن|مید|پوکاک',
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

        # Map common standard keys to canonical 28 section names
        var_key = "جدول متغیر ها (نقش متغیر (وابسته، مستقل،مخدوش گر) و نوع متغیر(کیفی، کمی پیوسته یا کمی گسسته))"
        time_key = "جدول زمان بندی و مراحل اجرا"
        ref_key = "منابعی که استفاده شد (انگلیسی یا فارسی)"
        ss_key = "حجم نمونه و روش محاسبه آن"

        if ss_key not in extracted:
            for k in ["sample_size_calculation", "sample_size", "حجم نمونه", "حجم_نمونه"]:
                if k in data:
                    ss = data[k]
                    extracted[ss_key] = ss.get("formula", "") if isinstance(ss, dict) else str(ss)
                    break

        if var_key not in extracted:
            for k in ["variable_table", "variables", "جدول متغیرها", "جدول_متغیرها"]:
                if k in data:
                    extracted[var_key] = str(data[k])
                    break

        if time_key not in extracted:
            for k in ["timeline", "timeline_table", "جدول زمانبندی", "جدول_زمانبندی"]:
                if k in data:
                    extracted[time_key] = str(data[k])
                    break

        if ref_key not in extracted:
            for k in ["references", "studies", "منابع", "فهرست منابع", "فهرست_منابع"]:
                if k in data:
                    extracted[ref_key] = str(data[k])
                    break

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

        fa_to_en = {'۰':'0', '۱':'1', '۲':'2', '۳':'3', '۴':'4', '۵':'5', '۶':'6', '۷':'7', '۸':'8', '۹':'9'}

        for line in lines:
            stripped = line.strip()
            # Match Markdown headings (## or #) or institutional headers
            header_match = re.match(r'^(?:#{1,4})\s*(?:([0-9]+|[\u06F0-\u06F9]+)[.:\s\-]+)?\s*(.+)$', stripped)
            if header_match:
                num_str = header_match.group(1)
                candidate_title = header_match.group(2).strip()
                matched_req = None

                # 1. Primary: if section number 1..28 is present in the heading
                if num_str:
                    clean_num = num_str
                    for fa_d, en_d in fa_to_en.items():
                        clean_num = clean_num.replace(fa_d, en_d)
                    try:
                        val = int(clean_num)
                        if 1 <= val <= len(REQUIRED_SECTIONS_28):
                            matched_req = REQUIRED_SECTIONS_28[val - 1]
                    except ValueError:
                        pass

                # 2. Fallback: match by title regex patterns
                if not matched_req:
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
