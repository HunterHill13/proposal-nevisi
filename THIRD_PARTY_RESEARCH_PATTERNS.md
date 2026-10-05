# Third-Party Research Patterns & Provenance Documentation
## Proposal-Nevisi v8.6 Research Recall, Deep Reading & Citation Validation Upgrade

This document records the provenance, architectural analysis, adaptation rationale, and licensing compliance for external research-grade workflows integrated from open-source biomedical research repositories into Proposal-Nevisi v8.5 and v8.6.

---

### 1. Source Repositories & License Compliance

Both source repositories are licensed under the **MIT License**. In compliance with MIT license conditions, the original copyright notices and permission notices are acknowledged, and all substantial logic reused has been adapted, sanitized, generalized to topic-agnostic biomedical architecture, and integrated with full attribution.

#### Source A: AIPOCH Medical Research Skills
- **Repository:** `https://github.com/aipoch/medical-research-skills`
- **License:** MIT License
- **Copyright:** (c) 2024-2026 AIPOCH
- **Architecture Role:** Conceptual workflows for biomedical search strategy construction, multi-stage paper reading, claim verification, topic saturation/whitespace analysis, structured contradiction diagnosis, figure-first review, and methods reverse-engineering.

#### Source B: K-Dense AI Claude Scientific Writer
- **Repository:** `https://github.com/K-Dense-AI/claude-scientific-writer`
- **License:** MIT License
- **Copyright:** (c) 2024-2026 K-Dense AI
- **Architecture Role:** Deterministic citation validation, multi-identifier deduplication, scholarly regex patterns, research packet assembly, manuscript audit trails, post-writing citation audits, claim-to-evidence matrix linting, and reproducible search manifests.

---

### 2. Required Architectural Audit Matrix (v8.6)
`SOURCE -> COMPONENT -> EXISTING EQUIVALENT -> GAP -> ACTION -> REASON`

| Source | Component | Existing Equivalent in Proposal-Nevisi | Gap Identified | Action Taken | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AIPOCH** | `literature-close-read` & `deep_reading_template.md` | `StructuredPaperReader` (18 fields) | Extracting 18 flat fields lacked explicit structural grouping into study identity, methods, results, interpretation, and provenance. | **ADAPT & EXTEND** | Structured into 5 canonical evidence sections (A-E) to guarantee technical fidelity and prevent LLM inference from contaminating quoted primary data. |
| **AIPOCH** | `result-figure-consistencycheck` | Narrative abstract extraction | Abstract conclusions frequently exaggerate effect sizes; narrative claims often overlook non-significant figure data points. | **ADAPT & PORT** | Implemented `extract_figure_table_evidence()` with `PRIMARY_DATA_VISUAL_REQUIRES_REVIEW` discrepancy flag. | Prioritizes primary visual data points over narrative claims when numerical mismatches occur. |
| **AIPOCH** | `methodology-extractor` | `study_design_type` string | Coarse design string did not answer what was done, with what comparator, at what dose, for what duration, and what was measured. | **ADAPT & GENERALIZE** | Added `reverse_engineer_methods()` generating domain-agnostic protocol breakdowns. | Enables cross-study comparability across diverse models (in vitro, in vivo, clinical, computational) without hardcoded oncology variables. |
| **K-Dense** | `skills/scientific-writing/scripts/audit_claims.py` & `lint_causal_claims.py` | `PaperToClaimVerifier` (6 drift types) | 6 drift types did not distinguish preclinical-to-clinical leap, population mismatch, dose mismatch, or secondary-to-primary source confusion. | **UPGRADE to v2.0** | Built formal 8-stage verification pipeline and 13-category issue detection (`CLAIM_VERIFICATION_ISSUES_V2`). | Establishes mathematical and semantic entailment from extracted finding to final claim status. |
| **K-Dense** | `skills/peer-review/scripts/audit_citations.py` | Final portfolio ceiling check | Did not audit proposal narrative text for unresolved citation placeholders (`[?]`), unused references in bibliography, or missing markers. | **ADAPT & IMPLEMENT** | Created `PostResearchCitationAuditor` auditing proposal markdown text vs reference portfolio. | Eliminates ghost citations, unreferenced claims, and orphaned bibliography items before release. |
| **AIPOCH** | `medical-topic-saturation-and-whitespace-checker` | `EvidenceBasedSaturationTracker` | Saturation could theoretically be declared purely from diminishing yields even if only a single database or single outcome was queried. | **UPGRADE** | Added Multi-Dimensional Incompleteness Guard (`SATURATION_INCOMPLETE`). | Prevents false saturation declarations when critical dimensions (database diversity, outcome diversity, negative evidence) remain unvisited. |
| **K-Dense** | `skills/literature-review/references/database_strategies.md` | Fixed 4-database query adapter | Lacked explicit rationale for why a given database was queried and which evidence types it can/cannot capture. | **ADAPT & ENHANCE** | Built `AdaptiveDatabaseSelector` with `DATABASE_SPECIALIZATION_REGISTRY`. | Dynamically adapts database portfolio (e.g. adding OpenAlex for computational/engineering domains) with full epistemic justification. |
| **AIPOCH** | `contradictory-findings-resolver` & Negative search | Linear query generator | Retrieval optimized for supporting studies without actively searching for null results or quantifying positive publication bias. | **ADAPT & BUILD** | Implemented `NegativeEvidenceScanner` and `POSITIVE_EVIDENCE_DOMINANCE` detector. | Actively recovers negative/inert findings to delineate boundary conditions and evaluate publication bias risk. |
| **Proposal-Nevisi Benchmark** | Custom Ground-Truth Architecture | Unit tests (software validity only) | Software unit tests pass without proving high literature recall on real-world topics. | **DESIGN & BUILD** | Created `ResearchRecallBenchmark` & `SearchMissAnalyzer` (13 failure modes). | Explicitly measures Recall, Precision, F1, Coverage against gold standards and diagnoses 'We missed this relevant paper because...'. |

---

### 3. Capability Extraction, Adaptation & Attribution Details

#### A. Research Recall Benchmark & Search Miss Taxonomy (Section 3 & 4)
- **Problem Solved:** Traditional search engines measure keyword hits rather than true literature recall.
- **Proposal-Nevisi Implementation:** `ResearchRecallBenchmark.evaluate_benchmark()` computes exact Recall, Precision, F1, and Gold-Standard Coverage against verified benchmark specifications. When relevant studies are missed, `SearchMissAnalyzer.diagnose_miss()` maps the failure to one of 13 standardized root causes (`DATE_FILTER_FAILURE`, `DATABASE_COVERAGE_FAILURE`, `DEDUPLICATION_ERROR`, `SCREENING_FALSE_NEGATIVE`, `CITATION_NETWORK_FAILURE`, `QUERY_FAMILY_FAILURE`, `MESH_MAPPING_FAILURE`, `SYNONYM_FAILURE`, `VOCABULARY_FAILURE`, etc.), answering: *"We missed this relevant paper because..."*.

#### B. Deep Paper Reading & Generic Evidence Sections (Section 5)
- **Problem Solved:** Title/abstract scanning leads to hallucination of findings and superficial literature reviews.
- **Proposal-Nevisi Implementation:** `StructuredPaperReader.read_paper()` organizes empirical evidence into 5 canonical sections:
  1. `study_identity`: Design, model/population, intervention, comparator, setting, sample size.
  2. `methods`: Experimental methodology, primary assay, dose/exposure, duration, controls.
  3. `results`: Primary endpoint, quantitative effect size, uncertainty/CI, p-value, adverse events, negative findings.
  4. `interpretation`: Authors' conclusions, limitations, alternative explanations, translational gap.
  5. `evidence_provenance`: Section location, table/figure reference, extraction confidence, directness status.

#### C. Figure-First / Table-First Evidence Recovery (Section 6)
- **Problem Solved:** Scientific abstracts frequently overstate claims or highlight positive secondary analyses while omitting non-significant primary data in figures.
- **Proposal-Nevisi Implementation:** `StructuredPaperReader.extract_figure_table_evidence()` extracts numerical data from figures/tables and flags `PRIMARY_DATA_VISUAL_REQUIRES_REVIEW` when visual data points contradict narrative text (e.g. abstract claims "potent suppression" but figure legend reveals "p > 0.05" or "< 10% change").

#### D. 8-Tier Evidence Hierarchy (Section 8)
- **Problem Solved:** Treating every paper equally or allowing citation counts to substitute for evidence quality.
- **Proposal-Nevisi Implementation:** `evaluate_evidence_hierarchy()` assigns findings to one of 8 confidence tiers (`DIRECT_HIGH_CONFIDENCE`, `DIRECT_MODERATE_CONFIDENCE`, `DIRECT_LOW_CONFIDENCE`, `INDIRECT_SUPPORT`, `MECHANISTIC_SUPPORT`, `CONTEXTUAL_SUPPORT`, `CONTRADICTORY`, `LIMITS_INTERPRETATION`) based on study design, risk of bias, quantitative precision, and directness.

#### E. Paper-to-Claim Verification 2.0 (Section 9)
- **Problem Solved:** Semantic drift where secondary citations gradually transform associative or preclinical findings into definitive clinical facts.
- **Proposal-Nevisi Implementation:** `PaperToClaimVerifier.verify_claim_v2()` executes the 8-stage verification pipeline:
  `CLAIM -> SOURCE PAPER -> SOURCE LOCATION -> EXTRACTED FINDING -> ENTAILMENT -> CONTEXT MATCH -> CAUSALITY CHECK -> FINAL CLAIM STATUS`
  Detects 13 specific issues including `PRECLINICAL_TO_CLINICAL_LEAP`, `MODEL_MISMATCH`, `ENDPOINT_MISMATCH`, `INTERVENTION_MISMATCH`, `DOSE_MISMATCH`, `TEMPORAL_MISMATCH`, `CORRELATION_TO_CAUSATION`, and `SELECTIVE_CITATION`.

#### F. Post-Research Citation Audit (Section 10)
- **Problem Solved:** Unresolved placeholders (`[?]`, `[citation needed]`) and unused references remaining in final submitted proposals.
- **Proposal-Nevisi Implementation:** `PostResearchCitationAuditor.audit_proposal_citations()` audits proposal text vs portfolio, verifying identifier resolution, detecting unused references (`UNUSED_REFERENCE_IN_PORTFOLIO`), and identifying missing citations.

---

### 5. Proposal-Nevisi v8.7 Evidence Grounding & Attribution Integrity Upgrade

#### A. Source Audit & Integration Matrix (v8.7)
`SOURCE -> COMPONENT -> EXISTING EQUIVALENT -> GAP -> ACTION -> REASON`

| Source | Component | Existing Equivalent in Proposal-Nevisi | Gap Identified | Action Taken | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SciFact (AllenAI / Wadden et al.)** | Claim verification dataset & rationale scorer | `PaperToClaimVerifier` | Prior claim verification provided binary pass/fail without standardized 5-tier verdicts and fine-grained sentence rationale mapping. | **ADAPT & FORMALIZE** | Implemented `ExactClaimEvidenceMapper` using SciFact-aligned verdicts (`SUPPORTED`, `PARTIALLY_SUPPORTED`, `NOT_SUPPORTED`, `CONTRADICTED`, `INSUFFICIENT_EVIDENCE`). | Guarantees semantic entailment between each proposal statement and source paper evidence text. |
| **K-Dense AI** | `lint_causal_claims.py` & `audit_claims.py` | Numeric extraction regex | Simple number regex failed to verify whether numbers ($IC_{50}$, doses, p-values) were directly reported, calculated, or hallucinated. | **BUILD** | Created `NumericProvenanceGate` (`NUMERIC_PROVENANCE_STATUSES`). | Rejects ungrounded numeric values from appearing in literature reviews; distinguishes explicit extraction from derived values. |
| **AIPOCH** | `methodology-extractor` & boundary linting | `study_design_type` string | In silico docking studies were sometimes conflated with in vitro wet-lab studies, and botanical extracts were confused with pure constituents. | **EXTEND & ENFORCE** | Built `ContextualBoundaryGate` across 11 mismatch categories (`CONTEXTUAL_BOUNDARY_MISMATCHES`). | Enforces strict epistemic walls: in silico $\neq$ wet lab, extract $\neq$ pure constituent, observational $\neq$ causal. |
| **W3C PROV-O / Scholarly Standards** | Provenance ontology & citation audit | Generic bibliography check | In-text citations `[X]` were checked for syntax but not semantically verified against the actual content of reference X. | **BUILD** | Added `CanonicalPaperEvidenceRecord` (16 fields, exact source location provenance) and `PostResearchCitationAuditor.audit_claim_citations()`. | Flags `CITATION_CLAIM_MISMATCH` if citation marker [X] is attached to claims unsupported by paper X. |
| **Proposal-Nevisi Core** | Fixed Literature Review Paragraph Template | Generic proposal synthesis | Boilerplate text generated identical structures ("گروه کنترل استاندارد") and suppressed null/negative findings. | **REPLACE** | Created `EvidenceDrivenParagraphBuilder`. | Produces variable-length, evidence-grounded paragraphs without filler boilerplate, surfacing negative results and formulation nuances. |

#### B. Architectural Additions in v8.7
1. **Canonical Paper Evidence Record (16 Fields):** Standardized schema capturing `study_id`, `authors`, `year`, `title`, `doi_pmid`, `study_design`, `model_system`, `formulation_entity`, `intervention`, `comparator`, `primary_endpoint`, `quantitative_findings`, `negative_or_null_findings`, `limitations`, `source_locations`, and `extraction_status`.
2. **Numeric Provenance Gate:** Strips non-quantitative tokens (citation markers, publication years, entity identifiers with hyphenated numbers) and verifies that any numeric claim in the proposal is grounded in the paper's quantitative results.
3. **Contextual Boundary Gate:** Prevents 11 specific boundary leaps:
   - `MODEL_MISMATCH`
   - `FORMULATION_MISMATCH`
   - `IN_SILICO_TO_EXPERIMENTAL_LEAP`
   - `PRECLINICAL_TO_CLINICAL_LEAP`
   - `CORRELATION_TO_CAUSATION`
   - `ENDPOINT_MISMATCH`
   - `DOSE_RANGE_MISMATCH`
   - `TEMPORAL_MISMATCH`
   - `NEGATIVE_FINDING_SUPPRESSION`
   - `SELECTIVE_EVIDENCE_CHERRY_PICKING`
   - `MULTI_SOURCE_CONFLATION`
4. **Evidence-Driven Paragraph Generator:** Formats literature review entries with explicit experimental conditions, specific comparator baselines, and honest statements of null findings.

---

### 6. Components Intentionally NOT Reused & Rationale

1. **Proprietary CLI Tools (`parallel-cli` in K-Dense):**
   - K-Dense relies on an external closed-source binary for parallelized web searches.
   - **Decision:** Omitted. Proposal-Nevisi uses standard-library Python multithreading and polite rate-limited REST adapters.

2. **Unstructured Prompt-Only Reviewers (AIPOCH):**
   - Certain AIPOCH skills use open-ended LLM prompts without schema validation.
   - **Decision:** Omitted. Proposal-Nevisi enforces deterministic schema validation with Draft-07 schemas and regex guards to prevent hallucinations.

3. **Domain-Specific Entity Dictionaries:**
   - Both repositories contain skills with hardcoded cancer or drug terms.
   - **Decision:** Omitted. Proposal-Nevisi enforces a strict anti-leakage invariant verified by 22 static analysis tests.


