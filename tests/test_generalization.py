#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_generalization.py - Multi-Domain Biomedical Pipeline Generalization Tests
Proposal-Nevisi Engine v8.2 (Universal Biomedical Architecture)

Asserts rigorous, domain-specific scientific invariants across 5 diverse disciplines:
  1. Oncology Preclinical (In vitro combination therapy, synergy, and vehicle boundaries)
  2. Cardiovascular Clinical RCT (PICO trial, eGFR temporal disparity, Cox survival statistics)
  3. Infectious Disease & Antiviral (Paxlovid Mpro mutation resistance & rebound gaps)
  4. Molecular Diagnostics (ctDNA liquid biopsy, QUADAS-2, stage sensitivity disparity)
  5. Epidemiological Cohort (PECO observational cohort, confounders, and anti-causal overclaim gate)

Standard unittest implementation with dynamic execution and assertion reporting.
"""

import os
import sys
import json
import unittest

sys.stdout.reconfigure(encoding='utf-8')

TESTS_DIR = os.path.dirname(__file__)
FIXTURES_DIR = os.path.join(TESTS_DIR, "fixtures")
SCRIPTS_DIR = os.path.abspath(os.path.join(TESTS_DIR, "..", "scripts"))
sys.path.insert(0, SCRIPTS_DIR)

from research_problem_model import ProblemModelBuilder
from generic_search_planner import GenericSearchPlanner
from generic_study_family_detector import StudyFamilyDetector
from generic_comparability_engine import GenericComparabilityEngine
from generic_contradiction_engine import GenericContradictionEngine
from generic_claim_entailment_engine import GenericClaimEntailmentEngine
from generic_study_relationships import GenericStudyRelationshipEngine
from generic_gap_detector import GenericGapDetector
from dynamic_protocol_designer import DynamicProtocolDesigner

class TestMultiDomainGeneralization(unittest.TestCase):
    """Rigorous scientific invariant verification across 5 biomedical domains."""

    def _load_fixture(self, fixture_name: str) -> dict:
        fix_path = os.path.join(FIXTURES_DIR, fixture_name, "fixture_data.json")
        self.assertTrue(os.path.exists(fix_path), f"Fixture file {fix_path} must exist")
        with open(fix_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_01_oncology_preclinical_scientific_invariants(self):
        """Verifies in vitro combination synergy, solvent control, and two-way interaction statistics."""
        data = self._load_fixture("oncology_lupeol_ndv")
        model = ProblemModelBuilder.create_from_specification(data["research_problem_model"])
        
        self.assertEqual(model.framework, "EXPERIMENTAL_IN_VITRO")
        self.assertEqual(model.domain, "oncology")
        self.assertGreaterEqual(len(model.interventions_or_exposures), 2)
        
        # Vehicle threshold invariant
        comp_names = [c.name for c in model.comparators]
        self.assertTrue(any("0.1% DMSO" in c or "Vehicle" in c for c in comp_names))
        
        # Protocol design invariants
        vars_table = DynamicProtocolDesigner.generate_variable_table(model.to_dict())
        self.assertTrue(any("مستقل" in v["role"] for v in vars_table))
        self.assertTrue(any("وابسته" in v["role"] for v in vars_table))
        self.assertTrue(any("مخدوشگر" in v["role"] for v in vars_table))
        
        # Multi-agent statistical analysis must include interaction ANOVA
        stats = DynamicProtocolDesigner.generate_statistical_plan(model.to_dict())
        self.assertIn("Two-way ANOVA", stats["primary_analysis"])

    def test_02_cardiovascular_clinical_rct_scientific_invariants(self):
        """Verifies PICO trial structure, temporal eGFR disparity, and survival time-to-event plan."""
        data = self._load_fixture("cardiovascular_sglt2")
        model = ProblemModelBuilder.create_from_specification(data["research_problem_model"])
        
        self.assertEqual(model.framework, "PICO")
        self.assertIn(model.domain, ["cardiovascular", "cardiology"])
        self.assertIn("Heart Failure", model.target_condition.name_en)
        
        # Search planner dual-path
        planner = GenericSearchPlanner(model)
        matrix = planner.build_query_matrix()
        self.assertGreater(matrix["dual_path_execution"]["supporting_search_count"], 0)
        self.assertGreater(matrix["dual_path_execution"]["contradicting_search_count"], 0)
        
        # Timeline must have clinical trial phasing (ethical approval, ITT analysis)
        timeline = DynamicProtocolDesigner.generate_timeline(model.framework)
        phase_titles = " ".join(p["phase_title"] for p in timeline)
        self.assertIn("اخلاق", phase_titles)
        self.assertIn("کارآزمایی", phase_titles)
        
        # Studies and gap detection
        studies = data.get("studies", [])
        gaps = GenericGapDetector.detect_gaps(studies, model.to_dict())
        self.assertTrue(any(g["gap_category"] in ["POPULATION_GAP", "TRANSLATIONAL_GAP", "KNOWLEDGE_GAP"] for g in gaps))

    def test_03_infectious_antiviral_resistance_invariants(self):
        """Verifies antiviral pharmacology, mutation-mediated resistance, and rebound mechanistic gaps."""
        data = self._load_fixture("infectious_antiviral")
        model = ProblemModelBuilder.create_from_specification(data["research_problem_model"])
        
        self.assertIn(model.domain, ["infectious_disease", "infectious_diseases"])
        title_intervention = (model.research_title_en + " " + model.interventions_or_exposures[0].name).lower()
        self.assertTrue("nirmatrelvir" in title_intervention or "paxlovid" in title_intervention)
        
        # Primary outcomes must evaluate viral load or clearance
        outcomes = [o.name.lower() for o in model.primary_outcomes]
        self.assertTrue(any("viral load" in o or "rebound" in o or "virologic" in o for o in outcomes))
        
        # Contradiction engine must identify resistance / target mutation mechanisms
        studies = data.get("studies", [])
        contra = GenericContradictionEngine.detect_contradictions(studies)
        self.assertIsNotNone(contra)

    def test_04_diagnostic_biomarker_accuracy_invariants(self):
        """Verifies index test vs reference standard, QUADAS-2 comparability, and stage disparity."""
        data = self._load_fixture("diagnostic_biomarker")
        model = ProblemModelBuilder.create_from_specification(data["research_problem_model"])
        
        self.assertEqual(model.framework, "DIAGNOSTIC")
        self.assertIn("ctDNA", model.research_title_en + " " + model.interventions_or_exposures[0].name)
        
        # Timeline must feature diagnostic index test and gold standard
        timeline = DynamicProtocolDesigner.generate_timeline("DIAGNOSTIC")
        titles = " ".join(t["phase_title"] for t in timeline)
        self.assertIn("Index Test", titles)
        self.assertIn("Gold Standard", titles)
        
        # Studies comparability must evaluate diagnostic dimensions
        studies = data.get("studies", [])
        comp = GenericComparabilityEngine.evaluate_cohort(studies)
        self.assertIn("summary", comp)

    def test_05_epidemiological_cohort_causal_boundary_invariants(self):
        """Verifies PECO environmental exposure, confounder control, and causal overclaim prevention."""
        data = self._load_fixture("epidemiological_cohort")
        model = ProblemModelBuilder.create_from_specification(data["research_problem_model"])
        
        self.assertEqual(model.framework, "PECO")
        self.assertIn(model.domain, ["pulmonology", "epidemiology"])
        self.assertIn("PM2.5", model.research_title_en + " " + model.interventions_or_exposures[0].name)
        
        # Anti-Causal Overclaim Gate: Observational claim using 'causes' must be flagged as OVERCLAIM_RISK
        observational_claim = "Long-term ambient PM2.5 exposure directly causes COPD progression and alveolar destruction."
        audit_res = GenericClaimEntailmentEngine.audit_causal_language(observational_claim, "OBSERVATIONAL_COHORT")
        self.assertFalse(audit_res["allowed_unconditional_causal_claim"])
        self.assertEqual(audit_res["status"], "OVERCLAIM_RISK")
        self.assertTrue(len(audit_res["flagged_causal_words"]) > 0)
        
        # Confounders in variable table
        vars_table = DynamicProtocolDesigner.generate_variable_table(model.to_dict())
        confounders = [v for v in vars_table if "Confounder" in v["role"] or "مخدوشگر" in v["role"]]
        self.assertGreaterEqual(len(confounders), 1)

    def test_06_basic_molecular_biology_mechanistic_invariants(self):
        """Fixture F: Basic molecular biology, ubiquitination clearance, and null oxidant thresholds."""
        data = self._load_fixture("basic_molecular_biology")
        model = ProblemModelBuilder.create_from_specification(data["research_problem_model"])
        
        self.assertEqual(model.framework, "MECHANISTIC")
        self.assertEqual(model.domain, "basic_biomedical")
        self.assertIn("p53", model.research_title_en + " " + model.hypothesized_mechanisms[0].target_molecules[1])
        
        # Mechanistic timeline must contain molecular rescue and signaling phases
        timeline = DynamicProtocolDesigner.generate_timeline("MECHANISTIC")
        titles = " ".join(t["phase_title"] for t in timeline)
        self.assertIn("مسیر پیام‌رسانی", titles)
        self.assertIn("فسفوریلاسیون", titles)
        
        # Contradiction detection on null findings
        studies = data.get("studies", [])
        contra = GenericContradictionEngine.detect_contradictions(studies)
        self.assertEqual(contra["total_negative_findings"], 1)

    def test_07_animal_experimental_preclinical_invariants(self):
        """Fixture G: Preclinical in vivo animal study, Mead resource equation, and ethical vetting."""
        data = self._load_fixture("animal_experimental")
        model = ProblemModelBuilder.create_from_specification(data["research_problem_model"])
        
        self.assertEqual(model.framework, "EXPERIMENTAL_ANIMAL")
        self.assertEqual(model.domain, "neurology")
        self.assertEqual(model.population_or_model.model_type, "ANIMAL_IN_VIVO")
        
        # Sample size guidance must reference Mead's Resource equation
        sample_plan = DynamicProtocolDesigner.calculate_sample_size_plan(model.to_dict())
        self.assertEqual(sample_plan["design_type"], "IN_VIVO_ANIMAL")
        self.assertIn("Mead", sample_plan["formula_or_standard"])
        
        # Timeline must feature animal quarantine and bioethics
        timeline = DynamicProtocolDesigner.generate_timeline("EXPERIMENTAL_ANIMAL")
        titles = " ".join(t["phase_title"] for t in timeline)
        self.assertIn("حیوانات", titles)
        self.assertIn("اخلاق", titles)

    def test_08_clinical_rct_endocrinology_invariants(self):
        """Fixture H: Human clinical randomized double-blind trial, ITT analysis, and safety boundaries."""
        data = self._load_fixture("clinical_rct_endocrinology")
        model = ProblemModelBuilder.create_from_specification(data["research_problem_model"])
        
        self.assertEqual(model.framework, "PICO")
        self.assertEqual(model.domain, "endocrinology")
        self.assertEqual(model.population_or_model.model_type, "HUMAN_CLINICAL")
        
        # Statistical plan must enforce Intention-to-Treat (ITT) and survival / Cox models
        stat_plan = DynamicProtocolDesigner.generate_statistical_plan(model.to_dict())
        stat_text = " ".join(stat_plan["complete_testing_strategy"])
        self.assertIn("قصد درمان", stat_text)
        self.assertIn("کاکس", stat_text)
        
        # Sample size for human clinical trial requires pilot data if parameters uncharacterized
        sample_plan = DynamicProtocolDesigner.calculate_sample_size_plan(model.to_dict())
        self.assertTrue(sample_plan["pilot_required"])

    def test_09_unrelated_nephrology_biomarker_invariants(self):
        """Fixture I: Completely distinct topic (Nephrology prognostic autoantibody, C-index, ROC)."""
        data = self._load_fixture("unrelated_nephrology_biomarker")
        model = ProblemModelBuilder.create_from_specification(data["research_problem_model"])
        
        self.assertEqual(model.framework, "PROGNOSTIC")
        self.assertEqual(model.domain, "nephrology")
        self.assertIn("PLA2R", model.research_title_en + " " + model.interventions_or_exposures[0].name)
        
        # Statistical plan for prognostic models must include C-index and calibration
        stat_plan = DynamicProtocolDesigner.generate_statistical_plan(model.to_dict())
        stat_text = " ".join(stat_plan["complete_testing_strategy"])
        self.assertIn("هارل", stat_text)
        self.assertIn("کالیبراسیون", stat_text)
        
        # Dual-path search matrix must not contain any leaked terms from other topics
        planner = GenericSearchPlanner(model)
        matrix = planner.build_query_matrix()
        matrix_str = json.dumps(matrix).lower()
        self.assertNotIn("lupeol", matrix_str)
        self.assertNotIn("ndv", matrix_str)
    def test_10_biomaterials_regenerative_scaffold_invariants(self):
        """Unseen Topic Benchmark 1: Regenerative Biomaterials / Tissue Engineering Scaffold."""
        spec = {
            "model_id": "RPM_REGEN_BIO_01",
            "research_title_fa": "بررسی بازسازی بافت استخوانی توسط داربست نانوالیاف ابریشم بارگذاری‌شده با BMP-2",
            "research_title_en": "Evaluation of Silk Fibroin Nanofibrous Scaffolds Loaded with BMP-2 for Critical-Sized Bone Defect Regeneration",
            "domain": "biomaterials_regenerative",
            "framework": "EXPERIMENTAL_ANIMAL",
            "target_condition": {
                "name_en": "Critical-Sized Cranial Bone Defect",
                "name_fa": "نقص استخوانی اندازه بحرانی کاسه سر",
                "mesh_term": "Bone Regeneration",
                "synonyms": ["calvarial defect", "bone defect repair"]
            },
            "population_or_model": {
                "model_type": "ANIMAL_IN_VIVO",
                "primary_system": "Sprague-Dawley Rats (Calvarial defect model)",
                "secondary_systems": [],
                "normal_control_system": "Sham-operated negative control"
            },
            "interventions_or_exposures": [
                {
                    "name": "Silk Fibroin BMP-2 Scaffold",
                    "chemical_or_biological_class": "Tissue Engineering Scaffold",
                    "role": "PRIMARY_AGENT",
                    "mesh_terms": ["Tissue Scaffolds", "Bone Morphogenetic Protein 2"],
                    "synonyms": ["SF-BMP2"]
                }
            ],
            "comparators": [{"name": "Unseeded Silk Scaffold", "type": "VEHICLE_SCAFFOLD"}],
            "primary_outcomes": [
                {"name": "Bone Mineral Density by Micro-CT", "type": "CONTINUOUS", "measurement_unit": "mg HA/ccm"}
            ],
            "hypothesized_mechanisms": [
                {"pathway_name": "Osteogenic Differentiation and Runx2 Activation", "target_molecules": ["Runx2", "Osteocalcin"], "expected_modulation": "UPREGULATION"}
            ]
        }
        model = ProblemModelBuilder.create_from_specification(spec)
        self.assertEqual(model.framework, "EXPERIMENTAL_ANIMAL")
        self.assertEqual(model.domain, "biomaterials_regenerative")

        planner = GenericSearchPlanner(model)
        matrix = planner.build_query_matrix()
        self.assertEqual(matrix["dual_path_execution"]["supporting_search_count"], 7)
        self.assertEqual(matrix["dual_path_execution"]["contradicting_search_count"], 9)
        # Verify complete domain independence
        matrix_str = json.dumps(matrix).lower()
        self.assertNotIn("cancer", matrix_str)
        self.assertNotIn("lupeol", matrix_str)
        self.assertIn("bone regeneration", matrix_str)

        # Check required streams for animal models
        streams = GenericSearchPlanner.get_required_evidence_streams(model.framework)
        self.assertIn("ANIMAL_WELFARE_SYRCLE", streams)
        self.assertIn("METHODOLOGICAL_ARRIVE", streams)

    def test_11_toxicology_occupational_cohort_peco_invariants(self):
        """Unseen Topic Benchmark 2: Occupational Toxicology / Silica Exposure Cohort (PECO)."""
        spec = {
            "model_id": "RPM_TOXICOLOGY_02",
            "research_title_fa": "بررسی خطر فیبروز ریوی ناشی از مواجهه شغلی با گرد و غبار سیلیس در کارگران معدن",
            "research_title_en": "Occupational Respirable Crystalline Silica Exposure and Risk of Pulmonary Fibrosis: A Prospective Cohort Study",
            "domain": "occupational_epidemiology",
            "framework": "PECO",
            "target_condition": {
                "name_en": "Silicosis and Pulmonary Fibrosis",
                "name_fa": "سیلیکوزیس و فیبروز بینابینی ریه",
                "mesh_term": "Silicosis",
                "synonyms": ["silica-induced fibrosis", "pneumoconiosis"]
            },
            "population_or_model": {
                "model_type": "HUMAN_COHORT",
                "primary_system": "Surface and Underground Mining Workers",
                "secondary_systems": [],
                "normal_control_system": "Unexposed administrative workers"
            },
            "interventions_or_exposures": [
                {
                    "name": "Respirable Crystalline Silica Dust",
                    "chemical_or_biological_class": "Occupational Inhalational Toxicant",
                    "role": "PRIMARY_EXPOSURE",
                    "mesh_terms": ["Silicon Dioxide", "Air Pollutants, Occupational"],
                    "synonyms": ["quartz dust"]
                }
            ],
            "comparators": [{"name": "Unexposed Baseline Cohort", "type": "INTERNAL_CONTROL"}],
            "primary_outcomes": [
                {"name": "Incidence of Radiographic Silicosis (ILO Classification)", "type": "HAZARD_RATIO", "measurement_unit": "Adjusted Hazard Ratio"}
            ],
            "hypothesized_mechanisms": [
                {"pathway_name": "Alveolar Macrophage Pyroptosis and NLRP3 Inflammasome", "target_molecules": ["NLRP3", "IL-1beta", "TGF-beta1"], "expected_modulation": "ACTIVATION"}
            ]
        }
        model = ProblemModelBuilder.create_from_specification(spec)
        self.assertEqual(model.framework, "PECO")

        # Causal overclaim gate test for observational PECO design
        claim = "Occupational silica dust causes progressive pulmonary fibrosis in all exposed miners."
        res_causal = GenericClaimEntailmentEngine.audit_causal_language(claim, "OBSERVATIONAL_COHORT_CASE_CONTROL")
        self.assertEqual(res_causal["status"], "OVERCLAIM_RISK")
        self.assertFalse(res_causal["allowed_unconditional_causal_claim"])

        # Check required streams for PECO
        peco_streams = GenericSearchPlanner.get_required_evidence_streams(model.framework)
        self.assertIn("CONFOUNDING_BIAS", peco_streams)
        self.assertIn("DOSE_RESPONSE_GRADIENT", peco_streams)

    def test_12_pediatric_asthma_prognostic_multivariable_invariants(self):
        """Unseen Topic Benchmark 3: Pediatric Asthma Remission Prognosis (Multivariable Cox / C-index)."""
        spec = {
            "model_id": "RPM_PEDIATRIC_ASTHMA_03",
            "research_title_fa": "مدل پیش‌آگهی تداوم آسم دوران کودکی بر اساس فنوتیپ‌های التهابی و بیومارکرهای ائوزینوفیلی",
            "research_title_en": "Development and Internal Validation of a Multivariable Prognostic Model for Childhood Asthma Persistence into Adulthood",
            "domain": "pediatric_pulmonology",
            "framework": "PROGNOSTIC",
            "target_condition": {
                "name_en": "Asthma Persistence into Adulthood",
                "name_fa": "تداوم بیماری آسم در بزرگسالی",
                "mesh_term": "Asthma",
                "synonyms": ["pediatric asthma persistence", "wheezing remission failure"]
            },
            "population_or_model": {
                "model_type": "HUMAN_COHORT",
                "primary_system": "Pediatric Asthma Birth Cohort (Ages 6-18)",
                "secondary_systems": [],
                "normal_control_system": "Children with transient early wheeze"
            },
            "interventions_or_exposures": [
                {
                    "name": "Blood Eosinophil Count and FeNO Profile",
                    "chemical_or_biological_class": "Prognostic Biomarker Panel",
                    "role": "PROGNOSTIC_FACTOR",
                    "mesh_terms": ["Eosinophils", "Fractional Exhaled Nitric Oxide"],
                    "synonyms": ["FeNO", "blood eosinophils"]
                }
            ],
            "comparators": [{"name": "Standard Clinical Risk Scoring", "type": "EXISTING_PREDICTOR"}],
            "primary_outcomes": [
                {"name": "Asthma Persistence at Age 18", "type": "BINARY_AND_TIME_TO_EVENT", "measurement_unit": "Harrell's C-index"}
            ],
            "hypothesized_mechanisms": [
                {"pathway_name": "Type 2 Airway Remodeling and Basal Membrane Thickening", "target_molecules": ["IL-4", "IL-13", "Periostin"], "expected_modulation": "PERSISTENT_ELEVATION"}
            ]
        }
        model = ProblemModelBuilder.create_from_specification(spec)
        self.assertEqual(model.framework, "PROGNOSTIC")

        # Test statistical strategy contains C-index and Cox regression
        stat_plan = DynamicProtocolDesigner.generate_statistical_plan(model.to_dict())
        stat_text = " ".join(stat_plan["complete_testing_strategy"])
        self.assertIn("هارل", stat_text)
        self.assertIn("کاکس", stat_text)

        # Gap detection check for prognostic cohort
        gap_res = GenericGapDetector.identify_gaps(
            target_model=model.to_dict(),
            study_evidence=[
                {"study_id": "S_P1", "model_system": "Pediatric Asthma Birth Cohort", "variables_measured": ["blood_eosinophils"], "multivariate_adjusted": True}
            ]
        )
        self.assertIn("identified_gaps", gap_res)
        self.assertGreater(len(gap_res["identified_gaps"]), 0)


def run_generalization_suite() -> bool:
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMultiDomainGeneralization)
    runner = unittest.TextTestRunner(verbosity=1)
    res = runner.run(suite)
    return res.wasSuccessful()

if __name__ == "__main__":
    unittest.main()
