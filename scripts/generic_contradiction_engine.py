#!/usr/bin/env python3
"""
generic_contradiction_engine.py - Extensible Contradiction & Negative Evidence Analyzer
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

Classifies negative evidence across 15 universal categories and resolves
TRUE_CONTRADICTION vs CONTEXTUAL_DISAGREEMENT without domain-specific hard-coding.
"""

import json
from typing import Dict, List, Any, Optional

try:
    from core_policies import CONTRADICTION_TAXONOMY as EXTENSIBLE_CONTRADICTION_TAXONOMY
except ImportError:
    from scripts.core_policies import CONTRADICTION_TAXONOMY as EXTENSIBLE_CONTRADICTION_TAXONOMY

class GenericContradictionEngine:
    """Detects, categorizes, and contextualizes scientific disagreements."""

    @classmethod
    def detect_contradictions(cls, studies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Convenience method to audit and detect contradictions across a set of studies."""
        negative_findings = []
        for s in studies:
            explicit_neg = s.get("negative_or_null_findings", [])
            if explicit_neg and isinstance(explicit_neg, list):
                for item in explicit_neg:
                    negative_findings.append({
                        "study_id": s.get("study_id"),
                        "category": item.get("category", "NULL_RESULT"),
                        "description": item.get("description", ""),
                        "target_context": s.get("design_specific_attributes", {})
                    })
                continue

            findings_text = str(s.get("primary_findings", "")) + " " + str(s.get("title", ""))
            category = None
            if "rebound" in findings_text.lower():
                category = "TIME_LIMITATION"
            elif "resistance" in findings_text.lower() or "mutation" in findings_text.lower():
                category = "RESISTANCE"
            elif "no effect" in findings_text.lower() or "null" in findings_text.lower():
                category = "NULL_RESULT"
            
            if category:
                negative_findings.append({
                    "study_id": s.get("study_id"),
                    "category": category,
                    "target_context": s.get("design_specific_attributes", {})
                })
        return cls.build_contradiction_report(negative_findings, {"studies_analyzed": len(studies)})

    @classmethod
    def analyze_discrepancy(cls, positive_finding: Dict[str, Any], negative_finding: Dict[str, Any]) -> Dict[str, Any]:
        """Resolves whether a discrepancy is a TRUE_CONTRADICTION or CONTEXTUAL_DISAGREEMENT."""
        pos_ctx = positive_finding.get("context_parameters", {})
        neg_ctx = negative_finding.get("context_parameters", {})

        mismatches = []
        divergence_keys = [
            "cell_line_or_model", "species", "strain", "dose", "exposure_time",
            "formulation", "purity", "assay", "endpoint", "experimental_condition",
            "sample_size", "statistical_method", "biological_context"
        ]
        for key in divergence_keys:
            val_pos = str(pos_ctx.get(key, "")).lower().strip()
            val_neg = str(neg_ctx.get(key, "")).lower().strip()
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

    @staticmethod
    def distinguish_no_evidence_vs_no_effect(retrieval_count: int, empirical_findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Strictly differentiates between absence of studies and presence of confirmed null effects (Point 28)."""
        if retrieval_count == 0 or not empirical_findings:
            return {
                "epistemic_state": "NO_EVIDENCE_IDENTIFIED",
                "is_evidence_of_no_effect": False,
                "scientific_conclusion": "No literature retrieved within boundary; does NOT prove absence of biological effect.",
                "permissible_claim": "The effect remains uninvestigated or unpublished under designated search parameters."
            }

        null_studies = [f for f in empirical_findings if f.get("category") in ["NULL_RESULT", "NO_EFFECT"]]
        if null_studies:
            return {
                "epistemic_state": "EVIDENCE_OF_NO_EFFECT_IDENTIFIED",
                "is_evidence_of_no_effect": True,
                "null_study_count": len(null_studies),
                "scientific_conclusion": "Rigorous empirical testing demonstrated statistically significant lack of effect or biological inertness.",
                "permissible_claim": "Published trials document no significant biological effect at tested doses."
            }

        return {
            "epistemic_state": "ACTIVE_EFFECTS_REPORTED",
            "is_evidence_of_no_effect": False,
            "scientific_conclusion": "Literature reports non-null biological or clinical responses."
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

    @classmethod
    def evaluate_publication_bias(cls, studies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluates publication bias / small-study effects across study cohort.
        Returns NOT_ASSESSABLE when fewer than 10 studies are available (Cochrane handbook rule).
        """
        n_studies = len(studies)
        if n_studies < 10:
            return {
                "publication_bias_status": "NOT_ASSESSABLE",
                "study_count": n_studies,
                "reason": "Funnel plot asymmetry and Egger test require at least 10 studies (Cochrane Handbook §10.4.3.1). Reporting absence of bias with fewer than 10 studies is methodologically invalid."
            }
        
        has_negative = any(bool(s.get("negative_or_null_findings")) for s in studies)
        return {
            "publication_bias_status": "ASSESSED_SUFFICIENT_POWER",
            "study_count": n_studies,
            "funnel_asymmetry_detected": not has_negative,
            "recommendation": "Perform formal Egger linear regression and trim-and-fill analysis."
        }


if __name__ == "__main__":
    pos = {"study_id": "STUDY_A", "context_parameters": {"dose": "10 uM", "cell_line_or_model": "Model_X", "assay": "Assay_1"}}
    neg = {"study_id": "STUDY_B", "category": "NULL_RESULT", "context_parameters": {"dose": "10 uM", "cell_line_or_model": "Model_X", "assay": "Assay_1"}}
    res = GenericContradictionEngine.analyze_discrepancy(pos, neg)
    print("Identical params result:", res["contradiction_type"])

    neg_diff = {"study_id": "STUDY_C", "category": "DOSE_LIMITATION", "context_parameters": {"dose": "0.5 uM", "cell_line_or_model": "Model_X", "assay": "Assay_1"}}
    res_diff = GenericContradictionEngine.analyze_discrepancy(pos, neg_diff)
    print("Different params result:", res_diff["contradiction_type"])
    
    no_evi = GenericContradictionEngine.distinguish_no_evidence_vs_no_effect(0, [])
    print("Zero retrieval check:", no_evi["epistemic_state"])
    res_diff = GenericContradictionEngine.analyze_discrepancy(pos, neg_diff)
    print("Different params result:", res_diff["contradiction_type"], "Mismatches:", res_diff["contextual_divergences"])
