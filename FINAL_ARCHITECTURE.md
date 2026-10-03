# FINAL ARCHITECTURE SPECIFICATION
## Proposal-Nevisi v8.0: Universal Evidence-Driven Medical Research & Proposal Engine

---

## 1. High-Level Architectural Pipeline

The `proposal-nevisi` system operates on an evidence-first, configuration-driven paradigm. No scientific text is composed until the complete multi-database search, bibliographic verification, study-design-aware comparability, contradiction analysis, claim entailment, and evidence synthesis have executed and validated without critical errors.

```
USER RESEARCH TOPIC & DOMAIN SPECIFICATION
                      │
                      ▼
         [ 1. RESEARCH PROBLEM MODEL ]
         - Framework Selection: PICO / PECO / Mechanistic / Diagnostic / Prognostic
         - Controlled Vocabulary & MeSH Extraction
         - Target Condition, Population, Interventions, Endpoints
                      │
                      ▼
          [ 2. DYNAMIC SEARCH PLAN ]
         - Dual-Path Strategy: SUPPORTING_SEARCH & CONTRADICTING_SEARCH
         - 8 Query Facets: Direct, Component, Combination, Mechanistic,
           Translational, Negative/Null, Safety/Limits, Methodological
         - Search Boundary & Saturation Criteria Definition
                      │
                      ▼
       [ 3. MULTI-DATABASE RETRIEVAL & PRISMA ]
         - PubMed / MEDLINE (E-Utilities API)
         - Europe PMC REST API
         - OpenAlex Scholarly Knowledgebase
         - Crossref DOI Registry
         - True Search Logging & PRISMA 2020 Flow Accounting
                      │
                      ▼
     [ 4. BIBLIOGRAPHIC & SOURCE VERIFICATION ]
         - Field-level resolution: DOI, PMID, Title, Authors, Year, Journal
         - Discrepancy flagging: EXACT, MINOR_VARIATION, UNVERIFIED, CONFLICT
         - Anti-hallucination barrier: zero fabricated citations
                      │
                      ▼
    [ 5. STUDY DESIGN & RISK OF BIAS PROFILING ]
         - Design Classification: In Vitro, In Vivo Animal, RCT, Observational, Diagnostic
         - Design-Aware RoB: Cochrane RoB2 (RCTs), SYRCLE (Animal), QUADAS-2 (Diagnostic),
           In Vitro Replication & Control Standards
         - Prohibition: NOT_REPORTED is never mapped to LOW_RISK
                      │
                      ▼
        [ 6. STUDY COMPARABILITY ANALYSIS ]
         - Study-Design-Aware Dimensional Matching
         - Confounder, Model, Dose, and Assay Divergence Identification
         - Extraction into Structured Study Evidence Records
                      │
                      ▼
       [ 7. DUAL-PATH CONTRADICTION ENGINE ]
         - Extensible 15+ Negative Evidence Taxonomy
         - True Contradiction vs Contextual Disagreement Resolution
         - Null Results, Antagonism, Off-Target Toxicity, and Failure Mapping
                      │
                      ▼
    [ 8. STUDY FAMILY & DE-DUPLICATION ENGINE ]
         - Prevention of Evidence Double-Counting
         - Shared Cohort, Multi-Center Registry, and Secondary Analysis Detection
         - Separation of Primary Evidence from Systematic Reviews
                      │
                      ▼
     [ 9. CLAIM-EVIDENCE ENTAILMENT ENGINE ]
         - Atomic Claim Decomposition
         - Passage-Level Entailment: DIRECTLY_SUPPORTED, PARTIALLY_SUPPORTED,
           INDIRECTLY_SUPPORTED, INFERRED, HYPOTHESIS_ONLY, UNSUPPORTED, CONTRADICTED
         - Causal vs Correlational Language Gate (Anti-Overclaim)
         - Anti-Numerical Hallucination Ledger
                      │
                      ▼
       [ 10. MULTI-DIMENSIONAL SYNTHESIS ]
         - Evidence-Weighted Synthesis (Strict Prohibition of Majority Voting)
         - 8-Dimensional Certainty: Directness, Consistency, Precision, Study Quality,
           Risk of Bias, Applicability, Evidence Volume, Contradiction Burden
         - Uncertainty Tracking: First-Class Explicit Status
                      │
                      ▼
   [ 11. 14-SECTION PROPOSAL GENERATOR (DOCX) ]
         - Strict Iranian Institutional Proposal Structure (Sections 1-14)
         - Individual Reference Paragraphs in Literature Review
         - Variables Table, Methodology Timeline, Detailed Problem Statement
         - Bidi RTL XML (<w:bidi/>, <w:rtlGutter/>), Dubai Persian Font, Complex Script Bold
                      │
                      ▼
       [ 12. INDEPENDENT SELF-AUDIT SUITE ]
         - Topic-Agnostic Core Engine Tests
         - Adversarial Scenario Suite (10 Stress Tests)
         - Multi-Domain Fixture Validation (Oncology, Cardiology, Antiviral, Diagnostic)
         - Dynamic Pass/Fail/Skipped Reporting (No Synthetic 100% Claims)
```

---

## 2. Core Functional Layers

### Layer 1: Research Problem Modeling (`scripts/research_problem_model.py`)
- Takes raw topic inputs and constructs an instance of `RESEARCH_PROBLEM_MODEL_SCHEMA.json`.
- Dynamically selects the scientific formulation:
  - **PICO:** Interventional clinical studies.
  - **PECO:** Environmental and occupational exposure studies.
  - **Diagnostic:** Index test vs. Reference standard in target condition.
  - **Mechanistic:** Target pathway, biochemical cascade, cellular phenotype.
  - **Experimental In Vitro / Animal:** Model system, vehicle, exposure schedule, primary endpoint.
- Produces canonical MeSH terms, controlled synonyms, and exclusion criteria.

### Layer 2: Dual-Path Search Planner (`scripts/generic_search_planner.py`)
- Employs an evidence-seeking rather than confirmation-seeking strategy.
- For every core hypothesis, systematically generates both:
  1. `SUPPORTING_SEARCH`: Queries interrogating efficacy, activation, enhancement, and therapeutic benefit.
  2. `CONTRADICTING_SEARCH`: Queries explicitly probing null effects, failure to replicate, resistance, cytotoxicity, antagonism, and sub-additive interactions.
- Constructs an 8-facet query matrix:
  - Facet A: Direct Evidence (exact question)
  - Facet B: Component Evidence (isolated interventions, conditions, and targets)
  - Facet C: Combination & Interaction Evidence (synergy, antagonism, CI metrics)
  - Facet D: Mechanistic Evidence (pathway phosphorylation, transcriptional regulation)
  - Facet E: Translational Evidence (cell -> animal -> clinical)
  - Facet F: Negative Evidence (null, failure, toxicity, resistance)
  - Facet G: Safety & Limitations (dose-limiting toxicities, off-target binding)
  - Facet H: Methodological Evidence (assay validity, confounding variables)

### Layer 3: Bibliographic & Study Design Auditor (`scripts/generic_reference_auditor.py`)
- Resolves each retrieved reference against Crossref, PubMed, and OpenAlex.
- Validates field-level bibliographic consistency (title similarity >= 0.85, matching author surnames, publication year, volume/issue).
- Classifies study designs into:
  - `IN_VITRO_EXPERIMENTAL`
  - `IN_VIVO_ANIMAL`
  - `RANDOMIZED_CONTROLLED_TRIAL`
  - `CONTROLLED_CLINICAL_STUDY`
  - `OBSERVATIONAL_COHORT_CASE_CONTROL`
  - `DIAGNOSTIC_ACCURACY_STUDY`
  - `SYSTEMATIC_REVIEW_META_ANALYSIS`
  - `METHODOLOGICAL_LANDMARK`
- Enforces time boundaries: Primary evidence defaults to `Publication Year >= CURRENT_YEAR - 6`. Older studies are admitted only when tagged with a legitimate `FOUNDATIONAL_JUSTIFICATION`.

### Layer 4: Study-Design-Aware Comparability & Contradiction Engine
- Replaces rigid single-format tables with design-aware schemas (`scripts/generic_comparability_engine.py` & `scripts/generic_contradiction_engine.py`).
- **Comparability:** Evaluates methodological compatibility based on the actual study design (e.g., cell passage and solvent purity for cell studies vs. randomization and blinding for clinical trials).
- **Contradiction Taxonomy (15+ Extensible Categories):**
  - `NULL_RESULT`, `NO_EFFECT`, `ANTAGONISM`, `SUBADDITIVITY`, `TOXICITY`, `OFF_TARGET_EFFECT`, `RESISTANCE`, `NON_RESPONSE`, `SAFETY_LIMITATION`, `DOSE_LIMITATION`, `TIME_LIMITATION`, `MODEL_LIMITATION`, `TRANSLATIONAL_FAILURE`, `METHODOLOGICAL_CONFLICT`, `CONTRADICTORY_RESULT`.
- Resolves whether discrepancies represent `TRUE_CONTRADICTION` (conflicting outcomes under identical conditions) or `CONTEXTUAL_DISAGREEMENT` (outcomes explained by differing doses, models, cell types, or exposure times).

### Layer 5: Evidence Ledger & Claim Entailment Engine (`scripts/generic_claim_entailment_engine.py`)
- Deconstructs syntheses into atomic claims.
- Traces every quantitative metric (concentrations, effect sizes, p-values, sample sizes) to a registered fact in `EVIDENCE_LEDGER.json`.
- Enforces causal language integrity:
  - Prohibits inferring causality (`causes`, `drives`, `induces`) from purely correlational observations (`associated with`, `correlated with`).
  - Classifies entailment status across 7 standardized levels.
  - Detects overclaim risks and enforces caveat qualification.

### Layer 6: Universal 14-Section Persian Proposal Output (`scripts/docx_builder.py`)
- Strictly renders the 14 standard sections demanded by Iranian medical universities and institutional review boards:
  1. موضوع پژوهش (عنوان فارسی و انگلیسی) - Research Title
  2. بیان مسئله - Statement of Problem (Extensive clinical, biological, and epidemiological background)
  3. مرور بر منابع - Literature Review (Individual, detailed paragraphs per reference; comprehensive synthesis)
  4. اهداف پژوهش (کلی، اختصاصی، کاربردی) - Objectives (General, Specific, Applied)
  5. فرضیات و سؤالات پژوهش - Hypotheses and Research Questions
  6. نوآوری و جنبه جدید طرح - Innovation & Evidence-Bounded Novelty
  7. روش اجرای پژوهش - Methodology (14 granular methodological sub-items)
  8. جدول متغیرها - Variables Specification Table
  9. ملاحظات اخلاقی و رضایت‌نامه - Ethical Considerations & Codes
  10. دستاوردهای پژوهش - Expected Research Deliverables
  11. محدودیت‌های پژوهش - Research Limitations & Mitigation Strategies
  12. جدول زمان‌بندی و گانت چارت - Timeline & Gantt Schedule
  13. هزینه‌ها و بودجه‌بندی - Budget & Resources Allocation
  14. فهرست منابع - References (Strict Arabic numbering, matching inline citations, full DOI/PMID links)
- Format Standards: Dubai Persian typography, complex script bolding (`<w:bCs/>`), native Right-to-Left bidirectional XML (`<w:bidi/>`), and clean typographic layouts.

---

## 3. Configuration-Driven Interface

Any medical research project is configured via `GENERIC_CONFIG_SCHEMA.json`:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ProposalNevisiProjectConfig",
  "type": "object",
  "required": ["project_id", "research_question", "domain", "study_framework"],
  "properties": {
    "project_id": { "type": "string" },
    "research_question": { "type": "string" },
    "domain": { 
      "type": "string",
      "enum": ["oncology", "cardiovascular", "infectious_disease", "immunology", "endocrinology", "neurology", "diagnostics", "basic_biomedical"]
    },
    "study_framework": {
      "type": "string",
      "enum": ["PICO", "PECO", "DIAGNOSTIC", "PROGNOSTIC", "MECHANISTIC", "EXPERIMENTAL_IN_VITRO", "EXPERIMENTAL_ANIMAL"]
    },
    "time_policy": {
      "type": "object",
      "properties": {
        "max_primary_evidence_age_years": { "type": "integer", "default": 6 },
        "allow_foundational_exceptions": { "type": "boolean", "default": true }
      }
    },
    "evidence_policy": {
      "type": "object",
      "properties": {
        "minimum_required_references": { "type": "integer", "default": 15 },
        "enforce_zero_padding": { "type": "boolean", "default": true },
        "require_opposing_evidence_search": { "type": "boolean", "default": true },
        "require_passage_level_entailment": { "type": "boolean", "default": true }
      }
    }
  }
}
```

---

## 4. Architectural Guarantees & Verification
1. **Zero Hard-Coding Leakage:** Core engine scripts contain zero biological constants or disease-specific assertions.
2. **Zero Numerical Hallucination:** All numeric values in proposals are grounded in audited evidence ledger records.
3. **No Synthetic Pass Claims:** Self-audit suites execute behavioral assertions and independently verify expected outcomes.
