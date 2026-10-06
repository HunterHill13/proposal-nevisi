#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compound_entity_normalizer.py - Universal Chemical & Botanical Entity Ontology Normalizer
Proposal-Nevisi Engine v9.1 (Layer 1: Scientific Accuracy)

Categorizes candidate experimental substances into rigorous ontological tiers:
- PURE_PARENT_COMPOUND
- DERIVATIVE
- CONJUGATE
- SALT_OR_FORMULATION
- STANDARDIZED_EXTRACT
- CRUDE_EXTRACT
- RELATED_COMPOUND
- UNKNOWN

Disentangles parent compound identity from analytical purity:
Mentioning a compound by name (e.g. 'Compound_X') establishes PARENT_COMPOUND identity,
but does NOT imply analytical purity >= 95% unless explicitly quantified.
100% General-Purpose: Zero hardcoded substance names.
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class NormalizedEntity:
    original_term: str
    normalized_name: str
    category: str  # PURE_PARENT_COMPOUND, DERIVATIVE, CONJUGATE, SALT_OR_FORMULATION, STANDARDIZED_EXTRACT, CRUDE_EXTRACT, RELATED_COMPOUND, UNKNOWN
    confidence: float
    parent_compound_identity: str
    chemical_form: str  # PARENT_MOLECULE, ESTER, ACETATE, SALT, NANOPARTICLE, EXTRACT_MIXTURE, UNKNOWN
    derivative_status: str  # NATURAL_PARENT, SEMI_SYNTHETIC_DERIVATIVE, SYNTHETIC_ANALOGUE, BIOCONJUGATE, NON_DERIVATIVE
    analytical_purity: str  # e.g. ">=98%", "95%", "NOT_REPORTED"
    formulation: str  # NEAT_COMPOUND, SOLUTION, STANDARDIZED_FRACTION, CRUDE_MIXTURE, UNKNOWN
    extract_status: str  # NON_EXTRACT, STANDARDIZED_EXTRACT, CRUDE_EXTRACT
    chemically_defined: bool
    is_parent_compound: bool
    purity_specification: Optional[str] = None
    solvent_or_preparation: Optional[str] = None
    methodological_warnings: List[str] = field(default_factory=list)
    dosage_unit_recommendation: str = "molar"
    is_pure: bool = False  # True ONLY if analytically pure (>=95% reported) OR verified pure parent
    is_mixture: bool = False
    chemical_or_biological_class: str = "UNSPECIFIED"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_term": self.original_term,
            "normalized_name": self.normalized_name,
            "category": self.category,
            "confidence": self.confidence,
            "parent_compound_identity": self.parent_compound_identity,
            "chemical_form": self.chemical_form,
            "derivative_status": self.derivative_status,
            "analytical_purity": self.analytical_purity,
            "formulation": self.formulation,
            "extract_status": self.extract_status,
            "chemically_defined": self.chemically_defined,
            "is_parent_compound": self.is_parent_compound,
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

    # Patterns for Crude Botanical / Biological Extracts
    CRUDE_EXTRACT_PATTERNS = [
        r'\b(?:crude\s+extract|whole\s+extract|botanical\s+extract|total\s+extract)\b',
        r'\b(?:methanolic|ethanolic|aqueous|hexane|hydroalcoholic|dichloromethane|acetone|petroleum\s+ether|ethyl\s+acetate)\s+extract\b',
        r'\bextract\s+of\b',
        r'عصاره\s+(?:متانولی|اتانولی|آبی|هگزانی|هیدروالکلی|کلروفرمی|استات\s+اتیل|تام|خام|گیاهی|کامل)',
        r'عصاره\s+کل\b',
        r'\bعصاره\b'
    ]

    # Patterns for Standardized / Titrated Extracts
    STANDARDIZED_EXTRACT_PATTERNS = [
        r'\b(?:standardi[zs]ed\s+extract|titrated\s+extract|quantified\s+extract|enriched\s+fraction)\b',
        r'\bextract\s+containing\s+\d+(?:\.\d+)?\s*%\b',
        r'عصاره\s+استاندارد(?:\s*شده)?',
        r'عصاره\s+تیتره(?:\s*شده)?',
        r'عصاره\s+حاوی\s+\d+(?:\.\d+)?\s*درصد'
    ]

    # Patterns for Bioconjugates / Nanoparticles
    CONJUGATE_PATTERNS = [
        r'\b(?:conjugate|conjugated|nanoparticle|liposom(?:e|al)|micell(?:e|ar)|polymeric\s+carrier|pegylated)\b',
        r'نانوذره',
        r'لیپوزوم',
        r'کونژوگه'
    ]

    # Patterns for Synthetic Derivatives / Analogs
    SYNTHETIC_ANALOG_PATTERNS = [
        r'\b(?:semi-?synthetic|synthetic\s+analog(?:ue)?|chemical\s+derivative|derivatives?|analog(?:ue)?s?)\b',
        r'\b(?:acetate|ester|succinate|carbamate|linoleate|palmitate|oleate|benzoate|stearate|propionate|butyrate|prodrug)\b',
        r'مشتق(?:\s+شیمیایی|\s+سنتزی)?',
        r'آنالوگ(?:\s+ساختاری|\s+سنتزی)?',
        r'پیش‌?دارو'
    ]

    # Patterns for Salts and Formulations
    SALT_FORMULATION_PATTERNS = [
        r'\b(?:hydrochloride|sulfate|sodium|potassium|citrate|tartrate|fumarate|maleate|besylate|mesylate|salt)\b',
        r'نمک\s+(?:هیدروکلراید|سولفات|سدیم|سیترات)'
    ]

    # Patterns for Explicit Pure Compounds (with stated purity or analytical standard)
    EXPLICIT_PURE_PATTERNS = [
        r'\b(?:isolated|purified|analytical\s+standard|reference\s+standard|pure\s+compound|chromatographically\s+pure)\b',
        r'\b(?:purity|خلوص)\s*(?:>=|≥|>|درصد|%|of)?\s*\d{2}(?:\.\d+)?\s*%',
        r'\b\d{2}(?:\.\d+)?\s*%\s*(?:pure|purity|خلوص)\b',
        r'ماده\s+(?:تخلیص‌?شده|موثره\s+خالص|استاندارد\s+مرجع)',
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
        (r'\bhydroalcoholic\b|هیدروالکلی', "Hydroalcoholic"),
        (r'\bdmso\b|دی‌متیل‌سولفوکسید', "DMSO")
    ]

    @classmethod
    def normalize(cls, entity_input: Any) -> NormalizedEntity:
        """
        Extracts and standardizes the entity category from text, dictionary, or string input.
        Separates parent compound identity from analytical purity.
        """
        if isinstance(entity_input, dict):
            raw_text = entity_input.get("name", "")
            raw_text += " " + entity_input.get("description", "")
            raw_text += " " + entity_input.get("purity", "")
            raw_text += " " + entity_input.get("formulation", "")
            orig = entity_input.get("name", str(entity_input))
            explicit_purity = entity_input.get("purity")
        else:
            raw_text = str(entity_input)
            orig = str(entity_input)
            explicit_purity = None

        text_clean = raw_text.strip()
        text_lower = text_clean.lower()
        cleaned_parent_name = cls._clean_name(orig)

        # Detect solvent
        detected_solvent = None
        for s_pat, s_name in cls.SOLVENT_PATTERNS:
            if re.search(s_pat, text_lower, re.IGNORECASE):
                detected_solvent = s_name
                break

        # Check explicit analytical purity (e.g. >=98% purity)
        purity_match = re.search(r'(\b\d{2}(?:\.\d+)?\s*%)|(?:purity|خلوص)\s*[:=]?\s*(\d{2}(?:\.\d+)?\s*%)', text_clean, re.IGNORECASE)
        analytical_purity = "NOT_REPORTED"
        purity_spec = None
        if explicit_purity:
            analytical_purity = str(explicit_purity).strip()
            purity_spec = analytical_purity
        elif purity_match:
            purity_spec = (purity_match.group(1) or purity_match.group(2)).strip()
            analytical_purity = purity_spec

        # 1. Check Standardized Extract
        is_std_extract = any(re.search(pat, text_lower, re.IGNORECASE) for pat in cls.STANDARDIZED_EXTRACT_PATTERNS)
        if is_std_extract:
            warnings = [
                "STANDARDIZED_EXTRACT: اثر مشاهده‌شده به فرمولاسیون فیتوشیمیایی تام نسبت داده می‌شود نه یک مولکول منفرد.",
                "کنترل نوسانات دسته به دسته (Batch-to-Batch) از طریق کروماتوگرافی معتبر الزامی است."
            ]
            return NormalizedEntity(
                original_term=orig,
                normalized_name=cleaned_parent_name,
                category="STANDARDIZED_EXTRACT",
                confidence=0.92,
                parent_compound_identity=cleaned_parent_name,
                chemical_form="EXTRACT_MIXTURE",
                derivative_status="NON_DERIVATIVE",
                analytical_purity=analytical_purity,
                formulation="STANDARDIZED_FRACTION",
                extract_status="STANDARDIZED_EXTRACT",
                chemically_defined=False,
                is_parent_compound=False,
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
                normalized_name=cleaned_parent_name,
                category="CRUDE_EXTRACT",
                confidence=0.95,
                parent_compound_identity=cleaned_parent_name,
                chemical_form="EXTRACT_MIXTURE",
                derivative_status="NON_DERIVATIVE",
                analytical_purity="NOT_APPLICABLE_MIXTURE",
                formulation="CRUDE_MIXTURE",
                extract_status="CRUDE_EXTRACT",
                chemically_defined=False,
                is_parent_compound=False,
                purity_specification=None,
                solvent_or_preparation=detected_solvent or "Crude Solvent",
                methodological_warnings=warnings,
                dosage_unit_recommendation="mass_concentration_ug_ml",
                is_pure=False,
                is_mixture=True,
                chemical_or_biological_class="CRUDE_BOTANICAL_MIXTURE"
            )

        # 3. Check Conjugate / Nanoparticle Formulation
        is_conjugate = any(re.search(pat, text_lower, re.IGNORECASE) for pat in cls.CONJUGATE_PATTERNS)
        if is_conjugate:
            warnings = [
                "CONJUGATE_FORMULATION: رهایش دارو، نفوذ سلولی و فارماکوکینتیک این فرمولاسیون با مولکول آزاد متفاوت است.",
                "داده‌های مهار یا IC50 نمی‌تواند مستقیماً به ماده آزاد نسبت داده شود."
            ]
            return NormalizedEntity(
                original_term=orig,
                normalized_name=cleaned_parent_name,
                category="CONJUGATE",
                confidence=0.90,
                parent_compound_identity=cleaned_parent_name,
                chemical_form="BIOCONJUGATE_OR_NANOPARTICLE",
                derivative_status="BIOCONJUGATE",
                analytical_purity=analytical_purity,
                formulation="NANOFORMULATION",
                extract_status="NON_EXTRACT",
                chemically_defined=True,
                is_parent_compound=False,
                purity_specification=purity_spec,
                solvent_or_preparation=detected_solvent,
                methodological_warnings=warnings,
                dosage_unit_recommendation="molar",
                is_pure=False,
                is_mixture=False,
                chemical_or_biological_class="NANOCARRIER_OR_CONJUGATE"
            )

        # 4. Check Synthetic Analog / Derivative
        is_analog = any(re.search(pat, text_lower, re.IGNORECASE) for pat in cls.SYNTHETIC_ANALOG_PATTERNS)
        if is_analog:
            warnings = [
                "SYNTHETIC_DERIVATIVE: خواص فارماکوکینتیک، حلالیت و میل ترکیبی این آنالوگ ممکن است با اسکلت مادری طبیعی متفاوت باشد.",
                "نتایج حاصل از مشتق سنتزی نباید به عنوان اثبات رفتار مولکول اولیه طبیعی تعمیم یابند."
            ]
            return NormalizedEntity(
                original_term=orig,
                normalized_name=cleaned_parent_name,
                category="SYNTHETIC_ANALOG",
                confidence=0.90,
                parent_compound_identity=cleaned_parent_name,
                chemical_form="MODIFIED_ANALOGUE",
                derivative_status="SYNTHETIC_ANALOGUE",
                analytical_purity=analytical_purity,
                formulation="NEAT_COMPOUND",
                extract_status="NON_EXTRACT",
                chemically_defined=True,
                is_parent_compound=False,  # NOT the parent compound
                purity_specification=purity_spec,
                solvent_or_preparation=detected_solvent,
                methodological_warnings=warnings,
                dosage_unit_recommendation="molar",
                is_pure=False,  # Not the pure parent compound
                is_mixture=False,
                chemical_or_biological_class="SYNTHETIC_STRUCTURAL_ANALOGUE"
            )

        # 5. Check Salt or Specific Formulation
        is_salt = any(re.search(pat, text_lower, re.IGNORECASE) for pat in cls.SALT_FORMULATION_PATTERNS)
        if is_salt:
            return NormalizedEntity(
                original_term=orig,
                normalized_name=cleaned_parent_name,
                category="SALT_OR_FORMULATION",
                confidence=0.92,
                parent_compound_identity=cleaned_parent_name,
                chemical_form="SALT_FORMULATION",
                derivative_status="SALT_FORM",
                analytical_purity=analytical_purity,
                formulation="SALT",
                extract_status="NON_EXTRACT",
                chemically_defined=True,
                is_parent_compound=True,
                purity_specification=purity_spec,
                solvent_or_preparation=detected_solvent,
                methodological_warnings=["وزن مولکولی نمک در محاسبات غلظت مولی مد نظر قرار گیرد."],
                dosage_unit_recommendation="molar",
                is_pure=(analytical_purity != "NOT_REPORTED"),
                is_mixture=False,
                chemical_or_biological_class="PHARMACEUTICAL_SALT"
            )

        # 6. Parent Compound (Default for chemical names)
        # Check if analytical purity was explicitly reported
        is_explicit_pure = any(re.search(pat, text_lower, re.IGNORECASE) for pat in cls.EXPLICIT_PURE_PATTERNS)
        
        warnings = [
            "PURE_COMPOUND: رعایت حد مجاز حلال ناقل (DMSO <= 0.1% v/v) برای پیشگیری از سمیت پس‌زمینه الزامی است.",
            "بررسی حلالیت آبی و پیشگیری از رسوب میکروکریستالی در غلظت‌های بالا الزامی است."
        ]

        if analytical_purity == "NOT_REPORTED" and not is_explicit_pure:
            warnings.append(
                "ANALYTICAL_PURITY_UNSPECIFIED: خلوص تحلیلی ماده در متن ذکر نشده است؛ "
                "هویت مولکولی به عنوان ماده مادر (Parent Compound) تایید می‌شود اما خلوص در وضعیت NOT_REPORTED قرار دارد."
            )
            has_analytical_proof = False
        else:
            has_analytical_proof = True

        return NormalizedEntity(
            original_term=orig,
            normalized_name=cleaned_parent_name,
            category="PURE_COMPOUND",  # backward-compatible with v9.0 checks expecting PURE_COMPOUND
            confidence=0.95 if is_explicit_pure else 0.85,
            parent_compound_identity=cleaned_parent_name,
            chemical_form="PARENT_MOLECULE",
            derivative_status="NATURAL_PARENT",
            analytical_purity=analytical_purity,
            formulation="NEAT_COMPOUND",
            extract_status="NON_EXTRACT",
            chemically_defined=True,
            is_parent_compound=True,
            purity_specification=purity_spec,  # NOT defaulting to ">=95%" if unstated!
            solvent_or_preparation=detected_solvent,
            methodological_warnings=warnings,
            dosage_unit_recommendation="molar",
            is_pure=has_analytical_proof,
            is_mixture=False,
            chemical_or_biological_class="PURE_SMALL_MOLECULE"
        )

    @staticmethod
    def _clean_name(text: str) -> str:
        clean = re.sub(r'^(?:عصاره\s+(?:متانولی|اتانولی|آبی|هگزانی|تام|خام)\s+|crude\s+extract\s+of\s+)', '', text, flags=re.IGNORECASE)
        clean = re.sub(r'\s*\([^)]*\)', '', clean)
        return clean.strip()
