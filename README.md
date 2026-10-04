# Proposal-Nevisi 🔬📄
### Universal Evidence-Driven Medical Research, Adversarial Verification & Proposal Engine (v8.2)
### موتور جامع و تعمیم‌پذیر سنتز شواهد، راستی‌آزمایی خصمانه و نگارش پروپوزال‌های علوم پزشکی

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Test Harness: 207/207 Passed](https://img.shields.io/badge/Unified%20Tests-207%2F207%20Passed-success.svg)](#unified-multi-tier-test-harness)
[![Mutation Testing: 100%](https://img.shields.io/badge/Mutation%20Score-100%25%20Killed-success.svg)](#unified-multi-tier-test-harness)
[![PRISMA 2020 Compliant](https://img.shields.io/badge/PRISMA-2020%20Compliant-orange.svg)](#prisma-2020-search-accounting)
[![Architecture: Topic-Agnostic](https://img.shields.io/badge/Architecture-Topic--Agnostic%20Core-blueviolet.svg)](#universal-architecture)

---

> **Language / زبان:** [English](#english) | [فارسی](#فارسی)

---

<a name="english"></a>
## English Documentation

**Proposal-Nevisi (v8.2)** is an autonomous, publication-grade academic research proposal drafting framework and **General-Purpose Evidence-Driven Medical Research Engine**. Redesigned from the ground up to eliminate all hard-coded domain dependencies, v8.2 operates across diverse biomedical disciplines—including **Oncology**, **Cardiology**, **Infectious Diseases**, **Molecular Diagnostics**, **Epidemiology**, **Endocrinology**, **Nephrology**, **Regenerative Medicine / Biomaterials**, **Occupational Toxicology**, **Pediatric Pulmonology**, and **Basic Molecular / Cellular Science**.

### Core Architecture & Capabilities (v8.2)

1. **Dynamic Research Problem Modeler (`scripts/research_problem_model.py`):**
   - Automatically structures questions using domain-appropriate frameworks: **PICO** (interventions), **PECO** (environmental/occupational exposures), **Diagnostic** (index test vs. reference standard), **Prognostic** (risk stratification), or **Mechanistic** (biochemical signaling cascades).
   - Generates controlled vocabulary, MeSH indexing, explicit boundary criteria, and question decomposition.

2. **12-Layer Dynamic Search Strategy & Decoupled Database Adapters (`scripts/generic_search_planner.py`):**
   - Decoupled API adapters for PubMed, Europe PMC, Crossref, and OpenAlex.
   - Connected-component transitive identity graph PRISMA deduplication across unique IDs (PMID, DOI, OpenAlex ID) rather than naive arithmetic summation.
   - Truthful execution status: dry-run/offline searches explicitly return `NOT_EXECUTED` without fabricating database responses; zero-result searches require `EMPTY_RETRIEVAL` state recording.

3. **Explicit Cross-Study Relationships Graph & Claim DAG (`scripts/generic_study_relationships.py`):**
   - Maps 22 distinct cross-study relationship types (`DIRECT_REPLICATION`, `CONCEPTUAL_REPLICATION`, `EXTENSION`, `TRANSLATIONAL_EXTENSION`, `SUPPORTS`, `CONTRADICTS`, `METHODOLOGICAL_INHERITANCE`, etc.) and builds acyclic Claim Dependency DAGs.

4. **Evidence-Based Research Gap Detector (`scripts/generic_gap_detector.py`):**
   - Systematically classifies research gaps across 18 universal taxonomy categories (`KNOWLEDGE_GAP`, `MECHANISTIC_GAP`, `METHODOLOGICAL_GAP`, `TRANSLATIONAL_GAP`, `POPULATION_GAP`, `COMBINATION_GAP`, etc.) with importance tiers.

5. **Study Family De-Duplication & Independent Streams (`scripts/generic_study_family_detector.py`):**
   - Automatically detects shared trial registrations (e.g. `NCTxxxx`), multi-center cohorts (e.g. `UK Biobank`, `NHANES`), and secondary subgroup publications to calculate independent evidence streams and prevent artificial evidence double-counting.

6. **Study-Design-Aware Comparability & Bias (`scripts/generic_comparability_engine.py`):**
   - Tailored comparability criteria for in vitro replication, animal SYRCLE standards, clinical RCT RoB2 allocation & blinding, and diagnostic QUADAS-2 standards.

7. **Extensible 15-Category Contradiction Engine (`scripts/generic_contradiction_engine.py`):**
   - Evaluates negative findings across 15 universal categories (`NULL_RESULT`, `ANTAGONISM`, `TOXICITY`, `RESISTANCE`, `MODEL_LIMITATION`, etc.).
   - Distinguishes `TRUE_CONTRADICTION` from `CONTEXTUAL_DISAGREEMENT` and enforces the epistemic principle: "No Evidence != Evidence of No Effect".

8. **Claim-Evidence Entailment, Sanitization & Anti-Overclaim Gate (`scripts/generic_claim_entailment_engine.py`):**
   - Separates in-text citation linkage, source document traceability, and scientific claim entailment.
   - Strict numerical provenance ledger auditing values, transformations, and measurement units (`WRONG_NUMERICAL_VALUE`, `WRONG_UNIT`).
   - Flexible citation parser handling ranges `[1-3]`, lists `[1,2,5]`, and author-year citations.
   - Prompt-injection resistance: sanitizes text against zero-width obfuscation, hidden HTML, fake system messages, base64 payloads, and hostile prompts.
   - Flags causal overclaims (`causes`, `induces`) derived from observational designs.
   - Enforces the `NO_SYNERGY_FALLACY` gate (`SYNERGY_NOT_ESTABLISHED` unless direct combination assays exist).

9. **Dynamic Protocol Designer & Sample Size Parameter Audit (`scripts/dynamic_protocol_designer.py`):**
   - Missing data policy: `0 != MISSING` and `False != MISSING`.
   - Sample size parameter provenance tracking (`provided`, `literature-derived`, `pilot-derived`, `assumed`, `missing`); returns `SAMPLE_SIZE_REQUIRES_INPUT` without silent assumptions when required parameters are absent.
   - Multi-layer statistical feasibility audit checking design compatibility, distribution assumptions, repeated measures, and censoring.

10. **Contextual Relevance Gate & 25-Reference Ceiling (`scripts/generic_reference_auditor.py`):**
    - Enforces a mandatory Contextual Relevance Gate evaluating direct, model, intervention, outcome, mechanistic, and methodological relevance to reject pure chemical/agent keyword matches in disparate biological contexts (e.g. veterinary livestock reproduction, agricultural crops).
    - Multi-factor scoring (14 criteria) prioritizing high-yield empirical evidence.
    - Decouples search corpus from proposal references: enforces a strict hard ceiling of **maximum 25 references** (15–25 range) balanced across 5 scientific axes.

11. **Institutional 14-Section Proposal Output & Real XML Inspection (`scripts/docx_builder.py`):**
    - Generates publication-grade Microsoft Word files (`.docx`) matching Iranian university standards.
    - Deep XML inspection tool (`DocxBuilder.inspect_docx_file`) verifying all 14 main sections, 14 Section 13 subsections, tables, and native Right-to-Left bidirectional XML (`<w:bidi/>`).
    - Enforces an individual, detailed analytical paragraph per reference in Section 3 without artificial axis grouping headers.

---

<a name="unified-multi-tier-test-harness"></a>
### Unified Multi-Tier Test Harness (`tests/run_all_tests.py`)

The engine includes a master test harness verifying 207 total software assertions across 7 independent test suites:
- **Suite 1: Static Analysis Hard-Code Leakage Audit (`test_hard_code_leakage.py`):** Asserts 0 hard-coded biological entities across all core generic scripts and verifies semantic generalization (19 tests - **PASS**).
- **Suite 2: Multi-Domain Generalization Suite (`test_generalization.py`):** Validates execution across 12 distinct biomedical fixtures (12 tests - **PASS**).
- **Suite 3: Adversarial Stress Scenarios & Negative Rejection Tests (`test_adversarial_scenarios.py`):** 76 stress tests evaluating contextual relevance gates, 25-reference ceiling, 14-factor scoring, fake citations, mismatched DOIs (`IDENTITY_CONFLICT`), retracted/corrected articles, publication status, exact calendar boundary parsing, leap-year safety, rejection of fake foundational exceptions, pseudo-replication, publication bias (<10 studies gate), causal overclaims, translational leaps, ungrounded numbers, synergy fallacies, no-evidence fallacies, structural drift, missing metadata, question-conditional hierarchy, conflict matrix, alternative explanations, evidence completeness, PRISMA record-level deduplication, decoupled database adapters, prompt injection sanitization, internal consistency directed graph, multi-pillar final scientific release gate verification (76 tests - **PASS**).
- **Suite 4: Tri-Tier Benchmark Audit (`self_audit_suite.py`):** 60 behavioral and scientific assertions on the benchmark proposal (60 tests - **PASS**).
- **Suite 5: Mutation Testing Layer (`test_mutations.py`):** 10 deliberate scientific defect mutations evaluating whether the auditor catches corrupted temporal cutoffs, retracted articles, mismatched DOIs, unsupported assertions, observational causal overclaims, duplicated records, assumed sample sizes, prompt injections, and missing citations (10 tests - **PASS**, 100% Mutation Score).
- **Suite 6: Property-Based Invariants & JSON Schemas (`test_property_and_schemas.py`):** 14 tests validating Invariants 1–8 (reordering stability, duplicate invariance, causal gates, unit changes), Draft-07 JSON Schema validation against SEARCH_PROVENANCE, REFERENCE_RECORD, and CLAIM_PROVENANCE, and randomized xenobiology synthetic domain benchmark (14 tests - **PASS**).
- **Suite 7: End-to-End Pipeline & 15 Negative Adversarial Scenarios (`test_e2e_integration.py`):** 16 tests validating positive full pipeline execution and 15 adversarial negative failure/demotion scenarios (16 tests - **PASS**).

```bash
# Run the complete test suite
python tests/run_all_tests.py

# Run the master production release gate
python scripts/master_release_gate.py
```

> **Note on Scientific Validation vs Software Verification:**
> Software verification tests verify the computational integrity, algorithmic boundaries, and validation logic of the software engines. They do not constitute external live laboratory experimentation or real clinical trials.

---

<a name="فارسی"></a>
## مستندات فارسی

مهارت **Proposal-Nevisi (نسخه v8.2)** یک پلتفرم جامع، تعاملی، مستقل از موضوع و مبتنی بر شواهد برای تدوین پروپوزال‌های پژوهشی علوم پزشکی و زیست‌پزشکی است.

### ویژگی‌های بنیادین نسخه v8.2:
1. **استقلال کامل از موضوع (Topic-Agnostic Core):** حذف تمام کلیدواژه‌ها و پیش‌فرض‌های ثابت از کدهای هسته و انتقال کامل تعاریف به مدل پویای مسئله پژوهش (`ResearchProblemModel`).
2. **گیت الزامی هم‌خوانی مفهومی و زیستی (Contextual Relevance Gate):** ممانعت قطعی از ورود مقالات بی‌ارتباط به بافتار زیستی (نظیر انجماد اسپرم دام در انکولوژی یا پزشکی انسانی) با ارزیابی ابعاد هشت‌گانه هم‌خوانی.
3. **تفکیک بدنه جستجو از مراجع نهایی و سقف سخت ۲۵ رفرنس:** جستجوی اولیه عمیق، چندپایگاهی و اشباع‌محور، توأم با اعمال سقف قطعی حداکثر ۲۵ رفرنس در پروپوزال نهایی با رتبه‌بندی ۱۴ عاملی و توزیع متوازن در ۵ محور علمی.
4. **مرور بر منابع تفصیلی بدون تیترهای مصنوعی:** نگارش یک پاراگراف تفصیلی و مستقل برای تک‌تک مراجع در بخش ۳ بدون هدرهای مصنوعی، همراه با سنتز نقادانه بین‌مطالعه‌ای و تحلیل شواهد متناقض.
5. **استراتژی جستجوی ۱۲ لایه‌ای، آداپتورهای چندپایگاهی و گراف تجمیع هویت در PRISMA:** اتصال چندپایگاهی برای PubMed, Europe PMC, Crossref و OpenAlex با گراف همبندی تجمیع هویت رکوردهای تکراری و ثبت وضعیت صادقانه `NOT_EXECUTED` و `EMPTY_RETRIEVAL`.
6. **دقت زمانی تقویمی و سد ضدتقلب استثناهای کلاسیک:** ارزیابی روز/ماه/سال تقویمی با پشتیبانی سال کبیسه و الزام اثبات استناد بالا ($\ge 100$) یا نقش متدولوژیک بنیادین برای مقالات قدیمی‌تر از پنجره زمانی مجاز (تعداد استناد به تنهایی برای دور زدن قانون زمانی کافی نیست).
7. **دفتر کل خاستگاه داده‌های کمی و اعتبارسنجی عبارات علّی:** جداسازی کامل اتصال استنادی، ردیابی سند منبع و دلالت علمی ادعا، همراه با بررسی دقیق مقادیر عددی، تبدیل واحدها و مهار ادعای علیت در مطالعات مشاهده‌ای.
8. **طراحی پروتکل پویا، سیاست داده‌های مفقوده و رهگیری پارامترهای حجم نمونه:** تضمین تمایز `0` و `False` از `MISSING` و اعلام وضعیت `SAMPLE_SIZE_REQUIRES_INPUT` در صورت غیبت پارامترهای حیاتی بدون مفروضات پنهان.
9. **خروجی رسمی ۱۴ گانه ورد و ابزار بازرسی عمیق XML:** تدوین کامل ۱۴ بخش مصوب با فونت دبی، تگ‌های native RTL bidi XML و بازرسی ساختاری فایل docx.
10. **سوئیت آزمون‌های هفت‌گانه ۲۰۷ تستی و لایه آزمون جهش (Mutation Testing):** پاس شدن ۱۰۰٪ آزمون‌ها در سوئیت جامع ۲۰۷ تستی با کشته شدن ۱۰/۱۰ جهش عمدی (امتیاز جهش ۱۰۰٪) و برقراری ناوردایی‌های کشف پویا و حسابداری آماری.

---

## مجوز (License)
این پروژه تحت مجوز [MIT License](LICENSE) منتشر شده است.
