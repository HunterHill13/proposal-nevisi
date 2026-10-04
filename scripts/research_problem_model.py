#!/usr/bin/env python3
"""
research_problem_model.py - Dynamic Topic Decomposition & Framework Selection
Proposal-Nevisi Engine v8.2 (Universal Biomedical Architecture)

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
    "nephrology",
    "hematology",
    "rheumatology",
    "dermatology",
    "urology",
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
    measurement_method: Optional[str] = None
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
    specific_objectives: List[str] = field(default_factory=list)
    hypotheses: List[str] = field(default_factory=list)
    endpoints: List[str] = field(default_factory=list)

    def decompose_research_question(self) -> Dict[str, Any]:
        """Deep decomposition: Question -> Concepts -> Entities -> Relationships -> Evidence Questions -> Search Families (Phase 3)."""
        concepts = [self.target_condition.name_en] + [agt.name for agt in self.interventions_or_exposures]
        entities = {
            "target_condition": self.target_condition.name_en,
            "population_model": self.population_or_model.primary_system,
            "agents": [agt.name for agt in self.interventions_or_exposures],
            "comparators": [c.name for c in self.comparators],
            "outcomes": [o.name for o in self.primary_outcomes]
        }
        relationships = []
        for agt in self.interventions_or_exposures:
            for out in self.primary_outcomes:
                relationships.append({
                    "subject": agt.name,
                    "predicate": "modulates_or_affects",
                    "object": out.name,
                    "context": self.population_or_model.primary_system
                })
        
        evidence_questions = self.generate_dynamic_evidence_questions()
        search_families = [
            "PRIMARY_EFFICACY", "SAFETY_AND_TOXICITY", "MECHANISTIC_PATHWAY",
            "MODEL_CHARACTERIZATION", "CONFOUNDERS_AND_BIAS", "ADVERSARIAL_AND_REPLICATION"
        ]

        return {
            "research_question_en": f"What is the effect of {', '.join([a.name for a in self.interventions_or_exposures])} on {', '.join([o.name for o in self.primary_outcomes])} in {self.population_or_model.primary_system}?",
            "concepts": concepts,
            "entities": entities,
            "relationships": relationships,
            "evidence_questions": evidence_questions,
            "search_families": search_families
        }

    def generate_dynamic_evidence_questions(self) -> List[Dict[str, Any]]:
        """Dynamically determines evidence questions based on study framework (Phase 4)."""
        ev_questions = []
        agents = [a.name for a in self.interventions_or_exposures]
        agt_str = ", ".join(agents) if agents else "the intervention"
        system = self.population_or_model.primary_system
        cond = self.target_condition.name_en

        if self.framework in ["PICO", "CLINICAL_TRIAL"]:
            ev_questions.append({"category": "EFFICACY", "question": f"Does {agt_str} significantly improve patient-important outcomes in patients with {cond} compared to control?"})
            ev_questions.append({"category": "SAFETY", "question": f"What are the serious adverse events, incidence of toxicities, and discontinuation rates associated with {agt_str}?"})
            ev_questions.append({"category": "DOSE_AND_DURATION", "question": f"What is the optimal therapeutic dosage, administration schedule, and treatment duration for {agt_str}?"})
            ev_questions.append({"category": "COMPARATIVE_EFFECTIVENESS", "question": f"How does the clinical efficacy of {agt_str} compare against current standard-of-care comparators?"})
        elif self.framework == "DIAGNOSTIC":
            ev_questions.append({"category": "ACCURACY", "question": f"What are the pooled sensitivity, specificity, and diagnostic likelihood ratios of {agt_str} for detecting {cond}?"})
            ev_questions.append({"category": "ROC_AUC", "question": f"What is the area under the ROC curve (AUC) and diagnostic discriminatory ability against the reference standard?"})
            ev_questions.append({"category": "THRESHOLD", "question": f"What is the pre-specified optimal diagnostic cutoff threshold and inter-assay reproducibility?"})
        elif self.framework in ["PECO", "OBSERVATIONAL"]:
            ev_questions.append({"category": "ASSOCIATION", "question": f"Is exposure to {agt_str} independently associated with altered risk or incidence of {cond}?"})
            ev_questions.append({"category": "CONFOUNDING", "question": f"Do observed effect estimates persist after multivariable adjustment for demographic and clinical confounders?"})
            ev_questions.append({"category": "DOSE_RESPONSE", "question": f"Is there an observable biological gradient or duration-dependent exposure response?"})
        elif self.framework == "PROGNOSTIC":
            ev_questions.append({"category": "PROGNOSTIC_VALUE", "question": f"Does {agt_str} provide independent risk stratification and time-to-event prognostic discrimination in {cond}?"})
            ev_questions.append({"category": "CALIBRATION_DISCRIMINATION", "question": f"What is the C-index and calibration slope of prognostic models incorporating {agt_str}?"})
        else: # EXPERIMENTAL_IN_VITRO, EXPERIMENTAL_ANIMAL, MECHANISTIC
            ev_questions.append({"category": "CONCENTRATION_RESPONSE", "question": f"What is the concentration-dependent inhibitory or modulation curve (IC50/EC50) of {agt_str} in {system}?"})
            ev_questions.append({"category": "SIGNALING_CASCADE", "question": f"Which specific downstream kinases, transcription factors, or cleavages are modulated by {agt_str}?"})
            ev_questions.append({"category": "SAFETY_MARGIN", "question": f"Does {agt_str} preserve viability in non-transformed/normal control models at biologically effective doses?"})
            if len(self.interventions_or_exposures) > 1:
                ev_questions.append({"category": "COMBINATION_INTERACTION", "question": f"Does concurrent administration of {agt_str} yield formal synergistic, additive, or antagonistic interaction?"})

        return ev_questions

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["decomposition"] = self.decompose_research_question()
        return d

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
        """Constructs an instantiated ResearchProblemModel from an input dictionary.
        Supports completely dynamic domains without hardcoded restriction.
        """
        # Dynamic domain extraction
        raw_domain = spec.get("domain", "basic_biomedical")
        if isinstance(raw_domain, str):
            domain = raw_domain.strip().lower()
        else:
            domain = str(raw_domain)
        if not domain:
            domain = "basic_biomedical"

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
            }),
            specific_objectives=spec.get("specific_objectives", []),
            hypotheses=spec.get("hypotheses", []),
            endpoints=spec.get("endpoints", [o.name for o in outcomes])
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
            {"pathway_name": "Target Signaling Pathway", "target_molecules": ["TargetProteinAlpha", "TargetKinaseBeta"], "expected_modulation": "INHIBITION"}
        ],
        "controlled_vocabulary": {
            "primary_mesh": ["Cell Survival", "Apoptosis"],
            "all_synonyms": ["programmed cell death", "cytotoxicity"],
            "exclusion_terms": ["retracted", "case report"]
        }
    }
    model = ProblemModelBuilder.create_from_specification(demo_spec)
    print("Successfully built ResearchProblemModel:", model.model_id, "Framework:", model.framework)
