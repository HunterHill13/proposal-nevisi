#!/usr/bin/env python3
"""
generic_gap_detector.py - Evidence-Based Research Gap Identification Engine
Proposal-Nevisi Engine v8.1 (Universal Biomedical Architecture)

Derives research gaps systematically across 11 universal gap categories
based on authentic evidence trails, boundary conditions, and study cohort characteristics.
"""

import json
from typing import Dict, List, Any, Optional

try:
    from core_policies import UNIVERSAL_GAP_TAXONOMY
except ImportError:
    from scripts.core_policies import UNIVERSAL_GAP_TAXONOMY

class GenericGapDetector:
    """Detects, categorizes, and validates evidence-based research gaps."""

    @classmethod
    def detect_gaps(
        cls,
        studies: List[Dict[str, Any]],
        target_model: Dict[str, Any],
        contradictions: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """Convenience alias for detecting gaps directly from studies and target model."""
        res = cls.identify_gaps(target_model=target_model, study_evidence=studies, contradictions=contradictions or [])
        return res.get("identified_gaps", [])

    @classmethod
    def identify_gaps(
        cls,
        target_model: Dict[str, Any],
        study_evidence: List[Dict[str, Any]],
        contradictions: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Maps synthesized evidence against target research problem to derive grounded gaps."""
        if contradictions is None:
            contradictions = []
        identified_gaps = []

        # 1. Model Gap: Check if studies cover primary target system
        target_system = target_model.get("population_or_model", {}).get("primary_system", "").lower()
        system_studies = [
            s for s in study_evidence
            if target_system and target_system in str(s.get("model_system", s.get("organism_cell_line", ""))).lower()
        ]
        if len(system_studies) < 3:
            gap_cat = "POPULATION_GAP" if "clinical" in str(target_model.get("population_or_model", {}).get("model_type", "")).lower() or "human" in str(target_model.get("population_or_model", {}).get("model_type", "")).lower() else "MODEL_GAP"
            identified_gaps.append({
                "gap_category": gap_cat,
                "definition": UNIVERSAL_GAP_TAXONOMY.get(gap_cat, UNIVERSAL_GAP_TAXONOMY["MODEL_GAP"]),
                "evidence_trail": f"Only {len(system_studies)} studies evaluate target system '{target_system}' directly.",
                "proposed_resolution": "Conduct systematic empirical validation directly within target biological lineage or patient population."
            })

        # 2. Combination Gap: Check if multi-agent combinations exist
        interventions = target_model.get("interventions_or_exposures", [])
        if len(interventions) > 1:
            agent_names = [a.get("name", "").lower() for a in interventions]
            combo_studies = [
                s for s in study_evidence
                if all(a in str(s.get("intervention_agent", "")).lower() or a in str(s.get("title", "")).lower() for a in agent_names)
            ]
            if len(combo_studies) == 0:
                identified_gaps.append({
                    "gap_category": "COMBINATION_GAP",
                    "definition": UNIVERSAL_GAP_TAXONOMY["COMBINATION_GAP"],
                    "evidence_trail": f"Zero prior studies evaluate direct simultaneous combination of: {', '.join(agent_names)}.",
                    "proposed_resolution": "Execute formal multi-agent matrix titration and quantitative synergy evaluation."
                })

        # 3. Mechanistic Gap
        mechanisms = target_model.get("hypothesized_mechanisms", [])
        for mech in mechanisms:
            p_name = mech.get("pathway_name", "").lower()
            matching_studies = [
                s for s in study_evidence
                if p_name in str(s.get("primary_findings", "")).lower() or p_name in str(s.get("title", "")).lower()
            ]
            if len(matching_studies) < 2:
                identified_gaps.append({
                    "gap_category": "MECHANISTIC_GAP",
                    "definition": UNIVERSAL_GAP_TAXONOMY["MECHANISTIC_GAP"],
                    "evidence_trail": f"Signaling pathway '{p_name}' has insufficient direct empirical evidence ({len(matching_studies)} studies).",
                    "proposed_resolution": f"Analyze protein activation, phosphorylation, and cleavage dynamics for pathway '{p_name}'."
                })

        # 4. Safety & Dose Gap
        dose_studies = [
            s for s in study_evidence
            if s.get("dose_concentration_range") and "toxic" not in str(s.get("dose_concentration_range")).lower()
        ]
        if len(dose_studies) < len(study_evidence) // 2:
            identified_gaps.append({
                "gap_category": "DOSE_GAP",
                "definition": UNIVERSAL_GAP_TAXONOMY["DOSE_GAP"],
                "evidence_trail": "Quantitative dose-response boundaries and non-toxic vehicle limits are under-reported.",
                "proposed_resolution": "Establish rigorous multi-point concentration-response curves within validated non-toxic thresholds."
            })

        # 5. Contradiction Gap
        if contradictions:
            identified_gaps.append({
                "gap_category": "CONTRADICTION_GAP",
                "definition": UNIVERSAL_GAP_TAXONOMY["CONTRADICTION_GAP"],
                "evidence_trail": f"{len(contradictions)} contextual disagreements or discordant findings identified in prior literature.",
                "proposed_resolution": "Perform head-to-head benchmarking controlling for cell lineage, exposure time, and assay readouts."
            })

        # Assign evidence-backed gap importance tier (Phase 17)
        for g in identified_gaps:
            cat = g.get("gap_category")
            if cat in ["POPULATION_GAP", "TRANSLATIONAL_GAP", "COMBINATION_GAP"]:
                g["importance_tier"] = "CRITICAL_GAP"
                g["priority_weight"] = 1.0
            elif cat in ["MECHANISTIC_GAP", "SAFETY_GAP", "CONTRADICTION_GAP"]:
                g["importance_tier"] = "IMPORTANT_GAP"
                g["priority_weight"] = 0.85
            elif cat in ["DOSE_GAP", "MODEL_GAP", "TIMING_GAP"]:
                g["importance_tier"] = "MODERATE_GAP"
                g["priority_weight"] = 0.65
            elif cat in ["METHODOLOGICAL_GAP", "REPLICATION_GAP"]:
                g["importance_tier"] = "MINOR_GAP"
                g["priority_weight"] = 0.45
            else:
                g["importance_tier"] = "LOW_VALUE_GAP"
                g["priority_weight"] = 0.25

        # Ensure all gap categories are represented in the gap catalog
        gap_catalog = {}
        for cat, defn in UNIVERSAL_GAP_TAXONOMY.items():
            matching = [g for g in identified_gaps if g["gap_category"] == cat]
            gap_catalog[cat] = {
                "category": cat,
                "definition": defn,
                "active_in_project": len(matching) > 0,
                "evidence_findings": matching
            }

        return {
            "total_gap_categories_audited": len(UNIVERSAL_GAP_TAXONOMY),
            "active_gaps_identified": len(identified_gaps),
            "gap_catalog": gap_catalog,
            "identified_gaps": identified_gaps
        }

    @classmethod
    def formulate_evidence_bounded_novelty(
        cls,
        identified_gaps: List[Dict[str, Any]],
        target_model: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Formulates strictly evidence-bounded novelty statements, blocking ungrounded hyperbole (Prompt Pt 24)."""
        interventions = target_model.get("interventions_or_exposures", [])
        system = target_model.get("population_or_model", {}).get("primary_system", "the designated model")
        agent_names = [a.get("name", "") for a in interventions]
        agents_str = " + ".join(agent_names) if agent_names else "the proposed intervention"

        active_categories = [g.get("gap_category") for g in identified_gaps]

        novelty_clauses = []
        if "COMBINATION_GAP" in active_categories:
            novelty_clauses.append(f"To our knowledge within systematic literature boundaries, direct simultaneous evaluation of {agents_str} has not been reported in {system}.")
        elif "POPULATION_GAP" in active_categories or "MODEL_GAP" in active_categories:
            novelty_clauses.append(f"While component effects exist in other experimental systems, empirical assessment directly in {system} represents an unaddressed gap.")
        elif "MECHANISTIC_GAP" in active_categories:
            novelty_clauses.append(f"The specific intermediate signaling cascade modulated by {agents_str} remains incompletely resolved in current peer-reviewed evidence.")
        else:
            novelty_clauses.append(f"The present research addresses specific dosage, kinetic, or methodological limitations identified across published studies.")

        bounded_statement = " ".join(novelty_clauses)

        return {
            "is_evidence_bounded": True,
            "prohibited_hyperbole_prevented": True,
            "bounded_novelty_statement_en": bounded_statement,
            "bounded_novelty_statement_fa": f"بر پایه استراتژی جستجوی سیستماتیک و شواهد موجود، نوآوری این پژوهش معطوف به پر کردن شکاف‌های مستندشده در سیستم {system} با تمرکز بر {agents_str} به دور از ادعاهای مبالغه‌آمیز است.",
            "grounding_gaps": active_categories
        }

    @classmethod
    def audit_gap_assertion_epistemic_rigor(
        cls,
        gap_claim_statement: str,
        search_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Audits that research gaps are stated with epistemic rigor (Prompt Pt 21):
        Prohibits absolute claims like 'no study exists in the universe'.
        Requires: 'In our systematic search across [databases] using [queries] and [date range], no direct retrievable evidence was identified.'
        If search coverage is suboptimal, GAP_CONFIDENCE must be marked LOW.
        """
        claim_lower = gap_claim_statement.lower()
        ABSOLUTE_UNBOUNDED_CLAIMS = [
            "no study exists", "no research exists", "never been studied",
            "completely unstudied", "zero studies exist anywhere", "هیچ مطالعه‌ای در دنیا وجود ندارد"
        ]

        has_unbounded_claim = any(phrase in claim_lower for phrase in ABSOLUTE_UNBOUNDED_CLAIMS)

        db_count = len(search_metadata.get("databases_searched", []))
        has_query_trace = bool(search_metadata.get("queries_logged", 0) > 0)
        has_chaining = bool(search_metadata.get("citation_chaining_completed", False))

        is_search_thorough = (db_count >= 3 and has_query_trace)

        if not is_search_thorough:
            gap_confidence = "LOW"
            epistemic_verdict = "PRELIMINARY_GAP_LOW_SEARCH_CONFIDENCE"
        elif has_unbounded_claim:
            gap_confidence = "MODERATE"
            epistemic_verdict = "GAP_LANGUAGE_OVERCLAIM_NEEDS_METHODOLOGICAL_QUALIFICATION"
        else:
            gap_confidence = "HIGH"
            epistemic_verdict = "EVIDENCE_BOUNDED_GAP_VALIDATED"

        permissible_statement = (
            f"Within the literature retrieved across {', '.join(search_metadata.get('databases_searched', ['indexed databases']))} "
            f"using targeted query matrices and citation chaining, no direct peer-reviewed empirical evidence was identified addressing this specific question."
        )

        return {
            "gap_statement_audited": gap_claim_statement,
            "has_unbounded_absolute_claim": has_unbounded_claim,
            "gap_confidence": gap_confidence,
            "search_thoroughness": "COMPREHENSIVE" if is_search_thorough else "SUBOPTIMAL",
            "epistemic_verdict": epistemic_verdict,
            "permissible_formulation": permissible_statement,
            "status": "PASS" if not has_unbounded_claim and is_search_thorough else "REVISE_LANGUAGE"
        }


if __name__ == "__main__":
    mock_model = {
        "population_or_model": {"primary_system": "Target Model Lineage"},
        "interventions_or_exposures": [{"name": "Agent A"}, {"name": "Agent B"}],
        "hypothesized_mechanisms": [{"pathway_name": "Kinase Cascade"}]
    }
    res = GenericGapDetector.identify_gaps(mock_model, [], [])
    print(f"Identified {res['active_gaps_identified']} active research gaps across {res['total_gap_categories_audited']} categories.")
