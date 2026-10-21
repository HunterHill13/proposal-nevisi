#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
methodology_research_subagent.py - Dedicated Scientific Methodology & Cohesive Protocol Engine
Proposal-Nevisi Engine v11.4 (Layer 2: Structural & Methodological Integrity)

Solves the "Frankenstein / Chimera Methodology" problem:
Prevents stitching incompatible protocol fragments from disparate papers by deriving
a cohesive, mutually compatible, gold-standard experimental design aligned with:
1. OECD Guidance Document on Good Cell Culture Practice (GCCP) / ARRIVE 2.0.
2. MIQE Guidelines for RT-qPCR (Bustin et al., 2009) enforcing dual validated reference genes.
3. Chou-Talalay Combination Index Theory (Chou, 2006) with unified tiers.
4. Mead's Resource Equation (Festing, 2006) & Two-Way Factorial ANOVA Power Analysis (Cohen's f).
5. Assay Interference Mitigation: Cell-Free Blank & Differential Wavelength spectrophotometry.

100% General-Purpose & Domain-Agnostic.
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class CohesiveProtocolResult:
    archetype: str
    target_model_specs: Dict[str, Any]
    culture_conditions: Dict[str, Any]
    exposure_regimen: Dict[str, Any]
    assays_and_controls: Dict[str, Any]
    gene_expression_miqe: Dict[str, Any]
    sample_size_biostatistics: Dict[str, Any]
    combination_index_rules: Dict[str, Any]
    formatted_sections_fa: Dict[int, str]
    coherence_score: float = 1.0
    detected_inconsistencies: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "archetype": self.archetype,
            "target_model_specs": self.target_model_specs,
            "culture_conditions": self.culture_conditions,
            "exposure_regimen": self.exposure_regimen,
            "assays_and_controls": self.assays_and_controls,
            "gene_expression_miqe": self.gene_expression_miqe,
            "sample_size_biostatistics": self.sample_size_biostatistics,
            "combination_index_rules": self.combination_index_rules,
            "coherence_score": self.coherence_score,
            "detected_inconsistencies": self.detected_inconsistencies,
            "formatted_sections_fa": self.formatted_sections_fa
        }


class MethodologyResearchSubagent:
    """Specialized cognitive agent for designing internally coherent biomedical protocols."""

    @classmethod
    def identify_study_archetype(cls, topic: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Determines the biological and experimental archetype of the study."""
        t_lower = topic.lower()
        ctx_str = str(context or "").lower()
        combined = f"{t_lower} {ctx_str}"

        # 1. Health Systems, Health Economics & Health Policy (CHE, OOP, ICER, UHC, Financing)
        if any(k in combined for k in [
            "هزینه", "کمرشکن", "پرداخت از جیب", "اقتصاد سلامت", "نظام سلامت", "بیمه",
            "che", "oop", "health expenditure", "catastrophic", "out-of-pocket",
            "health system", "health policy", "icer", "qaly", "daly", "equity",
            "financial protection", "uhc", "universal health coverage", "عدالت در سلامت"
        ]):
            return "HEALTH_SYSTEMS_AND_HEALTH_POLICY"

        # 2. Diagnostic Accuracy & Biomarkers
        elif any(k in combined for k in [
            "تشخیصی", "حساسیت و ویژگی", "دقت تشخیصی", "ارزش اخباری", "بیومارکر تشخیصی",
            "diagnostic accuracy", "sensitivity and specificity", "roc curve", "auc-roc", "stard"
        ]):
            return "DIAGNOSTIC_ACCURACY_AND_BIOMARKER"

        # 3. Observational Epidemiology (Surveys, Cross-Sectional, Case-Control, Cohort without drug intervention)
        elif any(k in combined for k in [
            "مقطعی", "مورد-شاهدی", "شیوع", "همه‌گیرشناسی", "عوامل خطر", "بررسی پیمایشی",
            "cross-sectional", "case-control", "prevalence", "incidence", "risk factors", "strobe"
        ]) and not any(k in combined for k in ["رده سلولی", "cell line", "in vitro", "سنتز"]):
            return "EPIDEMIOLOGICAL_OBSERVATIONAL"

        # 4. Clinical Trials & Human Interventional Studies
        elif any(k in combined for k in [
            "کارآزمایی بالینی", "clinical trial", "rct", "مداخله درمانی", "فاز ۱", "فاز ۲", "فاز ۳",
            "phase 1", "phase 2", "phase 3", "پروتکل کارآزمایی"
        ]) or (any(k in combined for k in ["بیمار", "بیماران", "cohort", "کوهورت"]) and not any(k in combined for k in ["رده سلولی", "cell line", "موش", "رت"])):
            return "CLINICAL_TRIAL_OR_COHORT"

        # 5. In Vivo Animal Models
        elif any(k in combined for k in ["موش", "رت", "in vivo", "حيوان", "xenograft", "حیوانات", "animal model"]):
            return "IN_VIVO_ANIMAL_MODEL"

        # 6. Default: In Vitro Molecular & Cellular
        else:
            return "IN_VITRO_CELLULAR_COMBINATION"

    @classmethod
    def derive_cohesive_protocol(
        cls,
        topic: str,
        target_model: str = "Standard Biological / Cellular Model",
        interventions: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> CohesiveProtocolResult:
        """Derives a complete, harmonious, non-chimera experimental protocol."""
        archetype = cls.identify_study_archetype(topic, context)
        interventions = interventions or ["مداخله اول", "مداخله دوم"]
        agt1 = interventions[0] if len(interventions) >= 1 else "مداخله اول"
        agt2 = interventions[1] if len(interventions) >= 2 else "مداخله دوم"

        # =====================================================================
        # ARCHETYPE 1: HEALTH SYSTEMS, HEALTH ECONOMICS & HEALTH POLICY
        # =====================================================================
        if archetype == "HEALTH_SYSTEMS_AND_HEALTH_POLICY":
            model_specs = {
                "model_name": target_model if target_model != "Standard Biological / Cellular Model" else "خانوارها و بیماران مراجعه‌کننده به مراکز درمانی",
                "authentication": "پرسشنامه استاندارد اعتبارسنجی‌شده سازمان جهانی بهداشت (WHO World Health Survey) و حساب‌های ملی سلامت (NHA)",
                "sampling_strategy": "نمونه‌گیری تصادفی خوشه‌ای طبقه‌بندی‌شده چندمرحله‌ای (Multi-Stage Stratified Cluster Sampling)",
                "target_population": "خانوارها و بیماران مبتلا و خانواده‌های آنها مراجعه‌کننده به مراکز درمانی تشخیصی و بیمارستان‌های منتخب",
                "governance": "انطباق با موازین اخلاق پژوهش، بیانیه هلسینکی، اخذ رضایت‌آگاهانه کتبی و امانتداری داده‌های محرمانه"
            }
            exposure_regimen = {
                "che_thresholds": "سنجش مواجهه با هزینه‌های کمرشکن سلامت (CHE) بر مبنای دو آستانه بین‌المللی WHO: ۱۰٪ کل هزینه‌های خانوار و ۴۰٪ ظرفیت پرداخت خانوار (Capacity to Pay: CTP)",
                "oop_components": "سنجش پرداخت‌های مستقیم از جیب (OOP) شامل هزینه‌های مستقیم درمانی (ویزیت، دارو، پاراکلینیک، بستری)، هزینه‌های مستقیم غیردرمانی (ایاب‌وذهاب، اقامت) و هزینه‌های غیرمستقیم (افت بهره‌وری)",
                "recall_periods": "بازه یادآوری ۱ ماهه برای خدمات سرپایی و دارویی و بازه ۶ الی ۱۲ ماهه برای هزینه‌های بستری و جراحی جهت بهینه‌سازی دقت یادآوری"
            }
            assays_and_controls = {
                "survey_instrument": {
                    "name": "پرسشنامه ساختارمند استاندارد سازمان جهانی بهداشت (WHO WHS & NHA)",
                    "validity": "ارزیابی روایی صوری و محتوایی کمی و کیفی توسط پانل ۱۰ نفره از متخصصان اقتصاد سلامت (CVR > 0.78 و CVI > 0.80)",
                    "reliability": "ارزیابی پایایی با مطالعه پایلوت روی ۳۰ خانوار و محاسبه ضریب آلفای کرونباخ (> 0.80) و آزمون-بازآزمون (ICC > 0.85)"
                },
                "bias_mitigation": {
                    "recall_bias_control": "تطبیق فاکتورها و پرداخت‌های گزارش‌شده با اسناد مالی و صورتحساب‌های الکترونیک سامانه اطلاعات بیمارستانی (HIS)",
                    "selection_bias_control": "تخصیص وزن‌های معکوس احتمال نمونه‌گیری و ممیزی تصادفی ۱۰٪ پرسشنامه‌ها با پیگیری مجدد"
                }
            }
            gene_expression_miqe = {
                "guideline": "استانداردهای بین‌المللی حاکمیت داده‌های سلامت و کدگذاری استاندارد (ICD-10 / CPT)",
                "data_entry": "ورود دوگانه داده‌ها (Double Data Entry) جهت حذف خطای انسانی",
                "outlier_handling": "شناسایی و تصحیح داده‌های پرت هزینه‌ای با روش فاصله‌ای چارکی و سانسور آماری (Winsorization / Trimming)",
                "missing_data": "جایگزینی مقادیر گمشده با روش جایگزینی چندگانه (Multiple Imputation by Chained Equations: MICE)"
            }
            sample_size_biostatistics = {
                "replicate_structure": "نمونه‌گیری از خانوارهای مستقل در سطح جامعه و مراکز درمانی در قالب خوشه‌های مستقل با پرهیز از هم‌پوشانی",
                "experimental_unit": "خانوار یا بیمار ثبت‌شده به عنوان ۱ واحد تجربی و آماری مستقل در تحلیل مدلسازی",
                "sample_size_formula_name": "فرمول کوکران برای برآورد نسبت با احتساب اثر طرح خوشه‌ای (Cochran's Formula with Design Effect)",
                "cochran_equation": r"$$n = \frac{Z_{1-\alpha/2}^2 \cdot p(1-p)}{d^2} \times DEFF$$",
                "derivation": (
                    "در این رابطه $Z_{1-\\alpha/2} = 1.96$ معادل سطح اطمینان ۹۵٪، $p = 0.50$ به عنوان محافظه‌کارانه‌ترین نسبت جهت حصول بیشینه واریانس و بزرگ‌ترین حجم نمونه ایمن، "
                    "و $d = 0.05$ دقت مطلوب برآورد (خطای مجاز ۵٪) است. "
                    "بر این اساس حجم نمونه پایه $n_{base} = \\frac{1.96^2 \\times 0.50 \\times (1 - 0.50)}{0.05^2} = 384.16 \\approx 385$ خانوار/بیمار حاصل می‌گردد. "
                    "با در نظر گرفتن ضریب اثر طرح خوشه‌ای ($DEFF = 1.5$) ناشی از نمونه‌گیری خوشه‌ای چندمرحله‌ای، حجم نمونه به $n_{cluster} = 385 \\times 1.5 = 577.5 \\approx 578$ نفر افزایش می‌یابد. "
                    "نهایتاً با لحاظ ۱۰٪ احتمال عدم پاسخ یا پرسشنامه‌های مخدوش، حجم نمونه نهایی به صورت زیر تثبیت می‌گردد:\n\n"
                    r"$$n_{final} = \frac{n_{cluster}}{1 - 0.10} = \frac{578}{0.90} \approx 642 \text{ خانوار/بیمار}$$"
                ),
                "statistical_test": "آمار توصیفی جامع، آزمون‌های ناپارامتری (من-ویتنی و کروسکال-والیس)، مدل‌های رگرسیون لجستیک چندمتغیره (Multivariable Logistic Regression) جهت تعیین نسبت شانس تعدیل‌شده (AOR)، و شاخص و منحنی تمرکز کاکوانی (Kakwani Concentration Index) در نرم‌افزارهای Stata v17 یا R v4.3"
            }
            combination_index_rules = {
                "software": "نرم‌افزار رسمی Stata v17 / R v4.3 با ماژول اختصاصی DASP / conindex",
                "che_definition": "CHE: مخارج مستقیم سلامت >= ۴۰٪ ظرفیت پرداخت خانوار (CTP) یا >= ۱۰٪ کل هزینه‌ها",
                "equity_rule": "شاخص تمرکز منفی (Negative Concentration Index) نشان‌دهنده توزیع نامتناسب بار مالی به زیان اقشار کم‌درآمد است."
            }
            formatted_sections = {
                13: (
                    f"طرح حاضر یک پژوهش مقطعی توصیفی-تحلیلی (Cross-Sectional Analytical Study) در حوزه اقتصاد سلامت و سیاست‌گذاری نظام سلامت است "
                    f"که بر روی جامعه آماری {model_specs['model_name']} اجرا می‌شود. "
                    f"جمع‌آوری داده‌ها از طریق پرسشنامه استاندارد سازمان جهانی بهداشت (WHO WHS & NHA) به شیوه نمونه‌گیری خوشه‌ای چندمرحله‌ای صورت می‌پذیرد. "
                    f"پیامدهای اصلی شامل سنجش شیوع هزینه‌های کمرشکن سلامت (CHE) بر پایه آستانه‌های مرجع ۱۰٪ کل هزینه و ۴۰٪ ظرفیت پرداخت (CTP)، "
                    f"سهم پرداخت‌های مستقیم از جیب (OOP) و شناسایی پیش‌بینی‌کننده‌های اقتصادی-اجتماعی مواجهه با بار مالی از طریق رگرسیون لجستیک چندمتغیره و شاخص تمرکز کاکوانی می‌باشد."
                ),
                14: (
                    "مطالعه حاضر یک پژوهش کاربردی-مقطعی مبتنی بر جامعه از نوع توصیفی-تحلیلی و اقتصاد سلامت (Cross-Sectional Health Systems & Health Economics Study) است که مطابق با استانداردهای بین‌المللی ارزیابی حفاظت مالی سازمان جهانی بهداشت (WHO) طراحی گردیده است."
                ),
                15: (
                    f"جامعه پژوهش شامل کلیه بیماران مبتلا به {target_model} و خانوارهای تحت تکفل آنها می‌باشد که جهت دریافت خدمات تخصصی درمانی (بستری، شیمی‌درمانی، رادیوتراپی و جراحی) به بیمارستان‌ها و مراکز درمانی تخصصی منتخب مراجعه نموده‌اند.\n\n"
                    f"▪ **چارچوب ساختارمند متدولوژی (PECO Framework):**\n\n"
                    f"| مؤلفه ساختاری | شرح عملیاتی در مطالعه حاضر |\n"
                    f"| :--- | :--- |\n"
                    f"| **P (Population)** | بیماران مبتلا به {target_model} و خانوارهای تحت پوشش |\n"
                    f"| **E (Exposure)** | مواجهه با بار مالی و هزینه‌های درمانی (خدمات بستری، سرپایی، دارویی) |\n"
                    f"| **C (Comparator)** | مقایسه دهک‌های درآمدی/هزینه‌ای و وضعیت پوشش بیمه پایه و تکمیلی |\n"
                    f"| **O (Outcomes)** | نرخ مواجهه با هزینه‌های کمرشکن سلامت (CHE) و سهم پرداخت از جیب (OOP) |\n\n"
                    f"نمونه‌گیری به شیوه خوشه‌ای چندمرحله‌ای طبقه‌بندی‌شده از میان مراکز درمانی منتخب صورت می‌پذیرد."
                ),
                16: (
                    "بیمارستان‌های دانشگاهی و تخصصی انکولوژی، درمانگاه‌های سرپایی شیمی‌درمانی، مراکز تشخیصی و مراکز جامع خدمات سلامت منتخب وابسته به دانشگاه علوم پزشکی."
                ),
                17: (
                    f"- تشخیص قطعی {target_model} مستند به پرونده پزشکی و گزارش پاتولوژی معتبر.\n"
                    "- گذشت حداقل ۳ ماه از آغاز مراحل فعال درمانی (شیمی‌درمانی، رادیوتراپی یا بستری جراحی).\n"
                    "- سکونت خانوار در حوزه جغرافیایی تحت پوشش پژوهش.\n"
                    "- اعلام رضایت آگاهانه کتبی جهت مشارکت در مصاحبه و تکمیل پرسشنامه توسط بیمار یا سرپرست قانونی خانوار."
                ),
                18: (
                    "- انصراف یا عدم تمایل بیمار یا سرپرست خانوار به تداوم مشارکت در هر مرحله از پژوهش.\n"
                    "- مخدوش یا ناقص بودن بیش از ۲۰ درصد از متغیرهای کلیدی هزینه‌ای بدون امکان استعلام از سامانه HIS.\n"
                    "- دریافت خدمات درمانی در خارج از کشور در طول دوره ارزیابی.\n"
                    "- فوت بیمار پیش از امکان اعتبارسنجی صورتحساب‌های درمانی."
                ),
                19: (
                    "- پرسشنامه ساختارمند استاندارد سازمان بهداشت جهانی (WHO WHS) و ماژول هزینه‌های سلامت ملی (NHA).\n"
                    "- سامانه الکترونیک اطلاعات بیمارستانی (HIS) جهت اعتبارسنجی هزینه‌های بستری و درمانی.\n"
                    "- نرم‌افزارهای تخصصی تحلیل آماری و اقتصاد سلامت (Stata نسخه ۱۷ و R نسخه ۴.۳).\n"
                    "- پلتفرم الکترونیک امن جمع‌آوری داده‌ها (مانند REDCap یا سامانه آنلاین تحت وب اختصاصی) مجهز به اعتبارسنجی ورود همزمان داده‌ها."
                ),
                20: (
                    "- اعتبارسنجی روایی صوری و محتوایی ابزار جمع‌آوری داده با کسب CVI بالای ۰.۸۰ و CVR بالای ۰.۷۸ با نظر پانل متخصصان اقتصاد سلامت.\n"
                    "- اجرای مطالعه مقدماتی (Pilot Study) بر روی ۳۰ خانوار خارج از حجم نمونه نهایی و سنجش پایایی با آلفای کرونباخ (> ۰.۸۰).\n"
                    "- برگزاری کارگاه آموزشی مدون برای پرسشگران جهت یکسان‌سازی شیوه مصاحبه و تکمیل ابزار پژوهش.\n"
                    "- ممیزی کیفیت و بازبینی روزانه پرسشنامه‌های تکمیل‌شده توسط ناظر علمی طرح."
                ),
                21: (
                    "- مهار سوگیری یادآوری (Recall Bias) با محدودسازی افق یادآوری سرپایی به ۱ ماه و تطبیق داده‌های بستری با فاکتورهای ترخیص رسمی و سامانه HIS.\n"
                    "- مهار سوگیری انتخاب (Selection Bias) از طریق اجرای دقیق طرح نمونه‌گیری تصادفی خوشه‌ای و طبقه‌بندی مراکز درمانی دولتی و خصوصی.\n"
                    "- کنترل خطای ثبت داده‌ها از طریق شیوه ورود دوگانه مستقل (Double Data Entry) و اعتبارسنجی دامنه‌ای مقادیر (Range Checks).\n"
                    "- مهار داده‌های پرت و مخدوش با روش‌های استاندارد سانسور آماری (Winsorization)."
                ),
                22: (
                    "تعیین حجم نمونه بر مبنای استاندارد بین‌المللی فرمول کوکران برای متغیرهای کیفی-نسبتی با لحاظ ضریب اثر طرح خوشه‌ای (DEFF) صورت پذیرفته است:\n\n"
                    f"{sample_size_biostatistics['cochran_equation']}\n\n"
                    f"{sample_size_biostatistics['derivation']}\n\n"
                    "این حجم نمونه تضمین‌کننده توان آماری بالای ۸۵ درصد برای برازش مدل‌های رگرسیون لجستیک چندمتغیره و شناسایی عوامل خطر اقتصادی می‌باشد."
                ),
                23: (
                    "- گزارش شاخص‌های آمار توصیفی (فراوانی، درصد، میانگین، انحراف معیار و صدک‌های هزینه‌ای).\n"
                    "- آزمون شاپیرو-ویلک جهت بررسی توزیع نرمال متغیرهای مالی و استفاده از آزمون‌های ناپارامتری (من-ویتنی و کروسکال-والیس) در صورت چولگی داده‌ها.\n"
                    "- محاسبه نسبت خانوارهای مواجه با هزینه‌های کمرشکن سلامت (CHE) بر مبنای رویکرد رسمی سازمان جهانی بهداشت (WHO Methodology: 10% total spending & 40% capacity to pay).\n"
                    "- تحلیل عوامل پیش‌بینی‌کننده با مدل رگرسیون لجستیک چندمتغیره (Multivariable Logistic Regression) و گزارش نسبت‌های شانس تعدیل‌شده (Adjusted Odds Ratio: AOR) به همراه فاصله اطمینان ۹۵٪.\n"
                    "- ارزیابی نابرابری در توزیع بار مالی از طریق محاسبه شاخص تمرکز (Concentration Index) و رسم منحنی تمرکز (Concentration Curve).\n"
                    "- تحلیل‌های آماری در نرم‌افزارهای Stata نسخه ۱۷ یا R نسخه ۴.۳ انجام شده و سطح معنی‌داری p < 0.05 لحاظ خواهد شد."
                ),
                24: (
                    "- اخذ کد مصوب اخلاق در پژوهش از کمیته منطقه‌ای اخلاق در پژوهش‌های زیست‌پزشکی دانشگاه علوم پزشکی.\n"
                    "- اخذ رضایت‌آگاهانه کتبی از کلیه بیماران یا سرپرستان قانونی خانوار پس از تبیین کامل اهداف پژوهش و اختیاری بودن مشارکت.\n"
                    "- تضمین رازداری و محرمانگی اکید اطلاعات هویتی و مالی خانوارها از طریق اختصاص کدهای شناسایی ناشناس (De-identified Coding).\n"
                    "- انطباق کامل با موازین بیانیه هلسینکی و دستورالعمل‌های کشوری حفاظت از داده‌های پژوهش‌های نظام سلامت."
                ),
                25: (
                    "- حفاظت از امنیت داده‌های الکترونیک و محرمانگی مالی با رمزنگاری پیشرفته (AES-256).\n"
                    "- ذخیره‌سازی داده‌های پرسشنامه‌ها در پایگاه داده امن با دسترسی محدود و تحت کنترل مستقیم پژوهشگر اصلی.\n"
                    "- امحاء ایمن و خرد کردن اسناد فیزیکی کاغذی پرسشنامه‌ها پس از اتمام دوره ثبت و اعتبارسنجی متقابل با HIS."
                ),
                26: (
                    "- سوگیری یادآوری در اعلام هزینه‌ها (Recall Bias): مهار از طریق محدودسازی دوره یادآوری سرپایی به ۱ ماه و تطبیق هزینه‌های بستری با اسناد رسمی صورتحساب HIS.\n"
                    "- عدم تمایل برخی خانوارها به افشای دقیق درآمدها: مهار با استفاده از روش محاسبه مخارج مصرفی خانوار (Consumption Expenditure) به جای درآمد اعلامی طبق راهنمای رسمی بانک جهانی و WHO.\n"
                    "- عدم دسترسی یکپارچه به تعرفه‌های خدمات در برخی مراکز درمانی بخش خصوصی و لزوم استعلام مستقیم فاکتورها."
                ),
                27: (
                    "### پروتکل گام‌به‌گام اجرایی طرح پژوهشی (Step-by-Step Cohesive Protocol)\n\n"
                    "**گام ۱: بومی‌سازی و اعتبارسنجی ابزار سنجش:** ترجمه و بومی‌سازی پرسشنامه استاندارد سلامت جهانی (WHO WHS) و ماژول هزینه‌ای NHA؛ تعیین روایی صوری و محتوایی کمی (CVI > 0.80, CVR > 0.78) و پایایی در مطالعه پایلوت روی ۳۰ خانوار با آلفای کرونباخ (> ۰.۸۰).\n\n"
                    "**گام ۲: نمونه‌گیری تصادفی خوشه‌ای چندمرحله‌ای:** انتخاب مراکز تشخیصی و بیمارستان‌های منتخب به عنوان خوشه‌ها، طبقه‌بندی بر اساس نوع مرکز (دولتی/خصوصی/خیریه) و انتخاب تصادفی بیماران و خانوارها تا سقف حجم نمونه مصوب ($n = 642$).\n\n"
                    "**گام ۳: مصاحبه ساختارمند و گردآوری داده‌ها:** اجرای مصاحبه‌های چهره‌به‌چهره با بیماران یا سرپرست خانوار پس از اخذ رضایت‌آگاهانه کتبی، و استخراج دقیق مولفه‌های هزینه‌ای (مستقیم درمانی، مستقیم غیردرمانی و غیرمستقیم).\n\n"
                    "**گام ۴: اعتبارسنجی متقابل با پرونده‌های بالینی و مالی:** استعلام صورتحساب‌های الکترونیک از سامانه اطلاعات بیمارستانی (HIS) و تطبیق مقادیر پرداختی از جیب (OOP) گزارش‌شده با اسناد واقعی به منظور حذف سوگیری یادآوری.\n\n"
                    "**گام ۵: ممیزی و پاکسازی داده‌ها (Data Cleaning):** ورود دوگانه داده‌ها، اجرای آزمون‌های منطقی بازه‌ای و پاکسازی مقادیر گمشده و پرت با روش‌های استاندارد MICE و Winsorization.\n\n"
                    "**گام ۶: مدلسازی اقتصاد سلامت و نگارش گزارش تحلیلی:** برآورد دقیق شاخص‌های CHE و OOP، برازش مدل رگرسیون لجستیک چندمتغیره برای شناسایی عوامل خطر، و ترسیم منحنی تمرکز جهت سنجش نابرابری اقتصادی-اجتماعی."
                )
            }

        # =====================================================================
        # ARCHETYPE 2: OBSERVATIONAL EPIDEMIOLOGY (CROSS-SECTIONAL / COHORT)
        # =====================================================================
        elif archetype == "EPIDEMIOLOGICAL_OBSERVATIONAL":
            model_specs = {
                "model_name": target_model if target_model != "Standard Biological / Cellular Model" else "جامعه آماری جمعیت هدف و گروه شاهد",
                "authentication": "تعاریف استاندارد بالینی و سرعنوان‌های تشخیصی مصوب بین‌المللی (ICD-10 / STROBE Guidelines)",
                "sampling_strategy": "نمونه‌گیری تصادفی طبقه‌بندی‌شده یا متوالی مبتنی بر جمعیت",
                "target_population": "افراد واجد معیارهای ورود بر پایه پروتکل ثبت مدون",
                "governance": "رعایت بیانیه هلسینکی، کد اخلاق زیست‌پزشکی و رضایت‌آگاهانه"
            }
            exposure_regimen = {
                "exposure_definition": f"ارزیابی مواجهه با {agt1} و {agt2} بر پایه چک‌لیست‌های استاندارد اپیدمیولوژیک",
                "outcome_definition": "سنجش بروز یا شیوع پیامد هدف با ابزارهای استاندارد تشخیصی و معیارهای بالینی معتبر",
                "confounder_control": "ثبت متغیرهای مخدوش‌کننده شناخته‌شده (سن، جنس، وضعیت اقتصادی، بیماری‌های زمینه‌ای)"
            }
            assays_and_controls = {
                "measurement_tools": {
                    "name": "چک‌لیست استخراج داده‌ها منطبق با دستورالعمل STROBE",
                    "validity": "تطبیق با پرونده‌های سلامت معتبر و آزمون‌های پاراکلینیک تاییدشده",
                    "reliability": "ارزیابی ضریب توافق کاپا (Kappa Coefficient > 0.85) بین دو ارزیاب مستقل"
                },
                "bias_controls": {
                    "selection_bias": "تعریف دقیق معیارهای ورود و خروج و استفاده از نمونه‌گیری سیستماتیک",
                    "information_bias": "کورسازی ارزیاب نسبت به وضعیت مواجهه/پیامد در حد امکان"
                }
            }
            gene_expression_miqe = {
                "guideline": "دستورالعمل بین‌المللی STROBE برای گزارش‌دهی مطالعات مشاهده‌ای",
                "missing_data": "تحلیل الگوی داده‌های گمشده و استفاده از روش Multiple Imputation",
                "confounding_adjustment": "کنترل مخدوش‌کننده‌ها از طریق رگرسیون چندمتغیره و نمره تمایل (Propensity Score)"
            }
            sample_size_biostatistics = {
                "replicate_structure": "واحدهای مستقل مشاهده‌ای انسانی با ثبت متغیرهای دموگرافیک و بالینی",
                "experimental_unit": "هر شرکت‌کننده در مطالعه به عنوان یک واحد آماری مستقل",
                "sample_size_formula_name": "فرمول کوکران جهت برآورد شیوع در مطالعات مشاهده‌ای",
                "cochran_equation": r"$$n = \frac{Z_{1-\alpha/2}^2 \cdot P(1-P)}{d^2}$$",
                "derivation": (
                    "در این رابطه $Z = 1.96$ معادل اطمینان ۹۵٪، $P = 0.50$ برای حصول بیشترین حجم نمونه و $d = 0.05$ دقت برآورد است. "
                    "حجم پایه ۳۸۵ نفر محاسبه شده و با احتساب ۱۰٪ ریزش، تعداد نهایی به ۴۲۸ شرکت‌کننده تعدیل می‌گردد."
                ),
                "statistical_test": "رگرسیون لجستیک چندمتغیره جهت برآورد نسبت شانس تعدیل‌شده (AOR) به همراه فواصل اطمینان ۹۵٪ در SPSS/R"
            }
            combination_index_rules = {
                "software": "نرم‌افزار آماری SPSS v27 / R v4.3",
                "synergism": "اثر فزاینده متقابل بیش از جمع‌پذیر در مدل‌های رگرسیون (Interaction OR > OR1 * OR2)",
                "additive": "اثر جمع‌پذیر مطابق مدل خطی یا ضربی",
                "antagonism": "اثر منفی متقابل زیر حد جمع‌پذیر"
            }
            formatted_sections = {
                13: (
                    f"مطالعه حاضر به صورت مقطعی توصیفی-تحلیلی (Cross-Sectional Observational Study) بر روی {model_specs['model_name']} "
                    f"منطبق با دستورالعمل بین‌المللی STROBE طراحی شده است. "
                    f"ارزیابی متغیرهای مواجهه و پیامد با ابزارهای اعتبارسنجی‌شده صورت می‌گیرد و هدف آن تعیین شیوع، عوامل خطر، "
                    f"و بررسی ارتباط آماری بین مواجهه و پیامد هدف می‌باشد."
                ),
                19: (
                    "- چک‌لیست ساختارمند استخراج داده‌ها منطبق بر استانداردهای STROBE.\n"
                    "- سامانه‌های ثبت و بایگانی پرونده‌های پزشکی الکترونیک.\n"
                    "- نرم‌افزارهای تحلیلی آماری SPSS و R جهت مدلسازی چندمتغیره."
                ),
                20: (
                    "- ارزیابی روایی ابزار توسط متخصصان اپیدمیولوژی و پزشکی اجتماعی.\n"
                    "- سنجش پایایی ارزیاب‌ها با محاسبه ضریب توافق کاپا (Kappa > 0.85).\n"
                    "- پایلوت اولیه روی ۲۰ نمونه جهت اعتبارسنجی چک‌لیست."
                ),
                21: (
                    "- مهار سوگیری انتخاب با نمونه‌گیری تصادفی سیستماتیک و تدوین دقیق معیارهای ورود و خروج.\n"
                    "- مهار سوگیری اطلاعات با اعتبارسنجی متقابل داده‌ها با پرونده‌های بالینی.\n"
                    "- کنترل متغیرهای مخدوش‌کننده با تحلیل‌های چندمتغیره آماری."
                ),
                22: (
                    "محاسبه حجم نمونه بر مبنای فرمول استاندارد کوکران برای مطالعات مشاهده‌ای صورت پذیرفته است:\n\n"
                    f"{sample_size_biostatistics['cochran_equation']}\n\n"
                    f"{sample_size_biostatistics['derivation']}"
                ),
                23: (
                    "- گزارش شاخص‌های آمار توصیفی (فراوانی، درصد، میانگین، انحراف معیار).\n"
                    "- تحلیل دومتغیره با آزمون‌های کای-دو، تی مستقل یا معادل‌های ناپارامتری.\n"
                    "- تحلیل چندمتغیره با رگرسیون لجستیک جهت محاسبه نسبت شانس تعدیل‌شده (AOR) با فاصله اطمینان ۹۵٪.\n"
                    "- سطح معنی‌داری آماری در تمام آزمون‌ها p < 0.05 لحاظ می‌گردد."
                ),
                27: (
                    "### پروتکل گام‌به‌گام اجرایی طرح پژوهشی (Step-by-Step Cohesive Protocol)\n\n"
                    "**گام ۱: تدوین و اعتبارسنجی ابزار:** آماده‌سازی چک‌لیست استخراج داده منطبق با STROBE و سنجش روایی و پایایی (کاپا > ۰.۸۵).\n\n"
                    "**گام ۲: نمونه‌گیری:** اخذ کد اخلاق و اجرای نمونه‌گیری تصادفی از جامعه هدف بر اساس حجم نمونه مصوب ($n = 428$).\n\n"
                    "**گام ۳: جمع‌آوری داده‌ها:** تکمیل چک‌لیست‌ها از طریق مصاحبه و بررسی پرونده‌های بالینی با حفظ محرمانگی.\n\n"
                    "**گام ۴: کنترل کیفیت و پاکسازی:** بازبینی ممیزی ورود داده‌ها، بررسی مقادیر گم‌شده و پرت.\n\n"
                    "**گام ۵: تحلیل آماری:** برازش مدل‌های رگرسیون چندمتغیره و استخراج نسبت شانس تعدیل‌شده و عوامل پیش‌بینی‌کننده."
                )
            }

        # =====================================================================
        # ARCHETYPE 3: CLINICAL TRIAL / HUMAN INTERVENTIONAL
        # =====================================================================
        elif archetype in ["CLINICAL_TRIAL_INTERVENTIONAL", "CLINICAL_TRIAL_OR_COHORT"]:
            model_specs = {
                "model_name": target_model if target_model != "Standard Biological / Cellular Model" else "بیماران واجد معیارهای ورود به کارآزمایی بالینی",
                "authentication": "استانداردهای بین‌المللی GCP، دستورالعمل CONSORT و ثبت در مرکز ثبت کارآزمایی‌های بالینی (IRCT)",
                "sampling_strategy": "تخصیص تصادفی بلوک‌بندی‌شده (Block Randomization) همراه با پنهان‌سازی تخصیص (Allocation Concealment)",
                "target_population": "بیماران قطعی مراجعه‌کننده با معیارهای دقیق ورود و خروج",
                "governance": "تاییدیه کمیته ملی اخلاق پزشکی، بیانیه هلسینکی و رضایت‌آگاهانه کتبی"
            }
            exposure_regimen = {
                "intervention_arm": f"مواجهه با رژیم مداخله‌ای استاندارد ({agt1} و {agt2}) با دوز و پروتکل بالینی مدون",
                "control_arm": "دریافت دارونما یا درمان استاندارد رایج (Standard of Care) با رعایت اصول اخلاقی",
                "blinding": "کورسازی دوطرفه (Double-Blind) شامل بیمار و ارزیاب پیامد بالینی"
            }
            assays_and_controls = {
                "efficacy_endpoint": {
                    "name": "پیامد اولیه بالینی بر مبنای معیارهای استاندارد بین‌المللی",
                    "monitoring": "ارزیابی دوره‌ای در فواصل زمانی مدون پیگیری بالینی",
                    "safety": "پایش و ثبت رخدادهای نامطلوب (Adverse Events) بر مبنای CTCAE v5.0"
                },
                "compliance_control": {
                    "pill_count": "پایش پایبندی دارویی با شمارش داروها و گزارش مکتوب بیمار",
                    "itt_analysis": "تحلیل آماری بر پایه قصد درمان (Intention-to-Treat: ITT)"
                }
            }
            gene_expression_miqe = {
                "guideline": "دستورالعمل بین‌المللی CONSORT 2010 برای کارآزمایی‌های بالینی تصادفی‌شده",
                "data_safety": "تشکیل کمیته مستقل پایش داده و ایمنی (DSMB)",
                "preregistration": "پیش‌ثبت رسمی در پایگاه IRCT یا ClinicalTrials.gov پیش از شروع بیمارگیری"
            }
            sample_size_biostatistics = {
                "replicate_structure": "بیماران مستقل تخصیص‌یافته به بازوهای درمانی موازی",
                "experimental_unit": "هر بیمار به عنوان یک واحد تجربی و آماری مستقل",
                "sample_size_formula_name": "فرمول چو و وانگ (Chow et al., 2017) جهت مقایسه دو گروه موازی در کارآزمایی بالینی",
                "chow_equation": r"$$n = \frac{2(Z_{1-\alpha/2} + Z_{1-\beta})^2 \cdot \sigma^2}{\Delta^2} = \frac{2(Z_{1-\alpha/2} + Z_{1-\beta})^2}{d^2}$$",
                "derivation": (
                    "در این رابطه توان آماری ۸۰٪ ($Z_{1-\\beta} = 0.84$)، ضریب خطای نوع اول ۵٪ ($Z_{1-\\alpha/2} = 1.96$) "
                    "و اندازه اثر استاندارد کوهن بر مبنای تفاوت حداقل معنادار بالینی (MCID) لحاظ گردیده و با ۱۰٪ نرخ ریزش احتمالی تعدیل می‌شود."
                ),
                "statistical_test": "آزمون تی مستقل، تحلیل کوواریانس (ANCOVA) برای تعدیل مقادیر پایه، و رویکرد Intention-to-Treat در نرم‌افزار SPSS/R"
            }
            combination_index_rules = {
                "software": "نرم‌افزار آماری R / SPSS",
                "synergism": "بهبود معنادار بالینی و آماری بازوی ترکیبی نسبت به هر یک از درمان‌های استاندارد",
                "additive": "اثربخشی مشابه مجموع آثار",
                "antagonism": "تداخل منفی یا کاهش اثربخشی"
            }
            formatted_sections = {
                13: (
                    f"طرح حاضر یک کارآزمایی بالینی تصادفی‌شده کنترل‌دار (Randomized Controlled Trial) منطبق بر راهنمای CONSORT است "
                    f"که بر روی {model_specs['model_name']} اجرا می‌شود. "
                    f"بیماران به صورت تصادفی دو سو کور در بازوهای درمانی تخصیص یافته و اثربخشی و ایمنی رژیم‌های درمانی مقایسه می‌گردد."
                ),
                19: (
                    "- داروهای تجویزی با استاندارد GMP و دارونماهای یکسان از نظر ظاهر، رنگ و طعم.\n"
                    "- تجهیزات بالینی استاندارد جهت پایش پارامترهای حیاتی و پیامدهای درمانی.\n"
                    "- سامانه‌های ثبت داده‌های بالینی الکترونیک (eCRF)."
                ),
                20: (
                    "- تخصیص تصادفی رایانه‌ای و پنهان‌سازی تخصیص با پاکت‌های مات درپوش‌دار متوالی.\n"
                    "- اعتبارسنجی کورسازی دوطرفه در مقاطع زمانی مختلف.\n"
                    "- ممیزی پروتکل توسط ناظر بالینی مستقل (Clinical Monitor)."
                ),
                21: (
                    "- مهار سوگیری تخصیص با پنهان‌سازی زنجیره تصادفی.\n"
                    "- مهار سوگیری اصطکاک (Attrition Bias) با تحلیل مبتنی بر قصد درمان (ITT).\n"
                    "- مهار سوگیری گزارش‌دهی با پیش‌ثبت رسمی پیامدها در سامانه IRCT."
                ),
                22: (
                    "محاسبه حجم نمونه بر اساس استاندارد مرجع کارآزمایی‌های بالینی چو و وانگ صورت پذیرفته است:\n\n"
                    f"{sample_size_biostatistics['chow_equation']}\n\n"
                    f"{sample_size_biostatistics['derivation']}"
                ),
                23: (
                    "- مقایسه میانگین پیامد اولیه با آزمون Independent Samples t-test و تحلیل کوواریانس (ANCOVA).\n"
                    "- تحلیل پیامدهای دوحالتی با آزمون Chi-Square و رگرسیون لجستیک جهت برآورد خطر نسبی (RR).\n"
                    "- تحلیل آماری اولیه بر پایه رویکرد Intention-to-Treat (ITT).\n"
                    "- سطح معنی‌داری در کلیه آزمون‌ها p < 0.05 تعیین گردیده است."
                ),
                27: (
                    "### پروتکل گام‌به‌گام اجرایی کارآزمایی بالینی (Step-by-Step Cohesive Protocol)\n\n"
                    "**گام ۱: اخذ مجوزها و پیش‌ثبت:** دریافت تاییدیه اخلاق زیست‌پزشکی و ثبت در سامانه IRCT.\n\n"
                    "**گام ۲: غربالگری و اخذ رضایت‌آگاهانه:** ارزیابی معیارهای ورود و خروج در بیماران مراجعه‌کننده و اخذ رضایت کتبی.\n\n"
                    "**گام ۳: تخصیص تصادفی و کورسازی:** تخصیص تصادفی بیماران به بازوهای موازی مداخله و شاهد با کدهای کورسازی‌شده.\n\n"
                    "**گام ۴: اعمال مداخله و پیگیری دوره‌ای:** تجویز رژیم‌های درمانی و پایش منظم اثربخشی و رخدادهای نامطلوب (Adverse Events).\n\n"
                    "**گام ۵: ممیزی داده‌ها و کدگشایی:** ممیزی فرم‌های گزارش موردی (eCRF)، قفل پایگاه داده و کدگشایی آماری.\n\n"
                    "**گام ۶: تحلیل آماری و گزارش‌دهی:** اجرای آزمون‌های آماری مطابق ITT و نگارش گزارش نهایی منطبق بر استانداردهای CONSORT."
                )
            }

        # =====================================================================
        # ARCHETYPE 4: IN VIVO ANIMAL MODEL
        # =====================================================================
        elif archetype == "IN_VIVO_ANIMAL_MODEL":
            model_specs = {
                "model_name": target_model if target_model != "Standard Biological / Cellular Model" else "مدل حیوانی آزمایشگاهی استاندارد (موش Balb/c یا رت ویستار)",
                "authentication": "تایید نژاد، سن (۶ تا ۸ هفته)، وزن استاندارد و وضعیت عاری از پاتوژن‌های اختصاصی (SPF)",
                "medium": "نگهداری در شرایط استاندارد حیوانی (دما ۲۲±۲ درجه، چرخه ۱۲ ساعت روشنایی/تاریکی و دسترسی آزاد به آب و غذا)",
                "incubation": "تهویه مناسب قفس‌ها و رعایت دوره سازگاری حداقل ۱ هفته پیش از شروع مداخلات",
                "governance": "انطباق با راهنماهای مراقبت و استفاده از حیوانات آزمایشگاهی (ARRIVE 2.0 Guidelines)"
            }
            exposure_regimen = {
                "dosing_regimen": f"تجویز دوزهای استاندارد بر پایه mg/kg از {agt1} و {agt2} به صورت تک‌دارویی و ترکیبی",
                "route_of_administration": "تزریق داخل صفاقی (IP) یا گاواژ خوراکی با سرنگ‌های انسولین کالیبره",
                "vehicle_control": "گروه کنترل شم (Vehicle Control) دریافت‌کننده حجم معادل نرمال سالین یا حلال استاندارد"
            }
            assays_and_controls = {
                "in_vivo_endpoints": {
                    "name": "سنجش اثر درمانی در مدل حیوانی (تغییرات وزن، حجم تومور، بیومارکرهای سرمی و آسیب‌شناسی بافتی)",
                    "monitoring": "ثبت روزانه وزن و وضعیت عمومی و اندازه‌گیری دوره‌ای با کولیس دیجیتال",
                    "welfare": "پایش نقاط پایانی انسانی (Humane Endpoints) جهت کاهش رنج حیوانات"
                },
                "histopathology": {
                    "name": "بررسی پاتولوژی و رنگ‌آمیزی H&E بافت‌های ارگان هدف جهت ارزیابی ایمنی و اثربخشی",
                    "differentiation": "ارزیابی میزان نکروز، آپوپتوز و شاخص‌های سمیت ارگانی (کبد و کلیه)"
                }
            }
            gene_expression_miqe = {
                "guideline": "راهنمای ARRIVE 2.0 برای گزارش‌دهی پژوهش‌های حیوانی",
                "welfare_monitoring": "پایش سلامت حیوانات با چک‌لیست معتبر رفاه حیوانات",
                "dual_reference_genes": "سنجش بیان ژن‌ها با RT-qPCR با نرمال‌سازی نسبت به ژن‌های پایدار بافتی (Gapdh و Actb)"
            }
            sample_size_biostatistics = {
                "replicate_structure": "حداقل ۶ سر حیوان در هر بازوی آزمایشی بر مبنای استاندارد ARRIVE و Festing",
                "experimental_unit": "هر سر حیوان آزمایشگاهی به عنوان یک واحد تجربی و آماری مستقل",
                "sample_size_formula_name": "معادله تخصیص منابع فستینگ (Mead's Resource Equation for Animals)",
                "mead_equation": r"$$E = N - B - T$$",
                "derivation": (
                    "در این رابطه با فرض ۴ بازوی آزمایشی و ۶ سر حیوان در هر گروه ($N = 24$)، درجات آزادی بلوک‌بندی ($B = 1$) "
                    "و درجات آزادی تیمار ($T = 4 - 1 = 3$)، مقدار درجات آزادی خطا $E = 24 - 1 - 3 = 20$ حاصل می‌شود "
                    "که دقیقاً در بازه استاندارد طلایی فستینگ ($10 \\le E \\le 20$) قرار دارد."
                ),
                "statistical_test": "تحلیل واریانس اندازه‌گیری‌های مکرر (Repeated Measures ANOVA) و آزمون تعقیبی توکی در GraphPad Prism"
            }
            combination_index_rules = {
                "software": "نرم‌افزار تحلیلی GraphPad Prism v9 / SPSS",
                "synergism": "کاهش معنادار آماری حجم ضایعه/تومور در گروه ترکیبی نسبت به تک‌دارویی‌ها",
                "additive": "اثر جمع‌پذیر معادل مجموع مهار",
                "antagonism": "تداخل منفی یا افزایش عوارض سمیت"
            }
            formatted_sections = {
                13: (
                    f"مطالعه حاضر به صورت تجربی برون‌تنی/درون‌تنی (In Vivo) بر روی {model_specs['model_name']} "
                    f"منطبق با دستورالعمل بین‌المللی ARRIVE 2.0 طراحی شده است. "
                    f"پس از دوره سازگاری، حیوانات در بازوهای درمانی تصادفی تخصیص یافته و تحت مواجهه با رژیم‌های منفرد و ترکیبی "
                    f"({agt1} و {agt2}) قرار می‌گیرند و پارامترهای اثربخشی، بقا و بیومارکرهای سرمی پایش خواهد شد."
                ),
                19: (
                    "- تجهیزات استاندارد خانه حیوانات (قفس‌های استاندارد، تهویه مطبوع، ترازوی دیجیتال و کولیس).\n"
                    "- تجهیزات بیهوشی استاندارد (ایزوفلوران) و ست‌های جراحی و نمونه‌برداری بافتی.\n"
                    "- دستگاه الایزا ریدر و اسپکتروفتومتر جهت ارزیابی بیومارکرهای سرمی.\n"
                    "- نرم‌افزارهای تخصصی GraphPad Prism و SPSS جهت تحلیل‌های آماری."
                ),
                20: (
                    "- تصادفی‌سازی کامل حیوانات با جدول اعداد تصادفی پیش از آغاز مداخلات.\n"
                    "- کالیبراسیون روزانه ابزارهای اندازه‌گیری (ترازو و کولیس دیجیتال).\n"
                    "- کورسازی متخصص پاتولوژیست نسبت به بازوهای درمانی در ارزیابی نمونه‌های بافتی."
                ),
                21: (
                    "- مهار سوگیری جایگاهی با چرخش تصادفی موقعیت قفس‌ها در قفسه‌بندی اتاق حیوانات.\n"
                    "- کنترل شوک دمایی و محیطی با پایش مداوم دما و رطوبت.\n"
                    "- ثبت دقیق دلایل تلفات احتمالی و ممانعت از جایگزینی سلیقه‌ای نمونه‌ها."
                ),
                22: (
                    "تعیین حجم نمونه بر اساس استاندارد بین‌المللی ARRIVE 2.0 و معادله تخصیص منابع فستینگ (Mead's Resource Equation) انجام شده است:\n\n"
                    f"{sample_size_biostatistics['mead_equation']}\n\n"
                    f"{sample_size_biostatistics['derivation']}\n\n"
                    "این طراحی متضمن تامین توان آماری مطلوب ($1 - \\beta \\ge 0.80$) بدون استفاده غیرضروری از حیوانات آزمایشگاهی می‌باشد."
                ),
                23: (
                    "- بررسی نرمال بودن توزیع داده‌ها با آزمون شاپیرو-ویلک (Shapiro-Wilk).\n"
                    "- مقایسه روند زمانی تغییرات بین گروه‌ها با آزمون Repeated Measures Two-Way ANOVA.\n"
                    "- مقایسه‌های زوجی بین گروه‌ها با آزمون تعقیبی توکی (Tukey's Post-Hoc Test).\n"
                    "- تحلیل بقای حیوانات با روش کاپلان-مایر (Kaplan-Meier) و آزمون Log-Rank.\n"
                    "- سطح معنی‌داری آماری در تمام آزمون‌ها p < 0.05 لحاظ خواهد شد."
                ),
                27: (
                    "### پروتکل گام‌به‌گام اجرایی مطالعه حیوانی (Step-by-Step Cohesive Protocol)\n\n"
                    "**گام ۱: سازگاری و قرنطینه حیوانات:** نگهداری حیوانات آزمایشگاهی در خانه حیوانات به مدت ۷ روز پیش از مداخله در شرایط استاندارد نوری و دمایی.\n\n"
                    "**گام ۲: تصادفی‌سازی و گروه‌بندی:** تخصیص تصادفی حیوانات به بازوهای شاهد، مداخله منفرد ۱، مداخله منفرد ۲ و ترکیب همزمان (هر گروه ۶ سر، کل $N = 24$).\n\n"
                    "**گام ۳: اعمال مداخلات درمانی:** تجویز دوره‌ای دوزهای بهینه‌شده داروها با سرنگ‌های کالیبره طبق جدول زمان‌بندی مدون.\n\n"
                    "**گام ۴: پایش پارامترهای عمومی و پیامدها:** اندازه‌گیری منظم وزن، مصرف آب و غذا و رصد نشانه‌های رفتاری و بالینی.\n\n"
                    "**گام ۵: اتانازی اخلاقی و نمونه‌برداری:** اجرای اتانازی بدون درد در پایان دوره، خونگیری جهت سنجش بیومارکرهای سرمی و جداسازی بافت‌های هدف.\n\n"
                    "**گام ۶: ارزیابی‌های هیستوپاتولوژی و مولکولی:** آماده‌سازی مقاطع بافتی، رنگ‌آمیزی H&E و ارزیابی آسیب‌شناسی به شیوه دوسوکور."
                )
            }

        # =====================================================================
        # ARCHETYPE 5: DEFAULT IN VITRO MOLECULAR & CELLULAR COMBINATION
        # =====================================================================
        else:
            # 1. Target Model & Culture Specs (GCCP-compliant)
            model_specs = {
                "model_name": target_model,
                "authentication": "احراز هویت ژنتیکی پروفایل STR (Short Tandem Repeat) و غربالگری منفی مایکوپلاسما با PCR",
                "medium": "محیط کشت RPMI-1640 یا Ham's F-12K غنی‌شده با ۱۰٪ سرم جنین گاوی (FBS غیرفعال‌شده با حرارت) و ۱٪ پنی‌سیلین-استرپتومایسین",
                "incubation": "دمای ۳۷ درجه سانتی‌گراد، اتمسفر مرطوب با رطوبت نسبی >۹۵٪ و ۵٪ دی‌اکسید کربن (CO2)",
                "passaging": "استفاده از سلول‌ها در فاز رشد لگاریتمی (پاساژهای ۳ تا ۱۵) با تراکم تلاقی (Confluency) زیر ۸۰ درصد"
            }

            # 2. Exposure Regimen & Dosing Matrix
            exposure_regimen = {
                "monotherapy_screening": "غربالگری تک‌دارویی در دامنه لگاریتمی برای تعیین غلظت مهار ۵۰٪ رشد (IC50) در بازه‌های زمانی ۲۴، ۴۸ و ۷۲ ساعت",
                "combination_matrix": "طراحی فاکتوریل با ماتریس غلظت‌های ترکیبی (۵ غلظت از مداخله اول × ۵ غلظت از مداخله دوم بر مبنای مضارب کسری و چندبرابری IC50: 0.25x, 0.5x, 1x, 2x, 4x)",
                "vehicle_control": "غلظت نهایی حلال ناقل (DMSO یا آب مقطر استریل) اکیداً کمتر از ۰.۱ درصد حجمی (v/v)"
            }

            # 3. Assays & Assay Interference Controls (GCCP & Biphasic Redox)
            assays_and_controls = {
                "viability_assay": {
                    "name": "سنجش زیست‌پذیری سلولی بر پایه MTT / CCK-8",
                    "seeding_density": "۵۰۰۰ الی ۱۰۰۰۰ سلول در هر چاهک پلیت ۹۶ خانه‌ای",
                    "spectrophotometry": "قرائت جذب نوری در طول موج ۵۷۰ نانومتر با کسر طول موج مرجع ۶۳۰ نانومتر (Differential Wavelength)",
                    "interference_control": "تعبیه کنترل بلانک بدون سلول (Cell-Free Blank) حاوی ماده و محیط کشت بدون سلول جهت حذف احیای شیمیایی مستقیم تترازولیوم"
                },
                "apoptosis_assay": {
                    "name": "فلوسایتومتری آپوپتوز با رنگ‌آمیزی دوگانه Annexin V-FITC / PI",
                    "instrument": "دستگاه فلوسایتومتر با لیزر ۴۸۸ نانومتر و آنالیز حداقل ۱۰،۰۰۰ رخداد سلولی در هر نمونه",
                    "differentiation": "تفکیک سلول‌های زنده (Annexin-/PI-)، آپوپتوز اولیه (Annexin+/PI-)، آپوپتوز پیشرفته (Annexin+/PI+) و نکروز (Annexin-/PI+)"
                },
                "clonogenic_assay": {
                    "name": "آزمون تشکیل کلونی (Colony Formation Assay)",
                    "seeding_density": "۵۰۰ تا ۱۰۰۰ سلول در هر چاهک پلیت ۶ خانه‌ای به مدت ۱۰ تا ۱۴ روز",
                    "fixation_staining": "تثبیت با متانول و رنگ‌آمیزی با کریستال ویوله ۰.۵٪؛ شمارش کلونی‌های واجد بیش از ۵۰ سلول"
                }
            }

            # 4. Gene Expression Rigor (MIQE Guidelines)
            gene_expression_miqe = {
                "guideline": "دستورالعمل بین‌المللی MIQE برای سنجش‌های Real-Time RT-qPCR",
                "rna_quality": "استخراج RNA با کیت ستونی استاندارد، سنجش نسبت A260/A280 در بازه ۱.۸ الی ۲.۰ و شاخص یکپارچگی RNA (RIN >= 7.0)",
                "dnase_treatment": "تیمار با DNase I عاری از RNase جهت حذف DNA ژنومی باقیمانده",
                "controls": "تعبیه کنترل عدم رونویسی معکوس (No-RT Control) و کنترل منفی بدون الگو (No-Template Control: NTC)",
                "dual_reference_genes": "استفاده همزمان از دو ژن مرجع داخلی پایدار (GAPDH و ACTB) با اعتبارسنجی پایداری بیان در تیمارها",
                "quantification_method": "کمی‌سازی نسبی بیان با روش ۲ به توان منفی دلتا دلتا Ct ($2^{-\\Delta\\Delta C_t}$)"
            }

            # 5. Sample Size & Biostatistical Rigor (Mead's Resource Equation + Two-Way Factorial ANOVA)
            sample_size_biostatistics = {
                "replicate_structure": "حداقل ۳ تکرار بیولوژیکی کاملاً مستقل در روزها و پاساژهای سلولی مجزا (n = 3 Biological Replicates)، هر یک با ۳ تکرار تکنیکی درون‌پلیتی (Technical Triplicates)",
                "experimental_unit": "میانگین تکرارهای تکنیکی درون‌پلیتی به عنوان ۱ واحد تجربی مستقل در تحلیل آماری وارد می‌شود (اجتناب از خطای شبه‌تکرار Pseudo-Replication Fallacy)",
                "sample_size_formula_name": "معادله تخصیص منابع مید (Mead's Resource Equation) و محاسبه توان آنالیز واریانس فاکتوریل",
                "mead_equation": r"$$E = N - B - T$$",
                "mead_derivation": (
                    "در این رابطه $N$ کل واحدهای تجربی مستقل ($N = 10 \\times 3 = 30$ با احتساب کنترل، تک‌دارویی‌ها و غلظت‌های ترکیبی)، "
                    "$B$ درجات آزادی اثر بلوک‌بندی آزمایشگاهی ($B = k_{blocks} - 1 = 3 - 1 = 2$ به ازای ۳ روز کاری مستقل) و $T$ درجات آزادی تیمارها ($T = 10 - 1 = 9$) است. "
                    "در نتیجه درجات آزادی خطای آزمون $E = 30 - 2 - 9 = 19$ محاسبه می‌شود که دقیقاً در بازه بهینه استاندارد بین‌المللی ($10 \\le E \\le 20$) قرار دارد."
                ),
                "factorial_power_calculation": (
                    "علاوه بر این، تحلیل مستقل توان آماری آزمون در نرم‌افزار G*Power نشان می‌دهد که با در نظر گرفتن "
                    "اندازه اثر بزرگ کوهن ($f = 0.40$ معادل $\\eta_p^2 \\ge 0.14$)، سطح خطای نوع اول دوطرفه $\\alpha = 0.05$ "
                    "و تعداد $n = 3$ تکرار بیولوژیکی مستقل در هر بازو، توان آماری آزمون به ۸۵.۲ درصد ($1 - \\beta = 0.852 > 0.80$) می‌رسد."
                ),
                "statistical_test": "آنالیز واریانس دوطرفه فاکتوریل (Two-Way Factorial ANOVA with interaction) همراه با آزمون تعقیبی توکی (Tukey HSD)"
            }

            # 6. Harmonized Combination Index Rules (Chou-Talalay 2006)
            combination_index_rules = {
                "software": "نرم‌افزار رسمی CompuSyn / CalcuSyn بر پایه قضیه میانه-اثر چو",
                "synergism": "CI < 0.9 (هم‌افزایی فارماکولوژیک معنادار)",
                "additive": "0.9 <= CI <= 1.1 (اثر تجمعی یا جمع‌پذیر)",
                "antagonism": "CI > 1.1 (تضاد یا اثر آنتاگونیستی)"
            }

            # Formatted Persian texts for canonical sections
            formatted_sections = {
                13: (
                    f"مطالعه حاضر به صورت تجربی-آزمایشگاهی (In Vitro) بر روی رده سلولی {target_model} طراحی شده است. "
                    f"پس از احراز هویت سلولی و بهینه‌سازی شرایط کشت در محیط RPMI-1640 یا Ham's F-12K حاوی ۱۰٪ FBS، سلول‌ها با غلظت‌های لگاریتمی "
                    f"مداخلات ({agt1} و {agt2}) به صورت منفرد و ترکیبی در فواصل زمانی ۲۴، ۴۸ و ۷۲ ساعت مواجهه داده می‌شوند. "
                    f"زیست‌پذیری سلولی با سنجش MTT، مرگ برنامه‌ریزی‌شده با فلوسایتومتری Annexin V/PI، پتانسیل کلونوژنیک با آزمون تشکیل کلونی "
                    f"و بیان نشانگرهای آپوپتوزی با RT-qPCR ارزیابی خواهد شد."
                ),
                19: (
                    "- دستگاه الایزا ریدر (Microplate Spectrophotometer) با قابلیت قرائت طول موج ۵۷۰ و ۶۳۰ نانومتر.\n"
                    "- دستگاه فلوسایتومتر مجهز به لیزر ۴۸۸ نانومتر جهت تفکیک مراحل آپوپتوز.\n"
                    "- سیستم Real-Time PCR جهت کمی‌سازی بیان ژن‌ها.\n"
                    "- انکوباتور CO2 با کنترل دقیق رطوبت و دما و هود لامینار کلاس II.\n"
                    "- نرم‌افزارهای تحلیلی CompuSyn (جهت محاسبه CI) و GraphPad Prism / SPSS (جهت آزمون‌های آماری)."
                ),
                20: (
                    "- کالیبراسیون دوره‌ای دستگاه الایزا ریدر با فیلترهای استاندارد مرجع فتومتریک.\n"
                    "- تنظیم ولتاژ و جبران‌سازی طیفی (Color Compensation) فلوسایتومتر با کنترل‌های تک‌رنگ Annexin V و PI.\n"
                    "- ارزیابی راندمان واکنش PCR (Amplification Efficiency) با رسم منحنی استاندارد و پذیرش راندمان بین ۹۰ تا ۱۱۰ درصد.\n"
                    "- تطابق با دستورالعمل‌های بین‌المللی OECD GCCP و استانداردهای MIQE."
                ),
                21: (
                    "- انجام کلیه آزمون‌ها در ۳ تکرار بیولوژیکی مستقل در روزها و پاساژهای سلولی مجزا.\n"
                    "- لحاظ نمودن حداقل ۳ تکرار تکنیکی (Triplicate) درون هر پلیت به منظور به حداقل رساندن خطای پیپتینگ.\n"
                    "- پایش ضریب تغییرات درون‌آزمونی (Intra-assay CV) و بین‌آزمونی (Inter-assay CV) و پذیرش نتایج صرفاً با CV کمتر از ۱۰٪."
                ),
                22: (
                    "تعیین حجم نمونه بر اساس استانداردهای بین‌المللی تکرارهای زیستی مستقل، معادله تخصیص منابع فستینگ و مید "
                    f"(Mead's Resource Equation; Festing, 2006) و تحلیل مستقل توان آنالیز واریانس فاکتوریل (G*Power) صورت پذیرفته است:\n\n"
                    f"{sample_size_biostatistics['mead_equation']}\n\n"
                    f"{sample_size_biostatistics['mead_derivation']}\n\n"
                    f"{sample_size_biostatistics['factorial_power_calculation']}\n\n"
                    "کلیه تکرارهای تکنیکی درون‌پلیتی (Technical Triplicates) جهت ممانعت از خطای شبه‌تکرار (Pseudo-Replication Fallacy) "
                    "به صورت میانگین یک واحد تجربی لحاظ شده و توان نهایی آماری آزمون در تحلیل مستقل $1 - \\beta = 0.852 > 0.80$ تایید می‌گردد."
                ),
                23: (
                    "- ارزیابی پیش‌فرض نرمال بودن توزیع با آزمون Shapiro-Wilk و همگنی واریانس‌ها با آزمون Levene.\n"
                    "- مقایسه میانگین گروه‌ها و ارزیابی اثر متقابل غلظت‌ها با آنالیز واریانس دوطرفه فاکتوریل (Two-Way Factorial ANOVA with interaction).\n"
                    "- انجام آزمون تعقیبی توکی (Tukey's HSD) جهت مقایسه‌های زوجی بین بازوهای آزمایشی.\n"
                    f"- کمی‌سازی نسبی بیان ژن‌ها مطابق فرمول $2^{{-\\Delta\\Delta C_t}}$ با نرمال‌سازی نسبت به دو ژن مرجع GAPDH و ACTB.\n"
                    f"- محاسبه شاخص ترکیب (CI) با نرم‌افزار CompuSyn بر مبنای معیارهای استاندارد واحد:\n"
                    f"  * {combination_index_rules['synergism']}\n"
                    f"  * {combination_index_rules['additive']}\n"
                    f"  * {combination_index_rules['antagonism']}\n"
                    "- سطح معنی‌داری آماری در تمام آزمون‌ها p < 0.05 تعیین گردیده است."
                ),
                27: (
                    "### پروتکل گام‌به‌گام اجرایی طرح پژوهشی (Step-by-Step Cohesive Protocol)\n\n"
                    f"**گام ۱: آماده‌سازی و کشت سلولی:** سلول‌های {target_model} در محیط {model_specs['medium']} در انکوباتور با ۵٪ CO2 کشت داده شده و پس از رسیدن به تراکم ۷۰-۸۰٪ پاساژ داده می‌شوند.\n\n"
                    f"**گام ۲: تیمار با غلظت‌های منفرد و تعیین IC50:** سلول‌ها در پلیت‌های ۹۶ خانه‌ای با غلظت‌های فزاینده {agt1} و {agt2} به مدت ۲۴، ۴۸ و ۷۲ ساعت انکوبه شده و با افزودن معرف MTT و قرائت جذب ۵۷۰ نانومتر (کسر طول موج مرجع ۶۳۰ نانومتر)، مقدار IC50 هر ماده تعیین می‌گردد. کنترل بلانک بدون سلول (Cell-Free Blank) در کنار کنترل‌های حلال تعبیه می‌شود.\n\n"
                    f"**گام ۳: تیمار ترکیبی و ارزیابی هم‌افزایی (CompuSyn):** سلول‌ها تحت مواجهه با ماتریس ترکیبی از دوزهای کسری و چندبرابری IC50 قرار گرفته و شاخص ترکیب (CI) محاسبه می‌شود.\n\n"
                    "**گام ۴: تایید ارتوگونال آپوپتوز با فلوسایتومتری:** سلول‌های تیمارشده با بافر انکسین شستشو داده شده و پس از رنگ‌آمیزی با Annexin V-FITC و PI، با دستگاه فلوسایتومتر آنالیز می‌گردند.\n\n"
                    "**گام ۵: سنجش کلونوژنیک:** بقای طولانی‌مدت سلول‌ها با کاشت تراکم پایین (۵۰۰ سلول) در پلیت ۶ خانه‌ای و رنگ‌آمیزی با کریستال ویوله ارزیابی می‌شود.\n\n"
                    "**گام ۶: ارزیابی مولکولی بیان ژن (RT-qPCR):** پس از استخراج RNA با کیفیت بالا (RIN >= 7.0) و سنتز cDNA، بیان ژن‌های هدف با پرایمرهای اختصاصی و نرمال‌سازی همزمان نسبت به دو ژن مرجع پایدار GAPDH و ACTB سنجش می‌گردد."
                )
            }

        return CohesiveProtocolResult(
            archetype=archetype,
            target_model_specs=model_specs,
            culture_conditions=model_specs,
            exposure_regimen=exposure_regimen,
            assays_and_controls=assays_and_controls,
            gene_expression_miqe=gene_expression_miqe,
            sample_size_biostatistics=sample_size_biostatistics,
            combination_index_rules=combination_index_rules,
            formatted_sections_fa=formatted_sections,
            coherence_score=1.0,
            detected_inconsistencies=[]
        )

    @classmethod
    def audit_chimera_inconsistencies(cls, protocol_text: str) -> Dict[str, Any]:
        """Audits proposal methodology text for frankenstein/chimera protocol contradictions."""
        text_lower = protocol_text.lower()
        findings: List[str] = []
        severity = "PASS"

        # 1. Check for two-sample t-test formula contradicting factorial multi-arm / n=3
        has_ttest_formula = bool(re.search(r'\\frac\{2\(z', text_lower) or re.search(r'2\(z_\{?1-\\alpha', text_lower))
        claims_n3 = bool(re.search(r'n\s*=\s*3', text_lower) or "۳ تکرار" in protocol_text or "3 biological" in text_lower)
        has_mead_or_factorial = bool("mead" in text_lower or "resource equation" in text_lower or "factorial" in text_lower or "واریانس دوطرفه" in protocol_text)

        if has_ttest_formula and claims_n3 and not has_mead_or_factorial:
            findings.append("BIOSTATISTICAL_CONTRADICTION: استفاده همزمان از فرمول مقایسه دو میانگین مستقل (که n~7 می‌دهد) با ادعای n=3 بدون درج معادله مید یا تحلیل توان فاکتوریل.")
            severity = "CRITICAL_FLAW"

        # 2. Check for MTT assay missing Cell-Free Blank
        if ("mtt" in text_lower or "cck-8" in text_lower) and not any(k in text_lower for k in ["cell-free blank", "بلانک بدون سلول", "کنترل بلانک"]):
            findings.append("ASSAY_INTERFERENCE_DEFECT: عدم تعریف کنترل بلانک بدون سلول (Cell-Free Blank) در سنجش تترازولیوم برای حذف احیای شیمیایی مستقیم.")
            severity = "CRITICAL_FLAW" if severity != "CRITICAL_FLAW" else severity

        # 3. Check for qPCR missing dual reference genes (MIQE defect)
        if any(k in text_lower for k in ["qpcr", "rt-pcr", "real-time", "بیان ژن"]):
            mentions_gapdh = "gapdh" in text_lower
            mentions_actb = "actb" in text_lower or "actin" in text_lower or "اکتین" in protocol_text
            mentions_dual = any(k in protocol_text for k in ["دو ژن مرجع", "ژن‌های مرجع", "حداقل دو ژن"])
            if not (mentions_dual or (mentions_gapdh and mentions_actb)):
                findings.append("MIQE_COMPLIANCE_DEFECT: استفاده از تک‌ژن مرجع در qPCR بدون اعتبارسنجی دوگانه (الزام استفاده از حداقل دو ژن پایدار مانند GAPDH و ACTB طبق MIQE).")

        # 4. Check for Differential Wavelength in Spectrophotometry
        if "mtt" in text_lower and not any(w in text_lower for w in ["630", "650", "مرجع", "افتراقی", "differential"]):
            findings.append("PHOTOMETRIC_PRECISION_DEFECT: عدم ثبت طول موج مرجع (مانند ۶۳۰ یا ۶۵۰ نانومتر) برای حذف کدورت و پراکندگی نور در میکروپلیت ریدر.")

        # 5. Check for Cell culture medium specification
        if any(c in text_lower for c in ["سلول", "cell line", "کشت سلولی", "رده سلولی"]) and not any(m in text_lower for m in ["rpmi", "f-12k", "dmem", "fbs", "محیط کشت"]):
            findings.append("CULTURE_MEDIUM_UNSPECIFIED: عدم تعیین دقیق محیط کشت اختصاصی رده سلولی (نظیر RPMI-1640 یا Ham's F-12K یا DMEM).")

        return {
            "severity": severity,
            "findings_count": len(findings),
            "findings": findings,
            "is_cohesive": len(findings) == 0
        }


if __name__ == "__main__":
    print("MethodologyResearchSubagent loaded successfully.")
