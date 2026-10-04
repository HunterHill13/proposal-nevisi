# Proposal-Nevisi 🔬📄
### Universal Evidence-Driven Medical Research, Adversarial Verification & Proposal Engine (v8.0)
### موتور جامع و تعمیم‌پذیر سنتز شواهد، راستی‌آزمایی خصمانه و نگارش پروپوزال‌های علوم پزشکی

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Test Harness: 124/124 Passed](https://img.shields.io/badge/Unified%20Tests-124%2F124%20Passed-success.svg)](#unified-multi-tier-test-harness)
[![PRISMA 2020 Compliant](https://img.shields.io/badge/PRISMA-2020%20Compliant-orange.svg)](#prisma-2020-search-accounting)
[![Architecture: Topic-Agnostic](https://img.shields.io/badge/Architecture-Topic--Agnostic%20Core-blueviolet.svg)](#universal-architecture)

---

> **Language / زبان:** [English](#english) | [فارسی](#فارسی)

---

<a name="english"></a>
## English Documentation

**Proposal-Nevisi (v8.0)** is an autonomous, publication-grade academic research proposal drafting framework and **General-Purpose Evidence-Driven Medical Research Engine**. Redesigned from the ground up to eliminate all hard-coded domain dependencies, v8.0 operates across diverse biomedical disciplines—including **Oncology**, **Cardiology**, **Infectious Diseases**, **Molecular Diagnostics**, **Epidemiology**, and **Basic Experimental Science**.

### Core Architecture & Capabilities (v8.0)

1. **Dynamic Research Problem Modeler (`scripts/research_problem_model.py`):**
   - Automatically structures questions using domain-appropriate frameworks: **PICO** (interventions), **PECO** (environmental/occupational exposures), **Diagnostic** (index test vs. reference standard), **Prognostic** (risk stratification), or **Mechanistic** (biochemical signaling cascades).
   - Generates controlled vocabulary, MeSH indexing, explicit boundary criteria, and question decomposition.

2. **12-Layer Dynamic Search Strategy & Saturation (`scripts/generic_search_planner.py`):**
   - Implements 12 comprehensive search layers (A through L) covering direct, component, mechanistic, model, translational, safety, null, contradiction, methodological, alternative explanations, confounders, and independent replications.
   - Forward/backward citation chaining, PRISMA 2020 logging, and automated search saturation & coverage scoring.

3. **Explicit Cross-Study Relationships Graph & Claim DAG (`scripts/generic_study_relationships.py`):**
   - Maps 22 distinct cross-study relationship types (`DIRECT_REPLICATION`, `CONCEPTUAL_REPLICATION`, `EXTENSION`, `TRANSLATIONAL_EXTENSION`, `SUPPORTS`, `CONTRADICTS`, `METHODOLOGICAL_INHERITANCE`, etc.) and builds acyclic Claim Dependency DAGs.

4. **Evidence-Based Research Gap Detector (`scripts/generic_gap_detector.py`):**
   - Systematically classifies research gaps across 15 universal taxonomy categories (`KNOWLEDGE_GAP`, `MECHANISTIC_GAP`, `METHODOLOGICAL_GAP`, `TRANSLATIONAL_GAP`, `POPULATION_GAP`, `COMBINATION_GAP`, etc.) with importance tiers.

5. **Study Family De-Duplication & Independent Streams (`scripts/generic_study_family_detector.py`):**
   - Automatically detects shared trial registrations (e.g. `NCTxxxx`), multi-center cohorts (e.g. `UK Biobank`, `NHANES`), and secondary subgroup publications to calculate independent evidence streams and prevent artificial evidence double-counting.

6. **Study-Design-Aware Comparability & Bias (`scripts/generic_comparability_engine.py`):**
   - Tailored comparability criteria for in vitro replication, animal SYRCLE standards, clinical RCT RoB2 allocation & blinding, and diagnostic QUADAS-2 standards.

7. **Extensible 15-Category Contradiction Engine (`scripts/generic_contradiction_engine.py`):**
   - Evaluates negative findings across 15 universal categories (`NULL_RESULT`, `ANTAGONISM`, `TOXICITY`, `RESISTANCE`, `MODEL_LIMITATION`, etc.).
   - Distinguishes `TRUE_CONTRADICTION` from `CONTEXTUAL_DISAGREEMENT` and enforces the epistemic principle: "No Evidence != Evidence of No Effect".

8. **Claim-Evidence Entailment & Anti-Overclaim Gate (`scripts/generic_claim_entailment_engine.py`):**
   - Audits 7-level claim entailment (`DIRECTLY_SUPPORTED` down to `CONTRADICTED`).
   - Flags causal overclaims (`causes`, `induces`) derived from observational designs.
   - Enforces the `NO_SYNERGY_FALLACY` gate (`SYNERGY_NOT_ESTABLISHED` unless direct combination assays exist).
   - Audits numerical transformations and cross-checks article section consistency.

9. **Dynamic Protocol Designer & 14-Section Structure Gate:**
   - Generates dynamic Variable Tables, Gantt Timelines, Statistical Feasibility audits, and Statistical Plans (`scripts/dynamic_protocol_designer.py`).
   - Validates institutional 14-section layout with subsections 13-1 to 13-14 (`scripts/proposal_structure_validator.py`).
   - Pre-flight 11-dimensional Quality Assurance gate (`scripts/multi_dimensional_qa_gate.py`).

10. **Institutional 14-Section Proposal Output (DOCX):**
    - Generates publication-grade Microsoft Word files (`.docx`) matching Iranian university standards.

    - Enforces an individual, detailed analytical paragraph per reference in the literature review.
    - Features Dubai Persian typography, complex script bolding (`<w:bCs/>`), and native Right-to-Left bidirectional XML (`<w:bidi/>`).

---

<a name="unified-multi-tier-test-harness"></a>
### Unified Multi-Tier Test Harness (`tests/run_all_tests.py`)

The engine includes a master test harness verifying 138 total assertions across 4 independent test suites:
- **Suite 1: Static Analysis Hard-Code Leakage Audit (`test_hard_code_leakage.py`):** Asserts 0 hard-coded biological entities across all core generic scripts and verifies semantic generalization (19 tests - **PASS**).
- **Suite 2: Multi-Domain Generalization Suite (`test_generalization.py`):** Validates execution across 9 distinct biomedical fixtures: Preclinical Oncology, Clinical Cardiology, Infectious Disease, Molecular Diagnostics, Epidemiological Cohort, Basic Molecular Biology, Preclinical Animal Pharmacology, Endocrinology Clinical RCT, and Nephrology Prognostic Biomarkers (9 tests - **PASS**).
- **Suite 3: Adversarial Stress Scenarios (`test_adversarial_scenarios.py`):** 50 stress tests evaluating fake citations, mismatched DOIs, retracted/corrected articles, publication status, pseudo-replication, publication bias (<10 studies gate), causal overclaims, translational leaps, ungrounded numbers, synergy fallacies, no-evidence fallacies, structural drift, missing metadata, question-conditional hierarchy, conflict matrix, alternative explanations, evidence completeness, PRISMA accounting, multi-layer graph, and sample size uncertainty (50 tests - **PASS**).
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
2. **استراتژی جستجوی ۱۲ لایه‌ای و اشباع شواهد (12-Layer Search):** جستجوی همزمان شواهد موافق، شواهد متناقض/منفی، زنجیره‌سازی استنادی و تفکیک پوشش جستجو از اشباع شواهد.
3. **ماتریس جامعیت شواهد و تحلیل مسیرهای مستقل شواهد:** بررسی کامل جریان‌های شواهد (مستقیم، مؤلفه‌ها، مکانیسم، سمیت، شواهد منفی، تکرار و کارآزمایی بالینی).
4. **سلسله‌مراتب شواهد وابسته به سؤال (Question-Conditional Evidence Hierarchy):** وزن‌دهی پویا به شواهد بر اساس نوع سؤال (درمانی، مکانیکی، تشخیصی، پیش‌آگهی).
5. **ماتریس تعارض شواهد و تحلیل توضیحات جایگزین:** تفکیک هوشمندانه تناقض واقعی از اختلاف ناشی از پارامترهای زمینه‌ای، همراه با ارزیابی سوگیری انتشار و مصنوعات سنجش.
6. **دروازه زبان علّی و ره‌گیری عددی:** جلوگیری از ادعای علیت بر پایه داده‌های همبستگی و ثبت دقیق خاستگاه ادعاها (`CLAIM_PROVENANCE_MAP`).
7. **طراحی پروتکل پویا و اعتبارسنجی ساختار ۱۴ گانه:** تولید پویای جدول متغیرها، گانت چارت زمان‌بندی، آزمون‌های آماری و ممیزی سخت‌گیرانه ساختار ۱۴ گانه و زیربخش‌های ۱۳-۱ تا ۱۳-۱۴.
8. **خروجی رسمی ۱۴ گانه ورد:** تدوین کامل ۱۴ بخش مصوب با فونت دبی، تگ‌های native RTL bidi XML و نگارش یک پاراگراف تفصیلی مجزا برای تک‌تک مراجع در مرور منابع.
9. **آزمون‌های اعتبارسنجی چهارگانه:** پاس شدن ۱۰۰٪ آزمون‌ها در سوئیت جامع ۱۳۸ تستی بدون ادعای ساختگی (138 / 138 PASS).

---

## مجوز (License)
این پروژه تحت مجوز [MIT License](LICENSE) منتشر شده است.
