#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
methodology_completeness_gate.py - Pajooheshyar 28-Section Methodology Completeness Gate
Proposal-Nevisi Engine v9.0 (Layer 2: Structural Compliance)

Enforces complete compliance with the 28 mandatory sections of the official
Iranian Biomedical Research Information System (Pajooheshyar / Ministry of Health).
Requires mandatory mathematical formula in Sample Size calculation.
100% General-Purpose: Zero hardcoded topics.
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
    "حجم نمونه و روش محاسبه آن",  # فرمول Cohen یا Mead یا مشابه، اجباری
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

# Aliases and normalization patterns for section recognition
SECTION_SYNONYMS = {
    "عنوان فارسی": [r"عنوان\s+فارسی", r"موضوع\s+فارسی", r"عنوان\s+طرح"],
    "عنوان انگلیسی": [r"عنوان\s+انگلیسی", r"english\s+title", r"موضوع\s+انگلیسی"],
    "نوع مطالعه": [r"نوع\s+مطالعه", r"طراحی\s+مطالعه", r"study\s+design"],
    "بیان مسئله و ضرورت انجام تحقیق": [r"بیان\s+مسئله", r"ضرورت\s+انجام\s+تحقیق", r"بیان\s+مساله", r"problem\s+statement"],
    "مروری بر متون": [r"مروری\s+بر\s+متون", r"مرور\s+بر\s+منابع", r"پیشینه\s+پژوهش", r"literature\s+review"],
    "اهداف (هدف کلی و اهداف اختصاصی)": [r"اهداف", r"هدف\s+کلی", r"اهداف\s+اختصاصی", r"اهداف\s+جزیی", r"objectives"],
    "فرضیات یا سوالات پژوهشی": [r"فرضیات", r"سوالات\s+پژوهشی", r"پرسش‌های\s+پژوهش", r"hypotheses"],
    "جامعه آماری": [r"جامعه\s+آماری", r"جامعه\s+مورد\s+مطالعه", r"target\s+population"],
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

# Mathematical formula detection patterns for Sample Size
SAMPLE_SIZE_FORMULA_PATTERNS = [
    r'n\s*=',
    r'N\s*=',
    r'E\s*=\s*N\s*-\s*B\s*-\s*T',  # Mead's resource equation
    r'\\frac\{',
    r'z_\{?\\alpha',
    r'Z_\{?\\alpha',
    r'z_\{\\alpha',
    r'\bCohen\b',
    r'\bCochran\b',
    r'\bMead\b',
    r'فرمول\s+(?:کوکران|کوهن|مید|محاسبه)',
    r'(?:z_\alpha|z_\beta)',
    r'\(Z_\{?1-\\alpha',
    r'n\s*=\s*\frac',
    r'n\s*=\s*\(',
    r'd\s*=\s*\\frac'
]

@dataclass
class CompletenessGateResult:
    is_complete: bool
    can_proceed: bool
    missing_sections: List[str] = field(default_factory=list)
    sections_needing_formula: List[str] = field(default_factory=list)
    present_sections: List[str] = field(default_factory=list)
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
            "total_required": self.total_required,
            "compliance_score": self.compliance_score,
            "detailed_status": self.detailed_status
        }

class MethodologyCompletenessGate:
    """Validates full structural and mathematical compliance against 28 Pajooheshyar sections."""

    @classmethod
    def validate(cls, proposal_input: Union[Dict[str, Any], str]) -> CompletenessGateResult:
        """
        Validates completeness from dictionary or markdown text.
        """
        if isinstance(proposal_input, str):
            extracted = cls._extract_sections_from_markdown(proposal_input)
        elif isinstance(proposal_input, dict):
            extracted = cls._extract_sections_from_dict(proposal_input)
        else:
            raise TypeError("proposal_input must be dict or markdown string")

        missing = []
        needing_formula = []
        present = []
        details = {}

        for req_sec in REQUIRED_SECTIONS_28:
            content = extracted.get(req_sec)
            
            # Check presence
            if not content or len(str(content).strip()) == 0:
                if req_sec == "ضمائم (در صورت نیاز)":
                    # Optional section, if missing record as optional present
                    present.append(req_sec)
                    details[req_sec] = "OPTIONAL_OMITTED_CLEAN"
                    continue
                missing.append(req_sec)
                details[req_sec] = "MISSING"
                continue

            content_str = str(content).strip()

            # Specific check for sample size formula
            if req_sec == "حجم نمونه و روش محاسبه آن":
                has_formula = any(re.search(pat, content_str, re.IGNORECASE) for pat in SAMPLE_SIZE_FORMULA_PATTERNS)
                if not has_formula:
                    needing_formula.append(req_sec)
                    details[req_sec] = "MISSING_MATHEMATICAL_FORMULA"
                    continue
                else:
                    present.append(req_sec)
                    details[req_sec] = "VALID_WITH_FORMULA"
                    continue

            present.append(req_sec)
            details[req_sec] = "PRESENT"

        is_complete = (len(missing) == 0 and len(needing_formula) == 0)
        can_proceed = is_complete
        score = round((len(present) / len(REQUIRED_SECTIONS_28)) * 100, 1)

        return CompletenessGateResult(
            is_complete=is_complete,
            can_proceed=can_proceed,
            missing_sections=missing,
            sections_needing_formula=needing_formula,
            present_sections=present,
            total_required=len(REQUIRED_SECTIONS_28),
            compliance_score=score,
            detailed_status=details
        )

    @classmethod
    def _extract_sections_from_dict(cls, data: Dict[str, Any]) -> Dict[str, str]:
        extracted = {}
        # Direct matches
        for sec in REQUIRED_SECTIONS_28:
            if sec in data:
                extracted[sec] = str(data[sec])

        # Synonyms and nested keys
        for sec, patterns in SECTION_SYNONYMS.items():
            if sec in extracted:
                continue
            for key, val in data.items():
                if any(re.search(p, key, re.IGNORECASE) for p in patterns):
                    extracted[sec] = str(val)
                    break

        # Check special structured fields
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

        header_regex = re.compile(r'^(?:#+|\*+|\-|\d+[\.-])\s*(.+?)(?::|\s*$)')

        for line in lines:
            line_str = line.strip()
            # Match heading
            if line_str.startswith('#') or re.match(r'^\d+[\.-]\s+', line_str):
                # Identify which section
                matched_sec = None
                for sec, patterns in SECTION_SYNONYMS.items():
                    if any(re.search(p, line_str, re.IGNORECASE) for p in patterns):
                        matched_sec = sec
                        break

                if matched_sec:
                    if current_sec:
                        extracted[current_sec] = "\n".join(current_buffer).strip()
                    current_sec = matched_sec
                    current_buffer = []
                    continue

            if current_sec:
                current_buffer.append(line)

        if current_sec:
            extracted[current_sec] = "\n".join(current_buffer).strip()

        return extracted

methodology_completeness_gate = MethodologyCompletenessGate
