# Proposal-Nevisi 🔬📄
### Evidence-Driven Deep Literature Research Engine & Academic Proposal Generator (v4.5)
### موتور پژوهش عمیق متون علمی و نگارش پروپوزال‌های پژوهشی علوم پزشکی

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Audit Suite: 34/34 Passed](https://img.shields.io/badge/Audit%20Suite-34%2F34%20Passed-success.svg)](#34-test-behavioral-self-audit-suite)
[![PRISMA 2020 Compliant](https://img.shields.io/badge/PRISMA-2020%20Compliant-orange.svg)](#15-stage-evidence-funnel)

---

> **Language / زبان:** [English](#english) | [فارسی](#فارسی)

---

<a name="english"></a>
## English Documentation

**Proposal-Nevisi** is an autonomous, publication-grade academic research proposal drafting framework and **Evidence-Driven Deep Literature Research Engine (v3.0)** tailored for medical, biomedical, and life science research protocols.

Unlike conventional retrieval agents that rely on superficial keyword searches and arbitrary paper limits, Proposal-Nevisi executes an end-to-end **15-Stage Evidence Funnel** across four major biomedical graph engines, enforces claim-level sentence provenance, performs claim-evidence entailment audits, and compiles beautifully formatted Microsoft Word documents adhering to native Arabic/Persian Right-to-Left (RTL) typography.

---

### Core Architectural Principles (v3.0)

1. **No Arbitrary Final-Paper Cap (Emergent Evidence Set):**
   - No hardcoded limits (e.g., neither fixed "15" nor "20" papers).
   - Reference volume emerges organically from the factual claims required in the proposal.
   - Every included citation must possess a designated evidentiary role (`Primary_efficacy`, `Mechanism`, `Model_justification`, `Methodology_standard`, `Safety_toxicity`, `Background_landscape`, `Contradictory_context`, `Gap_identification`) to completely prevent citation spamming.

2. **Multi-Database Literature Harvesting (Tier 1 & Tier 2):**
   - **PubMed / MEDLINE:** MeSH descriptors and Supplementary Concept Records combined with free-text words.
   - **Europe PMC:** Open access full-text XML retrieval via REST services.
   - **OpenAlex:** Global scholarly graph exploration, citation metrics, and related works mapping.
   - **Crossref:** Comprehensive metadata and DOI resolution across major commercial publishers.

3. **Strict 3-Tier Source Classification:**
   - **Tier A (Verified Full-Text XML > 1,000 chars):** PMC Open Access XML or Europe PMC FullText XML. Strictly required for all quantitative parameters (IC50, dosage, incubation time) and direct mechanistic claims. *Abstracts are never counted as full text!*
   - **Tier B (Screened Abstract & Metadata):** Validated for landscape, contextual, epidemiology, and background claims.
   - **Tier C (Discovered Citation Lead):** Logged in the registry but excluded from synthesis unless upgraded.

4. **Dedicated Contradictory & Safety Evidence Branch:**
   - Targeted query strings specifically discovering antagonism, biological resistance, viral neutralization, host barriers, and off-target cytotoxicity.
   - Outputs a dedicated assessment document: `CONTRADICTORY_EVIDENCE.md`.

5. **Saturation-Based Citation Chaining:**
   - Backward references, forward citations, and OpenAlex related works graphs.
   - Stopping rule based on marginal yield threshold ($\Delta < 2$ newly eligible records per iteration) rather than arbitrary iteration cutoffs.

6. **Zero Hardcoded Biochemical Fallbacks:**
   - Real-time live API verification with **PubChem** (compound CID, SMILES, IUPAC) and **Reactome** (host signaling pathways).
   - If an API or network fails, the status is explicitly logged as `UNVERIFIED`—synthetic boilerplate or fabricated values are strictly forbidden.

7. **Bounded Novelty Phrasing Policy:**
   - Absolute, ungrounded claims like *"This is the first study ever"* or *"ثابت می‌کند"* are strictly banned.
   - All novelty statements are bound by the documented search perimeter:  
     > *"No directly matching study evaluating the simultaneous combination of [Intervention 1] and [Intervention 2] in the [Target Model] was identified within the documented search boundary (PubMed, Europe PMC, OpenAlex, Crossref; 2020–2026)."*

8. **Master Word Typography & RTL Bidi XML:**
   - High-grade Persian academic typography using the `Dubai` font family.
   - Native OpenXML Right-to-Left bidirectional tags (`<w:bidi/>`, `<w:rtlGutter/>`).
   - Complex Script bolding (`<w:bCs/>`) for Persian headings.
   - Complete elimination of disruptive horizontal dividers (`---`).
   - Direct Word Citation Manager integration via COM automation.

---

### The 15-Stage Evidence Funnel

```text
Research Question
        ↓
Evidence Questions (12 Categories: EQ01 - EQ12)
        ↓
Concept / Synonym Expansion (MeSH & Controlled Vocabularies)
        ↓
Search Facets (Disease, Interventions, Combination, Mechanisms, Models)
        ↓
Multi-Database Retrieval (PubMed, Europe PMC, OpenAlex, Crossref)
        ↓
Contradictory / Negative Evidence Search Branch
        ↓
Canonical Deduplication (DOI, PMID, Normalized Title)
        ↓
Title & Abstract Screening (Explicit Audit Trail)
        ↓
Full-Text Retrieval & Strict 3-Tier Classification
        ↓
Saturation-Based Citation Chaining (Backward, Forward, Related Works)
        ↓
Claim-Level Evidence Extraction (Verbatim Quotes, Strict NR Policy)
        ↓
Evidence Gap Matrix (EQ01 - EQ12 Systematic Audit)
        ↓
Claim-Evidence Entailment Mapping (Formal Semantic Audit)
        ↓
Emergent Citation Selection (No Arbitrary Cap + Designated Evidentiary Roles)
        ↓
Academic Proposal Writing & Master Word Document Compilation
```

---

### Repository Structure

```text
proposal-nevisi/
├── SKILL.md                          # Full skill definition and agent instructions
├── README.md                         # Bilingual documentation (English & Persian)
├── LICENSE                           # MIT License
├── .gitignore                        # Git exclusion rules
├── references/                       # Reference protocols and style guides
│   ├── deep_research_protocol.md     # 15-stage Deep Literature Research Protocol
│   ├── ai_detection_checklist.md     # 6-layer anti-AI academic humanization checklist
│   └── proposal_template_structure.md# 14 mandatory Iranian medical proposal sections
└── scripts/                          # Executable Python pipeline engines
    ├── multi_db_searcher.py          # 4-DB discovery, screening, and saturation chaining
    ├── evidence_ledger_builder.py    # Evidence ledger, claim entailment, and gap matrix builder
    ├── self_audit_suite.py           # 18-test integrity and semantic verification suite
    ├── docx_builder.py               # Markdown-to-Word converter with Dubai RTL typography
    ├── citation_injector.py          # Word Citation Manager COM injector
    ├── citation_checkpoint.py        # NCBI verification and in-text citation auditor
    └── pubmed_searcher.py            # Focused PubMed E-utilities search and fetcher
```

---

### Artifact Suite Generated During Execution

| Artifact File | Description & Purpose |
| :--- | :--- |
| **`SEARCH_QUERY_LOG.json`** | Exact query strings sent to all 4 engines with HTTP status codes and hit counts. |
| **`SEARCH_BOUNDARY.json`** | Formal declaration of search databases, date window, filters, and bounded novelty claim. |
| **`SOURCE_REGISTRY.json`** | Comprehensive database of all discovered sources classified into Tier A, Tier B, and Tier C. |
| **`EXCLUDED_STUDIES.json`** | Full audit trail of excluded candidate studies with granular exclusion rationales. |
| **`CONTRADICTORY_EVIDENCE.md`** | Dedicated evaluation of biological barriers, antagonism risks, and toxicity limits. |
| **`EVIDENCE_GAP_MATRIX.md`** | Systematic gap analysis across all 12 Evidence Question categories (EQ01–EQ12). |
| **`CLAIM_EVIDENCE_MAP.json`** | Bidirectional mapping between claims and evidence with formal entailment ratings. |
| **`EVIDENCE_LEDGER.json`** | Claim ledger with granular quantitative parameters and exact verbatim text quotes. |
| **`LITERATURE_SEARCH_REPORT.md`** | Official PRISMA 2020 search audit report with screening funnel statistics. |
| **`LITERATURE_DEEP_RESEARCH.md`** | Dynamic evidence dossier tagged with explicit Epistemic Status headers. |
| **`references_with_fulltext.json`**| Final emergent evidence dataset with full metadata and verified text. |
| **`EndNote_Citations.enw`** | Formatted library for EndNote reference manager import. |
| **`references_library.ris`** | Formatted RIS library for Mendeley, Zotero, and Papers import. |

---

### Quick Start (CLI)

```bash
# 1. Install prerequisites
pip install python-docx pywin32

# 2. Run 4-Database Literature Harvester & Screener
python scripts/multi_db_searcher.py --output_json references_with_fulltext.json --audit_report LITERATURE_SEARCH_REPORT.md

# 3. Build Evidence Ledger, Claim Entailment Map & Gap Matrix
python scripts/evidence_ledger_builder.py --json_in references_with_fulltext.json --ledger_out EVIDENCE_LEDGER.json --dossier_out LITERATURE_DEEP_RESEARCH.md

# 4. Run Comprehensive 18-Test Self-Audit Suite
python scripts/self_audit_suite.py .

# 5. Compile Master Word Document with Dubai Typography
python scripts/docx_builder.py proposal_source.md output_proposal.docx
```

---
---

<a name="فارسی"></a>
## راهنمای فارسی (Persian Documentation)

مهارت **Proposal-Nevisi (نسخه ۳.۰)** یک دستیار خودکار، تخصصی و تعاملی برای تدوین و ارتقای پروپوزال‌های پژوهشی علوم پزشکی و زیست‌پزشکی در بالاترین تراز آکادمیک است که مجهز به **موتور پژوهش عمیق متون علمی مبتنی بر شواهد پدیدارشده (Evidence-Driven Deep Research Engine)** می‌باشد.

---

### اصول کلیدی و خطوط قرمز علمی (نسخه ۳.۰)

1. **قاعده قطعی عدم سقف ساختگی در تعداد منابع (No Arbitrary Final-Paper Cap):**
   - هیچ محدودیت از پیش‌تعیین‌شده و قراردادی (مانند ۱۵ یا ۲۰ مقاله) در انتخاب منابع نهایی وجود ندارد.
   - تعداد منابع نهایی به صورت **پدیدارشده (Emergent)** و دقیقاً متناسب با ادعاهای علمی مطرح‌شده در متن پروپوزال تعیین می‌گردد.
   - برای جلوگیری از اسپم استنادی، هر منبعی که وارد پروپوزال می‌شود باید دارای یک نقش استنادی صریح (`Primary_efficacy`, `Mechanism`, `Model_justification`, `Methodology_standard`, `Safety_toxicity`, `Background_landscape`, `Contradictory_context`, `Gap_identification`) باشد.

2. **بازیابی چندپایگاهی ادبیات (Multi-Database Retrieval):**
   - جست‌وجوی همزمان در ۴ پایگاه معتبر بین‌المللی:
     - **PubMed (MeSH):** بهره‌گیری از اصطلاحات کنترل‌شده توصیف‌گر MeSH و رکوردهای تکمیلی NLM.
     - **Europe PMC:** واکشی مقالات تمام‌متن آزاد (Open Access XML) از طریق REST API.
     - **OpenAlex:** کشف گراف استنادی جهانی، شاخص‌های ارجاعی و آثار مرتبط (Related Works).
     - **Crossref:** بازیابی متادیتا و شناسه‌های DOI رسمی ناشران تجاری.

3. **سطح‌بندی سه‌گانه منابع (3-Tier Classification):**
   - **Tier A (تمام‌متن تأییدشده PMC OA XML / Europe PMC XML بالای ۱۰۰۰ کاراکتر):** منحصراً برای استخراج داده‌های کمی (IC50، دوزها، زمان انکوباسیون) و شواهد مکانیسمی مستقیم. *چکیده مقاله هرگز تمام‌متن تلقی نمی‌شود.*
   - **Tier B (چکیده و متادیتای تأییدشده):** جهت تبیین بستر پژوهش، اپیدمیولوژی، و شواهد زمینه‌ای.
   - **Tier C (سرنخ‌های اولیه بدون متن کامل):** در رجیستری منابع ثبت می‌شود اما وارد استخراج کمی نمی‌گردد.

4. **شاخه اختصاصی شواهد متناقض و موانع ایمنی (Contradictory Evidence Branch):**
   - کوئری‌های هدفمند برای کشف پدیده‌های آنتاگونیسم (Antagonism)، مقاومت‌های دارویی/ویروسی، و سمیت‌های فراتر از پنجره درمانی.
   - تولید سند رسمی `CONTRADICTORY_EVIDENCE.md` جهت اتخاذ تدابیر کنترلی در متدولوژی طرح.

5. **زنجیره استنادی اشباع‌محور (Saturation Citation Chaining):**
   - پیمایش مراجع گذشته‌نگر، استنادهای آینده‌نگر و گراف مقالات مرتبط OpenAlex با توقف خودکار بر اساس قاعده بازده نهایی حاشیه‌ای ($\Delta < 2$).

6. **سیاست قطعی عدم داده‌های ساختگی (Zero Fallbacks):**
   - استعلام زنده مشخصات فیزیکوشیمیایی ترکیبات از پایگاه **PubChem**.
   - استعلام زنده مسیرهای سیگنالینگ از پایگاه **Reactome**.
   - در صورت خطای شبکه یا پایگاه داده، وضعیت به صورت `UNVERIFIED` ثبت شده و از درج داده‌های ساختگی اکیداً خودداری می‌شود.
   - استخراج پارامترها با نقل‌قول مستقیم درون‌متنی و ثبت قطعی `NR` (Not Reported) در صورت عدم گزارش.

7. **بیان اصالت مقید به مرز مستند (Strict Novelty Policy):**
   - ادعاهای مطلق و غیرعلمی مانند «برای اولین بار» یا «اثبات می‌کند» ممنوع است.
   - نوآوری منحصراً در چارچوب مرز جست‌وجوی مستندشده بیان می‌شود:
     > *"تا کنون هیچ مطالعه همزمانی با ارزیابی اثر توأم [مداخله ۱] و [مداخله ۲] در مدل [بیماری هدف] درون مرز جست‌وجوی مستندشده (PubMed, Europe PMC, OpenAlex, Crossref; 2020-2026) یافت نگردید."*

8. **تایپوگرافی مستر ورد (Master Word Typography):**
   - فونت استاندارد `Dubai` با راست‌به‌چپ سراسری (`<w:bidi/>` و `<w:rtlGutter/>`).
   - بومی‌سازی تیترهای فارسی با پررنگ‌سازی Complex Script (`<w:bCs/>`).
   - حذف ۱۰۰٪ خط‌تیره‌های جداکننده مخرّب (`---`).
   - ثبت مستقیم منابع در **Word Citation Manager** از طریق اتوماسیون COM بدون ارور Unreadable Content.

---

### ابعاد ۱۲ گانه سوالات شواهد (EQ01 تا EQ12)

در سند `EVIDENCE_GAP_MATRIX.md`، تمامی ابعاد زیر به صورت نظام‌مند ارزیابی می‌شوند:
- **EQ01:** انکولوژی مستقیم، سمیت سلولی و مقادیر IC50
- **EQ02:** کسکیدهای پیام‌رسانی مولکولی و مسیرهای آپوپتوز
- **EQ03:** متدولوژی هم‌افزایی و ضابطه تصمیم‌گیری چو-تالالی (CI Theorem)
- **EQ04:** مدل‌های سلولی و حیوانی (رده‌های سلولی و موش‌های سینژنیک)
- **EQ05:** شاخص درمانی، پنجره دوز ایمن و ارزیابی سمیت بافتی
- **EQ06:** دارورسانی، فارماکوکینتیک و کنترل حلال DMSO زیر ۰.۱٪
- **EQ07:** موانع مقاومت زیستی و تداخل‌های آنتاگونیستی
- **EQ08:** سینتیک تکثیر و انکولیز ویروسی
- **EQ09:** ریزمحیط تومور و القای مرگ سلولی ایمونوژنیک (ICD)
- **EQ10:** بیومارکرهای پیش‌بینی‌کننده حساسیت و پاسخ به درمان
- **EQ11:** ترجمان بالینی و چشم‌انداز کاربرد انسانی
- **EQ12:** استانداردهای متدولوژیک آزمایشگاهی (آزمون MTT و فلوسایتومتری)

---

### آزمون جامع ۱۸ گانه خود-ممیزی (18-Test Self-Audit Suite)

اسکریپت `scripts/self_audit_suite.py` تمامی ۱۸ ضابطه زیر را به صورت خودکار ممیزی می‌کند:
1. پوشش ۴ پایگاه داده (PubMed, Europe PMC, OpenAlex, Crossref)
2. شفافیت لاگ کوئری‌ها در `SEARCH_QUERY_LOG.json`
3. ثبت رسمی مرز جست‌وجو در `SEARCH_BOUNDARY.json`
4. اصالت رجیستری و طبقه‌بندی Tier A, B, C در `SOURCE_REGISTRY.json`
5. مستندسازی شفاف علل حذف در `EXCLUDED_STUDIES.json`
6. عدم وجود سقف ساختگی در تعداد منابع (پدیدارشدن منابع از دل شواهد)
7. ثبت شاخص‌های اشباع زنجیره استنادی
8. ارزیابی ریسک در شاخه شواهد متناقض (`CONTRADICTORY_EVIDENCE.md`)
9. تکمیل ماتریس خلأهای شواهد در ۱۲ حوزه (`EVIDENCE_GAP_MATRIX.md`)
10. ممیزی استلزام معنایی ادعاها (`CLAIM_EVIDENCE_MAP.json`)
11. حذف ۱۰۰٪ پیش‌فرض‌های هاردکد در کدهای اجرایی
12. رعایت سیاست نوآوری مقید و حذف مبالغه‌های غیرعلمی
13. نقل‌قول‌های مستقیم متنی بدون عبارات ساختگی
14. استعلام زنده پارامترهای شیمیایی از PubChem
15. استعلام زنده مسیرهای سیگنالینگ از Reactome
16. تخصیص نقش استنادی صریح برای تمامی مراجع نهایی
17. استانداردهای تایپوگرافی مستر ورد (دبی + RTL + bCs + بدون '---')
18. انطباق سرتاسری شناسه‌های مقالات در تمامی اسناد خروجی

---

### لایسنس (License)

این پروژه تحت مجوز بین‌المللی **MIT License** منتشر شده است.
