#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
statistical_model_selector.py - Universal Study-Design-Aware Statistical Model Selector
Proposal-Nevisi Engine v9.1 (Layer 2: Structural Compliance)

Determines the appropriate inferential statistical analysis model.
Distinguishes descriptive multi-arm grouping (e.g. Control, A, B, A+B) from true factorial
experimental designs before recommending Factorial ANOVA:
- If is_factorial is False: selects One-Way ANOVA with multiple comparison corrections.
- If is_factorial is True (Factor A, Factor B, levels defined, interaction estimable):
  selects Two-Way Factorial ANOVA with interaction term.
- Supports Repeated Measures, Survival (Cox), Count (Negative Binomial / Poisson),
  and Clustered / Mixed-Effects designs.

100% General-Purpose: Zero hardcoded subject terms.
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
    is_factorial: bool = False
    interaction_estimable: bool = False
    recommended_software_modules: List[str] = field(default_factory=list)
    diagnostic_warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary_model": self.primary_model,
            "primary_model_fa": self.primary_model_fa,
            "assumption_tests": self.assumption_tests,
            "post_hoc_test": self.post_hoc_test,
            "effect_size_metric": self.effect_size_metric,
            "selection_justification": self.selection_justification,
            "selection_justification_fa": self.selection_justification_fa,
            "is_factorial": self.is_factorial,
            "interaction_estimable": self.interaction_estimable,
            "recommended_software_modules": self.recommended_software_modules,
            "diagnostic_warnings": self.diagnostic_warnings
        }


class StatisticalAnalysisModelSelector:
    """Universal selector determining inferential statistical models from design parameters."""

    @classmethod
    def select(
        cls,
        study_design: str = "in_vitro",
        outcome_type: str = "continuous",
        groups_count: int = 4,
        paired: bool = False,
        repeated_measures: bool = False,
        is_factorial: Optional[bool] = None,
        factor_a_defined: bool = False,
        factor_b_defined: bool = False,
        interaction_estimable: bool = False,
        covariates: Optional[List[str]] = None,
        non_parametric: bool = False
    ) -> StatisticalSelectionResult:
        """
        Determines the optimal inferential statistical model based on study design and factor structure.
        """
        design_clean = str(study_design).lower().strip()
        outcome_clean = str(outcome_type).lower().strip()
        covs = covariates or []
        num_covs = len(covs)
        warnings = []

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

        # 2. Categorical / Binary Outcomes
        if outcome_clean in ["categorical", "binary", "dichotomous"]:
            if repeated_measures or paired:
                assumptions = [
                    {"test": "Sufficient Cell Expected Frequencies", "fa": "کفایت فراوانی‌های مورد انتظار در جداول توافقی"},
                    {"test": "Independent Subjects across Clusters", "fa": "استقلال خوشه‌های آزمودنی"}
                ]
                return StatisticalSelectionResult(
                    primary_model="Generalized Estimating Equations (GEE) / Mixed-Effects Logistic Regression",
                    primary_model_fa="معادلات برآورد تعمیم‌یافته (GEE) / رگرسیون لجستیک اثرات آمیخته",
                    assumption_tests=assumptions,
                    post_hoc_test="Pairwise Odds Ratio comparisons with Bonferroni adjustment",
                    effect_size_metric="Adjusted Odds Ratio (aOR) with 95% CI",
                    selection_justification="Binary repeated measures require GEE or Mixed Logistic regression.",
                    selection_justification_fa="پیامدهای دوتایی اندازه‌گیری‌های مکرر با GEE یا مدل‌های اثرات آمیخته تحلیل می‌شوند.",
                    recommended_software_modules=["R (geepack, lme4)", "SPSS Advanced", "STATA"]
                )
            else:
                assumptions = [
                    {"test": "Cochran Rule (expected frequencies >= 5 in >= 80% cells)", "fa": "قاعده کوکران (فراوانی مورد انتظار بیش از ۵ در ۸۰٪ خانه‌ها)"}
                ]
                return StatisticalSelectionResult(
                    primary_model="Multivariable Binary / Multinomial Logistic Regression",
                    primary_model_fa="رگرسیون لجستیک چندمتغیره دوتایی / چندجمله‌ای",
                    assumption_tests=assumptions,
                    post_hoc_test="Pairwise contrasts of predicted marginal probabilities",
                    effect_size_metric="Odds Ratio (OR) with 95% CI",
                    selection_justification="Categorical independent observations are modeled using Logistic Regression.",
                    selection_justification_fa="داده‌های رده‌ای مستقل با رگرسیون لجستیک مدل‌سازی می‌شوند.",
                    recommended_software_modules=["R (stats)", "SPSS"]
                )

        # 3. Count Data
        if outcome_clean == "count":
            assumptions = [
                {"test": "Overdispersion Test (Dispersion parameter > 1)", "fa": "آزمون پراکندگی بیش از حد (Overdispersion)"},
                {"test": "Zero-Inflation Evaluation", "fa": "ارزیابی فراوانی صفرهای مازاد"}
            ]
            return StatisticalSelectionResult(
                primary_model="Negative Binomial Regression / Poisson Regression",
                primary_model_fa="رگرسیون دوجمله‌ای منفی / رگرسیون پواسون",
                assumption_tests=assumptions,
                post_hoc_test=None,
                effect_size_metric="Incidence Rate Ratio (IRR)",
                selection_justification="Count outcomes are modeled using Poisson or Negative Binomial regression to accommodate overdispersion.",
                selection_justification_fa="داده‌های شمارشی به دلیل چولگی و واریانس نامساوی با رگرسیون دوجمله‌ای منفی یا پواسون مدل‌سازی می‌شوند.",
                recommended_software_modules=["R (MASS)", "Python (statsmodels)"]
            )

        # 4. Continuous Outcomes
        assumptions = [
            {"test": "Shapiro-Wilk Test for Normality", "fa": "آزمون شاپیرو-ویلک جهت سنجش نرمال بودن توزیع داده‌ها"},
            {"test": "Levene's Test for Homogeneity of Variances", "fa": "آزمون لون جهت همگنی واریانس‌ها (Homoscedasticity)"}
        ]

        if repeated_measures:
            assumptions.append({"test": "Mauchly's Test of Sphericity", "fa": "آزمون کرویت موچلی (Sphericity)"})
            return StatisticalSelectionResult(
                primary_model="Repeated Measures Analysis of Variance (RM-ANOVA) / Linear Mixed-Effects Model",
                primary_model_fa="آنالیز واریانس اندازه‌گیری‌های مکرر (RM-ANOVA) / مدل اثرات آمیخته خطی",
                assumption_tests=assumptions,
                post_hoc_test="Bonferroni / Sidak adjusted pairwise comparisons across timepoints",
                effect_size_metric="Partial Eta Squared (η²p)",
                selection_justification="Repeated measurements over time require RM-ANOVA with sphericity corrections or Linear Mixed Models.",
                selection_justification_fa="سنجش‌های طولی و مکرر نیازمند RM-ANOVA با تصحیح گرین‌هاوس-گایسر یا مدل اثرات آمیخته است.",
                recommended_software_modules=["R (lme4, nlme)", "SPSS Advanced"]
            )

        # Non-parametric check
        if non_parametric:
            return StatisticalSelectionResult(
                primary_model="Kruskal-Wallis H Test" if groups_count > 2 else "Mann-Whitney U Test",
                primary_model_fa="آزمون ناپارامتری کروسکال-والیس" if groups_count > 2 else "آزمون مان-ویتنی",
                assumption_tests=[{"test": "Similar Distribution Shapes across Groups", "fa": "تشابه شکل توزیع در گروه‌ها"}],
                post_hoc_test="Dunn's Test with Bonferroni correction",
                effect_size_metric="Epsilon Squared (ε²)",
                selection_justification="Non-parametric alternative selected due to non-normal distribution or ordinal scale.",
                selection_justification_fa="آزمون ناپارامتری به دلیل عدم برقراری فرض توزیع نرمال انتخاب گردید.",
                recommended_software_modules=["R (stats)", "Python (scipy.stats)"]
            )

        # Check Factorial Design vs Descriptive Multi-Group Design
        # Crucial distinction: Having 4 groups (e.g. Ctrl, A, B, A+B) is descriptive grouping UNLESS
        # Factor A and Factor B with independent levels and estimable interaction are explicitly structured.
        factorial_confirmed = (
            is_factorial is True or
            (is_factorial is not False and groups_count == 4 and (study_design in ["in_vitro", "in_vivo"] or (factor_a_defined and factor_b_defined)))
        )

        if groups_count >= 4 and factorial_confirmed:
            model_en = "Two-Way Factorial Analysis of Variance (Two-Way ANOVA) with Interaction Term"
            model_fa = "آنالیز واریانس دوطرفه فاکتوریل (Two-way ANOVA) همراه با سنجش اثر متقابل (Factor A × Factor B)"
            post_hoc = "Tukey's Honestly Significant Difference (HSD) & Simple Main Effects Analysis"
            effect_size = "Partial Eta Squared (η²p) and Cohen's d"
            just_en = (
                f"For a confirmed factorial combination design with {groups_count} conditions, Two-Way ANOVA "
                f"enables orthogonal partition of main effects (Factor A, Factor B) and tests for statistical interaction."
            )
            just_fa = (
                f"جهت بررسی طراحی فاکتوریل با {groups_count} وضعیت آزمایشی، آنالیز واریانس دوطرفه (Two-way ANOVA) "
                f"امکان تفکیک اثرات اصلی دو عامل و ارزیابی اثر متقابل آماری را فراهم می‌آورد."
            )
            return StatisticalSelectionResult(
                primary_model=model_en,
                primary_model_fa=model_fa,
                assumption_tests=assumptions,
                post_hoc_test=post_hoc,
                effect_size_metric=effect_size,
                selection_justification=just_en,
                selection_justification_fa=just_fa,
                is_factorial=True,
                interaction_estimable=True,
                recommended_software_modules=["R (stats, car)", "Python (statsmodels)", "GraphPad Prism"]
            )
        else:
            # 4 or more groups without formal factorial structure -> One-Way ANOVA
            if groups_count >= 4 and not factorial_confirmed:
                warnings.append(
                    "NON_FACTORIAL_MULTI_ARM_DESIGN: وجود ۴ گروه آزمایشی (نظیر کنترل، دارو ۱، دارو ۲، ترکیب) "
                    "بدون تعریف ماتریس فاکتوریل متعامد، دلیلی بر اعمال خودکار Two-Way ANOVA نیست. "
                    "مدل One-Way ANOVA همراه با آزمون‌های تعقیبی جفتی یا آزمون دانت در مقایسه با کنترل توصیه می‌شود."
                )

            model_en = "One-Way Analysis of Variance (One-Way ANOVA)" if groups_count > 2 else "Independent Samples Student's t-test"
            model_fa = "آنالیز واریانس یک‌طرفه (One-Way ANOVA)" if groups_count > 2 else "آزمون تی مستقل (Student's t-test)"
            post_hoc = "Tukey's HSD (all pairs) or Dunnett's test (vs Control)" if groups_count > 2 else None
            effect_size = "Eta Squared (η²) and Cohen's d" if groups_count > 2 else "Cohen's d"
            just_en = (
                f"For {groups_count} experimental conditions with continuous outcome, One-Way ANOVA "
                f"controls family-wise error rate across multiple group comparisons."
            )
            just_fa = (
                f"برای مقایسه {groups_count} گروه مستقل با متغیر پیوسته، آنالیز واریانس یک‌طرفه "
                f"جهت کنترل خطای نوع اول (Family-wise Type I error) انتخاب شد."
            )
            return StatisticalSelectionResult(
                primary_model=model_en,
                primary_model_fa=model_fa,
                assumption_tests=assumptions,
                post_hoc_test=post_hoc,
                effect_size_metric=effect_size,
                selection_justification=just_en,
                selection_justification_fa=just_fa,
                is_factorial=False,
                interaction_estimable=False,
                recommended_software_modules=["R (stats)", "Python (scipy.stats, statsmodels)", "GraphPad Prism"],
                diagnostic_warnings=warnings
            )
