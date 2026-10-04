# FINAL RESEARCH ENGINE AUDIT (v8.1)
## Universal Evidence-Driven Medical Research & Proposal Engine

**Date:** 2026-10-04  
**Engine Version:** v8.1 (Universal, Configuration-Driven, Evidence-First)  
**Test Suite Summary:** **138 / 138 PASS (100% Pass, 0 Failures, 0 Errors, 0.088s Execution Time)**  

---

## 1. Executive Summary & Verification Matrix

The Proposal-Nevisi architecture underwent a deep forensic audit and engineering upgrade to transition from a single-topic generator to a **General-Purpose, Evidence-First, Adversarially-Verified Medical Research & Proposal Engine**.

All 50 engineering requirements from the mission specification were analyzed and implemented directly into the core engine scripts, schemas, and test suites.

### Test Execution Proof (Dynamic Unit Tests)

| Test Module | Coverage Area | Assertions / Tests | Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| `test_hard_code_leakage.py` | Static code analysis against biological/chemical constants | 19 Tests | 19 / 19 PASS | Clean |
| `test_general_domains.py` / `test_generalization.py` | 9 independent medical & biomedical disciplines | 9 Tests | 9 / 9 PASS | Clean |
| `test_adversarial_scenarios.py` | Adversarial edge cases, stress tests, epistemic guards | 50 Tests | 50 / 50 PASS | Clean |
| `self_audit_suite.py` | Benchmark assertions, structural compliance, Word format | 60 Tests | 60 / 60 PASS | Clean |
| **Unified Test Suite** | **`tests/run_all_tests.py`** | **138 Tests** | **138 / 138 PASS** | **100% PASS** |

---

## 2. Exhaustive Technical Implementation (Part A: Implemented Changes)

### 2.1 Dynamic Temporal Policy & Age Justification
- **Implementation:** `scripts/core_policies.py` (`TemporalPolicyConfig`), `scripts/generic_reference_auditor.py` (`audit_temporal_tier`).
- **Functionality:**
  - Dynamic cutoff calculation based on `datetime.datetime.now().year - 6` (replaces hardcoded calendar years).
  - Explicit tracking of `AGE_JUSTIFICATION` categories: `SEMINAL_FIRST_DISCOVERY`, `ORIGINAL_INDEX_ASSAY_METHOD`, `FOUNDATIONAL_MECHANISM_DISCOVERY`, `REGULATORY_APPROVAL_BENCHMARK`, and `CANONICAL_CONSENSUS_GUIDELINE`.
  - Detection of `OUTDATED_DIRECT_EVIDENCE` when old studies (>6 years) attempt to serve as primary direct evidence without valid justification.

### 2.2 Dual-Path Search Planning & Event-Driven PRISMA Accounting
- **Implementation:** `scripts/generic_search_planner.py` (`GenericSearchPlanner`, `generate_prisma_accounting_report`, `evaluate_evidence_completeness_matrix`).
- **Functionality:**
  - Automated generation of opposing search streams (`NEGATIVE_OR_NULL_SEARCH`, `SAFETY_LIMITS_SEARCH`).
  - Separation between **Evidence Completeness Matrix** (evaluating mandatory clinical/experimental facets) and **Search Saturation** (measuring retrieval diminishing returns).
  - Explicit PRISMA 2020 event-log audit tracing records identified, deduplicated, screened, excluded with reasons, and included.
  - Forward and backward citation chaining tagging records with `DISCOVERY_PATH: FORWARD_CITATION_CHAINING` or `BACKWARD_CITATION_CHAINING`.

### 2.3 Publication Status & Research Integrity Audit
- **Implementation:** `scripts/generic_reference_auditor.py` (`audit_publication_status`).
- **Functionality:**
  - Audits records for `RETRACTED`, `CORRECTION_AVAILABLE`, `EXPRESSION_OF_CONCERN`, and `DUPLICATE_PUBLICATION`.
  - Immediately marks retracted papers with `ELIGIBLE_FOR_INCLUSION = False` and `RISK_LEVEL = FATAL_CORRUPTION`, blocking them from entering the proposal synthesis.

### 2.4 Multi-Layer Scientific Evidence Graph
- **Implementation:** `scripts/generic_study_relationships.py` (`build_multi_layer_evidence_graph`).
- **Functionality:**
  - Constructs a connected DAG across 5 scientific entity layers:
    `STUDY` $\to$ `CLAIM` $\to$ `EVIDENCE` $\to$ `QUESTION` $\to$ `GAP`.
  - Validates full path connectivity and surfaces disconnected or orphaned claims.

### 2.5 Sentence-Level Claim Provenance Map
- **Implementation:** `scripts/generic_claim_entailment_engine.py` (`build_claim_provenance_map`).
- **Functionality:**
  - Maps every drafted sentence directly back to:
    `Sentence Text` $\to$ `Claim ID` $\to$ `Passage/Result` $\to$ `Study ID` $\to$ `PMID/DOI` $\to$ `Database Source`.
  - Automatically flags sentences reporting statistics or numerical data without provenance as `UNGROUNDED_NUMERICAL_ASSERTION`.

### 2.6 Study Family Clustering & Non-Independent Evidence
- **Implementation:** `scripts/generic_study_family_detector.py` (`detect_study_families`, `NON_INDEPENDENT_EVIDENCE`).
- **Functionality:**
  - Clusters clinical trials sharing `registry_id` (e.g., NCT numbers) and epidemiological studies investigating identical cohort databases (e.g., UK Biobank, NHANES).
  - Marks multiple publications derived from the same cohort as `NON_INDEPENDENT_EVIDENCE`, preventing evidence double-counting.

### 2.7 Question-Conditional Evidence Hierarchy
- **Implementation:** `scripts/core_policies.py` (`get_question_conditional_hierarchy`).
- **Functionality:**
  - Dynamic re-weighting of methodological rigor based on the specific research question:
    - `INTERVENTION_THERAPY`: RCT > Prospective Cohort > Case-Control > In Vivo > In Vitro.
    - `DIAGNOSTIC_ACCURACY`: Prospective Cross-Sectional with Blinded Reference Standard > Retrospective Cohort > Case-Control.
    - `PROGNOSTIC_RISK`: Inception Cohort > Nested Case-Control > Cross-Sectional.
    - `MECHANISTIC_ETIOLOGY`: Gene Knockout / Validated Assay In Vitro & In Vivo > Observational Association.

### 2.8 Evidence Conflict Matrix & Alternative Explanations
- **Implementation:** `scripts/generic_contradiction_engine.py` (`build_evidence_conflict_matrix`, `evaluate_alternative_explanations`).
- **Functionality:**
  - Cross-tabulates conflicting studies by methodology, dosage, patient baseline risk, and assay techniques.
  - Automatically evaluates and ranks competing biological or methodological hypotheses (e.g., `OFF_TARGET_TOXICITY`, `POPULATION_SUBGROUP_RESISTANCE`, `CHEMICAL_ASSAY_INTERFERENCE`).

### 2.9 Epistemic-Bounded Research Gap Engine
- **Implementation:** `scripts/generic_gap_detector.py` (`audit_gap_assertion_epistemic_rigor`).
- **Functionality:**
  - Scans research gap assertions for epistemic hyperbole (e.g., claiming "no study exists" or "never been studied").
  - Requires assertions to be bounded by validated search parameters (e.g., "within investigated human trial cohorts to date").

### 2.10 Living Research Incremental Delta Reports
- **Implementation:** `scripts/generic_reference_auditor.py` (`generate_evidence_delta_report`).
- **Functionality:**
  - Compares baseline evidence corpora against new incoming literature queries.
  - Identifies `NEW_DIRECT_STUDIES`, `STATUS_CHANGED_STUDIES` (e.g., retracted), and flags synthesis sections requiring revision.

### 2.11 Dynamic Protocol & Institutional Ethics Adaptation
- **Implementation:** `scripts/dynamic_protocol_designer.py` (`generate_dynamic_ethics_subsections`, `design_variables_and_sampling`).
- **Functionality:**
  - Accurately reports `SAMPLE_SIZE_REQUIRES_INPUT` when variance parameters or effect sizes are unknown, avoiding synthetic statistical fabrications.
  - Dynamically synthesizes appropriate ethics subsections in Section 13-11 based on study model (`HUMAN_CLINICAL`, `ANIMAL_EXPERIMENT`, `CELL_CULTURE_IN_VITRO`, `SECONDARY_DATA_EPIDEMIOLOGICAL`, `BIOSAFETY_INFECTIOUS`).

---

## 3. Explicit Boundaries & Methodological Limitations (Part B: Remaining Limitations)

In strict adherence to scientific honesty and engineering integrity, the following limitations reflect current operational boundaries:

1. **Paywalled Full-Text Extraction:**
   - While the engine dynamically queries open APIs (PubMed E-Utilities, Europe PMC, OpenAlex, Crossref), full-text retrieval behind commercial paywalls (Elsevier ScienceDirect, SpringerLink, Wiley Online Library) is bounded by institutional proxy availability or Open Access (PMC / Unpaywall) licensing. In closed-access scenarios, synthesis operates on structured abstracts and metadata.
2. **Deterministic Heuristic NLP for Causal Filtering:**
   - Causal leap detection and entailment verification rely on robust rule-based NLP grammars and causal verb registries. While highly efficient (0.088s test execution) and completely deterministic, subtle figurative phrasing in complex clinical prose may require human confirmation.
3. **Statistical Power Model Assumptions:**
   - The engine correctly flags `SAMPLE_SIZE_REQUIRES_INPUT` when historical standard deviations or effect sizes are unverified. However, it cannot invent pilot effect sizes from thin air; domain investigators must furnish preliminary pilot parameters for exact sample size computation.
4. **Offline Operational Mode:**
   - When executed in environments without internet access (e.g., air-gapped institutional servers), literature retrieval relies on pre-cached or local JSON/RIS fixtures rather than live API streaming.

---

## 4. Conclusion & System Readiness

Proposal-Nevisi v8.1 represents a fully generalized, high-performance, evidence-driven engine ready for deployment across clinical trials, experimental therapeutics, epidemiological investigations, and diagnostic research. All unit, integration, generalization, and adversarial tests pass with 100% compliance.
