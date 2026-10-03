# EVIDENCE SYNTHESIS POLICY & PROTOCOL
## Multi-Dimensional Evidence Weighing, Certainty Profiling, and Anti-Double Counting Standards

**Policy Version:** 8.0  
**Scope:** Universal Medical & Biomedical Research Proposals  
**Governing Principle:** Evidence-Weighted Synthesis Over Simple Majority Vote  

---

## 1. Prohibition of Simple Majority Voting

A fundamental failure mode in automated literature analysis is "vote counting" (e.g., asserting that because 7 studies report a positive effect and 3 report a null effect, the scientific consensus supports efficacy).

Under this policy, **simple majority voting is strictly prohibited**. 

Evidence synthesis must weigh each study by:
1. **Methodological Directness:** Does the study test the exact biological system, model, dose, and outcome of interest?
2. **Risk of Bias & Study Design Quality:** Was the experiment properly controlled, randomized, blinded, and adequately powered?
3. **Precision & Effect Size:** Are statistical confidence intervals narrow, or are findings marginal ($p \approx 0.048$ with wide CIs)?
4. **Contextual Divergence:** Do the 3 negative studies use physiological drug concentrations while the 7 positive studies use supra-physiological, non-translatable concentrations?

A single, rigorously controlled, low-bias study with high directness outweighs multiple small, unblinded, poorly controlled publications.

---

## 2. Multi-Dimensional Evidence Certainty Framework

Evidence certainty is evaluated across eight distinct dimensions (adapted from GRADE principles for basic and translational science):

| Dimension | Description | Evaluation Scale |
| :--- | :--- | :--- |
| **1. Directness** | Extent to which the study population, intervention, and outcome match the target research question. | High / Moderate / Indirect / Surrogate |
| **2. Consistency** | Similarity of effect estimates and biological direction across independent laboratories and studies. | Consistent / Explained Inconsistency / Unexplained Inconsistency |
| **3. Precision** | Sample size adequacy, power calculation presence, and width of effect confidence intervals. | Precise / Imprecise / Severely Underpowered |
| **4. Study Quality** | Validity of assay protocols, reagent validation, appropriate positive/negative controls. | Robust / Acceptable / Methodologically Flawed |
| **5. Risk of Bias** | Design-aware bias assessment (RoB2, SYRCLE, QUADAS-2, or in vitro replication criteria). | Low / Some Concerns / High / Critical |
| **6. Applicability** | Degree of biological and translational relevance (e.g., cell line vs. primary tissue vs. human patient). | Direct Human / Validated Model / Distant Analogy |
| **7. Evidence Volume** | Total independent studies and biological replicates supporting the specific assertion. | Substantial / Moderate / Sparse / Single-Study |
| **8. Contradiction Burden** | Proportion and severity of verified contradictory or null publications. | Negligible / Contextual / Substantial / Severe |

*Scoring Prohibition:* The system must not generate fabricated composite pseudo-scores such as `8.7/10`. Evaluations must remain qualitatively structured and grounded in the audited dimensions above.

---

## 3. Evidence Directness vs. Evidence Quality

Evidence hierarchy must not blindly privilege clinical trials over basic experimental research when answering mechanistic questions:
- For a **mechanistic pathway hypothesis** (e.g., receptor phosphorylation or caspase-dependent cleavage), a well-controlled in vitro biochemical assay with genetic knockouts is **more direct** than an observational clinical cohort.
- For a **clinical efficacy or safety question**, randomized clinical trials are **more direct** than animal or cell culture models.

Directness and Quality must be evaluated independently:
$$\text{Evidence Weight} = f(\text{Directness}, \text{Quality}, \text{Consistency}, \text{Precision})$$

---

## 4. Study Family & Duplicate Publication De-Duplication

To prevent artificial inflation of evidence volume ("double-counting"):
1. **Shared Cohort Detection:** The engine must identify secondary analyses of pre-existing datasets (e.g., NHANES, UK Biobank, TCGA, or specific trial registries like NCT numbers). Multiple publications derived from the identical cohort must be grouped into a single **Study Family**.
2. **Multi-Center Trial Separation:** Preliminary phase II reports, interim analyses, and final 5-year follow-ups of the same clinical trial must not be treated as independent confirmatory studies.
3. **Primary vs. Secondary Separation:** A systematic review or meta-analysis must not be counted as independent evidence alongside the primary studies it reviewed. If primary studies $A, B,$ and $C$ are cited, meta-analysis $M$ (which synthesized $A, B, C$) cannot be cited as a "fourth independent confirmation".

---

## 5. Explicit Treatment of Uncertainty as a First-Class Citizen

When scientific evidence is absent, equivocal, or conflicting, the engine must never smooth over discrepancies to produce an artificially coherent narrative.

The engine must explicitly assign and render one of the standardized epistemic statuses:
- `UNKNOWN`: No empirical data located within the target domain.
- `NOT_REPORTED`: The primary publication fails to specify key parameters (e.g., solvent concentration, cell passage, blinding).
- `INSUFFICIENT_EVIDENCE`: Available studies are underpowered or single-replicate.
- `CONFLICTING_EVIDENCE`: High-quality studies report mutually irreconcilable findings under comparable conditions.
- `INDIRECT_EVIDENCE`: Findings observed only in surrogate models or distant taxonomic species.

---

## 6. Numerical Traceability & Anti-Hallucination Barrier

Every quantitative figure stated in the research proposal (e.g., $IC_{50}$ values, hazard ratios, viral titers, multiplicity of infection, sample sizes, and p-values) **must link to a verifiable Fact Entry in `EVIDENCE_LEDGER.json`**.

If a metric is omitted from the retrieved source literature, the system must write:
$$\text{Metric: } \mathbf{NOT\_REPORTED}$$
The model is strictly prohibited from interpolating, estimating, or hallucinating quantitative parameters.
