# Proposal-Nevisi 🔬📄
### Universal Evidence-Driven Medical Research, Adversarial Verification & Proposal Engine (v8.0)
### موتور جامع و تعمیم‌پذیر سنتز شواهد، راستی‌آزمایی خصمانه و نگارش پروپوزال‌های علوم پزشکی

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Test Harness: 77/77 Passed](https://img.shields.io/badge/Unified%20Tests-77%2F77%20Passed-success.svg)](#unified-multi-tier-test-harness)
[![PRISMA 2020 Compliant](https://img.shields.io/badge/PRISMA-2020%20Compliant-orange.svg)](#prisma-2020-search-accounting)
[![Architecture: Topic-Agnostic](https://img.shields.io/badge/Architecture-Topic--Agnostic%20Core-blueviolet.svg)](#universal-architecture)

---

> **Language / زبان:** [English](#english) | [فارسی](#فارسی)

---

<a name="english"></a>
## English Documentation

**Proposal-Nevisi (v8.0)** is an autonomous, publication-grade academic research proposal drafting framework and **General-Purpose Evidence-Driven Medical Research Engine**. Redesigned from the ground up to eliminate all hard-coded domain dependencies, v8.0 operates across diverse biomedical disciplines—including **Oncology**, **Cardiology**, **Infectious Diseases**, **Molecular Diagnostics**, and **Basic Experimental Science**.

### Core Architecture & Capabilities (v8.0)

1. **Dynamic Research Problem Modeler (`scripts/research_problem_model.py`):**
   - Automatically structures questions using domain-appropriate frameworks: **PICO** (interventions), **PECO** (environmental/occupational exposures), **Diagnostic** (index test vs. reference standard), **Prognostic** (risk stratification), or **Mechanistic** (biochemical signaling cascades).
   - Generates controlled vocabulary, MeSH indexing, and explicit boundary criteria.

2. **Dual-Path 8-Facet Search Planner (`scripts/generic_search_planner.py`):**
   - Replaces confirmation-seeking bias with dual-path retrieval: concurrent execution of `SUPPORTING_SEARCH` and `CONTRADICTING_SEARCH`.
   - Organizes queries into 8 systematic facets: Direct Evidence, Component Evidence, Combination/Interaction, Mechanistic, Translational, Negative/Null Evidence, Safety/Limitations, and Methodological Quality.

3. **Study Family De-Duplication (`scripts/generic_study_family_detector.py`):**
   - Automatically detects shared trial registrations (e.g. `NCTxxxx`), multi-center cohorts (e.g. `UK Biobank`, `NHANES`), and secondary subgroup publications to prevent artificial evidence double-counting.

4. **Study-Design-Aware Comparability & Bias (`scripts/generic_comparability_engine.py`):**
   - Replaces rigid single-format tables with dynamic comparability criteria tailored to the study design (in vitro replication & vehicle limits, animal randomization & housing, clinical RCT allocation & blinding, diagnostic QUADAS-2 standards).

5. **Extensible 15-Category Contradiction Engine (`scripts/generic_contradiction_engine.py`):**
   - Evaluates negative findings across 15 universal categories (`NULL_RESULT`, `ANTAGONISM`, `TOXICITY`, `RESISTANCE`, `MODEL_LIMITATION`, etc.).
   - Distinguishes `TRUE_CONTRADICTION` (conflicts under identical experimental conditions) from `CONTEXTUAL_DISAGREEMENT` (differences explained by dose, vehicle, or genetic background).

6. **Claim-Evidence Entailment & Causal Gate (`scripts/generic_claim_entailment_engine.py`):**
   - Audits 7-level claim entailment (`DIRECTLY_SUPPORTED` down to `CONTRADICTED`).
   - Automatically flags causal overclaims (`causes`, `induces`) derived from observational or correlational designs.
   - Asserts numerical traceability against `EVIDENCE_LEDGER.json` to eliminate numerical hallucination.

7. **Multi-Dimensional Certainty Synthesis (`scripts/generic_evidence_synthesis.py`):**
   - Evaluates certainty across 8 distinct dimensions (Directness, Consistency, Precision, Study Quality, Risk of Bias, Applicability, Evidence Volume, and Contradiction Burden).
   - Strictly prohibits simple majority vote-counting.

8. **Institutional 14-Section Proposal Output (DOCX):**
   - Generates production-grade Microsoft Word files (`.docx`) matching Iranian university standards.
   - Enforces an individual, detailed analytical paragraph per reference in the literature review.
   - Features Dubai Persian typography, complex script bolding (`<w:bCs/>`), and native Right-to-Left bidirectional XML (`<w:bidi/>`).

---

<a name="unified-multi-tier-test-harness"></a>
### Unified Multi-Tier Test Harness (`tests/run_all_tests.py`)

The engine includes a master test harness verifying 77 total assertions across 4 independent test suites:
- **Suite 1: Static Analysis Hard-Code Leakage Audit (`test_hard_code_leakage.py`):** Asserts 0 hard-coded biological entities in core generic scripts (**PASS**).
- **Suite 2: Multi-Domain Generalization Suite (`test_generalization.py`):** Validates execution across 4 distinct biomedical fixtures: Preclinical Oncology, Clinical Cardiology (SGLT2 in HFpEF), Infectious Disease (Paxlovid resistance in COVID-19), and Molecular Diagnostics (ctDNA liquid biopsy) (**PASS**).
- **Suite 3: Adversarial Stress Scenarios (`test_adversarial_scenarios.py`):** 12 stress tests evaluating fake citations, mismatched DOIs, causal overclaims, ungrounded numbers, and missing metadata (**PASS**).
- **Suite 4: Tri-Tier Benchmark Audit (`self_audit_suite.py`):** 60 behavioral and scientific assertions on the benchmark proposal (**PASS**).

```bash
# Run the complete test suite
python tests/run_all_tests.py
```

---

<a name="فارسی"></a>
## مستندات فارسی

مهارت **Proposal-Nevisi (نسخه v8.0)** یک پلتفرم جامع، تعاملی، مستقل از موضوع و مبتنی بر شواهد برای تدوین پروپوزال‌های پژوهشی علوم پزشکی و زیست‌پزشکی است.

### ویژگی‌های بنیادین نسخه v8.0:
1. **استقلال کامل از موضوع (Topic-Agnostic Core):** حذف تمام کلیدواژه‌ها و پیش‌فرض‌های ثابت از کدهای هسته و انتقال کامل تعاریف به مدل پویای مسئله پژوهش (`ResearchProblemModel`).
2. **جستجوی دومسیره شواهد (Dual-Path Search):** جستجوی همزمان شواهد موافق و شواهد متناقض/منفی برای پرهیز از سوگیری تأییدطلبانه.
3. **همسنجی متناسب با طراحی مطالعه:** ارزیابی همسنجی و سوگیری مطالعات بر پایه متدولوژی واقعی آن‌ها (سلولی، حیوانی، کارآزمایی بالینی و دقت تشخیصی).
4. **تاکسونومی ۱۵ گانه تناقضات:** تفکیک هوشمندانه تناقض واقعی از اختلاف ناشی از دوز، حلال یا رده سلولی.
5. **دروازه زبان علّی و ره‌گیری عددی:** جلوگیری از ادعای علیت بر پایه داده‌های همبستگی و تضمین ره‌گیری تمام اعداد در دفتر شواهد (`EVIDENCE_LEDGER`).
6. **خروجی رسمی ۱۴ گانه ورد:** تدوین کامل ۱۴ بخش مصوب با فونت دبی، تگ‌های native RTL bidi XML و نگارش یک پاراگراف تفصیلی مجزا برای تک‌تک مراجع در مرور منابع.
7. **آزمون‌های اعتبارسنجی چهارگانه:** پاس شدن ۱۰۰٪ آزمون‌ها در سوئیت جامع ۷۷ تستی بدون ادعای ساختگی.

---

## مجوز (License)
این پروژه تحت مجوز [MIT License](LICENSE) منتشر شده است.
