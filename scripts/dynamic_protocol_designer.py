#!/usr/bin/env python3
"""
dynamic_protocol_designer.py - Dynamic Variables, Timeline, and Statistical Planning
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

Generates dynamic Variable Tables, study-type-specific Gantt Timelines,
and coherent Statistical Analysis Plans tailored strictly to the Research Problem Model.
"""

import json
from typing import Dict, List, Any, Optional

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
    ],
    "PECO": [
        ("فاز ۱: طراحی پروتکل مواجهه، استقرار سیستم‌های پایش محیطی و اخذ مجوز اخلاق", 1, 3),
        ("فاز ۲: شناسایی و ورود افراد مواجهه‌یافته و گروه کنترل همتاشده", 3, 6),
        ("فاز ۳: سنجش دوز مواجهه تجمعی، نمونه‌گیری زیستی و کنترل مخدوش‌کننده‌ها", 6, 12),
        ("فاز ۴: پیگیری دوره‌ای ثبت پیامدهای بیماری و شاخص‌های بالینی", 10, 18),
        ("فاز ۵: مدل‌سازی رگرسیونی، تحلیل متغیرهای مخدوش‌کننده و تدوین گزارش", 18, 20)
    ],
    "PROGNOSTIC": [
        ("فاز ۱: تعریف کوهورت پیش‌آگهی، معیارهای ورود و ثبت بیومارکرهای پایه", 1, 3),
        ("فاز ۲: ارزیابی فاکتورهای پیش‌آگهی و اندازه‌گیری متغیرهای پیش‌بین", 3, 6),
        ("فاز ۳: پیگیری بقا و ثبت رخدادهای بالینی (Time-to-Event)", 6, 16),
        ("فاز ۴: تحلیل بقای کاپلان-مایر و مدل خطرات متناسب کاکس", 16, 18),
        ("فاز ۵: اعتبارسنجی داخلی مدل و گزارش قدرت تفکیک و کالیبراسیون", 18, 20)
    ],
    "MECHANISTIC": [
        ("فاز ۱: طراحی مداخله‌های ژنتیکی و فارماکولوژیک بر مسیر پیام‌رسانی", 1, 2),
        ("فاز ۲: کشت سلولی، تیمار با مهارکننده‌ها و سنجش اهداف بالادست", 2, 4),
        ("فاز ۳: سنجش‌های بیوشیمیایی فسفوریلاسیون، شکافت پروتئینی و بیان ژن", 4, 7),
        ("فاز ۴: ارزیابی فنوتیپی عملکردی (بقا، آپوپتوز، ترشح و مهاجرت)", 7, 9),
        ("فاز ۵: اثبات پیوستگی کسکید با رویکردهای نجات (Rescue Experiments) و تحلیل نهایی", 9, 12)
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
    def render_variable_table_markdown(cls, variables: List[Dict[str, str]]) -> str:
        """Renders the standard 6-column Markdown variable table."""
        header = "| نام متغیر | نقش متغیر | نوع متغیر | تعریف عملیاتی | نحوه اندازه‌گیری و ابزار | مقیاس / واحد سنجش |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        rows = []
        for v in variables:
            name = v.get("name", "")
            role = v.get("role", "")
            vtype = v.get("type", "")
            op_def = v.get("operational_definition", "")
            meas = v.get("measurement_method", "")
            unit = v.get("unit", "")
            rows.append(f"| **{name}** | {role} | {vtype} | {op_def} | {meas} | {unit} |")
        return header + "\n".join(rows)

    @classmethod
    def generate_timeline(cls, framework: str) -> List[Dict[str, Any]]:
        """Returns phased Gantt timeline appropriate for the study framework."""
        raw_phases = STUDY_TIMELINE_TEMPLATES.get(framework, STUDY_TIMELINE_TEMPLATES.get("EXPERIMENTAL_IN_VITRO", []))
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
    def render_timeline_markdown(cls, timeline: List[Dict[str, Any]], total_months: int = 12) -> str:
        """Renders standard Markdown Gantt chart table."""
        m_headers = " | ".join(str(m) for m in range(1, total_months + 1))
        sep_cols = " | ".join([":---:"] * total_months)
        header = f"| فاز اجرایی و شرح فعالیت‌ها | {m_headers} |\n| :--- | {sep_cols} |\n"
        rows = []
        for item in timeline:
            title = item.get("phase_title", "")
            start_m = item.get("start_month", 1)
            end_m = item.get("end_month", total_months)
            cells = []
            for m in range(1, total_months + 1):
                if start_m <= m <= end_m:
                    cells.append("■")
                else:
                    cells.append(" ")
            rows.append(f"| **{title}** | {' | '.join(cells)} |")
        return header + "\n".join(rows)

    @classmethod
    def generate_statistical_plan(cls, model_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Aligns statistical tests dynamically with outcome variable types and study design."""
        framework = model_dict.get("framework", "EXPERIMENTAL_IN_VITRO")
        outcomes = model_dict.get("primary_outcomes", [])
        interventions = model_dict.get("interventions_or_exposures", [])

        is_multi_agent = len(interventions) > 1
        
        tests = []
        if framework in ["EXPERIMENTAL_IN_VITRO", "EXPERIMENTAL_ANIMAL"]:
            if is_multi_agent:
                tests.append("تحلیل واریانس دوطرفه (Two-way ANOVA) جهت ارزیابی اثرات اصلی و اثر متقابل (Interaction effect)")
                tests.append("آزمون تعقیبی توکی (Tukey's HSD post-hoc test) جهت مقایسه‌های چندگانه میان گروه‌ها")
                tests.append("مدل‌های ریاضی استاندارد سنجش هم‌افزایی (مانند نسبت ترکیب یا نمایه میان‌کنش) جهت تعیین ماهیت تعامل")
            else:
                tests.append("تحلیل واریانس یک‌طرفه (One-way ANOVA) همراه با آزمون تعقیبی دانت یا توکی")
            tests.append("آزمون شاپیرو-ویلک (Shapiro-Wilk) جهت بررسی نرمال بودن توزیع داده‌ها")
        elif framework == "PICO":
            tests.append("تحلیل قصد درمان (Intention-to-Treat: ITT) به عنوان استراتژی اولیه تحلیل کارآزمایی")
            tests.append("مدل خطرات متناسب کاکس (Cox Proportional Hazards Model) جهت برازش نرخ رخدادها و برآورد نسبت خطر (Hazard Ratio)")
            tests.append("منحنی‌های بقای کاپلان-مایر (Kaplan-Meier survival curves) همراه با آزمون لگ-رتبه‌ای (Log-rank test)")
            tests.append("آزمون‌های مقایسه میانگین زوجی یا تحلیل کوواریانس (ANCOVA) برای تنظیم مقادیر پایه")
        elif framework == "DIAGNOSTIC":
            tests.append("محاسبه شاخص‌های تشخیصی: حساسیت (Sensitivity)، ویژگی (Specificity)، ارزش اخباری مثبت (PPV) و منفی (NPV)")
            tests.append("ترسیم منحنی مشخصه عملکرد سیستم (ROC Curve) و محاسبه مساحت زیر منحنی (AUC) با فواصل اطمینان ۹۵٪")
            tests.append("آزمون مک‌نمار (McNemar's test) جهت مقایسه عملکرد آزمون شاخص و استاندارد مرجع")
            tests.append("بررسی پایایی بین ارزیاب‌ها با ضریب کاپای کوهن (Cohen's Kappa)")
        elif framework == "PECO":
            tests.append("مدل رگرسیون لجستیک چندمتغیره (Multivariable Logistic Regression) جهت تعدیل مخدوش‌کننده‌ها")
            tests.append("برآورد نسبت شانس تعدیل‌شده (Adjusted Odds Ratio: aOR) با فواصل اطمینان ۹۵٪")
            tests.append("آزمون تمایل مواجهه (Propensity Score Matching) جهت همتاسازی گروه‌های در معرض و غیر در معرض")
        elif framework == "PROGNOSTIC":
            tests.append("مدل رگرسیون خطرات متناسب کاکس چندمتغیره (Multivariable Cox Regression)")
            tests.append("محاسبه شاخص هارل (Harrell's C-index) جهت سنجش قدرت تفکیک مدل پیش‌آگهی")
            tests.append("منحنی کالیبراسیون (Calibration Plot) جهت اعتبارسنجی انطباق پیش‌بینی با رخداد واقعی")
        else:
            tests.append("تحلیل واریانس یک‌طرفه (One-way ANOVA) همراه با آزمون تعقیبی دانت یا توکی")

        tests.append("سطح معنی‌داری آماری در تمام تحلیل‌ها p < 0.05 با فواصل اطمینان ۹۵٪ دوطرفه لحاظ خواهد شد")

        return {
            "primary_analysis": tests[0],
            "post_hoc_analysis": tests[1] if len(tests) > 1 else "Dunnett's test",
            "distribution_test": "Shapiro-Wilk normality test",
            "alpha_threshold": 0.05,
            "statistical_software": "R Statistical Environment / GraphPad Prism / SPSS",
            "complete_testing_strategy": tests
        }

    @classmethod
    def calculate_sample_size_plan(cls, model_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Provides mathematically rigorous and design-aware sample size guidance."""
        framework = model_dict.get("framework", "EXPERIMENTAL_IN_VITRO")
        if framework == "EXPERIMENTAL_IN_VITRO":
            return {
                "design_type": "IN_VITRO_CELLULAR",
                "biological_replicates": 3,
                "technical_replicates_per_plate": 3,
                "total_independent_runs": 3,
                "pseudo_replication_warning": "Technical replicates within the same plate must be averaged and treated as 1 biological unit to avoid pseudo-replication.",
                "formula_or_standard": "Triplicate independent biological passages (n=3 biological replicates, each assayed in technical triplicate)",
                "pilot_required": False
            }
        elif framework == "EXPERIMENTAL_ANIMAL":
            return {
                "design_type": "IN_VIVO_ANIMAL",
                "animals_per_group": 6,
                "formula_or_standard": "Mead's Resource Equation (E = N - B - T, where 10 <= E <= 20) and Charlebois Power Calculation",
                "alpha": 0.05,
                "power": 0.80,
                "pilot_required": False
            }
        elif framework in ["PICO", "PECO", "PROGNOSTIC"]:
            return {
                "design_type": "HUMAN_CLINICAL_OR_COHORT",
                "formula_or_standard": "Two-sample survival log-rank / proportions power equation: n = (Z_alpha + Z_beta)^2 * (p1(1-p1) + p2(1-p2)) / (p1 - p2)^2",
                "alpha": 0.05,
                "power": 0.80,
                "pilot_required": True,
                "note": "PILOT_REQUIRED if historical event rate or standard deviation in target sub-population is uncharacterized."
            }
        elif framework == "DIAGNOSTIC":
            return {
                "design_type": "DIAGNOSTIC_ACCURACY",
                "formula_or_standard": "Buderer's formula for diagnostic sensitivity and specificity: n = (Z_alpha/2)^2 * P * (1-P) / (L^2 * Prevalence)",
                "alpha": 0.05,
                "precision": 0.05,
                "pilot_required": False
            }
        return {"design_type": "GENERIC", "pilot_required": False}

    @classmethod
    def validate_objectives_hypotheses_variables_consistency(cls, model_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Cross-validates complete chain: Research Question -> Hypothesis -> Objective -> Independent Variable -> Dependent Variable -> Endpoint -> Statistical Analysis (Phase 24)."""
        objectives = model_dict.get("specific_objectives", [])
        hypotheses = model_dict.get("hypotheses", [])
        interventions = model_dict.get("interventions_or_exposures", [])
        outcomes = model_dict.get("primary_outcomes", [])
        endpoints = model_dict.get("endpoints", [o.get("name") for o in outcomes])

        chain_breaks = []

        # 1. Check Independent & Dependent Variables
        if not interventions:
            chain_breaks.append("MISSING_INDEPENDENT_VARIABLE")
        if not outcomes:
            chain_breaks.append("MISSING_DEPENDENT_VARIABLE")

        # 2. Check Objective <-> Endpoint Linkage
        if objectives and not endpoints:
            chain_breaks.append("OBJECTIVE_WITHOUT_ENDPOINT")

        # 3. Check Endpoint <-> Variable Linkage
        outcome_names = [o.get("name", "").lower() for o in outcomes]
        for ep in endpoints:
            if outcome_names and not any(o in str(ep).lower() or str(ep).lower() in o for o in outcome_names):
                chain_breaks.append(f"ENDPOINT_WITHOUT_VARIABLE: {ep}")

        # 4. Check Variable <-> Analysis Linkage
        stat_plan = cls.generate_statistical_plan(model_dict)
        if not stat_plan.get("primary_analysis"):
            chain_breaks.append("VARIABLE_WITHOUT_ANALYSIS")

        # 5. Check Hypothesis <-> Objective Alignment
        if hypotheses and not objectives:
            chain_breaks.append("HYPOTHESIS_WITHOUT_OBJECTIVE")
        elif hypotheses and objectives and len(hypotheses) > len(objectives) + 2:
            chain_breaks.append("UNGROUNDED_HYPOTHESIS_EXCEEDING_OBJECTIVES")

        is_consistent = (len(chain_breaks) == 0)

        return {
            "consistency_status": "CONSISTENT" if is_consistent else "DISCREPANCY_DETECTED",
            "is_graph_fully_connected": is_consistent,
            "objectives_count": len(objectives),
            "hypotheses_count": len(hypotheses),
            "interventions_count": len(interventions),
            "outcomes_count": len(outcomes),
            "endpoints_count": len(endpoints),
            "statistical_plan_aligned": bool(stat_plan.get("primary_analysis")),
            "discrepancies": chain_breaks
        }

    @classmethod
    def audit_statistical_feasibility(cls, model_dict: Dict[str, Any], proposed_test: Optional[str] = None) -> Dict[str, Any]:
        """Statistical feasibility gate verifying variable type, distribution assumptions, and test compatibility (Phase 22)."""
        framework = model_dict.get("framework", "EXPERIMENTAL_IN_VITRO")
        outcomes = model_dict.get("primary_outcomes", [])
        interventions = model_dict.get("interventions_or_exposures", [])

        inconsistencies = []

        # Check outcome type and appropriate test
        for out in outcomes:
            otype = str(out.get("type", "")).upper()
            if otype in ["HAZARD_RATIO", "MORTALITY", "TIME_TO_EVENT"] and framework == "EXPERIMENTAL_IN_VITRO":
                inconsistencies.append("TIME_TO_EVENT_ENDPOINT_IN_CELL_CULTURE_MODEL")
            if otype in ["SENSITIVITY", "SPECIFICITY", "ROC_AUC"] and framework not in ["DIAGNOSTIC", "PROGNOSTIC"]:
                inconsistencies.append("DIAGNOSTIC_METRIC_IN_INTERVENTIONAL_MODEL")

        # Test compatibility check
        if proposed_test:
            p_lower = proposed_test.lower()
            if "t-test" in p_lower and len(interventions) > 2:
                inconsistencies.append("STUDENT_T_TEST_USED_FOR_MULTI_ARM_EXPERIMENT")
            if "one-way anova" in p_lower and len(interventions) > 1 and "factorial" in str(model_dict).lower():
                inconsistencies.append("ONE_WAY_ANOVA_USED_FOR_FACTORIAL_COMBINATION")

        is_feasible = (len(inconsistencies) == 0)
        return {
            "feasibility_status": "STATISTICAL_PLAN_COMPATIBLE" if is_feasible else "STATISTICAL_PLAN_INCONSISTENT",
            "is_feasible": is_feasible,
            "inconsistencies": inconsistencies,
            "recommendation": "Statistical analysis plan conforms with experimental design and endpoint distributions." if is_feasible else f"Revise statistical plan: {', '.join(inconsistencies)}"
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
