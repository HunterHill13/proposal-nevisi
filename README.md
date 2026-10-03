# Proposal-Nevisi 🔬📄
### Evidence-Driven Deep Literature Research Engine & Academic Proposal Generator (v6.0)
### موتور سنتز عمیق شواهد علمی و نگارش پروپوزال‌های پژوهشی علوم پزشکی

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Audit Suite: 54/54 Passed](https://img.shields.io/badge/Audit%20Suite-54%2F54%20Passed-success.svg)](#54-test-behavioral-self-audit-suite)
[![PRISMA 2020 Compliant](https://img.shields.io/badge/PRISMA-2020%20Compliant-orange.svg)](#prisma-2020-search-accounting)

---

> **Language / زبان:** [English](#english) | [فارسی](#فارسی)

---

<a name="english"></a>
## English Documentation

**Proposal-Nevisi** is an autonomous, publication-grade academic research proposal drafting framework and **Evidence-Driven Deep Literature Research & Synthesis Engine (v6.0)** tailored for medical, biomedical, and life science research protocols.

Unlike conventional retrieval agents that rely on superficial keyword searches and arbitrary paper limits, Proposal-Nevisi executes an end-to-end **15-Stage Evidence Funnel** across four major biomedical graph engines, enforces claim-level sentence provenance, performs claim-evidence entailment audits, builds structured 34-field Study Evidence Records, conducts 12-dimension pairwise study comparability, classifies contradictions across Categories A–F, models claim dependencies as an acyclic DAG, reconciles PRISMA 2020 flow math, and compiles beautifully formatted Microsoft Word documents adhering to native Arabic/Persian Right-to-Left (RTL) typography.

---

### Core Architectural Principles (v6.0)

1. **No Arbitrary Final-Paper Cap (Emergent Evidence Set with Min 15 Sufficiency Gate):**
   - No hardcoded maximum caps (neither 15, 20, 50, nor 80).
   - Reference volume emerges organically from the factual claims required in the proposal.
   - The minimum count (15 references) acts as a **sufficiency gate**, NOT a selection target (zero dummy reference padding).
   - Every included reference must be actually cited in the proposal body text (`Unused References == 0`).

2. **Field-Level Bibliographic & Honest Author Verification:**
   - Evaluates metadata at the individual field level (DOI, PMID, Title, First Author, Journal, Year, Volume, Issue, Pages).
   - Author verification engine: `EXACT_AUTHOR_MATCH`, `FUZZY_AUTHOR_MATCH`, `AUTHOR_MISMATCH`, and `AUTHOR_UNAVAILABLE`.
   - Strictly zero fake positive score fallbacks (e.g. eliminating the 0.8 fallback for missing authors).

3. **Study-Level Evidence Modeling (34 Structured Fields):**
   - Every proposal reference is modeled in `STUDY_EVIDENCE_RECORD.json` across 34 granular fields (study design, tier, intervention, control, dose, exposure, outcomes, findings, quantitative parameters, risk of bias, limitations, etc.).
   - Dual-format export of `EVIDENCE_MATRIX.csv` and `EVIDENCE_MATRIX.json` with 20 unified columns.

4. **Pairwise Study Comparability Analysis (12 Dimensions):**
   - Evaluates study pairs across 12 dimensions in `STUDY_COMPARABILITY_MATRIX.json`: model system, cell line passage, agent source purity, vehicle control, dose range, exposure duration, assay readout, endpoint timing, normalization method, statistical test, replicate structure, and serum culture conditions.
   - Categorizes pairs into `HIGH_COMPARABILITY`, `MODERATE_COMPARABILITY`, `LOW_COMPARABILITY`, and `NOT_COMPARABLE`.

5. **Contradictory Evidence Engine & Strict Taxonomy (Categories A to F):**
   - Dedicated active search across 6 negative evidence categories: Antagonism, High-Dose Toxicity, Resistance, Interferon Clearance, Solubility Limits, and Null Findings.
   - Rigorous taxonomy classification: only Category A (`A_DIRECT_CONTRADICTION`) is a true direct contradiction (identical model, agent, dose, with opposite result). Differences in formulation or cell line are properly classified as `B_CONTEXTUAL_DISAGREEMENT` or `E_METHODOLOGICAL_DISAGREEMENT`.

6. **Claim Dependency Graph (Acyclic DAG) & Mechanism Chaining:**
   - Formal DAG modeling in `CLAIM_DEPENDENCY_GRAPH.json` (0 circular dependencies).
   - Mechanism chains strictly distinguish `DIRECTLY_SUPPORTED` steps from `BIOLOGICALLY_PLAUSIBLE_HYPOTHESIS` steps.
   - Cross-study relationships mapped using 12 approved typed edges.

7. **PRISMA 2020 Transparent Flow Accounting & 19-Section Synthesis:**
   - `PRISMA_SEARCH_ACCOUNTING.json` and `PRISMA_FLOW_DATA.json` with exact mathematical reconciliation across all identification, screening, eligibility, and inclusion stages.
   - Comprehensive evidence synthesis report in `FINAL_EVIDENCE_SYNTHESIS.md` containing all 19 structured sections.

8. **Master Word Typography & RTL Bidi XML:**
   - Persian `Dubai` typography with native Word `<w:bidi/>`, `<w:rtlGutter/>`, and `<w:bCs/>` bolding.
   - Clean professional layout free of disruptive divider dashes (`---`).

---

### 54-Test Behavioral Self-Audit Suite

The automated audit suite (`scripts/self_audit_suite.py`) verifies 54 rigorous criteria on real data:
- **Tests 1–16:** Retrieval pagination, zero-cap behavior, universal full-text auditing, tier segregation, multi-DB contribution, query matrix, contradictory search, deduplication, saturation, verbatim quotes, claim graph, sufficiency gate, research gaps, decoupled quality/relevance, PubChem/Reactome live grounding.
- **Tests 17–28:** Minimum 15 references, zero padding code, claim support, role integrity, bounded novelty, Dubai RTL typography, cross-artifact consistency, actual citations in proposal body, zero unused references.
- **Tests 29–34:** Bibliographic validity, DOI/PMID integrity, scientific relevance mapping, non-circular entailment, necessity/zero redundancy, composite validity gate.
- **Tests 35–54 (v6.0 New Engines):** 34-field study evidence completeness, RoB reporting honesty (NOT_REPORTED policy), direct vs indirect classification, in vitro to in vivo boundaries, 6 negative search categories, A–F contradiction taxonomy, 12 comparability dimensions, 7 certainty dimensions without fake numbers, CSV/JSON matrix export integrity, acyclic DAG dependency graph, mechanism chaining distinction, 12 typed cross-study edges, Chou-Talalay CI precision, 13 gap categories, negative evidence non-triviality, PRISMA flow mathematical reconciliation, 19 synthesis sections, field-level verification, honest author verification, and composite synthesis engine gate.

---

### Command-Line Execution

```bash
# 1. Install prerequisites
pip install python-docx pywin32

# 2. Run Complete v6.0 Synchronization & Evidence Synthesis Pipeline
python scripts/sync_proposal_and_audit.py "g:/path/to/project"

# 3. Run Comprehensive 54-Test Behavioral Self-Audit Suite
python scripts/self_audit_suite.py "g:/path/to/project"
```

---
---

<a name="فارسی"></a>
## راهنمای فارسی (Persian Documentation)

مهارت **Proposal-Nevisi (نسخه ۶.۰)** یک دستیار خودکار، تخصصی و فوق‌پیشرفته برای تدوین و ارتقای پروپوزال‌های پژوهشی علوم پزشکی و زیست‌پزشکی در بالاترین تراز آکادمیک است که مجهز به **موتور سنتز عمیق شواهد علمی (Evidence-Driven Deep Literature Research & Synthesis Engine)** می‌باشد.

---

### اصول کلیدی و معماری نسخه ۶.۰

1. **قاعده کفایت شواهد با پدیدار شدن طبیعی منابع (Sufficiency Gate, Min 15, No Max Cap):**
   - هیچ سقف ساختگی (۱۵، ۲۰، ۳۰، ۵۰ یا ۸۰) بر تعداد مراجع نهایی تحمیل نمی‌شود.
   - مراجع به طور طبیعی از دل شواهد استخراج شده و کف ۱۵ مقاله به عنوان **دروازه سنجش کفایت شواهد** (و نه هدف گزینش) عمل می‌کند.
   - پرسازی مصنوعی مراجع اکیداً ممنوع بوده (`Padding Added == 0`) و تمام مراجع منتخب باید در متن پروپوزال استناد شوند (`Unused Selected References == 0`).

2. **اعتبارسنجی فیلد-محور و صحت‌سنجی صادقانه نویسندگان:**
   - اعتبارسنجی مجزای فیلدهای DOI, PMID, Title, First Author, Journal, Year, Volume, Issue, Pages در `FINAL_REFERENCE_VALIDITY_AUDIT.json`.
   - حذف کامل ضرایب ساختگی 0.8 برای نویسندگان غایب و تمایز دقیق وضعیت‌های `EXACT_AUTHOR_MATCH`, `FUZZY_AUTHOR_MATCH`, `AUTHOR_MISMATCH`, و `AUTHOR_UNAVAILABLE`.

3. **مدل‌سازی شواهد در سطح مطالعه (۳۴ فیلد ساختاریافته):**
   - تولید سند `STUDY_EVIDENCE_RECORD.json` برای تک‌تک مطالعات با ۳۴ فیلد کامل.
   - خروجی همگام ماتریس شواهد در دو فرمت `EVIDENCE_MATRIX.csv` و `EVIDENCE_MATRIX.json` با ۲۰ ستون یکپارچه.

4. **ماتریس همسنجی دوبه‌دوی مطالعات در ۱۲ بعد متدولوژیک:**
   - ارزیابی قابلیت مقایسه مطالعات در ۱۲ بعد در `STUDY_COMPARABILITY_MATRIX.json`:
     `model_system`, `cell_line_passage`, `agent_source_purity`, `vehicle_control`, `dose_range`, `exposure_duration`, `assay_readout`, `endpoint_timing`, `normalization_method`, `statistical_test`, `replicate_structure`, `serum_culture_conditions`.

5. **موتور شواهد منفی و تاکسونومی ۶ گانه تناقضات (دسته‌های A تا F):**
   - جست‌وجوی اختصاصی در ۶ دسته شواهد منفی: آنتاگونیسم، سمیت دوز بالا، مقاومت سلولی، پاکسازی اینترفرونی، محدودیت حلالیت و نتایج بی‌اثر.
   - تفکیک علمی در `CONTRADICTION_ANALYSIS.json` و `NEGATIVE_EVIDENCE_REPORT.md` بر اساس دسته‌های A تا F بدون انتساب کاذب تناقض مستقیم به تفاوت‌های بافتی و مدل.

6. **گراف بدون دور وابستگی ادعاها (DAG) و زنجیره مکانیسمی:**
   - تدوین `CLAIM_DEPENDENCY_GRAPH.json` بدون هرگونه دور باطل.
   - تفکیک قطعی مراحل تأییدشده تجربی (`DIRECTLY_SUPPORTED`) از فرضیات نوآورانه طرح (`BIOLOGICALLY_PLAUSIBLE_HYPOTHESIS`).
   - یال‌های ارتباطی بین مطالعات در ۱۲ دسته استاندارد تاییدشده.

7. **حسابداری جریان PRISMA 2020 و گزارش نهایی تلفیق شواهد در ۱۹ بخش:**
   - انطباق ریاضی دقیق مراحل PRISMA در `PRISMA_SEARCH_ACCOUNTING.json` و `PRISMA_FLOW_DATA.json`.
   - تدوین سند جامع `FINAL_EVIDENCE_SYNTHESIS.md` در ۱۹ بخش ساختارمند استاندارد.

8. **تایپوگرافی مستر ورد (Dubai RTL Bidi XML):**
   - فونت استاندارد دبی با تگ‌های راست‌به‌چپ XML سراسری (`<w:bidi/>` و `<w:rtlGutter/>`) و پررنگ‌سازی Complex Script تیترها (`<w:bCs/>`).

---

### آزمونگر رفتاری ۵۴ گانه خود-ممیزی (54-Test Behavioral Self-Audit)

اسکریپت `scripts/self_audit_suite.py` تمامی ۵۴ ضابطه علمی و متدولوژیک را به صورت ۱۰۰٪ موفقیت‌آمیز بر داده‌های واقعی ارزیابی و تضمین می‌نماید.

---

### نحوه اجرای خط لوله

```bash
# اجرای خودکار کل پایپ‌لاین سنتز شواهد، ممیزی و کامپایل پروپوزال ورد
python scripts/sync_proposal_and_audit.py "g:/path/to/project"

# اجرای مستقل سوئیت ۵۴ آزمون خود-ممیزی
python scripts/self_audit_suite.py "g:/path/to/project"
```

---

### لایسنس (License)

این پروژه تحت مجوز بین‌المللی **MIT License** منتشر شده است.
