# MULTI-DOMAIN GENERALIZATION TEST REPORT
## Universal Evidence Synthesis Across Oncology, Cardiology, Infectious Diseases, and Diagnostics

**Report Date:** October 2026  
**System Architecture:** Proposal-Nevisi Engine v8.0  
**Harness Module:** `tests/test_generalization.py`  

---

## 1. Objective & Scope

This report documents the empirical evaluation of the `proposal-nevisi` core engine across four fundamentally diverse biomedical research domains. The goal of this evaluation is to prove that the engine is genuinely universal and domain-agnostic, capable of dynamically generating problem models, query matrices, design-aware comparability matrices, and evidence certainty profiles without altering a single line of core Python code.

---

## 2. Domain Fixture Evaluations

### Fixture 1: Preclinical Oncology & Phytotherapy
- **Project ID:** `FIXTURE_ONCOLOGY_LUPEOL_NDV`
- **Domain:** Oncology / Basic Biomedical Science
- **Selected Framework:** `EXPERIMENTAL_IN_VITRO`
- **Target Condition:** Non-Small Cell Lung Carcinoma (A549 cell line)
- **Interventions:** Lupeol (phytochemical) + Newcastle Disease Virus (oncolytic paramyxovirus)
- **Primary Outcomes:** Cell viability inhibition (IC50) and Combination Index (synergy vs antagonism)
- **Pipeline Execution Results:**
  - *Query Matrix:* 9 Supporting Queries, 4 Contradicting Queries generated across 8 facets.
  - *Study Families:* Correctly identified 2 distinct laboratory study streams (`FAM_LUP_01` and `FAM_NDV_01`).
  - *Comparability Engine:* Evaluated across in vitro dimensions (model system, culture medium, solvent concentration, exposure duration, and endpoint assays).
  - *Synthesis Certainty:* Evaluated as `HIGH` with verdict `EVIDENCE_SUPPORTS_HYPOTHESIS_WITH_BOUNDARIES`.
  - *Status:* **PASS**

---

### Fixture 2: Clinical Cardiology & Pharmacotherapy
- **Project ID:** `FIXTURE_CARDIO_SGLT2`
- **Domain:** Cardiovascular Medicine
- **Selected Framework:** `PICO` (Patient, Intervention, Comparator, Outcome)
- **Target Condition:** Heart Failure with Preserved Ejection Fraction (HFpEF)
- **Intervention:** Empagliflozin (SGLT2 Inhibitor, 10 mg daily) vs. Placebo
- **Primary Outcomes:** Composite of cardiovascular death or hospitalization for heart failure (Hazard Ratio)
- **Pipeline Execution Results:**
  - *Query Matrix:* 6 Supporting Queries, 3 Contradicting Queries generated.
  - *Study Families:* Detected that `ST_EMPEROR_SUBGROUP_RENAL` is a secondary subgroup analysis of the primary `ST_EMPEROR_PRESERVED_2021` trial (both derived from `NCT03057977`). Clustered into `FAM_EMPEROR_PRESERVED`.
  - *Comparability Engine:* Activated `CLINICAL_TRIAL` dimension set (population inclusion, disease severity NYHA II-IV, randomization allocation, blinding, and follow-up duration).
  - *Double-Counting Prevention:* Clustered publications were weighted as a single composite trial unit.
  - *Synthesis Certainty:* Evaluated as `MODERATE` with verdict `PRELIMINARY_EVIDENCE_REQUIRES_INVESTIGATION`.
  - *Status:* **PASS**

---

### Fixture 3: Infectious Diseases & Antiviral Resistance
- **Project ID:** `FIXTURE_INFECTIOUS_ANTIVIRAL`
- **Domain:** Infectious Disease & Medical Virology
- **Selected Framework:** `PICO`
- **Target Condition:** Acute SARS-CoV-2 Infection
- **Intervention:** Nirmatrelvir/Ritonavir (Paxlovid) vs. Supportive Care / Placebo
- **Primary Outcomes:** Viral rebound frequency and emergence of 3CL protease resistance mutations (E166V, L50F)
- **Pipeline Execution Results:**
  - *Query Matrix:* 6 Supporting Queries, 3 Contradicting Queries targeting viral rebound and protease mutations.
  - *Study Families:* Separated randomized trial data (`ST_EPIC_HR_2022`) from real-world post-marketing observational cohorts (`ST_REBOUND_CDC_2023`).
  - *Comparability Engine:* Evaluated cross-design evidence (RCT vs Observational Cohort) and assigned contextual divergence markers.
  - *Contradiction & Negative Findings:* Cataloged viral rebound incidence under `NON_RESPONSE` and `TIME_LIMITATION`.
  - *Synthesis Certainty:* `HIGH` certainty for primary hospitalization reduction with explicit qualification regarding rebound boundaries.
  - *Status:* **PASS**

---

### Fixture 4: Molecular Diagnostics & Precision Oncology
- **Project ID:** `FIXTURE_DIAGNOSTIC_BIOMARKER`
- **Domain:** Diagnostic Accuracy & Surgical Oncology
- **Selected Framework:** `DIAGNOSTIC` (Index Test vs Reference Standard)
- **Target Condition:** Postoperative Minimal Residual Disease (MRD) in Colorectal Cancer
- **Intervention / Index Test:** Tumor-informed personalized 16-plex NGS ctDNA assay (Signatera)
- **Comparator / Reference Standard:** Standard radiologic surveillance (CT scans) and serum CEA
- **Primary Outcomes:** Diagnostic sensitivity, specificity, and recurrence-free survival
- **Pipeline Execution Results:**
  - *Framework Dynamic Selection:* Engine recognized the diagnostic accuracy context and selected `DIAGNOSTIC` framework without imposing drug/exposure conventions.
  - *Query Matrix:* 6 Supporting Queries, 3 Contradicting Queries probing false negatives, clonal hematopoiesis of indeterminate potential (CHIP) interference, and assay sensitivity limits.
  - *Comparability Engine:* Evaluated QUADAS-2 diagnostic parameters (clinical spectrum, index test platform, reference standard validity, threshold pre-specification, and clinical blinding).
  - *Synthesis Certainty:* Evaluated as `MODERATE` with recommendation for prospective interventional validation.
  - *Status:* **PASS**

---

## 3. Comparative Summary Table

| Domain Fixture | Framework | Design Types Tested | Dual-Path Queries | Family Clustering | Synthesis Verdict | Overall Result |
| :--- | :---: | :---: | :---: | :---: | :--- | :---: |
| **Oncology (Lupeol+NDV)** | `EXPERIMENTAL_IN_VITRO` | In vitro cell culture, viability assays | 9 Supp / 4 Contra | 2 Independent | `EVIDENCE_SUPPORTS_HYPOTHESIS_WITH_BOUNDARIES` | **PASS** |
| **Cardiology (SGLT2)** | `PICO` | Clinical RCT, subgroup analysis | 6 Supp / 3 Contra | 1 Clustered Family | `PRELIMINARY_EVIDENCE_REQUIRES_INVESTIGATION` | **PASS** |
| **Infectious (Antivirals)** | `PICO` | RCT, observational cohort | 6 Supp / 3 Contra | 2 Independent | `EVIDENCE_SUPPORTS_HYPOTHESIS_WITH_BOUNDARIES` | **PASS** |
| **Diagnostics (ctDNA)** | `DIAGNOSTIC` | Diagnostic accuracy, liquid biopsy | 6 Supp / 3 Contra | 1 Independent | `PRELIMINARY_EVIDENCE_REQUIRES_INVESTIGATION` | **PASS** |

---

## 4. Generalization Conclusion

The test suite confirms that the `proposal-nevisi` v8.0 engine successfully decouples evidence-seeking principles from specific therapeutic compounds or experimental systems. The system adapts its schemas, risk-of-bias frameworks, comparability criteria, and query matrices dynamically to the user's research question while maintaining rigorous epistemic integrity across all biomedical domains.
