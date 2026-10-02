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
  formula callout boxes, styled tables, embedded Word Citation Manager sources via COM, and executes an automated 18-test self-audit.
---

# Proposal-Nevisi (مهارت جامع نگارش پروپوزال‌های پژوهشی علوم پزشکی و موتور Deep Research 3.0)

این مهارت یک راهکار خودکار، تعاملی، پیشرفته و با استاندارد سخت‌گیرانه برای تدوین پروپوزال‌های پژوهشی علوم پزشکی و زیست‌پزشکی در بالاترین تراز دانشگاهی است که مجهز به موتور اختصاصی **Deep Research 3.0** مبتنی بر شواهد پدیدارشده (Evidence-Driven)، بازیابی ۴ پایگاهی، اعتبارسنجی شیمیایی/مسیری زنده، ممیزی استلزام ادعا-شواهد (Claim-Evidence Entailment)، و نگارش انسان‌محور ضد هوش مصنوعی می‌باشد.

---

## اصول کلیدی و استانداردهای الزامی (Core Standards v3.0)

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

2. **قاعده قطعی عدم محدودیت ساختگی در تعداد منابع (No Arbitrary Final-Paper Cap):**
   - هیچ سقف ثابت و قراردادی (مانند ۱۵ یا ۲۰ مقاله) برای تعداد مراجع نهایی وجود ندارد.
   - تعداد منابع نهایی به صورت **پدیدارشده (Emergent)** و متناسب با نیاز ادعاهای متن تعیین می‌گردد.
   - هر منبعی که وارد پروپوزال می‌شود باید دارای یک نقش استنادی مشخص (`Primary_efficacy`, `Mechanism`, `Model_justification`, `Methodology_standard`, `Safety_toxicity`, `Background_landscape`, `Contradictory_context`, `Gap_identification`) باشد تا از اسپم استنادی جلوگیری شود.

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

9. **سوئیت جامع اسناد و خروجی‌های Deep Research v3.0:**
   - **`SOURCE_REGISTRY.json`:** پایگاه داده کامل تمام منابع کشف‌شده به همراه Tier و وضعیت غربالگری.
   - **`EXCLUDED_STUDIES.json`:** مستندسازی شفاف علل حذف تک‌تک مقالات غربال‌شده.
   - **`SEARCH_QUERY_LOG.json`:** لاگ کامل تک‌تک کوئری‌های ارسالی به ۴ پایگاه داده با کد وضعیت HTTP و تعداد نتایج.
   - **`SEARCH_BOUNDARY.json`:** تعریف رسمی مرز جست‌وجو و بیانیه اصالت طرح.
   - **`LITERATURE_SEARCH_REPORT.md`:** گزارش رسمی ممیزی فرآیند جست‌وجو بر مبنای استاندارد PRISMA 2020.
   - **`CONTRADICTORY_EVIDENCE.md`:** تحلیل تحلیلی شواهد متناقض، سمیت و موانع ایمنی.
   - **`EVIDENCE_GAP_MATRIX.md`:** ماتریس تحلیل خلأهای شواهد در ۱۲ حوزه کلیدی (EQ01-EQ12).
   - **`CLAIM_EVIDENCE_MAP.json`:** ممیزی معنایی استلزام ادعا-شواهد با برچسب‌های استاندارد.
   - **`EVIDENCE_LEDGER.json`:** دفتر کل شواهد آزمایشگاهی با نقل‌قول مستقیم درون‌متنی و فاقد عبارات ساختگی.
   - **`LITERATURE_DEEP_RESEARCH.md`:** پرونده تحلیلی شواهد تجربی به صورت کاملاً پویا و متصل به مراجع.
   - **`references_with_fulltext.json`**, **`EndNote_Citations.enw`**, **`references_library.ris`**

10. **آزمونگر سخت‌گیرانه ۱۸ گانه خود-ممیزی (18-Test Self-Audit Suite):**
    - پوشش ۴ پایگاه، شفافیت کوئری‌ها، ثبت مرز، اصالت رجیستری، شفافیت حذفیات، عدم سقف ساختگی، اشباع زنجیره استنادی، شاخه متناقض، ماتریس ۱۲ گانه خلأها، استلزام معنایی، حذف فال‌بک‌های هاردکد، سیاست اصالت مقید، نقل‌قول‌های پارامتری، استعلام زنده پاب‌کم، استعلام زنده ری‌اکتوم، تخصیص نقش استنادی، استانداردهای تایپوگرافی دبی، و انطباق سرتاسری اسناد.
