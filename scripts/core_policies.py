#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core_policies.py - Single Source of Truth Policy & Configuration Registry
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

Centralizes all non-negotiable institutional structures, temporal constraints,
evidence scales, search boundaries, and study-design taxonomy.
Guarantees zero divergence across validator, docx builder, proposal generator,
auditors, and test suites.
"""

from typing import Dict, List, Tuple, Any

# ==============================================================================
# 1. INSTITUTIONAL 14-SECTION PROPOSAL STRUCTURE (NON-NEGOTIABLE)
# ==============================================================================

MANDATORY_14_SECTIONS: List[Tuple[int, str, List[str]]] = [
    (1, "موضوع", [r"موضوع", r"عنوان", r"title"]),
    (2, "بیان مسئله", [r"بیان\s*مس[ئأه]له", r"problem\s*statement"]),
    (3, "مرور بر منابع", [r"مرور\s*بر\s*منابع", r"پیشینه\s*پژوهش", r"literature\s*review"]),
    (4, "اهمیت و ضرورت تحقیق", [r"اهمیت\s*و\s*ضرورت", r"significance\s*(?:and|&)\s*necessity"]),
    (5, "تعریف واژه‌ها", [r"تعریف\s*واژه(?:‌ها|ها)?", r"definition\s*of\s*terms"]),
    (6, "اهداف جزیی", [r"اهداف\s*جز[ئیی]", r"specific\s*objectives"]),
    (7, "اهداف کلی", [r"هدف\s*کلی", r"اهداف\s*کلی", r"general\s*objective"]),
    (8, "اهداف کاربردی", [r"اهداف\s*کاربردی", r"applied\s*objectives"]),
    (9, "فرضیات و سوالات", [r"فرضی[اه]ت\s*و\s*س[وؤ]الات", r"فرضیه‌ها\s*و\s*پرسش‌ها", r"hypotheses\s*(?:and|&)\s*questions"]),
    (10, "دستاوردها", [r"دستاوردها", r"achievements", r"deliverables"]),
    (11, "جدول متغیرها", [r"جدول\s*متغیرها", r"متغیرها", r"variable\s*table"]),
    (12, "جدول زمان‌بندی و مراحل اجرا", [r"جدول\s*زمان[\s\-]*بندی", r"مراحل\s*اجرا", r"timeline", r"gantt\s*chart"]),
    (13, "روش اجرا", [r"روش\s*اجرا", r"متدولوژی", r"methodology"]),
    (14, "منابع مورد استفاده", [r"منابع\s*(?:مورد\s*استفاده)?", r"فهرست\s*منابع", r"references"])
]

# Section 13 Sub-sections: 13-1 to 13-14 (Non-Negotiable)
MANDATORY_SUBSECTIONS_13: List[Tuple[str, str, List[str]]] = [
    ("13-1", "نوع مطالعه", [r"نوع\s*مطالعه", r"study\s*type", r"study\s*design"]),
    ("13-2", "جامعه مورد مطالعه", [r"جامعه\s*مورد\s*مطالعه", r"study\s*population", r"target\s*population"]),
    ("13-3", "محل انجام مطالعه", [r"محل\s*انجام", r"study\s*setting", r"location"]),
    ("13-4", "معیارهای ورود به مطالعه", [r"معیارهای\s*ورود", r"inclusion\s*criteria"]),
    ("13-5", "معیارهای خروج از مطالعه", [r"معیارهای\s*خروج", r"exclusion\s*criteria"]),
    ("13-6", "ابزارهای گردآوری اطلاعات", [r"ابزارهای\s*گردآوری", r"data\s*collection\s*instruments"]),
    ("13-7", "تعیین اعتبار ابزار گردآوری", [r"اعتبار\s*ابزار", r"روایی", r"validity"]),
    ("13-8", "تعیین پایایی / قابلیت اعتماد ابزار در صورت نیاز", [r"پایایی", r"قابلیت\s*اعتماد", r"reliability"]),
    ("13-9", "حجم نمونه و روش محاسبه آن", [r"حجم\s*نمونه", r"sample\s*size"]),
    ("13-10", "روش تجزیه و تحلیل داده", [r"تجزیه\s*و\s*تحلیل\s*داده", r"تحلیل\s*آماری", r"statistical\s*analysis"]),
    ("13-11", "ملاحظات اخلاقی در صورت نیاز", [r"ملاحظات\s*اخلاقی", r"ethical\s*considerations"]),
    ("13-12", "نحوه رعایت نکات امنیتی و حفاظت پروژه در صورت نیاز", [r"حفاظت\s*(?:زیستی|پروژه)", r"نکات\s*امنیتی", r"biosafety", r"security"]),
    ("13-13", "مشکلات و محدودیت‌ها", [r"مشکلات\s*و\s*محدودیت", r"limitations\s*(?:and|&)\s*challenges"]),
    ("13-14", "روش انجام طرح، شیوه اجرایی مراحل طرح و چگونگی جمع‌آوری اطلاعات", [r"شیوه\s*اجرایی", r"مراحل\s*طرح", r"روش\s*انجام\s*طرح", r"چگونگی\s*جمع[\s\-]*آوری"])
]

# Minimum content expectations per section to enforce adequate depth
SECTION_CONTENT_EXPECTATIONS: Dict[int, Dict[str, Any]] = {
    1: {"min_words": 10, "required_fields": ["fa_title", "en_title"]},
    2: {"min_words": 500, "min_paragraphs": 4, "required_elements": ["burden_of_disease", "current_state", "biological_rationale", "contradictions_and_limits", "research_gap", "study_rationale"]},
    3: {"min_words": 600, "independent_paragraphs_per_reference": True, "cross_study_synthesis_required": True},
    4: {"min_words": 150, "structured_bullets": True},
    5: {"min_words": 100, "min_terms": 3},
    6: {"min_words": 50, "min_aims": 2},
    7: {"min_words": 20, "single_overarching_statement": True},
    8: {"min_words": 50, "applied_perspectives": True},
    9: {"min_words": 50, "two_sided_hypotheses": True},
    10: {"min_words": 80, "tangible_deliverables": True},
    11: {"min_variables": 3, "required_columns": ["name", "role", "type", "operational_def", "measurement", "unit"]},
    12: {"min_phases": 4, "gantt_chart_required": True},
    13: {"min_subsections": 14, "min_words": 500},
    14: {"min_references": 15, "zero_padding_rule": True}
}

# ==============================================================================
# 2. TEMPORAL EVIDENCE POLICY CONFIGURATION
# ==============================================================================

class TemporalPolicyConfig:
    CURRENT_OPERATING_YEAR: int = 2026
    MAX_PRIMARY_EVIDENCE_AGE_YEARS: int = 6
    PRIMARY_EVIDENCE_CUTOFF_YEAR: int = 2020  # CURRENT_OPERATING_YEAR - 6
    MINIMUM_RECENT_PRIMARY_PROPORTION: float = 0.75  # >= 75% of main evidence must be recent

    APPROVED_FOUNDATIONAL_CATEGORIES: Dict[str, str] = {
        "FOUNDATIONAL_MATHEMATICAL_MODEL": "Seminal mathematical/pharmacological framework or synergy equation",
        "ORIGINAL_DIAGNOSTIC_CRITERIA": "Landmark international diagnostic criteria (e.g. WHO staging criteria, Gold Standard)",
        "SEMINAL_DISCOVERY": "First isolation/discovery of virus, gene, receptor, or biological pathway",
        "STANDARDIZED_ASSAY_METHOD": "Seminal assay methodology protocol still universally referenced across literature",
        "LANDMARK_HISTORICAL_BENCHMARK": "Seminal clinical trial or benchmark epidemiological cohort study",
        "ORIGINAL_CHEMICAL_SYNTHESIS": "Original extraction, NMR elucidation, or chemical synthesis of agent"
    }

# ==============================================================================
# 3. SEVEN-LEVEL CLAIM ENTAILMENT SCALE
# ==============================================================================

CLAIM_ENTAILMENT_SCALE: Dict[str, Dict[str, str]] = {
    "DIRECTLY_SUPPORTED": {
        "level": 1,
        "definition": "Primary empirical data or author conclusion explicitly affirms exact relationship, dose, model, and outcome.",
        "allowed_verbs": ["demonstrates", "shows", "confirms", "proves"]
    },
    "PARTIALLY_SUPPORTED": {
        "level": 2,
        "definition": "Evidence affirms core biological direction but differs in secondary parameter or sub-population.",
        "allowed_verbs": ["indicates", "partially supports", "suggests within tested model"]
    },
    "INDIRECTLY_SUPPORTED": {
        "level": 3,
        "definition": "Evidence from surrogate marker, analogous agent class, or upstream cascade component.",
        "allowed_verbs": ["suggests", "by analogy with", "provides indirect biological rationale"]
    },
    "INFERRED": {
        "level": 4,
        "definition": "Logical synthesis derived from two or more distinct empirical premises without direct co-testing.",
        "allowed_verbs": ["it is rationally inferred that", "synthesized evidence suggests"]
    },
    "HYPOTHESIS_ONLY": {
        "level": 5,
        "definition": "Theoretical rationale or author speculation unsupported by empirical measurement.",
        "allowed_verbs": ["we hypothesize that", "it is conjectured that"]
    },
    "UNSUPPORTED": {
        "level": 6,
        "definition": "Cited paper contains zero data, text, or rationale supporting the assertion.",
        "allowed_verbs": ["PROHIBITED - EXCISE OR RETRACT CLAIM"]
    },
    "CONTRADICTED": {
        "level": 7,
        "definition": "Cited paper's empirical findings directly refute the statement attached to citation marker.",
        "allowed_verbs": ["CRITICAL AUDIT FAILURE - HALT PIPELINE"]
    }
}

# ==============================================================================
# 4. EXTENSIBLE CONTRADICTION & NEGATIVE EVIDENCE TAXONOMY
# ==============================================================================

CONTRADICTION_TAXONOMY: Dict[str, str] = {
    "NULL_RESULT": "No statistically significant difference between intervention and comparator (p >= 0.05)",
    "NO_EFFECT": "Biological inertness; absence of phenotypic or biochemical shift at tested range",
    "ANTAGONISM": "Combined efficacy is strictly inferior to monotherapy or CI > 1.2",
    "SUBADDITIVITY": "Combined response is less than algebraic sum without overt antagonism",
    "TOXICITY": "Dose-limiting tissue necrosis, host cell lethality, or organ damage",
    "OFF_TARGET_EFFECT": "Non-specific engagement with unintended pathways or receptors",
    "RESISTANCE": "Acquired or innate loss of sensitivity, selection of escape mutations",
    "NON_RESPONSE": "Primary non-responsiveness within specific genetic or clinical subsets",
    "SAFETY_LIMITATION": "Narrow therapeutic window; overlapping MTD and biologically active dose",
    "DOSE_LIMITATION": "Activity restricted to supra-physiological, clinically unachievable levels",
    "TIME_LIMITATION": "Rapidly transient effect due to receptor desensitization or negative feedback",
    "MODEL_LIMITATION": "Efficacy demonstrated in 2D cell cultures but completely failed in 3D or in vivo models",
    "TRANSLATIONAL_FAILURE": "Preclinical in vitro / animal efficacy failed to translate to clinical benefit",
    "METHODOLOGICAL_CONFLICT": "Apparent effect driven by optical interference, vehicle toxicity, or assay artifact",
    "CONTRADICTORY_RESULT": "Opposite biological effect observed under ostensibly identical experimental parameters"
}

# ==============================================================================
# 5. EXPANDED RESEARCH GAP TAXONOMY (14 UNIVERSAL CATEGORIES)
# ==============================================================================

UNIVERSAL_GAP_TAXONOMY: Dict[str, str] = {
    "KNOWLEDGE_GAP": "Fundamental gap in current biomedical knowledge or disease pathology",
    "EVIDENCE_GAP": "Scarcity of empirical studies evaluating specific intervention or question",
    "MECHANISTIC_GAP": "Incomplete signaling pathway elucidation or unverified intermediate cascades",
    "METHODOLOGICAL_GAP": "Reliance on legacy assays lacking modern quantitative rigor or reproducibility",
    "POPULATION_GAP": "Lack of evidence in specific clinical, demographic, or disease sub-populations",
    "MODEL_GAP": "Preclinical findings restricted to simplified 2D monocultures or non-human lineages",
    "INTERVENTION_GAP": "Optimal agent configuration, analogue superiority, or delivery mode uncharacterized",
    "DOSE_GAP": "Lack of concentration-response mapping within physiological / non-toxic boundaries",
    "TIMING_GAP": "Uncharacterized therapeutic window, kinetic duration, or chronopharmacology",
    "OUTCOME_GAP": "Primary endpoints restricted to surrogate markers without functional / phenotype validation",
    "TRANSLATIONAL_GAP": "In vitro efficacy uncorroborated in intact physiological or in vivo systems",
    "SAFETY_GAP": "Incomplete toxicological boundaries, therapeutic window, or organ-sparing assessment",
    "CONTRADICTION_GAP": "Unresolved discrepancies across published studies under divergent experimental contexts",
    "COMBINATION_GAP": "Lack of empirical studies evaluating direct simultaneous co-administration or multi-agent synergy",
    "REPLICATION_GAP": "Absence of independent confirmatory replications in separate laboratory environments"
}


# ==============================================================================
# 6. STUDY DESIGN COMPATIBILITY & RISK OF BIAS TOOLS
# ==============================================================================

STUDY_DESIGN_ROB_TOOL_MAP: Dict[str, str] = {
    "RANDOMIZED_CONTROLLED_TRIAL": "COCHRANE_ROB2",
    "CONTROLLED_CLINICAL_STUDY": "ROBINS_I",
    "OBSERVATIONAL_COHORT_CASE_CONTROL": "NEWCASTLE_OTTAWA_SCALE",
    "IN_VIVO_ANIMAL": "SYRCLE_ANIMAL_ROB",
    "IN_VITRO_EXPERIMENTAL": "IN_VITRO_REPLICATION_CRITERIA",
    "DIAGNOSTIC_ACCURACY_STUDY": "QUADAS_2",
    "SYSTEMATIC_REVIEW_META_ANALYSIS": "AMSTAR_2",
    "METHODOLOGICAL_LANDMARK": "METHOD_VALIDATION_STANDARDS"
}

# ==============================================================================
# 7. EVIDENCE TYPE HIERARCHY & WEIGHTING
# ==============================================================================

EVIDENCE_TYPE_HIERARCHY: Dict[str, Dict[str, Any]] = {
    "META_ANALYSIS": {"tier": 1, "is_primary": False, "weight": 1.0, "synthesis_rule": "Summarizes primary evidence; must not be counted alongside primary studies."},
    "SYSTEMATIC_REVIEW": {"tier": 1, "is_primary": False, "weight": 0.95, "synthesis_rule": "Secondary synthesis; unbundle to primary trials to avoid double counting."},
    "RANDOMIZED_CONTROLLED_TRIAL": {"tier": 2, "is_primary": True, "weight": 0.9, "synthesis_rule": "Primary clinical evidence gold standard."},
    "CONTROLLED_CLINICAL_STUDY": {"tier": 3, "is_primary": True, "weight": 0.75, "synthesis_rule": "Primary clinical evidence non-randomized."},
    "PROSPECTIVE_COHORT": {"tier": 4, "is_primary": True, "weight": 0.7, "synthesis_rule": "Primary observational longitudinal evidence."},
    "RETROSPECTIVE_CASE_CONTROL": {"tier": 5, "is_primary": True, "weight": 0.6, "synthesis_rule": "Primary observational retrospective evidence."},
    "IN_VIVO_ANIMAL": {"tier": 6, "is_primary": True, "weight": 0.5, "synthesis_rule": "Primary preclinical in vivo animal model."},
    "EX_VIVO_TISSUE": {"tier": 7, "is_primary": True, "weight": 0.45, "synthesis_rule": "Primary ex vivo human/animal tissue culture."},
    "IN_VITRO_EXPERIMENTAL": {"tier": 8, "is_primary": True, "weight": 0.4, "synthesis_rule": "Primary preclinical in vitro cell culture."},
    "CASE_REPORT_SERIES": {"tier": 9, "is_primary": True, "weight": 0.3, "synthesis_rule": "Descriptive clinical case report/series."},
    "NARRATIVE_REVIEW": {"tier": 10, "is_primary": False, "weight": 0.2, "synthesis_rule": "Non-systematic commentary; background context only, cannot substantiate causal claims."},
    "EXPERT_OPINION_EDITORIAL": {"tier": 11, "is_primary": False, "weight": 0.1, "synthesis_rule": "Author opinion; excluded from quantitative certainty weighting."}
}

