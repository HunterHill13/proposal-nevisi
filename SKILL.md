---
name: proposal-nevisi
description: >
  Comprehensive end-to-end Iranian medical and biomedical research proposal drafting, deep literature research,
  humanization, and Word (.docx) publication workflow. Interactively clarifies scope and methodological ambiguities,
  executes a 15-stage Evidence-Driven Deep Research Engine across 4 databases (PubMed/MeSH, Europe PMC, OpenAlex, Crossref),
  applies dedicated Contradictory/Negative evidence discovery, executes saturation-based citation chaining, classifies
  sources into 3 tiers (Tier A: Full-Text verified, Tier B: Abstract landscape, Tier C: Leads), extracts granular
  experimental parameters with exact sentence provenance, grounds compounds in PubChem and pathways in Reactome
  (strictly zero synthetic runtime fallbacks), maps claim-evidence entailment, builds an Evidence Gap Matrix (EQ01-EQ12),
  produces an emergent reference set with zero arbitrary caps, enforces strict novelty phrasing boundaries, applies the 6-layer
  anti-AI detection academic protocol, produces beautifully formatted Word documents featuring Dubai Persian typography,
  native RTL bidi XML (<w:bidi/>, <w:rtlGutter/>), Complex Script bolding (<w:bCs/>), zero divider dashes (---),
  formula callout boxes, styled tables, embedded Word Citation Manager sources via COM, and executes an automated 24-test self-audit suite.
---

# Proposal-Nevisi (مهارت جامع نگارش پروپوزال‌های پژوهشی علوم پزشکی و موتور Deep Research 4.0)

این مهارت یک راهکار خودکار، تعاملی، پیشرفته و با استاندارد سخت‌گیرانه برای تدوین پروپوزال‌های پژوهشی علوم پزشکی و زیست‌پزشکی در بالاترین تراز دانشگاهی است که مجهز به موتور اختصاصی **Deep Research 4.0** مبتنی بر شواهد پدیدارشده (Evidence-Driven)، بازیابی ۴ پایگاهی، اعتبارسنجی شیمیایی/مسیری زنده، ممیزی استلزام ادعا-شواهد (Claim-Evidence Entailment)، و نگارش انسان‌محور ضد هوش مصنوعی می‌باشد.

---

## اصول کلیدی و استانداردهای الزامی (Core Standards v4.0)

1. **معماری ۱۵ مرحله‌ای بازیابی و استخراج شواهد (The 15-Stage Evidence Funnel):**
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
   Deduplication (DOI, PMID, Normalized Title)
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

2. **قاعده کفایت شواهد و ممیزی کاربرد مراجع (Reference Usage & Zero Padding Policy):**
   - **تفکیک چهار شاخص کلیدی مراجع:**
     1. `Natural Selected References`: تعداد منابعی که بر پایه ضرورت شواهد و پوشش ادعاها به طور طبیعی انتخاب شده‌اند (بدون سقف و بدون اعمال هدف عددی).
     2. `Actually Cited Unique References`: تعداد منابع یکتا که واقعاً در بدنه متن پروپوزال با شناسه استنادی معتبر (مانند `[1]` تا `[N]`) استناد شده‌اند (الزام: حداقل ۱۵ منبع، سقف نامحدود).
     3. `Unused Selected References`: تعداد منابعی که در فهرست مراجع وجود دارند ولی در متن پروپوزال استفاده نشده‌اند (خط قرمز: باید دقیقاً صفر باشد: `Unused Selected References == 0`).
     4. `Padding Added`: تعداد مقالاتی که صرفاً برای رسیدن به کف عددی افزوده شده‌اند (خط قرمز: باید دقیقاً صفر باشد: `Padding Added == 0`).
   - **کف مراجع یک دروازه سنجش کفایت است، نه هدف گزینش (The minimum reference count is a sufficiency gate, not a selection target):** الگوریتم گزینش ابتدا تمام منابعی را که واقعاً برای پوشش ادعاهای ضروری و حوزه‌های شواهد پروپوزال نیاز است به صورت طبیعی (Natural Evidence Selection) استخراج می‌کند؛ سپس در مرحله پایانی کفایت آن را با حداقل ۱۵ ارزیابی می‌نماید.
   - **ممنوعیت مطلق افزودن منبع برای رساندن به عدد (No reference may be added solely to satisfy the minimum count):** افزودن هرگونه مقاله ضعیف یا اضافی صرفاً برای رساندن عدد به ۱۵ اکیداً غیرمجاز است. اگر تعداد مراجع واجد شرایط کمتر از ۱۵ باشد (مثلاً ۱۲)، سیستم باید وضعیت را صریحاً `FAILED_MINIMUM_REFERENCE_REQUIREMENT` اعلام کند، نه اینکه با ۳ مقاله ضعیف‌تر عدد را به ۱۵ برساند!
   - **تعیین پدیدارشده منابع بدون سقف حداکثری (The final reference set is determined by evidence necessity, min 15, no max cap):** هیچ سقفی (مانند ۱۵، ۲۰، ۳۰، ۵۰ یا ۸۰) برای تعداد مراجع نهایی وجود ندارد و اگر ۳۸ یا ۷۴ مقاله واقعاً ضروری باشند، همگی بدون برش وارد پروپوزال می‌شوند.
   - **ممیزی زایدات و همپوشانی (Reference Redundancy Audit):** هر منبع منتخب بررسی می‌شود؛ چنانچه منبع دیگری با وزن و رتبه کیفی بالاتر دقیقاً همان ادعاها و دامنه‌ها را پوشش دهد، منبع مازاد به عنوان `REDUNDANT` حذف می‌گردد تا از تراکم بی‌مورد جلوگیری شود.

3. **سطح‌بندی سه‌گانه منابع (Strict 3-Tier Source Classification):**
   - **Tier A (تمام‌متن تأییدشده PMC OA XML / Europe PMC XML > 1000 کاراکتر):** منحصراً برای استخراج پارامترهای کمی (دوز، IC50، زمان انکوباسیون) و شواهد مکانیسمی مستقیم. چکیده هرگز به عنوان متن کامل پذیرفته نمی‌شود!
   - **Tier B (چکیده و متادیتای تأییدشده):** برای ترسیم بستر پژوهش، اپیدمیولوژی، و شواهد زمینه‌ای.
   - **Tier C (سرنخ‌های اولیه بدون متن کامل):** در رجیستری منابع ثبت شده اما وارد استخراج کمی نمی‌شوند.

4. **شاخه اختصاصی کشف شواهد متناقض و ارزیابی ریسک (Contradictory Evidence Branch):**
   - کوئری‌های اختصاصی جهت کشف پدیده‌های آنتاگونیسم (Antagonism)، مقاومت‌های دارویی/ویروسی، سمیت‌های فراتر از پنجره درمانی، و عدم اثربخشی.
   - تولید سند رسمی `CONTRADICTORY_EVIDENCE.md` جهت پیش‌بینی موانع و تدوین راهکارهای کنترلی در متدولوژی طرح.

5. **زنجیره استنادی اشباع‌محور (Saturation Citation Chaining):**
   - پیمایش مراجع گذشته‌نگر (Backward)، استنادهای آینده‌نگر (Forward) و گراف مقالات مرتبط (OpenAlex Related Works).
   - توقف فرآیند بر اساس قانون بازده نهایی حاشیه‌ای (Marginal Yield < Threshold) به جای تعداد گام‌های صلب.

6. **سیاست قطعی عدم داده‌های ساختگی و حذف کامل Fallbackهای هاردکد (Zero Hardcoded Fallbacks):**
   - در صورت اختلال شبکه یا عدم پاسخ‌دهی سرورهای PubChem یا Reactome، وضعیت رکورد صریحاً به عنوان `UNVERIFIED` ثبت می‌گردد و هیچ مقدار حدسی یا هاردکد جایگزین نمی‌شود.
   - مراجع متدولوژیک کلاسیک (چو-تالالی ۲۰۰۶ و مسمن ۱۹۸۳) با فلگ `is_foundation: True` کاملاً از شواهد تجربی جدید تفکیک می‌شوند.

7. **بیان اصالت و نوآوری در چارچوب مرز مستند (Strict Novelty Policy):**
   - ادعای مطلق و غیرعلمی «برای اولین بار» یا «اثبات می‌کند» ممنوع است.
   - بیان نوآوری صرفاً در قالب کران‌دار و مقید به مرز جست‌وجو مجاز است:
     *"No directly matching study was identified within the documented search boundary (PubMed, Europe PMC, OpenAlex, Crossref; 2020-2026)."*

8. **تایپوگرافی مستر ورد (Master Word Typography):**
   - فونت استاندارد `Dubai` با راست‌به‌چپ سراسری (`<w:bidi/>` و `<w:rtlGutter/>`).
   - بومی‌سازی تیترهای فارسی با پررنگ‌سازی Complex Script (`<w:bCs/>`).
   - حذف ۱۰۰٪ خط‌تیره‌های جداکننده مخرّب (`---`).
   - ثبت مستقیم منابع در **Word Citation Manager** از طریق اتوماسیون COM.

9. **سوئیت جامع اسناد و خروجی‌های Deep Research v4.5:**
   - **`SOURCE_REGISTRY.json`:** پایگاه داده کامل تمام منابع کشف‌شده به همراه Tier و وضعیت غربالگری.
   - **`EXCLUDED_STUDIES.json`:** مستندسازی شفاف علل حذف تک‌تک مقالات غربال‌شده.
   - **`SEARCH_QUERY_LOG.json`:** لاگ کامل تک‌تک کوئری‌های ارسالی به ۴ پایگاه داده با کد وضعیت HTTP و تعداد نتایج.
   - **`SEARCH_BOUNDARY.json`:** تعریف رسمی مرز جست‌وجو و بیانیه اصالت طرح.
   - **`LITERATURE_SEARCH_REPORT.md`:** گزارش رسمی ممیزی فرآیند جست‌وجو بر مبنای استاندارد PRISMA 2020.
   - **`CONTRADICTORY_EVIDENCE.md`:** تحلیل تحلیلی شواهد متناقض، سمیت و موانع ایمنی.
   - **`EVIDENCE_GAP_MATRIX.md`:** ماتریس تحلیل خلأهای شواهد در ۱۲ حوزه کلیدی (EQ01-EQ12).
   - **`CLAIM_EVIDENCE_MAP.json`:** ممیزی معنایی استلزام ادعا-شواهد با برچسب‌های استاندارد.
   - **`EVIDENCE_LEDGER.json`:** دفتر کل شواهد آزمایشگاهی با نقل‌قول مستقیم درون‌متنی و فاقد عبارات ساختگی.
   - **`PROPOSAL_REFERENCE_SET.json`:** مراجع برگزیده نهایی با نقش دقیق، لینک ادعاها، شماره ارجاع و فاقد زایدات (حداقل ۱۵ منبع بدون سقف).
   - **`FINAL_REFERENCE_USAGE_AUDIT.json`:** سند رسمی ممیزی تطابق ارجاعات در متن پروپوزال، شمارش دقیق استنادات یکتا، و تأیید عدم وجود منبع بدون استفاده.
   - **`FINAL_REFERENCE_VALIDITY_AUDIT.json`:** سند ساختاریافته ممیزی ۴ محوره اعتبار کتابشناختی، ارتباط علمی، پشتیبانی ادعا، و ضرورت استناد تک‌تک منابع.
   - **`FINAL_REFERENCE_VALIDITY_AUDIT.md`:** گزارش تفصیلی انسانی و واکاوی ۷‌گانه تک‌تک مراجع نهایی.
   - **`EVIDENCE_SUFFICIENCY_REPORT.md`:** گیت ممیزی ۱۰ ضابطه کیفیت با تفکیک انتخاب طبیعی و پدینگ صفر.
   - **`LITERATURE_DEEP_RESEARCH.md`:** پرونده تحلیلی شواهد تجربی به صورت کاملاً پویا و متصل به مراجع.
   - **`references_with_fulltext.json`**, **`EndNote_Citations.enw`**, **`references_library.ris`**

10. **آزمونگر سخت‌گیرانه ۳۴ گانه خود-ممیزی (34-Test Behavioral Self-Audit Suite v4.5):**
    - ارزیابی رفتاری روی داده‌های واقعی:
      1. پیاده‌سازی صفحه‌بندی واقعی (Real Pagination)
      2. فقدان سقف ساختگی در بازیابی و گزینش (Zero Hardcoded Caps)
      3. ممیزی سراسری دسترسی به متن کامل (Universal Full-Text Audit)
      4. تفکیک شواهد کمی به Tier A
      5. مشارکت فعال هر ۴ پایگاه علمی (PubMed, Europe PMC, OpenAlex, Crossref)
      6. ساختار چندوجهی ماتریس کوئری (QUERY_MATRIX.json)
      7. شواهد متناقض عمیق (CONTRADICTORY_EVIDENCE.md)
      8. پالایش کانونیکال و بدون تکرار (Canonical Deduplication)
      9. اشباع انطباقی زنجیره استنادی (Adaptive Saturation)
      10. نقل‌قول‌های پارامتری مستقیم (Claim-Quote Verbatim Integrity)
      11. گراف ادعا-شواهد (CLAIM_EVIDENCE_GRAPH.json)
      12. گیت ۱۰ گانه کفایت شواهد (Evidence Sufficiency Gate)
      13. نقشه‌برداری شکاف‌های پژوهشی بر مرز جست‌وجو (RESEARCH_GAP_MAP.json)
      14. استقلال رتبه کیفیت و ارتباط (Decoupled Quality vs Relevance)
      15. اعتبارسنجی زنده پاب‌کم (PubChem Live Grounding)
      16. اعتبارسنجی زنده ری‌اکتوم (Reactome Live Grounding)
      17. کفایت حداقل ۱۵ منبع پروپوزال (Count >= 15, Max Unlimited)
      18. عدم وجود سقف حداکثری بر مراجع (No Arbitrary Maximum Cap)
      19. عدم پرسازی جعلی منابع و ممیزی زایدات (Zero Reference Padding)
      20. اتصال ۱۰۰٪ مراجع به ادعاها (Claim Linkage)
      21. یکپارچگی نقش‌های استنادی (Reference Roles Integrity)
      22. ممیزی سیاست نوآوری کران‌دار (Strict Novelty Policy)
      23. استانداردهای تایپوگرافی دبی و XML دوزبانه
      24. انطباق سرتاسری اسناد خروجی (Cross-Artifact Consistency)
      25. ضابطه عدم تأثیر حداقل آستانه بر گزینش شواهد (Zero-Padding Gate)
      26. استفاده واقعی پروپوزال از حداقل ۱۵ منبع یکتا در بدنه متن (Actually Cited >= 15)
      27. استناد قطعی به ۱۰۰٪ مراجع نهایی در متن پروپوزال (Unused Selected References == 0)
      28. پشتیبانی مستند شواهدی برای تمامی ادعاهای اساسی پروپوزال (Every Major Claim Has Evidence)
      29. ممیزی اعتبار کتابشناختی (Bibliographic Validity Audit: 100% verified, 0 invalid, 0 fabricated)
      30. یکپارچگی شناسه‌های DOI و PMID و فقدان متادیتای تخمینی (DOI/PMID Integrity Audit)
      31. انطباق ارتباط علمی با دامنه‌های ۱۱ گانه تخصصی طرح (Scientific Relevance Audit)
      32. ممیزی استلزام ادعا-مرجع و منع مغالطات تعمیم مدل یا داروی تک به ترکیب (Claim-to-Reference Entailment Audit)
      33. ممیزی ضرورت و عدم زایدات مراجع نهایی (Reference Necessity / Redundancy Audit)
      34. گیت جامع تأیید اعتبار و ارتباط مراجع نهایی (Overall Reference Validity Gate Audit)
