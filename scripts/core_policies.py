#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core_policies.py - Single Source of Truth Policy & Configuration Registry
Proposal-Nevisi Engine v8.2 (Universal Biomedical Architecture)

Centralizes all non-negotiable institutional structures, temporal constraints,
evidence scales, search boundaries, and study-design taxonomy.
Guarantees zero divergence across validator, docx builder, proposal generator,
auditors, and test suites.
"""

import os
import json
from typing import Dict, List, Tuple, Any

def get_project_metadata() -> Dict[str, Any]:
    """Dynamically loads single-source-of-truth project metadata."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(current_dir, "..", "project_metadata.json"),
        os.path.join(current_dir, "project_metadata.json"),
        os.path.abspath("project_metadata.json")
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    version_path = os.path.join(os.path.dirname(p), "VERSION")
                    if os.path.exists(version_path):
                        with open(version_path, "r", encoding="utf-8") as vf:
                            v_str = vf.read().strip()
                            if v_str and data.get("engine_version") != v_str:
                                data["engine_version"] = v_str
                                data["version_display"] = f"v{v_str}"
                    return data
            except Exception:
                pass
    v_val = "8.2.0"
    for vp in [os.path.join(current_dir, "..", "VERSION"), os.path.abspath("VERSION")]:
        if os.path.exists(vp):
            try:
                with open(vp, "r", encoding="utf-8") as vf:
                    v_val = vf.read().strip() or v_val
            except Exception:
                pass
    return {"project_name": "proposal-nevisi", "version_display": f"v{v_val}", "engine_version": v_val, "metrics": {}}

PROJECT_METADATA = get_project_metadata()
ENGINE_VERSION = "8.3.0"
VERSION_DISPLAY = "v8.3.0"

# Scientific Evidence Relationship Taxonomy (v8.3 Section 2)
EVIDENCE_RELATIONSHIPS = [
    "DIRECT",               # Direct match for target intervention + model + outcome
    "CLOSE_ANALOG",         # High relevance but differs in one key component (e.g. derivative, different cancer cell line)
    "MECHANISTIC_SUPPORT",  # Molecular pathway, intracellular cascade, target signaling without direct main intervention co-testing
    "METHOD_SUPPORT",       # Canonical mathematical/assay methodology (e.g. median-effect, cytotoxicity protocol)
    "BACKGROUND",           # Epidemiological background, disease definition, clinical problem statement
    "INDIRECT"              # Distant or indirect conceptual support
]

# Compound Identity Taxonomy (v8.3 Section 3)
COMPOUND_IDENTITY_TYPES = [
    "PARENT_COMPOUND",      # Exact parent molecule tested
    "COMPOUND_DERIVATIVE",  # Synthesized chemical derivative, conjugate, or salt
    "COMPOUND_ANALOG",      # Structural analog or related triterpenoid
    "CONTAINING_EXTRACT",   # Whole crude plant extract containing the target agent
    "NOT_APPLICABLE",       # Non-compound (viral platform or methodological landmark)
    "UNKNOWN_IDENTITY"      # Ambiguous compound formulation
]

# Evidence Polarity Taxonomy (Mandatory Epistemic Guardrail)
EVIDENCE_POLARITY_TYPES = [
    "SUPPORTS",                 # Finding directly confirms the directional claim
    "NEUTRAL",                  # Finding is descriptive/characterizing without directional efficacy
    "CONTRADICTS",              # Finding directly refutes the claim
    "LIMITS_INTERPRETATION"     # Finding demonstrates boundary constraint (e.g. non-cytotoxic, buffered resistance)
]

# Viral Platform Identity Taxonomy (v8.3 Section 4)
VIRAL_PLATFORM_TYPES = [
    "WT_VIRUS",             # Wild-type / naturally occurring viral isolate
    "VIRUS_STRAIN_SPECIFIED",# Specifically characterized biological viral strain
    "RECOMBINANT_VIRUS",    # Genetically modified / recombinant virus
    "ENGINEERED_VIRUS",     # Engineered oncolytic construct
    "CHIMERIC_HYBRID_VIRUS",# Hybrid / pseudotyped platform (e.g. rVSV-hybrid)
    "VIRUS_DERIVED_PLATFORM",# Derivative viral nanoparticle, virosome, or vector
    "NOT_APPLICABLE"        # Non-viral study
]

# Biological Model Match Taxonomy (v8.3 Section 5)
MODEL_MATCH_STATUSES = [
    "EXACT",                # Target cell line / primary system exactly matching problem model
    "CLOSE",                # Related cell line within identical disease / histology class
    "DIFFERENT",            # Different tissue, disparate cancer type, or in vivo animal divergence
    "UNKNOWN"               # Unspecified or unverified model system
]

# Outcome Match Taxonomy (v8.3 Section 6)
OUTCOME_MATCH_TYPES = [
    "CELL_VIABILITY",
    "GROWTH_INHIBITION",
    "APOPTOSIS",
    "CASPASE_ACTIVITY",
    "CELL_CYCLE",
    "ONCOLYSIS",
    "SYNERGY",
    "SELECTIVITY",
    "IC50",
    "CI",
    "ANTI_METASTATIC_MIGRATION",
    "METABOLIC_ALTERATION",
    "VIRAL_REPLICATION",
    "OTHER"
]

# Epistemically Bounded Search Gap Statuses (Blanket claims strictly prohibited)
BOUNDED_SEARCH_GAP_STATUSES = [
    "NO_DIRECT_STUDY_IDENTIFIED_IN_SEARCHED_SOURCES",
    "NO_DIRECT_STUDY_IDENTIFIED_UP_TO_SEARCH_DATE"
]

# Strict Synergy Fallacy Invariants:
# 1. MONOTHERAPY_A + MONOTHERAPY_B != SYNERGY
# 2. SYNERGY = HYPOTHESIS (Untested wet-lab hypothesis unless empirical quantitative co-treatment CI data exists)

# Synergy Evidence Taxonomy (v8.3 Section 7)
SYNERGY_EVIDENCE_STATUSES = [
    "DIRECT",               # Both interventions co-tested with quantitative CI / isobologram / formal synergy design
    "ANALOGOUS",            # Secondary agent tested with a different drug partner or in an analogous model
    "MONOTHERAPY_ONLY",     # Separate monotherapies only; synergy cannot be extrapolated
    "NOT_FOUND",            # No empirical combination studies identified
    "NOT_APPLICABLE"        # Single-agent, mechanistic, or methodological benchmark study
]

# CI Classification Provenance (v8.3 Section 12)
CI_CLASSIFICATION_SOURCES = [
    "CHOU_2006_LANDMARK",   # Theoretical basis, experimental design, and computerized simulation (Pharmacol Rev 2006)
    "CHOU_TALALAY_1984",    # Quantitative analysis of dose-effect relationships (Adv Enzyme Regul 1984)
    "EMPIRICAL_STUDY",      # Study-specific cutoff reported by authors
    "UNVERIFIED"            # Threshold unsupported by verified methodology citation
]

FINAL_INCLUSION_REASON_CATEGORIES = [
    "DIRECT_DISEASE_MODEL_EVIDENCE",    # Direct experimental evidence on target disease/cell/animal model
    "INTERVENTION_EFFICACY_EVIDENCE",   # Efficacy/synergy/combination data for primary or secondary intervention
    "MECHANISTIC_RATIONALE",            # Molecular pathways, signaling cascades, targets, apoptosis, gene expression
    "METHODOLOGICAL_BENCHMARK",         # Standard bioassay, mathematical model, CI formula, analytical benchmark
    "SAFETY_SELECTIVITY_BOUNDARY"       # Toxicity boundaries, therapeutic window, selectivity index, null evidence
]

PROPOSAL_SECTIONS_FOR_EVIDENCE = [
    "SECTION_1_TITLE",
    "SECTION_2_PROBLEM_STATEMENT",
    "SECTION_3_LITERATURE_REVIEW",
    "SECTION_4_NECESSITY",
    "SECTION_5_DEFINITIONS",
    "SECTION_6_SPECIFIC_OBJECTIVES",
    "SECTION_7_GENERAL_OBJECTIVES",
    "SECTION_8_APPLIED_OBJECTIVES",
    "SECTION_9_HYPOTHESES_QUESTIONS",
    "SECTION_10_DELIVERABLES",
    "SECTION_11_VARIABLE_TABLE",
    "SECTION_12_TIMELINE",
    "SECTION_13_METHODOLOGY"
]

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
    14: {"min_references": 15, "max_references": 25, "zero_padding_rule": True}
}

MAX_FINAL_REFERENCES: int = 25
MIN_FINAL_REFERENCES: int = 15

# ==============================================================================
# 8. CONTEXTUAL RELEVANCE & BIOLOGICAL COMPATIBILITY POLICIES
# ==============================================================================

class ContextualRelevanceConfig:
    """Configures contextual relevance assessment, biological transferability, and irrelevant context exclusion."""
    MIN_OVERALL_RELEVANCE_THRESHOLD: float = 0.50
    
    # 10 Universal Contextual Relevance Dimensions (Phase 4 Relevance Gate)
    RELEVANCE_DIMENSIONS = [
        "biological_topic_alignment",
        "condition_phenotype_alignment",
        "primary_agent_alignment",
        "comparator_second_agent_alignment",
        "experimental_model_population_alignment",
        "outcome_alignment",
        "mechanistic_pathway_alignment",
        "study_design_alignment",
        "research_question_fit",
        "proposal_section_utility"
    ]
    
    # Legacy alias dimensions for backwards compatibility
    LEGACY_DIMENSIONS = [
        "direct_relevance",
        "model_relevance",
        "intervention_relevance",
        "outcome_relevance",
        "mechanistic_relevance",
        "methodological_relevance",
        "transferability",
        "overall_relevance"
    ]
    
    # 6 Standard Relevance Tiers
    RELEVANCE_TIERS = [
        "DIRECTLY_RELEVANT",      # Direct alignment across agent, condition, model, outcomes (>= 0.80)
        "HIGHLY_RELEVANT",        # High alignment on core components with transferable model/pathway (0.65 - 0.79)
        "INDIRECTLY_RELEVANT",    # Biological analogue, upstream cascade, or parallel model (0.50 - 0.64)
        "METHOD_RELEVANT",        # Analytical assay, mathematical formula, or standard protocol (>= 0.70 method score)
        "BACKGROUND_ONLY",        # Epidemiological background, disease definition (0.35 - 0.49, Section 2/4 only)
        "IRRELEVANT"              # Off-topic, disconnected context, incompatible species/system (< 0.35)
    ]
    
    # Standard Rejection Categories
    REJECTION_REASONS = {
        "REJECT_LOW_CONTEXTUAL_RELEVANCE": "Insufficient alignment with target clinical/biological context; keyword match without contextual transferability",
        "REJECT_IRRELEVANT_OFF_TOPIC": "Study classified as IRRELEVANT due to disparate biological domain or incompatible context",
        "REJECT_INCOMPATIBLE_BIOLOGICAL_SYSTEM": "Study evaluated incompatible non-target biological system without transferable methodology",
        "REJECT_UNTRANSFERABLE_SPECIES": "Disparate non-target organism without translational or mechanistic bearing on target disease",
        "REJECT_DISCONNECTED_ENDPOINT": "Endpoints evaluated share zero biological, pathological, or pharmacological overlap with target research question",
        "REJECT_RETRACTED_OR_CONFLICT": "Article is retracted or exhibits severe identity/integrity conflict",
        "REJECT_TEMPORAL_BREACH": "Article exceeds 6-year recency threshold without approved foundational methodology exception"
    }



# ==============================================================================
# 2. TEMPORAL EVIDENCE POLICY CONFIGURATION
# ==============================================================================

class TemporalPolicyConfig:
    import datetime
    CURRENT_OPERATING_DATE: datetime.date = datetime.date.today()
    CURRENT_OPERATING_YEAR: int = CURRENT_OPERATING_DATE.year
    MAX_PRIMARY_EVIDENCE_AGE_YEARS: int = 6
    PRIMARY_EVIDENCE_CUTOFF_YEAR: int = CURRENT_OPERATING_YEAR - 6

    # 6 Standard Temporal Classes (Part 3)
    TEMPORAL_CLASSES = [
        "CORE_RECENT_PRIMARY",
        "CORE_RECENT_SECONDARY",
        "HISTORICAL_BACKGROUND",
        "FOUNDATIONAL_METHODOLOGY",
        "LANDMARK_GUIDELINE",
        "CLASSICAL_METHOD",
        "OUT_OF_WINDOW_NON_FOUNDATIONAL"
    ]

    APPROVED_FOUNDATIONAL_CATEGORIES: Dict[str, str] = {
        "FOUNDATIONAL_MATHEMATICAL_MODEL": "Seminal mathematical/pharmacological framework, index, or synergy equation",
        "ORIGINAL_DIAGNOSTIC_CRITERIA": "Landmark international diagnostic criteria (e.g. WHO staging criteria, Gold Standard)",
        "SEMINAL_DISCOVERY": "First isolation/discovery of virus, gene, receptor, or biological pathway",
        "STANDARDIZED_ASSAY_METHOD": "Seminal assay methodology protocol still universally referenced across literature",
        "LANDMARK_HISTORICAL_BENCHMARK": "Seminal clinical trial or benchmark epidemiological cohort study",
        "ORIGINAL_CHEMICAL_SYNTHESIS": "Original extraction, NMR elucidation, or chemical synthesis of agent",
        "METHODOLOGICAL_LANDMARK": "Methodological landmark or standard analytical assay protocol",
        "HISTORICAL_FOUNDATION": "Historical background or established scientific framework",
        "CLASSICAL_STATISTICAL_METHOD": "Classical statistical or epidemiological method introducing standard metrics"
    }

    OUTDATED_DIRECT_EVIDENCE: str = "OUTDATED_DIRECT_EVIDENCE"  # Old study reporting routine direct finding without landmark status

    @classmethod
    def get_cutoff_year(cls, current_year: int = None) -> int:
        cy = current_year or cls.CURRENT_OPERATING_YEAR
        return cy - cls.MAX_PRIMARY_EVIDENCE_AGE_YEARS

    @classmethod
    def get_cutoff_date(cls, current_date=None):
        import datetime
        cd = current_date or cls.CURRENT_OPERATING_DATE
        try:
            return cd.replace(year=cd.year - cls.MAX_PRIMARY_EVIDENCE_AGE_YEARS)
        except ValueError:
            # Handle Feb 29 leap year
            return cd.replace(month=2, day=28, year=cd.year - cls.MAX_PRIMARY_EVIDENCE_AGE_YEARS)

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
    "DIRECT_EVIDENCE_GAP": "Absence of direct empirical studies testing the specific intervention on target condition",
    "MECHANISTIC_GAP": "Incomplete signaling pathway elucidation or unverified intermediate cascades",
    "METHODOLOGICAL_GAP": "Reliance on legacy assays lacking modern quantitative rigor or reproducibility",
    "POPULATION_GAP": "Lack of evidence in specific clinical, demographic, or disease sub-populations",
    "MODEL_GAP": "Preclinical findings restricted to simplified 2D monocultures or non-human lineages",
    "INTERVENTION_GAP": "Optimal agent configuration, analogue superiority, or delivery mode uncharacterized",
    "DOSE_GAP": "Lack of concentration-response mapping within physiological / non-toxic boundaries",
    "TIMING_GAP": "Uncharacterized therapeutic window, kinetic duration, or chronopharmacology",
    "LONGITUDINAL_GAP": "Lack of longitudinal follow-up, durable response evaluation, or late recurrence data",
    "OUTCOME_GAP": "Primary endpoints restricted to surrogate markers without functional / phenotype validation",
    "TRANSLATIONAL_GAP": "In vitro efficacy uncorroborated in intact physiological or in vivo systems",
    "SAFETY_GAP": "Incomplete toxicological boundaries, therapeutic window, or organ-sparing assessment",
    "CONTRADICTION_GAP": "Unresolved discrepancies across published studies under divergent experimental contexts",
    "COMBINATION_GAP": "Lack of empirical studies evaluating direct simultaneous co-administration or multi-agent synergy",
    "REPLICATION_GAP": "Absence of independent confirmatory replications in separate laboratory environments",
    "IMPLEMENTATION_GAP": "Lack of evidence regarding real-world feasibility, barrier analysis, or adoption"
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
# 7. QUESTION-CONDITIONAL EVIDENCE HIERARCHY & WEIGHTING
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

def get_question_conditional_hierarchy(question_type: str, study_design: str) -> Dict[str, Any]:
    """Dynamically weights evidence relevance and quality conditional on the scientific question type (Prompt Pt 14).
    Therapeutic Efficacy: RCT > Prospective Cohort > Retrospective > Animal > In Vitro
    Molecular Mechanism: In Vitro / In Vivo Mechanistic > Ex Vivo > Clinical Association
    Diagnostic Accuracy: Diagnostic Accuracy (QUADAS-2) > Prospective Screening > Case-Control
    Prognostic Factor: Prospective Cohort > Registry Analysis > Cross-sectional
    """
    q_type = (question_type or "THERAPEUTIC_EFFICACY").upper()
    s_design = (study_design or "IN_VITRO_EXPERIMENTAL").upper()

    base_record = EVIDENCE_TYPE_HIERARCHY.get(s_design, {"tier": 5, "weight": 0.5, "is_primary": True})
    conditional_weight = base_record["weight"]
    relevance_note = "Standard hierarchy weighting applied."

    if "MECHANISTIC" in q_type or "MOLECULAR" in q_type or "BASIC_SCIENCE" in q_type:
        if "IN_VITRO" in s_design or "MECHANISTIC" in s_design or "EX_VIVO" in s_design:
            conditional_weight = min(1.0, base_record["weight"] + 0.45)
            relevance_note = "Mechanistic question prioritizes direct biochemical and cellular perturbation assays."
        elif "RCT" in s_design or "CLINICAL" in s_design:
            conditional_weight = 0.60
            relevance_note = "Clinical trial provides indirect evidence for intracellular molecular cascades."
    elif "DIAGNOSTIC" in q_type:
        if "DIAGNOSTIC" in s_design or "QUADAS" in s_design:
            conditional_weight = 0.95
            relevance_note = "Diagnostic accuracy study with gold-standard comparison is the primary evidence."
        elif "IN_VITRO" in s_design:
            conditional_weight = 0.30
            relevance_note = "Analytical bench assay provides analytical validity only, not clinical diagnostic accuracy."
    elif "PROGNOSTIC" in q_type:
        if "PROSPECTIVE_COHORT" in s_design:
            conditional_weight = 0.95
            relevance_note = "Prospective longitudinal cohort is the gold standard for prognostic risk stratification."
        elif "IN_VITRO" in s_design:
            conditional_weight = 0.20
            relevance_note = "In vitro models cannot estimate patient time-to-event survival hazard ratios."

    return {
        "question_type": q_type,
        "study_design": s_design,
        "base_weight": base_record["weight"],
        "conditional_weight": round(conditional_weight, 3),
        "relevance_note": relevance_note,
        "is_primary_evidence": base_record.get("is_primary", True)
    }

