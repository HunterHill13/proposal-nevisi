#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_cross_topic_adversarial.py - Universal Cross-Topic Adversarial Test Suite
Proposal-Nevisi Engine v8.4 (Universal Biomedical Architecture)

Fulfills Section 20 requirements by stress-testing the research engine across
10 fundamentally distinct biomedical domains:
- Scenario A: Drug + Cancer (Targeted therapy / kinase inhibitor)
- Scenario B: Antibiotic + Bacterial Infection (Antimicrobial combination)
- Scenario C: Diagnostic Biomarker + Disease (Circulating tumor DNA)
- Scenario D: Surgical Intervention + Clinical Outcome (Minimally invasive technique)
- Scenario E: Vaccine + Infectious Disease (Viral prophylaxis)
- Scenario F: Medical Device + Diagnostic Accuracy (Continuous monitoring)
- Scenario G: Gene Therapy + Inherited Disease (Viral vector gene addition)
- Scenario H: Public-Health Intervention + Epidemiological Outcome (Population prevention)
- Scenario I: Staged Interventions where Synergy is NOT Relevant (Multimodal sequencing)
- Scenario J: Topic where Literature Contains Mostly Negative Evidence (Failed repurposed drug)
"""

import os
import sys
import unittest
from typing import Dict, List, Any

TESTS_DIR = os.path.dirname(__file__)
SCRIPTS_DIR = os.path.abspath(os.path.join(TESTS_DIR, "..", "scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from core_policies import (
    MAX_FINAL_REFERENCES, NO_QUOTA_FILLING,
    GENERIC_EXCLUSION_ONTOLOGY, UNIVERSAL_ENTITY_TYPES, EVIDENCE_ROLES
)
from generic_search_planner import GenericSearchPlanner
from generic_reference_auditor import GenericReferenceAuditor
from generic_evidence_synthesis import GenericEvidenceSynthesizer


class TestCrossTopicAdversarialScenarios(unittest.TestCase):
    """Verifies that v8.4 operates truly topic-agnostically across Scenarios A through J."""

    def setUp(self):
        self.auditor = GenericReferenceAuditor()

    # ==========================================================================
    # SCENARIO A: Drug + Cancer (Targeted kinase inhibitor)
    # ==========================================================================
    def test_scenario_a_targeted_oncology(self):
        """Scenario A: Third-generation EGFR-TKI in NSCLC cell model."""
        problem = {
            "model_id": "RPM_SCENARIO_A",
            "domain": "oncology",
            "framework": "PICO",
            "study_type": "IN_VITRO_EXPERIMENTAL",
            "target_condition": {"name_en": "Non-Small Cell Lung Carcinoma", "mesh_term": "Carcinoma, Non-Small-Cell Lung"},
            "population_or_model": {"primary_system": "PC9 adenocarcinoma cells", "cell_lines": ["PC9"]},
            "interventions_or_exposures": [{"name": "Osimertinib", "chemical_or_biological_class": "Kinase Inhibitor"}],
            "primary_outcomes": [{"name": "Cell Viability", "type": "VIABILITY"}],
            "hypothesized_mechanisms": [{"pathway_name": "EGFR phosphorylation", "target_molecules": ["EGFR", "Akt"]}]
        }
        # 1. Decomposition
        decomp = GenericSearchPlanner.decompose_problem_for_search(problem)
        self.assertEqual(decomp["decomposed_question_components"]["intervention_a"], "Osimertinib")
        self.assertEqual(decomp["decomposed_question_components"]["intervention_b"], "NOT_APPLICABLE")
        self.assertIn("population_or_model", decomp["applicable_dimensions"])

        # 2. Evidence gate
        rec_direct = {
            "title": "Osimertinib suppresses PC9 cell viability via inhibition of EGFR phosphorylation",
            "abstract": "We investigated the antiproliferative effect of osimertinib in PC9 cells.",
            "year": 2023
        }
        gate = self.auditor.audit_scientific_evidence_gates(rec_direct, problem)
        self.assertEqual(gate["universal_entity_type"], "PARENT_ENTITY")
        self.assertEqual(gate["evidence_role"], "DIRECT_EVIDENCE")
        self.assertEqual(gate["evidence_polarity"], "SUPPORTS")

    # ==========================================================================
    # SCENARIO B: Antibiotic + Bacterial Infection
    # ==========================================================================
    def test_scenario_b_antimicrobial_combination(self):
        """Scenario B: Meropenem plus vaborbactam against carbapenem-resistant Klebsiella pneumoniae."""
        problem = {
            "model_id": "RPM_SCENARIO_B",
            "domain": "infectious_diseases",
            "framework": "PICO",
            "study_type": "IN_VITRO_EXPERIMENTAL",
            "target_condition": {"name_en": "Klebsiella pneumoniae Infection", "mesh_term": "Klebsiella Infections"},
            "population_or_model": {"primary_system": "K. pneumoniae clinical isolates (KPC-producing strains)"},
            "interventions_or_exposures": [
                {"name": "Meropenem", "chemical_or_biological_class": "Carbapenem Antibiotic"},
                {"name": "Vaborbactam", "chemical_or_biological_class": "Beta-Lactamase Inhibitor"}
            ],
            "primary_outcomes": [{"name": "Minimum Inhibitory Concentration", "type": "MIC"}],
            "hypothesized_mechanisms": [{"pathway_name": "KPC beta-lactamase inhibition", "target_molecules": ["KPC-2"]}]
        }
        decomp = GenericSearchPlanner.decompose_problem_for_search(problem)
        self.assertEqual(decomp["decomposed_question_components"]["intervention_b"], "Vaborbactam")
        self.assertIn("combination", decomp["applicable_dimensions"])

        rec = {
            "title": "Restoration of meropenem activity by vaborbactam against KPC-producing Klebsiella pneumoniae isolates",
            "abstract": "The combination of meropenem and vaborbactam synergistically decreased minimum inhibitory concentrations.",
            "year": 2022
        }
        gate = self.auditor.audit_scientific_evidence_gates(rec, problem)
        self.assertEqual(gate["evidence_role"], "DIRECT_EVIDENCE")
        self.assertEqual(gate["synergy_evidence"], "DIRECT")

    # ==========================================================================
    # SCENARIO C: Diagnostic Biomarker + Disease
    # ==========================================================================
    def test_scenario_c_diagnostic_biomarker(self):
        """Scenario C: Circulating tumor DNA for minimal residual disease in colorectal cancer."""
        problem = {
            "model_id": "RPM_SCENARIO_C",
            "domain": "diagnostics",
            "framework": "DIAGNOSTIC",
            "study_type": "DIAGNOSTIC_ACCURACY_STUDY",
            "target_condition": {"name_en": "Colorectal Neoplasms", "mesh_term": "Colorectal Neoplasms"},
            "population_or_model": {"primary_system": "Postoperative stage II-III colorectal cancer patients"},
            "interventions_or_exposures": [{"name": "Circulating Tumor DNA Assay", "role": "INDEX_TEST"}],
            "comparators": [{"name": "Radiological CT surveillance", "type": "REFERENCE_STANDARD"}],
            "primary_outcomes": [{"name": "Diagnostic Sensitivity and Specificity", "type": "ACCURACY"}]
        }
        decomp = GenericSearchPlanner.decompose_problem_for_search(problem)
        # In diagnostic accuracy without molecular pathways, mechanism is NOT_APPLICABLE
        self.assertEqual(decomp["decomposed_question_components"]["mechanism"], "NOT_APPLICABLE")
        self.assertEqual(decomp["decomposed_question_components"]["safety_toxicity"], "NOT_APPLICABLE")
        self.assertIn("mechanism", decomp["not_applicable_dimensions"])

        rec = {
            "title": "Postoperative circulating tumor DNA analysis predicts recurrence in stage II colorectal cancer",
            "abstract": "We evaluated the sensitivity and specificity of ctDNA for detecting minimal residual disease.",
            "year": 2023
        }
        gate = self.auditor.audit_scientific_evidence_gates(rec, problem)
        self.assertIn(gate["evidence_role"], ["DIRECT_EVIDENCE", "DIAGNOSTIC_EVIDENCE"])

    # ==========================================================================
    # SCENARIO D: Surgical Intervention + Clinical Outcome
    # ==========================================================================
    def test_scenario_d_surgical_technique(self):
        """Scenario D: Laparoscopic vs open appendectomy in acute appendicitis."""
        problem = {
            "model_id": "RPM_SCENARIO_D",
            "domain": "surgery",
            "framework": "SURGICAL",
            "study_type": "RANDOMIZED_CONTROLLED_TRIAL",
            "target_condition": {"name_en": "Acute Appendicitis", "mesh_term": "Appendicitis"},
            "population_or_model": {"primary_system": "Adult patients presenting with acute uncomplicated appendicitis"},
            "interventions_or_exposures": [{"name": "Laparoscopic Appendectomy", "role": "INDEX_PROCEDURE"}],
            "comparators": [{"name": "Open Appendectomy", "type": "CONVENTIONAL_CONTROL"}],
            "primary_outcomes": [{"name": "Wound Infection Rate", "type": "COMPLICATION"}]
        }
        decomp = GenericSearchPlanner.decompose_problem_for_search(problem)
        self.assertEqual(decomp["decomposed_question_components"]["intervention_b"], "NOT_APPLICABLE")
        self.assertIn("postoperative", decomp["decomposed_question_components"]["safety_toxicity"])

        # Adversarial off-topic check: agricultural fertilizer paper must be rejected
        irrelevant_paper = {
            "title": "Effects of nitrogen fertilizer on crop yields in rural agriculture",
            "abstract": "Evaluated grain crop yield under nitrogen supplement.",
            "year": 2023
        }
        rel = self.auditor.audit_contextual_relevance(irrelevant_paper, problem)
        self.assertFalse(rel["is_contextually_relevant"])
        self.assertEqual(rel["relevance_tier"], "IRRELEVANT")
        self.assertEqual(rel["generic_exclusion_code"], "WRONG_SETTING")

    # ==========================================================================
    # SCENARIO E: Vaccine + Infectious Disease
    # ==========================================================================
    def test_scenario_e_prophylactic_vaccine(self):
        """Scenario E: mRNA vaccine preventing respiratory syncytial virus."""
        problem = {
            "model_id": "RPM_SCENARIO_E",
            "domain": "infectious_diseases",
            "framework": "PICO",
            "study_type": "CONTROLLED_CLINICAL_STUDY",
            "target_condition": {"name_en": "Respiratory Syncytial Virus Infection", "mesh_term": "Respiratory Syncytial Virus Infections"},
            "population_or_model": {"primary_system": "Older adults aged 60 years or above"},
            "interventions_or_exposures": [{
                "name": "mRNA-1345 Vaccine",
                "chemical_or_biological_class": "Lipid Nanoparticle mRNA",
                "synonyms": ["mRNA-based respiratory syncytial virus vaccine", "mRNA-1345"]
            }],
            "primary_outcomes": [{"name": "Vaccine Efficacy Against Lower Respiratory Tract Disease", "type": "EFFICACY"}]
        }
        decomp = GenericSearchPlanner.decompose_problem_for_search(problem)
        self.assertIn("population_or_model", decomp["applicable_dimensions"])

        rec = {
            "title": "Efficacy of an mRNA-based respiratory syncytial virus vaccine in older adults",
            "abstract": "Randomized trial demonstrating 83.7% vaccine efficacy against lower respiratory tract disease.",
            "year": 2023
        }
        gate = self.auditor.audit_scientific_evidence_gates(rec, problem)
        self.assertEqual(gate["evidence_role"], "DIRECT_EVIDENCE")
        self.assertEqual(gate["evidence_polarity"], "SUPPORTS")

    # ==========================================================================
    # SCENARIO F: Medical Device + Diagnostic Accuracy
    # ==========================================================================
    def test_scenario_f_medical_device_monitoring(self):
        """Scenario F: Continuous glucose monitoring device in type 1 diabetes."""
        problem = {
            "model_id": "RPM_SCENARIO_F",
            "domain": "endocrinology",
            "framework": "DIAGNOSTIC",
            "study_type": "PROSPECTIVE_COHORT",
            "target_condition": {"name_en": "Type 1 Diabetes Mellitus", "mesh_term": "Diabetes Mellitus, Type 1"},
            "population_or_model": {"primary_system": "Adolescents with type 1 diabetes"},
            "interventions_or_exposures": [{"name": "Continuous Glucose Monitor Sensor", "chemical_or_biological_class": "Biosensor Device"}],
            "comparators": [{"name": "Self-Monitoring Blood Glucose Fingerstick", "type": "STANDARD_COMPARATOR"}],
            "primary_outcomes": [{"name": "Mean Absolute Relative Difference", "type": "ACCURACY"}]
        }
        decomp = GenericSearchPlanner.decompose_problem_for_search(problem)
        self.assertEqual(decomp["decomposed_question_components"]["mechanism"], "NOT_APPLICABLE")

        # Disconnected animal livestock paper rejected
        semen_paper = {
            "title": "Cryopreserved bull semen viability assessment using flow cytometry",
            "abstract": "Post-thaw sperm motility in livestock breeding.",
            "year": 2023
        }
        rel = self.auditor.audit_contextual_relevance(semen_paper, problem)
        self.assertFalse(rel["is_contextually_relevant"])
        self.assertEqual(rel["generic_exclusion_code"], "WRONG_POPULATION")

    # ==========================================================================
    # SCENARIO G: Gene Therapy + Inherited Disease
    # ==========================================================================
    def test_scenario_g_recombinant_gene_therapy(self):
        """Scenario G: AAV-mediated Factor IX gene addition in Hemophilia B."""
        problem = {
            "model_id": "RPM_SCENARIO_G",
            "domain": "hematology",
            "framework": "PICO",
            "study_type": "CONTROLLED_CLINICAL_STUDY",
            "target_condition": {"name_en": "Hemophilia B", "mesh_term": "Hemophilia B"},
            "population_or_model": {"primary_system": "Adult severe hemophilia B patients"},
            "interventions_or_exposures": [{"name": "Etranacogene Dezaparvovec", "chemical_or_biological_class": "AAV5 Vector Gene Therapy"}],
            "primary_outcomes": [{"name": "Endogenous Factor IX Activity", "type": "ACTIVITY"}],
            "hypothesized_mechanisms": [{"pathway_name": "Hepatic Factor IX expression", "target_molecules": ["FIX"]}]
        }
        rec = {
            "title": "Etranacogene dezaparvovec gene therapy in adults with severe or moderate-severe hemophilia B",
            "abstract": "Sustained elevation of factor IX activity following single intravenous administration of recombinant AAV5 vector.",
            "year": 2023
        }
        gate = self.auditor.audit_scientific_evidence_gates(rec, problem)
        self.assertEqual(gate["evidence_role"], "DIRECT_EVIDENCE")

    # ==========================================================================
    # SCENARIO H: Public-Health Intervention + Epidemiological Outcome
    # ==========================================================================
    def test_scenario_h_public_health_epidemiology(self):
        """Scenario H: Community-wide dietary salt reduction on stroke incidence."""
        problem = {
            "model_id": "RPM_SCENARIO_H",
            "domain": "epidemiology",
            "framework": "PECO",
            "study_type": "PROSPECTIVE_COHORT",
            "target_condition": {"name_en": "Stroke", "mesh_term": "Stroke"},
            "population_or_model": {"primary_system": "Community-dwelling adult cohort (n=20,000)"},
            "interventions_or_exposures": [{"name": "Potassium-Enriched Salt Substitution", "role": "PUBLIC_HEALTH_INTERVENTION"}],
            "comparators": [{"name": "Standard Table Salt", "type": "USUAL_EXPOSURE"}],
            "primary_outcomes": [{"name": "Incident Fatal and Non-Fatal Stroke", "type": "EPIDEMIOLOGICAL_INCIDENCE"}]
        }
        decomp = GenericSearchPlanner.decompose_problem_for_search(problem)
        self.assertEqual(decomp["decomposed_question_components"]["mechanism"], "NOT_APPLICABLE")
        self.assertEqual(decomp["decomposed_question_components"]["safety_toxicity"], "NOT_APPLICABLE")

        rec = {
            "title": "Effect of salt substitution on cardiovascular events and death in rural communities",
            "abstract": "Large-scale trial demonstrated significant reduction in stroke incidence with potassium-enriched salt.",
            "year": 2021
        }
        gate = self.auditor.audit_scientific_evidence_gates(rec, problem)
        self.assertIn(gate["evidence_role"], ["DIRECT_EVIDENCE", "EPIDEMIOLOGICAL_EVIDENCE"])
        self.assertEqual(gate["evidence_polarity"], "SUPPORTS")

    # ==========================================================================
    # SCENARIO I: Staged Interventions where Synergy is NOT Relevant
    # ==========================================================================
    def test_scenario_i_non_synergistic_multimodal_care(self):
        """Scenario I: Surgical resection followed by adjuvant physical therapy (synergy concept not applicable)."""
        problem = {
            "model_id": "RPM_SCENARIO_I",
            "domain": "orthopedics",
            "framework": "PICO",
            "study_type": "RANDOMIZED_CONTROLLED_TRIAL",
            "target_condition": {"name_en": "Rotator Cuff Tears", "mesh_term": "Rotator Cuff Injuries"},
            "population_or_model": {"primary_system": "Postoperative patients following arthroscopic repair"},
            "interventions_or_exposures": [
                {"name": "Early Supervised Physical Therapy", "role": "ACTIVE_INTERVENTION"},
                {"name": "Delayed Immobilization", "role": "COMPARATOR_ARM"}
            ],
            "primary_outcomes": [{"name": "Constant-Murley Shoulder Score at 12 Months", "type": "FUNCTIONAL_OUTCOME"}]
        }
        rec = {
            "title": "Early versus delayed physical therapy following arthroscopic rotator cuff repair",
            "abstract": "Evaluated range of motion and functional scores between early rehabilitation and delayed immobilization.",
            "year": 2022
        }
        gate = self.auditor.audit_scientific_evidence_gates(rec, problem)
        # Chou-Talalay / Synergy formula should be NOT_APPLICABLE
        self.assertIn(gate["synergy_evidence"], ["MONOTHERAPY_ONLY", "NOT_APPLICABLE"])

    # ==========================================================================
    # SCENARIO J: Topic where Literature Contains Mostly Negative Evidence
    # ==========================================================================
    def test_scenario_j_mostly_negative_evidence(self):
        """Scenario J: Failed repurposed agent (Hydroxychloroquine in severe viral infection)."""
        problem = {
            "model_id": "RPM_SCENARIO_J",
            "domain": "infectious_diseases",
            "framework": "PICO",
            "study_type": "RANDOMIZED_CONTROLLED_TRIAL",
            "target_condition": {"name_en": "Severe Viral Respiratory Distress", "mesh_term": "Respiratory Distress Syndrome"},
            "population_or_model": {"primary_system": "Hospitalized adult patients with severe hypoxemia"},
            "interventions_or_exposures": [{"name": "Repurposed Compound Z", "role": "PRIMARY_AGENT"}],
            "comparators": [{"name": "Standard Supportive Care", "type": "CONTROL"}],
            "primary_outcomes": [{"name": "28-Day Mortality", "type": "MORTALITY"}]
        }
        # Negative trial
        rec_neg = {
            "title": "Repurposed Compound Z in hospitalized patients: randomized controlled trial demonstrates no clinical benefit",
            "abstract": "Treatment did not reduce 28-day mortality or mechanical ventilation need (p = 0.42). Null result confirmed.",
            "year": 2021
        }
        gate = self.auditor.audit_scientific_evidence_gates(rec_neg, problem)
        self.assertEqual(gate["evidence_polarity"], "CONTRADICTS")

        # Literature synthesis must honestly reflect the negative evidence without pretending efficacy exists
        narrative = GenericEvidenceSynthesizer.generate_7_point_synthesis_narrative(
            problem, [rec_neg]
        )
        self.assertIn("point_3_contradictory", narrative)
        self.assertEqual(narrative["point_6_what_is_missing"]["epistemic_gap_status"], "NO_DIRECT_STUDY_IDENTIFIED_IN_SEARCHED_SOURCES")

    # ==========================================================================
    # PORTFOLIO CEILING & SATURATION VERIFICATION
    # ==========================================================================
    def test_portfolio_ceiling_and_no_quota_filling_across_domains(self):
        """Verifies MAX_FINAL_REFERENCES == 25 and NO_QUOTA_FILLING == True invariant."""
        self.assertEqual(MAX_FINAL_REFERENCES, 25)
        self.assertTrue(NO_QUOTA_FILLING)
        self.assertGreaterEqual(len(GENERIC_EXCLUSION_ONTOLOGY), 16)
        self.assertGreaterEqual(len(UNIVERSAL_ENTITY_TYPES), 10)
        self.assertGreaterEqual(len(EVIDENCE_ROLES), 10)


if __name__ == "__main__":
    unittest.main()
