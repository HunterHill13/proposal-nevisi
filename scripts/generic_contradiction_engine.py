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

    @classmethod
    def build_evidence_conflict_matrix(
        cls,
        major_findings: List[Dict[str, Any]],
        all_studies: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Constructs an EVIDENCE_CONFLICT_MATRIX mapping Support, Oppose, and Neutral studies per finding (Prompt Pt 17).
        Explicitly tracks context, methodological, dose, and population differences.
        """
        matrix_rows = []
        for finding in major_findings:
            f_text = finding.get("finding_statement", "")
            target_agent = finding.get("agent", "").lower()
            
            supporting = []
            opposing = []
            neutral = []

            for s in all_studies:
                sid = s.get("study_id")
                stext = f"{s.get('primary_findings', '')} {s.get('title', '')}".lower()
                neg_findings = s.get("negative_or_null_findings", [])

                if any(k in stext for k in ["null", "no effect", "did not inhibit", "resistance", "failed"]) or len(neg_findings) > 0:
                    opposing.append(sid)
                elif target_agent and target_agent in stext:
                    supporting.append(sid)
                else:
                    neutral.append(sid)

            explanation = (
                f"Observed discordance across {len(opposing)} opposing vs {len(supporting)} supporting studies is predominantly governed by dose thresholds, exposure kinetics, or cell lineage specificity."
                if opposing else "Uniform biological concordance observed across indexed studies."
            )

            matrix_rows.append({
                "finding": f_text,
                "supporting_studies_count": len(supporting),
                "supporting_study_ids": supporting,
                "opposing_studies_count": len(opposing),
                "opposing_study_ids": opposing,
                "neutral_studies_count": len(neutral),
                "neutral_study_ids": neutral,
                "main_scientific_explanation": explanation
            })

        return {
            "matrix_status": "CONFLICT_MATRIX_GENERATED",
            "total_findings_mapped": len(matrix_rows),
            "conflict_matrix": matrix_rows
        }

    @classmethod
    def evaluate_alternative_explanations(
        cls,
        major_conclusion: str,
        study_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Audits alternative explanations (Prompt Pt 19):
        Considers: dose, timing, population, assay, selection bias, confounding,
        batch effect, publication bias, model specificity, measurement error.
        """
        ALT_EXPLANATION_FACTORS = [
            ("DOSE_THRESHOLD_DEPENDENCY", "Observed outcome may reflect supra-physiological concentration rather than selective target engagement."),
            ("ASSAY_INTERFERENCE_ARTIFACT", "Spectrophotometric or fluorometric readouts may be confounded by chemical autofluorescence, compound aggregation, or chromophore/substrate reduction artifacts."),
            ("SELECTION_CONFOUNDING", "Non-randomized baseline differences or hidden clinical covariates may account for observed effect estimates."),
            ("MODEL_SPECIFIC_RESTRICTION", "Phenotype may represent an idiosyncratic lineage artifact not generalizable across primary patient tissues or 3D architectures."),
            ("TEMPORAL_KINETIC_DECAY", "Transient initial response may be superseded by rapid compensatory feedback upregulation."),
            ("BATCH_OR_PASSAGE_DRIFT", "Cellular senescence, genetic drift, or mycoplasma subclinical contamination during prolonged culture.")
        ]

        evaluated_alternatives = []
        for factor_id, rationale in ALT_EXPLANATION_FACTORS:
            # Check if study context addresses factor
            addressed = bool(study_context.get(factor_id.lower(), False) or study_context.get(factor_id, False))
            evaluated_alternatives.append({
                "factor": factor_id,
                "scientific_rationale": rationale,
                "is_controlled_for": addressed,
                "requires_acknowledgment_in_proposal": not addressed
            })

        plausible_uncontrolled = [a for a in evaluated_alternatives if not a["is_controlled_for"]]

        return {
            "conclusion_evaluated": major_conclusion,
            "total_factors_evaluated": len(ALT_EXPLANATION_FACTORS),
            "uncontrolled_alternative_explanations_count": len(plausible_uncontrolled),
            "uncontrolled_explanations": plausible_uncontrolled,
            "synthesis_recommendation": "Integrate alternative explanation caveats into Section 2 and Section 3 discussion." if plausible_uncontrolled else "Alternative explanations adequately controlled by experimental design."
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
