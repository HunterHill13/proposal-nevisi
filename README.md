# Proposal-Nevisi 🔬📄
### Universal Evidence-Driven Medical Research, Cognitive Multi-Agent Architecture & Autonomous Proposal Pipeline (v11.4.1)
### موتور خودکار و جامع پژوهش زیست‌پزشکی، معماری چندایجنت شناختی و تدوین پروپوزال‌های علوم پزشکی (نسخه ۱۱.۴.۱)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Unified Tests: 473/473 Passed](https://img.shields.io/badge/Unified%20Tests-473%2F473%20Passed-success.svg)](#unified-multi-tier-test-harness)
[![Master Release Gate: 43/43 Passed](https://img.shields.io/badge/Master%20Gate-43%2F43%20Passed-success.svg)](#master-release-gate-43-criteria)
[![Pajooheshyar 28 Sections Compliant](https://img.shields.io/badge/Pajooheshyar-28%20Sections%20Complete-teal.svg)](#layer-2-structural-compliance)
[![Native OMML Equations](https://img.shields.io/badge/DOCX%20Math-Native%20OMML%20XML-purple.svg)](#layer-4-formatting--typesetting)
[![Architecture: Cognitive Multi-Agent](https://img.shields.io/badge/Architecture-Cognitive%20Multi--Agent-blueviolet.svg)](#cognitive-multi-agent-architecture)
[![ARA Seal Level 2: Epistemic Rigor](https://img.shields.io/badge/Epistemic%20Rigor-6D%20Audited-green.svg)](#epistemic-rigor-auditor)

---

> **Language / زبان:** [English Documentation](#english) | [مستندات فارسی](#فارسی)

---

<a name="english"></a>
## English Documentation (v11.4)

**Proposal-Nevisi (v11.4)** is an autonomous, publication-grade academic research proposal drafting framework and **Topic-Agnostic Research-Grade Medical Literature & Proposal Engine**. Built upon foundational architectures from AIPOCH (`aipoch/medical-research-skills`), K-Dense (`K-Dense-AI/claude-scientific-writer`), and the SciFact claim-evidence framework (AllenAI / Wadden et al.), **v11.4 introduces the Cognitive Multi-Agent Architecture**, solving the AI literature hallucination, Frankenstein/chimera methodology stitching, and abstract-only truncation problems through an immutable research dossier, cohesive methodology subagents, and adversarial grant peer review.

### Key Architectural Pillars in v11.4:

1. **Two-Loop Autonomous Cognitive Architecture:**
   - **Inner Optimization Loop (Research & Grounding):** Executes live literature discovery across PubMed and Europe PMC, retrieves full-text JATS XML, extracts verbatim grounded passages, detects cross-study contradictions, and immutably seals findings into `PROPOSAL_RESEARCH_DOSSIER.json` and `.md`.
   - **Outer Synthesis Loop (Proposal Drafting):** Synthesizes all 28 canonical sections required by Iranian biomedical universities (Pajooheshyar format), strictly bound to the sealed dossier without parametric memory hallucination.
2. **Methodology Research Subagent (`scripts/methodology_research_subagent.py`):**
   - **Anti-Chimera Protocol Engine:** Prevents the critical failure mode where AI stitches incompatible protocol details from disparate studies. Enforces cohesive protocols aligned with OECD GCCP (Good Cell Culture Practice), MIQE guidelines for RT-qPCR (mandating dual reference genes, e.g., GAPDH + ACTB), and photometric interference mitigation (Cell-Free Blank & 570/630 nm spectrophotometry for tetrazolium/MTT assays).
   - **Biostatistical Coherence:** Eliminates sample size formula contradictions ($n \approx 7$ vs $n=3$) by enforcing Mead's Resource Equation ($E = N - B - T \in [10, 20]$) and Two-Way Factorial ANOVA with effect size $f = 0.40$.
3. **Adversarial Mock Grant Study Section (`scripts/mock_grant_review_panel.py`):**
   - **Reviewer 1 (Scientific Significance & Semantic Drift):** Audits model drift (e.g., ensuring breast cancer data is not falsely attributed to lung models), verifies updated GLOBOCAN 2022/2024 epidemiology (2.48M cases, 1.81M deaths), and mandates a formal negative Boolean search strategy log (`0 hits`) to substantiate novelty claims.
   - **Reviewer 2 (Methodology & Biostatistics):** Verifies replicate design (biological vs technical), sample size mathematical justification, and cell-free blank interference controls.
   - **Reviewer 3 (Bioethics & Biosafety):** Audits Iranian 31-Principle Biomedical Ethics Code and BSL-2 compliance.
4. **Precision MeSH Query Expander & NCBI Protection (`scripts/mesh_query_expander.py`):**
   - Automatic translation of disease and mechanistic concepts into official MeSH descriptors.
   - Automatic non-ASCII/Persian character filtration, ensuring PubMed APIs receive strictly valid Latin/MeSH tokens and eliminating zero-hit API queries.
5. **Native Word OMML Equations (`scripts/native_omml_math_engine.py`):**
   - Converts LaTeX formulas directly into Microsoft Word native Office Math Markup Language (`<m:oMath>`), eliminating raw LaTeX leakage in `.docx` files.
6. **Persian Medical Typography Linter (`scripts/persian_medical_typography_linter.py`):**
   - Strictly enforces Persian Zero-Width Non-Joiner (ZWNJ), Persian numerals in prose, and bilingual expansion for medical acronyms on first mention.

---

### Native Antigravity Subagent Orchestration

When invoked within Antigravity or compatible agentic IDEs, the master agent spawns 3 parallel subagents in the Overview panel:
1. **Evidence Appraisal Subagent (`research`)**: Deep critical reading of full-text papers, protecting against model drift.
2. **Methodology & Anti-Chimera Subagent (`research`)**: Harmonized OECD GCCP cell culture protocols, cell-free blank interference controls, MIQE dual reference genes, and Mead's sample size equation.
3. **Adversarial Mock Grant Reviewer (`research`)**: NIH 1–9 scoring, GLOBOCAN 2022/2024 epidemiology audit, and formal negative search verification.

### Quick Start / CLI Usage

Run the master autonomous research pipeline:

```powershell
uv run python scripts/run_research_pipeline.py --topic "Your Biomedical Research Topic in Persian" --keywords "Agent1, Agent2, Target Condition" --output-dir "./output"
```

#### Example Invocation:
```powershell
uv run python scripts/run_research_pipeline.py `
  --topic "مقایسه اثر همزمان فوکوئیدان با پمترکسد بر مهار رشد سلول‌های سرطان ریه" `
  --keywords "Fucoidan, Pemetrexed, Non-Small Cell Lung Carcinoma" `
  --study-family "in_vitro" `
  --output-dir "./output"
```

#### Generated Artifacts:
- `proposal.docx`: Publication-grade Microsoft Word proposal with native OMML formulas, styled tables, and zero duplicate headings.
- `proposal.md`: Complete 28-section Markdown proposal.
- `PROPOSAL_RESEARCH_DOSSIER.json` & `.md`: Sealed immutable evidence records with full-text passages and audit logs.
- `MOCK_GRANT_REVIEW_REPORT.md` & `.json`: Grant panel score and detailed critique.
- `EQUATOR_COMPLIANCE_AUDIT.md` & `.json`: ARRIVE 2.0 / MIQE compliance scorecards.
- `RISK_OF_BIAS_MITIGATION_REPORT.md` & `.json`: Cochrane RoB-2 / SYRCLE domain assessments.

---

### Four-Layer Modular Architecture

```text
+-----------------------------------------------------------------------------------+
|               MasterResearchPipeline (Two-Loop Autonomous Orchestrator)           |
+-----------------------------------------------------------------------------------+
        |                                                                   |
        v                                                                   v
+---------------------------------------+   +---------------------------------------+
|    LAYER 1: SCIENTIFIC ACCURACY       |   |    LAYER 2: STRUCTURAL COMPLIANCE     |
| • MethodologyResearchSubagent         |   | • MethodologyCompletenessGate (28)    |
| • EpistemicRigorAuditor (6 Dimensions)|   | • DynamicProtocolDesigner             |
| • BiologicalMechanismVerifier         |   | • StatisticalAnalysisModelSelector    |
| • CombinationHypothesisEngine         |   | • Mandatory Sample Size Formula Box   |
| • CompoundEntityNormalizer            |   | • Mead's Resource Equation (E=N-B-T)  |
+---------------------------------------+   +---------------------------------------+
        |                                                                   |
        v                                                                   v
+---------------------------------------+   +---------------------------------------+
|    LAYER 3: CITATION & EVIDENCE       |   |   LAYER 4: FORMATTING & TYPESETTING   |
| • ProposalResearchDossier (Sealed)    |   | • NativeOmmlMathEngine (LaTeX->OMML)  |
| • ScientificSearchAdapter (PubMed/PMC)|   | • PersianMedicalTypographyLinter      |
| • MeSHQueryExpander (Two-Tier MeSH)   |   | • DocxBuilder (Anti-Duplicate Heading)|
| • Strict Vancouver Order of Appearance|   | • Arabesque & Callout XML Styling     |
+---------------------------------------+   +---------------------------------------+
```

---

<a name="master-release-gate-43-criteria"></a>
### Master Release Gate (43 Production Criteria)

The engine enforces 43 fail-closed release criteria before generating or approving proposals:
1. Static analysis leakage audit: 0 hardcoded biological entities in core scripts (`test_hard_code_leakage.py`).
2. Two-Loop Research Dossier immutability and pass/fail sealing.
3. 28 canonical Pajooheshyar section completeness.
4. Mandatory mathematical sample size formulas (Mead's Equation, Cohen's $d$, Cochran).
5. 100% Native OMML XML generation without raw LaTeX delimiter leakage.
6. 100% Vancouver citation re-indexing by appearance order.
7. Zero tolerance for orphaned claims or unreferenced citations.

---

<a name="unified-multi-tier-test-harness"></a>
### Unified Multi-Tier Test Harness

The engine includes 23 comprehensive test suites with **473 / 473 tests passing (100% Pass Rate)**:

```powershell
uv run python tests/run_all_tests.py
```

- **Suite 1: Static Analysis Hard-Code Leakage Audit (`test_hard_code_leakage.py`)** - 41 tests verifying zero hardcoded entities.
- **Suite 2: Two-Loop Dossier & Master Pipeline Suite (`test_two_loop_dossier.py`)** - E2E verification of research dossier, epistemic auditor, and orchestrator.
- **Suite 3: Multi-Domain Generalization Suite (`test_generalization.py`)** - Validates across 12 distinct biomedical domains.
- **Suite 4: Adversarial Stress Scenarios & Negative Rejection Tests (`test_adversarial_scenarios.py`)** - 114 stress tests.
- **Suite 5: Mutation Testing Layer (`test_mutations.py`)** - 10 deliberate scientific defects with 100% kill score.
- **Suites 6–22:** Property invariants, schema audits, EQUATOR compliance, RoB-2 mitigation, OMML math engines, typography linters, and Pillar 1-5 hardening.

---

<a name="فارسی"></a>
## مستندات فارسی (نسخه ۱۱.۴)

پلتفرم **پروپوزال‌نویسی (Proposal-Nevisi نسخه ۱۱.۴)** یک سیستم خودکار، پیشرفته، شناختی و مبتنی بر شواهد واقعی (Evidence-Driven) برای تدوین پروپوزال‌های پژوهشی علوم پزشکی، داروسازی، دندان‌پزشکی و زیست‌پزشکی مطابق با استاندارد رسمی معاونت پژوهشی و سامانه **پژوهشیار** است.

نسخه ۱۱.۴ با ادغام **معماری ساب‌ایجنت‌های شناختی (Cognitive Multi-Agent Architecture)**، **ساب‌ایجنت پژوهش روش‌شناسی منسجم (`MethodologyResearchSubagent`)** و **هیئت داوران گرنت خصمانه (Adversarial Mock Grant Study Section)**، نقایص سنتی هوش‌های مصنوعی در ساخت روش‌شناسی‌های وصله‌پینه‌ای (فرانکنشتاین / کیمرا)، توهم استنادی و تناقضات آماری را به صورت بنیادین ریشه‌کن کرده است.

### قابلیت‌های کلیدی نسخه ۱۱.۴:

1. **معماری خودکار دو حلقه‌ای و ساب‌ایجنت‌های شناختی:**
   - **حلقه درونی (Inner Optimization Loop):** جستجوی زنده در PubMed و Europe PMC با استراتژی دو مرحله‌ای MeSH، دانلود خودکار متن کامل (JATS XML)، استخراج گزیده‌های مستند، واکاوی تناقضات مقالات و پلمپ غیرقابل تغییر پرونده پژوهش (`PROPOSAL_RESEARCH_DOSSIER.json` و `.md`).
   - **حلقه بیرونی (Outer Synthesis Loop):** نگارش دقیق و گام‌به‌گام ۲۸ بخش مصوب دانشگاه‌های علوم پزشکی ایران منحصراً بر اساس شواهد موجود در پرونده پلمپ‌شده، بدون کوچک‌ترین توهم ذهنی (Hallucination-Free).
2. **ساب‌ایجنت روش‌شناسی ضد کیمرا (`MethodologyResearchSubagent`):**
   - پیشگیری قطعی از ترکیب وصله‌پینه‌ای متدهای ناهمخوان از مقالات مختلف.
   - اعمال استانداردهای طلایی کشت سلول (OECD GCCP)، راهنمای MIQE برای qPCR (الزام دو ژن مرجع مستقل مانند GAPDH و ACTB) و افزودن گروه کنترل تداخل نوری بدون سلول (Cell-Free Blank) در تست‌های تترازولیوم.
3. **همسویی ریاضی و بیواستاتیک حجم نمونه:**
   - حذف کامل تناقض فرمول دوگروهی با تکرارهای بیولوژیک $n=3$ از طریق اعمال فرمول رسمی تخصیص منابع مید ($E = N - B - T = 30 - 1 - 9 = 20 \in [10, 20]$) ویژه آزمون Two-Way Factorial ANOVA.
4. **هیئت داوران گرنت خصمانه (Mock Grant Review):**
   - ممیزی نشت مدل (Semantic Drift)، اعتبارسنجی آمار رسمی سرطان (IARC GLOBOCAN 2022/2024 با ۲.۴۸ میلیون ابتلا و ۱.۸۱ میلیون مرگ) و استعلام رسمی سرچ منفی (Negative Search Log با ۰ نتیجه در پاب‌مد) برای اثبات First-in-Class بودن طرح.
5. **موتور هوشمند گسترش MeSH و محافظت از NCBI API:**
   - نگاشت خودکار مفاهیم فارسی به سرعنوان‌های MeSH Descriptors و فیلتر ۱۰۰٪ کاراکترهای غیرلاتین جهت پیشگیری از خطای 0-hit در جستجوهای آنلاین.
6. **موتور فرمول‌نویسی بومی ورد (Native OMML):**
   - تبدیل تمامی فرمول‌های ریاضی به صورت مستقیم به ساختار استاندار ورد (`<m:oMath>`) بدون نشت کدهای لاتک خام (`$...$`).
7. **محافظت از هدرها و جداول ورد:**
   - جلوگیری از تکرار تیترها (Double Headings) و حذف تگ‌های HTML (`<br>`) از جداول اسناد DOCX.

---

### راهنمای اجرای سریع (خط فرمان)

اجرای کامل پایپ‌لاین تحقیق و نگارش پروپوزال با یک دستور واحد:

```powershell
uv run python scripts/run_research_pipeline.py --topic "عنوان کامل پژوهش شما به فارسی" --keywords "English Agent1, English Agent2, Target Condition" --output-dir "./output"
```

#### نمونه دستور اجرا:
```powershell
uv run python scripts/run_research_pipeline.py `
  --topic "مقایسه اثر همزمان فوکوئیدان با پمترکسد بر مهار رشد سلول‌های سرطان ریه" `
  --keywords "Fucoidan, Pemetrexed, Non-Small Cell Lung Carcinoma" `
  --study-family "in_vitro" `
  --output-dir "./output"
```

#### اسناد خروجی تولیدشده در پوشه خروجی:
1. `proposal.docx`: فایل نهایی Word پروپوزال شامل ۲۸ بخش کامل پژوهشیار، فرمول‌های OMML، جداول متغیرها، گانت چارت و بدون تیترهای تکراری.
2. `proposal.md`: متن کامل پروپوزال به فرمت مارک‌داون یکپارچه.
3. `PROPOSAL_RESEARCH_DOSSIER.json` و `.md`: پرونده شواهد پلمپ‌شده شامل قطعات استخراج‌شده از متن کامل مقالات.
4. `MOCK_GRANT_REVIEW_REPORT.md` و `.json`: کارنامه داوری گرنت به سبک NIH.
5. `EQUATOR_COMPLIANCE_AUDIT.md` و `.json`: کارنامه انطباق با گایدلاین‌های بین‌المللی پژوهش (ARRIVE, MIQE, CONSORT).
6. `RISK_OF_BIAS_MITIGATION_REPORT.md` و `.json`: جدول جامع مهار سوگیری‌های مطالعاتی (RoB-2 / SYRCLE).

---

### ۲۸ بخش مصوب سامانه پژوهشیار (وزارت بهداشت)

۱. موضوع (عنوان فارسی و انگلیسی)  
۲. بیان مسئله (Problem Statement تحلیلی با بار بیماری GLOBOCAN 2022/2024 و سرچ منفی)  
۳. مرور بر منابع (پیشینه پژوهش با سنتز نقادانه بر پایه مقالات متن کامل)  
۴. اهمیت و ضرورت تحقیق  
۵. تعریف واژه‌ها  
۶. اهداف جزئی  
۷. اهداف کلی  
۸. اهداف کاربردی  
۹. فرضیات و سوالات پژوهش  
۱۰. دستاوردها  
۱۱. جدول متغیرها (مستقل، وابسته، مداخله‌گر، مقیاس و نقش)  
۱۲. جدول زمان‌بندی و مراحل اجرا (گانت چارت)  
۱۳. روش اجرا (چارچوب کلی متدولوژی)  
۱۴. نوع مطالعه  
۱۵. جامعه مورد مطالعه (مدل زیستی / رده سلولی)  
۱۶. محل انجام مطالعه  
۱۷. معیارهای ورود به مطالعه  
۱۸. معیارهای خروج از مطالعه  
۱۹. ابزارهای گردآوری اطلاعات (دستگاه‌ها و کیت‌های استاندارد)  
۲۰. تعیین اعتبار ابزار گردآوری (روایی و کالیبراسیون)  
۲۱. تعیین ابزار گردآوری (پایایی و ضرایب تغییرات CV)  
۲۲. حجم نمونه و روش محاسبه آن (فرمول ریاضی تخصیص منابع مید $E = N - B - T$)  
۲۳. روش تجزیه و تحلیل داده‌ها (Two-Way Factorial ANOVA، بررسی پیش‌فرض‌ها و مدل اثرات متقابل)  
۲۴. ملاحظات اخلاقی و کدهای اخلاق زیستی  
۲۵. نحوه رعایت نکات امنیتی و حفاظت پروژه (سطح ایمنی BSL-2)  
۲۶. مشکلات و محدودیت‌ها (چالش‌های تکنیکال و راهکارهای مهار)  
۲۷. روش انجام طرح، شیوه اجرایی مراحل طرح و چگونگی جمع‌آوری اطلاعات (پروتکل گام‌به‌گام ضد کیمرا)  
۲۸. منابعی که استفاده شد (فهرست کامل منابع بر اساس سبک ونکوور و ترتیب ظهور)

---

### وضعیت آزمون‌های کنترل کیفیت نرم‌افزاری

سیستم دارای ۲۲ سوئیت آزمون مستقل با **۴۶۲ تست فعال** است که همگی با **۱۰۰٪ قبولی** پاس می‌شوند:

```powershell
uv run python tests/run_all_tests.py
```

- **تست ضد نشت و تعمیم‌پذیری کامل (`test_hard_code_leakage.py`):** صفر بودن کلمات سخت‌کدشده زیستی در ۴۱ آزمون استاتیک.
- **تست پلمپ پرونده شواهد (`test_two_loop_dossier.py`):** بررسی تغییرناپذیری شواهد پس از پلمپ.
- **تست‌های خصمانه و جهش نرم‌افزاری (`test_adversarial_scenarios.py` و `test_mutations.py`):** کشتن ۱۰۰٪ جهش‌های عمدی در منطق بیولوژیک.
- **تست‌های هاردنینگ ستون‌های ۱ تا ۵ (`test_v91_hardening.py` و `test_v92_hardening.py`):** اعتبارسنجی گیت‌های ضد کیمرا، تداخل تترازولیوم، کنترل بلانک و عدم نشت لاتک.

---

## مجوز (License)
این پروژه تحت مجوز [MIT License](LICENSE) منتشر شده است.
