# Proposal-Nevisi 🔬📄
### Universal Evidence-Driven Medical Research, Adversarial Verification & Proposal Engine (v8.5)
### موتور جامع و تعمیم‌پذیر سنتز شواهد، راستی‌آزمایی خصمانه و نگارش پروپوزال‌های علوم پزشکی

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Unified Tests: 289/289 Passed](https://img.shields.io/badge/Unified%20Tests-289%2F289%20Passed-success.svg)](#unified-multi-tier-test-harness)
[![Mutation Testing: 100%](https://img.shields.io/badge/Mutation%20Score-100%25%20Killed-success.svg)](#unified-multi-tier-test-harness)
[![PRISMA 2020 Compliant](https://img.shields.io/badge/PRISMA-2020%20Compliant-orange.svg)](#prisma-2020-search-accounting)
[![Architecture: Topic-Agnostic](https://img.shields.io/badge/Architecture-Topic--Agnostic%20Core-blueviolet.svg)](#universal-architecture)

---

> **Language / زبان:** [English](#english) | [فارسی](#فارسی)

---

<a name="english"></a>
## English Documentation

**Proposal-Nevisi (v8.5)** is an autonomous, publication-grade academic research proposal drafting framework and **Topic-Agnostic Research-Grade Medical Literature & Proposal Engine**. Adapted from proven architectures in AIPOCH and K-Dense, v8.5 completely decouples the research and literature synthesis subsystems from any project-specific biological assumptions, entities, mechanisms, diseases, cell lines, or compounds. It operates seamlessly across diverse biomedical disciplines—including **Oncology**, **Cardiology**, **Infectious Diseases**, **Molecular Diagnostics**, **Epidemiology**, **Endocrinology**, **Nephrology**, **Regenerative Medicine / Biomaterials**, **Occupational Toxicology**, **Pediatric Pulmonology**, and **Basic Molecular / Cellular Science**.

> **Bifurcated Validation Architecture & Scientific Boundaries (v8.5):** Proposal-Nevisi strictly differentiates **Software Validation** (289 automated unit/adversarial/schema tests validating logic, zero hard-code leakage, and document compilation) from **Scientific Evidence Validation** (empirical grounding, biological incompatibility filtering, entity hierarchy gating, viral platform gating, and search gap auditing). All findings are explicitly qualified: separate monotherapies are never asserted as proof of combination synergy, and unstudied combinations are honestly reported as authentic empirical research gaps (`NO_DIRECT_STUDY_IDENTIFIED_IN_SEARCHED_SOURCES`).


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

مهارت **Proposal-Nevisi (نسخه v8.5)** یک پلتفرم جامع، تعاملی، مستقل از موضوع (Topic-Agnostic) و مبتنی بر شواهد برای تدوین پروپوزال‌های پژوهشی علوم پزشکی و زیست‌پزشکی است.

### ویژگی‌های بنیادین نسخه v8.5:
1. **استقلال کامل و قطعی از موضوع (Topic-Agnostic Core):** بازطراحی و ارتقای کامل بر مبنای الگوهای اثبات‌شده AIPOCH و K-Dense بدون هرگونه فرض پنهان در خصوص بیماری، دارو، رده سلولی یا مکانیسم.
2. **۱۶ خانواده پرس‌وجوی استاندارد و نگاشت اصطلاح‌نامه MeSH (`SEARCH_FAMILIES_ONTOLOGY`):** تلفیق جستجوی واژگان کنترل‌شده MeSH با واژگان آزاد عنوان/چکیده، همراه با مقایسه کمی بازده و پوشش اشتراکی.
3. **تعقیب استنادی چندجهته با ردیابی مسیر اکتشاف (`CitationChasingEngine`):** پیاده‌سازی زنجیره‌سازی استنادی پس‌رو (Backward)، پیش‌رو (Forward) و هم‌عرض (Lateral) با ثبت شفاف مسیر، عمق و خاستگاه کشف.
4. **موتور اکتشاف مقالات هسته در ۸ دسته استاندارد (`SeedPaperDiscoveryEngine`):** تعیین لنگرهای اکتشافی مستقل از سبد مراجع نهایی (عدم گنجاندن خودکار در پروپوزال بدون عبور از فیلتر غربالگری).
5. **پایش اشباع ۷ بُعدی شواهد و گارد اشباع کاذب (`EvidenceBasedSaturationTracker`):** ارزیابی روند کاهش بازده حاشیه‌ای در ابعاد رکورد، موجودیت، شواهد، تناقض، شبکه استنادی، پایگاه و واژگان توأم با مسدودسازی اعلام اشباع در خطاهای سیستمی.
6. **خوانش ساختاریافته ۴ تراکه متون با استخراج ۱۸ فیلد قطعی (`StructuredPaperReader`):** پوشش تراک‌های بالینی، بیوانفورماتیک، آزمایشگاهی و هیبرید با استخراج قطعی دوز، حجم نمونه، جهت اثر، نقطه پایانی و روش اندازه‌گیری.
7. **راستی‌آزمایی انطباق مقاله با ادعا و کشف ۶ نوع انحراف استنادی (`PaperToClaimVerifier`):** تشخیص دقیق ادعای فراتر از داده (Overstatement)، انحراف متنی (Citation Drift)، عدم انطباق بافتاری (Context Mismatch)، استناد گزینشی (Selective Citation) و تبدیل همبستگی به علیت (Correlation to Causation).
8. **تفکیک سه‌سطحی تبیین تناقضات علمی (`CONTRADICTION_EXPLANATION_LEVELS`):** دسته‌بندی تبیین‌ها به تجربیِ اثبات‌شده (Demonstrated)، مکانیسمی محتمل (Plausible) و عدم‌قطعیت تجربیِ حل‌نشده (Unresolved Uncertainty).
9. **شناسنامه بازتولیدپذیر اجرای پژوهش (`ResearchRunManifest`):** تولید خودکار مانیفست کامل اجرای پژوهش حاوی تمام پرس‌وجوها، معیارهای تنوع پایگاهی، منحنی اشباع و چک‌سام رمزنگاری‌شده SHA-256.
10. **سوئیت آزمون جامع ۲۸۹ تستی با قبولی ۱۰۰٪:** اجرای خودکار ۹ سوئیت آزمون و کشتن ۱۰/۱۰ جهش علمی با نمره جهش ۱۰۰٪ و ممیزی عدم نشت در تمام ۲۲ اسکریپت هسته.

> **Note on Scientific Validation vs Software Verification:**
> Software verification tests verify the computational integrity, algorithmic boundaries, and validation logic of the software engines. They do not constitute external live laboratory experimentation or real clinical trials.

---

## مجوز (License)
این پروژه تحت مجوز [MIT License](LICENSE) منتشر شده است.
