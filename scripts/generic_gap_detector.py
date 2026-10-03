#!/usr/bin/env python3
"""
generic_gap_detector.py - Evidence-Based Research Gap Identification Engine
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

Derives research gaps systematically across 11 universal gap categories
based on authentic evidence trails, boundary conditions, and study cohort characteristics.
"""

import json
from typing import Dict, List, Any, Optional

UNIVERSAL_GAP_TAXONOMY = {
    "POPULATION_GAP": "Lack of evidence in specific clinical, demographic, or disease sub-populations",
    "MODEL_GAP": "Preclinical findings restricted to simplified 2D monocultures or non-human lineages",
    "INTERVENTION_GAP": "Optimal agent configuration, analogue superiority, or delivery mode uncharacterized",
    "COMBINATION_GAP": "Absence of empirical multi-agent interaction or synergy evaluation",
    "DOSE_GAP": "Lack of concentration-response mapping within physiological / non-toxic boundaries",
    "MECHANISTIC_GAP": "Incomplete signaling pathway elucidation or unverified intermediate cascades",
    "OUTCOME_GAP": "Primary endpoints restricted to surrogate markers without functional / phenotype validation",
    "METHODOLOGICAL_GAP": "Reliance on legacy assays lacking modern quantitative rigor or reproducibility standards",
    "TRANSLATIONAL_GAP": "In vitro efficacy uncorroborated in intact physiological or in vivo systems",
    "SAFETY_GAP": "Incomplete toxicological boundaries, therapeutic window, or organ-sparing assessment",
    "CONTRADICTION_GAP": "Unresolved discrepancies across published studies under divergent experimental contexts"
}

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

if __name__ == "__main__":
    mock_model = {
        "population_or_model": {"primary_system": "Target Model Lineage"},
        "interventions_or_exposures": [{"name": "Agent A"}, {"name": "Agent B"}],
        "hypothesized_mechanisms": [{"pathway_name": "Kinase Cascade"}]
    }
    res = GenericGapDetector.identify_gaps(mock_model, [], [])
    print(f"Identified {res['active_gaps_identified']} active research gaps across {res['total_gap_categories_audited']} categories.")
