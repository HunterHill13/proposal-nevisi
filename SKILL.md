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

2. **قاعده کفایت و عدم محدودیت حداکثری در تعداد منابع (Min 15 References & No Max Cap):**
   - **کف الزامی ۱۵ منبع (`MIN_PROPOSAL_REFERENCES = 15`):** پروپوزال باید برای تضمین جامعیت و پوشش کامل بخش‌های دهگانه خود، حداقل ۱۵ منبع پدیدارشده و معتبر داشته باشد.
   - **عدم وجود سقف حداکثری (`MAX_PROPOSAL_REFERENCES = None`):** هیچ سقف مصنوعی و بسته‌ای برای تعداد منابع نهایی وجود ندارد و تعداد بر اساس نیاز ادعاهای متن (Emergent) تعیین می‌شود.
   - **سیاست قطعی عدم پرسازی جعلی (Zero Padding Policy):** افزودن هرگونه مقاله ضعیف، نامرتبط یا ساختگی صرفاً برای رسیدن به عدد ۱۵ اکیداً ممنوع است. در صورتی که تعداد شواهد واجد شرایط کمتر از ۱۵ باشد، سیستم باید وضعیت را صریحاً `FAILED_MINIMUM_REFERENCE_REQUIREMENT` اعلام کند و کسری شواهد را گزارش نماید.
   - **انتخاب پوشش‌محور با نقش مشخص (Coverage-Based Reference Selection):** هر منبع نهایی در `PROPOSAL_REFERENCE_SET.json` باید دارای نقش معتبر (`role`, `roles`)، ادعاهای متصل (`supported_claims` حداقل ۱ مورد)، رتبه کیفیت، و دلیل ضرورت (`necessity_reason`) باشد.

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

9. **سوئیت جامع اسناد و خروجی‌های Deep Research v4.0:**
   - **`SOURCE_REGISTRY.json`:** پایگاه داده کامل تمام منابع کشف‌شده به همراه Tier و وضعیت غربالگری.
   - **`EXCLUDED_STUDIES.json`:** مستندسازی شفاف علل حذف تک‌تک مقالات غربال‌شده.
   - **`SEARCH_QUERY_LOG.json`:** لاگ کامل تک‌تک کوئری‌های ارسالی به ۴ پایگاه داده با کد وضعیت HTTP و تعداد نتایج.
   - **`SEARCH_BOUNDARY.json`:** تعریف رسمی مرز جست‌وجو و بیانیه اصالت طرح.
   - **`LITERATURE_SEARCH_REPORT.md`:** گزارش رسمی ممیزی فرآیند جست‌وجو بر مبنای استاندارد PRISMA 2020.
   - **`CONTRADICTORY_EVIDENCE.md`:** تحلیل تحلیلی شواهد متناقض، سمیت و موانع ایمنی.
   - **`EVIDENCE_GAP_MATRIX.md`:** ماتریس تحلیل خلأهای شواهد در ۱۲ حوزه کلیدی (EQ01-EQ12).
   - **`CLAIM_EVIDENCE_MAP.json`:** ممیزی معنایی استلزام ادعا-شواهد با برچسب‌های استاندارد.
   - **`EVIDENCE_LEDGER.json`:** دفتر کل شواهد آزمایشگاهی با نقل‌قول مستقیم درون‌متنی و فاقد عبارات ساختگی.
   - **`PROPOSAL_REFERENCE_SET.json`:** مراجع برگزیده نهایی با نقش دقیق و لینک ادعاها (حداقل ۱۵ منبع بدون سقف).
   - **`EVIDENCE_SUFFICIENCY_REPORT.md`:** گیت ممیزی کفایت شواهد در ۱۰ بخش ساختاری پروپوزال.
   - **`LITERATURE_DEEP_RESEARCH.md`:** پرونده تحلیلی شواهد تجربی به صورت کاملاً پویا و متصل به مراجع.
   - **`references_with_fulltext.json`**, **`EndNote_Citations.enw`**, **`references_library.ris`**

10. **آزمونگر سخت‌گیرانه ۲۴ گانه خود-ممیزی (24-Test Behavioral Self-Audit Suite):**
    - ارزیابی رفتاری روی داده‌های واقعی: پیاده‌سازی صفحه‌بندی واقعی، فقدان سقف ساختگی در بازیابی و گزینش، ممیزی سراسری دسترسی به متن کامل، تفکیک شواهد کمی به Tier A، مشارکت فعال هر ۴ پایگاه، ساختار چندوجهی ماتریس کوئری، شواهد متناقض عمیق، پالایش کانونیکال و بدون تکرار، اشباع انطباقی زنجیره استنادی، نقل‌قول‌های پارامتری مستقیم، گراف ادعا-شواهد، گیت ۱۰ گانه کفایت شواهد، نقشه‌برداری شکاف‌های پژوهشی بر مرز جست‌وجو، استقلال رتبه کیفیت و ارتباط، اعتبارسنجی زنده پاب‌کم، اعتبارسنجی زنده ری‌اکتوم، کفایت حداقل ۱۵ منبع پروپوزال، عدم وجود سقف حداکثری بر مراجع، عدم پرسازی جعلی منابع، اتصال ۱۰۰٪ مراجع به ادعاها، یکپارچگی نقش‌های استنادی، ممیزی سیاست نوآوری کران‌دار، استانداردهای تایپوگرافی دبی و XML دوزبانه، و انطباق سرتاسری اسناد خروجی.
