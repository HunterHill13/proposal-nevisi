# Proposal-Nevisi 🔬📄
### Universal Evidence-Driven Medical Research, Adversarial Verification & Proposal Engine (v8.4)
### موتور جامع و تعمیم‌پذیر سنتز شواهد، راستی‌آزمایی خصمانه و نگارش پروپوزال‌های علوم پزشکی

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Unified Tests: 267/267 Passed](https://img.shields.io/badge/Unified%20Tests-267%2F267%20Passed-success.svg)](#unified-multi-tier-test-harness)
[![Mutation Testing: 100%](https://img.shields.io/badge/Mutation%20Score-100%25%20Killed-success.svg)](#unified-multi-tier-test-harness)
[![PRISMA 2020 Compliant](https://img.shields.io/badge/PRISMA-2020%20Compliant-orange.svg)](#prisma-2020-search-accounting)
[![Architecture: Topic-Agnostic](https://img.shields.io/badge/Architecture-Topic--Agnostic%20Core-blueviolet.svg)](#universal-architecture)

---

> **Language / زبان:** [English](#english) | [فارسی](#فارسی)

---

<a name="english"></a>
## English Documentation

**Proposal-Nevisi (v8.4)** is an autonomous, publication-grade academic research proposal drafting framework and **Topic-Agnostic Research-Grade Medical Literature & Proposal Engine**. Adapted from proven architectures in AIPOCH and K-Dense, v8.4 completely decouples the research and literature synthesis subsystems from any project-specific biological assumptions, entities, mechanisms, diseases, cell lines, or compounds. It operates seamlessly across diverse biomedical disciplines—including **Oncology**, **Cardiology**, **Infectious Diseases**, **Molecular Diagnostics**, **Epidemiology**, **Endocrinology**, **Nephrology**, **Regenerative Medicine / Biomaterials**, **Occupational Toxicology**, **Pediatric Pulmonology**, and **Basic Molecular / Cellular Science**.

> **Bifurcated Validation Architecture & Scientific Boundaries (v8.4):** Proposal-Nevisi strictly differentiates **Software Validation** (267 automated unit/adversarial/schema tests validating logic, zero hard-code leakage, and document compilation) from **Scientific Evidence Validation** (empirical grounding, biological incompatibility filtering, entity hierarchy gating, viral platform gating, and search gap auditing). All findings are explicitly qualified: separate monotherapies are never asserted as proof of combination synergy, and unstudied combinations are honestly reported as authentic empirical research gaps (`NO_DIRECT_STUDY_IDENTIFIED_IN_SEARCHED_SOURCES`).


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

The engine includes a master test harness verifying 267 total software assertions across 8 independent test suites:
- **Suite 1: Static Analysis Hard-Code Leakage Audit (`test_hard_code_leakage.py`):** Asserts 0 hard-coded biological entities across all 22 core generic scripts (22 tests - **PASS**).
- **Suite 2: Multi-Domain Generalization Suite (`test_generalization.py`):** Validates execution across 12 distinct biomedical fixtures (12 tests - **PASS**).
- **Suite 3: Adversarial Stress Scenarios & Negative Rejection Tests (`test_adversarial_scenarios.py`):** 114 stress tests evaluating swappable search backends, deduplication, saturation curves, relevance gates, 25-reference ceiling, 14-factor scoring, screening funnels, DOI conflicts, retracted papers, calendar cutoffs, leap years, causal overclaims, synergy fallacies (114 tests - **PASS**).
- **Suite 4: Tri-Tier Benchmark Audit (`self_audit_suite.py`):** 60 behavioral and scientific assertions on the benchmark proposal (60 tests - **PASS**).
- **Suite 5: Mutation Testing Layer (`test_mutations.py`):** 10 deliberate scientific defect mutations with 100% kill score (10 tests - **PASS**).
- **Suite 6: Property-Based Invariants & JSON Schemas (`test_property_and_schemas.py`):** 14 tests validating Invariants 1–8 and Draft-07 JSON Schemas (14 tests - **PASS**).
- **Suite 7: End-to-End Pipeline & Integration Scenarios (`test_e2e_integration.py`):** 24 tests validating full pipeline execution and adversarial failure/demotion scenarios (24 tests - **PASS**).
- **Suite 8: Cross-Topic Adversarial Test Suite (`test_cross_topic_adversarial.py`):** 11 tests verifying topic-agnosticism across Scenarios A through J (11 tests - **PASS**).

```bash
# Run the master production release gate
python scripts/master_release_gate.py
```

---

<a name="فارسی"></a>
## مستندات فارسی

مهارت **Proposal-Nevisi (نسخه v8.4)** یک پلتفرم جامع، تعاملی، مستقل از موضوع (Topic-Agnostic) و مبتنی بر شواهد برای تدوین پروپوزال‌های پژوهشی علوم پزشکی و زیست‌پزشکی است.

### ویژگی‌های بنیادین نسخه v8.4:
1. **استقلال کامل و قطعی از موضوع (Topic-Agnostic Core):** بازطراحی کامل بر مبنای الگوهای اثبات‌شده AIPOCH و K-Dense بدون هرگونه فرض پنهان در خصوص بیماری، دارو، رده سلولی یا مکانیسم.
2. **تجزیه انطباقی مسئله و ابعاد نامرتبط:** پشتیبانی کامل از مسائل تک‌مداخله‌ای، جراحی، اپیدمیولوژیک و تشخیصی با برچسب‌گذاری صریح `NOT_APPLICABLE` بدون تحمیل ابعاد اجباری ترکیبی.
3. **تاکسونومی جامع ۱۶ گانه انصراف PRISMA (`GENERIC_EXCLUSION_ONTOLOGY`):** تعریف ۱۶ کد عمومی بدون سوگیری همراه با نگاشت سازگار به عقب با الگوهای پیشین.
4. **سلسله‌مراتب عمومی موجودیت‌ها و نقش‌های شواهد:** تفکیک ۱۳ موجودیت زیستی و ۱۰ نقش علمی شواهد به صورت کاملاً مستقل از قطبیت شواهد (`SUPPORTS`, `CONTRADICTS`, `LIMITS_INTERPRETATION`).
5. **سنتز ساختارمند ۷ مرحله‌ای ادبیات پژوهش:** تدوین خودکار روایت تحلیلی و مستند مرور متون منطبق بر شواهد واقعی و وضعیت‌های محصور شکاف جستجو.
6. **سوئیت آزمون جامع ۲۶۷ تستی با قبولی ۱۰۰٪:** اجرای خودکار ۸ سوئیت آزمون و کشتن ۱۰/۱۰ جهش علمی با نمره جهش ۱۰۰٪.

> **Note on Scientific Validation vs Software Verification:**
> Software verification tests verify the computational integrity, algorithmic boundaries, and validation logic of the software engines. They do not constitute external live laboratory experimentation or real clinical trials.

---

<a name="فارسی"></a>
## مستندات فارسی

مهارت **Proposal-Nevisi (نسخه v8.2)** یک پلتفرم جامع، تعاملی، مستقل از موضوع و مبتنی بر شواهد برای تدوین پروپوزال‌های پژوهشی علوم پزشکی و زیست‌پزشکی است.

### ویژگی‌های بنیادین نسخه v8.2:
1. **استقلال کامل از موضوع (Topic-Agnostic Core):** حذف تمام کلیدواژه‌ها و پیش‌فرض‌های ثابت از کدهای هسته و انتقال کامل تعاریف به مدل پویای مسئله پژوهش (`ResearchProblemModel`).
2. **گیت ۱۰ بعدی هم‌خوانی مفهومی و ۶ سطح رتبه‌بندی (10-Dimension Relevance Gate):** سنجش ۱۰ بعد زیستی و روش‌شناختی و تفکیک ۶ سطح رتبه‌بندی (`DIRECTLY_RELEVANT`, `HIGHLY_RELEVANT`, `INDIRECTLY_RELEVANT`, `METHOD_RELEVANT`, `BACKGROUND_ONLY`, `IRRELEVANT`) و ممانعت قطعی و بی‌قیدوشرط از ورود مقالات بی‌ارتباط به بافتار زیستی (نظیر انجماد اسپرم دام در انکولوژی یا پزشکی انسانی).
3. **تفکیک بدنه جستجو از مراجع نهایی و سقف سخت ۲۵ رفرنس:** جستجوی اولیه عمیق، چندپایگاهی و اشباع‌محور، توأم با اعمال سقف قطعی حداکثر ۲۵ رفرنس در پروپوزال نهایی با رتبه‌بندی ۱۴ عاملی، توزیع متوازن در ۵ محور علمی، و الزام ثبت توجیه سه‌بخشی (`FINAL_INCLUSION_REASON`، بخش پشتیبانی‌شده در پروپوزال و دلیل ضرورت) برای تک‌تک مراجع.
4. **مرور بر منابع تفصیلی بدون تیترهای مصنوعی:** نگارش یک پاراگراف تفصیلی و مستقل برای تک‌تک مراجع در بخش ۳ بدون هدرهای مصنوعی، همراه با سنتز نقادانه بین‌مطالعه‌ای و تحلیل شواهد متناقض.
5. **آداپتور جستجوی علمی چندپایگاهی و گراف تجمیع هویت (`ScientificSearchAdapter`):** پیاده‌سازی معماری آداپتور (Option B + C) بر پایه کتابخانه استاندارد پایتون برای PubMed, Europe PMC, Crossref و OpenAlex با گراف همبندی تجمیع هویت شناساگرهای چندگانه (DOI, PMID, OpenAlex ID)، پایش منحنی اشباع جستجو و ثبت وضعیت صادقانه `NOT_EXECUTED` و `EMPTY_RETRIEVAL`.
6. **دقت زمانی تقویمی و سد ضدتقلب استثناهای کلاسیک:** ارزیابی روز/ماه/سال تقویمی با پشتیبانی سال کبیسه و الزام اثبات استناد بالا ($\ge 100$) یا نقش متدولوژیک بنیادین برای مقالات قدیمی‌تر از پنجره زمانی مجاز (تعداد استناد به تنهایی برای دور زدن قانون زمانی کافی نیست).
7. **دفتر کل خاستگاه داده‌های کمی و اعتبارسنجی عبارات علّی:** جداسازی کامل اتصال استنادی، ردیابی سند منبع و دلالت علمی ادعا، همراه با بررسی دقیق مقادیر عددی، تبدیل واحدها و مهار ادعای علیت در مطالعات مشاهده‌ای.
8. **طراحی پروتکل پویا، سیاست داده‌های مفقوده و رهگیری پارامترهای حجم نمونه:** تضمین تمایز `0` و `False` از `MISSING` و اعلام وضعیت `SAMPLE_SIZE_REQUIRES_INPUT` در صورت غیبت پارامترهای حیاتی بدون مفروضات پنهان.
9. **خروجی رسمی ۱۴ گانه ورد و ابزار بازرسی عمیق XML:** تدوین کامل ۱۴ بخش مصوب با فونت دبی، تگ‌های native RTL bidi XML و بازرسی ساختاری فایل docx.
10. **سوئیت آزمون‌های هفت‌گانه ۲۱۸ تستی و لایه آزمون جهش (Mutation Testing):** پاس شدن ۱۰۰٪ آزمون‌ها در سوئیت جامع ۲۱۸ تستی با کشته شدن ۱۰/۱۰ جهش عمدی (امتیاز جهش ۱۰۰٪) و برقراری ناوردایی‌های کشف پویا و حسابداری آماری.

---

## مجوز (License)
این پروژه تحت مجوز [MIT License](LICENSE) منتشر شده است.
