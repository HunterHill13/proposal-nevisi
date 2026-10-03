#!/usr/bin/env python3
"""
test_adversarial_scenarios.py - Adversarial Stress-Testing Suite (12 Scenarios)
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

Stress-tests the engine against deliberate epistemic deception, fake DOIs,
partial entailment, ungrounded numbers, observational overclaiming, and bias misattribution.
"""

import os
import sys
import unittest

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
sys.path.insert(0, SCRIPTS_DIR)

from generic_reference_auditor import GenericReferenceAuditor
from generic_claim_entailment_engine import GenericClaimEntailmentEngine
from generic_contradiction_engine import GenericContradictionEngine
from generic_study_family_detector import StudyFamilyDetector

class TestAdversarialScenarios(unittest.TestCase):

    def setUp(self):
        self.auditor = GenericReferenceAuditor(current_year=2026, max_primary_age_years=6, min_required_references=2)

    def test_01_fake_citation_detection(self):
        """Test 1: Deliberately fabricated citation with bogus DOI and title."""
        fake_local = {"ref_id": "REF_FAKE", "title": "Fabricated Paper on Nonexistent Drug", "doi": "10.1000/fake.doi.999", "year": 2024}
        authoritative = {"title": "Real unrelated paper on physics", "year": 2015, "authors": ["Einstein A"]}
        res = self.auditor.audit_bibliographic_fields(fake_local, authoritative)
        self.assertEqual(res["verification_status"], "CONFLICT_OR_UNVERIFIED")
        self.assertLess(res["title_similarity"], 0.60)

    def test_02_mismatched_doi(self):
        """Test 2: Real DOI that belongs to a totally different paper."""
        local = {"ref_id": "REF_MISMATCH", "title": "Oncolytic activity in lung cancer", "doi": "10.1056/NEJMoa123", "year": 2023}
        authoritative = {"title": "Clinical cardiology trial of beta blockers", "doi": "10.1056/NEJMoa123", "year": 2018}
        res = self.auditor.audit_bibliographic_fields(local, authoritative)
        self.assertEqual(res["verification_status"], "CONFLICT_OR_UNVERIFIED")
        self.assertFalse(res["year_match"])

    def test_03_partial_claim_support(self):
        """Test 3: Paper supports general inhibition but not specific combination synergy."""
        study = {"study_id": "S_PARTIAL", "study_design": "IN_VITRO_EXPERIMENTAL"}
        facts = [{"directness": "INDIRECT_EVIDENCE", "text_or_data": "Compound A moderately reduces cell growth alone."}]
        res = GenericClaimEntailmentEngine.evaluate_claim_entailment(
            "CLM_P", "Compound A exhibits strong synergistic apoptosis when combined with Agent B.",
            study, facts
        )
        self.assertEqual(res["entailment_status"], "INDIRECTLY_SUPPORTED")
        self.assertNotEqual(res["entailment_status"], "DIRECTLY_SUPPORTED")

    def test_04_contradictory_studies_contextual_resolution(self):
        """Test 4: Two studies with conflicting outcomes resolved via parameter differences."""
        pos = {"study_id": "S_POS", "context_parameters": {"dose": "50 uM", "cell_line_or_model": "A549", "assay": "MTT"}}
        neg = {"study_id": "S_NEG", "category": "NULL_RESULT", "context_parameters": {"dose": "1 uM", "cell_line_or_model": "A549", "assay": "MTT"}}
        res = GenericContradictionEngine.analyze_discrepancy(pos, neg)
        self.assertEqual(res["contradiction_type"], "CONTEXTUAL_DISAGREEMENT")
        self.assertIn("dose: '50 um' vs '1 um'", res["contextual_divergences"][0].lower())

    def test_05_foundational_paper_approved(self):
        """Test 5: Seminal 1984 paper with valid foundational mathematical model justification."""
        ref = {
            "ref_id": "REF_CHOU_1984",
            "year": 1984,
            "foundational_justification": {
                "is_justified": True,
                "category": "FOUNDATIONAL_MATHEMATICAL_MODEL",
                "rationale": "Chou-Talalay Median-Effect Equation for Combination Index calculations."
            }
        }
        res = self.auditor.audit_temporal_tier(ref)
        self.assertEqual(res["temporal_tier"], "FOUNDATIONAL/HISTORICAL_EVIDENCE")
        self.assertTrue(res["is_temporally_valid"])

    def test_06_unjustified_old_paper_rejected(self):
        """Test 6: Old paper (2012) without foundational justification is flagged."""
        ref = {"ref_id": "REF_OLD_UNJUSTIFIED", "year": 2012}
        res = self.auditor.audit_temporal_tier(ref)
        self.assertEqual(res["temporal_tier"], "FOUNDATIONAL/HISTORICAL_EVIDENCE")
        self.assertFalse(res["is_temporally_valid"])

    def test_07_abstract_only_evidence_flagged(self):
        """Test 7: Abstract-only paper is flagged and cannot sustain granular facts."""
        record = {
            "study_id": "S_ABS",
            "fulltext_status": "ABSTRACT_ONLY"
        }
        self.assertEqual(record["fulltext_status"], "ABSTRACT_ONLY")

    def test_08_null_result_cataloged(self):
        """Test 8: Study with null outcome is properly categorized in negative evidence."""
        neg_finding = {"category": "NULL_RESULT", "description": "No significant reduction in tumor volume (p=0.42)"}
        report = GenericContradictionEngine.build_contradiction_report([neg_finding], {"boundary": "All databases"})
        self.assertEqual(report["contradiction_status"], "CONTRADICTORY_OR_QUALIFYING_EVIDENCE_IDENTIFIED")
        self.assertEqual(report["total_negative_findings"], 1)

    def test_09_missing_metadata_never_low_risk(self):
        """Test 9: NOT_REPORTED is never mapped to LOW_RISK."""
        rob = {"overall_rob": "NOT_REPORTED"}
        self.assertNotEqual(rob["overall_rob"], "LOW_RISK")

    def test_10_unsupported_claim_detected(self):
        """Test 10: Claim with zero supporting facts is labeled UNSUPPORTED."""
        study = {"study_id": "S_EMPTY", "study_design": "IN_VITRO_EXPERIMENTAL"}
        res = GenericClaimEntailmentEngine.evaluate_claim_entailment(
            "CLM_UNSUPPORTED", "The drug completely cures advanced disease.", study, []
        )
        self.assertEqual(res["entailment_status"], "UNSUPPORTED")

    def test_11_causal_overclaim_detection(self):
        """Test 11: Causal verb from observational design triggers overclaim flag."""
        study = {"study_id": "S_OBS", "study_design": "OBSERVATIONAL_COHORT_CASE_CONTROL"}
        facts = [{"directness": "DIRECT_EVIDENCE", "text_or_data": "Odds ratio 1.8 for disease association."}]
        res = GenericClaimEntailmentEngine.evaluate_claim_entailment(
            "CLM_CAUSAL", "Factor X causes severe cardiac fibrosis in adults.", study, facts
        )
        self.assertIsNotNone(res["causal_overclaim_warning"])
        self.assertEqual(res["causal_overclaim_warning"]["flag"], "OVERCLAIM_CAUSAL_INFERENCE_FROM_OBSERVATIONAL_DATA")

    def test_12_numerical_hallucination_detection(self):
        """Test 12: Ungrounded numerical quantity in claim triggers hallucination risk."""
        study = {"study_id": "S_VITRO", "study_design": "IN_VITRO_EXPERIMENTAL"}
        facts = [{"directness": "DIRECT_EVIDENCE", "text_or_data": "IC50 was measured at 25 uM."}]
        # Claim claims 98.5% which is nowhere in the fact text!
        res = GenericClaimEntailmentEngine.evaluate_claim_entailment(
            "CLM_NUM", "Treatment achieves 98.5% viability inhibition at 25 uM.", study, facts
        )
        self.assertTrue(res["numerical_traceability"]["hallucination_risk"])
        self.assertIn("98.5%", res["numerical_traceability"]["untraced_numbers"])

    def test_13_no_synergy_fallacy_gate(self):
        """Test 13: Claiming synergy from two monotherapy studies triggers SYNERGY_NOT_ESTABLISHED (Point 29)."""
        study = {"study_id": "S_MONO", "study_design": "IN_VITRO_EXPERIMENTAL"}
        facts = [{"directness": "DIRECT_EVIDENCE", "text_or_data": "Agent A shows active monotherapy inhibition."}]
        res = GenericClaimEntailmentEngine.evaluate_claim_entailment(
            "CLM_SYN", "Agent A and Agent B exert strong synergistic cell death.", study, facts
        )
        self.assertEqual(res["synergy_fallacy_audit"]["synergy_status"], "SYNERGY_NOT_ESTABLISHED")

    def test_14_no_evidence_not_evidence_of_no_effect(self):
        """Test 14: Zero literature retrieved cannot be reported as evidence of no effect (Point 28)."""
        res = GenericContradictionEngine.distinguish_no_evidence_vs_no_effect(0, [])
        self.assertEqual(res["epistemic_state"], "NO_EVIDENCE_IDENTIFIED")
        self.assertFalse(res["is_evidence_of_no_effect"])

    def test_15_proposal_structure_drift_gate(self):
        """Test 15: Omitting a mandatory proposal section triggers FAIL in validator (Point 15)."""
        from proposal_structure_validator import ProposalStructureValidator
        # Defective proposal omitting section 10 (دستاوردها)
        defective_text = "## 1. موضوع\n## 2. بیان مسئله\n## 11. جدول متغیرها\n| متغیر |\n"
        val = ProposalStructureValidator.validate_proposal_text(defective_text)
        self.assertEqual(val["PROPOSAL_STRUCTURE_VALIDATION"], "FAIL")
        self.assertIn("دستاوردها", val["missing_sections"])

    def test_16_data_provenance_traceability(self):
        """Test 16: Granular source location tracking in data provenance (Point 26)."""
        record_with_loc = {"study_id": "S_01", "source_location": {"page": 142, "table": "Table 2"}}
        record_without_loc = {"study_id": "S_02", "source_location": {}}
        aud1 = GenericClaimEntailmentEngine.audit_data_provenance(record_with_loc)
        aud2 = GenericClaimEntailmentEngine.audit_data_provenance(record_without_loc)
        self.assertTrue(aud1["is_provenance_traceable"])
        self.assertFalse(aud2["is_provenance_traceable"])


if __name__ == "__main__":
    unittest.main()

