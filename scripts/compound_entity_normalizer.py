#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compound_entity_normalizer.py - Universal Chemical & Botanical Entity Normalizer
Proposal-Nevisi Engine v9.0 (Layer 1: Scientific Accuracy)

Categorizes candidate experimental substances into standardized ontological tiers:
- PURE_COMPOUND
- STANDARDIZED_EXTRACT
- CRUDE_EXTRACT
- SYNTHETIC_ANALOG

Emits rigorous methodological warnings regarding concentration attribution,
fractionation requirements, and vehicle artifact controls.
100% General-Purpose: Zero hardcoded substance names.
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class NormalizedEntity:
    original_term: str
    normalized_name: str
    category: str
    confidence: float
    purity_specification: Optional[str] = None
    solvent_or_preparation: Optional[str] = None
    methodological_warnings: List[str] = field(default_factory=list)
    dosage_unit_recommendation: str = "molar"
    is_pure: bool = True
    is_mixture: bool = False
    chemical_or_biological_class: str = "UNSPECIFIED"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_term": self.original_term,
            "normalized_name": self.normalized_name,
            "category": self.category,
            "confidence": self.confidence,
            "purity_specification": self.purity_specification,
            "solvent_or_preparation": self.solvent_or_preparation,
            "methodological_warnings": self.methodological_warnings,
            "dosage_unit_recommendation": self.dosage_unit_recommendation,
            "is_pure": self.is_pure,
            "is_mixture": self.is_mixture,
            "chemical_or_biological_class": self.chemical_or_biological_class
        }

class CompoundEntityNormalizer:
    """Universal normalizer classifying biomedical test substances without topic bias."""

    # Patterns for Crude Extracts
    CRUDE_EXTRACT_PATTERNS = [
        r'\b(?:crude\s+extract|whole\s+extract|botanical\s+extract|total\s+extract)\b',
        r'\b(?:methanolic|ethanolic|aqueous|hexane|hydroalcoholic|dichloromethane|acetone|petroleum\s+ether|ethyl\s+acetate)\s+extract\b',
        r'\bextract\s+of\b',
        r'عصاره\s+(?:متانولی|اتانولی|آبی|هگزانی|هیدروالکلی|کلروفرمی|استات\s+اتیل|تام|خام|گیاهی|کامل)',
        r'عصاره\s+کل\b',
        r'\bعصاره\b'
    ]

    # Patterns for Standardized Extracts
    STANDARDIZED_EXTRACT_PATTERNS = [
        r'\b(?:standardi[zs]ed\s+extract|titrated\s+extract|quantified\s+extract)\b',
        r'\bextract\s+containing\s+\d+(?:\.\d+)?\s*%\b',
        r'عصاره\s+استاندارد(?:\s*شده)?',
        r'عصاره\s+تیتره(?:\s*شده)?',
        r'عصاره\s+حاوی\s+\d+(?:\.\d+)?\s*درصد'
    ]

    # Patterns for Synthetic Derivatives / Analogs
    SYNTHETIC_ANALOG_PATTERNS = [
        r'\b(?:semi-?synthetic|synthetic\s+analog(?:ue)?|chemical\s+derivative|derivatives?)\b',
        r'\b(?:ester|acetate|succinate|carbamate|quaternary\s+(?:ammonium|phosphonium)|conjugate|prodrug)\b',
        r'مشتق(?:\s+شیمیایی|\s+سنتزی)?',
        r'آنالوگ(?:\s+ساختاری|\s+سنتزی)?',
        r'پیش‌?دارو'
    ]

    # Patterns for Pure Compounds
    PURE_COMPOUND_PATTERNS = [
        r'\b(?:pure|isolated|purified|analytical\s+standard|reference\s+standard)\b',
        r'\b(?:purity|خلوص)\s*(?:>=|≥|>|درصد|%|of)?\s*\d{2}(?:\.\d+)?\s*%',
        r'\b\d{2}(?:\.\d+)?\s*%\s*(?:pure|purity|خلوص)\b',
        r'ماده\s+(?:خالص|تخلیص‌?شده|موثره\s+خالص)',
        r'ترکیب\s+خالص'
    ]

    # Solvents / Extraction media
    SOLVENT_PATTERNS = [
        (r'\bmethanol(?:ic)?\b|متانول(?:ی)?', "Methanol"),
        (r'\bethanol(?:ic)?\b|اتانول(?:ی)?', "Ethanol"),
        (r'\bhexane\b|هگزان(?:ی)?', "Hexane"),
        (r'\baqueous\b|آب(?:ی)?', "Water (Aqueous)"),
        (r'\bethyl\s+acetate\b|استات\s+اتیل', "Ethyl Acetate"),
        (r'\bdichloromethane\b|دی‌کلرومتان', "Dichloromethane"),
        (r'\bchloroform\b|کلروفرم', "Chloroform"),
        (r'\bhydroalcoholic\b|هیدروالکلی', "Hydroalcoholic")
    ]

    @classmethod
    def normalize(cls, entity_input: Any) -> NormalizedEntity:
        """
        Extracts and standardizes the entity category from text, dictionary, or string input.
        """
        if isinstance(entity_input, dict):
            raw_text = entity_input.get("name", "")
            raw_text += " " + entity_input.get("description", "")
            raw_text += " " + entity_input.get("purity", "")
            raw_text += " " + entity_input.get("formulation", "")
            orig = entity_input.get("name", str(entity_input))
        else:
            raw_text = str(entity_input)
            orig = str(entity_input)

        text_clean = raw_text.strip()
        text_lower = text_clean.lower()

        detected_solvent = None
        for s_pat, s_name in cls.SOLVENT_PATTERNS:
            if re.search(s_pat, text_lower, re.IGNORECASE):
                detected_solvent = s_name
                break

        # Check Purity Specification (e.g. >=98% purity)
        purity_match = re.search(r'(\b\d{2}(?:\.\d+)?\s*%)|(?:purity|خلوص)\s*[:=]?\s*(\d{2}(?:\.\d+)?\s*%)', text_clean, re.IGNORECASE)
        purity_spec = None
        if purity_match:
            purity_spec = (purity_match.group(1) or purity_match.group(2)).strip()

        # 1. Check Standardized Extract
        is_std_extract = any(re.search(pat, text_lower, re.IGNORECASE) for pat in cls.STANDARDIZED_EXTRACT_PATTERNS)
        if is_std_extract:
            warnings = [
                "STANDARDIZED_EXTRACT: اثر مشاهده‌شده به فرمولاسیون فیتوشیمیایی تام نسبت داده می‌شود نه یک مولکول منفرد.",
                "کنترل نوسانات دسته به دسته (Batch-to-Batch) از طریق کروماتوگرافی معتبر الزامی است."
            ]
            return NormalizedEntity(
                original_term=orig,
                normalized_name=cls._clean_name(orig),
                category="STANDARDIZED_EXTRACT",
                confidence=0.92,
                purity_specification=purity_spec,
                solvent_or_preparation=detected_solvent,
                methodological_warnings=warnings,
                dosage_unit_recommendation="mass_concentration_ug_ml",
                is_pure=False,
                is_mixture=True,
                chemical_or_biological_class="STANDARDIZED_BOTANICAL_MIXTURE"
            )

        # 2. Check Crude Extract
        is_crude_extract = any(re.search(pat, text_lower, re.IGNORECASE) for pat in cls.CRUDE_EXTRACT_PATTERNS)
        if is_crude_extract:
            warnings = [
                "CRUDE_EXTRACT_ATTRIBUTION_FALLACY: اثر مشاهده‌شده ناشی از مخلوط کمپلکس بوده و انتساب قطعی به یک مؤلفه خالص بدون جداسازی و تخلیص بیولوژیک فاقد اعتبار است.",
                "دوزاژ باید بر حسب غلظت وزنی (µg/mL یا mg/kg) بیان گردد نه غلظت مولی (µM).",
                "ارزیابی سمیت حلال استخراجی (Vehicle cytotoxicity) و حذف اثر پس‌زمینه حلال الزامی است."
            ]
            return NormalizedEntity(
                original_term=orig,
                normalized_name=cls._clean_name(orig),
                category="CRUDE_EXTRACT",
                confidence=0.95,
                purity_specification=None,
                solvent_or_preparation=detected_solvent or "Crude Solvent",
                methodological_warnings=warnings,
                dosage_unit_recommendation="mass_concentration_ug_ml",
                is_pure=False,
                is_mixture=True,
                chemical_or_biological_class="CRUDE_BOTANICAL_MIXTURE"
            )

        # 3. Check Synthetic Analog / Derivative
        is_analog = any(re.search(pat, text_lower, re.IGNORECASE) for pat in cls.SYNTHETIC_ANALOG_PATTERNS)
        if is_analog:
            warnings = [
                "SYNTHETIC_DERIVATIVE: خواص فارماکوکینتیک، حلالیت و میل ترکیبی این آنالوگ ممکن است با اسکلت مادری طبیعی متفاوت باشد.",
                "نتایج حاصل از مشتق سنتزی نباید به عنوان اثبات رفتار مولکول اولیه طبیعی تعمیم یابند."
            ]
            return NormalizedEntity(
                original_term=orig,
                normalized_name=cls._clean_name(orig),
                category="SYNTHETIC_ANALOG",
                confidence=0.90,
                purity_specification=purity_spec,
                solvent_or_preparation=detected_solvent,
                methodological_warnings=warnings,
                dosage_unit_recommendation="molar",
                is_pure=True,
                is_mixture=False,
                chemical_or_biological_class="SYNTHETIC_STRUCTURAL_ANALOGUE"
            )

        # 4. Check Explicit Pure Compound or default
        is_explicit_pure = any(re.search(pat, text_lower, re.IGNORECASE) for pat in cls.PURE_COMPOUND_PATTERNS)
        purity_val = 0.95 if is_explicit_pure else 0.85

        warnings = [
            "PURE_COMPOUND: رعایت حد مجاز حلال ناقل (DMSO <= 0.1% v/v) برای پیشگیری از سمیت پس‌زمینه الزامی است.",
            "بررسی حلالیت آبی و پیشگیری از رسوب میکروکریستالی در غلظت‌های بالا الزامی است."
        ]

        return NormalizedEntity(
            original_term=orig,
            normalized_name=cls._clean_name(orig),
            category="PURE_COMPOUND",
            confidence=purity_val,
            purity_specification=purity_spec or ">=95% Analytical Grade",
            solvent_or_preparation=detected_solvent,
            methodological_warnings=warnings,
            dosage_unit_recommendation="molar",
            is_pure=True,
            is_mixture=False,
            chemical_or_biological_class="PURE_SMALL_MOLECULE"
        )

    @staticmethod
    def _clean_name(text: str) -> str:
        clean = re.sub(r'^(?:عصاره\s+(?:متانولی|اتانولی|آبی|هگزانی|تام|خام)\s+|crude\s+extract\s+of\s+)', '', text, flags=re.IGNORECASE)
        clean = re.sub(r'\s*\([^)]*\)', '', clean)
        return clean.strip()
