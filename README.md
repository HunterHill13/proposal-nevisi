# Proposal-Nevisi 🔬📄
### Universal Evidence-Driven Medical Research, Adversarial Verification & Proposal Engine (v8.6)
### موتور جامع و تعمیم‌پذیر سنتز شواهد، راستی‌آزمایی خصمانه و نگارش پروپوزال‌های علوم پزشکی

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Unified Tests: 303/303 Passed](https://img.shields.io/badge/Unified%20Tests-303%2F303%20Passed-success.svg)](#unified-multi-tier-test-harness)
[![Mutation Testing: 100%](https://img.shields.io/badge/Mutation%20Score-100%25%20Killed-success.svg)](#unified-multi-tier-test-harness)
[![PRISMA 2020 Compliant](https://img.shields.io/badge/PRISMA-2020%20Compliant-orange.svg)](#prisma-2020-search-accounting)
[![Architecture: Topic-Agnostic](https://img.shields.io/badge/Architecture-Topic--Agnostic%20Core-blueviolet.svg)](#universal-architecture)

---

> **Language / زبان:** [English](#english) | [فارسی](#فارسی)

---

<a name="english"></a>
## English Documentation

**Proposal-Nevisi (v8.6)** is an autonomous, publication-grade academic research proposal drafting framework and **Topic-Agnostic Research-Grade Medical Literature & Proposal Engine**. Adapted from proven architectures in AIPOCH and K-Dense, v8.6 introduces an empirical Research Recall Benchmark with a 13-category Search Miss Diagnosis Taxonomy, Adaptive Database Specialization with negative evidence scanning, a 5-section Deep Paper Reading Architecture (Sections A-E), Figure-First/Table-First evidence recovery with discrepancy flags (`PRIMARY_DATA_VISUAL_REQUIRES_REVIEW`), Methods reverse-engineering, an 8-tier Evidence Hierarchy, Paper-to-Claim Verification 2.0 (8-stage pipeline, 13 issues), and Post-Research Citation Auditing. It operates seamlessly across diverse biomedical disciplines—including **Oncology**, **Cardiology**, **Infectious Diseases**, **Molecular Diagnostics**, **Epidemiology**, **Endocrinology**, **Nephrology**, **Regenerative Medicine / Biomaterials**, **Occupational Toxicology**, **Pediatric Pulmonology**, and **Basic Molecular / Cellular Science**.

> **Bifurcated Validation Architecture & Scientific Boundaries (v8.6):** Proposal-Nevisi strictly differentiates **Software Validation** (303 automated unit/adversarial/schema tests validating logic, zero hard-code leakage, and document compilation) from **Scientific Evidence Validation** (empirical grounding, biological incompatibility filtering, entity hierarchy gating, viral platform gating, and search gap auditing). All findings are explicitly qualified: separate monotherapies are never asserted as proof of combination synergy, and unstudied combinations are honestly reported as authentic empirical research gaps (`NO_DIRECT_STUDY_IDENTIFIED_IN_SEARCHED_SOURCES`). The overall operational status is truthfully reported as **RESEARCH-GRADE — SOFTWARE VALIDATED, LIVE RECALL PARTIALLY VALIDATED**.


### Core Architecture & Capabilities (v8.4)

1. **Adaptive Research Problem Modeler & Decomposition (`scripts/research_problem_model.py`, `scripts/generic_search_planner.py`):**
   - Automatically structures questions using domain-appropriate frameworks: **PICO** (interventions), **PECO** (environmental/occupational exposures), **Diagnostic** (index test vs. reference standard), **Prognostic** (risk stratification), or **Mechanistic** (biochemical signaling cascades).
   - Dynamically partitions dimensions into `applicable_dimensions` and `not_applicable_dimensions` (e.g. for single-agent, surgical, or epidemiological questions).

2. **12-Layer Dynamic Search Strategy & Provenance-Tracked Query Expansion (`scripts/scientific_search_adapter.py`, `scripts/generic_search_planner.py`):**
   - Federated search engine integrating PubMed, Europe PMC, Crossref, and OpenAlex.
   - Connected-component transitive identity graph deduplication across multiple persistent IDs (PMID, DOI, OpenAlex ID) and title similarity.
   - Query expansion with term provenance tracking (acronyms, hyphenation variants, base lemmas) and multi-metric search saturation curve calculation.
   - Truthful execution status: 8 standardized database statuses (`EXECUTED`, `UNAVAILABLE`, `PARTIALLY_QUERIED`, `NOT_APPLICABLE`, `NOT_SEARCHED`, `EMPTY_RETRIEVAL`, `ERROR`, `NOT_EXECUTED`).

3. **16-Category Generic PRISMA Exclusion Ontology (`scripts/core_policies.py`, `scripts/generic_reference_auditor.py`):**
   - 16 topic-agnostic exclusion codes (`OUT_OF_SCOPE`, `WRONG_POPULATION`, `WRONG_CONDITION`, `WRONG_INTERVENTION`, `WRONG_COMPARATOR`, `WRONG_MODEL`, `WRONG_OUTCOME`, `WRONG_STUDY_DESIGN`, `WRONG_SETTING`, `INSUFFICIENT_EVIDENCE`, `NOT_PRIMARY_RESEARCH`, `RETRACTED`, `DUPLICATE`, `OUTDATED`, `METHOD_ONLY`, `PERIPHERAL_EVIDENCE`).
   - Seamless dual-matching backwards compatibility with earlier domain-specific aliases.

4. **Universal Entity Hierarchy & Evidence Roles (`scripts/core_policies.py`, `scripts/generic_reference_auditor.py`):**
   - 13 universal entity types (`PARENT_ENTITY`, `DERIVATIVE`, `ANALOGUE`, `EXTRACT`, `METABOLITE`, `FORMULATION`, `RECOMBINANT_VARIANT`, `COMBINATION`, `ANALYTE_BIOMARKER`, `DEVICE_SURGICAL_TOOL`, `BEHAVIORAL_DIGITAL`, `NOT_APPLICABLE`, `UNKNOWN_ENTITY`).
   - 10 distinct evidence roles (`DIRECT_EVIDENCE`, `INDIRECT_EVIDENCE`, `MECHANISTIC_EVIDENCE`, `METHODOLOGICAL_EVIDENCE`, `EPIDEMIOLOGICAL_EVIDENCE`, `SAFETY_EVIDENCE`, `ANALOGOUS_EVIDENCE`, `LIMITING_EVIDENCE`, `CONTRADICTORY_EVIDENCE`, `CONTEXTUAL_EVIDENCE`) decoupled from evidence polarity.

5. **7-Point Structured Literature Synthesis Narrative (`scripts/generic_evidence_synthesis.py`):**
   - Generates publication-grade literature review narratives systematically covering:
     1. Current Knowledge Base
     2. Consistency of Evidence Across Studies
     3. Contradictions & Divergent Findings
     4. Biological Plausibility & Mechanistic Support
     5. Methodological & Model Limitations
     6. Genuine Research Gaps
     7. Explicit Proposal Value Proposition

6. **14-Category Generic Contradiction Root-Cause Taxonomy (`scripts/core_policies.py`, `scripts/generic_contradiction_engine.py`):**
   - Evaluates negative and divergent findings across 14 generic categories (`POPULATION`, `MODEL`, `INTERVENTION`, `FORMULATION`, `DOSE_EXPOSURE`, `DURATION`, `TIMING`, `COMPARATOR`, `ASSAY`, `ENDPOINT`, `STUDY_DESIGN`, `BIOLOGICAL_CONTEXT`, `STATISTICAL_POWER`, `MEASUREMENT_METHOD`).
   - Distinguishes `TRUE_CONTRADICTION` from `CONTEXTUAL_DISAGREEMENT` and enforces "No Evidence != Evidence of No Effect".

7. **Institutional 14-Section Word Proposal Output (`scripts/docx_builder.py`):**
   - Generates publication-grade Microsoft Word files (`.docx`) matching Iranian university standards.
   - Deep XML inspection tool verifying all 14 main sections, 14 Section 13 subsections, tables, and native Right-to-Left bidirectional XML (`<w:bidi/>`).
   - Strict ceiling of maximum 25 references with `NO_QUOTA_FILLING = True` and individual, detailed paragraphs per reference.

---

<a name="unified-multi-tier-test-harness"></a>
### Unified Multi-Tier Test Harness (`scripts/master_release_gate.py`)

The engine includes a master test harness verifying 303 total software assertions across 10 independent test suites and passing all 28 Master Release Gate criteria:
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

```bash
# Run the master production release gate
python scripts/master_release_gate.py
```

---

<a name="فارسی"></a>
## مستندات فارسی

مهارت **Proposal-Nevisi (نسخه v8.6)** یک پلتفرم جامع، تعاملی، مستقل از موضوع (Topic-Agnostic) و مبتنی بر شواهد برای تدوین پروپوزال‌های پژوهشی علوم پزشکی و زیست‌پزشکی است.

### ویژگی‌های بنیادین نسخه v8.6:
1. **استقلال کامل و قطعی از موضوع (Topic-Agnostic Core):** بازطراحی و ارتقای کامل بر مبنای الگوهای اثبات‌شده AIPOCH و K-Dense بدون هرگونه فرض پنهان در خصوص بیماری، دارو، رده سلولی یا مکانیسم.
2. **بنچ‌مارک تجربی ریکال و دقت (`ResearchRecallBenchmark`):** سنجش کمی میزان بازیابی مقالات کلیدی (Recall, Precision, F1, Coverage) و ارزیابی سهم مجزای پایگاه‌ها، پرس‌وجوها، مقالات هسته و تعقیب استنادی.
3. **تاکسونومی ۱۳ گانه علت‌یابی مقالات جا افتاده (`SearchMissAnalyzer`):** تشخیص دقیق چرایی عدم بازیابی مقالات کلیدی در ۱۳ رده مستقل (واژگان، پایگاه، بازه زمانی، نوع طراحی، فیلتر زبان و ...).
4. **انتخاب انطباقی پایگاه‌ها با ثبت نقاط کور (`AdaptiveDatabaseSelector`):** ثبت رسمی نقاط قوت و نقاط کور هر پایگاه (PubMed, Europe PMC, OpenAlex, Crossref) جهت تضمین تنوع منابع.
5. **اسکنر شواهد منفی و ارزیابی سوگیری انتشار (`NegativeEvidenceScanner`):** کشف خودکار سلطه شواهد مثبت (`POSITIVE_EVIDENCE_DOMINANCE`) و ملزم ساختن جستجوی شواهد منفی و پوچ.
6. **خوانش عمیق ۵ بخشی متون (`StructuredPaperReader` Sections A-E):** استخراج ساختارمند هویت مطالعه، متدولوژی، نتایج کلیدی، تفسیر بافتاری و تمامیت ره‌گیری شواهد.
7. **بازیابی شواهد شکل‌محور و جدول‌محور با پرچم مغایرت (`PRIMARY_DATA_VISUAL_REQUIRES_REVIEW`):** کشف مغایرت‌های آماری و تفسیری میان متن چکیده و داده‌های خام جداول و نمودارها.
8. **سلسله‌مراتب ۸ سطحی شواهد (`EVIDENCE_HIERARCHY_TIERS`):** رتبه‌بندی کیفی از شواهد مستقیم با قطعیت بالا تا شواهد محدودکننده تفسیر؛ بدون جایگزین کردن تعداد استناد به جای کیفیت متدولوژیک.
9. **راستی‌آزمایی انطباق مقاله با ادعا ۲.۰ (`PaperToClaimVerifier` v2.0):** خط لوله ۸ مرحله‌ای و کشف ۱۳ نوع عیب استنادی شامل انحراف عددی، ناهمخوانی مدل و ادعای علیت غیرمجاز.
10. **ممیزی ارجاعات پس از نگارش (`PostResearchCitationAuditor`):** کشف ارجاعات یتیم (Unresolved Placeholders)، منابع خوانده‌نشده در پروپوزال، و رفرنس‌های ثبت‌نشده در سبد شواهد.
11. **سنتز مقایسه‌ای مضمونی و حل ریشه‌ای تناقضات:** ساخت ماتریس مقایسه بین‌مطالعه‌ای و تبیین واگرایی نتایج بر اساس تفاوت‌های پارامتری (دوز، مدل، زمان) به جای رای‌گیری عددی ساده.
12. **سوئیت آزمون جامع ۳۰۳ تستی با قبولی ۱۰۰٪:** اجرای خودکار ۱۰ سوئیت آزمون، پاس شدن ۲۸ معیار رهاسازی، کشتن ۱۰/۱۰ جهش علمی با نمره ۱۰۰٪ و ممیزی عدم نشت در ۲۲ اسکریپت.

> **Note on Scientific Validation vs Software Verification:**
> Software verification tests verify the computational integrity, algorithmic boundaries, and validation logic of the software engines (303/303 passed). The operational readiness status is truthfully designated as **RESEARCH-GRADE — SOFTWARE VALIDATED, LIVE RECALL PARTIALLY VALIDATED**, clearly distinguished from external wet-lab experiments or live multi-center clinical trials.

---

## مجوز (License)
این پروژه تحت مجوز [MIT License](LICENSE) منتشر شده است.
