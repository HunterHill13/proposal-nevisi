#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_v87_remediation_regressions.py
Proposal-Nevisi v8.7.0 Remediation Regression Test Suite.

Verifies complete remediation of Real-World Evidence Audit failure modes (FAIL_01 through FAIL_09):
- Test A: Off-target intervention hard-reject in screening and contextual relevance (FAIL_01 to FAIL_04).
- Test B: Derivative/analogue vs pure compound boundary enforcement (FAIL_06).
- Test C: Extract/mixture vs pure constituent boundary enforcement (FAIL_07).
- Test D: Non-human / murine model mismatch vs human target model (FAIL_08).
- Test E: No-quota-filling policy allows justified under-quota reference portfolios without fake padding (FAIL_09).
- Test F: Fail-closed template placeholder sanitization gate blocks leaked tokens (FAIL_05).
- Test G: Multi-claim sentence atomization prevents citation conflation.
- Test H: Numeric provenance gate partitions PROTOCOL_DESIGN from SOURCE_DERIVED numbers.
- Test I: Search recall preserves foundational landmark methods across temporal windows.
- Test J: Direct combination absence reported with bounded epistemic phrase.

100% Topic-Agnostic and Domain-General: Uses synthetic generic models and entities.
"""

import os
import sys
import unittest
from typing import Dict, Any, List

scripts_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, os.path.abspath(scripts_dir))

from core_policies import (
    MAX_FINAL_REFERENCES, MIN_FINAL_REFERENCES, NO_QUOTA_FILLING,
    BOUNDED_SEARCH_GAP_STATUSES, NUMERIC_PROVENANCE_CATEGORIES,
    ENTITY_TYPE_HIERARCHY, CONTEXTUAL_BOUNDARY_MISMATCHES
)
from generic_reference_auditor import (
    GenericReferenceAuditor, ContextualBoundaryGate, NumericProvenanceGate,
    ExactClaimEvidenceMapper, MultiClaimAtomizer, FinalTextSanitizationGate,
    EvidenceDrivenParagraphBuilder, CanonicalPaperEvidenceRecord
)
from scientific_search_adapter import ScientificSearchAdapter


class TestV87RemediationRegressions(unittest.TestCase):
    """Regression test suite validating architectural fixes for FAIL_01 through FAIL_09."""

    def setUp(self):
        self.generic_problem_model = {
            "model_id": "RPM_SYNTH_ONCOLOGY_001",
            "domain": "oncology",
            "framework": "PICO",
            "interventions_or_exposures": [
                {"name": "Agent-Alpha", "entity_type": "SMALL_MOLECULE"},
                {"name": "Platform-Beta", "entity_type": "BIOLOGIC_VECTOR"}
            ],
            "population_or_model": {
                "primary_system": "Human Adenocarcinoma Cell Line",
                "cell_lines": ["Cell-Human-Lung-01"]
            },
            "primary_outcomes": [
                {"name": "Cell Viability Suppression", "measurement_method": "Colorimetric bioassay"}
            ],
            "target_condition": {
                "name_en": "Target Neoplasm",
                "name_fa": "بدخیمی هدف"
            }
        }

    def test_case_a_off_target_intervention_hard_reject(self):
        """Test A (FAIL_01 to FAIL_04): Off-target intervention candidate paper is HARD-REJECTED.
        When target intervention is Agent-Alpha, candidate evaluating OffTarget-Compound-Omega
        must be hard-rejected in Stage 1 screening and contextual relevance with WRONG_INTERVENTION.
        """
        off_target_paper = {
            "ref_id": "REF_OFF_TARGET_01",
            "title": "Cytotoxicity of OffTarget-Compound-Omega in Cell-Human-Lung-01",
            "abstract": "We investigated the cytotoxic effects of OffTarget-Compound-Omega in human cells.",
            "intervention_agent": "OffTarget-Compound-Omega",
            "model_system": "Cell-Human-Lung-01",
            "year": 2024
        }

        # 1. ScientificSearchAdapter Stage 1 screening check
        screen_res = ScientificSearchAdapter.screen_two_stage([off_target_paper], self.generic_problem_model)
        self.assertEqual(screen_res["stage_1_passed"], 0)
        self.assertEqual(len(screen_res["stage_1_excluded"]), 1)
        self.assertEqual(screen_res["stage_1_excluded"][0]["exclusion_code"], "WRONG_INTERVENTION")

        # 2. GenericReferenceAuditor contextual relevance check
        rel_audit = GenericReferenceAuditor.audit_contextual_relevance(off_target_paper, self.generic_problem_model)
        self.assertFalse(rel_audit["is_contextually_relevant"])
        self.assertEqual(rel_audit["relevance_tier"], "IRRELEVANT")
        self.assertEqual(rel_audit["rejection_category"], "WRONG_INTERVENTION")

        # 3. ContextualBoundaryGate intervention mismatch check
        claim = {
            "claim_id": "CLM_OFF_01",
            "claim_text": "Agent-Alpha significantly suppresses target cellular growth.",
            "claim_entity": "Agent-Alpha"
        }
        boundary_res = ContextualBoundaryGate.audit_context_boundaries(claim, off_target_paper, self.generic_problem_model)
        self.assertIn("INTERVENTION_MISMATCH", boundary_res["mismatches"])

    def test_case_b_derivative_analogue_not_pure_compound(self):
        """Test B (FAIL_06): Semi-synthetic derivative must not be conflated with pure compound.
        Contextual boundary gate flags FORMULATION_MISMATCH, and paragraph builder qualifies derivative.
        """
        derivative_paper = {
            "ref_id": "REF_DERIVATIVE_01",
            "title": "Synthesis and evaluation of Agent-Alpha C-3 Ester Derivatives",
            "abstract": "Novel synthetic derivative analogues based on Agent-Alpha showed enhanced potency.",
            "intervention_agent": "Agent-Alpha Synthetic Ester Derivative",
            "model_system": "Cell-Human-Lung-01",
            "intervention_or_exposure": {"entity_granularity": "DERIVATIVE"},
            "year": 2024,
            "authors": ["Chemist A", "Biologist B"]
        }

        # Boundary gate check when claim asserts unmodified natural parent compound
        claim = {
            "claim_id": "CLM_DERIV_01",
            "claim_text": "Natural pure parent Agent-Alpha directly exhibits potent activity.",
            "claim_entity": "natural parent agent-alpha"
        }
        boundary_res = ContextualBoundaryGate.audit_context_boundaries(claim, derivative_paper, self.generic_problem_model)
        self.assertIn("FORMULATION_MISMATCH", boundary_res["mismatches"])

        # Paragraph builder must explicitly qualify the derivative nature
        para = EvidenceDrivenParagraphBuilder.build_literature_paragraph(derivative_paper, citation_number=1, problem_model=self.generic_problem_model)
        self.assertIn("مشتق شیمیایی سنتزشده / آنالوگ ساختاری", para)

    def test_case_c_extract_mixture_not_pure_constituent(self):
        """Test C (FAIL_07): Botanical crude extract must not be conflated with pure isolated constituent.
        Contextual boundary gate flags FORMULATION_MISMATCH, and paragraph builder qualifies extract.
        """
        extract_paper = {
            "ref_id": "REF_EXTRACT_01",
            "title": "Ethanolic botanical extract of Plant-Flora containing Agent-Alpha traces",
            "abstract": "Crude plant extract of Plant-Flora exhibited bioactivity in cell assays.",
            "intervention_agent": "Crude Plant Extract",
            "model_system": "Cell-Human-Lung-01",
            "intervention_or_exposure": {"entity_granularity": "EXTRACT"},
            "year": 2024,
            "authors": ["Botanist C"]
        }

        claim = {
            "claim_id": "CLM_EXTR_01",
            "claim_text": "Pure isolated Agent-Alpha directly causes cellular inhibition as a single agent.",
            "claim_entity": "pure constituent agent-alpha"
        }
        boundary_res = ContextualBoundaryGate.audit_context_boundaries(claim, extract_paper, self.generic_problem_model)
        self.assertIn("FORMULATION_MISMATCH", boundary_res["mismatches"])

        para = EvidenceDrivenParagraphBuilder.build_literature_paragraph(extract_paper, citation_number=2, problem_model=self.generic_problem_model)
        self.assertIn("عصاره تام", para)

    def test_case_d_model_mismatch_murine_vs_human_nsclc(self):
        """Test D (FAIL_08): Murine / mouse model must not be attributed to human target model without qualification.
        Contextual boundary gate flags MODEL_MISMATCH and SPECIES_MISMATCH.
        """
        murine_paper = {
            "ref_id": "REF_MURINE_01",
            "title": "Evaluation of Agent-Alpha in murine TC-1 cells",
            "abstract": "Agent-Alpha inhibited progression in murine mouse TC-1 cell model.",
            "intervention_agent": "Agent-Alpha",
            "model_system": "murine mouse TC-1 cell line",
            "year": 2024
        }

        # Claim claims effect in target human system without mentioning mouse/TC-1
        claim = {
            "claim_id": "CLM_MURINE_01",
            "claim_text": "Agent-Alpha effectively suppresses human adenocarcinoma cells [1].",
            "claim_model": "human adenocarcinoma"
        }
        boundary_res = ContextualBoundaryGate.audit_context_boundaries(claim, murine_paper, self.generic_problem_model)
        self.assertIn("MODEL_MISMATCH", boundary_res["mismatches"])
        self.assertIn("SPECIES_MISMATCH", boundary_res["mismatches"])

    def test_case_e_no_quota_filling_under_floor_acceptance(self):
        """Test E (FAIL_09): With NO_QUOTA_FILLING active, an under-quota portfolio (e.g. 7 valid refs)
        is accepted without forced padding or failure.
        """
        valid_seven_refs = [
            {
                "citation_number": idx,
                "ref_id": f"REF_VALID_{idx:02d}",
                "title": f"Empirical Study {idx} on Target System",
                "authors": [f"Author {idx}"],
                "year": 2024,
                "final_inclusion_reason": "INTERVENTION_EFFICACY_EVIDENCE",
                "proposal_section_supported": ["SECTION_3_LITERATURE_REVIEW"],
                "why_this_paper_is_needed": "Provides empirical benchmark data."
            }
            for idx in range(1, 8)
        ]

        # Audit portfolio under NO_QUOTA_FILLING
        audit_res = GenericReferenceAuditor.audit_final_reference_portfolio(
            references=valid_seven_refs,
            max_references=MAX_FINAL_REFERENCES,
            min_references=MIN_FINAL_REFERENCES,
            allow_under_quota_if_justified=True,
            no_quota_filling=True
        )

        self.assertEqual(audit_res["portfolio_status"], "PASS")
        self.assertEqual(audit_res["total_references"], 7)
        self.assertEqual(len(audit_res["violations"]), 0)

    def test_case_f_placeholder_leakage_blocks_release_and_sanitizes(self):
        """Test F (FAIL_05): FinalTextSanitizationGate blocks release when Persian template placeholders
        or code placeholders are present, and approves release after sanitization.
        """
        dirty_text = (
            "در این بخش اثرات **عامل مداخله** بر روی **مدل بیولوژیک** بررسی شده است. "
            "همچنین مقایسه با گروه کنترل استاندارد انجام شد [?]. TODO: بررسی نهایی."
        )

        # 1. Scan must fail-closed
        scan_dirty = FinalTextSanitizationGate.scan_text(dirty_text)
        self.assertFalse(scan_dirty["is_clean"])
        self.assertEqual(scan_dirty["release_verdict"], "RELEASE_BLOCKED")
        self.assertGreater(scan_dirty["placeholder_count"], 0)

        # 2. Sanitize must clean the text
        clean_text = FinalTextSanitizationGate.sanitize_text(dirty_text)
        scan_clean = FinalTextSanitizationGate.scan_text(clean_text)
        self.assertTrue(scan_clean["is_clean"])
        self.assertEqual(scan_clean["release_verdict"], "RELEASE_APPROVED")
        self.assertEqual(scan_clean["placeholder_count"], 0)

    def test_case_g_multi_claim_sentence_atomization(self):
        """Test G: MultiClaimAtomizer decomposes compound sentences into atomic assertions.
        When Claim 1 is supported and Claim 2 is unsupported, verdict is PARTIALLY_SUPPORTED
        and citation is flagged as NOT valid for all claims.
        """
        compound_sentence = (
            "Agent-Alpha in vitro significantly reduced cell viability by 45% [1], "
            "and completely eradicated metastatic tumor progression in vivo [1]."
        )
        # Source paper only examined in vitro cell viability and reports 45%
        in_vitro_paper = {
            "ref_id": "REF_VITRO_01",
            "title": "In vitro evaluation of Agent-Alpha",
            "abstract": "Agent-Alpha reduced cell viability by 45% in vitro. In vivo assays were not conducted.",
            "primary_findings": "Cell viability decreased by 45%.",
            "study_design": "IN_VITRO_EXPERIMENTAL",
            "quantitative_parameters": "45%",
            "intervention_agent": "Agent-Alpha"
        }

        atom_res = MultiClaimAtomizer.verify_compound_sentence(
            sentence=compound_sentence,
            paper_record=in_vitro_paper,
            problem_model=self.generic_problem_model
        )

        self.assertGreaterEqual(atom_res["total_atoms"], 2)
        self.assertEqual(atom_res["composite_verdict"], "PARTIALLY_SUPPORTED")
        self.assertFalse(atom_res["all_atoms_supported"])
        self.assertFalse(atom_res["citation_valid_for_all_claims"])

    def test_case_h_numeric_provenance_protocol_design_vs_source_derived(self):
        """Test H: NumericProvenanceGate partitions prospective PROTOCOL_DESIGN values from retrospective
        empirical SOURCE_DERIVED numbers.
        """
        dummy_paper = {
            "ref_id": "REF_DUMMY",
            "abstract": "Agent-Alpha demonstrated qualitative changes without concentration titration.",
            "primary_findings": "Qualitative changes only.",
            "quantitative_parameters": ""
        }

        # 1. Prospective protocol design parameters (e.g. proposed treatment duration and concentrations)
        protocol_claim = {
            "claim_id": "CLM_PROTO_01",
            "claim_text": "The cells will be treated for 48 h with concentrations of 10, 20, and 40 uM."
        }
        res_proto = NumericProvenanceGate.audit_claim_numbers(
            claim_text=protocol_claim,
            paper_record=dummy_paper,
            provenance_category="PROTOCOL_DESIGN"
        )
        self.assertTrue(res_proto["is_verified"])
        self.assertEqual(res_proto["provenance_category"], "PROTOCOL_DESIGN")
        self.assertEqual(res_proto["numeric_status"], "PROTOCOL_DESIGN")

        # 2. Retrospective empirical claim with missing numbers
        empirical_claim = {
            "claim_id": "CLM_EMP_01",
            "claim_text": "Agent-Alpha exhibited an IC50 of 28.5 uM in cell assays."
        }
        res_emp = NumericProvenanceGate.audit_claim_numbers(
            claim_text=empirical_claim,
            paper_record=dummy_paper,
            provenance_category="SOURCE_DERIVED"
        )
        self.assertFalse(res_emp["is_verified"])
        self.assertEqual(res_emp["numeric_status"], "NOT_REPORTED")
        self.assertIn(28.5, res_emp["unverified_values"])

    def test_case_i_search_recall_preserves_landmark_methods_across_time(self):
        """Test I: Layer B Foundational/Landmark exemption allows methodology papers older than 6 years
        to bypass the temporal recency cutoff, while unexempted older papers are excluded.
        """
        landmark_paper = {
            "ref_id": "REF_CHOU_METHOD",
            "title": "Theoretical basis and equations for median-effect principle",
            "abstract": "Mathematical methodology for drug combination index calculations.",
            "year": 1984,
            "foundational_justification": {
                "is_justified": True,
                "category": "FOUNDATIONAL_MATHEMATICAL_MODEL",
                "rationale": "Seminal citation defining synergy formulas."
            },
            "is_methodological_landmark": True
        }

        unexempted_old_paper = {
            "ref_id": "REF_OLD_GENERIC",
            "title": "Agent-Alpha suppresses Target Neoplasm in Cell-Human-Lung-01",
            "abstract": "Agent-Alpha was tested in Cell-Human-Lung-01 target neoplasm cells.",
            "intervention_agent": "Agent-Alpha",
            "model_system": "Cell-Human-Lung-01",
            "year": 1995
        }

        screen_res = ScientificSearchAdapter.screen_two_stage(
            corpus=[landmark_paper, unexempted_old_paper],
            problem_model=self.generic_problem_model
        )

        # Landmark paper must pass Stage 2
        passed_ids = [r.get("ref_id") for r in screen_res["final_eligible_records"]]
        self.assertIn("REF_CHOU_METHOD", passed_ids)

        # Unexempted old paper must be excluded with OUTDATED_DIRECT_EVIDENCE
        excluded_ids = [r.get("ref_id") for r in screen_res["stage_2_excluded"]]
        self.assertIn("REF_OLD_GENERIC", excluded_ids)
        exc_entry = next(r for r in screen_res["stage_2_excluded"] if r.get("ref_id") == "REF_OLD_GENERIC")
        self.assertEqual(exc_entry["exclusion_code"], "OUTDATED_DIRECT_EVIDENCE")

    def test_case_j_direct_combination_absence_bounded_epistemic_reporting(self):
        """Test J: When no direct co-treatment study exists between Agent-Alpha and Platform-Beta,
        the epistemic gap is bounded by NO_DIRECT_STUDY_IDENTIFIED_IN_SEARCHED_SOURCES.
        """
        self.assertIn("NO_DIRECT_STUDY_IDENTIFIED_IN_SEARCHED_SOURCES", BOUNDED_SEARCH_GAP_STATUSES)
        self.assertNotIn("NO_DIRECT_STUDY_EXISTS", BOUNDED_SEARCH_GAP_STATUSES)

        monotherapy_paper = {
            "ref_id": "REF_MONO_01",
            "title": "Monotherapy evaluation of Agent-Alpha",
            "abstract": "Agent-Alpha alone was evaluated; no combinations tested.",
            "intervention_agent": "Agent-Alpha",
            "model_system": "Cell-Human-Lung-01",
            "year": 2024
        }
        gates = GenericReferenceAuditor.audit_scientific_evidence_gates(monotherapy_paper, self.generic_problem_model)
        self.assertEqual(gates["synergy_evidence"], "MONOTHERAPY_ONLY")


if __name__ == "__main__":
    unittest.main()
