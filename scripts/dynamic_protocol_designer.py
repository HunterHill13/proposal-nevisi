#!/usr/bin/env python3
"""
dynamic_protocol_designer.py - Dynamic Variables, Timeline, and Statistical Planning
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

Generates dynamic Variable Tables, study-type-specific Gantt Timelines,
and coherent Statistical Analysis Plans tailored strictly to the Research Problem Model.
"""

import json
from typing import Dict, List, Any

STUDY_TIMELINE_TEMPLATES = {
    "EXPERIMENTAL_IN_VITRO": [
        ("فاز ۱: مرور سیستماتیک منابع و تدوین نهایی پروتکل آزمایشگاهی", 1, 2),
        ("فاز ۲: تهیه و آماده‌سازی رده‌های سلولی، آزمون‌های کنترل کیفی و تایید هویت", 2, 3),
        ("فاز ۳: بهینه‌سازی دوز و سنجش غلظت‌های غیرسمی حلال / کنترل‌ها", 3, 4),
        ("فاز ۴: اجرای آزمون‌های سنجش بقا و مهار تکثیر سلولی", 4, 6),
        ("فاز ۵: آزمون‌های سنجش میان‌کنش و تحلیل کمی اثرات ترکیبی", 6, 8),
        ("فاز ۶: سنجش‌های مولکولی مسیرهای پیام‌رسانی و مکانیسم‌های مرگ سلولی", 7, 10),
        ("فاز ۷: پردازش داده‌ها، تحلیل آماری و نگارش گزارش نهایی", 10, 12)
    ],
    "EXPERIMENTAL_ANIMAL": [
        ("فاز ۱: تدوین پروتکل، اخذ تاییدیه کمیته اخلاق کار با حیوانات آزمایشگاهی", 1, 2),
        ("فاز ۲: خرید، قرنطینه و سازگاری حیوانات آزمایشگاهی در بیوتروم", 2, 3),
        ("فاز ۳: القای مدل بیماری و پایش دوره نهفتگی", 3, 5),
        ("فاز ۴: اجرای مداخله دارویی / درمانی و کنترل عوارض", 5, 8),
        ("فاز ۵: نمونه‌برداری بافتی، سنجش‌های پاتولوژیک و ایمونوهیستوشیمی", 8, 10),
        ("فاز ۶: آنالیز آماری داده‌های پیش‌بالینی و تدوین مستندات", 10, 12)
    ],
    "PICO": [
        ("فاز ۱: ثبت در رجیستری کارآزمایی‌های بالینی و اخذ مجوز کمیته اخلاق", 1, 3),
        ("فاز ۲: غربالگری، اخذ رضایت آگاهانه و ورود بیماران واجد شرایط", 3, 7),
        ("فاز ۳: اجرای پروتکل تصادفی‌سازی، کورسازی و تجویز مداخله", 6, 12),
        ("فاز ۴: پیگیری دوره‌ای بیماران، ثبت عوارض جانبی و سنجش پیامدها", 8, 16),
        ("فاز ۵: پاک‌سازی داده‌ها، خروج از کورسازی و آنالیز آماری طبق پروتکل ITT", 16, 18),
        ("فاز ۶: تدوین گزارش نهایی و تحلیل پیامدهای بالینی", 18, 20)
    ],
    "DIAGNOSTIC": [
        ("فاز ۱: تدوین پروتکل، هماهنگی با آزمایشگاه مرجع و اخذ کد اخلاق", 1, 2),
        ("فاز ۲: جمع‌آوری نمونه‌های زیستی طبق معیارهای ورود و خروج", 2, 5),
        ("فاز ۳: اجرای آزمون شاخص (Index Test) توسط اپراتورهای مستقل و کور", 4, 7),
        ("فاز ۴: اجرای آزمون استاندارد طلایی (Gold Standard) مرجع", 5, 8),
        ("فاز ۵: محاسبه شاخص‌های تشخیصی (حساسیت، ویژگی، ROC curve)", 8, 10),
        ("فاز ۶: اعتبارسنجی تکرارپذیری، تحلیل آماری و گزارش نتایج", 10, 12)
    ]
}

class DynamicProtocolDesigner:
    """Extracts research design components dynamically from the problem model."""

    @classmethod
    def generate_variable_table(cls, model_dict: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extracts structured variable rows: Independent, Dependent, Confounders, Controls."""
        variables = []

        # 1. Independent Variables (Interventions)
        interventions = model_dict.get("interventions_or_exposures", [])
        for agt in interventions:
            name = agt.get("name", "مداخله پژوهش")
            variables.append({
                "name": name,
                "role": "مستقل (Independent)",
                "type": "کمی پیوسته (Continuous)",
                "operational_definition": f"غلظت و دوز مواجهه با {name} در مدل تجربی",
                "measurement_method": "تیتراسیون رقت‌های متوالی در شرایط کنترل‌شده",
                "unit": "میکرومولار / غلظت استاندارد"
            })

        # 2. Dependent Variables (Primary Outcomes)
        outcomes = model_dict.get("primary_outcomes", [])
        for out in outcomes:
            name = out.get("name", "پیامد اولیه")
            unit = out.get("measurement_unit", "درصد مهار")
            variables.append({
                "name": name,
                "role": "وابسته (Dependent)",
                "type": "کمی پیوسته (Continuous)",
                "operational_definition": f"میزان تغییر در شاخص {name} نسبت به گروه کنترل منفی",
                "measurement_method": "سنجش کمی نوری / الایزا / فلوسایتومتری",
                "unit": unit
            })

        # 3. Controls / Covariates
        comparators = model_dict.get("comparators", [])
        for comp in comparators:
            cname = comp.get("name", "کنترل پایه")
            variables.append({
                "name": cname,
                "role": "کنترل پایه (Baseline Control)",
                "type": "کیفی رتبه‌ای (Categorical)",
                "operational_definition": f"شرایط پایه فاقد مداخله فعال جهت نرمال‌سازی داده‌ها ({cname})",
                "measurement_method": "انکوباسیون همزمان در شرایط یکسان با حلال فاقد ماده موثره",
                "unit": "فاقد واحد (نسبت به کنترل)"
            })

        # 4. Confounders
        variables.append({
            "name": "تعداد پاساژ و یکنواختی محیط کشت / شرایط آزمون",
            "role": "مخدوشگر بالقوه (Confounder)",
            "type": "کمی گسسته (Discrete)",
            "operational_definition": "تغییرات بیولوژیکی ناشی از پیری سلولی یا نوسانات محیط کشت",
            "measurement_method": "استفاده از پاساژهای مشخص و یکسان در تمام تکرارهای زیستی",
            "unit": "شماره پاساژ"
        })

        return variables

    @classmethod
    def generate_timeline(cls, framework: str) -> List[Dict[str, Any]]:
        """Returns phased Gantt timeline appropriate for the study framework."""
        raw_phases = STUDY_TIMELINE_TEMPLATES.get(framework, STUDY_TIMELINE_TEMPLATES["EXPERIMENTAL_IN_VITRO"])
        timeline = []
        for phase_name, start_m, end_m in raw_phases:
            timeline.append({
                "phase_title": phase_name,
                "start_month": start_m,
                "end_month": end_m,
                "duration_months": end_m - start_m + 1
            })
        return timeline

    @classmethod
    def generate_statistical_plan(cls, model_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Aligns statistical tests dynamically with outcome variable types and study design."""
        framework = model_dict.get("framework", "EXPERIMENTAL_IN_VITRO")
        outcomes = model_dict.get("primary_outcomes", [])
        interventions = model_dict.get("interventions_or_exposures", [])

        is_multi_agent = len(interventions) > 1
        
        tests = []
        if is_multi_agent:
            tests.append("تحلیل واریانس دوطرفه (Two-way ANOVA) جهت ارزیابی اثرات اصلی و اثر متقابل (Interaction effect)")
            tests.append("آزمون تعقیبی توکی (Tukey's HSD post-hoc test) جهت مقایسه‌های چندگانه میان گروه‌ها")
            tests.append("مدل‌های ریاضی استاندارد سنجش هم‌افزایی (مانند نسبت ترکیب یا نمایه میان‌کنش) جهت تعیین ماهیت تعامل")
        else:
            tests.append("تحلیل واریانس یک‌طرفه (One-way ANOVA) همراه با آزمون تعقیبی دانت یا توکی")

        tests.append("آزمون شاپیرو-ویلک (Shapiro-Wilk) جهت بررسی نرمال بودن توزیع داده‌ها")
        tests.append("سطح معنی‌داری آماری در تمام تحلیل‌ها p < 0.05 لحاظ خواهد شد")

        return {
            "primary_analysis": tests[0],
            "post_hoc_analysis": tests[1] if len(tests) > 1 else "Dunnett's test",
            "distribution_test": "Shapiro-Wilk normality test",
            "alpha_threshold": 0.05,
            "statistical_software": "GraphPad Prism / R Statistical Environment",
            "complete_testing_strategy": tests
        }

if __name__ == "__main__":
    demo_model = {
        "framework": "EXPERIMENTAL_IN_VITRO",
        "interventions_or_exposures": [{"name": "Compound X"}, {"name": "Biologic Y"}],
        "primary_outcomes": [{"name": "Cellular Apoptosis", "measurement_unit": "% apoptosis"}],
        "comparators": [{"name": "Vehicle Control"}]
    }
    vt = DynamicProtocolDesigner.generate_variable_table(demo_model)
    tl = DynamicProtocolDesigner.generate_timeline("EXPERIMENTAL_IN_VITRO")
    sp = DynamicProtocolDesigner.generate_statistical_plan(demo_model)
    print(f"Generated {len(vt)} variables, {len(tl)} timeline phases, primary stat test: {sp['primary_analysis']}")
