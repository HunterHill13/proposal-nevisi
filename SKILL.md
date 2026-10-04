---
name: proposal-nevisi
description: >
  Universal, configuration-driven Iranian medical and biomedical research proposal drafting, deep literature research,
  evidence synthesis, humanization, and Word (.docx) publication engine (v8.1). Operates across diverse biomedical domains
  (oncology, cardiology, infectious diseases, diagnostics, epidemiology, immunology, endocrinology, nephrology, basic experimental science). Generates dynamic
  Research Problem Models (PICO, PECO, Diagnostic, Prognostic, Mechanistic), executes multi-layer dynamic literature searches
  (Layers across PubMed, Europe PMC, OpenAlex, Crossref), produces design-aware Study Evidence Records (STUDY_EVIDENCE_RECORD_SCHEMA),
  maps 22 cross-study relationship types, detects gaps across 18 universal categories, performs study-design-aware comparability and RoB analysis (RoB2, SYRCLE, QUADAS-2, in vitro),
  clusters study families, cohorts, and trial registries to prevent evidence double-counting (NON_INDEPENDENT_EVIDENCE),
  resolves contradictions across an extensible 15-category taxonomy (distinguishing TRUE_CONTRADICTION from CONTEXTUAL_DISAGREEMENT),
  builds evidence conflict matrices and evaluates alternative explanations, tracks discovery paths in citation chaining,
  enforces epistemic gap bounds and rules ("No Evidence != Evidence of No Effect", "No Synergy Fallacy"),
  enforces 7-level claim entailment and causal language boundaries with sentence-level CLAIM_PROVENANCE_MAP,
  enforces dynamic temporal boundaries with explicit age justification and OUTDATED_DIRECT_EVIDENCE tracking,
  supports living research incremental delta reports, handles sample size uncertainty (SAMPLE_SIZE_REQUIRES_INPUT),
  renders publication-grade 14-section Word proposals with dynamic ethics frameworks, individual reference paragraphs,
  Dubai Persian typography, native RTL bidi XML, and passes a unified 153-assertion test harness
  (Static analysis zero leakage, 9-domain generalization fixtures, 65 adversarial stress tests, and 60-test benchmark).
---

# Proposal-Nevisi (موتور جامع، عمومی و مبتنی بر شواهد نگارش پروپوزال‌های علوم پزشکی v8.1)

این مهارت یک پلتفرم جامع، تعاملی، مستقل از موضوع (Topic-Agnostic) و مبتنی بر شواهد برای تدوین پروپوزال‌های پژوهشی علوم پزشکی و زیست‌پزشکی در بالاترین تراز دانشگاهی و ژورنال‌های بین‌المللی است. نسخه v8.1 با ارتقای عمیق موتور شواهد، به عنوان یک **General-Purpose Evidence-Driven Medical Research Engine** عمل می‌کند که برای تمامی حوزه‌های بالینی، پایه‌ای، دارویی، تشخیصی، قلبی-عروقی، عفونی، اپیدمیولوژیک و انکولوژی با چارچوب‌های استاندارد (PICO, PECO, Diagnostic, Prognostic, Mechanistic) قابل استفاده است.

---

## ۱. چرخه فرآیندی موتور عمومی شواهد (Universal Pipeline)

```text
موضوع و عنوان ورودی پژوهشگر
           │
           ▼
[ ۱. مدل‌سازی پویای مسئله پژوهش (Research Problem Model) ]
├── انتخاب چارچوب متناسب: PICO / PECO / Diagnostic / Prognostic / Mechanistic
├── شناسایی جمعیت/مدل (Human, Animal, Cell Culture, Diagnostic, Epidemiological)
├── اصطلاحات کنترل‌شده MeSH و واژگان تخصصی
           │
           ▼
[ ۲. استراتژی جستجوی پویای ۹ لایه‌ای و اشباع شواهد (9-Layer Search & Saturation) ]
├── لایه‌های نه‌گانه (A: مستقیم، B: اجزاء، C: مکانیسمی، D: مدل، E: ترنسلیشنال، F: ایمنی/سمیت، G: شواهد منفی/پوچ، H: متناقض، I: روش‌شناختی)
├── زنجیره‌سازی استنادی پیش‌رو و پس‌رو (Forward/Backward Citation Chaining)
├── سنجش اشباع شواهد (Search Saturation Assessment: دیمینیشینگ ریترن و کفایت متدولوژیک)
           │
           ▼
[ ۳. بازیابی چندپایگاهی و حسابداری PRISMA 2020 ]
├── بازیابی همزمان از PubMed/MEDLINE, Europe PMC, OpenAlex, Crossref
├── ثبت دقیق لاگ جستجو، حذف موارد تکراری و جریان غربالگری واقعی
           │
           ▼
[ ۴. اعتبارسنجی فیلد-محور کتابشناختی و مرز زمانی ]
├── تطبیق دقیق DOI, PMID, Title, First Author, Journal, Year
├── اعمال قانون زمانی ۶ ساله (Main Evidence >= CURRENT_YEAR - 6)
├── تایید استثناهای بنیادین با توجیه معتبر (FOUNDATIONAL_JUSTIFICATION)
           │
           ▼
[ ۵. طبقه‌بندی طراحی مطالعه و ارزیابی سوگیری متناسب با متدولوژی ]
├── سنجش RoB متناسب: Cochrane RoB2 برای کارآزمایی‌ها، SYRCLE برای حیوانات، QUADAS-2 برای تشخیصی
├── قانون اکید: وضعیت NOT_REPORTED هرگز به LOW_RISK تبدیل نمی‌شود
           │
           ▼
[ ۶. گراف روابط مطالعات و تحلیل شکاف‌های پژوهشی (Study Relationships & Gaps) ]
├── ترسیم روابط بین‌مطالعه‌ای در ۲۲ بعد پویا (DIRECT_REPLICATION, EXTENSION, TRANSLATIONAL_EXTENSION, SUPPORTS, CONTRADICTS, ...)
├── شناسایی نظام‌مند شکاف‌های پژوهشی در ۱۱ طبقه تاکسونومی (KNOWLEDGE_GAP, MECHANISTIC_GAP, POPULATION_GAP, METHODOLOGICAL_GAP, ...)
           │
           ▼
[ ۷. ردیابی خوشه‌های مطالعاتی و ممانعت از دوباره‌شماری (Study Family Clustering) ]
├── شناسایی کارآزمایی‌های مشترک (NCT)، کوهورت‌های اپیدمیولوژیک مشترک و زیرگروه‌ها
├── تفکیک مقالات مروری سیستماتیک از مطالعات اولیه برای جلوگیری از شمارش مضاعف شواهد
           │
           ▼
[ ۸. موتور تحلیل شواهد منفی، تناقضات و واگرایی پارامتری ]
├── رده‌بندی تناقضات در ۱۵ شاخه تاکسونومی و تفکیک TRUE_CONTRADICTION از CONTEXTUAL_DISAGREEMENT
├── تحلیل واگرایی پارامتری (گونه، رده سلولی، دوز، مدت، حامل، روش سنجش)
├── اعمال قواعد معرفت‌شناختی: No Evidence != Evidence of No Effect و No Synergy Fallacy
           │
           ▼
[ ۹. موتور التزام گزاره-شواهد و دروازه زبان علّی (Claim Entailment & Causal Gate) ]
├── تفکیک ادعاهای اتمیک و درجه‌بندی التزام در مقیاس ۷ سطحی
├── مسدودسازی ادعای علیت (Causes/Induces) در مطالعات مشاهده‌ای و همبستگی
├── ره‌گیری کامل مقادیر عددی در دفتر شواهد (EVIDENCE_LEDGER) و ممانعت از توهم اعداد
           │
           ▼
[ ۱۰. سنتز چندبعدی شواهد بدون رای‌گیری اکثریتی ]
├── سنتز وزن‌دهی‌شده بر پایه ۸ بعد قطعیت شواهد (مستقیم بودن، همسویی، دقت، کیفیت، سوگیری، کاربردپذیری، حجم، بار تناقض)
├── ممنوعیت قاطع ساده‌سازی به رای‌گیری اکثریتی (Vote Counting)
           │
           ▼
[ ۱۱. طراحی پروتکل پویا، اعتبارسنجی ساختار و نگارش پروپوزال ۱۴ گانه ]
├── طراحی پویای جدول متغیرها (مستقل، وابسته، مخدوش‌کننده، کوواریات، کنترل)
├── طراحی پویای گانت چارت زمان‌بندی و برنامه جامع تحلیل آماری متناسب با مقیاس متغیرها
├── اعمال دروازه اعتبارسنجی ساختاری ۱۴ گانه (PROPOSAL_STRUCTURE_VALIDATION = PASS/FAIL) با پشتیبانی نیم‌فاصله و ارقام فارسی
├── نگارش کامل یک پاراگراف تفصیلی و مستقل برای تک‌تک مراجع در بخش مرور منابع
├── فرمت‌بندی رسمی با فونت Dubai، تگ‌های native RTL bidi XML و خروجی Word (.docx)
           │
           ▼
[ ۱۲. ممیزی خودکار چندبعدی و دروازه کیفیت پیش از پرواز (9D QA Gate) ]
├── ارزیابی ۹ بعد کیفی نهایی: تمامیت ساختار، ره‌گیری استنادها، استقلال موضوعی، مرز زمانی، کنترل علیت، تعادل تناقض، انسجام متغیرها، دقت آماری و آزمون‌های رفتاری
├── اجرای سوئیت تست یکپارچه ۸۲ تستی با قبولی ۱۰۰٪
```

---

## ۲. اصول و خطوط قرمز علمی مهارت (Non-Negotiable Scientific Principles)

1. **ممنوعیت کامل Hard-Code شدن موجودیت‌های یک طرح در کدهای هسته:**
   تمام نام‌های ترکیبات، سویه‌ها، رده‌های سلولی، دوزها و بیماری‌ها به عنوان ورودی و در مدل `ResearchProblemModel` تعریف می‌شوند. کدهای اصلی در `scripts/` فاقد هرگونه پیش‌فرض محدودکننده به یک موضوع خاص هستند.

2. **استراتژی جستجوی ۹ لایه‌ای و شواهد منفی الزامی (9-Layer Search):**
   هیچ جستجویی نباید صرفاً تأییدطلبانه (Confirmation-Seeking) باشد. جستجوی فعال شواهد منفی (Null, Toxicity, Antagonism, Failure, Resistance, Dose Limits) به صورت لایه‌بندی شده و سیستمی اجرا می‌شود.

3. **اصل تفکیک ارتباط از التزام (Relevance vs. Entailment):**
   مرتبط بودن موضوعی یک مقاله به هیچ عنوان به معنای اثبات ادعای متن پروپوزال توسط آن مقاله نیست. هر استناد باید بر پایه التزام دقیق محتوایی در مقیاس ۷ سطحی (`DIRECTLY_SUPPORTED` تا `CONTRADICTED`) تایید شود.

4. **ممنوعیت مطلق پرکردن زینتی مراجع (Zero Citation Padding):**
   هیچ منبعی نباید صرفاً برای زیاد نشان دادن تعداد مراجع به فهرست افزوده شود. هر منبع موجود در رفرنس‌ها باید دارای استناد معتبر در متن، لینک به ادعای علمی و گزاره تاییدشده در دفتر شواهد باشد (`Unused References == 0`).

5. **دروازه زبان علّی (Anti-Overclaim Causal Gate):**
   تبدیل عبارات همبستگی در مطالعات مشاهده‌ای به ادعاهای علیت اکیداً ممنوع بوده و به صورت خودکار با پرچم `OVERCLAIM_RISK` متوقف و اصلاح می‌گردد.

6. **مغالطه سینرژی بدون آزمون تجربی (No Synergy Fallacy):**
   اثبات اثربخشی جداگانه دو مداخله به هیچ وجه نباید به عنوان اثبات سینرژی (هم‌افزایی) بیان شود. سینرژی نیازمند آزمون مستقیم ترکیبی با ماتریس دوز و شاخص‌های آماری نظیر Chou-Talalay CI یا Bliss Independence است؛ در غیر این صورت وضعیت الزاما `SYNERGY_NOT_ESTABLISHED` است.

7. **تمایز فقدان شواهد از شواهد فقدان اثر (No Evidence != Evidence of No Effect):**
   اگر کارآزمایی بالینی برای یک مداخله انجام نشده است، نباید ادعا کرد «این مداخله فاقد اثر بالینی است». فرمول‌بندی معرفت‌شناختی دقیق `NO_DIRECT_EVALUATION_FOUND` الزامی است.

8. **قاعده ره‌گیری عددی و ممانعت از توهم ارقام:**
   تمام اعداد علمی اعم از دوز، $IC_{50}$، نسبت خطر، مقادیر $p$ و حجم نمونه باید مستقیماً از متن مقاله مرجع استخراج و در `EVIDENCE_LEDGER` ثبت شده باشند. در صورت عدم ذکر، وضعیت `NOT_REPORTED` ثبت شده و حدس زدن عدد اکیداً ممنوع است.

9. **قانون زمانی مراجع و توجیه منابع بنیادین:**
   شواهد اصلی اولیه باید در پنجره ۶ سال اخیر ($\text{Year} \ge \text{CURRENT\_YEAR} - 6$) باشند. ارجاع به مقالات قدیمی‌تر تنها در صورت داشتن برچسب توجیه بنیادین (`FOUNDATIONAL_JUSTIFICATION` نظیر مدل‌های ریاضی، روش‌های سنجش استاندارد، یا کشف‌های تاریخی مرجع) مجاز است.

---

## ۳. ساختار الزامی ۱۴ گانه بدنه پروپوزال (Institutional 14-Section Proposal Structure)

خروجی نهایی پروپوزال در فایل Word (`.docx`) باید واجد دقیقاً ۱۴ بخش استاندارد به شرح زیر باشد:
1. **موضوع:** عنوان کامل فارسی و انگلیسی.
2. **بیان مسئله:** نگارش تفصیلی پیرامون بار بیماری، اپیدمیولوژی، مبانی سلولی-مولکولی، چالش‌های درمانی و توجیه علمی طرح.
3. **مرور بر منابع:** اختصاص **یک پاراگراف تفصیلی و مستقل برای تک‌تک مراجع مورد استفاده** (با تحلیل جامعه/مدل، دوز، روش، یافته‌ها و ارتباط آن با طرح حاضر).
4. **اهمیت و ضرورت تحقیق:** تبیین ضرورت اجرای پژوهش در بندهای علمی و کاربردی.
5. **تعریف واژه‌ها:** تعاریف مفهومی و عملیاتی واژگان کلیدی طرح.
6. **اهداف جزیی:** اهداف مرحله‌ای متناسب با آزمون متغیرها.
7. **اهداف کلی:** بیان یکپارچه هدف اصلی با عبارت «تعیین...».
8. **اهداف کاربردی:** تبیین کاربردهای تشخیصی، درمانی و پیش‌بالینی طرح.
9. **فرضیات و سوالات پژوهش:** تفکیک روشن فرضیه‌های آماری/تجربی از سوالات پژوهشی.
10. **دستاوردها:** برشمردن دستاوردهای ملموس علمی، تولید شواهد و چاپ مقالات.
11. **جدول متغیرها:** جدول ساختارمند شامل نام متغیر، نقش، نوع، مقیاس و ابزار اندازه‌گیری.
12. **جدول زمان‌بندی و مراحل اجرا:** گانت چارت زمان‌بندی ماهانه.
13. **روش اجرا:** تفکیک متدولوژی در ۱۴ محور استاندارد (۱۳-۱ نوع مطالعه، ۱۳-۲ جامعه، ۱۳-۳ محل، ۱۳-۴ ورود، ۱۳-۵ خروج، ۱۳-۶ ابزارها، ۱۳-۷ روایی، ۱۳-۸ پایایی، ۱۳-۹ حجم نمونه و فرمول، ۱۳-۱۰ تحلیل داده‌ها، ۱۳-۱۱ ملاحظات اخلاقی، ۱۳-۱۲ حفاظت زیستی، ۱۳-۱۳ محدودیت‌ها، و ۱۳-۱۴ شیوه اجرایی گام‌به‌گام).
14. **فهرست منابع:** نمایه مراجع به فرمت استاندارد ونکوور به همراه شناسه DOI و لینک مستقیم.

---

## ۴. اسکریپت‌ها و ماژول‌های اجرایی مهارت (`scripts/`)

- **`research_problem_model.py`:** استخراج و ساخت مدل مسئله پژوهش بر مبنای چارچوب‌های PICO/PECO/Diagnostic/Mechanistic.
- **`generic_search_planner.py`:** طراحی استراتژی جستجوی ۹ لایه‌ای (A تا I)، زنجیره‌سازی استنادی و سنجش اشباع شواهد.
- **`generic_study_relationships.py`:** ترسیم روابط چندبُعدی بین‌مطالعه‌ای در ۲۲ نوع ارتباط پویا (Replication, Extension, Supports, Contradicts, ...).
- **`generic_gap_detector.py`:** شناسایی نظام‌مند شکاف‌های پژوهشی بر پایه شواهد تجربی در ۱۱ شاخه ساختارمند.
- **`generic_study_family_detector.py`:** شناسایی و خوشه‌بندی مطالعات مشترک، کدهای کارآزمایی و کوهورت‌های اپیدمیولوژیک جهت جلوگیری از شمارش مضاعف شواهد.
- **`generic_comparability_engine.py`:** ارزیابی همسنجی دوبه‌دوی مطالعات متناسب با طراحی مطالعه (سلولی، حیوانی، بالینی، تشخیصی، اپیدمیولوژیک).
- **`generic_contradiction_engine.py`:** تحلیل و رده‌بندی شواهد متناقض بر مبنای تاکسونومی ۱۵ گانه، تفکیک تناقض واقعی از اختلاف زمینه‌ای، و قاعده عدم اثبات اثر.
- **`generic_claim_entailment_engine.py`:** ممیزی التزام ادعاها در ۷ سطح، کنترل مغالطه سینرژی، کنترل ادعاهای علیت و ره‌گیری دقیق مقادیر عددی.
- **`generic_reference_auditor.py`:** ممیزی اعتبار کتابشناختی، سنجش مرز زمانی و پایش دقیق ممانعت از پرکردن زینتی مراجع.
- **`generic_evidence_synthesis.py`:** تلفیق چندبعدی شواهد بر پایه ۸ بعد قطعیت و ممانعت از ساده‌سازی اکثریتی.
- **`dynamic_protocol_designer.py`:** طراحی خودکار و پویای جدول متغیرها، گانت چارت زمان‌بندی و برنامه تحلیل آماری منطبق بر داده‌ها.
- **`proposal_structure_validator.py`:** دروازه اعتبارسنجی دقیق ساختار ۱۴ گانه با پشتیبانی کامل ارقام فارسی، یونیکد و نیم‌فاصله‌های استاندارد.
- **`multi_dimensional_qa_gate.py`:** دروازه ممیزی نهایی ۹ بعدی پیش از پرواز (QA Pre-Flight Gate).
- **`docx_builder.py`:** تولیدکننده سند نهایی Word با تایپوگرافی اختصاصی دبی فارسی و تگ‌های بومی RTL OpenXML.
- **`generate_compliant_proposal.py`:** اسمبلر جامع تولید پروپوزال منطبق بر شواهد و ممیزی‌شده.
- **`project_organizer.py`:** ماژول ساماندهی و ایجاد ساختار پوشه‌بندی استاندارد پروپوزال و تفکیک خودکار فایل‌های خروجی در فولدرهای اختصاصی.
- **`self_audit_suite.py`:** سوئیت آزمون ۶۰ گانه تجربی بنچ‌مارک در سه لایه ساختاری، علمی و کنترل‌های منفی.

---

## ۵. سوئیت جامع آزمون و اعتبارسنجی (`tests/`)

موتور با اجرای دستور زیر ممیزی می‌شود:
```bash
python tests/run_all_tests.py
```
این سیستم به صورت پویا ۴ سوئیت آزمون مستقل را اجرا و نتایج واقعی را گزارش می‌کند:
1. **آزمون نشت کدهای ایستا (`test_hard_code_leakage.py`):** اثبات وجود ۰ کلیدواژه بیولوژیک در کدهای هسته و استقلال سمانتیک کامل (۱۹ تست).
2. **آزمون تعمیم‌پذیری ۹ گانه (`test_general_domains.py` / `test_generalization.py`):** اجرای کامل پایپ‌لاین روی ۹ فیکسچر مستقل از رشته‌های مختلف پزشکی (۹ تست).
3. **آزمون‌های تنش خصمانه و کنترل‌های منفی ۶۵ گانه (`test_adversarial_scenarios.py`):** ۶۵ آزمون چالش‌برانگیز شامل رفرنس جعلی، عدم تطابق DOI (وضعیت IDENTITY_CONFLICT)، مقالات رترکت‌شده، سلسله‌مراتب شرطی، ماتریس تضاد، تبیین‌های جایگزین، ماتریس تکمیلی بودن، گزارش PRISMA، گراف چندلایه‌ای، ره‌گیری ادعا، ممیزی معرفت‌شناختی شکاف، گزارش دلتا، کوهورت‌های مشترک، جهش علیت، عدم قطعیت حجم نمونه، موضوعات کاملاً جدید خارج از فیکسچر، پروتکل‌های غیرمداخله‌ای، اثرات متقابل چندمداخله‌ای، و دروازه نهایی انتشار علمی ۵ ستونه (۶۵ تست).
4. **سوئیت بنچ‌مارک ۶۰ آزمونه (`self_audit_suite.py`):** اعتبارسنجی ۱۰۰ درصدی طرح‌های تاریخی، الزامات متدولوژیک و رعایت کامل فرمت ۱۴ گانه Word (۶۰ تست).

**مجموع آزمون‌ها:** ۱۵۳ آزمون مستقل با قبولی ۱۰۰٪ (153 / 153 PASS).

---

## ۶. معماری پوشه‌بندی و ساماندهی خودکار پروژه (Standard Workspace Layout)

مهارت `proposal-nevisi` در هر سشن جدید پژوهشی، به صورت خودکار یا از طریق اجرای ماژول `project_organizer.py` ساختار پوشه‌بندی استاندارد، تمیز و تفکیک‌شده زیر را ایجاد و حفظ می‌کند:

```text
├── proposal/          # سند خروجی نهایی Word (.docx)، نسخه مارک‌داون (.md) و استایل‌گایدها
├── references/        # مجموعه نهایی رفرنس‌ها، کش راستی‌آزمایی کتابشناختی، ممیزی مراجع و فایل‌های RIS/EndNote
├── evidence/          # سوابق شواهد مطالعات، ماتریس‌ها، گراف‌های DAG، دفاتر التزام و تحلیل سنتز نهایی
├── literature_search/ # ماتریس و لاگ جستجو، پایگاه‌های مورد جستجو، گزارش PRISMA و پیکره مقالات
├── contradictions/    # تحلیل و لاگ تناقضات، ماتریس همسنجی مطالعات و گزارش شواهد منفی
├── policies/          # معماری نهایی سیستم، خط‌مشی‌ها و گزارش‌های تفصیلی ممیزی و تعمیم‌پذیری
├── archive/           # پیش‌نویس‌های قدیمی، نسخه‌های منسوخ و فایل‌های موقت
└── schemas/           # اسکیماهای اعتبارسنجی ساختار داده‌ها
```

**قاعده تفکیک خروجی‌ها:** هیچ فایلی به صورت سرگردان و پراکنده در ریشه پروژه قرار نمی‌گیرد و تمامی ابزارها و اسکریپت‌ها (`self_audit_suite.py` و `reference_validity_auditor.py` و ...) دارای مکانیزم `resolve_path` هستند تا هم در پوشه‌های تفکیک‌شده و هم در صورت جابه‌جایی، فایل‌ها را با انعطاف کامل و دقت ۱۰۰٪ مکان‌یابی و اجرا نمایند.

