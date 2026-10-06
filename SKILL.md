---
name: proposal-nevisi
description: >
  Universal, configuration-driven Iranian medical and biomedical research proposal drafting, deep literature research,
  evidence synthesis, humanization, and Word (.docx) publication engine (v9.0). Operates across diverse biomedical domains
  (oncology, cardiology, infectious diseases, diagnostics, epidemiology, immunology, endocrinology, nephrology, basic experimental science).
  Built on a 4-layer modular architecture (Layer 1: Scientific Accuracy via BiologicalMechanismAdversarialVerifier, CombinationHypothesisEngine,
  CompoundEntityNormalizer; Layer 2: Structural Compliance via MethodologyCompletenessGate validating 28 Pajooheshyar sections and mandatory sample size formula,
  and CombinationModelSelector; Layer 3: Citation Integrity via CitationTracker enforcing Vancouver order-of-appearance, orphaned claim detection, and unused reference filtering;
  Layer 4: Formatting & Typesetting via NativeOmmlMathEngine converting LaTeX to native Word OMML XML <m:oMath>, and PersianMedicalTypographyLinter
  enforcing ZWNJ, Persian numerals, and abbreviation expansions). Enforces ProposalReadinessGate as a fail-closed pre-generation gatekeeper.
  Supports multi-source federated searches (PubMed, Europe PMC, OpenAlex, Crossref), 16 query families, MeSH mapping, multi-directional citation chasing,
  saturation tracking, deep paper reading (Sections A-E), SciFact-aligned claim verification, 8-tier evidence hierarchy,
  and passes a unified 350-assertion test harness across 13 suites and 43 release gate criteria with zero hardcoded biological leakage across all 31 engine scripts.
---

# Proposal-Nevisi (موتور جامع، ماژولار و مبتنی بر شواهد نگارش پروپوزال‌های علوم پزشکی v9.0)

این مهارت یک پلتفرم جامع، تعاملی، کاملاً ماژولار، مستقل از موضوع (Topic-Agnostic) و مبتنی بر شواهد برای تدوین پروپوزال‌های پژوهشی علوم پزشکی و زیست‌پزشکی در بالاترین تراز دانشگاهی و استانداردهای پژوهشی کشور است.

نسخه ۹.۰ تمام منطق‌های شرطی شکننده و وابسته به موضوع را به طور کامل حذف کرده و معماری ماژولار ۴ لایه‌ای زیر را با سد بازدارنده آمادگی (`ProposalReadinessGate`) پیاده‌سازی نموده است:

---

## ۱. معماری ۴ لایه‌ای ماژولار نسخه ۹.۰

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
   - اعتبارسنجی دقیق و بدون اغماض ۲۸ بخش استاندارد سامانه پژوهشیار (وزارت بهداشت).
   - الزام قطعی درج فرمول ریاضی محاسبه حجم نمونه (فرمول کوهن، رابطه تخصیص منابع مید $E = N - B - T$، فرمول کوکران و ...) در بخش ۱۰؛ نبود فرمول مانع کامپایل سند خواهد شد.
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

## ۲. اسکریپت‌ها و ماژول‌های اجرایی مهارت (`scripts/`)

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

## ۳. سوئیت جامع آزمون و اعتبارسنجی (`tests/`)

موتور با اجرای دستور زیر ممیزی و آزاد می‌شود:
```bash
python scripts/master_release_gate.py
```
این سیستم به صورت پویا ۱۳ سوئیت آزمون مستقل را اجرا و نتایج زیر را ثبت کرده است:
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

**مجموع آزمون‌ها:** ۳۵۰ آزمون مستقل با قبولی ۱۰۰٪ (350 / 350 PASS)، نمره کشندگی جهش ۱۰۰٪ (10 / 10 KILLED)، عدم نشت کد در ۳۱ اسکریپت و پاس کامل ۴۳ معیار Master Release Gate.
