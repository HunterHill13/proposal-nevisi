#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_property_and_schemas.py - Metamorphic Properties, Schemas & Independent Synthetic Benchmark (Phases 18, 19, 20)
Proposal-Nevisi Engine v8.2 (Universal Biomedical Architecture)

Validates:
1. 8 Metamorphic / Property-Based Invariants (Phase 19)
2. JSON Schema contract validation with negative failure tests (Phase 20)
3. Independent synthetic randomized domain benchmark (Phase 18)
"""

import unittest
import copy
import random
import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.abspath(os.path.join(TESTS_DIR, "..", "scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from generic_search_planner import GenericSearchPlanner
from generic_reference_auditor import GenericReferenceAuditor
from generic_claim_entailment_engine import GenericClaimEntailmentEngine
from schema_validator import SchemaValidator
from research_problem_model import ProblemModelBuilder

class TestPropertyAndSchemas(unittest.TestCase):
    """Executes metamorphic property-based assertions and schema validations."""

    def setUp(self):
        self.auditor = GenericReferenceAuditor(current_year=2026)

    # =========================================================================
    # PHASE 19: METAMORPHIC / PROPERTY-BASED INVARIANTS (1 to 8)
    # =========================================================================

    def test_invariant_01_reordering_references_preserves_identity(self):
        """Invariant 1: Reordering references must never alter their identity classifications."""
        ref1 = {"ref_id": "R1", "title": "Paper One", "doi": "10.1000/1", "year": 2024}
        ref2 = {"ref_id": "R2", "title": "Paper Two", "doi": "10.1000/2", "year": 2023}
        meta1 = {"title": "Paper One", "doi": "10.1000/1", "year": 2024}
        meta2 = {"title": "Paper Two", "doi": "10.1000/2", "year": 2023}

        # Order A: [ref1, ref2]
        res1_a = self.auditor.audit_bibliographic_fields(ref1, meta1)
        res2_a = self.auditor.audit_bibliographic_fields(ref2, meta2)

        # Order B: [ref2, ref1]
        res2_b = self.auditor.audit_bibliographic_fields(ref2, meta2)
        res1_b = self.auditor.audit_bibliographic_fields(ref1, meta1)

        self.assertEqual(res1_a["verification_status"], res1_b["verification_status"])
        self.assertEqual(res2_a["verification_status"], res2_b["verification_status"])

    def test_invariant_02_adding_duplicate_does_not_increase_unique_count(self):
        """Invariant 2: Adding a duplicate record must never increase the unique study count."""
        base_records = [
            {"pmid": "111", "doi": "10.1000/1", "title": "Study Alpha"},
            {"pmid": "222", "doi": "10.1000/2", "title": "Study Beta"}
        ]
        res_base = GenericSearchPlanner.deduplicate_records(base_records)
        initial_unique = res_base["unique_records_count"]

        # Add duplicate of Study Alpha
        expanded = base_records + [{"pmid": "111", "title": "Study Alpha (Alternative Index)"}]
        res_expanded = GenericSearchPlanner.deduplicate_records(expanded)

        self.assertEqual(res_expanded["unique_records_count"], initial_unique)
        self.assertEqual(res_expanded["duplicates_removed_count"], 1)

    def test_invariant_03_changing_citation_order_preserves_claim_support(self):
        """Invariant 3: Changing the order of citations or facts must not alter claim entailment status."""
        claim = "Compound Z inhibits cytokine release."
        source = {"study_id": "ST_01", "study_design": "IN_VITRO_EXPERIMENTAL"}
        f1 = {"directness": "DIRECT_EVIDENCE", "text_or_data": "Z reduces IL-6 release by 50%"}
        f2 = {"directness": "INDIRECT_EVIDENCE", "text_or_data": "Z alters NF-kB transcription"}

        res_order1 = GenericClaimEntailmentEngine.evaluate_claim_entailment("C1", claim, source, [f1, f2])
        res_order2 = GenericClaimEntailmentEngine.evaluate_claim_entailment("C1", claim, source, [f2, f1])

        self.assertEqual(res_order1["entailment_status"], res_order2["entailment_status"])
        self.assertEqual(res_order1["entailment_status"], "DIRECTLY_SUPPORTED")

    def test_invariant_04_adding_irrelevant_evidence_does_not_promote_entailment(self):
        """Invariant 4: Adding irrelevant or hypothesis-level evidence must not promote direct entailment."""
        claim = "Agent Q decreases myocardial infarct size."
        source = {"study_id": "ST_02", "study_design": "ANIMAL_IN_VIVO"}
        f_hypo = [{"directness": "HYPOTHESIS", "text_or_data": "Agent Q is proposed to affect necrosis"}]

        res_before = GenericClaimEntailmentEngine.evaluate_claim_entailment("C2", claim, source, f_hypo)
        self.assertEqual(res_before["entailment_status"], "HYPOTHESIS_ONLY")

        # Add another non-direct fact
        f_combined = f_hypo + [{"directness": "INFERENCE", "text_or_data": "Related compound Q-prime shows trend"}]
        res_after = GenericClaimEntailmentEngine.evaluate_claim_entailment("C2", claim, source, f_combined)

        self.assertNotEqual(res_after["entailment_status"], "DIRECTLY_SUPPORTED")

    def test_invariant_05_removing_only_supporting_evidence_demotes_claim(self):
        """Invariant 5: Removing the only supporting evidence must demote claim to UNSUPPORTED."""
        claim = "Therapy W improves overall survival."
        source = {"study_id": "ST_03", "study_design": "RANDOMIZED_CONTROLLED_TRIAL"}
        f_direct = [{"directness": "DIRECT_EVIDENCE", "text_or_data": "Median OS extended by 4.2 months (p=0.01)"}]

        res_with = GenericClaimEntailmentEngine.evaluate_claim_entailment("C3", claim, source, f_direct)
        self.assertEqual(res_with["entailment_status"], "DIRECTLY_SUPPORTED")

        res_without = GenericClaimEntailmentEngine.evaluate_claim_entailment("C3", claim, source, [])
        self.assertEqual(res_without["entailment_status"], "UNSUPPORTED")

    def test_invariant_06_observational_to_rct_design_changes_causal_gate(self):
        """Invariant 6: Changing observational to RCT design must appropriately clear the causal overclaim risk."""
        claim_text = "Treatment with Molecule M causes remission."

        # Observational design -> Overclaim risk
        res_obs = GenericClaimEntailmentEngine.audit_causal_language(claim_text, "OBSERVATIONAL_COHORT_CASE_CONTROL")
        self.assertEqual(res_obs["status"], "OVERCLAIM_RISK")

        # Interventional RCT design -> Compliant with causal verb
        res_rct = GenericClaimEntailmentEngine.audit_causal_language(claim_text, "RANDOMIZED_CONTROLLED_TRIAL")
        self.assertEqual(res_rct["status"], "COMPLIANT")

    def test_invariant_07_changing_numerical_unit_triggers_inconsistency(self):
        """Invariant 7: Changing a numerical unit without converting value triggers numerical discrepancy."""
        source_rec = {
            "study_id": "ST_05",
            "original_value": 50.0,
            "unit": "micromolar",
            "claim_unit": "molar", # Mismatched unit without formula
            "source_location": {"page": 4}
        }
        res = GenericClaimEntailmentEngine.audit_numerical_provenance(50.0, source_rec)
        self.assertFalse(res["is_provenance_verified"])
        self.assertIn("WRONG_UNIT", res["detected_issues"])

    def test_invariant_08_missing_metadata_never_becomes_positive_assertion(self):
        """Invariant 8: Missing metadata must never silently become a positive assertion."""
        # Reference with completely missing publication date and year
        ref_empty = {"ref_id": "REF_UNKNOWN_DATE"}
        res = self.auditor.audit_temporal_tier(ref_empty)

        self.assertFalse(res["is_temporally_valid"])
        self.assertFalse(res["core_evidence_eligible"])
        self.assertEqual(res["temporal_tier"], "DATE_UNCERTAIN")

    # =========================================================================
    # PHASE 20: JSON SCHEMA CONTRACT VALIDATION (Draft-07)
    # =========================================================================

    def test_schema_01_search_provenance_schema_valid_and_invalid(self):
        """Schema Test 1: SEARCH_PROVENANCE_SCHEMA validation against compliant and malformed records."""
        schema = SchemaValidator.load_schema("SEARCH_PROVENANCE_SCHEMA")

        valid_record = {
            "provenance_type": "SEARCH_PROVENANCE_RECORD",
            "total_queries_executed": 4,
            "databases_queried": ["PubMed", "Europe PMC"],
            "records_retrieved": 14,
            "records_screened": 14,
            "records_included": 5,
            "records_excluded": 9,
            "reproducibility_verified": True,
            "query_event_logs": [
                {
                    "database": "PubMed",
                    "exact_query": "Empagliflozin AND HFpEF",
                    "search_layer": "LAYER_A",
                    "execution_status": "SEARCH_EXECUTED",
                    "results_count": 14,
                    "retrieved_count": 14,
                    "screened_count": 14,
                    "included_count": 5,
                    "excluded_count": 9,
                    "timestamp": "2026-10-04T12:00:00Z"
                }
            ]
        }
        self.assertTrue(SchemaValidator.is_valid(valid_record, schema))

        # Negative test 1: Missing required query_event_logs
        invalid_missing = copy.deepcopy(valid_record)
        del invalid_missing["query_event_logs"]
        self.assertFalse(SchemaValidator.is_valid(invalid_missing, schema))

        # Negative test 2: Invalid provenance_type enum
        invalid_enum = copy.deepcopy(valid_record)
        invalid_enum["provenance_type"] = "FAKE_STATUS_NOT_IN_ENUM"
        self.assertFalse(SchemaValidator.is_valid(invalid_enum, schema))

        # Negative test 3: Negative results_count
        invalid_count = copy.deepcopy(valid_record)
        invalid_count["records_retrieved"] = -5
        self.assertFalse(SchemaValidator.is_valid(invalid_count, schema))

    def test_schema_02_reference_record_schema_valid_and_invalid(self):
        """Schema Test 2: REFERENCE_RECORD_SCHEMA validation against compliant and malformed records."""
        schema = SchemaValidator.load_schema("REFERENCE_RECORD_SCHEMA")

        valid_ref = {
            "ref_id": "REF_01",
            "title": "Empagliflozin in Heart Failure with Preserved Ejection Fraction",
            "year": 2021,
            "authors": ["Anker SD", "Butler J", "Filippatos G"],
            "journal": "N Engl J Med",
            "doi": "10.1056/nejmoa2107038",
            "pmid": "34449189",
            "verification_status": "EXACT_VERIFIED",
            "is_retracted": False,
            "is_corrected": False,
            "core_evidence_eligible": True
        }
        self.assertTrue(SchemaValidator.is_valid(valid_ref, schema))

        # Negative test 1: Missing required title
        invalid_no_title = copy.deepcopy(valid_ref)
        del invalid_no_title["title"]
        self.assertFalse(SchemaValidator.is_valid(invalid_no_title, schema))

        # Negative test 2: Invalid verification_status enum
        invalid_status = copy.deepcopy(valid_ref)
        invalid_status["verification_status"] = "UNSUPPORTED_STATUS"
        self.assertFalse(SchemaValidator.is_valid(invalid_status, schema))

        # Negative test 3: Wrong type for year (string instead of integer)
        invalid_year = copy.deepcopy(valid_ref)
        invalid_year["year"] = "twenty-twenty-one"
        self.assertFalse(SchemaValidator.is_valid(invalid_year, schema))

    def test_schema_03_claim_provenance_schema_valid_and_invalid(self):
        """Schema Test 3: CLAIM_PROVENANCE_SCHEMA validation against compliant and malformed claims."""
        schema = SchemaValidator.load_schema("CLAIM_PROVENANCE_SCHEMA")

        valid_claim = {
            "claim_id": "CLM_001",
            "claim_text": "Empagliflozin reduced the combined risk of cardiovascular death or hospitalization.",
            "source_ref_id": "REF_EMPEROR_PRESERVED",
            "source_study_design": "RCT",
            "claim_type": "CAUSAL",
            "entailment_level": "FULLY_ENTAILED",
            "verdict": "ENTAILED",
            "has_overclaim_risk": False,
            "flagged_issues": []
        }
        self.assertTrue(SchemaValidator.is_valid(valid_claim, schema))

        # Negative test 1: Missing required claim_text
        invalid_claim = copy.deepcopy(valid_claim)
        del invalid_claim["claim_text"]
        self.assertFalse(SchemaValidator.is_valid(invalid_claim, schema))

        # Negative test 2: Invalid entailment_level
        invalid_entailment = copy.deepcopy(valid_claim)
        invalid_entailment["entailment_level"] = "ABSOLUTELY_PROVEN_TRUE"
        self.assertFalse(SchemaValidator.is_valid(invalid_entailment, schema))

    # =========================================================================
    # PHASE 18: INDEPENDENT SYNTHETIC RANDOMIZED DOMAIN BENCHMARK
    # =========================================================================

    def test_synthetic_randomized_domain_benchmark(self):
        """Phase 18: Independent synthetic domain benchmark evaluating core agnostic execution on randomized inputs."""
        # Generate an entirely synthetic non-human novel biological domain
        frameworks = ["PICO", "PECO", "DIAGNOSTIC", "PROGNOSTIC", "MECHANISTIC", "EXPERIMENTAL_IN_VITRO"]
        selected_framework = random.choice(frameworks)
        
        spec = {
            "model_id": f"SYNTHETIC_MODEL_{random.randint(1000, 9999)}",
            "research_title_fa": "بررسی اثر عامل سنتتیک بر سیستم ناشناخته",
            "research_title_en": "Investigation of Synthetic Agent Omega in Xenobiotic Cellular Matrix",
            "domain": "xenobiology_synthetic",
            "framework": selected_framework,
            "target_condition": {
                "name_en": "Synthetic Metabolic Desynchrony",
                "name_fa": "ناهماهنگی متابولیک سنتتیک",
                "mesh_term": "Metabolic Diseases",
                "synonyms": ["SMD", "desynchrony"]
            },
            "population_or_model": {
                "model_type": "SYNTHETIC_BIOENGINEERED_SYSTEM",
                "primary_system": "Cellular Matrix Alpha-9",
                "secondary_systems": [],
                "normal_control_system": "Standard unperturbed matrix"
            },
            "interventions_or_exposures": [
                {
                    "name": "Synthetic Molecule Omega-42",
                    "chemical_or_biological_class": "Xenobiotic Regulator",
                    "role": "PRIMARY_AGENT",
                    "mesh_terms": ["Organic Chemicals"],
                    "synonyms": ["Omega-42"]
                }
            ],
            "comparators": [{"name": "Vehicle Solute", "type": "PLACEBO"}],
            "primary_outcomes": [
                {"name": "Resynchronization Index", "type": "PERCENTAGE", "measurement_unit": "% resync"}
            ],
            "hypothesized_mechanisms": [
                {"pathway_name": "Kinase-X Phosphorylation Cascade", "target_molecules": ["Kin-X", "Reg-Y"], "expected_modulation": "ACTIVATION"}
            ]
        }

        # 1. Build Research Problem Model
        model = ProblemModelBuilder.create_from_specification(spec)
        self.assertEqual(model.domain, "xenobiology_synthetic")
        self.assertEqual(model.framework, selected_framework)

        # 2. Plan Multi-Facet Search
        planner = GenericSearchPlanner(model)
        query_matrix = planner.build_query_matrix()
        self.assertIn("LAYER_A_DIRECT_EVIDENCE", query_matrix["query_matrix_facets"])
        self.assertGreater(query_matrix["dual_path_execution"]["supporting_search_count"], 0)

        # 3. Deduplicate Noisy Records
        noisy_records = [
            {"pmid": "999001", "doi": "10.5555/syn.01", "title": "Synthetic Molecule Omega-42 in Matrix Alpha-9"},
            {"pmid": "999001", "title": "Synthetic Molecule Omega-42 in Matrix Alpha-9 (Duplicate entry)"},
            {"pmid": "999002", "doi": "10.5555/syn.02", "title": "Unrelated Baseline Control Study"}
        ]
        dedup = GenericSearchPlanner.deduplicate_records(noisy_records)
        self.assertEqual(dedup["unique_records_count"], 2)
        self.assertEqual(dedup["duplicates_removed_count"], 1)

if __name__ == "__main__":
    unittest.main()
