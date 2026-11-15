# Objective Quality & Scientific Rubric: Professor Namoosi (v14.1.0)
## Objective Evaluation Criteria for Isolated Proposal Quality Auditing

> **Scope:** This document is the exclusive and binding evaluation rubric executed by the isolated zero-context auditor subagent (`professor-namoosi-auditor`).  
> **Zero-Context Mandate:** The isolated auditor operates with zero conversational memory, auditing exclusively the physical artifacts on disk (`output/[topic_slug]/proposal.md` and `proposal.docx`) against the binary hard constraints and qualitative criteria defined below.

---

## 1. Hard Constraints Table (Binary Immediate Rejection Gate)

If ANY of the following 7 Hard Constraints are violated, the proposal immediately receives **`REJECT_HARD_FAIL`** and is returned to the authoring agent for surgical remediation:

| Error ID | Constraint Name | Technical Definition & Failure Threshold | Enforcement Action |
| :--- | :--- | :--- | :---: |
| **`HARD-01`** | **`DATA_INVARIANT_VIOLATION`** | Any modified, rounded, hallucinated, or ungrounded numbers (doses, $IC_{50}$ concentrations, statistical test statistics, $p$-values, adjusted odds ratios, epidemiological statistics, or reference IDs). | **Immediate Rejection** |
| **`HARD-02`** | **`PHANTOM_CITATION_VIOLATION`** | Any synthetic reference, citation lacking a verifiable PMID or DOI, or paper nonexistent in PubMed/Europe PMC. | **Immediate Rejection** |
| **`HARD-03`** | **`PIPELINE_BYPASS_VIOLATION`** | Bypassing the official pipeline (`run_research_pipeline.py`) or failing to produce the mandatory 28 canonical Pajooheshyar section headings. | **Immediate Rejection** |
| **`HARD-04`** | **`CROSS_DOMAIN_ENTITY_LEAKAGE`** | Leakage of cell-culture parameters (cell seeding, MTT, apoptosis, $IC_{50}$, cell-free blank) into non-laboratory domains (health systems, epidemiology, clinical surveys). | **Immediate Rejection** |
| **`HARD-05`** | **`LATEX_LEAKAGE_IN_WORD`** | Unconverted raw LaTeX delimiters (`$`, `\frac`, `\sum`) leaking into readable text rather than native Word OMML equations. | **Immediate Rejection** |
| **`HARD-06`** | **`BANNED_CLICHE_AND_META_LEAKAGE`** | Formulaic machine transition clichés («در این راستا»، «نقش بسزایی دارد») or extraneous conversational assistant meta-disclaimers leaking into proposal text (violating the Clean Author Manuscript Delivery Standard). | **Immediate Rejection** |
| **`HARD-07`** | **`WORD_VISUAL_STANDARD_VIOLATION`** | Deviation from approved Word typography standards: missing cover page header, unstyled raw markdown stars (`**`), or distorted word spacing caused by soft line breaks. | **Immediate Rejection** |

---

## 2. Objective Multi-Dimensional Pass/Fail Checklist

Once all Hard Constraints pass, the isolated auditor verifies the following criteria:

### 2.1. Structural Canonical Pajooheshyar 28 Sections
- [ ] Exactly 28 canonical sections present, numbered sequentially from Section 1 (Topic) to Section 28 (References).
- [ ] No merged, omitted, or modified H2 (`##`) headings.

### 2.2. Biostatistical Coherence & Archetype Alignment
- [ ] Section 22 contains a clear, mathematically sound sample size derivation tailored to the research archetype:
  - **Health Systems / Health Policy:** Cochran population formula with cluster design effect ($\text{DEFF} \ge 1.5$) and attrition buffer.
  - **Observational Epidemiology:** Prevalence-based Cochran formula with finite population correction if applicable.
  - **Clinical Trial (RCT):** Two-arm comparative trial formula with CONSORT power ($1-\beta \ge 0.80$) and intention-to-treat (ITT) framework.
  - **In Vivo Animal Models:** Festing & Mead's resource allocation equation ($E = N - B - T \in [10, 20]$) adhering to ARRIVE 2.0.
  - **In Vitro Bioassays:** Factorial ANOVA replicate design ($\ge 3$ biological replicates), vehicle control (DMSO $< 0.1\%$), and cell-free blank interference controls.
  - **Diagnostic Accuracy:** Buderer sensitivity/specificity formula compliant with STARD guidelines.
  - **Usability & Digital Health:** Nielsen-Landauer problem discovery model and SUS scale sample sizing.
- [ ] 100% numerical consistency between Section 22 sample sizes and Section 27 experimental arm/group counts.

### 2.3. Vancouver Citation Integrity & Monotonic Order
- [ ] Citation numbering strictly starts at `[1]` and increments monotonically without gaps or unreferenced orphan claims.
- [ ] 100% concordance between in-text citation markers `[n]` in Sections 2–3 and Reference `[n]` metadata in Section 28.
- [ ] Adequate bibliographic depth (typically 15 to 40 authoritative references).

### 2.4. Zero-Bias Evidence Architecture & Epistemic Honesty
- [ ] Dual-path literature retrieval executed (supporting vs. contradicting/adverse evidence).
- [ ] If no negative or contradicting papers exist in international databases, an explicit publication bias caveat is injected into Sections 3 and 26.
- [ ] Risk-of-bias framework matches the study archetype (QUADAS-2 for diagnostic, STROBE for observational, Cochrane RoB-2 for clinical trials, SYRCLE for animal studies).

### 2.5. Stylometry, Prose Cadence & Burstiness
- [ ] Sentence length distribution exhibits healthy statistical variance (standard deviation $\sigma \ge 8.0$ words per sentence).
- [ ] Rigorous orthographic hygiene: zero-width non-joiners (ZWNJ) preserved, zero raw machine em-dashes.

### 2.6. Consensus Heuristic Readiness Score
- [ ] Consensus score calculated across the 6 study section dimensions.
- [ ] **Approval Threshold:** Heuristic Readiness Score $\le 2.0$ (Exceptional $\le 1.5$) with **0 Blocker flaws**.
