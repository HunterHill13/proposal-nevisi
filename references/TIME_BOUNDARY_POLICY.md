# TIME BOUNDARY & HISTORICAL EVIDENCE POLICY
## Recency Thresholds, Foundational Justifications, and Temporal Evidence Stratification

**Policy Version:** 8.0  
**Scope:** Universal Medical & Biomedical Research Proposals  
**Governing Principle:** Temporal Relevance Balanced with Foundational Methodological Legitimacy  

---

## 1. Dual-Tier Temporal Evidence Policy

Scientific literature ages at differing rates across biomedical domains:
- **Fast-Moving Horizons (Therapeutic Efficacy, Molecular Targets, Clinical Guidelines):** Requires contemporary evidence reflecting current standards of care and current genomic/biological consensus.
- **Foundational Horizons (Mathematical Models, Seminal Biological Discoveries, Validated Assays):** Retains permanent epistemic validity and must not be artificially excluded simply due to chronological age.

To balance these requirements without arbitrary age discrimination, the engine establishes two operational tiers:

```text
                             BIBLIOGRAPHIC CORPUS
                                      │
                   ┌──────────────────┴──────────────────┐
                   ▼                                     ▼
        RECENT PRIMARY EVIDENCE               FOUNDATIONAL EVIDENCE
     Publication Year >= 2020                 Publication Year < 2020
   (CURRENT_YEAR - 6 sliding window)      (Requires explicit justification)
                   │                                     │
         Must constitute the                   Permissible ONLY with verified
       majority of the proposal's             FOUNDATIONAL_JUSTIFICATION
        evidence base (>= 75%).                 in research ledger.
```

---

## 2. Default Temporal Thresholds

1. **Current Operating Year:** Calculated dynamically from the environment runtime (e.g., 2026).
2. **Primary Literature Window:**
   $$\text{Year}_{\text{primary}} \ge \text{CURRENT\_YEAR} - 6 \quad (\text{i.e., } \ge 2020)$$
3. **Target Proportion:** At least $75\%$ to $80\%$ of all cited primary evidence must reside within this 6-year window to reflect current biomedical knowledge.

---

## 3. Foundational Exception Framework (`FOUNDATIONAL_JUSTIFICATION`)

Studies published prior to $\text{CURRENT\_YEAR} - 6$ (prior to 2020) are fully legitimate and protected from arbitrary pruning **if and only if** they satisfy one of the standardized foundational criteria:

| Exception Class | Approved Justification Codes | Illustrative Historical Examples |
| :--- | :--- | :--- |
| **Mathematical / Pharmacological Framework** | `FOUNDATIONAL_MATHEMATICAL_MODEL` | Chou & Talalay (1984) Median-Effect & Combination Index equation; Bliss (1939) Independence. |
| **Original Diagnostic Standard** | `ORIGINAL_DIAGNOSTIC_CRITERIA` | WHO diagnostic classification, original Gold Standard staging criteria. |
| **Seminal Biological Discovery** | `SEMINAL_DISCOVERY` | First isolation or characterization of a virus, receptor, oncogene, or signaling pathway. |
| **Standardized Assay Methodology** | `STANDARDIZED_ASSAY_METHOD` | Original description of MTT colorimetric assay (Mosmann, 1983); plaque assay protocol. |
| **Landmark Trial / Benchmark** | `LANDMARK_HISTORICAL_BENCHMARK` | Definitive seminal clinical trial or foundational epidemiological study establishing baseline risk. |
| **Original Drug Synthesis** | `ORIGINAL_CHEMICAL_SYNTHESIS` | Primary extraction, NMR structural elucidation, or synthesis of a natural product/compound. |

---

## 4. Metadata Recording Standard

For every reference admitted with $\text{Year} < \text{CURRENT\_YEAR} - 6$, the reference audit ledger (`PROPOSAL_REFERENCE_SET.json` and `FINAL_REFERENCE_VALIDITY_AUDIT.json`) must record:

```json
{
  "ref_id": "REF_CHOU_1984",
  "citation_marker": "[1]",
  "title": "Quantitative analysis of dose-effect relationships...",
  "year": 1984,
  "temporal_tier": "FOUNDATIONAL/HISTORICAL_EVIDENCE",
  "foundational_justification": {
    "is_justified": true,
    "category": "FOUNDATIONAL_MATHEMATICAL_MODEL",
    "rationale": "Defines the canonical Chou-Talalay Combination Index equation used to quantitatively calculate synergy versus antagonism in Section 7 (Methodology)."
  }
}
```

If an older paper lacks a valid justification, the audit flags it as:
$$\mathbf{UNJUSTIFIED\_HISTORICAL\_REFERENCE}$$
The reference must either be updated with contemporary primary literature or provided with valid foundational rationale.

---

## 5. Recency vs. Relevance Priority Hierarchy

Chronological recency must never supersede directness or quality:
$$\text{Study Selection Priority: } \mathbf{Directness} \succ \mathbf{Relevance} \succ \mathbf{Evidence\ Quality} \succ \mathbf{Study\ Design} \succ \mathbf{Recency}$$

A highly direct, methodologically pristine study from 2018 is vastly superior to a tangential, low-quality paper published in 2025.
