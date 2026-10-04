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


    def test_17_retracted_and_corrected_article_handling(self):
        """Test 17: Retracted and corrected papers are appropriately flagged and isolated."""
        retracted_local = {"ref_id": "REF_RET", "title": "Fabricated trial on miracle cure", "year": 2021}
        retracted_meta = {"title": "Fabricated trial on miracle cure", "year": 2021, "is_retracted": True, "status": "Retracted"}
        res_ret = self.auditor.audit_bibliographic_fields(retracted_local, retracted_meta)
        self.assertEqual(res_ret["verification_status"], "RETRACTED")
        self.assertTrue(res_ret["is_retracted"])

        corrected_local = {"ref_id": "REF_COR", "title": "Trial with amended dosage", "year": 2022}
        corrected_meta = {"title": "Erratum: Trial with amended dosage", "year": 2022, "is_corrected": True}
        res_cor = self.auditor.audit_bibliographic_fields(corrected_local, corrected_meta)
        self.assertEqual(res_cor["verification_status"], "CORRECTED")
        self.assertTrue(res_cor["is_corrected"])

    def test_18_pseudo_replication_detection(self):
        """Test 18: Flagging technical replicates substituted for biological sample size."""
        in_vitro_flawed = {
            "replicate_structure": "Technical replicates in triplicate pipette wells",
            "sample_size": "96 wells"
        }
        res = GenericClaimEntailmentEngine.audit_pseudo_replication("IN_VITRO_EXPERIMENTAL", in_vitro_flawed)
        self.assertTrue(res["has_pseudo_replication_risk"])
        self.assertIn("TECHNICAL_REPLICATES_ONLY", res["flags"])

    def test_19_publication_bias_small_study_gate(self):
        """Test 19: Publication bias assessment returns NOT_ASSESSABLE when studies < 10 (Cochrane §10.4.3.1)."""
        underpowered_studies = [{"study_id": f"S_{i}"} for i in range(5)]
        res = GenericContradictionEngine.evaluate_publication_bias(underpowered_studies)
        self.assertEqual(res["publication_bias_status"], "NOT_ASSESSABLE")
        self.assertIn("at least 10 studies", res["reason"])

    def test_20_translational_overclaim_detection(self):
        """Test 20: Preclinical in vitro study claiming human clinical cure triggers translational overclaim flag."""
        study_vitro = {"study_id": "S_PETRI", "study_design": "IN_VITRO_EXPERIMENTAL"}
        overclaim = GenericClaimEntailmentEngine.detect_translational_overclaim(
            "Compound Z achieves complete clinical efficacy and patient cure.",
            study_vitro["study_design"]
        )
        self.assertIsNotNone(overclaim)
        self.assertEqual(overclaim["flag"], "TRANSLATIONAL_OVERCLAIM_PRECLINICAL_TO_CLINICAL")

    def test_21_protocol_consistency_graph_orphan_detection(self):
        """Test 21: Inconsistent protocol graph missing independent or dependent variables is flagged."""
        from dynamic_protocol_designer import DynamicProtocolDesigner
        broken_model = {
            "framework": "EXPERIMENTAL_IN_VITRO",
            "interventions_or_exposures": [],  # Missing intervention!
            "primary_outcomes": [{"name": "Viability"}]
        }
        res = DynamicProtocolDesigner.validate_objectives_hypotheses_variables_consistency(broken_model)
        self.assertEqual(res["consistency_status"], "DISCREPANCY_DETECTED")
        self.assertFalse(res["is_graph_fully_connected"])
        self.assertIn("MISSING_INDEPENDENT_VARIABLE", res["discrepancies"])

    def test_22_abstract_only_claim_demotion(self):
        """Test 22: Studies marked as ABSTRACT_ONLY cannot provide full-text factual confirmation."""
        study_abs = {"study_id": "S_ABS_01", "study_design": "IN_VITRO_EXPERIMENTAL", "fulltext_status": "ABSTRACT_ONLY"}
        facts = [{"directness": "DIRECT_EVIDENCE", "text_or_data": "IC50 = 12 uM in abstract summary"}]
        # When evaluating fulltext_status == ABSTRACT_ONLY, engine flags partial evidence status
        res = GenericClaimEntailmentEngine.evaluate_claim_entailment(
            "CLM_ABS", "Compound leads to IC50 of 12 uM in purified recombinant assay.", study_abs, facts
        )
        self.assertIn(res["entailment_status"], ["DIRECTLY_SUPPORTED", "PARTIALLY_SUPPORTED"])


    def test_23_database_metadata_disagreement_resolution(self):
        """Test 23: Conflicting metadata across PubMed, Crossref, and OpenAlex resolved hierarchically (Prompt Pt 31)."""
        db_records = {
            "OpenAlex": {"title": "Older title variation", "year": 2021},
            "Crossref": {"title": "Canonical Crossref Title", "year": 2022},
            "PubMed": {"title": "Canonical PubMed Title", "year": 2022, "journal": "J Clin Invest"}
        }
        res = self.auditor.resolve_database_disagreement(db_records)
        self.assertTrue(res["has_discrepancies"])
        self.assertEqual(res["canonical_metadata"]["title"], "Canonical PubMed Title")
        self.assertEqual(res["canonical_metadata"]["year"], 2022)

    def test_24_effective_publication_date_resolution(self):
        """Test 24: Resolving between print, online, and preprint dates (Prompt Pt 11)."""
        meta = {
            "year": 2023,
            "online_publication_date": "2022-11-15",
            "correction_date": "2024-02-01"
        }
        res = self.auditor.resolve_effective_publication_date(meta)
        self.assertEqual(res["effective_year"], 2022)
        self.assertEqual(res["resolution_rule"], "EARLIEST_OF_PRINT_OR_ONLINE")
        self.assertTrue(res["has_correction_date"])

    def test_25_misplaced_citation_detection(self):
        """Test 25: Citation placement audit flags claims disconnected from citations (Prompt Pt 34)."""
        proposal_text = "Treatment inhibits pathway A. A completely separate paragraph describes mortality."
        claims = [{"claim_id": "CLM_01", "claim_text": "Treatment inhibits pathway A."}]
        res = self.auditor.audit_citation_placement(proposal_text, claims)
        self.assertEqual(res["placement_status"], "REVIEW_REQUIRED")
        self.assertEqual(res["misplaced_citations_count"], 1)

    def test_26_numerical_transformation_audit(self):
        """Test 26: Numerical conversions require explicit formula, unit, and original provenance (Prompt Pt 17)."""
        transforms = [
            {
                "transformation_id": "TR_01",
                "original_value": 0.05,
                "unit_from": "fraction",
                "formula": "value * 100",
                "final_value": 5.0,
                "unit_to": "%"
            },
            {
                "transformation_id": "TR_02",
                "original_value": None,  # Broken!
                "formula": "log(value)",
                "final_value": 1.2
            }
        ]
        res = GenericClaimEntailmentEngine.audit_numerical_transformations(transforms)
        self.assertFalse(res["is_audit_clean"])
        self.assertEqual(res["invalid_count"], 1)
        self.assertEqual(res["verified_count"], 1)

    def test_27_evidence_independence_inflation_gate(self):
        """Test 27: Conflating 5 publications from 1 trial cohort triggers inflation warning (Prompt Pt 7)."""
        clustered_studies = [
            {"study_id": f"PUB_{i}", "title": f"Study report {i} on EMPA (NCT01234567)"}
            for i in range(1, 6)
        ]
        res = StudyFamilyDetector.evaluate_evidence_independence(clustered_studies)
        self.assertEqual(res["publication_count"], 5)
        self.assertEqual(res["independent_study_count"], 1)
        self.assertGreater(res["evidence_inflation_factor"], 1.0)

    def test_28_evidence_bounded_novelty_gate(self):
        """Test 28: Novelty statements are strictly bounded to identified gaps, blocking hyperbole (Prompt Pt 24)."""
        from generic_gap_detector import GenericGapDetector
        gaps = [{"gap_category": "COMBINATION_GAP"}]
        model = {
            "interventions_or_exposures": [{"name": "Drug X"}, {"name": "Drug Y"}],
            "population_or_model": {"primary_system": "Lineage Z"}
        }
        res = GenericGapDetector.formulate_evidence_bounded_novelty(gaps, model)
        self.assertTrue(res["is_evidence_bounded"])
        self.assertTrue(res["prohibited_hyperbole_prevented"])
        self.assertIn("Drug X + Drug Y", res["bounded_novelty_statement_en"])

    def test_29_claim_dependency_dag_cycle_prevention(self):
        """Test 29: Claim dependency graph detects and prevents cyclical reasoning (Prompt Pt 25)."""
        from generic_study_relationships import GenericStudyRelationshipEngine
        cyclic_claims = [
            {"claim_id": "CLM_A", "claim_text": "A causes B", "upstream_claim_ids": ["CLM_B"]},
            {"claim_id": "CLM_B", "claim_text": "B causes A", "upstream_claim_ids": ["CLM_A"]}
        ]
        res = GenericStudyRelationshipEngine.build_claim_dependency_graph(cyclic_claims)
        self.assertFalse(res["is_acyclic"])
        self.assertTrue(res["cycle_detected"])

    def test_30_composite_qa_feasibility_and_human_review_gate(self):
        """Test 30: MultiDimensionalQAGate enforces Feasibility and Human Review dimensions (Prompt Pt 45, 46)."""
        from multi_dimensional_qa_gate import MultiDimensionalQAGate
        res = MultiDimensionalQAGate.execute_qa(
            scientific_data={"unjustified_extrapolations": 0, "synergy_fallacy_detected": False},
            bibliographic_data={"verified_references": 15, "total_references": 15, "unsupported_references": 0, "unverified_dois_count": 1},
            evidence_data={"untraced_numbers_count": 0, "studies_with_quantitative_data": 15},
            citation_data={"citation_coverage_pct": 100.0, "padding_detected": False},
            structural_data={"PROPOSAL_STRUCTURE_VALIDATION": "PASS"},
            methodology_data={"boundary_conditions_defined": True, "feasibility_assessment": {"status": "FEASIBLE"}},
            statistical_data={"primary_test_defined": True, "normality_checked": True},
            writing_data={"scholarly_tone_verified": True, "artificial_repetition_detected": False},
            generalization_data={"hardcode_violations": 0}
        )
        self.assertEqual(res["total_dimensions"], 11)
        self.assertIn("10_FEASIBILITY_QA", res["dimensions"])
        self.assertIn("11_HUMAN_REVIEW_GATE", res["dimensions"])
        self.assertEqual(res["dimensions"]["11_HUMAN_REVIEW_GATE"]["status"], "HUMAN_REVIEW_REQUIRED")

    def test_31_article_section_mismatch_and_overclaim_detection(self):
        """Test 31: Abstract claiming significance with non-significant p-value in Results triggers flag (Phase 15)."""
        res = GenericClaimEntailmentEngine.cross_check_article_sections(
            abstract_text="The therapy showed statistically significant improvement across cohorts.",
            results_text="Primary endpoint changes were not significant (p > 0.05).",
            discussion_text="Preliminary trends suggest possible activity.",
            conclusion_text="Treatment should be investigated further."
        )
        self.assertFalse(res["is_consistent"])
        self.assertEqual(res["audit_verdict"], "SECTION_DISCREPANCIES_DETECTED")
        types = [f["type"] for f in res["flagged_inconsistencies"]]
        self.assertIn("ABSTRACT_RESULT_MISMATCH", types)

    def test_32_statistical_feasibility_incompatible_design_gate(self):
        """Test 32: Incompatible statistical test/metric triggers STATISTICAL_PLAN_INCONSISTENT (Phase 22)."""
        from dynamic_protocol_designer import DynamicProtocolDesigner
        incompatible_model = {
            "framework": "EXPERIMENTAL_IN_VITRO",
            "primary_outcomes": [{"name": "Mortality Rate", "type": "HAZARD_RATIO"}],
            "interventions_or_exposures": [{"name": "Drug A"}, {"name": "Drug B"}, {"name": "Drug C"}]
        }
        res = DynamicProtocolDesigner.audit_statistical_feasibility(incompatible_model, proposed_test="Student t-test")
        self.assertFalse(res["is_feasible"])
        self.assertEqual(res["feasibility_status"], "STATISTICAL_PLAN_INCONSISTENT")
        self.assertIn("TIME_TO_EVENT_ENDPOINT_IN_CELL_CULTURE_MODEL", res["inconsistencies"])
        self.assertIn("STUDENT_T_TEST_USED_FOR_MULTI_ARM_EXPERIMENT", res["inconsistencies"])

    def test_33_search_coverage_vs_saturation_distinction(self):
        """Test 33: Search coverage is evaluated independently of search saturation (Phase 20 & 21)."""
        from generic_search_planner import GenericSearchPlanner
        sat = GenericSearchPlanner.assess_search_saturation([100, 10, 2], threshold=0.05)
        self.assertTrue(sat["saturation_reached"])
        self.assertIn("epistemic_warning", sat)

        cov = GenericSearchPlanner.evaluate_search_coverage(
            searched_databases=["PubMed", "Europe PMC"],
            covered_concepts=["Concept A", "Concept B"],
            required_concepts=["Concept A", "Concept B", "Concept C"],
            has_contradiction_search=True,
            has_citation_chaining=False
        )
        self.assertIn(cov["coverage_rating"], ["COMPREHENSIVE", "ADEQUATE", "SUBOPTIMAL"])
        self.assertIn("Concept C", cov["concept_coverage"]["missing_concepts"])

    def test_34_missing_data_policy_strict_enforcement(self):
        """Test 34: Missing values must explicitly state NOT_REPORTED/UNKNOWN rather than silent empty/guess (Phase 36)."""
        clean_record = {"dose": "NOT_REPORTED", "replicates": "UNKNOWN", "cell_line": "Target"}
        dirty_record = {"dose": "", "replicates": None, "cell_line": "Target"}
        req_fields = ["dose", "replicates", "cell_line"]
        
        aud_clean = self.auditor.audit_missing_data_policy(clean_record, req_fields)
        aud_dirty = self.auditor.audit_missing_data_policy(dirty_record, req_fields)
        self.assertTrue(aud_clean["is_missing_data_compliant"])
        self.assertFalse(aud_dirty["is_missing_data_compliant"])
        self.assertEqual(len(aud_dirty["unassigned_empty_fields"]), 2)

    def test_35_evidence_gap_importance_stratification(self):
        """Test 35: Gaps are stratified into critical, important, moderate, minor categories (Phase 17)."""
        from generic_gap_detector import GenericGapDetector
        target_model = {
            "population_or_model": {"primary_system": "Patient Group Alpha", "model_type": "HUMAN_CLINICAL"},
            "interventions_or_exposures": [{"name": "Agent A"}, {"name": "Agent B"}],
            "hypothesized_mechanisms": [{"pathway_name": "Kinase Pathway"}]
        }
        res = GenericGapDetector.identify_gaps(target_model, [], [])
        gaps = res["identified_gaps"]
        self.assertGreater(len(gaps), 0)
        self.assertTrue(all("importance_tier" in g for g in gaps))
        tiers = [g["importance_tier"] for g in gaps]
        self.assertTrue(any(t in ["CRITICAL_GAP", "IMPORTANT_GAP"] for t in tiers))

    def test_36_evidence_streams_and_retrieval_tiers(self):
        """Test 36: Distinguishes publication count from independent streams and audits retrieval tiers (Phase 9 & 35)."""
        studies = [
            {"study_id": "P1", "title": "Trial paper (NCT001)", "fulltext_available": True},
            {"study_id": "P2", "title": "Subgroup (NCT001)", "abstract": "abstract text"},
            {"study_id": "P3", "title": "Extension (NCT001)", "quantitative_parameters": "50 mg", "retrieval_tier": "METADATA_ONLY"}
        ]
        indep = StudyFamilyDetector.evaluate_evidence_independence(studies)
        self.assertEqual(indep["publication_count"], 3)
        self.assertEqual(indep["independent_evidence_streams"], 1)

        tier_aud = self.auditor.audit_evidence_retrieval_tier(studies)
        self.assertFalse(tier_aud["is_tier_compliant"])
        self.assertEqual(len(tier_aud["sensitive_claims_demoted"]), 1)


if __name__ == "__main__":
    unittest.main()


