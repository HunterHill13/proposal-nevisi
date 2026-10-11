# Scientific Rigor and Credibility Roadmap for proposal-nevisi

This roadmap provides evidence-based standards, guidelines, and mathematical frameworks to elevate the scientific rigor, precision, and credibility of the biomedical research proposal generation system `proposal-nevisi`.

## 1. EQUATOR Network Reporting Guidelines & Compliance

To ensure transparency and reproducibility, the system must enforce relevant EQUATOR Network reporting guidelines based on the study design:

- **ARRIVE 2.0 (Animal Research: Reporting of In Vivo Experiments):** Essential for preclinical animal studies. The system must enforce reporting of study design, sample size calculations, inclusion/exclusion criteria, randomization, blinding, outcome measures, and statistical methods.
- **MIQE (Minimum Information for Publication of Quantitative Real-Time PCR Experiments):** For qPCR studies, the system should prompt for RNA integrity (RIN), primer sequences, amplification efficiency, reference gene validation, and data analysis methods (e.g., $2^{-\Delta\Delta C_t}$).
- **OECD/GCCP (Good Cell Culture Practice):** For *in vitro* cell culture studies, require documentation of cell line provenance, passage number, authentication, and mycoplasma testing status.
- **CONSORT (Consolidated Standards of Reporting Trials):** For clinical randomized controlled trials, enforce the inclusion of a participant flow diagram, detailed randomization sequence generation, allocation concealment, blinding details, and clearly defined primary/secondary outcomes.
- **STROBE (Strengthening the Reporting of Observational Studies in Epidemiology):** For observational studies (cohort, case-control, cross-sectional), require explicit descriptions of setting, participant selection criteria, variable definitions, bias mitigation, and handling of missing data.

**Implementation in proposal-nevisi:** Integrate a dynamic checklist system that triggers specific metadata prompts and methodology constraints based on the selected "Study Type" (Section 14) to ensure all required fields for the respective guideline are populated.

## 2. Formal Bio-statistical Sample Size & Power Calculation

Sample size justification is a critical requirement. The proposal system must embed the following mathematical formulas for the primary study designs (Section 22):

### A. *In Vitro* Replicate Power
For standard *in vitro* assays comparing continuous outcomes between groups, the sample size $n$ per group can be estimated using the two-sample t-test formula:
$$ n = \frac{2(Z_{1-\alpha/2} + Z_{1-\beta})^2 \sigma^2}{d^2} $$
Where:
- $Z_{1-\alpha/2}$ = Standard normal deviate for significance level (e.g., 1.96 for $\alpha=0.05$)
- $Z_{1-\beta}$ = Standard normal deviate for power (e.g., 0.84 for 80% power)
- $\sigma$ = Estimated standard deviation
- $d$ = Minimum clinically/biologically significant difference

### B. *In Vivo* Animal Group Sizing
- **Resource Equation Method (when $\sigma$ and $d$ are unknown):**
  $$ E = (\text{Total number of animals}) - (\text{Number of groups}) $$
  Target $E$ should be between 10 and 20.
- **Cohen's $f$ for ANOVA:**
  For comparing multiple groups, determine total sample size $N$ using effect size $f$:
  $$ N = \frac{\lambda}{f^2} $$
  Where $\lambda$ is the non-centrality parameter derived from $\alpha$, power, and degrees of freedom.

### C. Clinical 2-Arm RCT (Kelsey/Fleiss Formulas)
For binary outcomes (proportions):
$$ n = \frac{(Z_{1-\alpha/2} + Z_{1-\beta})^2 [p_1(1-p_1) + p_2(1-p_2)]}{(p_1 - p_2)^2} $$
Where $p_1$ and $p_2$ are the anticipated event proportions in the control and intervention groups, respectively.

### D. Diagnostic Sensitivity/Specificity Sizing
To estimate the sample size for a required Sensitivity ($Sn$):
$$ N_{cases} = \frac{Z_{1-\alpha/2}^2 \cdot Sn(1-Sn)}{W^2} $$
Where $W$ is the maximum acceptable width of the 95% confidence interval (margin of error).
Total $N$ depends on disease prevalence ($P$):
$$ N_{total} = \frac{N_{cases}}{P} $$

## 3. Reagent and Biological Resource Authentication

Adhering to the NIH Rigor and Reproducibility Mandate and utilizing the Research Resource Identifiers (RRID) standard:

- **Cell Line Authentication:** Proposals must explicitly state the use of Short Tandem Repeat (STR) profiling for human cell line authentication and mandate routine mycoplasma contamination testing.
- **Antibody Validation:** Require specification of RRIDs for all antibodies. Proposals must detail validation steps for the specific application (e.g., knockout validation, western blot specificity).
- **Chemical/Reagent Purity:** Specify CAS Registry Numbers and mandate purity verification (e.g., $\ge 95\%$ via HPLC/MS) for key experimental compounds and drugs.

**Implementation:** Add validation constraints in the "Materials and Methods" or "Variables" table (Section 11/13/21) requiring RRID/CAS inclusion and authentication protocols.

## 4. Pre-emptive Risk of Bias (RoB) Mitigation

Risk of Bias (RoB) must be addressed proactively in the research design phase:

- **SYRCLE's Risk of Bias Tool for Animal Studies:** The system must prompt for specific mitigation strategies including: sequence generation (randomization), baseline characteristics matching, allocation concealment, random housing, blinded interventions, random outcome assessment, and blinding of outcome assessors.
- **Cochrane RoB-2 for Clinical Trials:** Enforce protocols mitigating bias arising from: the randomization process, deviations from intended interventions, missing outcome data, measurement of the outcome, and selection of the reported result.

**Implementation:** Embed RoB checklists into the methodology (Section 13) and limitation (Section 26) sections. Force researchers to explicitly state how blinding and randomization will be achieved and verified.

## 5. Evidence Synthesis & Claim Grounding (GRADE Framework)

To elevate the Literature Review (Section 3), evidence must be synthesized using the GRADE (Grading of Recommendations Assessment, Development and Evaluation) framework.

- **Weighting Literature:** Automatically parse and categorize cited literature into GRADE certainty levels:
  - **High:** Well-designed RCTs or meta-analyses of RCTs without serious limitations.
  - **Moderate:** RCTs with limitations or exceptional observational studies.
  - **Low/Very Low:** Observational studies (cohort, case-control), case series, or expert opinions.
- **Claim Grounding:** AI-generated claims must be grounded in High or Moderate certainty evidence. The system should penalize or flag claims relying exclusively on Low certainty evidence unless appropriately hedged.

**Implementation:** The system's CitationTracker and Passage Grounding modules must evaluate the study design of the cited source and assign a corresponding evidence weight, explicitly describing the certainty of the aggregated evidence in the text.
