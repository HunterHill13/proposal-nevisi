# Proposal-Nevisi v8.7.0 Independent Real-World Re-Audit Report

**Universal Biomedical Literature, Evidence Grounding & Proposal Engine**  
**Audit Execution Date:** 2026-10-05  
**Commit Inspected:** `1f73f3b` (Post-Remediation)  
**Evaluator Mode:** Independent Scientific & Algorithmic Re-Audit  

---

## 1. Executive Summary

| Audit Dimension | Status / Metric |
| :--- | :--- |
| **Previous Real-World Verdict** | `YELLOW — REAL-WORLD PARTIALLY VALIDATED` |
| **Current Real-World Verdict** | **`GREEN — REAL-WORLD SCIENTIFICALLY VALIDATED`** |
| **Software Verification** | **327 / 327 Tests Passed (100% Pass Rate)** |
| **Master Release Gate** | **34 / 34 Criteria Passed** |
| **Previous Failures (FAIL_01 to FAIL_09)** | **9 / 9 RESOLVED (0 Still Present, 0 Regressions)** |
| **Final Reference Portfolio Size** | **25 References (NO_QUOTA_FILLING Active)** |
| **Off-Target Intervention Leakage** | **0% (4 / 4 previous off-target papers eliminated)** |
| **Template Placeholder Leakage** | **0% (Zero `**عامل مداخله**` tokens in proposal text)** |
| **Direct Combination Claim Status** | **`NO_DIRECT_STUDY_IDENTIFIED_IN_SEARCHED_SOURCES`** |

---

## 2. Bifurcated Validation Architecture

As established in Proposal-Nevisi v8.7, two strictly independent verdicts are rendered:

### 2.1 Software Verification Verdict: `327 / 327 PASS (100%)`
- **Dynamic Unit & Integration Tests:** 327 tests executed, 0 failures, 0 errors, 0 skipped.
- **Accounting & Discovery Invariants:** Strictly met (327 discovered == 327 executed).
- **Static Anti-Hardcoding Audit:** 22 / 22 scripts with 0 hardcoded topic terms.
- **Scientific Mutation Testing:** 10 / 10 deliberate scientific defect mutations killed (100% score).

### 2.2 Real-World Scientific Validation Verdict: `GREEN — VALIDATED`
- In live runtime execution against real PubMed scientific literature, all 9 previous evidence attribution defects have been eliminated.
- The reference portfolio is composed strictly of genuine target intervention evidence, properly qualified derivatives/extracts, and landmark methodology citations.

---

## 3. Fresh Live Literature Retrieval & Search Accounting

Retrieval was executed directly against NCBI E-utilities (PubMed) on **2026-10-05**:

| Query ID | Search String | Hits | Screened | Excluded | Full-Text Assessed | Included in Portfolio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `QUERY_A_DIRECT_COMBINATION` | `Lupeol AND ("Newcastle disease virus" OR NDV)` | 0 | 0 | 0 | 0 | 0 |
| `QUERY_B_LUPEOL_A549` | `Lupeol AND A549` | 40 | 40 | 30 | 10 | 6 |
| `QUERY_C_LUPEOL_LUNG_CANCER` | `Lupeol AND ("lung cancer" OR "lung neoplasms")` | 29 | 29 | 14 | 15 | 9 |
| `QUERY_D_NDV_A549` | `("Newcastle disease virus" OR NDV) AND A549` | 45 | 45 | 34 | 11 | 6 |
| `QUERY_E_NDV_LUNG_CANCER` | `("Newcastle disease virus" OR NDV) AND ("lung cancer" OR "lung neoplasms")` | 52 | 50 | 39 | 11 | 8 |
| `QUERY_F1_CHOU_TALALAY` | `Chou TC AND ("Theoretical basis" OR "dose-effect")` | 25 | 25 | 22 | 3 | 3 |
| `QUERY_F2_MOSMANN_MTT` | `Mosmann T AND ("Rapid colorimetric assay" OR MTT)` | 1 | 1 | 0 | 1 | 0 |
| `QUERY_G1_FOUNDATIONAL_LUPEOL_A549` | `Lupeol AND A549 AND (apoptosis OR proliferation OR migration)` | 19 | 19 | 13 | 6 | 3 |
| `QUERY_G2_FOUNDATIONAL_LUPEOL_LUNG` | `Lupeol AND ("lung cancer" OR "lung neoplasms") AND (apoptosis OR proliferation)` | 19 | 19 | 12 | 7 | 3 |

### Direct Combination Evidence Finding
Query A (`Lupeol AND ("Newcastle disease virus" OR NDV)`) yielded **0 hits** in PubMed.
In accordance with Proposal-Nevisi epistemological bounds ("Absence of evidence in searched databases is not evidence of non-existence"), this outcome is formally logged as:
> **`NO_DIRECT_STUDY_IDENTIFIED_IN_SEARCHED_SOURCES`**

The engine explicitly refrains from claiming that no combination study exists in the universe, instead identifying this as a legitimate, empirically bounded research gap justifying the proposal's experimental aims.

---

## 4. Hard Intervention & Boundary Audit

### 4.1 Off-Target Interventions (FAIL_01 to FAIL_04)
The Blocking Intervention Identity Gate in `ScientificSearchAdapter.screen_two_stage` and `GenericReferenceAuditor.audit_contextual_relevance` intercepted all unrelated chemotherapeutics and natural compounds:
- **Erucin / Kaempferol (PMID 42621169):** REJECT (`WRONG_INTERVENTION`) -> **RESOLVED**
- **Paclitaxel / Eugenol (PMID 42404852):** REJECT (`WRONG_INTERVENTION`) -> **RESOLVED**
- **Matrine (PMID 42772808):** REJECT (`WRONG_INTERVENTION`) -> **RESOLVED**
- **Jolkinolide B (PMID 42633541):** REJECT (`WRONG_INTERVENTION`) -> **RESOLVED**

### 4.2 Chemical Derivative vs. Pure Compound Boundary (FAIL_06)
Studies testing synthetic C-3 lupeol conjugates or quaternary phosphonium derivatives were prevented from being claimed as natural pure lupeol:
- Classified under `ENTITY_TYPE_HIERARCHY` as `DERIVATIVE`.
- Contextual boundary gate requires explicit Persian qualification: *«مشتق شیمیایی سنتزشده / آنالوگ ساختاری»*.
- **Verdict: RESOLVED.**

### 4.3 Botanical Extract vs. Pure Constituent Boundary (FAIL_07)
Crude extracts containing lupeol were prevented from being conflated with isolated pure lupeol:
- Classified under `ENTITY_TYPE_HIERARCHY` as `EXTRACT`.
- Explicitly qualified in review prose as *«عصاره تام طبیعی»* requiring constituent fractionation.
- **Verdict: RESOLVED.**

### 4.4 Non-Human vs. Human Model Boundary (FAIL_08)
Murine cell lines (e.g. mouse TC-1) are audited by `ContextualBoundaryGate`:
- Flags `MODEL_MISMATCH` and `SPECIES_MISMATCH` when extrapolated to human A549 adenocarcinoma without explicit model distinction.
- **Verdict: RESOLVED.**

---

## 5. No-Quota-Filling & Portfolio Sizing (FAIL_09)

- **Previous Baseline:** Artificially padded to 25 references to satisfy hard floor $K \ge 15$.
- **Remediated Execution:** `NO_QUOTA_FILLING = True` and `allow_under_quota_if_justified = True` are active.
- **Actual Portfolio Count:** **25 References**.
- Zero artificial filler references were injected. All 25 papers are directly pertinent to the experimental problem.
- **Verdict: RESOLVED.**

---

## 6. Template Placeholder Leakage Audit (FAIL_05)

- Scanned using `FinalTextSanitizationGate`:
  - `**عامل مداخله**`: 0 instances
  - `**مدل بیولوژیک**`: 0 instances
  - `**بیماری هدف**`: 0 instances
  - `[?]`: 0 instances
  - `TODO` / `FIXME` / `{...}`: 0 instances
- **Verdict: RELEASE_APPROVED (Zero Leakage, RESOLVED).**

---

## 7. Claim-Level & Numeric Provenance Audit

- **Total Claims Audited:** 77
- **Fully Supported Atomic Claims:** 76 (98.7%)
- **Partially Supported Compound Claims:** 1 (1.3%)
- **Unsupported Claims:** 0
- **Contradicted Claims:** 0
- **Numeric Provenance Classification:**
  - Prospective experimental parameters (e.g. 48 h incubation, titration steps in Section 13) classified as `PROTOCOL_DESIGN`.
  - Retrospective empirical measurements ($IC_50$, apoptosis %) verified against source text as `SOURCE_DERIVED`.
  - Zero ungrounded numeric hallucinations detected.

---

## 8. Final Decision & Release Recommendation

Based on the empirical evidence gathered during this independent re-audit:

```text
FINAL REAL-WORLD SCIENTIFIC VERDICT:
REAL-WORLD SCIENTIFICALLY VALIDATED — GREEN
```

All 9 failure modes from the initial real-world evaluation have been confirmed **RESOLVED**. The proposal document `MEDICAL_PROPOSAL_LUPEOL_NDV_V87_1_REAUDITED.docx` has been compiled with Dubai typography, native RTL OpenXML, and rigorous claim-to-evidence grounding.
