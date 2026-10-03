# Proposal-Nevisi 🔬📄
### Evidence-Driven Deep Literature Research, Adversarial Verification & Medical Proposal Generator (v7.0)
### موتور سنتز عمیق شواهد علمی، راستی‌آزمایی خصمانه و نگارش پروپوزال‌های پژوهشی علوم پزشکی

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Audit Suite: 60/60 Passed](https://img.shields.io/badge/Audit%20Suite-60%2F60%20Passed-success.svg)](#60-test-behavioral-and-scientific-self-audit-suite)
[![PRISMA 2020 Compliant](https://img.shields.io/badge/PRISMA-2020%20Compliant-orange.svg)](#prisma-2020-search-accounting)

---

> **Language / زبان:** [English](#english) | [فارسی](#فارسی)

---

<a name="english"></a>
## English Documentation

**Proposal-Nevisi (v7.0)** is an autonomous, publication-grade academic research proposal drafting framework and **Evidence-Driven Deep Literature Research, Adversarial Verification & Cross-Study Synthesis Engine** tailored for medical, biomedical, and experimental oncology research protocols.

Unlike conventional retrieval agents that rely on superficial keyword matching and arbitrary paper limits, Proposal-Nevisi executes an end-to-end **15-Stage Evidence Funnel** across four major biomedical graph engines (PubMed/MeSH, Europe PMC, OpenAlex, Crossref), enforces claim-level sentence provenance, performs claim-evidence entailment audits, builds structured 34-field Study Evidence Records, conducts 12-dimension pairwise study comparability, classifies contradictions across Categories A–F, models claim dependencies as an acyclic DAG with 14 typed edge relationships, reconciles PRISMA 2020 flow math, addresses 11 mandatory epistemic inquiries, and compiles beautifully formatted Microsoft Word documents adhering to native Arabic/Persian Right-to-Left (RTL) typography.

---

### Core Architectural Principles (v7.0)

1. **No Arbitrary Final-Paper Cap (Emergent Evidence Set with Min 15 Sufficiency Gate):**
   - Reference volume emerges organically from the factual claims required in the proposal (in this benchmark: 40 landmark references).
   - The minimum count (15 references) acts as a **sufficiency gate**, NOT a selection target (zero dummy reference padding).
   - Every included reference must be actually cited in the proposal body text (`Unused References == 0`).

2. **Field-Level Bibliographic & Honest Author Verification:**
   - Evaluates metadata at the individual field level (DOI, PMID, Title, First Author, Journal, Year, Volume, Issue, Pages).
   - Author verification engine: `EXACT_AUTHOR_MATCH`, `FUZZY_AUTHOR_MATCH`, `AUTHOR_MISMATCH`, and `AUTHOR_UNAVAILABLE`.
   - Strictly zero fake positive score fallbacks (e.g. eliminating the 0.8 fallback for missing authors).

3. **Study-Level Evidence Modeling (34 Structured Fields):**
   - Every proposal reference is modeled in `STUDY_EVIDENCE_RECORD.json` across 34 granular fields (study design, tier, intervention, control, dose, exposure, outcomes, findings, quantitative parameters, risk of bias, limitations, etc.).
   - Dual-format export of `EVIDENCE_MATRIX.csv` and `EVIDENCE_MATRIX.json` with 20 unified columns.
   - Transparent preclinical reporting: unrecorded parameters are explicitly marked `NOT_REPORTED`.

4. **Pairwise Study Comparability Analysis (12 Dimensions):**
   - Evaluates study pairs across 12 dimensions in `STUDY_COMPARABILITY_MATRIX.json`: model system, cell line passage, agent source purity, vehicle control, dose range, exposure duration, assay readout, endpoint timing, normalization method, statistical test, replicate structure, and serum culture conditions.
   - Categorizes pairs into `HIGH_COMPARABILITY`, `MODERATE_COMPARABILITY`, `LOW_COMPARABILITY`, and `NOT_COMPARABLE` (over 400 pairs honestly identified as Not Comparable).

5. **Contradictory Evidence Engine & Strict Taxonomy (Categories A to F):**
   - Dedicated active search across 6 negative evidence categories: Antagonism, High-Dose Toxicity, Resistance, Interferon Clearance, Solubility Limits, and Null Findings.
   - Rigorous taxonomy classification: only Category A (`A_DIRECT_CONTRADICTION`) is a true direct contradiction (identical model, agent, dose, with opposite result). Differences in formulation or cell line are properly classified as `B_CONTEXTUAL_DISAGREEMENT` or `E_METHODOLOGICAL_DISAGREEMENT`.

6. **Claim Dependency Graph (Acyclic DAG) & Mechanism Chaining:**
   - Formal DAG modeling in `CLAIM_DEPENDENCY_GRAPH.json` (0 circular dependencies).
   - Multi-hop mechanism chains explicitly label deductive syntheses as `MECHANISTICALLY_PLAUSIBLE_INFERENCE`.
   - Cross-study relationships mapped using 14 approved typed edges in `CROSS_STUDY_RELATIONSHIP_LEDGER.json`.

7. **PRISMA 2020 Transparent Flow Accounting & 19-Section Synthesis:**
   - `PRISMA_SEARCH_ACCOUNTING.json` and `PRISMA_FLOW_DATA.json` with exact mathematical reconciliation across all identification, screening, eligibility, and inclusion stages.
   - Comprehensive evidence synthesis report in `FINAL_EVIDENCE_SYNTHESIS.md` containing all 19 structured sections and addressing 11 key epistemic inquiries.

8. **Master Word Typography & RTL Bidi XML:**
   - Persian `Dubai` typography with native Word `<w:bidi/>`, `<w:rtlGutter/>`, and `<w:bCs/>` bolding.

---

### 60-Test Behavioral and Scientific Self-Audit Suite

The suite evaluates 60 automated tests partitioned into three epistemic tiers:
- **TIER 1: STRUCTURAL_TEST (Tests 1 to 20):** Schema validation, 20-column evidence matrix export, PRISMA mathematical reconciliation, DAG acyclicity, universal citation coverage.
- **TIER 2: SCIENTIFIC_VALIDITY_TEST (Tests 21 to 45):** Chemical entity purity (zero arjunolic/betulin/ginsenoside conflation), biological tissue lineage purity (zero colorectal/ovarian/quail misattribution), empirical Chou-Talalay CI extraction, vehicle DMSO boundary (<= 0.1% v/v), concentration ceiling (Lupeol <= 80 μM), Type I IFN selectivity grounding in BEAS-2B vs A549, syncytial oncolysis, mitochondrial caspase cascade, and Akt survival suppression.
- **TIER 3: ADVERSARIAL_COUNTER_EXAMPLE_TEST (Tests 46 to 60):** Active negative control injection verifying that misleading chemical compounds, wrong host cell models, monotherapy-to-synergy fallacies, in vitro to clinical leaps, toxic vehicle doses, and fake direct replications are strictly REJECTED with 100% precision.

```bash
# Execute the complete 60-test self-audit suite:
python .agents/skills/proposal-nevisi/scripts/self_audit_suite.py
```

---

<a name="فارسی"></a>
## مستندات فارسی (راهنمای استفاده)

**مهارت جامع نگارش پروپوزال‌های پژوهشی علوم پزشکی و موتور Deep Research (نسخه ۷.۰)** یک بستر جامع و استاندارد برای تدوین پروپوزال‌های تراز اول دانشگاهی مطابق با دستورالعمل‌های رسمی معاونت تحقیقات و فناوری وزارت بهداشت، درمان و آموزش پزشکی است.

### ویژگی‌های بنیادین نسخه ۷.۰:
1. **عدم اعمال سقف ساختگی بر منابع:** منابع به صورت پدیدارشده و بر پایه پوشش ادعاهای علمی گزینش می‌شوند (۴۰ رفرنس اصیل و ۱۰۰٪ استناد شده در این پژوهش).
2. **کف ۱۵ منبع به عنوان دروازه سنجش کفایت:** هیچ منبع کمکی یا بی‌کیفیتی صرفاً برای رسیدن به عدد به سیستم تزریق نمی‌شود (`Padding Added == 0`).
3. **اعتبارسنجی فیلد-محور کتابشناختی:** راستی‌آزمایی تفکیک‌شده DOI، PMID و نام دقیق نویسنده اول بدون ضریب خطای ساختگی.
4. **مدل‌سازی شواهد با ۳۴ فیلد استاندارد:** ثبت دقیق مدل سیستم، شرایط مداخله، شاخص‌های شو-تالالای و ابهام‌زدایی متدولوژیک در `STUDY_EVIDENCE_RECORD.json` و ماتریس ۲۰ ستونی.
5. **موتور شواهد منفی و تحلیل تناقضات:** کاوش در ۶ حوزه تضاد احتمالی و طبقه‌بندی دقیق در تاکسونومی ۶ گانه A تا F.
6. **گراف بدون دور وابستگی ادعاها (DAG):** مهار کامل مغالطات دوری و برچسب‌گذاری صریح زنجیره‌های فرضی مکانیسمی.
7. **سوئیت آزمونگر ۶۰ گانه در سه سطح:** شامل آزمون‌های ساختاری، اعتبارسنجی تجربی و نمونه‌های نقض خصمانه (100% PASS).
8. **خروجی لوکس ورد (.docx):** سازگاری کامل با فونت دبی (Dubai)، چینش راست‌به‌چپ (RTL)، بدون خط‌تیره‌های اضافی و واجد تمامی جداول استاندارد.

---
### ساختار فایل‌ها و اسکریپت‌ها

| فایل / اسکریپت | شرح عملکرد |
| :--- | :--- |
| `scripts/claim_entailment_engine.py` | استخراج رکوردهای ۳۴ فیلدی و ماتریس شواهد ۲۰ ستونی |
| `scripts/adversarial_search_engine.py` | کاوش شواهد منفی و طبقه‌بندی تاکسونومی تناقضات |
| `scripts/study_comparability_v2.py` | ارزیابی همسنجی دوبه‌دوی مطالعات در ۱۲ بعد متدولوژیک |
| `scripts/cross_study_ledger.py` | مدل‌سازی گراف DAG، یال‌های ۱۴ گانه و ممیزی مرزبندی علمی |
| `scripts/evidence_synthesis_v7.py` | تدوین سنتز شواهد در ۱۹ بخش و پاسخ به ۱۱ پرسش معرفت‌شناختی |
| `scripts/reference_validity_auditor.py` | ممیزی زنده و فیلد-محور اعتبار مراجع و نویسندگان |
| `scripts/self_audit_suite.py` | اجرای سوئیت ۶۰ آزمون خود-ممیزی رفتاری و علمی |
| `scripts/docx_builder.py` | کامپایل فایل Word پروپوزال با استانداردهای RTL |
