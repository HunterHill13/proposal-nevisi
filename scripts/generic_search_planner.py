#!/usr/bin/env python3
"""
generic_search_planner.py - Multi-Facet Dual-Path Literature Search Planner
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

Generates an 8-facet query matrix and dual-path search plan (SUPPORTING vs CONTRADICTING)
dynamically from any ResearchProblemModel across biomedical fields.
"""

import json
from typing import Dict, List, Any
try:
    from research_problem_model import ResearchProblemModel, ProblemModelBuilder
except ImportError:
    from scripts.research_problem_model import ResearchProblemModel, ProblemModelBuilder

class GenericSearchPlanner:
    """Constructs dynamic, multi-database query matrices for evidence-seeking literature retrieval."""

    def __init__(self, model: ResearchProblemModel):
        self.model = model

    def build_query_matrix(self) -> Dict[str, Any]:
        """Builds all 8 systematic search facets."""
        cond_en = self.model.target_condition.name_en
        cond_mesh = self.model.target_condition.mesh_term
        system = self.model.population_or_model.primary_system
        agents = [agt.name for agt in self.model.interventions_or_exposures]
        primary_agent = agents[0] if agents else "Target Intervention"
        adjuvant_agent = agents[1] if len(agents) > 1 else None

        facets = {}

        # Layer A: Direct Evidence Queries
        if adjuvant_agent:
            facets["LAYER_A_DIRECT_EVIDENCE"] = [
                f'("{primary_agent}"[Title/Abstract] AND "{adjuvant_agent}"[Title/Abstract] AND ("{cond_en}"[Title/Abstract] OR "{cond_mesh}"[MeSH Terms]))',
                f'("{primary_agent}" AND "{adjuvant_agent}" AND "{system}")'
            ]
        else:
            facets["LAYER_A_DIRECT_EVIDENCE"] = [
                f'("{primary_agent}"[Title/Abstract] AND ("{cond_en}"[Title/Abstract] OR "{cond_mesh}"[MeSH Terms]))',
                f'("{primary_agent}" AND "{system}")'
            ]

        # Layer B: Component Evidence Queries
        facets["LAYER_B_COMPONENT_EVIDENCE"] = []
        for agt in agents:
            facets["LAYER_B_COMPONENT_EVIDENCE"].append(
                f'("{agt}"[Title/Abstract] AND ("{cond_en}"[Title/Abstract] OR "{cond_mesh}"[MeSH Terms]))'
            )
            facets["LAYER_B_COMPONENT_EVIDENCE"].append(
                f'("{agt}"[Title/Abstract] AND "{system}"[Title/Abstract])'
            )

        # Layer C: Mechanistic Evidence Queries
        facets["LAYER_C_MECHANISTIC_EVIDENCE"] = []
        for mech in self.model.hypothesized_mechanisms:
            p_name = mech.pathway_name
            targets = " OR ".join([f'"{t}"' for t in mech.target_molecules])
            facets["LAYER_C_MECHANISTIC_EVIDENCE"].append(
                f'("{primary_agent}" AND ("{p_name}" OR {targets}) AND ("signaling" OR "pathway" OR "phosphorylation" OR "cleavage" OR "modulation"))'
            )

        # Layer D: Model Evidence Queries
        facets["LAYER_D_MODEL_EVIDENCE"] = [
            f'("{system}"[Title/Abstract] AND ("{cond_en}" OR "{cond_mesh}") AND ("biology" OR "characteristics" OR "molecular profiling" OR "heterogeneity"))'
        ]

        # Layer E: Translational Evidence Queries
        facets["LAYER_E_TRANSLATIONAL_EVIDENCE"] = [
            f'("{primary_agent}" AND ("in vivo" OR "xenograft" OR "animal model" OR "clinical trial" OR "pharmacokinetics"))'
        ]

        # Layer F: Safety & Toxicity Queries
        facets["LAYER_F_SAFETY_TOXICITY"] = [
            f'("{primary_agent}" AND ("maximum tolerated dose" OR "LD50" OR "cytotoxicity" OR "safety profile" OR "therapeutic window"))'
        ]

        # Layer G: Negative & Null Evidence Queries (MANDATORY DUAL-PATH)
        facets["LAYER_G_NEGATIVE_NULL_EVIDENCE"] = [
            f'("{primary_agent}" AND ("no effect" OR "lack of efficacy" OR "failed to inhibit" OR "null response" OR "non-significant" OR "resistance"))',
            f'("{primary_agent}" AND ("toxicity" OR "adverse effect" OR "off-target" OR "tolerance" OR "subadditive"))'
        ]
        if adjuvant_agent:
            facets["LAYER_G_NEGATIVE_NULL_EVIDENCE"].append(
                f'("{primary_agent}" AND "{adjuvant_agent}" AND ("antagonism" OR "antagonistic" OR "subadditive" OR "no synergy" OR "attenuation"))'
            )

        # Layer H: Contradictory Evidence Queries
        facets["LAYER_H_CONTRADICTORY_EVIDENCE"] = [
            f'("{primary_agent}" AND ("conflicting" OR "contradictory" OR "discrepancy" OR "failed replication" OR "opposite effect"))'
        ]
        if adjuvant_agent:
            facets["LAYER_H_CONTRADICTORY_EVIDENCE"].append(
                f'("{primary_agent}" AND "{adjuvant_agent}" AND ("discordant" OR "inconsistent" OR "independent action" OR "antagonistic interaction"))'
            )

        # Layer I: Methodological Evidence Queries
        outcomes = [o.name for o in self.model.primary_outcomes]
        outcome_str = " OR ".join([f'"{o}"' for o in outcomes])
        facets["LAYER_I_METHODOLOGICAL_EVIDENCE"] = [
            f'("{system}" AND ({outcome_str}) AND ("assay validation" OR "reproducibility" OR "protocol" OR "standardization"))'
        ]

        # Backward compatibility aliases for existing suites
        facets["FACET_A_DIRECT_EVIDENCE"] = facets["LAYER_A_DIRECT_EVIDENCE"]
        facets["FACET_B_COMPONENT_EVIDENCE"] = facets["LAYER_B_COMPONENT_EVIDENCE"]
        facets["FACET_C_COMBINATION_INTERACTION"] = facets["LAYER_A_DIRECT_EVIDENCE"]
        facets["FACET_D_MECHANISTIC_EVIDENCE"] = facets["LAYER_C_MECHANISTIC_EVIDENCE"]
        facets["FACET_E_TRANSLATIONAL_EVIDENCE"] = facets["LAYER_E_TRANSLATIONAL_EVIDENCE"]
        facets["FACET_F_NEGATIVE_NULL_EVIDENCE"] = facets["LAYER_G_NEGATIVE_NULL_EVIDENCE"]
        facets["FACET_G_SAFETY_LIMITATIONS"] = facets["LAYER_F_SAFETY_TOXICITY"]
        facets["FACET_H_METHODOLOGICAL_EVIDENCE"] = facets["LAYER_I_METHODOLOGICAL_EVIDENCE"]

        # Dual-Path Grouping
        supporting_queries = (
            facets["LAYER_A_DIRECT_EVIDENCE"] +
            facets["LAYER_B_COMPONENT_EVIDENCE"] +
            facets["LAYER_C_MECHANISTIC_EVIDENCE"] +
            facets["LAYER_D_MODEL_EVIDENCE"] +
            facets["LAYER_E_TRANSLATIONAL_EVIDENCE"]
        )

        contradicting_queries = (
            facets["LAYER_F_SAFETY_TOXICITY"] +
            facets["LAYER_G_NEGATIVE_NULL_EVIDENCE"] +
            facets["LAYER_H_CONTRADICTORY_EVIDENCE"]
        )

        return {
            "model_id": self.model.model_id,
            "domain": self.model.domain,
            "framework": self.model.framework,
            "search_boundary": {
                "databases": ["PubMed", "Europe PMC", "OpenAlex", "Crossref"],
                "target_condition": cond_en,
                "primary_system": system,
                "time_window": "2020-2026 (primary) / unrestricted (foundational)"
            },
            "query_matrix_facets": facets,
            "dual_path_execution": {
                "supporting_search_count": len(supporting_queries),
                "supporting_queries": supporting_queries,
                "contradicting_search_count": len(contradicting_queries),
                "contradicting_queries": contradicting_queries
            },
            "epistemic_policy": {
                "absence_of_contradiction_rule": "NO_RELEVANT_CONTRADICTING_EVIDENCE_IDENTIFIED",
                "prohibit_unbounded_claims": True
            }
        }

    @staticmethod
    def assess_search_saturation(iteration_yields: List[int], threshold: float = 0.05) -> Dict[str, Any]:
        """Assesses whether evidence saturation has been achieved across iterative query cycles."""
        if not iteration_yields:
            return {"saturation_reached": False, "novel_evidence_rate": 1.0, "recommendation": "Initiate baseline search"}

        if len(iteration_yields) < 2:
            return {"saturation_reached": False, "novel_evidence_rate": 1.0, "recommendation": "Execute additional query facets"}

        latest_yield = iteration_yields[-1]
        cumulative = sum(iteration_yields[:-1])
        novel_rate = (latest_yield / cumulative) if cumulative > 0 else 1.0

        is_saturated = novel_rate <= threshold
        return {
            "saturation_reached": is_saturated,
            "novel_evidence_rate": round(novel_rate, 4),
            "threshold": threshold,
            "recommendation": "Evidence saturation satisfied; proceed to extraction" if is_saturated else "Continue iterative expansion"
        }

    @staticmethod
    def generate_citation_chaining_plan(seed_pmids: List[str]) -> Dict[str, Any]:
        """Generates backward and forward citation chaining tasks to mitigate search bias."""
        return {
            "backward_citation_chaining": {
                "description": "Examine cited reference lists of high-impact seed studies",
                "seeds_to_expand": seed_pmids[:5],
                "expected_target": "Foundational methodology and historical lineage"
            },
            "forward_citation_chaining": {
                "description": "Retrieve recent papers citing landmark seed studies",
                "seeds_to_expand": seed_pmids[:5],
                "expected_target": "Modern replications, extensions, and recent contradictory trials"
            },
            "related_articles_expansion": {
                "description": "Query PubMed/EuropePMC related articles API for latent conceptual clusters",
                "seeds_to_expand": seed_pmids[:3]
            }
        }


if __name__ == "__main__":
    from research_problem_model import ProblemModelBuilder
    demo_spec = {
        "model_id": "RPM_CARDIO_SGLT2",
        "research_title_fa": "بررسی اثرات امپاگلیفلوزین بر نارسایی قلبی",
        "research_title_en": "Evaluation of Empagliflozin on Cardiac Remodeling in Heart Failure with Preserved Ejection Fraction",
        "domain": "cardiovascular",
        "framework": "PICO",
        "target_condition": {
            "name_en": "Heart Failure with Preserved Ejection Fraction",
            "name_fa": "نارسایی قلبی با کسر تخلیه‌ای حفظ‌شده",
            "mesh_term": "Heart Failure",
            "synonyms": ["HFpEF", "diastolic heart failure"]
        },
        "population_or_model": {
            "model_type": "HUMAN_CLINICAL",
            "primary_system": "Adult Patients with HFpEF",
            "secondary_systems": [],
            "normal_control_system": "Age-matched healthy controls"
        },
        "interventions_or_exposures": [
            {
                "name": "Empagliflozin",
                "chemical_or_biological_class": "SGLT2 Inhibitor",
                "role": "PRIMARY_AGENT",
                "mesh_terms": ["Sodium-Glucose Transporter 2 Inhibitors"],
                "synonyms": ["Jardiance"]
            }
        ],
        "comparators": [
            {"name": "Matching Placebo", "type": "PLACEBO"}
        ],
        "primary_outcomes": [
            {"name": "Cardiovascular Mortality or HF Hospitalization", "type": "HAZARD_RATIO", "measurement_unit": "Hazard Ratio"}
        ],
        "hypothesized_mechanisms": [
            {"pathway_name": "Myocardial Energetics and Fibrosis", "target_molecules": ["NHE1", "BNP", "TGF-beta"], "expected_modulation": "INHIBITION"}
        ],
        "controlled_vocabulary": {
            "primary_mesh": ["Heart Failure", "Sodium-Glucose Transporter 2 Inhibitors"],
            "all_synonyms": ["HFpEF", "cardiac remodeling", "gliflozins"],
            "exclusion_terms": ["type 1 diabetes only", "end-stage renal disease"]
        }
    }
    model = ProblemModelBuilder.create_from_specification(demo_spec)
    planner = GenericSearchPlanner(model)
    matrix = planner.build_query_matrix()
    print("Generated Query Matrix for Domain:", matrix["domain"])
    print("Supporting Queries:", matrix["dual_path_execution"]["supporting_search_count"])
    print("Contradicting Queries:", matrix["dual_path_execution"]["contradicting_search_count"])
