# Proposal-Nevisi 🔬📄
### Universal Evidence-Driven Medical Research, Adversarial Verification & Proposal Engine (v8.1)
### موتور جامع و تعمیم‌پذیر سنتز شواهد، راستی‌آزمایی خصمانه و نگارش پروپوزال‌های علوم پزشکی

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Test Harness: 161/161 Passed](https://img.shields.io/badge/Unified%20Tests-161%2F161%20Passed-success.svg)](#unified-multi-tier-test-harness)
[![PRISMA 2020 Compliant](https://img.shields.io/badge/PRISMA-2020%20Compliant-orange.svg)](#prisma-2020-search-accounting)
[![Architecture: Topic-Agnostic](https://img.shields.io/badge/Architecture-Topic--Agnostic%20Core-blueviolet.svg)](#universal-architecture)

---

> **Language / زبان:** [English](#english) | [فارسی](#فارسی)

---

<a name="english"></a>
## English Documentation

**Proposal-Nevisi (v8.1)** is an autonomous, publication-grade academic research proposal drafting framework and **General-Purpose Evidence-Driven Medical Research Engine**. Redesigned from the ground up to eliminate all hard-coded domain dependencies, v8.1 operates across diverse biomedical disciplines—including **Oncology**, **Cardiology**, **Infectious Diseases**, **Molecular Diagnostics**, **Epidemiology**, **Endocrinology**, **Nephrology**, **Regenerative Medicine / Biomaterials**, **Occupational Toxicology**, **Pediatric Pulmonology**, and **Basic Molecular / Cellular Science**.

### Core Architecture & Capabilities (v8.1)

1. **Dynamic Research Problem Modeler (`scripts/research_problem_model.py`):**
   - Automatically structures questions using domain-appropriate frameworks: **PICO** (interventions), **PECO** (environmental/occupational exposures), **Diagnostic** (index test vs. reference standard), **Prognostic** (risk stratification), or **Mechanistic** (biochemical signaling cascades).
   - Generates controlled vocabulary, MeSH indexing, explicit boundary criteria, and question decomposition.

2. **12-Layer Dynamic Search Strategy & Decoupled Database Adapters (`scripts/generic_search_planner.py`):**
   - Decoupled API adapters for PubMed, Europe PMC, Crossref, and OpenAlex.
   - Record-level PRISMA 2020 deduplication across unique IDs (PMID, DOI, OpenAlex ID) rather than naive arithmetic summation.
   - Framework-specific required evidence streams (Interventional, PECO, Diagnostic, Prognostic, Animal, In Vitro).
   - Truthful execution status: dry-run searches explicitly return `NOT_EXECUTED` without fabricating database responses.

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
   - Audits 7-level claim entailment (`DIRECTLY_SUPPORTED` down to `CONTRADICTED`).
   - Prompt-injection resistance: sanitizes text against prompt manipulation and script injection payloads.
   - Flags causal overclaims (`causes`, `induces`) derived from observational designs.
   - Enforces the `NO_SYNERGY_FALLACY` gate (`SYNERGY_NOT_ESTABLISHED` unless direct combination assays exist).
   - Audits numerical transformations and cross-checks article section consistency.

9. **Dynamic Protocol Designer & Sample Size Parameter Audit (`scripts/dynamic_protocol_designer.py`):**
   - Granular parameter provenance tracking (`provided`, `literature-derived`, `pilot-derived`, `assumed`, `missing`).
   - Generates dynamic Variable Tables, Gantt Timelines, Statistical Feasibility audits, and Statistical Plans.
   - Validates institutional 14-section layout with subsections 13-1 to 13-14 and directed internal consistency graph (`scripts/proposal_structure_validator.py`).
   - Pre-flight 11-dimensional Quality Assurance gate (`scripts/multi_dimensional_qa_gate.py`).

10. **Institutional 14-Section Proposal Output & Real XML Inspection (`scripts/docx_builder.py`):**
    - Generates publication-grade Microsoft Word files (`.docx`) matching Iranian university standards.
    - Deep XML inspection tool (`DocxBuilder.inspect_docx_file`) verifying all 14 main sections, 14 Section 13 subsections, tables, and native Right-to-Left bidirectional XML (`<w:bidi/>`).
    - Enforces an individual, detailed analytical paragraph per reference in the literature review with Dubai Persian typography.

---

<a name="unified-multi-tier-test-harness"></a>
### Unified Multi-Tier Test Harness (`tests/run_all_tests.py`)

The engine includes a master test harness verifying 161 total assertions across 4 independent test suites:
- **Suite 1: Static Analysis Hard-Code Leakage Audit (`test_hard_code_leakage.py`):** Asserts 0 hard-coded biological entities across all core generic scripts and verifies semantic generalization (19 tests - **PASS**).
- **Suite 2: Multi-Domain Generalization Suite (`test_generalization.py`):** Validates execution across 12 distinct biomedical fixtures: Preclinical Oncology, Clinical Cardiology, Infectious Disease, Molecular Diagnostics, Epidemiological Cohort, Basic Molecular Biology, Preclinical Animal Pharmacology, Endocrinology Clinical RCT, Nephrology Prognostic Biomarkers, Regenerative Medicine Biomaterial Scaffolds, Occupational Toxicology PECO Cohorts, and Pediatric Asthma Prognostics (12 tests - **PASS**).
- **Suite 3: Adversarial Stress Scenarios & Negative Rejection Tests (`test_adversarial_scenarios.py`):** 70 stress tests evaluating fake citations, mismatched DOIs (IDENTITY_CONFLICT), retracted/corrected articles, publication status, exact 6-year calendar boundary parsing, leap-year safety, rejection of fake foundational exceptions, pseudo-replication, publication bias (<10 studies gate), causal overclaims, translational leaps, ungrounded numbers, synergy fallacies, no-evidence fallacies, structural drift, missing metadata, question-conditional hierarchy, conflict matrix, alternative explanations, evidence completeness, PRISMA record-level deduplication, decoupled database adapters, prompt injection sanitization, internal consistency directed graph, multi-pillar final scientific release gate verification (70 tests - **PASS**).
- **Suite 4: Tri-Tier Benchmark Audit (`self_audit_suite.py`):** 60 behavioral and scientific assertions on the benchmark proposal (60 tests - **PASS**).

```bash
# Run the complete test suite
python tests/run_all_tests.py
```

---

<a name="فارسی"></a>
## مستندات فارسی

مهارت **Proposal-Nevisi (نسخه v8.1)** یک پلتفرم جامع، تعاملی، مستقل از موضوع و مبتنی بر شواهد برای تدوین پروپوزال‌های پژوهشی علوم پزشکی و زیست‌پزشکی است.

### ویژگی‌های بنیادین نسخه v8.1:
1. **استقلال کامل از موضوع (Topic-Agnostic Core):** حذف تمام کلیدواژه‌ها و پیش‌فرض‌های ثابت از کدهای هسته و انتقال کامل تعاریف به مدل پویای مسئله پژوهش (`ResearchProblemModel`).
2. **استراتژی جستجوی ۱۲ لایه‌ای، آداپتورهای دیتابیس و حذف افزونگی مبتنی بر شناسه رکوردها (PRISMA Record-Level De-duplication):** جستجوی همزمان شواهد موافق، شواهد متناقض/منفی، زنجیره‌سازی استنادی و تفکیک پوشش جستجو از اشباع شواهد با آداپتورهای مجزا برای PubMed, Europe PMC, Crossref و OpenAlex بدون ادعای اجرای ساختگی.
3. **مرز زمانی ۶ ساله دقیق و رد برچسب‌های جعلی کلاسیک:** ارزیابی تقویمی دقیق (`CURRENT_DATE - 6 YEARS`)، پشتیبانی از سال کبیسه و رد سخت‌گیرانه مقالات فاقد استناد بالا که به دروغ عنوان کلاسیک گرفته‌اند.
4. **ماتریس جامعیت شواهد و جریان‌های وابسته به نوع سؤال:** تفکیک جریان‌های مورد نیاز بر اساس نوع سؤال (درمانی، تماس محیطی، تشخیصی، پیش‌آگهی، حیوانی و درون‌تنی).
5. **ماتریس تعارض شواهد و تحلیل توضیحات جایگزین:** تفکیک هوشمندانه تناقض واقعی از اختلاف ناشی از پارامترهای زمینه‌ای، همراه با ارزیابی سوگیری انتشار و مصنوعات سنجش.
6. **دروازه زبان علّی، خاستگاه ادعاها و پاک‌سازی پرامپت‌ها:** جلوگیری از ادعای علیت بر پایه داده‌های همبستگی، ثبت دقیق خاستگاه ادعاها (`CLAIM_PROVENANCE_MAP`) و مقاومت در برابر تزریق پرامپت.
7. **طراحی پروتکل پویا، رهگیری پارامترهای حجم نمونه و گراف یکپارچگی درونی:** رهگیری دقیق خاستگاه پارامترهای آماری (`provided`, `literature-derived`, `pilot-derived`, `assumed`, `missing`) و بررسی جهت‌دار اتصال عنوان، اهداف، متغیرها، طراحی و تحلیل.
8. **خروجی رسمی ۱۴ گانه ورد و ابزار بازرسی عمیق XML:** تدوین کامل ۱۴ بخش مصوب با فونت دبی، تگ‌های native RTL bidi XML و نگارش یک پاراگراف تفصیلی مجزا برای تک‌تک مراجع در مرور منابع همراه با بازرسی ساختاری فایل docx.
9. **آزمون‌های اعتبارسنجی چهارگانه:** پاس شدن ۱۰۰٪ آزمون‌ها در سوئیت جامع ۱۶۱ تستی بدون ادعای ساختگی (161 / 161 PASS).

---

## مجوز (License)
این پروژه تحت مجوز [MIT License](LICENSE) منتشر شده است.
