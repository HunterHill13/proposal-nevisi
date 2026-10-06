#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
combination_model_selector.py - Universal Study-Design-Aware Statistical Model Selector
Proposal-Nevisi Engine v9.0 (Layer 2: Structural Compliance)

Selects the mathematically and epistemologically sound statistical model based on:
- study_design (in_vitro, in_vivo, RCT, observational, cohort, case_control, quasi-experimental)
- outcome_type (continuous, categorical, survival, count)
- groups_count
- paired / dependent structure
- repeated_measures
- covariates

Emits assumption verification tests, post-hoc procedures, effect size metrics, and rationale.
100% General-Purpose: Zero hardcoded project subjects.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class StatisticalSelectionResult:
    primary_model: str
    primary_model_fa: str
    assumption_tests: List[Dict[str, str]]
    post_hoc_test: Optional[str]
    effect_size_metric: str
    selection_justification: str
    selection_justification_fa: str
    recommended_software_modules: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary_model": self.primary_model,
            "primary_model_fa": self.primary_model_fa,
            "assumption_tests": self.assumption_tests,
            "post_hoc_test": self.post_hoc_test,
            "effect_size_metric": self.effect_size_metric,
            "selection_justification": self.selection_justification,
            "selection_justification_fa": self.selection_justification_fa,
            "recommended_software_modules": self.recommended_software_modules
        }

class CombinationModelSelector:
    """Universal selector determining appropriate statistical models from design parameters."""

    @classmethod
    def select(
        cls,
        study_design: str = "in_vitro",
        outcome_type: str = "continuous",
        groups_count: int = 4,
        paired: bool = False,
        repeated_measures: bool = False,
        covariates: Optional[List[str]] = None
    ) -> StatisticalSelectionResult:
        """
        Determines the optimal primary statistical model, assumption tests, and post-hoc methods.
        """
        design_clean = str(study_design).lower().strip()
        outcome_clean = str(outcome_type).lower().strip()
        covs = covariates or []
        num_covs = len(covs)

        # 1. Survival Analysis
        if outcome_clean == "survival":
            assumptions = [
                {"test": "Proportional Hazards Assumption (Schoenfeld residuals)", "fa": "آزمون فرض خطرات متناسب (بقایای شوئنفلد)"},
                {"test": "Log-Rank Test for Kaplan-Meier Curves", "fa": "آزمون لاگ-رنک برای منحنی‌های کاپلان-مایر"}
            ]
            post_hoc = "Pairwise Log-Rank with Benjamini-Hochberg FDR correction"
            effect_size = "Hazard Ratio (HR) with 95% Confidence Interval"
            just_en = (
                f"For time-to-event outcomes with {num_covs} covariates in a {study_design} setting, "
                f"Cox Proportional Hazards Regression provides unbiased estimation while accounting for censoring."
            )
            just_fa = (
                f"جهت تحلیل پیامدهای بقا و زمان تا رخداد با احتساب سانسور و {num_covs} متغیر مخدوش‌کننده، "
                f"مدل رگرسیون خطرات متناسب کاکس انتخاب گردید."
            )
            return StatisticalSelectionResult(
                primary_model="Cox Proportional Hazards Regression",
                primary_model_fa="رگرسیون خطرات متناسب کاکس (Cox Proportional Hazards)",
                assumption_tests=assumptions,
                post_hoc_test=post_hoc,
                effect_size_metric=effect_size,
                selection_justification=just_en,
                selection_justification_fa=just_fa,
                recommended_software_modules=["R (survival, survminer)", "Python (lifelines)", "SPSS Advanced"]
            )

        # 2. Categorical / Binary / Ordinal
        if outcome_clean in ["categorical", "binary", "dichotomous"]:
            if repeated_measures or paired:
                assumptions = [
                    {"test": "Sufficient Cell Expected Frequencies", "fa": "کفایت فراوانی‌های مورد انتظار در جداول توافقی"},
                    {"test": "Independent Subjects across Clusters", "fa": "استقلال خوشه‌های آزمودنی"}
                ]
                model_en = "Generalized Estimating Equations (GEE) / Mixed-Effects Logistic Regression"
                model_fa = "معادلات برآورد تعمیم‌یافته (GEE) / رگرسیون لجستیک اثرات آمیخته"
                effect_size = "Adjusted Odds Ratio (aOR) with 95% CI"
                just_en = "Repeated categorical measurements require GEE or mixed-effects logistic regression to handle within-subject clustering."
                just_fa = "اندازه‌گیری‌های مکرر طبقه‌ای جهت لحاظ همبستگی درون‌خوشه‌ای نیازمند معادلات GEE یا مدل‌های آمیخته هستند."
            elif groups_count == 2 and num_covs == 0:
                assumptions = [{"test": "Cochran Rule for Chi-Square", "fa": "قاعده کوکران برای آزمون خی‌دو (حداقل ۵ در هر خانه)"}]
                model_en = "Pearson Chi-Square Test / Fisher's Exact Test"
                model_fa = "آزمون خی‌دو پیرسون / آزمون دقیق فیشر"
                effect_size = "Relative Risk (RR) / Odds Ratio (OR)"
                just_en = "Two-group independent categorical comparison without covariates is optimally assessed via Chi-Square or Fisher's exact test."
                just_fa = "مقایسه متغیر طبقه‌ای میان دو گروه مستقل فاقد کووریت از طریق آزمون خی‌دو یا فیشر ارزیابی می‌شود."
            else:
                assumptions = [
                    {"test": "Hosmer-Lemeshow Goodness-of-Fit", "fa": "آزمون برازش هاسمر-لمشو"},
                    {"test": "Absence of Multicollinearity (VIF < 5)", "fa": "عدم هم‌خطی میان متغیرها"}
                ]
                model_en = "Multivariable Binary Logistic Regression"
                model_fa = "رگرسیون لجستیک دوگانه چندمتغیره"
                effect_size = "Adjusted Odds Ratio (aOR)"
                just_en = "Multivariable logistic regression assesses odds of categorical outcome controlling for covariates."
                just_fa = "رگرسیون لجستیک جهت برآورد شانس رخداد پیامد دوگانه با تعدیل متغیرهای مخدوش‌کننده الزامی است."

            return StatisticalSelectionResult(
                primary_model=model_en,
                primary_model_fa=model_fa,
                assumption_tests=assumptions,
                post_hoc_test=None,
                effect_size_metric=effect_size,
                selection_justification=just_en,
                selection_justification_fa=just_fa,
                recommended_software_modules=["R (stats, lme4)", "SPSS Complex Samples", "STATA"]
            )

        # 3. Count Data
        if outcome_clean == "count":
            assumptions = [
                {"test": "Overdispersion Test (Dispersion parameter > 1)", "fa": "آزمون پراکندگی بیش از حد (Overdispersion)"},
                {"test": "Zero-Inflation Evaluation", "fa": "ارزیابی فراوانی صفرهای مازاد"}
            ]
            model_en = "Negative Binomial Regression / Poisson Regression"
            model_fa = "رگرسیون دوجمله‌ای منفی / رگرسیون پواسون"
            effect_size = "Incidence Rate Ratio (IRR)"
            just_en = "Count outcomes are modeled using Poisson or Negative Binomial regression to accommodate skewness and overdispersion."
            just_fa = "داده‌های شمارشی به دلیل چولگی و واریانس نامساوی با رگرسیون دوجمله‌ای منفی یا پواسون مدل‌سازی می‌شوند."
            return StatisticalSelectionResult(
                primary_model=model_en,
                primary_model_fa=model_fa,
                assumption_tests=assumptions,
                post_hoc_test=None,
                effect_size_metric=effect_size,
                selection_justification=just_en,
                selection_justification_fa=just_fa,
                recommended_software_modules=["R (MASS)", "Python (statsmodels)"]
            )

        # 4. Continuous Outcomes (Standard experimental in vitro / in vivo / clinical trial)
        assumptions = [
            {"test": "Shapiro-Wilk Test for Normality", "fa": "آزمون شاپیرو-ویلک جهت سنجش نرمال بودن توزیع داده‌ها"},
            {"test": "Levene's Test for Homogeneity of Variances", "fa": "آزمون لون جهت همگنی واریانس‌ها (Homoscedasticity)"}
        ]
        if repeated_measures:
            assumptions.append({"test": "Mauchly's Test of Sphericity", "fa": "آزمون کرویت موچلی (Sphericity)"})

        # Factorial interaction in combination studies (e.g. 2x2 factor A and factor B)
        if design_clean in ["in_vitro", "in_vivo"] and groups_count >= 4 and not repeated_measures:
            model_en = "Two-Way Factorial Analysis of Variance (Two-way ANOVA) with Interaction"
            model_fa = "آنالیز واریانس دوطرفه فاکتوریل (Two-way ANOVA) همراه با سنجش اثر متقابل (Interaction)"
            post_hoc = "Tukey's Honestly Significant Difference (HSD) & Dunnett's test vs Control"
            effect_size = "Partial Eta Squared (η²p) and Cohen's d"
            just_en = (
                f"For a factorial combination study evaluating {groups_count} treatment groups, Two-way ANOVA "
                f"enables simultaneous testing of main effects and mutual interaction terms."
            )
            just_fa = (
                f"جهت بررسی تجربی ترکیب دوتایی با {groups_count} گروه، آنالیز واریانس دوطرفه (Two-way ANOVA) "
                f"امکان تفکیک اثرات اصلی هر مداخله و آزمون اثر متقابل (Interaction) را فراهم می‌آورد."
            )
        elif repeated_measures:
            model_en = "Repeated Measures Analysis of Variance (RM-ANOVA) / Linear Mixed-Effects Model"
            model_fa = "آنالیز واریانس اندازه‌گیری‌های مکرر (RM-ANOVA) / مدل اثرات آمیخته خطی"
            post_hoc = "Bonferroni-adjusted pairwise comparisons"
            effect_size = "Partial Eta Squared (η²p)"
            just_en = "Repeated assessments over time require RM-ANOVA with Greenhouse-Geisser correction for sphericity departures."
            just_fa = "اندازه‌گیری‌های متوالی زمانی نیازمند آنالیز واریانس اندازه‌گیری‌های مکرر با تصحیح گرین‌هاوس-گیسر است."
        elif groups_count == 2:
            if paired:
                model_en = "Paired Samples t-Test (or Wilcoxon Signed-Rank Test if non-normal)"
                model_fa = "آزمون تی زوجی (Paired t-test) / آزمون ویلکاکسون در صورت عدم نرمال بودن"
            else:
                model_en = "Independent Samples t-Test (or Mann-Whitney U Test if non-normal)"
                model_fa = "آزمون تی مستقل (Independent t-test) / آزمون مان-ویتنی در صورت عدم نرمال بودن"
            post_hoc = None
            effect_size = "Cohen's d with 95% Confidence Interval"
            just_en = f"Two independent/paired groups with continuous outcome are tested via Student's t-test with non-parametric fallback."
            just_fa = "مقایسه دو گروه با پیامد کمی پیوسته بر پایه آزمون تی با پشتیبان ناپارامتری انجام می‌شود."
        else:
            # One-way ANOVA or ANCOVA
            if num_covs > 0:
                model_en = "One-Way Analysis of Covariance (ANCOVA)"
                model_fa = "آنالیز کوواریانس یک‌طرفه (ANCOVA)"
                post_hoc = "Bonferroni-adjusted marginal means comparisons"
                effect_size = "Partial Eta Squared (η²p)"
                just_en = f"Comparing {groups_count} groups while adjusting for {num_covs} continuous covariates necessitates ANCOVA."
                just_fa = f"مقایسه {groups_count} گروه با تعدیل {num_covs} متغیر مخدوش‌کننده پیوسته مستلزم آنالیز کوواریانس (ANCOVA) است."
            else:
                model_en = "One-Way Analysis of Variance (One-way ANOVA)"
                model_fa = "آنالیز واریانس یک‌طرفه (One-way ANOVA)"
                post_hoc = "Tukey's HSD post-hoc test (or Games-Howell if variances unequal)"
                effect_size = "Eta Squared (η²) and Cohen's d"
                just_en = f"Comparing continuous outcome across {groups_count} independent experimental groups."
                just_fa = f"مقایسه میانگین پیامد پیوسته میان {groups_count} گروه مستقل آزمایشی با تحلیل واریانس یک‌طرفه ارزیابی می‌گردد."

        return StatisticalSelectionResult(
            primary_model=model_en,
            primary_model_fa=model_fa,
            assumption_tests=assumptions,
            post_hoc_test=post_hoc,
            effect_size_metric=effect_size,
            selection_justification=just_en,
            selection_justification_fa=just_fa,
            recommended_software_modules=["GraphPad Prism 10", "R (rstatix, car)", "SPSS Statistics"]
        )

combination_model_selector = CombinationModelSelector
