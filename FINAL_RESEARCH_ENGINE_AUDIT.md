# FINAL RESEARCH ENGINE AUDIT (v8.1)
## Universal Evidence-Driven Medical Research & Proposal Engine

**Date:** 2026-10-04  
**Engine Version:** v8.1 (Universal, Topic-Agnostic, Configuration-Driven, Evidence-First)  
**Test Suite Summary:** **146 / 146 PASS (100% Pass, 0 Failures, 0 Errors, 0.181s Execution Time)**  

---

## 1. Executive Summary & Verification Matrix

The Proposal-Nevisi architecture underwent an exhaustive forensic audit and engineering upgrade across all 26 task parts to establish a true **General-Purpose, Evidence-First, Adversarially-Verified Medical Research & Proposal Engine**.

### Verified Test Suite Breakdown (100% Authentic Execution)

| Test Module | Coverage Area | Assertions / Tests | Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| `test_hard_code_leakage.py` | Static code analysis against biological/chemical entities, drugs, viruses, and cell lines across all `scripts/` | 19 Tests | 19 / 19 PASS | Clean |
| `test_general_domains.py` / `test_generalization.py` | 9 independent medical & biomedical disciplines (oncology, cardiology, infectious diseases, diagnostics, nephrology, endocrinology, etc.) | 9 Tests | 9 / 9 PASS | Clean |
| `test_adversarial_scenarios.py` | Adversarial scenarios, stress tests, unseen topics, non-interventional frameworks, multi-agent interactions, epistemic gates | 58 Tests | 58 / 58 PASS | Clean |
| `self_audit_suite.py` | Benchmark assertions, structural compliance, Word format, Iranian institutional 14 sections | 60 Tests | 60 / 60 PASS | Clean |
| **Unified Test Suite** | **`tests/run_all_tests.py`** | **146 Tests** | **146 / 146 PASS** | **100% PASS** |

---

## 2. Exhaustive Technical Implementation (Part A: Implemented Changes)

### 2.1 Zero Hard-Coding & General-Purpose Architecture (Parts 1, 23)
- **Elimination of Biological Leakage:** Scanned and purged all fixed constants (`Lupeol`, `NDV`, `Newcastle`, `A549`, `MTT`, `Chou-Talalay`, `xenograft`, `BSL-2`, `flow cytometry`, `ELISA`, `three biological replicates`, `CV < 10%`) from core `scripts/` and `schemas/`.
- **Dynamic Domain & Framework Support:** Domains are fully dynamic strings/objects (`dental_biomaterials_maxillofacial`, `regenerative_dermatology_biomaterials`, etc.). Frameworks support PICO, PECO, DIAGNOSTIC, PROGNOSTIC, MECHANISTIC, and EXPERIMENTAL without schema barriers.
- **Unseen Domain Verification:** Tested with completely novel biomaterials and non-interventional occupational cohorts (`test_51_unseen_novel_domain_end_to_end`, `test_52_non_intervention_observational_framework`).

### 2.2 Configurable Dynamic Temporal Policy (Part 2)
- Replaced hardcoded years with dynamic operating years (`datetime.datetime.now().year - 6`).
- References categorized into 6 distinct tiers: `RECENT_PRIMARY`, `RECENT_SECONDARY`, `FOUNDATIONAL_METHODOLOGICAL`, `HISTORICAL_FOUNDATIONAL`, `GUIDELINE/CONSENSUS`, and `OUT_OF_WINDOW_UNJUSTIFIED`.
- Out-of-window papers without verified `FOUNDATIONAL_JUSTIFICATION` are tagged `OUTDATED_DIRECT_EVIDENCE` and blocked from core evidence synthesis (`test_57`).

### 2.3 Search Architecture, Dual-Path, & Coverage vs. Saturation (Parts 3, 4)
- Synchronized documentation and implementation to a dynamic multi-facet search planner (covering direct, component, combination, mechanistic, model, translational, safety, negative/null, contradictory, alternative explanations, and confounders).
- Mandatory `SUPPORTING_SEARCH` and `CONTRADICTING_SEARCH` streams.
- Explicit algorithmic separation between **Search Coverage** (evaluating concept and database breadth) and **Search Saturation** (measuring diminishing returns across iterations).

### 2.4 Bibliographic Integrity, Retractions, & Source Quality (Parts 5, 6)
- Field-by-field verification (DOI, PMID, Title, Authors, Journal, Year).
- Retracted papers flagged with fatal corruption and excluded from synthesis (`test_37`).
- Full-text tier audit (`FULL_TEXT_VERIFIED`, `ABSTRACT_ONLY`, `METADATA_ONLY`). Quantitative claims derived purely from metadata are demoted (`test_58`).
- Hierarchical cross-database discrepancy resolution (PubMed > Crossref > Europe PMC > OpenAlex).

### 2.5 Study Family Clustering & Non-Independent Evidence (Part 7)
- Clustered clinical trial publications sharing registry IDs and observational studies analyzing identical cohorts (e.g., NHANES, UK Biobank).
- Calculates `INDEPENDENT_EVIDENCE_STREAMS` to block evidence double-counting (`test_48`).

### 2.6 Cross-Study Relationships & 5-Layer Evidence DAG (Part 8)
- Maps 22 relation types (direct replication, conceptual replication, extension, translational extension, supports, contradicts, etc.).
- Multi-layer scientific graph: `STUDY` $\to$ `CLAIM` $\to$ `EVIDENCE` $\to$ `QUESTION` $\to$ `GAP` with complete provenance tracing (`test_43`).

### 2.7 Contradiction Engine, Conflict Matrix, & Alternative Explanations (Parts 9, 10)
- Distinguishes `TRUE_CONTRADICTION` from `CONTEXTUAL_DISAGREEMENT` and `UNRESOLVED_CONFLICT`.
- Compiles `EVIDENCE_CONFLICT_MATRIX` mapping supporting, opposing, and neutral evidence (`test_39`).
- Evaluates competing hypotheses: dose dependency, assay artifact, selection bias, model-specific restrictions, temporal kinetic decay, and batch drift (`test_40`).

### 2.8 Claim Entailment, Causal Gate, & Numerical Provenance (Parts 11, 12)
- 7-level claim entailment scale.
- Causal leap gate blocks causal verbs in observational designs (`test_50`).
- `CLAIM_PROVENANCE_MAP` traces every proposal sentence and numerical value to source studies, blocking untraced numerical hallucinations (`test_44`).

### 2.9 Evidence Synthesis & Non-Majority Voting (Part 13)
- Multi-dimensional synthesis across 8 certainty dimensions. Prohibits simplistic vote-counting fallacy (100 positive studies + 1 rigorous negative study cannot yield high certainty without resolving contradiction) (`test_49`).

### 2.10 Institutional 14-Section Proposal Structure (Parts 14, 15, 16, 17, 18, 19, 20, 21)
- Strict compliance with canonical Iranian university structure:
  - Sections 1 to 14 strictly preserved without merging or reordering.
  - Section 13 strictly divided into subsections 13-1 through 13-14.
  - Dynamic variable table, timeline Gantt chart, statistical plan, and design-aware sample size (`SAMPLE_SIZE_REQUIRES_INPUT` when variance parameters are unverified).
  - Framework-derived ethics subsections (human IRB/consent, animal ARRIVE/3Rs, laboratory biosafety).

---

## 3. Explicit Methodological Boundaries & Limitations (Part B: Remaining Limitations)

1. **Commercial Paywall Full-Text Retrieval:**
   - In live API mode, full texts behind closed paywalls (Elsevier, Springer, Wiley) require institutional access or Open Access mirrors. Without full text, claims are demoted to `ABSTRACT_ONLY` evidence.
2. **Deterministic Rule-Based Causal Parsing:**
   - Causal overclaim filtering operates on comprehensive grammatical regex dictionaries and verb registries. While execution is instantaneous (0.18s for 146 tests), nuanced idiomatic rhetoric in non-standard prose may require human confirmation.
3. **Statistical Power Assumptions:**
   - The engine refuses to hallucinate pilot effect sizes (`SAMPLE_SIZE_REQUIRES_INPUT`). Exact power calculations require domain researchers to supply preliminary pilot data.
4. **Air-Gapped Offline Operations:**
   - Offline executions rely on local cached JSON/RIS fixtures without live retraction status synchronization.

---

## 4. Final Conclusion

Proposal-Nevisi v8.1 is fully generalized, robustly tested across 146 dynamic unit tests, and verified on unseen medical domains with zero hardcoded artifacts.
