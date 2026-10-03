#!/usr/bin/env python3
"""
generic_contradiction_engine.py - Extensible Contradiction & Negative Evidence Analyzer
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

Classifies negative evidence across 15 universal categories and resolves
TRUE_CONTRADICTION vs CONTEXTUAL_DISAGREEMENT without domain-specific hard-coding.
"""

import json
from typing import Dict, List, Any, Optional

EXTENSIBLE_CONTRADICTION_TAXONOMY = {
    "NULL_RESULT": "No statistically significant difference between intervention and comparator (p >= 0.05)",
    "NO_EFFECT": "Biological inertness; absence of phenotypic or biochemical shift at tested range",
    "ANTAGONISM": "Combined efficacy is strictly inferior to monotherapy or CI > 1.2",
    "SUBADDITIVITY": "Combined response is less than algebraic sum without overt antagonism",
    "TOXICITY": "Dose-limiting tissue necrosis, host cell lethality, or organ damage",
    "OFF_TARGET_EFFECT": "Non-specific engagement with unintended pathways or receptors",
    "RESISTANCE": "Acquired or innate loss of sensitivity, selection of escape mutations",
    "NON_RESPONSE": "Primary non-responsiveness within specific genetic or clinical subsets",
    "SAFETY_LIMITATION": "Narrow therapeutic window; overlapping MTD and biologically active dose",
    "DOSE_LIMITATION": "Activity restricted to supra-physiological, clinically unachievable levels",
    "TIME_LIMITATION": "Rapidly transient effect due to receptor desensitization or negative feedback",
    "MODEL_LIMITATION": "Efficacy demonstrated in 2D cell cultures but completely failed in 3D or in vivo models",
    "TRANSLATIONAL_FAILURE": "Preclinical in vitro / animal efficacy failed to translate to clinical benefit",
    "METHODOLOGICAL_CONFLICT": "Apparent effect driven by optical interference, vehicle toxicity, or assay artifact",
    "CONTRADICTORY_RESULT": "Opposite biological effect observed under ostensibly identical experimental parameters"
}

class GenericContradictionEngine:
    """Detects, categorizes, and contextualizes scientific disagreements."""

    @classmethod
    def analyze_discrepancy(cls, positive_finding: Dict[str, Any], negative_finding: Dict[str, Any]) -> Dict[str, Any]:
        """Resolves whether a discrepancy is a TRUE_CONTRADICTION or CONTEXTUAL_DISAGREEMENT."""
        pos_ctx = positive_finding.get("context_parameters", {})
        neg_ctx = negative_finding.get("context_parameters", {})

        mismatches = []
        for key in ["dose", "exposure_time", "cell_line_or_model", "species", "formulation", "assay"]:
            val_pos = str(pos_ctx.get(key, "")).lower()
            val_neg = str(neg_ctx.get(key, "")).lower()
            if val_pos and val_neg and val_pos != val_neg:
                mismatches.append(f"{key}: '{val_pos}' vs '{val_neg}'")

        category = negative_finding.get("category", "CONTRADICTORY_RESULT")
        if category not in EXTENSIBLE_CONTRADICTION_TAXONOMY:
            category = "CONTRADICTORY_RESULT"

        if not mismatches:
            classification = "TRUE_CONTRADICTION"
            rationale = "Studies utilized ostensibly identical experimental parameters (dose, duration, model, assay) yet observed conflicting outcomes. Suggests uncharacterized biological modifiers or reproducibility divergence."
        else:
            classification = "CONTEXTUAL_DISAGREEMENT"
            rationale = f"Discrepancy is functionally explained by experimental parameter variations: {'; '.join(mismatches)}."

        return {
            "contradiction_type": classification,
            "category": category,
            "category_definition": EXTENSIBLE_CONTRADICTION_TAXONOMY[category],
            "contextual_divergences": mismatches,
            "scientific_rationale": rationale,
            "positive_study_id": positive_finding.get("study_id"),
            "negative_study_id": negative_finding.get("study_id")
        }

    @classmethod
    def build_contradiction_report(cls, negative_findings: List[Dict[str, Any]], search_boundary: Dict[str, Any]) -> Dict[str, Any]:
        """Compiles negative evidence report adhering to the strict absence-of-contradiction rule."""
        if not negative_findings:
            return {
                "contradiction_status": "NO_RELEVANT_CONTRADICTING_EVIDENCE_IDENTIFIED",
                "total_negative_findings": 0,
                "discrepancy_analyses": [],
                "search_boundary": search_boundary,
                "epistemic_caveat": "Absence of identified contradictory evidence reflects literature retrieved within the designated search boundary and cannot prove the universal non-existence of negative outcomes."
            }

        analyses = []
        for item in negative_findings:
            mock_pos = {"study_id": "PRIMARY_HYPOTHESIS", "context_parameters": item.get("target_context", {})}
            analyses.append(cls.analyze_discrepancy(mock_pos, item))

        return {
            "contradiction_status": "CONTRADICTORY_OR_QUALIFYING_EVIDENCE_IDENTIFIED",
            "total_negative_findings": len(negative_findings),
            "discrepancy_analyses": analyses,
            "search_boundary": search_boundary,
            "epistemic_caveat": "Identified negative findings provide essential boundary conditions and safety/efficacy thresholds."
        }


if __name__ == "__main__":
    pos = {"study_id": "STUDY_A", "context_parameters": {"dose": "10 uM", "cell_line_or_model": "A549", "assay": "MTT"}}
    neg = {"study_id": "STUDY_B", "category": "NULL_RESULT", "context_parameters": {"dose": "10 uM", "cell_line_or_model": "A549", "assay": "MTT"}}
    res = GenericContradictionEngine.analyze_discrepancy(pos, neg)
    print("Identical params result:", res["contradiction_type"])

    neg_diff = {"study_id": "STUDY_C", "category": "DOSE_LIMITATION", "context_parameters": {"dose": "0.5 uM", "cell_line_or_model": "A549", "assay": "MTT"}}
    res_diff = GenericContradictionEngine.analyze_discrepancy(pos, neg_diff)
    print("Different params result:", res_diff["contradiction_type"], "Mismatches:", res_diff["contextual_divergences"])
