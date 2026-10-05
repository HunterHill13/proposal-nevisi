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
ENGINE_VERSION = "8.7.0"
VERSION_DISPLAY = "v8.7.0"

# Generalized Evidence Roles (v8.4 Section 9 - Distinct from Polarity)
EVIDENCE_ROLES = [
    "DIRECT_EVIDENCE",              # Directly evaluates target intervention on target condition/model measuring primary outcome
    "INDIRECT_EVIDENCE",            # Evaluates related intervention or closely transferable model
    "MECHANISTIC_EVIDENCE",         # Evaluates molecular/cellular pathway, target engagement, signaling cascade
    "METHODOLOGICAL_EVIDENCE",      # Evaluates assay technique, mathematical formula, experimental benchmark
    "CONTEXTUAL_EVIDENCE",          # Epidemiological burden, clinical guidelines, standard of care
    "NEGATIVE_EVIDENCE",            # Demonstrates lack of efficacy, non-superiority, or biological inertness
    "SAFETY_EVIDENCE",              # Evaluates toxicology, adverse events, selectivity, therapeutic window
    "FEASIBILITY_EVIDENCE",         # Evaluates technical feasibility, formulation stability, deliverability
    "EPIDEMIOLOGICAL_EVIDENCE",     # Population incidence, prevalence, clinical risk factors
    "DIAGNOSTIC_EVIDENCE"           # Evaluates diagnostic accuracy, sensitivity, specificity, AUC
]

# Universal Entity Hierarchy (v8.4 Section 8 - Generic Across All Biomedical Interventions)
UNIVERSAL_ENTITY_TYPES = [
    "PARENT_ENTITY",        # Exact specified primary/secondary intervention entity (molecule, biologic, viral strain, technique, device, biomarker)
    "DERIVATIVE",           # Synthesized chemical derivative, conjugate, modified peptide, or salt
    "ANALOGUE",             # Structural analogue, class member, or related biological counterpart
    "FORMULATION",          # Nanoparticle, liposome, emulsion, vehicle formulation, or sustained release
    "EXTRACT",              # Whole crude botanical extract or natural fraction containing agent
    "COMBINATION",          # Direct combination of two or more distinct interventions
    "RECOMBINANT_VARIANT",  # Genetically modified / recombinant construct or vector
    "ENGINEERED_VERSION",   # Engineered cell, oncolytic construct, or advanced medical device
    "BIOSIMILAR",           # Biosimilar, bioequivalent, or generic formulation
    "DEVICE_VARIANT",       # Medical device model, modified surgical instrument, or biomaterial
    "DIAGNOSTIC_VARIANT",   # Modified assay probe, alternative diagnostic platform, or surrogate test
    "NOT_APPLICABLE",       # Methodological landmark, epidemiological baseline, or unperturbed control
    "UNKNOWN_IDENTITY"      # Ambiguous, unspecified, or unverified entity formulation
]

# Scientific Evidence Relationship Taxonomy (Backwards Compatible v8.3 Mapping)
EVIDENCE_RELATIONSHIPS = [
    "DIRECT",               # Direct match for target intervention + model + outcome
    "CLOSE_ANALOG",         # High relevance but differs in one key component (e.g. derivative, different cell line)
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


# ==============================================================================
# 9. ADVANCED RESEARCH & SCREENING ENGINE POLICIES (v8.3 ENHANCED)
# Cross-Audited & Adapted from AIPOCH and K-Dense Architectures
# ==============================================================================

NO_QUOTA_FILLING: bool = True  # Strictly prohibits padding references to reach max quota

# 16 Standard Generic Exclusion Codes (v8.4 Section 7 - Topic-Agnostic Two-Stage PRISMA Taxonomy)
GENERIC_EXCLUSION_ONTOLOGY: Dict[str, str] = {
    "OUT_OF_SCOPE": "Completely unrelated to the core biomedical problem model or clinical domain",
    "WRONG_POPULATION": "Non-target organism, clinical population, demographic group, or tissue source",
    "WRONG_CONDITION": "Investigates a non-target pathology or physiological state without translational relevance",
    "WRONG_INTERVENTION": "Evaluates an unrelated drug, agent class, surgical technique, or therapeutic modality",
    "WRONG_COMPARATOR": "Comparator group or control is absent, inappropriate, or non-informative",
    "WRONG_MODEL": "Utilizes an incompatible or non-transferable experimental model system",
    "WRONG_OUTCOME": "Endpoints evaluated share zero biological, clinical, or pharmacological overlap with research question",
    "WRONG_STUDY_DESIGN": "Study design cannot address the research question (e.g. case report for incidence)",
    "WRONG_SETTING": "Setting (e.g. agronomic, non-clinical environment) is disconnected from target scope",
    "INSUFFICIENT_EVIDENCE": "Methodologically deficient, lacking controls, or presenting purely speculative assertions",
    "NOT_PRIMARY_RESEARCH": "Non-systematic commentary, news, book review, or opinion piece",
    "RETRACTED": "Article officially retracted, withdrawn, or flagged with unresolved expression of concern",
    "DUPLICATE": "Identical record or multi-database duplicate cross-matched across identifiers",
    "OUTDATED": "Article exceeds temporal recency boundary without approved foundational landmark exception",
    "METHOD_ONLY": "Methodological assay description without biological/clinical evaluation and not flagged as landmark exception",
    "PERIPHERAL_EVIDENCE": "Distant analog, unrelated natural product, or non-transferable secondary finding"
}

# Unified Exclusion Taxonomy: Generic Ontology with Backwards-Compatible Legacy Mappings
EXCLUSION_TAXONOMY: Dict[str, str] = {
    **GENERIC_EXCLUSION_ONTOLOGY,
    "OUT_OF_TOPIC": "Completely unrelated to the core biomedical problem model or clinical domain (alias for OUT_OF_SCOPE)",
    "WRONG_DISEASE": "Investigates a non-target pathology with zero translational or mechanistic relevance (alias for WRONG_CONDITION)",
    "WRONG_COMPOUND": "Chemical entity is distinct from target compound or its legitimate derivatives (alias for WRONG_INTERVENTION)",
    "WRONG_FORMULATION": "Formulation or vehicle artifact produces uninterpretable phenotypic outcomes (alias for WRONG_INTERVENTION)",
    "ANIMAL_ONLY": "Preclinical animal study without translational bearing on target cellular or human context (alias for WRONG_MODEL)",
    "AGRICULTURAL_ONLY": "Agronomic, veterinary herd production, crop protection, or soil science study (alias for WRONG_SETTING)",
    "FOOD_NUTRITION_ONLY": "General food chemistry, culinary additive, or dietary supplement study without disease focus (alias for WRONG_CONDITION)",
    "SPERM_FERTILITY_ONLY": "Veterinary livestock semen cryopreservation or artificial insemination study (alias for WRONG_POPULATION)",
    "PERIPHERAL_ANALOGUE": "Distant analog or unrelated natural product added without direct mechanistic rationale (alias for PERIPHERAL_EVIDENCE)"
}

# Standardized Database Execution Statuses (v8.4 Section 6 - Zero False Execution Claims)
SEARCH_DATABASE_STATUSES: List[str] = [
    "EXECUTED",             # API successfully queried and authentic records retrieved
    "UNAVAILABLE",          # API / database endpoint unavailable or network offline
    "PARTIALLY_QUERIED",    # Multi-source federated search executed across subset of configured engines
    "NOT_APPLICABLE",       # Database not applicable to target scientific question
    "NOT_SEARCHED",         # Search planned but deferred or not contacted
    "EMPTY_RETRIEVAL",      # API queried successfully but returned zero matching records
    "ERROR",                # Network failure, timeout, HTTP error, or unparseable response
    "NOT_EXECUTED"          # API was not contacted (dry-run, offline mode, or missing credentials)
]

# Standardized 7-Phase Research Pipeline
RESEARCH_PIPELINE_STAGES: List[str] = [
    "PHASE_A_DECOMPOSITION",            # Generic research question decomposition into search components
    "PHASE_B_MULTI_LAYER_SEARCH",       # 9-Layer adaptive multi-source query execution
    "PHASE_C_TWO_STAGE_SCREENING",      # Title/Abstract (Stage 1) and Full-Text/Evidence (Stage 2)
    "PHASE_D_EVIDENCE_EVALUATION",      # Identity, directness, and polarity categorization
    "PHASE_E_CONTRADICTION_RESOLUTION", # Root-cause analysis across divergent findings
    "PHASE_F_CLAIM_MAPPING",            # Atomic claim entailment and provenance tracing
    "PHASE_G_PORTFOLIO_SELECTION"       # High-value scoring and selection (capped at <= 25, no padding)
]

# 14 Generic Contradiction Root-Cause Categories (v8.4 Section 10 Adaptive Diagnostic Taxonomy)
GENERIC_CONTRADICTION_ROOT_CAUSES: List[str] = [
    "POPULATION",           # Demographic, species, or clinical sub-population differences
    "MODEL",                # In vitro 2D vs 3D vs in vivo organism, genetic divergence, or cellular lineage
    "INTERVENTION",         # Specific variant, construct, strain, or synthetic purity disparity
    "FORMULATION",          # Pure API vs complex vehicle, excipient, or delivery nanocarrier
    "DOSE_EXPOSURE",        # Physiological vs supra-physiological exposure concentration
    "DURATION",             # Acute vs chronic incubation kinetics / treatment window
    "TIMING",               # Pre-treatment vs co-treatment vs post-treatment schedule
    "COMPARATOR",           # Mismatched negative control, vehicle control, or active benchmark
    "ASSAY",                # Different analytical principle (e.g. tetrazolium dye vs flow cytometry)
    "ENDPOINT",             # Anti-migratory / cytostatic vs direct cytocidal cell viability
    "STUDY_DESIGN",         # Prospective vs retrospective, unblinded vs blinded architecture
    "BIOLOGICAL_CONTEXT",   # Basal pathway competency, receptor expression, or resistance mutations
    "STATISTICAL_POWER",    # Small sample size, underpowered cohort, or high measurement variance
    "MEASUREMENT_METHOD"    # Operator variability, instrument sensitivity, or calibration protocol
]

# Legacy aliases preserved for backwards compatibility with earlier test suites
CONTRADICTION_ROOT_CAUSES: List[str] = list(dict.fromkeys(
    GENERIC_CONTRADICTION_ROOT_CAUSES + [
        "CELL_LINE", "DOSE", "EXPOSURE_TIME", "COMPOUND_PURITY",
        "VIRAL_STRAIN", "MOI", "ASSAY_TYPE"
    ]
))

# High-Value Paper Screener Scoring Weights (AIPOCH-adapted)
HIGH_VALUE_SCORING_WEIGHTS: Dict[str, float] = {
    "topical_relevance": 0.20,
    "model_relevance": 0.15,
    "intervention_identity_match": 0.15,
    "outcome_relevance": 0.10,
    "study_design_quality": 0.10,
    "methodological_quality": 0.05,
    "recency": 0.10,
    "directness": 0.05,
    "quantitative_usefulness": 0.05,
    "contradiction_value": 0.05
}

# Strict 9-Step Selection Priority Ordering (No Quota-Filling Rule)
SELECTION_ORDER_PRIORITIES: List[str] = [
    "DIRECT_RELEVANCE",             # 1. Target intervention on exact target model/condition
    "SCIENTIFIC_QUALITY",           # 2. Peer-reviewed rigor, proper controls, sample size
    "EVIDENCE_STRENGTH",            # 3. High quantitative effect size, statistical significance
    "MODEL_RELEVANCE",              # 4. Exact or closely transferable cellular/organism system
    "OUTCOME_RELEVANCE",            # 5. Direct viability, cytotoxicity, or synergistic index
    "RECENCY",                      # 6. Published within last 6 years (unless landmark exception)
    "COMPLEMENTARITY",              # 7. Covers orthogonal biological axes (mechanistic, safety, model)
    "CONTRADICTION_LIMITATION_VALUE",# 8. Essential bounding/limiting evidence (e.g. non-cytotoxic baselines)
    "METHODOLOGICAL_NECESSITY"      # 9. Essential validated mathematical or assay benchmark (Chou, Mosmann)
]

# ==============================================================================
# 10. v8.5 ADVANCED RESEARCH ENGINE ONTOLOGIES & REGISTRIES
# Adapted from AIPOCH and K-Dense Proven Architectures
# ==============================================================================

# 16 Standard Generic Search Families (v8.5 Section 5 - Topic-Agnostic Query Families)
SEARCH_FAMILIES_ONTOLOGY: Dict[str, str] = {
    "EXACT_CONCEPT_COMBINATION": "Boolean intersection of clean target concepts without modification",
    "SYNONYM_EXPANDED_COMBINATION": "Cross-sectional retrieval incorporating verified biomedical synonyms",
    "CONTROLLED_VOCABULARY_MESH": "MeSH descriptor and subject heading tree hierarchical retrieval",
    "POPULATION_MODEL_SPECIFIC": "Targeted retrieval focusing on organism, tissue, or specific cellular lineage",
    "INTERVENTION_SPECIFIC": "Focused retrieval on primary intervention pharmacodynamics or chemistry",
    "OUTCOME_SPECIFIC": "Retrieval constrained to primary and secondary phenotypic/clinical outcomes",
    "MECHANISM_SPECIFIC": "Retrieval on molecular signaling, target binding, and biochemical pathways",
    "STUDY_DESIGN_SPECIFIC": "Filtered retrieval by methodology (RCT, cohort, in vitro replication)",
    "METHODOLOGY_ASSAY_SPECIFIC": "Measurement standards, bioassay protocols, and validation benchmarks",
    "NEGATIVE_NULL_RESULT": "Deliberate search for lack of effect, antagonism, inertness, or failure to replicate",
    "HISTORICAL_FOUNDATIONAL": "Seminal origin papers and foundational mathematical/biochemical models",
    "RECENT_EMERGING_LITERATURE": "Literature within immediate window (<3 years) capturing latest consensus",
    "TERMINOLOGY_VARIANT": "Alternate naming conventions, historical disease designations, and synonyms",
    "ACRONYM_ABBREVIATION": "Disambiguated acronym and abbreviated term permutations",
    "ALTERNATIVE_SPELLING_HYPHENATION": "Spelling variants, British/American English, and hyphenation variants",
    "CITATION_DERIVED_DISCOVERY": "Literature recovered via backward, forward, or lateral citation chasing"
}

# 7 Independent Saturation Novelty Dimensions (v8.5 Section 8 - Multi-Dimensional Saturation)
SATURATION_DIMENSIONS: Dict[str, str] = {
    "RECORD_NOVELTY": "Marginal discovery rate of genuinely new, unique bibliographic records",
    "ENTITY_NOVELTY": "Discovery of previously unobserved biological entities, compounds, or cell models",
    "EVIDENCE_NOVELTY": "Discovery of novel effect directions, quantitative effect sizes, or endpoints",
    "CONTRADICTION_NOVELTY": "Discovery of newly identified conflicting findings or divergent parameters",
    "CITATION_NETWORK_NOVELTY": "Discovery of relevant studies via backward, forward, or lateral citation links",
    "DATABASE_NOVELTY": "Yield of unique eligible records contributing from distinct database engines",
    "VOCABULARY_NOVELTY": "Discovery of previously unmapped terminology, synonyms, or MeSH descriptors"
}

# 8 High-Value Seed Paper Categories (v8.5 Section 9 - Discovery Anchors)
SEED_PAPER_CATEGORIES: Dict[str, str] = {
    "SYSTEMATIC_REVIEW_META_ANALYSIS": "Synthesizes evidence landscape and provides comprehensive reference network",
    "CLINICAL_PRACTICE_GUIDELINE": "Authoritative clinical consensus defining standard-of-care benchmark",
    "HISTORICAL_LANDMARK": "Foundational mathematical model or biological discovery origin",
    "HIGHLY_CITED_FOUNDATIONAL": "Seminal paper establishing field parameters and initial proof-of-concept",
    "RECENT_HIGH_IMPACT": "Recent publication establishing state-of-the-art methodology or efficacy",
    "KEY_METHODOLOGICAL": "Canonical bioassay or analytical protocol benchmark",
    "CONTRADICTORY_NULL_RESULT": "Definitive paper establishing boundary conditions or negative efficacy",
    "EXPLORATORY_ANCHOR": "Initial high-scoring study selected as seed for citation chasing"
}

# Citation Chasing Directions (v8.5 Section 7)
CITATION_CHASE_DIRECTIONS: List[str] = [
    "BACKWARD",     # Inspecting references cited by seed paper
    "FORWARD",      # Inspecting papers citing the seed paper
    "LATERAL"       # Inspecting related studies by same author group or sharing key entities
]

# 6 Citation Drift & Misattribution Types (v8.5 Section 11 - AIPOCH Adapted)
CITATION_DRIFT_TYPES: Dict[str, str] = {
    "NO_DRIFT": "Claim accurately and conservatively reflects explicit primary evidence of cited study",
    "OVERSTATEMENT": "Claim exaggerates effect size, certainty, or generality beyond observed data",
    "CITATION_DRIFT": "Secondary retellings gradually altered or broadened the original author conclusion",
    "CONTEXT_MISMATCH": "Claim transfers finding to different population, model, tissue, or endpoint",
    "SELECTIVE_CITATION": "Claim cites positive sub-analysis while omitting primary null or adverse outcome",
    "CORRELATION_TO_CAUSATION": "Claim asserts causal direction from purely observational or cross-sectional design"
}

# 4 Structured Paper Reading Tracks (v8.5 Section 10 - AIPOCH Literature Reader Pro Adapted)
STRUCTURED_PAPER_READING_TRACKS: List[str] = [
    "CLINICAL_EPIDEMIOLOGY",        # Human trials, observational cohorts, diagnostic/prognostic models
    "COMPUTATIONAL_BIOINFORMATICS", # Omics analysis, screening pipelines, predictive algorithms
    "BASIC_EXPERIMENTAL",           # In vitro cell cultures, in vivo animal models, molecular assays
    "HYBRID"                        # Multi-track studies integrating computational and laboratory validation
]

# 3 Contradiction Explanation Partitions (v8.5 Section 12 - AIPOCH Contradiction Resolver Adapted)
CONTRADICTION_EXPLANATION_LEVELS: List[str] = [
    "DEMONSTRATED_EXPLANATION",     # Discrepancy empirically verified by direct parameter variation (e.g. dose/time)
    "PLAUSIBLE_EXPLANATION",        # Discrepancy mechanistically substantiated by differences in model/assay
    "UNRESOLVED_UNCERTAINTY"        # Discrepancy unexplained under available evidence; true research gap
]

# ==============================================================================
# v8.6 ADVANCED RESEARCH RECALL, DEEP READING & POST-AUDIT REGISTRIES
# ==============================================================================

# Search Miss Diagnostic Taxonomy (v8.6 Section 4)
SEARCH_MISS_TAXONOMY: Dict[str, str] = {
    "VOCABULARY_FAILURE": "Search query lacked specific clinical/technical terminology used in target study",
    "SYNONYM_FAILURE": "Target study used alternative synonym or lexical variant not included in query expansion",
    "MESH_MAPPING_FAILURE": "Controlled vocabulary indexing differed or MeSH term was not mapped/assigned",
    "DATABASE_COVERAGE_FAILURE": "Target journal or publication not indexed in searched database endpoints",
    "QUERY_FAMILY_FAILURE": "Applicable query family (e.g. comparator or negative result) was not executed",
    "DATE_FILTER_FAILURE": "Publication date falls outside configured temporal search window",
    "STUDY_DESIGN_FILTER_FAILURE": "Methodology filter excluded study design (e.g. in vitro vs in vivo)",
    "ENTITY_RESOLUTION_FAILURE": "Intervention, target gene, or compound identifier failed to resolve or align",
    "CITATION_NETWORK_FAILURE": "Target study was disconnected from seeds' citation paths or exceeded chase depth",
    "DEDUPLICATION_ERROR": "Study was falsely flagged as duplicate of another record and discarded",
    "SCREENING_FALSE_NEGATIVE": "Title/abstract screening filter erroneously rejected eligible paper",
    "METADATA_RETRIEVAL_FAILURE": "Bibliographic metadata or abstract was incomplete or unindexed",
    "FULL_TEXT_RETRIEVAL_FAILURE": "Full-text payload unavailable behind paywall or inaccessible format"
}

# Empirical Research Recall Benchmark Statuses (v8.6 Section 3)
RECALL_BENCHMARK_STATUSES: List[str] = [
    "EMPIRICALLY_VALIDATED_RECALL",       # Evaluated against explicit ground-truth gold standard (recall >= 0.85)
    "PARTIALLY_VALIDATED_RECALL",         # Evaluated against partial gold standard (0.0 < recall < 0.85)
    "UNVALIDATED_RECALL",                 # Evaluated against gold standard but zero targets retrieved
    "RECALL_NOT_EMPIRICALLY_ESTABLISHED"  # No empirical gold standard provided for topic
]

# Deep Paper Reading Generic Sections (v8.6 Section 5 - AIPOCH Close-Reading Adapted)
DEEP_READING_SECTIONS: Dict[str, List[str]] = {
    "STUDY_IDENTITY": [
        "study_design", "population_or_model", "intervention_or_exposure",
        "comparator", "setting", "sample_size"
    ],
    "METHODS": [
        "experimental_clinical_methodology", "primary_assay",
        "intervention_dose_exposure", "duration", "controls",
        "randomization_blinding", "inclusion_exclusion_criteria"
    ],
    "RESULTS": [
        "primary_endpoint", "effect_direction", "quantitative_effect_size",
        "uncertainty_ci", "p_value", "adverse_events",
        "negative_null_findings", "subgroup_findings"
    ],
    "INTERPRETATION": [
        "authors_conclusion", "limitations", "alternative_explanations",
        "translational_limitations", "internal_validity_concerns"
    ],
    "EVIDENCE_PROVENANCE": [
        "source_paper", "source_section", "table_figure_location",
        "extraction_confidence", "evidence_directness_status"
    ]
}

# Figure-First Visual Review Discrepancy Flag (v8.6 Section 6)
PRIMARY_DATA_VISUAL_REQUIRES_REVIEW = "PRIMARY_DATA_VISUAL_REQUIRES_REVIEW"

# Evidence Hierarchy Strength Levels (v8.6 Section 8)
EVIDENCE_HIERARCHY_TIERS: List[str] = [
    "DIRECT_HIGH_CONFIDENCE",       # Direct target intervention/model, rigorous design, low RoB, strong effect
    "DIRECT_MODERATE_CONFIDENCE",   # Direct target intervention/model, moderate sample or minor methodological limits
    "DIRECT_LOW_CONFIDENCE",        # Direct target intervention/model, high RoB or unconfirmed replication
    "INDIRECT_SUPPORT",             # Related intervention or analog model providing transferable precedent
    "MECHANISTIC_SUPPORT",          # Upstream/downstream biochemical pathway, receptor, or molecular cascade
    "CONTEXTUAL_SUPPORT",           # Epidemiological baseline, clinical standard of care, or assay benchmark
    "CONTRADICTORY",                # Directly refutes hypothesis or reports conflicting empirical direction
    "LIMITS_INTERPRETATION"         # Boundary condition, toxic concentration artifact, or confounding factor
]

# Claim Verification 2.0 Issue Categories (v8.6 Section 9 - K-Dense & AIPOCH Adapted)
CLAIM_VERIFICATION_ISSUES_V2: Dict[str, str] = {
    "UNSUPPORTED_CLAIM": "No primary empirical evidence found in cited source supporting claim",
    "PARTIALLY_SUPPORTED_CLAIM": "Evidence supports only a component or sub-phenotype of stated claim",
    "OVERGENERALIZATION": "Claim expands specific laboratory finding to broad universal generalization",
    "POPULATION_MISMATCH": "Claim targets clinical population while source examined different cohort",
    "MODEL_MISMATCH": "Claim asserts cellular/organismal model distinct from experimental system tested",
    "ENDPOINT_MISMATCH": "Claim asserts clinical/functional endpoint different from measured assay outcome",
    "INTERVENTION_MISMATCH": "Claim references pure compound/agent while source tested conjugate/mixture/extract",
    "DOSE_MISMATCH": "Claim quotes efficacy at standard dose while source observed effect only at supra-physiological/toxic levels",
    "TEMPORAL_MISMATCH": "Acute short-term exposure cited as proof of durable chronic response",
    "CORRELATION_TO_CAUSATION": "Observational correlation or association framed as definitive causal mechanism",
    "PRECLINICAL_TO_CLINICAL_LEAP": "In vitro or murine cell line finding asserted as established human clinical efficacy",
    "SECONDARY_TO_PRIMARY_CONFUSION": "Review article commentary cited as if it were original empirical experimentation",
    "SELECTIVE_CITATION": "Favorable secondary metric quoted while omitting neutral or adverse primary endpoint"
}

# Post-Research Citation Audit Statuses (v8.6 Section 10 - K-Dense Adapted)
POST_CITATION_AUDIT_STATUSES: Dict[str, str] = {
    "VERIFIED_PRIMARY_SOURCE": "Reference verified as primary empirical study matching topic scope",
    "VERIFIED_SECONDARY_REVIEW": "Reference verified as systematic review, guideline, or method origin",
    "UNVERIFIED_SOURCE": "Bibliographic metadata or identifier could not be definitively resolved",
    "UNUSED_REFERENCE_IN_PORTFOLIO": "Reference exists in bibliography pool but is nowhere cited in text",
    "UNRESOLVED_CITATION_PLACEHOLDER": "Unresolved citation marker detected in proposal narrative (e.g. [?])",
    "MISSING_CITATION_IN_TEXT": "Specific empirical claim asserted without mandatory literature attribution"
}

# Adaptive Database Specialization Registry (v8.6 Section 14)
DATABASE_SPECIALIZATION_REGISTRY: Dict[str, Dict[str, Any]] = {
    "pubmed": {
        "domain": "BIOMEDICAL_CORE",
        "why_used": "Canonical index of peer-reviewed biomedical, clinical, and life sciences literature with controlled MeSH indexing.",
        "can_capture": ["Peer-reviewed clinical trials", "Mechanistic biology", "MeSH-indexed systematic reviews", "Biomedical toxicology"],
        "cannot_capture": ["Non-biomedical engineering", "Unindexed preprint archives", "Grey literature reports", "Direct clinical trial registry records"]
    },
    "europe_pmc": {
        "domain": "BIOMEDICAL_OPEN_ACCESS",
        "why_used": "Comprehensive repository providing full-text XML access, European grant links, and life sciences preprints.",
        "can_capture": ["Full-text open access content", "Life sciences preprints", "Direct figure/table data extraction", "European clinical registries"],
        "cannot_capture": ["Strictly closed-access proprietary journals", "Non-biomedical physical sciences"]
    },
    "openalex": {
        "domain": "INTERDISCIPLINARY_SCHOLARLY",
        "why_used": "Global multidisciplinary graph capturing cross-disciplinary works, citation networks, and institutional linkages.",
        "can_capture": ["Cross-disciplinary technologies", "Comprehensive citation network relationships", "Author and institution disambiguation", "Global conference proceedings"],
        "cannot_capture": ["Deep full-text XML markup", "Detailed clinical assay parameters"]
    },
    "crossref": {
        "domain": "METADATA_REGISTRY",
        "why_used": "Authoritative DOI registration agency capturing exact publication metadata, errata, and funder acknowledgments.",
        "can_capture": ["Canonical DOI resolution", "Publisher errata and retractions", "Funder attribution metadata", "Official publication dates"],
        "cannot_capture": ["Detailed experimental assay protocols", "Bioinformatic sequence annotations"]
    }
}

# Negative Evidence & Publication Bias Indicators (v8.6 Section 13)
PUBLICATION_BIAS_INDICATORS: Dict[str, str] = {
    "POSITIVE_EVIDENCE_DOMINANCE": "Excess of positive findings (>85%) with absence of null/negative studies indicates potential publication bias",
    "SYMMETRIC_EVIDENCE_DISTRIBUTION": "Balanced distribution of positive, neutral, and adverse findings indicates robust reporting",
    "NEGATIVE_EVIDENCE_RECOVERED": "Deliberate negative query families successfully identified inertness or boundary conditions"
}

# ==============================================================================
# 29. CANONICAL PAPER EVIDENCE RECORD FIELDS (v8.7 - Provenance & Traceability)
# ==============================================================================

CANONICAL_EVIDENCE_RECORD_FIELDS: List[str] = [
    "bibliographic_identity",
    "study_design",
    "population_or_model",
    "intervention_or_exposure",
    "comparator",
    "outcomes",
    "measurements",
    "quantitative_results",
    "qualitative_results",
    "negative_or_null_results",
    "limitations",
    "funding_or_coi",
    "evidence_directness",
    "evidence_quality",
    "source_locations",
    "provenance"
]

# Standardized Extraction Source Locations (v8.7 Section 6 - SciFact & RefVerifier Adapted)
EXTRACTION_SOURCE_LOCATIONS: Dict[str, str] = {
    "ABSTRACT": "Reported in Abstract text",
    "INTRODUCTION": "Reported in Introduction background / hypothesis",
    "METHODS": "Reported in Methods / Experimental Design section",
    "RESULTS": "Reported in primary Results narrative",
    "DISCUSSION": "Reported in Discussion / Authors' Interpretation",
    "TABLE": "Extracted directly from structured Data Table",
    "FIGURE": "Extracted directly from Data Chart / Image / Graph",
    "SUPPLEMENTARY": "Extracted from Supplementary Online Materials / Appendix",
    "NOT_AVAILABLE": "Source location cannot be definitively resolved from available text"
}

# Numeric Provenance Statuses (v8.7 Section 7 - W3C PROV-O Adapted)
NUMERIC_PROVENANCE_STATUSES: Dict[str, str] = {
    "DIRECTLY_REPORTED": "Value is verbatim extracted from primary text, table, or figure in the cited source",
    "CALCULATED_FROM_REPORTED_DATA": "Value is deterministically computed via transparent, verified transformation from reported raw data",
    "DERIVED": "Value is derived through validated secondary modeling explicitly documented in source",
    "INFERRED": "Value was inferred by synthesis model (strictly prohibited in primary quantitative claims)",
    "NOT_REPORTED": "Source paper does not report this numeric parameter; must never be hallucinated or filled with generic defaults"
}

# Contextual Boundary Mismatches (v8.7 Section 8 - Dynamic Topic-Agnostic Taxonomies)
CONTEXTUAL_BOUNDARY_MISMATCHES: Dict[str, str] = {
    "MODEL_MISMATCH": "Claim asserts a model/tissue distinct from the biological system evaluated in source",
    "POPULATION_MISMATCH": "Claim targets a clinical/demographic population distinct from the studied cohort",
    "SPECIES_MISMATCH": "Claim transfers non-human animal findings directly to human physiology without translational qualification",
    "CELL_MODEL_MISMATCH": "Claim attributes finding to specific cell lineage absent from source experimental design",
    "INTERVENTION_MISMATCH": "Claim asserts target intervention while source examined an alternative agent",
    "FORMULATION_MISMATCH": "Claim attributes mixture/extract/formulation effect to pure single constituent without isolation proof",
    "OUTCOME_MISMATCH": "Claim asserts clinical/functional endpoint different from measured assay parameter",
    "STUDY_DESIGN_MISMATCH": "Claim presents computational/in silico analysis as empirical wet-lab experimentation",
    "TIMEPOINT_MISMATCH": "Claim extrapolates acute short-term response to long-term chronic durability",
    "DOSE_EXPOSURE_MISMATCH": "Claim asserts physiological efficacy when effect occurred strictly at supra-physiological/toxic levels",
    "IN_SILICO_TO_EXPERIMENTAL_LEAP": "Computational binding/docking/prediction asserted as physical in vitro or in vivo efficacy"
}

# Formulation & Entity Granularity Distinctions (v8.7 Section 9 - Generic Pure vs Mixture Policy)
FORMULATION_ENTITY_DISTINCTIONS: Dict[str, str] = {
    "PURE_CONSTITUENT": "Isolated, purified single active chemical or biological molecule (>95% purity)",
    "EXTRACT": "Crude or semi-purified natural product/botanical extract containing heterogeneous phytochemicals",
    "MIXTURE": "Defined or undefined combination of multiple independent chemical or biological entities",
    "FORMULATION": "Active agent incorporated into nano-carriers, liposomes, excipients, or delivery vehicles",
    "COMBINATION": "Concomitant multi-agent intervention administered simultaneously or sequentially",
    "DERIVATIVE": "Chemically modified synthetic or semi-synthetic analog of parent scaffold",
    "METABOLITE": "In vivo biological breakdown product or biotransformed intermediate",
    "ANALOGUE": "Structural congener or bioisostere possessing distinct pharmacokinetic properties",
    "NOT_APPLICABLE": "Methodological, diagnostic, or computational landmark not involving physical agents"
}

# SciFact-Aligned Claim-Evidence Verdicts (v8.7 Section 5)
CLAIM_EVIDENCE_VERDICTS: Dict[str, str] = {
    "SUPPORTED": "Primary source evidence fully entails the claim with matching model, dose, and causality bounds",
    "PARTIALLY_SUPPORTED": "Evidence supports claim direction or sub-phenotype but contains translational, dose, or model disparities",
    "NOT_SUPPORTED": "Cited source contains zero empirical evidence or text supporting the asserted claim",
    "CONTRADICTED": "Primary source evidence directly refutes or reports contrary outcome to asserted claim",
    "INSUFFICIENT_EVIDENCE": "Source evidence is equivocal, underpowered, or missing critical parameters to establish claim"
}

# Evidence Status Per Paper (v8.7 Section 15)
EVIDENCE_STATUS_PER_PAPER: Dict[str, str] = {
    "DIRECT_EVIDENCE": "Direct evaluation of target problem model intervention and outcome under matching conditions",
    "INDIRECT_SUPPORT": "Transferable precedent from related entity or closely analogous model system",
    "BACKGROUND_ONLY": "General epidemiology, disease pathology, standard of care, or clinical guidelines",
    "CONTEXTUAL_EVIDENCE": "Methodological landmark, assay validation, or baseline comparison data",
    "CONTRADICTORY_EVIDENCE": "Empirical evidence demonstrating antagonism, toxicity, null response, or boundary limit",
    "INSUFFICIENT_EVIDENCE": "Inconclusive, unverified, or critically underreported experimental record",
    "REJECTED": "Excluded on scope, severe bias, retraction, or irreconcilable biological incompatibility"
}

# Linguistic Certainty Calibration Levels (v8.7 Section 12)
CLAIM_CERTAINTY_LEVELS: Dict[str, Dict[str, Any]] = {
    "DEMONSTRATES": {"tier": 1, "allowed_designs": ["RANDOMIZED_CONTROLLED_TRIAL", "IN_VIVO_ANIMAL", "IN_VITRO_EXPERIMENTAL"], "requires_repetition": True},
    "SUPPORTS": {"tier": 2, "allowed_designs": ["IN_VIVO_ANIMAL", "IN_VITRO_EXPERIMENTAL", "CONTROLLED_CLINICAL_STUDY"], "requires_repetition": False},
    "SUGGESTS": {"tier": 3, "allowed_designs": ["OBSERVATIONAL_COHORT_CASE_CONTROL", "IN_VITRO_EXPERIMENTAL", "COMPUTATIONAL_IN_SILICO"], "requires_repetition": False},
    "ASSOCIATED_WITH": {"tier": 4, "allowed_designs": ["OBSERVATIONAL_COHORT_CASE_CONTROL", "CROSS_SECTIONAL", "ECOLOGICAL_STUDY"], "strictly_non_causal": True},
    "OBSERVED": {"tier": 5, "allowed_designs": ["CASE_SERIES", "PRELIMINARY_SCREENING"], "strictly_descriptive": True},
    "MAY_INDICATE": {"tier": 6, "allowed_designs": ["COMPUTATIONAL_IN_SILICO", "IN_VITRO_EXPERIMENTAL"], "exploratory": True},
    "HYPOTHESIZED": {"tier": 7, "allowed_designs": ["NARRATIVE_REVIEW", "EDITORIAL", "THEORETICAL"], "non_empirical": True}
}

# Negative Search Claim Boundaries (v8.7 Section 17)
NEGATIVE_SEARCH_CLAIM_BOUNDS: Dict[str, str] = {
    "SCOPE_BOUNDED_NEGATIVE": "No eligible study was identified within the defined search perimeter ({databases}, {dates}, {languages})",
    "UNWARRANTED_ABSOLUTE_NEGATIVE": "Prohibited leap from search retrieval absence to global non-existence ('it does not exist')"
}




