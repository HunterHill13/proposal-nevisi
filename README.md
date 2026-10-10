# Proposal-Nevisi 🔬📄
### Universal Evidence-Driven Medical Research, Two-Loop Architecture & Autonomous Proposal Pipeline (v11.0)
### موتور خودکار و جامع پژوهش زیست‌پزشکی، معماری دو حلقه‌ای و تدوین پروپوزال‌های علوم پزشکی (نسخه ۱۱.۰)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Unified Tests: 440/440 Passed](https://img.shields.io/badge/Unified%20Tests-440%2F440%20Passed-success.svg)](#unified-multi-tier-test-harness)
[![Master Release Gate: 43/43 Passed](https://img.shields.io/badge/Master%20Gate-43%2F43%20Passed-success.svg)](#master-release-gate-43-criteria)
[![Pajooheshyar 28 Sections Compliant](https://img.shields.io/badge/Pajooheshyar-28%20Sections%20Complete-teal.svg)](#layer-2-structural-compliance)
[![Native OMML Equations](https://img.shields.io/badge/DOCX%20Math-Native%20OMML%20XML-purple.svg)](#layer-4-formatting--typesetting)
[![Architecture: Two-Loop Autonomous](https://img.shields.io/badge/Architecture-Two--Loop%20Autonomous-blueviolet.svg)](#two-loop-autonomous-architecture)
[![ARA Seal Level 2: Epistemic Rigor](https://img.shields.io/badge/Epistemic%20Rigor-6D%20Audited-green.svg)](#epistemic-rigor-auditor)

---

> **Language / زبان:** [English Documentation](#english) | [مستندات فارسی](#فارسی)

---

<a name="english"></a>
## English Documentation (v11.0)

**Proposal-Nevisi (v11.0)** is an autonomous, publication-grade academic research proposal drafting framework and **Topic-Agnostic Research-Grade Medical Literature & Proposal Engine**. Built upon foundational architectures from AIPOCH (`aipoch/medical-research-skills`), K-Dense (`K-Dense-AI/claude-scientific-writer`), and the SciFact claim-evidence framework (AllenAI / Wadden et al.), **v11.0 introduces the Master Autonomous Two-Loop Research Architecture**, solving the AI literature hallucination and abstract-only truncation problems through an immutable research dossier and fail-closed epistemic auditing.

### Key Architectural Pillars in v11.0:

1. **Two-Loop Autonomous Architecture:**
   - **Inner Optimization Loop (Research & Grounding):** Executes live literature discovery across PubMed and Europe PMC, retrieves full-text XML, extracts verbatim grounded passages, detects cross-study contradictions, and immutably seals findings into `PROPOSAL_RESEARCH_DOSSIER.json` and `.md`.
   - **Outer Synthesis Loop (Proposal Drafting):** Synthesizes all 28 canonical sections required by Iranian biomedical universities (Pajooheshyar format), strictly bound to the sealed dossier without parametric memory hallucination.
2. **Epistemic Rigor Auditor (`scripts/epistemic_rigor_auditor.py`):**
   - 6-Dimensional audit gate aligned with ARA Seal Level 2:
     - Evidence Grounding & DOI/PMID Authenticity
     - Falsifiability & Explicit Null Hypothesis ($H_0$)
     - Methodological & Statistical Coherence
     - Boundary Conditions & Applicability Limits
     - Contradiction & Discordance Resolution
     - Biological Resource Authentication (Cell line STR profiling, mycoplasma guards, catalog codes)
3. **Tri-Fold Peer Review & Compliance Engines:**
   - **Mock Grant Review Panel (`scripts/mock_grant_review_panel.py`):** Simulates an NIH/IRB grant review panel, scoring Significance, Investigators, Innovation, Approach, and Environment on a 1–9 NIH scale.
   - **EQUATOR Compliance Auditor (`scripts/equator_compliance_auditor.py`):** Enforces global reporting standards: ARRIVE 2.0 (in vivo), MIQE (RT-qPCR), CONSORT 2010 (clinical RCTs), and STROBE (observational studies).
   - **Pre-Emptive Risk of Bias Mitigator (`scripts/pre_emptive_risk_of_bias_mitigator.py`):** Implements Cochrane RoB-2 and SYRCLE frameworks, verifying randomization, blinding, and attrition controls.
4. **Native Word OMML Equations (`scripts/native_omml_math_engine.py`):**
   - Converts LaTeX formulas directly into Microsoft Word native Office Math Markup Language (`<m:oMath>`), eliminating raw LaTeX leakage in `.docx` files.
5. **Persian Medical Typography Linter (`scripts/persian_medical_typography_linter.py`):**
   - Strictly enforces Persian Zero-Width Non-Joiner (ZWNJ), Persian numerals in prose, and bilingual expansion for medical acronyms on first mention.

---

### Quick Start / CLI Usage

Run the master autonomous research pipeline with a single command:

```powershell
uv run python scripts/run_research_pipeline.py --topic "Your Biomedical Research Topic" --output-dir "./output"
```

To supply explicit MeSH keywords or study family designs:
```powershell
uv run python scripts/run_research_pipeline.py \
  --topic "Investigating the Synergistic Effect of Metformin and Curcumin in Colon Cancer HCT116 Cells" \
  --keywords "Metformin, Curcumin, Colonic Neoplasms, Apoptosis" \
  --study-family "in_vitro" \
  --output-dir "./output"
```

#### Generated Artifacts:
- `proposal.docx`: Publication-grade Microsoft Word proposal with native OMML formulas and styled tables.
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
| • EpistemicRigorAuditor (6 Dimensions)|   | • MethodologyCompletenessGate (28)    |
| • BiologicalMechanismVerifier         |   | • DynamicProtocolDesigner             |
| • CombinationHypothesisEngine         |   | • StatisticalAnalysisModelSelector    |
| • CompoundEntityNormalizer            |   | • Mandatory Sample Size Formula Box   |
+---------------------------------------+   +---------------------------------------+
        |                                                                   |
        v                                                                   v
+---------------------------------------+   +---------------------------------------+
|    LAYER 3: CITATION & EVIDENCE       |   |   LAYER 4: FORMATTING & TYPESETTING   |
| • ProposalResearchDossier (Sealed)    |   | • NativeOmmlMathEngine (LaTeX->OMML)  |
| • ScientificSearchAdapter (PubMed/PMC)|   | • PersianMedicalTypographyLinter      |
| • Strict Vancouver Order of Appearance|   | • DocxBuilder (Styled Word Generator) |
+---------------------------------------+   +---------------------------------------+
```

---

<a name="master-release-gate-43-criteria"></a>
### Master Release Gate (43 Production Criteria)

The engine enforces 43 fail-closed release criteria before generating or approving proposals:
1. Static analysis leakage audit: 0 hardcoded biological entities in core scripts (`test_hard_code_leakage.py`).
2. Two-Loop Research Dossier immutability and pass/fail sealing.
3. 28 canonical Pajooheshyar section completeness.
4. Mandatory mathematical sample size formulas (Cohen's $d$, Mead's Equation, Cochran).
5. 100% Native OMML XML generation without raw LaTeX delimiter leakage.
6. 100% Vancouver citation re-indexing by appearance order.
7. Zero tolerance for orphaned claims or unreferenced citations.

---

<a name="unified-multi-tier-test-harness"></a>
### Unified Multi-Tier Test Harness

The engine includes 20 comprehensive test suites with **440 / 440 tests passing (100% Pass Rate)**:

```powershell
uv run python tests/run_all_tests.py
```

- **Suite 1: Static Analysis Hard-Code Leakage Audit (`test_hard_code_leakage.py`)** - Zero hardcoded biological entities.
- **Suite 2: Two-Loop Dossier & Master Pipeline Suite (`test_two_loop_dossier.py`)** - E2E verification of research dossier, epistemic auditor, and orchestrator.
- **Suite 3: Multi-Domain Generalization Suite (`test_generalization.py`)** - Validates across 12 distinct biomedical domains.
- **Suite 4: Adversarial Stress Scenarios & Negative Rejection Tests (`test_adversarial_scenarios.py`)** - 114 stress tests.
- **Suite 5: Mutation Testing Layer (`test_mutations.py`)** - 10 deliberate scientific defects with 100% kill score.
- **Suites 6–20:** Property invariants, schema audits, EQUATOR compliance, RoB-2 mitigation, OMML math engines, and typography linters.

---

<a name="فارسی"></a>
## مستندات فارسی (نسخه ۱۱.۰)

پلتفرم **پروپوزال‌نویسی (Proposal-Nevisi نسخه ۱۱.۰)** یک سیستم خودکار، پیشرفته و مبتنی بر شواهد واقعی (Evidence-Driven) برای تدوین پروپوزال‌های پژوهشی علوم پزشکی، داروسازی، دندان‌پزشکی و زیست‌پزشکی مطابق با استاندارد رسمی معاونت پژوهشی و سامانه **پژوهشیار** است.

نسخه ۱۱.۰ با معرفی **معماری خودکار دو حلقه‌ای (Two-Loop Research Architecture)** و **پرونده پژوهش پلمپ‌شده (`ProposalResearchDossier`)**، مشکل همیشگی هوش‌های مصنوعی در ساخت مقالات نامعتبر یا اکتفا به چکیده (Abstract-Only) را به صورت زیرساختی حل کرده است.

### قابلیت‌های کلیدی نسخه ۱۱.۰:

1. **معماری خودکار دو حلقه‌ای (Two-Loop Architecture):**
   - **حلقه درونی (Inner Optimization Loop):** جستجوی زنده در PubMed و Europe PMC، دانلود خودکار متن کامل (Full-Text XML)، استخراج گزیده‌های مستند، واکاوی تناقضات مقالات و پلمپ غیرقابل تغییر پرونده پژوهش (`PROPOSAL_RESEARCH_DOSSIER.json` و `.md`).
   - **حلقه بیرونی (Outer Synthesis Loop):** نگارش دقیق و گام‌به‌گام ۲۸ بخش مصوب دانشگاه‌های علوم پزشکی ایران منحصراً بر اساس شواهد موجود در پرونده پلمپ‌شده، بدون کوچک‌ترین توهم ذهنی (Hallucination-Free).
2. **ممیز دقت اپیستمیک ۶ بعدی (`EpistemicRigorAuditor`):**
   - اعتبارسنجی فرضیه پوچ ($H_0$)، استنادهای متنی با DOI/PMID واقعی، همسویی روش‌شناختی، تعیین دقیق مرزهای تعمیم‌پذیری، حل شواهد متناقض و احراز هویت منابع زیستی (پروفایلینگ STR رده‌های سلولی و استانداردهای خلوص).
3. **ممیزی‌های سه‌گانه داوری گرنت و استانداردهای بین‌المللی:**
   - **داوری شبیه‌سازی‌شده گرنت (Mock Grant Review):** نمره‌دهی ۱ تا ۹ طبق استاندارد NIH و داوری پیش از ارسال به شورای پژوهشی.
   - **انطباق با شبکه گایدلاین‌های جهانی EQUATOR:** پشتیبانی خودکار از ARRIVE 2.0 (حیوانات آزمایشگاهی)، MIQE (آزمایش‌های RT-qPCR)، CONSORT 2010 (کارآزمایی بالینی) و STROBE (مطالعات مشاهده‌ای).
   - **مهار پیش‌دستانه سوگیری (RoB-2 / SYRCLE):** ارزیابی و مهار خطاهای تصادفی‌سازی، کورسازی و خروج از مطالعه.
4. **فرمول‌های ریاضی بومی ورد (Native OMML):**
   - درج تمامی فرمول‌های تعیین حجم نمونه (کوهن، رابطه منابع مید $E = N - B - T$، کوکران) به صورت فرمول‌های واقعی و استاندارد ورد مایکروسافت بدون نشت کدهای لاتک خام (`$...$`).
5. **لینتر تایپوگرافی پزشکی فارسی:**
   - رعایت دقیق نیم‌فاصله (ZWNJ)، فارسی‌سازی ارقام در متن، و باز کردن نام اختصاری اصطلاحات پزشکی در نخستین کاربرد.

---

### راهنمای اجرای سریع (خط فرمان)

اجرای کامل پایپ‌لاین تحقیق و نگارش پروپوزال با یک دستور واحد:

```powershell
uv run python scripts/run_research_pipeline.py --topic "عنوان کامل پژوهش شما" --output-dir "./output"
```

در صورت تمایل به تعیین کلمات کلیدی تخصصی MeSH یا خانواده طراحی مطالعه:
```powershell
uv run python scripts/run_research_pipeline.py `
  --topic "بررسی اثر هم‌افزایی متفورمین و کورکومین بر مهار رشد سلول‌های سرطان کولون HCT116" `
  --keywords "Metformin, Curcumin, Colonic Neoplasms, Apoptosis" `
  --study-family "in_vitro" `
  --output-dir "./output"
```

#### اسناد خروجی تولیدشده در پوشه خروجی:
1. `proposal.docx`: فایل نهایی Word پروپوزال شامل ۲۸ بخش کامل پژوهشیار، فرمول‌های OMML، جداول متغیرها و صفحه امضا.
2. `proposal.md`: متن کامل پروپوزال به فرمت مارک‌داون.
3. `PROPOSAL_RESEARCH_DOSSIER.json` و `.md`: پرونده شواهد پلمپ‌شده شامل قطعات استخراج‌شده از متن کامل مقالات.
4. `MOCK_GRANT_REVIEW_REPORT.md` و `.json`: کارنامه داوری گرنت و نقاط قوت و ضعف روش‌شناسی.
5. `EQUATOR_COMPLIANCE_AUDIT.md` و `.json`: کارنامه انطباق با گایدلاین‌های بین‌المللی پژوهش.
6. `RISK_OF_BIAS_MITIGATION_REPORT.md` و `.json`: جدول جامع مهار سوگیری‌های مطالعاتی.

---

### ۲۸ بخش مصوب سامانه پژوهشیار (وزارت بهداشت)

۱. عنوان فارسی  
۲. بیان مسئله  
۳. مرور بر منابع (پیشینه پژوهش با تحلیل نقادانه و ونکوور ترتیبی)  
۴. اهمیت و ضرورت تحقیق  
۵. تعریف واژه‌ها  
۶. اهداف جزئی  
۷. اهداف کلی  
۸. اهداف کاربردی  
۹. فرضیات پژوهش  
۱۰. سوالات پژوهش  
۱۱. نوع مطالعه  
۱۲. روش جمع‌آوری اطلاعات  
۱۳. روش نمونه‌گیری  
۱۴. جامعه پژوهش  
۱۵. محیط پژوهش  
۱۶. حجم نمونه و نحوه محاسبه آن (با فرمول‌های ریاضی استاندارد)  
۱۷. مشخصات ابزار گردآوری اطلاعات  
۱۸. روایی و پایایی ابزار  
۱۹. روش کار و مراحل آزمایشگاهی / بالینی  
۲۰. روش تجزیه و تحلیل داده‌ها (آمار توصیفی و استنباطی با کنترل خطای نوع اول)  
۲۱. ملاحظات اخلاقی و کدهای اخلاق  
۲۲. پیش‌بینی محدودیت‌های تحقیق و راهکارهای مهار آن  
۲۳. جدول متغیرها (مستقل، وابسته، مخدوش‌کننده، مقیاس و نقش)  
۲۴. جدول زمان‌بندی و گانت چارت مراحل اجرا  
۲۵. فهرست هزینه‌ها و بودجه‌بندی  
۲۶. محل اجرای طرح و همکاران  
۲۷. سازمان‌های بهره‌بردار از نتایج طرح  
۲۸. منابع و مآخذ (فهرست کامل منابع معتبر به شیوه ونکوور ترتیبی)

---

### وضعیت آزمون‌های کنترل کیفیت نرم‌افزاری

سیستم دارای ۲۰ سوئیت آزمون مستقل با **۴۴۰ تست فعال** است که همگی با **۱۰۰٪ قبولی** پاس می‌شوند:

```powershell
uv run python tests/run_all_tests.py
```

- **تست ضد نشت و تعمیم‌پذیری کامل (`test_hard_code_leakage.py`):** صفر بودن کلمات سخت‌کدشده زیستی در اسکریپت‌ها.
- **تست پلمپ پرونده شواهد (`test_two_loop_dossier.py`):** بررسی تغییرناپذیری شواهد پس از پلمپ.
- **تست‌های خصمانه و جهش نرم‌افزاری (`test_adversarial_scenarios.py` و `test_mutations.py`):** کشتن ۱۰۰٪ جهش‌های عمدی در منطق بیولوژیک.

---

## مجوز (License)
این پروژه تحت مجوز [MIT License](LICENSE) منتشر شده است.
