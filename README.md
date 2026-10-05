# Proposal-Nevisi 🔬📄
### Universal Evidence-Driven Medical Research, Adversarial Verification & Proposal Engine (v8.7)
### موتور جامع و تعمیم‌پذیر سنتز شواهد، راستی‌آزمایی خصمانه و نگارش پروپوزال‌های علوم پزشکی

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Unified Tests: 317/317 Passed](https://img.shields.io/badge/Unified%20Tests-317%2F317%20Passed-success.svg)](#unified-multi-tier-test-harness)
[![Mutation Testing: 100%](https://img.shields.io/badge/Mutation%20Score-100%25%20Killed-success.svg)](#unified-multi-tier-test-harness)
[![Master Release Gate: 34/34 Passed](https://img.shields.io/badge/Master%20Gate-34%2F34%20Passed-success.svg)](#master-release-gate-34-criteria)
[![PRISMA 2020 Compliant](https://img.shields.io/badge/PRISMA-2020%20Compliant-orange.svg)](#prisma-2020-search-accounting)
[![Architecture: Topic-Agnostic](https://img.shields.io/badge/Architecture-Topic--Agnostic%20Core-blueviolet.svg)](#universal-architecture)

---

> **Language / زبان:** [English](#english) | [فارسی](#فارسی)

---

<a name="english"></a>
## English Documentation

**Proposal-Nevisi (v8.7)** is an autonomous, publication-grade academic research proposal drafting framework and **Topic-Agnostic Research-Grade Medical Literature & Proposal Engine**. Adapted from proven architectures in AIPOCH (`aipoch/medical-research-skills`), K-Dense (`K-Dense-AI/claude-scientific-writer`), and the SciFact claim-evidence framework (AllenAI / Wadden et al.), v8.7 completely eliminates semantic evidence attribution errors, numeric hallucination, and contextual boundary leaps. It operates seamlessly across diverse biomedical disciplines—including **Oncology**, **Cardiology**, **Infectious Diseases**, **Molecular Diagnostics**, **Epidemiology**, **Endocrinology**, **Nephrology**, **Regenerative Medicine / Biomaterials**, **Occupational Toxicology**, **Pediatric Pulmonology**, and **Basic Molecular / Cellular Science**.

> **Bifurcated Validation Architecture & Scientific Boundaries (v8.7):** Proposal-Nevisi strictly differentiates **Software Validation** (317 automated unit/adversarial/schema tests validating logic, zero hard-code leakage across 22 scripts, and document compilation) from **Scientific Evidence Validation** (empirical grounding, biological incompatibility filtering, entity hierarchy gating, viral platform gating, and search gap auditing). All findings are explicitly qualified: separate monotherapies are never asserted as proof of combination synergy, and unstudied combinations are honestly reported as authentic empirical research gaps (`NO_DIRECT_STUDY_IDENTIFIED_IN_SEARCHED_SOURCES`). The overall operational status is truthfully reported as:  
> **`RESEARCH-GRADE — SOFTWARE VALIDATED, LIVE RECALL PARTIALLY VALIDATED`**.

---

### Core Architecture & Capabilities (v8.7)

1. **Evidence Grounding & Semantic Attribution Integrity Engine (`scripts/generic_reference_auditor.py`, `scripts/core_policies.py`):**
   - **Canonical Paper Evidence Record (`CanonicalPaperEvidenceRecord`):** Captures 16 standardized fields with exact source location provenance (`ABSTRACT`, `METHODS`, `RESULTS`, `DISCUSSION`, `TABLE`, `FIGURE`, `SUPPLEMENTARY`).
   - **Numeric Provenance Gate (`NumericProvenanceGate`):** Enforces strict provenance statuses (`DIRECTLY_REPORTED`, `CALCULATED_FROM_REPORTED_DATA`, `DERIVED`, `INFERRED`, `NOT_REPORTED`). Rejects ungrounded or invented numbers ($IC_{50}$, doses, concentrations, p-values, sample sizes) while correctly ignoring citation markers and publication years.
   - **Contextual Boundary Gate (`ContextualBoundaryGate`):** Detects and blocks 11 mismatch categories: `MODEL_MISMATCH`, `FORMULATION_MISMATCH`, `IN_SILICO_TO_EXPERIMENTAL_LEAP`, `PRECLINICAL_TO_CLINICAL_LEAP`, `CORRELATION_TO_CAUSATION`, `ENDPOINT_MISMATCH`, `DOSE_RANGE_MISMATCH`, `TEMPORAL_MISMATCH`, `NEGATIVE_FINDING_SUPPRESSION`, `SELECTIVE_EVIDENCE_CHERRY_PICKING`, and `MULTI_SOURCE_CONFLATION`.
   - **Exact Claim-to-Evidence Mapper (`ExactClaimEvidenceMapper`):** Implements a SciFact-aligned verification pipeline returning 5 standardized verdicts: `SUPPORTED`, `PARTIALLY_SUPPORTED`, `NOT_SUPPORTED`, `CONTRADICTED`, and `INSUFFICIENT_EVIDENCE`.
   - **Evidence-Driven Paragraph Builder (`EvidenceDrivenParagraphBuilder`):** Generates variable-length, evidence-grounded literature review paragraphs without filler boilerplate ("گروه کنترل استاندارد"), explicitly highlighting formulation caveats (extract vs pure constituent) and surfacing neutral/null findings.
   - **Strict Claim-to-Citation Binding (`audit_claim_citations`):** Verifies that each in-text citation marker `[X]` corresponds strictly to claims supported by paper X, flagging `CITATION_CLAIM_MISMATCH` if unsupported.

2. **Empirical Research Recall Benchmark & 13-Category Search Miss Diagnosis (`scripts/scientific_search_adapter.py`, `scripts/core_policies.py`):**
   - **Quantitative Retrieval Metrics:** Calculates Recall, Precision, F1-Score, and Domain Coverage against ground-truth portfolios with canonical identifier normalization (`doi:`, `pmid:`, URL stripping).
   - **Component Contribution Attribution:** Quantifies the distinct retrieval contribution of databases, query families, seed papers, and citation chasing.
   - **13-Category Miss Taxonomy (`SearchMissAnalyzer`):** Diagnoses why relevant papers were missed (`VOCABULARY_MISMATCH`, `DATABASE_COVERAGE_GAP`, `DATE_RANGE_RESTRICTION`, `STUDY_DESIGN_FILTER_MISMATCH`, `LANGUAGE_RESTRICTION`, `QUERY_SPECIFICITY_TOO_HIGH`, `SEARCH_FIELD_LIMITATION`, `RETRIEVAL_RANKING_CUTOFF`, `DEDUPLICATION_FALSE_COLLAPSE`, `SEED_DISCOVERY_BLINDSPOT`, `RELEVANCE_GATE_FALSE_REJECTION`, `PAYWALL_METADATA_DEFICIT`, `UNKNOWN_SEARCH_MISS`).

3. **Adaptive Database Selection & Negative Evidence Scanning (`scripts/scientific_search_adapter.py`, `scripts/core_policies.py`):**
   - **Database Specialization Registry:** Explicitly registers database rationale (`why_used`), core capabilities, and known blind spots for PubMed, Europe PMC, OpenAlex, and Crossref.
   - **Negative Evidence Scanner (`NegativeEvidenceScanner`):** Detects `POSITIVE_EVIDENCE_DOMINANCE`, assesses publication bias, and enforces active querying for null outcomes, toxicity thresholds, antagonism, and failures.

4. **5-Section Deep Paper Reading & Figure/Table-First Recovery (`scripts/generic_reference_auditor.py`, `scripts/core_policies.py`):**
   - **Sections A–E Structured Reading:**
     - **Section A:** Study Identity & Architecture (identifiers, design, setting, population/cell line).
     - **Section B:** Methodology Reverse-Engineering (step-by-step protocol, controls, concentrations, duration, assay methods).
     - **Section C:** Primary Empirical Results & Quantitative Values ($IC_{50}$, hazard ratios, $p$-values, effect sizes).
     - **Section D:** Contextual Interpretation, Boundary Conditions & Limitations.
     - **Section E:** Citation Entailment, Provenance Integrity & Audit Ledger.
   - **Figure-First / Table-First Review:** Recovers primary data from graphs and tables, flagging discrepancies between abstract prose and raw visual data via `PRIMARY_DATA_VISUAL_REQUIRES_REVIEW`.

5. **8-Tier Evidence Hierarchy & Claim Verification 2.0 (`scripts/generic_reference_auditor.py`, `scripts/core_policies.py`):**
   - **8 Evidence Tiers:** Stratifies evidence from `DIRECT_HIGH_CONFIDENCE` down to `LIMITS_INTERPRETATION`. Citation counts are strictly forbidden from substituting for methodological quality or direct relevance.
   - **Paper-to-Claim Verifier 2.0:** Formal 8-stage verification pipeline detecting 13 specific issues (`CLAIM_VERIFICATION_ISSUES_V2`), including numerical drift, biological model mismatch, overclaim of causality from correlation, and selective citation.

6. **Post-Research & Post-Writing Citation Audit (`scripts/generic_reference_auditor.py`):**
   - Audits draft text against the evidence portfolio to detect unresolved citation placeholders (`UNRESOLVED_PLACEHOLDERS`), unused portfolio references (`UNUSED_PORTFOLIO_REFERENCE`), and uncached/unverified citations.

7. **Thematic Comparative Synthesis & Parameter Root-Cause Analysis (`scripts/generic_evidence_synthesis.py`):**
   - Constructs cross-study comparison matrices that resolve conflicting findings through underlying parametric variations (dosage, cell lineage, timepoints, assay methods) rather than naive vote-counting.

8. **16 Query Families & MeSH Controlled Vocabulary Mapping (`scripts/scientific_search_adapter.py`):**
   - 16 generic query families covering direct intervention, component monotherapies, signaling pathways, toxicity, negative evidence, and methodological benchmarks.
   - Bridges MeSH terms with free-text title/abstract queries and logs keyword-to-MeSH translation yield.

9. **Multi-Directional Citation Chasing Engine (`scripts/scientific_search_adapter.py`):**
   - Executes Backward Chasing (reference lists), Forward Chasing (citing articles), and Lateral Chasing (related co-citations) with complete provenance tracking (source paper, direction, depth).

10. **Multi-Dimensional Saturation Tracker & False Saturation Guard (`scripts/scientific_search_adapter.py`):**
    - Monitors diminishing returns across 7 dimensions (records, entities, evidence, contradictions, citation network, databases, vocabulary).
    - Blocks premature saturation declarations caused by network errors or incomplete dimensions via `SATURATION_INCOMPLETE`.

11. **Institutional 14-Section Word Proposal Output (`scripts/docx_builder.py`):**
    - Builds publication-ready `.docx` proposals matching Iranian university standards.
    - Features Dubai Persian typography, native RTL OpenXML (`<w:bidi/>`), and dedicated, comprehensive paragraphs for each individual reference.
    - Enforces a strict hard ceiling of maximum 25 references (`MAX_FINAL_REFERENCES = 25`) with zero artificial quota filling (`NO_QUOTA_FILLING = True`).

---

<a name="master-release-gate-34-criteria"></a>
### Master Release Gate (34 Production Criteria)

The engine enforces 34 non-negotiable release criteria verified on every build:
1. `MAX_FINAL_REFERENCES == 25` (Hard Ceiling)
2. `NO_QUOTA_FILLING == True` (Zero Artificial Padding)
3. `GENERIC_EXCLUSION_ONTOLOGY` (16 Topic-Agnostic Categories)
4. Two-Stage Screening & Citation Integrity Engine
5. `SEARCH_DATABASE_STATUSES` (8 Standardized Statuses)
6. `RESEARCH_PIPELINE_STAGES` (7 Standard Phases)
7. `GENERIC_CONTRADICTION_ROOT_CAUSES` (14 Generic Root Causes)
8. `HIGH_VALUE_SCORING_WEIGHTS` (10 Dimensions Normalized)
9. `SELECTION_ORDER_PRIORITIES` (9 Strict Tiers)
10. Universal Entity Hierarchy (13 Types) & Evidence Roles (10 Roles)
11. Bounded Search Gap Policy ("Absence of Evidence != Evidence of Absence")
12. Anti-Hardcoding Static Leakage Audit (22/22 Scripts Zero Leakage)
13. Portfolio Audit with Decoupled Search Pool and Ceiling Enforcement
14. 7-Point Structured Literature Synthesis Narrative Engine
15. `SEARCH_FAMILIES_ONTOLOGY` (16 Query Families) & MeSH Mapper
16. Citation Chasing Engine (Backward, Forward, Lateral) with Provenance
17. Seed Paper Discovery Engine (8 Categories & Non-Automatic Inclusion)
18. Evidence-Based Saturation Tracker (7 Dimensions & False Saturation Guard)
19. Structured Paper Reader (4 Tracks & 18 Deterministic Fields)
20. Paper-to-Claim Verifier (6 Citation Drift Types & Entailment Verdicts)
21. Enhanced Triple-Check Deduplication & Identifier Canonicalization
22. Reproducible Research Run Manifest & SHA-256 Checksum
23. Research Recall Benchmark & Diagnostic Taxonomy (13 Failure Modes)
24. Deep Reading 5-Section Architecture & Figure-First Visual Review
25. 8-Tier Evidence Hierarchy & Confidence Evaluation
26. Paper-to-Claim Verification 2.0 (8-Stage Pipeline & 13 Issues)
27. Post-Research Citation Auditor (Placeholders & Unused References)
28. Adaptive Database Selector & Negative Evidence Scanner
29. Canonical Paper Evidence Record (16 Fields & Location Provenance)
30. Numeric Provenance Gate (Anti-Numeric Hallucination & Exact Extraction)
31. Contextual Boundary Gate (11 Boundary Mismatches & Leap Prevention)
32. Exact Claim-to-Evidence Mapper (SciFact-Aligned 5-Tier Claim Verdicts)
33. Evidence-Driven Paragraph Builder (Anti-Boilerplate & Null/Negative Surfacing)
34. Strict Claim-to-Citation Binding & Literature Review Gate

---

<a name="unified-multi-tier-test-harness"></a>
### Unified Multi-Tier Test Harness (`scripts/master_release_gate.py`)

The engine includes a master test harness verifying 317 total software assertions across 11 independent test suites:
- **Suite 1: Static Analysis Hard-Code Leakage Audit (`test_hard_code_leakage.py`):** Asserts 0 hard-coded biological entities across all 22 core generic scripts (22 tests - **PASS**).
- **Suite 2: Multi-Domain Generalization Suite (`test_generalization.py`):** Validates execution across 12 distinct biomedical fixtures (12 tests - **PASS**).
- **Suite 3: Adversarial Stress Scenarios & Negative Rejection Tests (`test_adversarial_scenarios.py`):** 114 stress tests evaluating swappable search backends, deduplication, saturation curves, relevance gates, 25-reference ceiling, 14-factor scoring, screening funnels, DOI conflicts, retracted papers, calendar cutoffs, leap years, causal overclaims, synergy fallacies (114 tests - **PASS**).
- **Suite 4: Tri-Tier Benchmark Audit (`self_audit_suite.py`):** 60 behavioral and scientific assertions on the benchmark proposal (60 tests - **PASS**).
- **Suite 5: Mutation Testing Layer (`test_mutations.py`):** 10 deliberate scientific defect mutations with 100% kill score (10 tests - **PASS**).
- **Suite 6: Property-Based Invariants & JSON Schemas (`test_property_and_schemas.py`):** 14 tests validating Invariants 1–8 and Draft-07 JSON Schemas (14 tests - **PASS**).
- **Suite 7: End-to-End Pipeline & Integration Scenarios (`test_e2e_integration.py`):** 24 tests validating full pipeline execution and adversarial failure/demotion scenarios (24 tests - **PASS**).
- **Suite 8: Cross-Topic Adversarial Test Suite (`test_cross_topic_adversarial.py`):** 11 tests verifying topic-agnosticism across Scenarios A through J (11 tests - **PASS**).
- **Suite 9: Advanced Research Engine Integration (`test_advanced_research_engine.py`):** 22 tests verifying multi-source federated search, citation chasing, and claim verification (22 tests - **PASS**).
- **Suite 10: Deep Reading & Recall Benchmark Suite (`test_v86_deep_reading_and_recall_benchmark.py`):** 14 tests verifying recall benchmarking, 13-category search miss taxonomy, 5-section deep reading, figure-first evidence recovery, methods reverse-engineering, 8-tier evidence hierarchy, paper-to-claim verifier 2.0, post-research citation auditing, and thematic comparative synthesis (14 tests - **PASS**).
- **Suite 11: Evidence Grounding & Semantic Attribution Integrity Suite (`test_v87_evidence_grounding_and_attribution.py`):** 14 tests validating Canonical Paper Evidence Records, numeric provenance, contextual boundary gates, SciFact claim-evidence mapping, anti-boilerplate paragraph generation, and claim-to-citation binding (14 tests - **PASS**).

```bash
# Run the master production release gate
python scripts/master_release_gate.py
```

---

<a name="فارسی"></a>
## مستندات فارسی

مهارت **Proposal-Nevisi (نسخه v8.7)** یک پلتفرم جامع، تعاملی، کاملاً مستقل از موضوع (Topic-Agnostic) و مبتنی بر شواهد برای تدوین پروپوزال‌های پژوهشی علوم پزشکی و زیست‌پزشکی در بالاترین تراز دانشگاهی است.

### ویژگی‌های بنیادین نسخه v8.7:

1. **موتور اصالت انتساب شواهد و نگاشت معنایی متون (Evidence Grounding & Semantic Attribution Integrity):**
   - **رکورد استاندارد ۱۶ فیلدی شواهد مقاله (`CanonicalPaperEvidenceRecord`):** استخراج بدون حدس و گمان هویت، طراحی، مدل، فرمولاسیون، مداخله، مقایسه‌گر، پیامد اولیه، مقادیر کمی، یافته‌های منفی و ردیابی مکان استخراج در مقاله (متن، جدول، شکل).
   - **گیت اصالت داده‌های کمی (`NumericProvenanceGate`):** پیشگیری قطعی از جعل مقادیر عددی ($IC_{50}$، دوز، درصد مهار، p-value) با تفکیک داده‌های استخراجی صریح از مقادیر مشتق و حذف خطاهای توکن‌های عددی غیرکمی (شماره استناد و سال انتشار).
   - **گیت مرزهای متنی در ۱۱ بعد (`ContextualBoundaryGate`):** مسدودسازی خطاهای جهش این‌سیلیکو به آزمایشگاهی، پیش‌بالینی به بالینی، نسبت دادن عصاره به ماده خالص، ادعای علیت در مطالعات همبستگی، و پنهان‌سازی نتایج منفی.
   - **نگاشت گزاره به شواهد منطبق بر استاندارد بین‌المللی SciFact (`ExactClaimEvidenceMapper`):** اعتبارسنجی گزاره‌ها در ۵ سطح استاندارد (`SUPPORTED`, `PARTIALLY_SUPPORTED`, `NOT_SUPPORTED`, `CONTRADICTED`, `INSUFFICIENT_EVIDENCE`).
   - **سازنده پاراگراف‌های متغیر بر پایه شواهد (`EvidenceDrivenParagraphBuilder`):** تولید بخش پیشینه پژوهش بدون کلیشه‌های تکراری (نظیر "گروه کنترل استاندارد") با اشاره شفاف به فرمولاسیون و نتایج پوچ یا منفی.
   - **ممیزی اتصال گزاره به ارجاع در متن (`audit_claim_citations`):** اطمینان از اینکه هیچ مارکر استنادی `[X]` در کنار ادعایی که توسط مقاله X پشتیبانی نمی‌شود قرار نگیرد.
2. **استقلال کامل و قطعی از موضوع (Topic-Agnostic Core):** بازطراحی و ارتقای کامل بر مبنای الگوهای اثبات‌شده AIPOCH، K-Dense و SciFact بدون هرگونه فرض پنهان در خصوص بیماری، دارو، رده سلولی یا مکانیسم.
3. **بنچ‌مارک تجربی ریکال و دقت (`ResearchRecallBenchmark`):** سنجش کمی میزان بازیابی مقالات کلیدی (Recall, Precision, F1, Coverage) با نرمال‌سازی شناسه‌های استنادی.
4. **تاکسونومی ۱۳ گانه علت‌یابی مقالات جا افتاده (`SearchMissAnalyzer`):** تشخیص دقیق چرایی عدم بازیابی مقالات کلیدی در ۱۳ رده مستقل.
5. **انتخاب انطباقی پایگاه‌ها با ثبت نقاط کور (`AdaptiveDatabaseSelector`):** ثبت رسمی نقاط قوت و نقاط کور هر پایگاه (PubMed, Europe PMC, OpenAlex, Crossref).
6. **اسکنر شواهد منفی و ارزیابی سوگیری انتشار (`NegativeEvidenceScanner`):** کشف خودکار سلطه شواهد مثبت (`POSITIVE_EVIDENCE_DOMINANCE`) و جستجوی شواهد منفی و نتایج پوچ.
7. **خوانش عمیق ۵ بخشی متون (`StructuredPaperReader` Sections A–E):** استخراج ساختارمند هویت مطالعه، متدولوژی، نتایج کلیدی، تفسیر بافتاری و تمامیت ره‌گیری شواهد.
8. **بازیابی شواهد شکل‌محور و جدول‌محور با پرچم مغایرت (`PRIMARY_DATA_VISUAL_REQUIRES_REVIEW`):** کشف مغایرت‌های آماری و تفسیری میان متن چکیده و داده‌های خام جداول و نمودارها.
9. **سلسله‌مراتب ۸ سطحی شواهد (`EVIDENCE_HIERARCHY_TIERS`):** رتبه‌بندی کیفی شواهد بدون جایگزین کردن تعداد استناد به جای کیفیت متدولوژیک.
10. **خروجی رسمی ۱۴ گانه در قالب فایل Word (`.docx`):** ساخت سند رسمی با فونت اختصاصی دبی فارسی، تگ‌های بومی RTL OpenXML، پاراگراف‌های تفصیلی اختصاصی برای هر رفرنس و اعمال سقف سخت ۲۵ رفرنس (`MAX_FINAL_REFERENCES = 25`) بدون پر کردن صوری رفرنس‌ها (`NO_QUOTA_FILLING = True`).
11. **سوئیت آزمون جامع ۳۱۷ تستی با قبولی ۱۰۰٪:** اجرای خودکار ۱۱ سوئیت آزمون، پاس شدن تمام ۳۴ معیار مستر گیت، کشتن ۱۰/۱۰ جهش علمی با نمره ۱۰۰٪ و ممیزی عدم نشت در ۲۲ اسکریپت.

> **Note on Scientific Validation vs Software Verification:**  
> Software verification tests verify the computational integrity, algorithmic boundaries, and validation logic of the software engines (317/317 passed). The operational readiness status is truthfully designated as **`RESEARCH-GRADE — SOFTWARE VALIDATED, LIVE RECALL PARTIALLY VALIDATED`**, clearly distinguished from external wet-lab experiments or live multi-center clinical trials.

---

## مجوز (License)
این پروژه تحت مجوز [MIT License](LICENSE) منتشر شده است.

