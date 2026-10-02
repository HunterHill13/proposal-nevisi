# Proposal-Nevisi (مهارت جامع نگارش پروپوزال‌های پژوهشی علوم پزشکی و موتور Deep Research 3.0)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Audit Suite: 18/18 Passed](https://img.shields.io/badge/Audit%20Suite-18%2F18%20Passed-success.svg)](#18-test-self-audit-suite)
[![PRISMA 2020 Compliant](https://img.shields.io/badge/PRISMA-2020%20Compliant-orange.svg)](#evidence-driven-literature-funnel)

یک مهارت جامع، دقیق و تعاملی برای تدوین پروپوزال‌های پژوهشی علوم پزشکی و زیست‌پزشکی مطابق با بالاترین استانداردهای دانشگاهی و وزارت بهداشت، درمان و آموزش پزشکی ایران. این سیستم مجهز به **موتور اختصاصی Deep Research 3.0 مبتنی بر شواهد پدیدارشده (Evidence-Driven)**، بازیابی ۴ پایگاهی، ممیزی استلزام ادعا-شواهد (Claim-Evidence Entailment)، و نگارش انسان‌محور ضد هوش مصنوعی می‌باشد.

---

## ویژگی‌های کلیدی (Key Features v3.0)

1. **معماری ۱۵ مرحله‌ای بازیابی و استخراج شواهد (15-Stage Evidence Funnel):**
   - تبدیل خودکار عنوان به ۱۲ حوزه سوالات شواهد (EQ01 تا EQ12).
   - گسترش مفاهیم با اصطلاحات کنترل‌شده MeSH در شبکه NLM.
   - جست‌وجوی همزمان در ۴ پایگاه بین‌المللی: **PubMed** (MeSH)، **Europe PMC** (REST API)، **OpenAlex** (Graph API) و **Crossref** (Works API).
   - شاخه اختصاصی کشف شواهد متناقض (Contradictory / Negative Evidence) جهت ارزیابی ریسک‌های آنتاگونیسم، مقاومت و سمیت.
   - زنجیره استنادی اشباع‌محور (Saturation Citation Chaining) با پایش مراجع گذشته‌نگر، استنادهای آینده‌نگر و گراف مقالات مرتبط.

2. **قاعده قطعی عدم سقف ساختگی در تعداد منابع (No Arbitrary Final-Paper Cap):**
   - هیچ سقف ثابت و قراردادی (مانند ۱۵ یا ۲۰ مقاله) برای تعداد مراجع نهایی وجود ندارد.
   - منابع به صورت **پدیدارشده (Emergent)** و متناسب با ادعاهای علمی پروپوزال گزینش می‌شوند.
   - هر منبع دارای نقش استنادی مشخص (`Primary_efficacy`, `Mechanism`, `Model_justification`, `Methodology_standard`, `Safety_toxicity`, `Background_landscape`, `Contradictory_context`, `Gap_identification`) جهت پیشگیری از اسپم استنادی است.

3. **سطح‌بندی سه‌گانه منابع (Strict 3-Tier Source Classification):**
   - **Tier A (تمام‌متن تأییدشده PMC OA XML / Europe PMC XML > 1000 کاراکتر):** منحصراً برای استخراج پارامترهای کمی (دوز، IC50، زمان انکوباسیون) و شواهد مکانیسمی مستقیم. (چکیده هرگز متن کامل محسوب نمی‌شود).
   - **Tier B (چکیده و متادیتای تأییدشده):** برای تبیین بستر پژوهش، اپیدمیولوژی، و شواهد زمینه‌ای.
   - **Tier C (سرنخ‌های اولیه بدون متن کامل):** در رجیستری منابع ثبت شده اما وارد استخراج کمی نمی‌شوند.

4. **سیاست قطعی عدم داده‌های ساختگی (Zero Hallucination & Zero Fallbacks):**
   - استعلام زنده مشخصات فیزیکوشیمیایی ترکیبات از پایگاه **PubChem**.
   - استعلام زنده مسیرهای سیگنال‌دهی سلولی از پایگاه **Reactome**.
   - در صورت عدم پاسخ‌دهی سرورها، وضعیت منحصراً به صورت `UNVERIFIED` ثبت شده و از درج داده‌های ساختگی خودداری می‌شود.
   - استخراج پارامترها با نقل‌قول مستقیم درون‌متنی و ثبت قطعی `NR` (Not Reported) در صورت عدم گزارش.

5. **بیان اصالت مقید به مرز مستند (Strict Novelty Policy):**
   - ممنوعیت عبارات غیرعلمی و نامقید مانند «برای اولین بار» یا «اثبات می‌کند».
   - تعریف دقیق مرز جست‌وجو در `SEARCH_BOUNDARY.json` و مقیدسازی نوآوری به مرز مستندشده.

6. **تایپوگرافی مستر ورد (Master Word Typography):**
   - فونت استاندارد `Dubai` با راست‌به‌چپ سراسری (`<w:bidi/>` و `<w:rtlGutter/>`).
   - بومی‌سازی تیترهای فارسی با پررنگ‌سازی Complex Script (`<w:bCs/>`).
   - حذف ۱۰۰٪ خط‌تیره‌های جداکننده مخرّب (`---`).
   - ثبت مستقیم منابع در **Word Citation Manager** از طریق اتوماسیون COM بدون بروز خطای Unreadable Content.

7. **آزمونگر سخت‌گیرانه ۱۸ گانه خود-ممیزی (18-Test Self-Audit Suite):**
   - ممیزی خودکار تمامی ابعاد پوشش پایگاه‌ها، شفافیت لاگ، اصالت رجیستری، استلزام معنایی، و تایپوگرافی.

---

## ساختار مخزن و اسکریپت‌ها (Repository Structure)

```text
proposal-nevisi/
├── SKILL.md                          # سند جامع دستورالعمل و استانداردهای مهارت
├── README.md                         # مستندات و راهنمای کاربری مخزن
├── .gitignore                        # فایل‌های نادیده‌گرفته‌شده در گیت
├── references/                       # راهنماها و پروتکل‌های مرجع
│   ├── deep_research_protocol.md     # پروتکل ۱۵ مرحله‌ای پژوهش عمیق متون علمی
│   ├── ai_detection_checklist.md     # چک‌لیست ۶ لایه‌ای نگارش انسان‌محور ضد AI
│   └── proposal_template_structure.md# ساختار ۱۴ بخش استاندارد پروپوزال دانشگاهی
└── scripts/                          # موتورها و اسکریپت‌های اجرایی پایتون
    ├── multi_db_searcher.py          # موتور بازیابی ۴ پایگاهی، غربالگری و زنجیره اشباع
    ├── evidence_ledger_builder.py    # سازنده دفتر کل شواهد، ممیزی استلزام و ماتریس خلأها
    ├── self_audit_suite.py           # آزمونگر خودکار ۱۸ گانه ممیزی و راستی‌آزمایی شواهد
    ├── docx_builder.py               # مبدل حرفه‌ای Markdown به Word با تایپوگرافی دبی
    ├── citation_injector.py          # ثبت پاکیزه مراجع در نرم‌افزار Word با پروتکل COM
    ├── citation_checkpoint.py        # ممیز اصالت مراجع در NCBI و پوشش استنادهای درون‌متنی
    └── pubmed_searcher.py            # واکشی تخصصی چکیده‌ها و متادیتا از PubMed E-utilities
```

---

## اسناد و پرونده‌های شواهد تولیدشده (Artifact Suite)

پس از اجرای کامل فرآیند، اسناد زیر در ریشه پروژه تولید و ممیزی می‌شوند:

| نام سند | شرح و هدف سند |
| :--- | :--- |
| **`SEARCH_QUERY_LOG.json`** | لاگ شفاف تک‌تک کوئری‌های ارسالی به ۴ پایگاه با کد وضعیت HTTP و زمان پاسخ |
| **`SEARCH_BOUNDARY.json`** | تعریف رسمی مرز جست‌وجو (پایگاه‌ها، تاریخ، فیلترها) و بیانیه نوآوری مقید |
| **`SOURCE_REGISTRY.json`** | رجیستری جامع تمام منابع کشف‌شده به همراه Tier و وضعیت غربالگری |
| **`EXCLUDED_STUDIES.json`** | مستندسازی شفاف مقالات حذف‌شده در غربالگری عنوان/چکیده با ذکر علت |
| **`CONTRADICTORY_EVIDENCE.md`** | تحلیل شواهد متناقض، ریسک آنتاگونیسم، موانع ایمنی و پنجره غلظت ایمن |
| **`EVIDENCE_GAP_MATRIX.md`** | ماتریس تحلیل خلأهای شواهد در ۱۲ حوزه کلیدی (EQ01 تا EQ12) |
| **`CLAIM_EVIDENCE_MAP.json`** | نقشه استلزام معنایی ادعاها با رتبه‌های استاندارد (`DIRECTLY_SUPPORTED` و ...) |
| **`EVIDENCE_LEDGER.json`** | دفتر کل شواهد آزمایشگاهی با پارامترهای کمی و نقل‌قول‌های مستقیم متنی |
| **`LITERATURE_SEARCH_REPORT.md`** | گزارش ممیزی فرآیند جست‌وجو مطابق با فلوچارت PRISMA 2020 |
| **`LITERATURE_DEEP_RESEARCH.md`** | پرونده تحلیلی شواهد عمیق با برچسب‌های Epistemic Status و سنتز پویا |
| **`references_with_fulltext.json`** | پایگاه داده مقالات نهایی منتخب همراه با متن کامل و متادیتا |
| **`EndNote_Citations.enw`** | خروجی استاندارد کتابخانه مراجع برای EndNote |
| **`references_library.ris`** | خروجی استاندارد کتابخانه مراجع برای Mendeley و Zotero |

---

## نحوه اجرا و استفاده (Quick Start)

### پیش‌نیازها
- پایتون نسخه ۳.۱۰ به بالا
- بسته‌های `python-docx` و `pywin32` (برای اتوماسیون ورد در ویندوز):
```bash
pip install python-docx pywin32
```

### ۱. اجرای موتور بازیابی چندپایگاهی و غربالگری
```bash
python scripts/multi_db_searcher.py --output_json references_with_fulltext.json --audit_report LITERATURE_SEARCH_REPORT.md
```

### ۲. استخراج پارامترها، استلزام ادعاها و تولید پرونده شواهد
```bash
python scripts/evidence_ledger_builder.py --json_in references_with_fulltext.json --ledger_out EVIDENCE_LEDGER.json --dossier_out LITERATURE_DEEP_RESEARCH.md
```

### ۳. اجرای آزمون جامع ۱۸ گانه خود-ممیزی
```bash
python scripts/self_audit_suite.py .
```

### ۴. ساخت فایل Word با فرمت‌بندی مستر
```bash
python scripts/docx_builder.py proposal_source.md output_proposal.docx
```

---

## لایسنس (License)

این پروژه تحت مجوز **MIT License** منتشر شده است.
