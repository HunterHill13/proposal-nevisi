# CITATION ENTAILMENT & ANTI-OVERCLAIM POLICY
## Atomic Claim Verification, Strict Passage Entailment, and Zero-Padding Enforcement

**Policy Version:** 8.0  
**Scope:** Universal Medical & Biomedical Research Proposals  
**Governing Principle:** Formal Separation of Bibliographic Relevance from Epistemic Entailment  

---

## 1. Relevance vs. Entailment Distinction

The most pervasive defect in scientific AI writing is confusing **Topical Relevance** with **Claim Entailment**:
- **Relevance:** The cited paper discusses the same biological compound, disease, or organ system (e.g., both paper and proposal mention "A549 cells" and "curcumin").
- **Entailment:** The text of the cited paper contains empirical findings, measurements, or logical conclusions that mathematically and scientifically prove the specific assertion attached to the citation.

A paper may be 100% relevant to the subject matter yet provide zero entailment for the cited claim (e.g., citing a paper showing curcumin toxicity to support the assertion that curcumin synergizes with viral vectors).

Under this policy, **relevance alone is insufficient**. Every cited sentence must satisfy strict textual or data entailment.

---

## 2. Seven-Level Entailment Classification Scale

Every scientific claim in the proposal is mapped to one of seven formal entailment states:

```text
                                SCIENTIFIC STATEMENT
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
         EMPIRICALLY TESTED                             NOT TESTED EMPIRICALLY
                 │                                               │
    ┌────────────┴────────────┐                     ┌────────────┴────────────┐
    ▼                         ▼                     ▼                         ▼
[ DIRECTLY_SUPPORTED ]  [ PARTIALLY_SUPPORTED ] [ INFERRED ]           [ HYPOTHESIS_ONLY ]
Paper demonstrates       Paper proves a          Logical deduction     Theoretical
exact claim under        subset of claim or      synthesizing multiple conjecture without
identical conditions.    intermediate outcome.   empirical facts.      direct measurement.
```

| Entailment Level | Code | Definition & Criteria | Permissible Proposal Language |
| :--- | :--- | :--- | :--- |
| **Level 1** | `DIRECTLY_SUPPORTED` | Primary data or author conclusion explicitly affirms the exact relationship, dose, and model. | Definitive: *"demonstrates"*, *"shows"*, *"confirms"* |
| **Level 2** | `PARTIALLY_SUPPORTED` | Evidence affirms the core direction but differs in secondary parameters (e.g., different cell line). | Qualified: *"indicates"*, *"partially supports"*, *"in [specific model]"* |
| **Level 3** | `INDIRECTLY_SUPPORTED`| Evidence from a surrogate marker, analogous drug class, or upstream pathway component. | Indirect: *"suggests"*, *"by analogy with"*, *"provides indirect evidence"* |
| **Level 4** | `INFERRED` | Logical synthesis derived from two or more distinct empirical premises without direct co-testing. | Inferential: *"it is inferred that"*, *"rationally deduced"* |
| **Level 5** | `HYPOTHESIS_ONLY` | Theoretical rationale or author speculation unsupported by experimental measurement. | Speculative: *"we hypothesize"*, *"postulated"*, *"conjectured"* |
| **Level 6** | `UNSUPPORTED` | Cited paper contains no data, text, or rationale supporting the assertion. | **PROHIBITED** (Sentence must be excised or citation removed) |
| **Level 7** | `CONTRADICTED` | Cited paper's findings directly refute the statement attached to its citation marker. | **CRITICAL AUDIT FAILURE** (Immediate halt) |

---

## 3. The Causal vs. Correlational Language Gate

The engine strictly prohibits elevating observational or correlational findings into causal claims:
- If a study reports: *"Serum biomarker X was significantly elevated in patients with myocardial infarction ($r = 0.65$)"*, the proposal **must not state**: *"Biomarker X causes myocardial infarction"*.
- Acceptable formulation: *"Elevated biomarker X is significantly associated with myocardial infarction, suggesting potential involvement in cardiac remodeling."*

### Automated Syntax Regex Filters:
Any claim using causal verbs (`causes`, `drives`, `induces`, `triggers`, `is responsible for`) linked to a study with study design `OBSERVATIONAL_COHORT_CASE_CONTROL` or `CROSS_SECTIONAL` triggers an automatic **OVERCLAIM_DETECTION_FLAG**.

---

## 4. Prohibition of Citation Padding (Zero Decorative References)

No reference may be added to a proposal merely to increase the bibliography count or create an appearance of erudition.

For every reference $R_i$ admitted to `PROPOSAL_REFERENCE_SET.json`:
1. It must be explicitly cited in the narrative text with an inline bracketed index (e.g., `[14]`).
2. It must be linked to at least one atomic claim in `CLAIM_EVIDENCE_MAP.json`.
3. It must have verified text excerpts or data points in `EVIDENCE_LEDGER.json`.

Any reference failing these criteria is flagged as `UNUSED_REFERENCE` or `DECORATIVE_PADDING` and is immediately excised prior to document compilation.

---

## 5. Passage-Level Extraction & Provenance Audit

To guarantee auditability:
- For every primary claim concerning doses, concentrations, binding affinities, and IC50 values, the auditor extracts the exact supporting passage from the source publication's text, tables, or figure legends.
- If full text is unavailable and evaluation relies on the abstract, the claim must be explicitly annotated with:
$$\text{Extraction Mode: } \mathbf{ABSTRACT\_ONLY}$$
- Conclusions requiring granular methodology (e.g., exact vehicle concentration or wash steps) cannot be sustained solely by `ABSTRACT_ONLY` sources.
