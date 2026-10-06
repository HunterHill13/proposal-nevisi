#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
combination_model_selector.py - Unified Façade for Statistical and Combination Interaction Modeling
Proposal-Nevisi Engine v9.1 (Layer 2: Structural Compliance)

Architecturally separates:
1. Inferential Statistical Analysis Models (ANOVA, GLM, RM-ANOVA, Cox)
   via StatisticalAnalysisModelSelector
2. Pharmacological / Biological Combination Interaction Models (Chou-Talalay, Bliss, Loewe, ZIP, HSA)
   via CombinationInteractionModelSelector

Provides backward compatibility for existing callers and test suites while ensuring
scientifically sound model choices.
"""

from typing import Dict, List, Any, Optional
try:
    from scripts.statistical_model_selector import (
        StatisticalAnalysisModelSelector,
        StatisticalSelectionResult
    )
    from scripts.combination_interaction_model_selector import (
        CombinationInteractionModelSelector,
        CombinationInteractionResult
    )
except ImportError:
    from statistical_model_selector import (
        StatisticalAnalysisModelSelector,
        StatisticalSelectionResult
    )
    from combination_interaction_model_selector import (
        CombinationInteractionModelSelector,
        CombinationInteractionResult
    )

class CombinationModelSelector:
    """Unified façade providing both inferential statistical and synergy interaction model selection."""

    # Re-export component selectors
    statistical_selector = StatisticalAnalysisModelSelector
    interaction_selector = CombinationInteractionModelSelector

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
        Determines the optimal inferential statistical model.
        Distinguishes multi-group descriptive layouts from true factorial designs.
        """
        return StatisticalAnalysisModelSelector.select(
            study_design=study_design,
            outcome_type=outcome_type,
            groups_count=groups_count,
            paired=paired,
            repeated_measures=repeated_measures,
            is_factorial=is_factorial,
            factor_a_defined=factor_a_defined,
            factor_b_defined=factor_b_defined,
            interaction_estimable=interaction_estimable,
            covariates=covariates,
            non_parametric=non_parametric
        )

    @classmethod
    def select_interaction_model(
        cls,
        agent_a_type: str = "small_molecule",
        agent_b_type: str = "oncolytic_virus",
        dose_matrix_type: str = "checkerboard",
        num_dose_levels_a: int = 5,
        num_dose_levels_b: int = 5,
        endpoint_type: str = "cell_viability",
        live_virus_involved: Optional[bool] = None,
        schedule_dependent: bool = True
    ) -> CombinationInteractionResult:
        """
        Determines the pharmacological combination interaction / synergy model.
        """
        return CombinationInteractionModelSelector.select(
            agent_a_type=agent_a_type,
            agent_b_type=agent_b_type,
            dose_matrix_type=dose_matrix_type,
            num_dose_levels_a=num_dose_levels_a,
            num_dose_levels_b=num_dose_levels_b,
            endpoint_type=endpoint_type,
            live_virus_involved=live_virus_involved,
            schedule_dependent=schedule_dependent
        )

    @classmethod
    def generate_methodology_statistical_section(
        cls,
        statistical_result: StatisticalSelectionResult,
        interaction_result: Optional[CombinationInteractionResult] = None
    ) -> Dict[str, str]:
        """
        Generates a comprehensive, bilingual methodology narrative covering both
        inferential statistical testing and pharmacological synergy modeling.
        """
        stat = statistical_result
        inter = interaction_result

        fa_text = f"تحلیل آماری داده‌ها با استفاده از {stat.primary_model_fa} انجام خواهد شد. "
        fa_text += f"پیش‌فرض‌های آماری شامل {', '.join([a['fa'] for a in stat.assumption_tests])} مورد ارزیابی قرار می‌گیرند. "
        if stat.post_hoc_test:
            fa_text += f"در صورت معناداری اثر کلی، آزمون‌های تعقیبی {stat.post_hoc_test} جهت مقایسه‌های جفتی به کار گرفته می‌شوند. "
        fa_text += f"شاخص اندازه اثر بر اساس {stat.effect_size_metric} گزارش خواهد شد."

        if inter:
            fa_text += f"\n\nمدل ارزیابی برهم‌کنش و هم‌افزایی دارویی: سنجش هم‌افزایی/آنتاگونیسم با استفاده از {inter.recommended_model_fa} صورت می‌پذیرد. "
            fa_text += f"دلیل انتخاب: {inter.decision_rationale_fa} "
            if inter.viral_kinetic_considerations:
                fa_text += "\nملاحظات کینتیک بیولوژیک و ویروسی:\n- " + "\n- ".join(inter.viral_kinetic_considerations)

        en_text = f"Statistical analysis will be conducted using {stat.primary_model}. "
        en_text += f"Model assumptions including {', '.join([a['test'] for a in stat.assumption_tests])} will be verified. "
        if stat.post_hoc_test:
            en_text += f"Pairwise comparisons will be performed using {stat.post_hoc_test}. "
        en_text += f"Effect size will be quantified via {stat.effect_size_metric}."

        if inter:
            en_text += f"\n\nCombination Interaction Modeling: Synergism and antagonism will be evaluated using {inter.recommended_model}. "
            en_text += f"Rationale: {inter.decision_rationale}"

        return {
            "fa": fa_text,
            "en": en_text
        }
