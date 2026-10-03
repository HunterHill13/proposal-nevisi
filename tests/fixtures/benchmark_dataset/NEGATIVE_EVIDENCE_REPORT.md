# NEGATIVE AND CONTRADICTORY EVIDENCE REPORT
**Proposal-Nevisi v7.0 Adversarial Evidence Synthesis**  
**Date:** 2026-10-03  
**Topic:** Evaluation of Combined Lupeol and Newcastle Disease Virus on A549 Lung Cancer Cells In Vitro  

---
## 1. Executive Summary & Adversarial Retrieval Framework
Scientific integrity requires that literature research does not merely search for confirmatory studies, but actively executes adversarial searches designed to discover contradictory, null, non-reproducible, or boundary-limiting evidence.
In v7.0, systematic adversarial searches were executed across 6 mandatory negative facets:
1. **Antagonism & Subadditivity:** Investigating potential viral envelope disruption or drug interference.
2. **High-Dose Toxicity & Off-Target Effects:** Benchmarking solvent thresholds (DMSO) and non-specific membrane damage.
3. **Cellular Resistance & Non-Responsiveness:** Identifying survival signaling persistence in A549 cells under monotherapies.
4. **Type I Interferon Neutralization:** Assessing host innate antiviral clearance mechanisms in normal lung epithelium.
5. **Solubility & Aqueous Limits:** Cataloging precipitation boundaries of lipophilic triterpenoids.
6. **Negative & Null Findings:** Documenting sub-micromolar inefficacy and monotherapy plateaus.

---
## 2. Adversarial Evidence Ledger
| ID | Facet | Source | Verbatim Finding | Polarity | Taxonomy | Mitigation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **NEG-LEDGER-01** | SOLUBILITY_BIOAVAILABILITY_LIMITS | Luo X et al. (2025, PMID 39662867) & Soares DCF et al. (2025, PMID 40638886) | Lupeol is practically insoluble in water (< 1.0 μg/mL at 25°C). Concentrations exceeding 8... | `QUALIFICATION` | `D_DOSE_DEPENDENT_DIVERGENCE` | Restricts maximum in vitro Lupeol test concentration to 80 μM and mand... |
| **NEG-LEDGER-02** | RESISTANCE_OR_NON_RESPONSIVENESS | Hirsch FR et al. (2016, PMID 27598681) & He W et al. (2018, PMID 30003730) | Subpopulations of A549 lung adenocarcinoma cells exhibit residual Akt phosphorylation and ... | `CONTEXT_DEPENDENT` | `B_CONTEXTUAL_DISAGREEMENT` | Provides the biological necessity for combination therapy: co-treatmen... |
| **NEG-LEDGER-03** | INTERFERON_INDUCED_VIRAL_CLEARANCE | Li H et al. (2025, PMID 39642411) & Ginting TE et al. (2026, PMID 42699700) | Normal human bronchial epithelial cells (BEAS-2B) mount rapid and robust IFN-β and IFN-λ u... | `SUPPORT` | `B_CONTEXTUAL_DISAGREEMENT` | Validates the project's safety hypothesis: NDV is inherently self-limi... |
| **NEG-LEDGER-04** | HIGH_DOSE_TOXICITY_OFF_TARGET | Razura-Carmona FF et al. (2025, PMID 40675401) & Soares DCF et al. (2025, PMID 40638886) | Free unformulated lupeol at concentrations > 100 μM displays mild non-specific membrane di... | `QUALIFICATION` | `D_DOSE_DEPENDENT_DIVERGENCE` | In vitro experimental titration in A549 must be strictly capped at 80 ... |
| **NEG-LEDGER-05** | ANTAGONISM_OR_SUBADDITIVITY | Systematic 4-Database Saturation Search (2026) | Exhaustive retrieval across 4 databases yielded 0 published studies reporting pharmacologi... | `NULL` | `C_NULL_RESULT` | Establishes that antagonism has not been empirically reported, but man... |
| **NEG-LEDGER-06** | NEGATIVE_OR_NULL_FINDINGS | Torres-Sanchez A et al. (2024, PMID 38931361) & Bhatt M et al. (2021, PMID 32329697) | Low sub-micromolar doses of Lupeol (< 5 μM) exert negligible cytotoxic inhibition (p > 0.0... | `QUALIFICATION` | `D_DOSE_DEPENDENT_DIVERGENCE` | Defines the biologically active cytotoxic threshold: concentrations < ... |

---
## 3. Contradiction vs. Qualification Taxonomy Analysis
All identified tensions across the literature were rigorously categorized using the Categories A–F taxonomy. **Zero direct contradictions (Category A) were identified**, confirming that observed divergent outcomes in the literature represent **contextual qualifications (Category B)**, **dose-dependent divergences (Category D)**, or **monotherapy plateaus (Category C)** rather than direct empirical irreproducibility.

### Summary of Identified Tensions:
### TENS-01: Solvent Concentration & Solubility Boundary (Aqueous Precipitation vs Cytotoxicity)
- **Studies Involved:** STUDY-09 (Luo X et al., 2025) vs. STUDY-13 (Soares DCF et al., 2025)
- **Classification:** `D_DOSE_DEPENDENT_DIVERGENCE` (Direct Contradiction: `False`)
- **Model Difference:** Free DMSO solubilization vs Liposomal carrier encapsulation
- **Scientific Explanation:** Pure lupeol precipitates at > 80 μM in aqueous RPMI, whereas liposomal encapsulation allows higher bioavailable delivery without DMSO toxicity.
- **Resolution for Proposed Study:** Maintain final vehicle DMSO concentration strictly at <= 0.1% (v/v) and verify solubility in complete RPMI-1640 medium.

### TENS-02: Cytotoxic Threshold Divergence: Sub-Micromolar Inefficacy vs Micromolar Apoptosis
- **Studies Involved:** STUDY-07 (Torres-Sanchez A et al., 2024) vs. STUDY-03 (He W et al., 2018)
- **Classification:** `D_DOSE_DEPENDENT_DIVERGENCE` (Direct Contradiction: `False`)
- **Model Difference:** Low concentration metabolic exposure (< 10 μM) vs pharmacological titration (25-100 μM)
- **Scientific Explanation:** Biphasic concentration response: low concentrations act as mild metabolic regulators, while higher concentrations (> 25 μM) trigger mitochondrial membrane depolarization and apoptosis.
- **Resolution for Proposed Study:** Establish clear 5-point dose titration curves (10, 20, 40, 60, 80 μM) to isolate antineoplastic cytotoxicity from baseline metabolic noise.

### TENS-03: Differential Viral Permissiveness: A549 Carcinoma vs Normal Bronchial Epithelium
- **Studies Involved:** STUDY-15 (Liang Y et al., 2021) vs. STUDY-19 (Ginting TE et al., 2026)
- **Classification:** `B_CONTEXTUAL_DISAGREEMENT` (Direct Contradiction: `False`)
- **Model Difference:** Malignant human lung carcinoma cells (A549, IFN-deficient) vs Normal human lung epithelial cells (BEAS-2B, IFN-competent)
- **Scientific Explanation:** A549 cells lack functional Type I interferon feedback, allowing uncontrolled viral oncolysis, while normal BEAS-2B cells induce IFN-β to clear NDV.
- **Resolution for Proposed Study:** Compare A549 and BEAS-2B under identical infection conditions (MOI = 0.1, 1, 5) to empirically quantify the Selectivity Index.

### TENS-04: Single-Agent Monotherapy Plateau (Incomplete Apoptotic Eradication)
- **Studies Involved:** STUDY-03 (He W et al., 2018) vs. STUDY-38 (Herbst RS et al., 2018)
- **Classification:** `C_NULL_RESULT` (Direct Contradiction: `False`)
- **Model Difference:** Single-agent monotherapy in vitro plateau vs multi-targeted combination requirements
- **Scientific Explanation:** Monotherapy Lupeol fails to eliminate 100% of colonies due to residual Akt/ERK survival signaling.
- **Resolution for Proposed Study:** Directly justifies the hypothesis of combining Lupeol with oncolytic NDV to overcome single-agent resistance via multi-target synergy.

### TENS-05: Synthetic Derivative Potency vs Natural Core Molecule Baseline
- **Studies Involved:** STUDY-11 (Deng S et al., 2024) vs. STUDY-03 (He W et al., 2018)
- **Classification:** `E_METHODOLOGICAL_DISAGREEMENT` (Direct Contradiction: `False`)
- **Model Difference:** Semi-synthetic thiazolidinedione-conjugated lupeol vs unmodified natural Lupeol
- **Scientific Explanation:** Chemical derivatization at C-3 lowers IC50 to ~12 μM, whereas natural unmodified Lupeol requires ~40 μM. Findings on conjugates must not be falsely extrapolated to pure natural lupeol.
- **Resolution for Proposed Study:** Proposal strictly uses pure natural Lupeol (PubChem CID 259846, purity >= 98%) as the primary test compound, establishing its authentic natural baseline.

---
## 4. Methodological Safeguards Integrated into Proposal
1. **DMSO Solvent Boundary:** Final concentration strictly maintained at $\le 0.1\%$ (v/v) to prevent solvent-induced membrane artifact.
2. **Concentration Window:** Lupeol testing capped at $80\ \mu\text{M}$ to prevent aqueous precipitation in complete medium.
3. **Normal Cell Benchmarking:** Inclusion of normal human bronchial epithelial cells (BEAS-2B) to empirically establish the Selectivity Index ($SI > 2.0$).
4. **Chou-Talalay CI Strictness:** Primary hypothesis explicitly defined as $CI < 1.0$ to be empirically tested; synergy is never asserted as pre-existing fact.

*End of Negative Evidence Report.*