# GENERALIZATION & ARCHITECTURAL AUDIT
## Proposal-Nevisi Engine: From Case-Specific Implementation to General-Purpose Medical Research Pipeline

**Audit Date:** October 2026  
**Audited Target:** `proposal-nevisi` skill codebase and evidence pipeline  
**Evaluation Standard:** Universal Medical Evidence Synthesis & General Biomedical Applicability  

---

## 1. Executive Summary

This audit evaluates the architectural separation between generic evidence-synthesis mechanisms and domain-specific instantiations in the `proposal-nevisi` skill. Historically, the engine was developed and tested against a complex biomedical problem: *Synergistic oncolytic and phytochemical interactions of Lupeol and Newcastle Disease Virus (NDV) in A549 lung adenocarcinoma*. 

While this test case provided an exemplary stress test for contradictory evidence, biochemical mechanism graphs, and multi-database retrieval, key components in early versions inadvertently hard-coded biological entities, cell lines, dosage units, and oncology-specific heuristics directly into core Python scripts.

This document formally categorizes all engine components, details the exact points of topic-specific leakage, outlines the generic abstractions introduced in v8.0, and sets the baseline for the multi-domain generalization framework.

---

## 2. Component Categorization Matrix

| Component / Script | Current Functionality | Generic vs. Overfitted Aspects | Remediation Strategy in v8.0 |
| :--- | :--- | :--- | :--- |
| **SKILL.md** | Workflow orchestrator & user manual | Mixed. High-level workflow is generic, but examples and step descriptions over-emphasized Lupeol/NDV. | Elevate to configuration-driven lifecycle; treat Lupeol/NDV as one of several validation fixtures. |
| **`deep_research_protocol.md`** | 15-stage literature search protocol | High generic rigor. Methodological principles are sound, but search templates were fixed to oncology. | Abstract into dynamic Query Matrix Generator supporting PICO, PECO, mechanistic, and diagnostic frameworks. |
| **`scripts/research_problem_model.py`** | *New in v8.0* | None (New). | Dynamically decomposes any research topic into structured facets, terminologies, and framework models. |
| **`scripts/generic_search_planner.py`** | *New in v8.0* | None (New). | Replaces static query lists with dynamic 8-category dual-path (`SUPPORTING_SEARCH` & `CONTRADICTING_SEARCH`) generation. |
| **`scripts/generic_comparability_engine.py`** | Multi-study comparability matrix | Overfitted in v7: 12 static dimensions strictly evaluated cell lines, passage, and solvent toxicity. | Implements study-design-aware comparability (in vitro, animal, clinical RCT, observational, diagnostic). |
| **`scripts/generic_contradiction_engine.py`** | Contradiction & negative evidence detection | Partially generic in v7: 6 categories (A–F) covered key angles, but taxonomy was limited to oncology drug assays. | Expands to extensible 15+ negative evidence categories; distinguishes true contradiction from contextual disagreement. |
| **`scripts/generic_claim_entailment_engine.py`** | Claim decomposition & evidence entailment | Overfitted in v7: Stored 15 atomic claims with hardcoded Lupeol/NDV assertions. | Dynamically parses claims from synthesized evidence; strictly enforces directness levels and overclaim detection. |
| **`scripts/generic_reference_auditor.py`** | Field-level citation & bibliographic audit | Overfitted in v7: Hardcoded `concept_checks` for `lupeol`, `newcastle`, and `a549`. | Derives validation boundaries and conceptual requirements dynamically from the active `ResearchProblemModel`. |
| **`scripts/generic_study_family_detector.py`** | *New in v8.0* | None (New). | Detects shared cohorts, overlapping trial registries, and secondary analyses to prevent evidence double-counting. |
| **`scripts/docx_builder.py`** | Word document generation (14 sections, RTL, Dubai font) | Fully Generic. Builds native OpenXML Persian proposals with zero domain assumptions. | Retain as production-grade output renderer; preserve exact 14-section academic structure. |
| **`scripts/self_audit_suite.py`** | Multi-tier self-verification suite | Mixed in v7: 60 tests included ~12 tests with hard-coded string assertions on Lupeol/NDV. | Refactor into modular architecture: core engine test suite (topic-agnostic) + multi-domain test fixtures. |

---

## 3. Forensic Identification of Domain Leakage

### 3.1 Hard-Coded Biological Entities
In v7.0 and earlier, the following biological and biochemical entities appeared in core operational logic:
1. **Compounds & Biological Agents:** `Lupeol`, `lup-20(29)-en-3β-ol`, `Newcastle Disease Virus`, `NDV`, `AF2240`, `LaSota`, `Mukteswar`.
2. **Cell Models & Tissues:** `A549`, `human non-small cell lung cancer`, `4T1`, `mammary carcinoma`, `MRC-5`, `normal lung fibroblasts`.
3. **Assays & Pharmacological Models:** `MTT cell viability`, `Chou-Talalay Combination Index (CI)`, `IC50`, `Isobologram`, `Flow cytometry annexin V/PI`.
4. **Molecular Pathways:** `Akt phosphorylation`, `Bcl-2 down-regulation`, `Bax up-regulation`, `Caspase-3/9 cleavage`, `IFN-beta release`.

*Impact of Leakage:* When applying the skill to a cardiology topic (e.g., SGLT2 inhibitors in heart failure) or an infectious disease topic (e.g., Paxlovid resistance in SARS-CoV-2), the core auditor erroneously flagged relevant papers as failing concept checks because they lacked terms like `lupeol` or `A549`.

### 3.2 Fixed In Vitro Comparability Assumption
The 12 comparability dimensions in `study_comparability_v2.py`:
- `cell_line_identity`
- `passage_number_range`
- `culture_medium_composition`
- `lupeol_solvent_vehicle`
- `vehicle_concentration_pct`
- `viral_multiplicity_of_infection`
- `viral_strain_pathotype`
- `treatment_schedule_sequence`
- `exposure_duration_hours`
- `endpoint_assay_methodology`
- `replicate_structure`
- `statistical_model_ci`

*Critique:* These 12 dimensions are valid **only** for in vitro virotherapy and phytotherapy cell experiments. They are nonsensical for:
- **Randomized Controlled Trials (RCTs):** Require allocation concealment, randomization method, blinding (participants/personnel/outcome assessors), intention-to-treat analysis, baseline comparability.
- **Animal Studies (In Vivo):** Require animal species, strain, sex, age, housing pathogen status, randomization, sample size justification, route of administration, blinding of outcome measurement.
- **Diagnostic Accuracy Studies:** Require index test, reference standard, spectrum of disease, blinding between index and reference, threshold pre-specification.

### 3.3 Fixed Fallacy Detection Heuristics
In `reference_validity_auditor.py`, fallacy checks were explicitly tailored to catch cross-cancer contamination:
```python
# Old overfitted pattern
if "4t1" in title_lower or "breast cancer" in title_lower:
    if "lung" not in title_lower and "a549" not in title_lower:
        issues.append("FALLACY_BREAST_CANCER_MODEL_ATTRIBUTED_TO_LUNG")
```
*Remediation:* Fallacy detection must be generalized into **Population/Model Mismatch Detection**, where the study's experimental model is compared against the target condition defined in the `ResearchProblemModel`.

---

## 4. Architectural Transformation in v8.0

```text
+-------------------------------------------------------------------------------+
|                             TOPIC AGNOSTIC CORE                               |
+-------------------------------------------------------------------------------+
|  1. Research Problem Modeler (PICO / PECO / Mechanistic / Diagnostic)         |
|  2. Dynamic Search Planner (A-H Facets, Supporting + Contradicting)          |
|  3. Multi-Database Retrieval & Normalization Engine                          |
|  4. Bibliographic Field-Level Verifier (Crossref / PubMed / OpenAlex)         |
|  5. Study Design Classifier & Design-Aware Risk-of-Bias Auditor               |
|  6. Study-Design-Aware Comparability Engine                                  |
|  7. Extensible Contradiction & Contextual Disagreement Engine                 |
|  8. Study Family & Duplicate Publication Detector                             |
|  9. Claim-Evidence Entailment & Causal Language Gate                          |
| 10. Multi-Dimensional Evidence Certainty Synthesizer                          |
| 11. 14-Section DOCX Proposal Renderer (Bidi RTL, Dubai Font)                  |
+-------------------------------------------------------------------------------+
                                      |
       +------------------------------+------------------------------+
       |                              |                              |
+--------------+              +---------------+              +---------------+
|   Fixture 1  |              |   Fixture 2   |              |   Fixture 3   |
| Oncology:    |              | Cardiology:   |              | Infectious:   |
| Lupeol + NDV |              | SGLT2 in HF   |              | Antivirals    |
+--------------+              +---------------+              +---------------+
```

---

## 5. Audit Conclusion

The architectural decoupling separates the general-purpose scientific engine from individual project fixtures. The historical Lupeol+NDV benchmark remains preserved as a regression fixture and demonstration case, but all production scripts operate strictly via dynamic configuration and design-aware schemas.
