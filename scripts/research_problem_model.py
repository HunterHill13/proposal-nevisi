#!/usr/bin/env python3
"""
research_problem_model.py - Dynamic Topic Decomposition & Framework Selection
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

Transforms raw user research topics into structured, framework-aligned
Research Problem Models across oncology, cardiology, infectious diseases,
immunology, diagnostics, and basic experimental biomedicine.
"""

import json
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict

# Framework types supported by the universal engine
SUPPORTED_FRAMEWORKS = [
    "PICO",                # Interventional clinical studies
    "PECO",                # Environmental / occupational exposure studies
    "DIAGNOSTIC",          # Index test vs reference standard in target condition
    "PROGNOSTIC",          # Risk prediction / prognostic factor studies
    "MECHANISTIC",         # Signaling cascades, pathway modulation, basic biology
    "EXPERIMENTAL_IN_VITRO", # Cell culture, biochemical assays, viability, synergy
    "EXPERIMENTAL_ANIMAL"    # In vivo preclinical animal models
]

SUPPORTED_DOMAINS = [
    "oncology",
    "cardiovascular",
    "infectious_disease",
    "immunology",
    "endocrinology",
    "neurology",
    "pulmonology",
    "gastroenterology",
    "diagnostics",
    "basic_biomedical"
]

@dataclass
class TargetCondition:
    name_en: str
    name_fa: str
    mesh_term: str
    synonyms: List[str] = field(default_factory=list)

@dataclass
class PopulationOrModel:
    model_type: str  # HUMAN_CLINICAL, ANIMAL_IN_VIVO, CELL_CULTURE_IN_VITRO, EX_VIVO_TISSUE, IN_SILICO
    primary_system: str
    secondary_systems: List[str] = field(default_factory=list)
    normal_control_system: Optional[str] = None

@dataclass
class InterventionOrExposure:
    name: str
    chemical_or_biological_class: str
    role: str  # PRIMARY_AGENT, ADJUVANT_AGENT, REFERENCE_DRUG, EXPOSURE_FACTOR, INDEX_TEST
    mesh_terms: List[str] = field(default_factory=list)
    synonyms: List[str] = field(default_factory=list)

@dataclass
class Comparator:
    name: str
    type: str  # VEHICLE_CONTROL, NEGATIVE_CONTROL, POSITIVE_CONTROL, PLACEBO, STANDARD_OF_CARE, GOLD_STANDARD

@dataclass
class PrimaryOutcome:
    name: str
    type: str  # EFFICACY, VIABILITY, TOXICITY, SYNERGY, MORTALITY, SENSITIVITY, SPECIFICITY, HAZARD_RATIO
    measurement_unit: str
    preferred_assays: List[str] = field(default_factory=list)

@dataclass
class HypothesizedMechanism:
    pathway_name: str
    target_molecules: List[str]
    expected_modulation: str  # UPREGULATION, DOWNREGULATION, PHOSPHORYLATION, INHIBITION, CLEAVAGE, SECRETION

@dataclass
class ControlledVocabulary:
    primary_mesh: List[str]
    all_synonyms: List[str]
    exclusion_terms: List[str] = field(default_factory=list)

@dataclass
class ResearchProblemModel:
    model_id: str
    research_title_fa: str
    research_title_en: str
    domain: str
    framework: str
    target_condition: TargetCondition
    population_or_model: PopulationOrModel
    interventions_or_exposures: List[InterventionOrExposure]
    comparators: List[Comparator]
    primary_outcomes: List[PrimaryOutcome]
    hypothesized_mechanisms: List[HypothesizedMechanism]
    controlled_vocabulary: ControlledVocabulary
    eligibility_criteria: Dict[str, List[str]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def save_json(self, output_path: str):
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)


class ProblemModelBuilder:
    """Dynamically builds and validates a Research Problem Model from user inputs."""

    @staticmethod
    def infer_framework(domain: str, title: str, system_type: str) -> str:
        """Dynamically determines the appropriate framework without forcing PICO."""
        title_lower = title.lower()
        if "diagnostic" in title_lower or "sensitivity" in title_lower or "biomarker" in title_lower:
            return "DIAGNOSTIC"
        if "prognos" in title_lower or "survival" in title_lower or "risk score" in title_lower:
            return "PROGNOSTIC"
        if "in vitro" in title_lower or "cell line" in title_lower or system_type == "CELL_CULTURE_IN_VITRO":
            return "EXPERIMENTAL_IN_VITRO"
        if "animal" in title_lower or "mice" in title_lower or "rat" in title_lower or system_type == "ANIMAL_IN_VIVO":
            return "EXPERIMENTAL_ANIMAL"
        if "exposure" in title_lower or "environmental" in title_lower or "occupational" in title_lower:
            return "PECO"
        if "patient" in title_lower or "clinical trial" in title_lower or "randomized" in title_lower:
            return "PICO"
        return "MECHANISTIC"

    @classmethod
    def create_from_specification(cls, spec: Dict[str, Any]) -> ResearchProblemModel:
        """Constructs an instantiated ResearchProblemModel from an input dictionary."""
        # Validation of required fields
        domain = spec.get("domain", "basic_biomedical")
        if domain not in SUPPORTED_DOMAINS:
            raise ValueError(f"Domain '{domain}' not in supported domains: {SUPPORTED_DOMAINS}")

        title_en = spec.get("research_title_en", "")
        title_fa = spec.get("research_title_fa", "")
        
        pop_spec = spec.get("population_or_model", {})
        framework = spec.get("framework") or cls.infer_framework(
            domain, title_en, pop_spec.get("model_type", "CELL_CULTURE_IN_VITRO")
        )

        target_cond = TargetCondition(**spec["target_condition"])
        pop_model = PopulationOrModel(**pop_spec)

        interventions = [InterventionOrExposure(**item) for item in spec.get("interventions_or_exposures", [])]
        comparators = [Comparator(**item) for item in spec.get("comparators", [])]
        outcomes = [PrimaryOutcome(**item) for item in spec.get("primary_outcomes", [])]
        mechanisms = [HypothesizedMechanism(**item) for item in spec.get("hypothesized_mechanisms", [])]
        vocab = ControlledVocabulary(**spec.get("controlled_vocabulary", {
            "primary_mesh": [], "all_synonyms": [], "exclusion_terms": []
        }))

        return ResearchProblemModel(
            model_id=spec.get("model_id", "RPM_DEFAULT_001"),
            research_title_fa=title_fa,
            research_title_en=title_en,
            domain=domain,
            framework=framework,
            target_condition=target_cond,
            population_or_model=pop_model,
            interventions_or_exposures=interventions,
            comparators=comparators,
            primary_outcomes=outcomes,
            hypothesized_mechanisms=mechanisms,
            controlled_vocabulary=vocab,
            eligibility_criteria=spec.get("eligibility_criteria", {
                "inclusion": ["Peer-reviewed original research", "Full-text or structured abstract available"],
                "exclusion": ["Non-English/Non-Persian manuscripts without summary", "Duplicate datasets"]
            })
        )


if __name__ == "__main__":
    # Demonstration CLI execution
    demo_spec = {
        "model_id": "RPM_DEMO_GENERIC",
        "research_title_fa": "بررسی اثرات مداخله چندگانه در یک مدل عمومی",
        "research_title_en": "Evaluation of Multi-Target Intervention in a Generic Experimental Model",
        "domain": "basic_biomedical",
        "framework": "EXPERIMENTAL_IN_VITRO",
        "target_condition": {
            "name_en": "Cellular Proliferation Disorder",
            "name_fa": "اختلال تکثیر سلولی",
            "mesh_term": "Cell Proliferation",
            "synonyms": ["abnormal growth", "hyperproliferation"]
        },
        "population_or_model": {
            "model_type": "CELL_CULTURE_IN_VITRO",
            "primary_system": "Target Cell Model",
            "secondary_systems": [],
            "normal_control_system": "Non-transformed isogenic control"
        },
        "interventions_or_exposures": [
            {
                "name": "Candidate Molecule A",
                "chemical_or_biological_class": "Small molecule inhibitor",
                "role": "PRIMARY_AGENT",
                "mesh_terms": ["Enzyme Inhibitors"],
                "synonyms": ["Agent A"]
            }
        ],
        "comparators": [
            {"name": "Vehicle Control (0.1% DMSO)", "type": "VEHICLE_CONTROL"}
        ],
        "primary_outcomes": [
            {"name": "Cell Viability Inhibition", "type": "VIABILITY", "measurement_unit": "IC50 (µM)", "preferred_assays": ["Standard Viability Assay", "Spectrophotometric Assay"]}
        ],
        "hypothesized_mechanisms": [
            {"pathway_name": "Apoptotic Signaling", "target_molecules": ["Caspase-3", "Bax"], "expected_modulation": "CLEAVAGE"}
        ],
        "controlled_vocabulary": {
            "primary_mesh": ["Cell Survival", "Apoptosis"],
            "all_synonyms": ["programmed cell death", "cytotoxicity"],
            "exclusion_terms": ["retracted", "case report"]
        }
    }
    model = ProblemModelBuilder.create_from_specification(demo_spec)
    print("Successfully built ResearchProblemModel:", model.model_id, "Framework:", model.framework)
