---
name: proposal-nevisi
description: >
  Universal, configuration-driven Iranian medical and biomedical research proposal drafting, deep literature research,
  evidence synthesis, humanization, and Word (.docx) publication engine (v10.0). Operates across diverse biomedical domains
  (oncology, cardiology, infectious diseases, diagnostics, epidemiology, immunology, endocrinology, nephrology, basic experimental science).
  Built on a 4-layer hardened modular architecture (Layer 1: Scientific Accuracy via BiologicalMechanismAdversarialVerifier, CombinationHypothesisEngine,
  CompoundEntityNormalizer, and BiphasicRedoxContextRule; Layer 2: Structural Compliance strictly enforcing the canonical 28 sections of Iranian biomedical proposals: 1.موضوع, 2.بیان مسئله, 3.مرور بر منابع, 4.اهمیت وضرورت تحقیق, 5.تعریف واژه ها, 6.اهداف جزیی, 7.اهداف کلی, 8.اهداف کاربردی, 9.فرضیات و سوالات, 10.دستاورد ها, 11.جدول متغیر ها, 12.جدول زمان بندی و مراحل اجرا, 13.روش اجرا, 14.نوع مطالعه, 15.جامعه مورد مطالعه, 16.محل انجام مطالعه, 17.معیار های ورود به مطالعه, 18.معیار های خروج از مطالعه, 19.ابزار های گردآوری اطلاعات, 20.تعیین اعتبار ابزار گردآوری, 21.تعیین ابزار گردآوری, 22.حجم نمونه و روش محاسبه آن, 23.روش تجزیه و تحلیل داده, 24.ملاحظلات اخلاقی در صورت نیاز, 25.نحوه رعایت نکات امنیتی و حفاظت پروژه در صورت نیاز, 26.مشکلات و محدودیت ها, 27.روش انجام طرح، شیوه اجرایی مراحل طرح و چگونگی جمع آوری اطلاعات, 28.منابعی که استفاده شد (انگلیسی یا فارسی), design-sensitive sample size evaluation,
  AssayInterferencePolicy (cell-free blank & orthogonal triangulation), and decoupled StatisticalAnalysisModelSelector / CombinationInteractionModelSelector;
  Layer 3: Citation & Full-Text Integrity via FullTextRetrievalEngine (Europe PMC JATS XML / PMC BioC / OpenAlex OA cascade with persistent disk caching),
  Passage Grounding (mandatory extraction of verbatim evidence sentences), Abstract-Only Quota Gate (strictly <= 20% with mandatory justification),
  CitationTracker enforcing global document Vancouver re-indexing, LiveReferenceVerificationGate (fail-closed PubMed/Crossref authentication with zero offline provisional loophole and auto-drop unverified citations),
  orphaned claim detection, and unused reference elimination;
  Layer 4: Formatting & Typesetting via NativeOmmlMathEngine converting LaTeX to native Word OMML XML <m:oMath>,
  and PersianMedicalTypographyLinter protecting English parentheses, math, and DOIs). Enforces ProposalReadinessGate as a fail-closed pre-generation and Word pre-flight gatekeeper.
  Harmonizes synergy metrics across sections via Single Source of Truth SynergyMetricConfig.
  Supports multi-source federated searches (PubMed, Europe PMC, OpenAlex, Crossref), 16 query families, MeSH mapping, multi-directional citation chasing,
  saturation tracking, deep paper reading, SciFact-aligned claim verification, 8-tier evidence hierarchy,
  and passes a unified 429-assertion test harness across 19 suites and 44 release gate criteria with zero hardcoded biological leakage across all engine scripts.
---

# Proposal-Nevisi (موتور جامع، ماژولار و مبتنی بر شواهد نگارش پروپوزال‌های علوم پزشکی v10.2)

این مهارت یک پلتفرم جامع، تعاملی، کاملاً ماژولار، مستقل از موضوع (Topic-Agnostic) و مبتنی بر شواهد برای تدوین پروپوزال‌های پژوهشی علوم پزشکی و زیست‌پزشکی در بالاترین تراز دانشگاهی و استانداردهای پژوهشی کشور است.

نسخه ۱۰.۲ بر مبنای هاردنینگ پیشرفته ضدتوهم، خط لوله واکشی متن کامل، دروازه‌های اعتبارسنجی زنده، استانداردهای بازتولیدپذیری EQUATOR و مهار پیشگیرانه سوگیری طراحی گردیده و موارد زیر را تضمین می‌کند:
- **ستون ۱ (LiveReferenceVerificationGate):** گیت اعتبارسنجی زنده مراجع علیه PubMed E-utilities و Crossref با کش پایدار محلی و سیاست Fail-Closed؛ حذف کامل بای‌پَس‌های آفلاین و پالایش خودکار رفرنس‌های نامعتبر (`auto_drop_unverified`).
- **ستون ۲ (FullTextRetrievalEngine & Passage Grounding):** خط لوله واکشی آبشاری متن کامل از Europe PMC JATS XML، PMC BioC API و OpenAlex OA با کش پایدار در `.cache/fulltext/` و استخراج الزامی حداقل ۲ گزیده متنی مستند (Passages) برای اثبات مطالعه عمیق متن.
- **ستون ۳ (Abstract-Only Quota Gate):** سقف قطعی حداکثر ۲۰٪ برای مقالات فقط-چکیده (Tier B) به همراه الزام ارائه توجیه علمی اختصاصی در متادیتا و گزارش ممیزی `FINAL_REFERENCE_VALIDITY_AUDIT.md`.
- **ستون ۴ (EvidenceRoleClaimBindingGate & CitationTracker):** اتصال نقش شواهد و بخش‌های سند جهت ممانعت از سوگیری مجاورت کلیدواژه، به همراه بازشماری یکپارچه ونکوور درون‌متنی و حذف هرگونه ارجاع بدون استفاده.
- **ستون ۵ (BiphasicRedoxContextRule & AssayInterferencePolicy):** تفکیک دوحالته ردوکس در ارزیابی مکانیسمی، اجبار کنترل بلانک بدون سلول (Cell-Free Blank) و ترایانگولاسیون ارتوگونال با فلوسایتومتری Annexin V/PI و آزمون کلونوژنیک.
- **ستون ۶ (Pre-Flight Compilation Gatekeeper):** مسدودسازی قطعی تولید فایل ورد (.docx) در `ProposalReadinessGate` در صورت وجود هرگونه رفرنس تأییدنشده یا تخطی از سقف مقالات چکیده.
- **ستون ۷ (MockGrantReviewPanel & Inter-Section Semantic Drift Gate):** شبیه‌سازی هیئت داوران گرنت (Mock Study Section) متشکل از ۳ داور تخصصی (اصالت علمی، متدولوژی و بیواستاتیک، اخلاق و ایمنی زیستی) در مقیاس داوری ۱ تا ۹ با آستانه قبولی ۳.۵، پایش تناظر ۱ به ۱ اهداف با متدولوژی و صدور کارنامه رسمی `MOCK_GRANT_REVIEW_REPORT.md` و `.json`.
- **ستون ۸ (EquatorComplianceAuditor & Biological Resource Authentication):** ممیزی و تطابق خودکار با راهنماهای بین‌المللی شبکه EQUATOR (شامل OECD/GCCP برای کشت سلولی، MIQE برای سنجش‌های بیان ژن، ARRIVE 2.0 برای مطالعات حیوانی) به همراه استانداردهای احراز هویت زیستی NIH (شناسنامه STR سلول، غربالگری مایکوپلاسما، خلوص مواد دارویی $\ge 95\%$ و کنترل حلال ناقل) و صدور کارنامه رسمی `EQUATOR_COMPLIANCE_AUDIT.md` و `.json`.
- **ستون ۹ (PreEmptiveRiskOfBiasMitigator):** مهار پیشگیرانه سوگیری بر اساس استانداردهای بین‌المللی Cochrane RoB-2 و SYRCLE در ۵ دامنه بنیادین (سوگیری انتخاب، سوگیری عملکرد، سوگیری تشخیص و کورسازی ارزیاب، سوگیری ریزش و مدیریت داده‌های پرت، و سوگیری گزارش‌دهی انتخابی و پیش‌ثبت پروتکل در OSF/پژوهشیار) و صدور کارنامه رسمی `RISK_OF_BIAS_MITIGATION_REPORT.md` و `.json`.
- الزام قطعی و بدون انحراف ساختار مصوب ۲۸ بخشی پژوهشیار در تمام خروجی‌های سند Markdown و Word.
- تبدیل و اعتبارسنجی E2E فرمول‌های ریاضی به تگ‌های بومی ورد `<m:oMath>` در `docx_builder` و حذف کامل نشت سینتکس LaTeX.
- محافظت کامل از عبارات انگلیسی داخل پرانتز و شناسه‌های DOI/PMID در `PersianMedicalTypographyLinter`.

---

## ۱. ساختار قطعی، مصوب و الزامی ۲۸ بخشی پروپوزال (Mandatory 28 Canonical Sections)

کلیه پروپوزال‌های تدوین‌شده توسط این مهارت، بدون هیچ‌گونه استثنا، حذف یا ادغام، باید دارای **دقیقاً ۲۸ بخش اصلی** زیر با هدینگ سطح دو (`##`) و با شماره‌گذاری و عناوین فارسی استاندارد زیر باشند:

1. **موضوع** (شامل عنوان کامل فارسی و انگلیسی طرح)
2. **بیان مسئله** (Problem Statement تحلیلی با شواهد بیولوژیک و اپیدمیولوژیک)
3. **مرور بر منابع (مقالات و فعالیت های مشابه به موضوع ما)** (سنتز پیشینه با پاراگراف‌های مجزا به ازای هر مطالعه)
4. **اهمیت وضرورت تحقیق** (دلایل توجیه‌کننده بالینی، علمی و اقتصادی)
5. **تعریف واژه ها (واژه های بولد و علمی که نیازمند توضیح هستند)** (تعاریف واژگان تخصصی و مداخلات)
6. **اهداف جزیی (تعیین تاثیر متغیر مستقل روی متغیر وابسته)** (اهداف اختصاصی مرحله‌ای و آزمون‌پذیر)
7. **اهداف کلی (همین موضوع با کلمه تعیین..)** (عنوان طرح با عبارت آغازین تعیین...)
8. **اهداف کاربردی** (کاربردهای ملموس در نظام سلامت، بالین و داروسازی)
9. **فرضیات و سوالات** (فرضیه‌های متوازن هم‌افزایی/تضاد و سوالات کلیدی پژوهش)
10. **دستاورد ها (چه دستاوردی ازین تحقیق خواهیم داشت)** (خروجی‌های ملموس، مقالات علمی و دانش فنی بومی)
11. **جدول متغیر ها (نقش متغیر (وابسته، مستقل،مخدوش گر) و نوع متغیر(کیفی، کمی پیوسته یا کمی گسسته))** (جدول استاندارد متغیرها با تمام ستون‌های متدولوژیک)
12. **جدول زمان بندی و مراحل اجرا** (گانت چارت فازبندی‌شده زمانی به صورت جدول Markdown)
13. **روش اجرا** (نمای کلی و چارچوب کلی متدولوژی پژوهش)
14. **نوع مطالعه** (طراحی تجربی برون‌تن، درون‌تن، کارآزمایی بالینی، مشاهده‌ای یا تشخیصی)
15. **جامعه مورد مطالعه** (مدل زیستی، رده سلولی، حیوان آزمایشگاهی یا جامعه انسانی هدف)
16. **محل انجام مطالعه** (آزمایشگاه‌ها، مراکز تحقیقاتی و دانشگاه محل اجرا)
17. **معیار های ورود به مطالعه** (شرایط احراز نمونه‌ها، سلول‌ها یا بیماران)
18. **معیار های خروج از مطالعه** (شرایط حذف، آلودگی یا افت شاخص‌ها)
19. **ابزار های گردآوری اطلاعات** (دستگاه‌های آزمایشگاهی، کیت‌ها و نرم‌افزارهای تحلیلی)
20. **تعیین اعتبار ابزار گردآوری** (روایی، کالیبراسیون و استانداردهای مرجع بین‌المللی)
21. **تعیین ابزار گردآوری** (پایایی، قابلیت اعتماد ابزار، تکرارهای مستقل و ضرایب CV)
22. **حجم نمونه و روش محاسبه آن** (فرمول ریاضی استاندارد کوهن/مید/کوکران و تعیین تکرارهای بیولوژیک مستقل)
23. **روش تجزیه و تحلیل داده** (آزمون‌های پیش‌فرض، آنالیز واریانس فاکتوریل، مدل‌های برهم‌کنش و نرم‌افزارها)
24. **ملاحظلات اخلاقی در صورت نیاز** (کد اخلاق، رضایت آگاهانه و استانداردهای مصوب کمیته اخلاق)
25. **نحوه رعایت نکات امنیتی و حفاظت پروژه در صورت نیاز** (سطح ایمنی زیستی BSL، مدیریت پسماند و PPE)
26. **مشکلات و محدودیت ها** (چالش‌های فنی، فارماکولوژیک و بیولوژیک و راهکارهای مهار)
27. **روش انجام طرح، شیوه اجرایی مراحل طرح و چگونگی جمع آوری اطلاعات** (پروتکل گام‌به‌گام اجرایی طرح)
28. **منابعی که استفاده شد (انگلیسی یا فارسی)** (فهرست کامل منابع به شیوه ونکوور بر مبنای ترتیب ظهور در متن)

> **قانون قطعی برای مدل‌های هوش مصنوعی (Absolute Instruction for AI Agents):**  
> هنگام استفاده از این اسکیل در هر سشنی، هرگز ساختارهای قدیمی (نظیر ساختار ۱۴ بخشی) را تولید نکنید. خروجی پروپوزال باید **دقیقاً و مو‌به‌مو شامل این ۲۸ بخش با شماره‌گذاری و عناوین فوق** باشد. عدم رعایت این ۲۸ بخش منجر به رد سند در گیت `MethodologyCompletenessGate` و `ProposalStructureValidator` خواهد شد.

---

## ۲. معماری ۴ لایه‌ای ماژولار نسخه ۹.۰

```text
+-----------------------------------------------------------------------------------+
|                        ProposalReadinessGate (Master Gatekeeper)                  |
+-----------------------------------------------------------------------------------+
        │                                                                   │
        ▼                                                                   ▼
+---------------------------------------+   +---------------------------------------+
|    LAYER 1: SCIENTIFIC ACCURACY       |   |    LAYER 2: STRUCTURAL COMPLIANCE     |
| • BiologicalMechanismVerifier         |   | • MethodologyCompletenessGate (28)    |
| • CombinationHypothesisEngine         |   | • CombinationModelSelector (ANOVA/GLM)|
| • CompoundEntityNormalizer            |   | • Mandatory Sample Size Formula Box   |
+---------------------------------------+   +---------------------------------------+
        │                                                                   │
        ▼                                                                   ▼
+---------------------------------------+   +---------------------------------------+
|    LAYER 3: CITATION INTEGRITY        |   |   LAYER 4: FORMATTING & TYPESETTING   |
| • CitationTracker                     |   | • NativeOmmlMathEngine (LaTeX->OMML)  |
| • Strict Vancouver Order of Appearance|   | • PersianMedicalTypographyLinter      |
| • Orphaned Claim & Unused Ref Auditor |   | • YAML Rules & First-Mention Expansion|
+---------------------------------------+   +---------------------------------------+
```

### لایه ۱: صحت علمی (Scientific Accuracy)
1. **راستی‌آزمای خصمانه مکانیسم‌های بیولوژیک (`BiologicalMechanismAdversarialVerifier`):**
   - دارای هستی‌شناسی ساختارمند از تنظیم‌کننده‌های مرگ برنامه‌ریزی‌شده سلولی (آپوپتوز) و چرخه سلولی (Bcl-2, Bcl-xL, Bax, Bak, Caspases, p53, AKT, PTEN و ...).
   - شناسایی و مسدودسازی وارونگی نقش پروتئین‌ها (نظیر معرفی اشتباه Bcl-xL به عنوان پیش‌آپوپتوزی یا Bax به عنوان ضدآپوپتوزی) با برگرداندن وضعیت `CONTRADICTED`.
2. **موتور فرضیات ترکیب درمانی (`CombinationHypothesisEngine`):**
   - تولید خودکار دو فرضیه موازی و متوازن: فرضیه هم‌افزایی ($H_1$) و فرضیه تضاد / اثر تجمعی ($H_2$).
   - محاسبه شاخص توازن شواهد (`evidence_balance_score`) و صدور اخطار سوگیری شواهد مثبت (`POSITIVE_EVIDENCE_DOMINANCE_WARNING`) در صورت غیبت شواهد منفی یا بی‌اثر.
3. **نرمال‌ساز هویت مواد (`CompoundEntityNormalizer`):**
   - دسته‌بندی مواد در ۴ رده استاندارد: ماده خالص (`PURE_COMPOUND`)، عصاره استاندارد (`STANDARDIZED_EXTRACT`)، عصاره خام گیاهی (`CRUDE_EXTRACT`) و آنالوگ سنتزی (`SYNTHETIC_ANALOG`).
   - پیشگیری قطعی از مغالطه انتساب اثرات عصاره به مولکول خالص بدون ذکر مشخصات خلوص و استانداردسازی.

### لایه ۲: تطابق ساختاری (Structural Compliance)
4. **گیت جامعیت ۲۸ بخشی پژوهشیار (`MethodologyCompletenessGate`):**
   - اعتبارسنجی دقیق و بدون اغماض ۲۸ بخش مصوب فوق.
   - الزام قطعی درج فرمول ریاضی محاسبه حجم نمونه (فرمول کوهن، رابطه تخصیص منابع مید $E = N - B - T$، فرمول کوکران و ...) در بخش ۲۲؛ نبود فرمول مانع کامپایل سند خواهد شد.
5. **انتخاب‌گر مدل آماری ترکیبی (`CombinationModelSelector`):**
   - انتخاب مدل آماری متناسب با طراحی تجربی (مانند Two-Way Factorial ANOVA با ترم اثر متقابل $A \times B$، Repeated Measures ANOVA یا رگرسیون کاکس).
   - تعریف آزمون‌های بررسی پیش‌فرض‌های آماری (نرمالیته، همگنی واریانس‌ها) و آزمون‌های تعقیبی مناسب (Tukey HSD, Bonferroni).

### لایه ۳: تمامیت استنادها (Citation Integrity)
6. **ره‌گیر یکپارچه استنادات (`CitationTracker`):**
   - اعمال دقیق شیوه ونکوور بر مبنای ترتیب ظهور در متن.
   - کشف و گزارش ادعاهای بی‌ارجاع (`Orphaned Claims`) و منابع استفاده‌نشده در کتاب‌شناسی (`Unused References`).
   - شماره‌گذاری و بازآرایی پویای ارجاعات در صورت جابه‌جایی پاراگراف‌ها.

### لایه ۴: فرمت‌بندی و تایپوگرافی (Formatting & Typesetting)
7. **موتور فرمول‌نویسی بومی ورد (`NativeOmmlMathEngine`):**
   - تبدیل کدهای ریاضی لاتک به فرمول‌های استاندارد Office Math Markup Language (`<m:oMath>`, `<m:oMathPara>`) در ساختار XML ورد با پشتیبانی از فال‌بک یونیکد تمیز.
   - حذف کامل و قطعی کدهای لاتک، علامت‌های دلار (`$...$`) و براکت‌های ریاضی از متن سند Word.
8. **لینتر تایپوگرافی پزشکی فارسی (`PersianMedicalTypographyLinter`):**
   - موتور مبتنی بر قوانین (`typography_rules.yaml`) برای تنظیم دقیق نیم‌فاصله‌ها (ZWNJ).
   - تبدیل خودکار ارقام انگلیسی به فارسی در متن با محافظت از فرمول‌های علمی و مارکرهای استنادی.
   - بسط و ترجمه خودکار اختصارات انگلیسی در نخستین اشاره در متن.

### گیت آمادگی جامع (`ProposalReadinessGate`)
- یکپارچه‌ساز و سد نهایی پیش از تولید پروپوزال (Fail-Closed). تا زمانی که وضعیت تمام ۸ ماژول فوق به صورت کامل ارزیابی و تأیید نشود، هیچ سندی کامپایل نخواهد شد.

---

## ۳. اسکریپت‌ها و ماژول‌های اجرایی مهارت (`scripts/`)

- **`proposal_readiness_gate.py`:** گیت جامع آمادگی پیش از تولید سند پروپوزال (v9.0).
- **`biological_mechanism_adversarial_verifier.py`:** راستی‌آزمای بیولوژیک و ناظر بر عدم وارونگی مسیرهای مرگ سلولی و چرخه سلولی (v9.0).
- **`combination_hypothesis_engine.py`:** موتور تولید فرضیات دوگانه ترکیب درمانی و ارزیابی توازن شواهد (v9.0).
- **`compound_entity_normalizer.py`:** نرمال‌ساز هستی‌شناختی مواد دارویی، عصاره‌ها و مشتقات (v9.0).
- **`methodology_completeness_gate.py`:** گیت جامعیت ۲۸ بخشی پژوهشیار با الزام فرمول حجم نمونه (v9.0).
- **`combination_model_selector.py`:** انتخاب‌گر مدل‌های آماری فاکتوریل و اثرات متقابل (v9.0).
- **`citation_tracker.py`:** ره‌گیر استنادات به سبک ونکوور و کاشف ادعاهای بی‌منبع (v9.0).
- **`native_omml_math_engine.py`:** تبدیل‌گر LaTeX به OMML بومی Word و حذف نشت کدهای لاتک (v9.0).
- **`persian_medical_typography_linter.py` & `typography_rules.yaml`:** لینتر قوانین تایپوگرافی، نیم‌فاصله و اصطلاحات پزشکی (v9.0).
- **`research_problem_model.py`:** استخراج و ساخت مدل مسئله پژوهش بر مبنای چارچوب‌های PICO/PECO/Diagnostic/Mechanistic.
- **`generic_search_planner.py`:** طراحی استراتژی جستجوی ۱۶ لایه‌ای، تجزیه ابعاد مسئله پژوهش و نقشه‌برداری اصطلاحات MeSH.
- **`scientific_search_adapter.py`:** آداپتور چندپایگاهی (PubMed, Europe PMC, OpenAlex, Crossref)، تعقیب استنادی سه‌جهته، بنچ‌مارک ریکال و ردیاب اشباع.
- **`generic_reference_auditor.py`:** رکورد ۱۶ فیلدی شواهد کانونی، گیت اصالت داده‌های عددی، گیت مرزهای متنی، ونگاشت ادعا-شواهد بر مبنای SciFact.
- **`generic_evidence_synthesis.py`:** تلفیق چندبعدی شواهد بر پایه ۸ بعد قطعیت، سنتز ساختارمند ۷ نقطه‌ای و تحلیل ریشه‌ای اختلافات.
- **`docx_builder.py`:** ساخت سند نهایی Word با فونت دبی، تگ‌های بومی RTL OpenXML، فرمول‌های OMML و پاراگراف‌های تفصیلی مراجع.
- **`generate_compliant_proposal.py`:** پایپ‌لاین یکپارچه و منطبق بر ۲۸ بخش پژوهشیار با کنترل کامل گیت آمادگی.

---

## ۴. سوئیت جامع آزمون و اعتبارسنجی (`tests/`)

موتور با اجرای دستور زیر ممیزی و آزاد می‌شود:
```bash
python scripts/master_release_gate.py
```
این سیستم به صورت پویا ۱۴ سوئیت آزمون مستقل را اجرا و نتایج زیر را ثبت کرده است:
1. **آزمون نشت کدهای ایستا (`test_hard_code_leakage.py`):** اثبات وجود ۰ کلیدواژه بیولوژیک در کدهای هسته در ۳۱ اسکریپت (۳۱ تست).
2. **آزمون تعمیم‌پذیری ۱۲ گانه دامنه‌ای (`test_generalization.py`):** اجرای کامل پایپ‌لاین روی ۱۲ فیکسچر مستقل (۱۲ تست).
3. **آزمون‌های تنش خصمانه و کنترل‌های منفی ۱۱۴ گانه (`test_adversarial_scenarios.py`):** ۱۱۴ آزمون شامل آداپتور، اشباع، غربالگری و سقف ۲۵ رفرنس (۱۱۴ تست).
4. **سوئیت بنچ‌مارک ۶۰ آزمونه (`self_audit_suite.py`):** اعتبارسنجی ۱۰۰ درصدی طرح‌های تاریخی و رعایت فرمت (۶۰ تست).
5. **سوئیت آزمون جهش‌های علمی (`test_mutations.py`):** آزمون ۱۰ جهش مخرب عمدی با نمره کشندگی ۱۰۰٪ (۱۰ تست).
6. **سوئیت آزمون‌های خاصیت و اسکیمای Draft-07 (`test_property_and_schemas.py`):** ممیزی ناوردایی‌ها و تطابق اسکیماها (۱۴ تست).
7. **سوئیت آزمون‌های یکپارچگی سرتاسری E2E (`test_e2e_integration.py`):** شبیه‌سازی کامل پایپ‌لاین (۲۴ تست).
8. **سوئیت آزمون‌های خصمانه چندموضوعی دامنه‌مستقل (`test_cross_topic_adversarial.py`):** اعتبارسنجی سناریوهای A تا J (۱۱ تست).
9. **سوئیت موتور پژوهش پیشرفته v8.5 (`test_advanced_research_engine.py`):** اعتبارسنجی جستجوی چندپایگاهی و تعقیب استنادی (۲۲ تست).
10. **سوئیت خوانش عمیق و بنچ‌مارک ریکال v8.6 (`test_v86_deep_reading_and_recall_benchmark.py`):** آزمون بخش‌های A-E، رده‌بندی ۸ سطحی شواهد و تاکسونومی ۱۳ گانه (۱۴ تست).
11. **سوئیت اصالت شواهد و نگاشت معنایی v8.7 (`test_v87_evidence_grounding_and_attribution.py`):** آزمون داده‌های عددی، گیت مرزهای متنی و SciFact (۱۴ تست).
12. **سوئیت رگرسیون ممیزی واقعی v8.7 (`test_v87_remediation_regressions.py`):** پیشگیری قطعی از خطاهای انتساب شواهد و رفع سقف‌های تصنعی (۱۰ تست).
13. **سوئیت آزمون‌های خصمانه معماری ماژولار v9.0 (`test_v90_adversarial.py`):** اعتبارسنجی شکست‌های عمدی مکانیسم، سوگیری مثبت، فرمول حجم نمونه، OMML، ونکوور و گیت آمادگی (۱۴ تست).
14. **سوئیت هاردنینگ علمی و اعتبارسنجی ۲۸ بخشی v9.1 (`test_v91_hardening.py`):** اعتبارسنجی ساختار ۲۸ بخشی، گیت جامعیت، عدم نشت لاتک، محافظت از پرانتزهای انگلیسی و ره‌گیری ونکوور (۲۰ تست).

**مجموع آزمون‌ها:** ۳۷۸ آزمون مستقل با قبولی ۱۰۰٪ (378 / 378 PASS)، نمره کشندگی جهش ۱۰۰٪ (10 / 10 KILLED)، عدم نشت کد در تمام اسکریپت‌ها و پاس کامل ۴۳ معیار Master Release Gate.
