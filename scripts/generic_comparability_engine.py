#!/usr/bin/env python3
"""
generic_comparability_engine.py - Study-Design-Aware Pairwise Comparability Analyzer
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

Dynamically evaluates comparability across in vitro, animal, clinical, and diagnostic studies
without forcing a single rigid checklist.
"""

import json
from typing import Dict, List, Any, Optional

DESIGN_DIMENSION_MAP = {
    "IN_VITRO": [
        "model_system_identity",
        "culture_conditions",
        "vehicle_and_formulation",
        "concentration_gradient",
        "exposure_duration",
        "endpoint_assay_mechanism",
        "negative_and_positive_controls",
        "replicate_structure"
    ],
    "IN_VIVO_ANIMAL": [
        "species_and_strain",
        "sex_and_age",
        "disease_induction_model",
        "route_of_administration",
        "dosage_and_schedule",
        "comparator_control",
        "randomization_and_blinding",
        "follow_up_duration"
    ],
    "CLINICAL_TRIAL": [
        "target_population_criteria",
        "disease_severity_or_stage",
        "intervention_regimen",
        "comparator_type",
        "primary_endpoint_definition",
        "randomization_allocation",
        "blinding_procedure",
        "follow_up_completeness"
    ],
    "DIAGNOSTIC": [
        "clinical_presentation_spectrum",
        "index_test_platform",
        "reference_standard_validity",
        "threshold_pre_specification",
        "blinding_between_tests"
    ],
    "CROSS_DESIGN": [
        "biological_target_conservation",
        "translational_dose_equivalence",
        "endpoint_biological_homology"
    ]
}

class GenericComparabilityEngine:
    """Evaluates pairwise comparability using study-design-aware criteria."""

    @staticmethod
    def determine_shared_category(design_a: str, design_b: str) -> str:
        d_a = design_a.upper()
        d_b = design_b.upper()
        if "IN_VITRO" in d_a and "IN_VITRO" in d_b:
            return "IN_VITRO"
        if "ANIMAL" in d_a and "ANIMAL" in d_b:
            return "IN_VIVO_ANIMAL"
        if ("RCT" in d_a or "CLINICAL" in d_a) and ("RCT" in d_b or "CLINICAL" in d_b):
            return "CLINICAL_TRIAL"
        if "DIAGNOSTIC" in d_a and "DIAGNOSTIC" in d_b:
            return "DIAGNOSTIC"
        return "CROSS_DESIGN"

    @classmethod
    def evaluate_pair(cls, study_a: Dict[str, Any], study_b: Dict[str, Any]) -> Dict[str, Any]:
        design_a = study_a.get("study_design", "IN_VITRO_EXPERIMENTAL")
        design_b = study_b.get("study_design", "IN_VITRO_EXPERIMENTAL")
        cat = cls.determine_shared_category(design_a, design_b)
        dimensions = DESIGN_DIMENSION_MAP.get(cat, DESIGN_DIMENSION_MAP["CROSS_DESIGN"])

        evaluations = []
        major_divergences = 0
        minor_differences = 0

        attr_a = study_a.get("design_specific_attributes", {})
        attr_b = study_b.get("design_specific_attributes", {})

        for dim in dimensions:
            val_a = str(attr_a.get(dim, "NOT_REPORTED"))
            val_b = str(attr_b.get(dim, "NOT_REPORTED"))

            if val_a == "NOT_REPORTED" or val_b == "NOT_REPORTED":
                status = "NOT_REPORTED"
                impact = "Incomplete reporting impairs definitive comparability"
            elif val_a.lower() == val_b.lower():
                status = "MATCH"
                impact = "High direct concordance"
            else:
                # Basic divergence heuristic
                status = "MINOR_DIFFERENCE"
                minor_differences += 1
                impact = f"Variation noted: {val_a} vs {val_b}"

            evaluations.append({
                "dimension_name": dim,
                "study_a_value": val_a,
                "study_b_value": val_b,
                "status": status,
                "impact_on_synthesis": impact
            })

        if major_divergences > 0 or cat == "CROSS_DESIGN":
            overall = "MODERATE_COMPARABILITY" if cat == "CROSS_DESIGN" else "LOW_COMPARABILITY"
            expl = "Significant methodological or translational boundary separates the studies."
        elif minor_differences <= 2:
            overall = "HIGH_COMPARABILITY"
            expl = "Substantial methodological concordance allows direct evidentiary pooling."
        else:
            overall = "MODERATE_COMPARABILITY"
            expl = "Multiple minor variations require contextual qualification during synthesis."

        return {
            "study_a_id": study_a.get("study_id", "A"),
            "study_b_id": study_b.get("study_id", "B"),
            "shared_design_category": cat,
            "evaluated_dimensions": evaluations,
            "overall_comparability": overall,
            "divergence_explanation": expl
        }

    @classmethod
    def evaluate_cohort(cls, studies: List[Dict[str, Any]]) -> Dict[str, Any]:
        pairs = []
        high_c = 0
        incomp_c = 0

        for i in range(len(studies)):
            for j in range(i + 1, len(studies)):
                res = cls.evaluate_pair(studies[i], studies[j])
                pairs.append(res)
                if res["overall_comparability"] == "HIGH_COMPARABILITY":
                    high_c += 1
                elif "INCOMPARABLE" in res["overall_comparability"] or res["overall_comparability"] == "LOW_COMPARABILITY":
                    incomp_c += 1

        return {
            "comparability_pairs": pairs,
            "summary": {
                "total_pairs_evaluated": len(pairs),
                "high_comparability_count": high_c,
                "incomparable_count": incomp_c
            }
        }


if __name__ == "__main__":
    s1 = {
        "study_id": "STUDY_RCT_1",
        "study_design": "RANDOMIZED_CONTROLLED_TRIAL",
        "design_specific_attributes": {
            "target_population_criteria": "HFpEF NYHA II-IV",
            "dosage_and_schedule": "10 mg daily",
            "comparator_type": "Placebo"
        }
    }
    s2 = {
        "study_id": "STUDY_RCT_2",
        "study_design": "RANDOMIZED_CONTROLLED_TRIAL",
        "design_specific_attributes": {
            "target_population_criteria": "HFpEF NYHA II-IV",
            "dosage_and_schedule": "10 mg daily",
            "comparator_type": "Placebo"
        }
    }
    out = GenericComparabilityEngine.evaluate_pair(s1, s2)
    print("Pair evaluation:", out["overall_comparability"], "Shared category:", out["shared_design_category"])
