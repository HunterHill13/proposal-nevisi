#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_v87_evidence_grounding_and_attribution.py
Proposal-Nevisi v8.7.0 Evidence Grounding, Context Boundary & Attribution Test Suite.

Validates:
  - Cases A through J: Adversarial test cases preventing semantic evidence attribution errors.
  - Case K: Draft-07 schema compliance for Canonical Paper Evidence Record.
  - Case L: Draft-07 schema compliance for Claim-to-Evidence Unit Mapping.
  - Case M: Synthetic End-to-End research problem with deliberately incompatible papers.
  - Case N: Core architecture invariants.

Zero domain leakage: Uses synthetic generic test models (Model-Alpha, Compound-X, etc.).
"""

import os
import sys
import json
import unittest

scripts_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, os.path.abspath(scripts_dir))

from core_policies import (
    MAX_FINAL_REFERENCES, NO_QUOTA_FILLING, ENGINE_VERSION,
    CANONICAL_EVIDENCE_RECORD_FIELDS, NUMERIC_PROVENANCE_STATUSES,
    CONTEXTUAL_BOUNDARY_MISMATCHES, FORMULATION_ENTITY_DISTINCTIONS,
    CLAIM_EVIDENCE_VERDICTS
)
from generic_reference_auditor import (
    CanonicalPaperEvidenceRecord, NumericProvenanceGate, ContextualBoundaryGate,
    ExactClaimEvidenceMapper, EvidenceDrivenParagraphBuilder, PostResearchCitationAuditor
)
from schema_validator import SchemaValidator

class TestV87EvidenceGroundingAndAttribution(unittest.TestCase):
    """Test suite for v8.7.0 Evidence Grounding and Semantic Attribution Engine."""

    def setUp(self):
        self.schemas_dir = os.path.join(os.path.dirname(__file__), "..", "schemas")

    def test_case_a_model_mismatch_rejection(self):
        """Case A: Paper evaluates Model-Alpha, claim asserts Model-Beta -> REJECT (MODEL_MISMATCH)."""
        paper = {
            "ref_id": "REF_SYNTH_01",
            "title": "Empirical evaluation of Agent-X in Model-Alpha",
            "abstract": "We investigated Agent-X efficacy exclusively in Model-Alpha systems.",
            "model_system": "Model-Alpha",
            "study_design": "IN_VITRO_EXPERIMENTAL",
            "primary_findings": "Observed cellular modulation in Model-Alpha."
        }
        claim = {
            "claim_id": "CLM_A",
            "claim_text": "Agent-X significantly suppresses pathology in Model-Beta.",
            "claim_model": "Model-Beta"
        }
        res = ExactClaimEvidenceMapper.map_and_verify_claim(claim, paper)
        self.assertEqual(res["verdict"], "NOT_SUPPORTED")
        self.assertFalse(res["is_authorized_for_literature_review"])
        self.assertIn("MODEL_MISMATCH", res["mismatches"])

    def test_case_b_formulation_mixture_vs_pure_rejection(self):
        """Case B: Paper examines natural extract/mixture, claim attributes effect to pure constituent -> REJECT (FORMULATION_MISMATCH)."""
        paper = {
            "ref_id": "REF_SYNTH_02",
            "title": "Activity of botanical crude extract containing Phytochemical-Q",
            "abstract": "The whole botanical ethanolic extract containing Phytochemical-Q showed biological activity.",
            "intervention_agent": "Whole Ethanolic Extract of Plant-Z",
            "study_design": "IN_VITRO_EXPERIMENTAL",
            "primary_findings": "Crude extract demonstrated functional changes."
        }
        claim = {
            "claim_id": "CLM_B",
            "claim_text": "Pure isolated Phytochemical-Q directly inhibits target pathway as a single agent.",
            "claim_entity": "pure isolated phytochemical-q"
        }
        res = ExactClaimEvidenceMapper.map_and_verify_claim(claim, paper)
        self.assertEqual(res["verdict"], "NOT_SUPPORTED")
        self.assertFalse(res["is_authorized_for_literature_review"])
        self.assertIn("FORMULATION_MISMATCH", res["mismatches"])

    def test_case_c_in_silico_computational_leap_rejection(self):
        """Case C: Paper is computational docking, claim asserts experimental wet-lab cell growth inhibition -> REJECT (IN_SILICO_TO_EXPERIMENTAL_LEAP)."""
        paper = {
            "ref_id": "REF_SYNTH_03",
            "title": "Molecular docking and binding dynamics of Ligand-Delta",
            "abstract": "In silico molecular modeling and virtual docking demonstrated strong binding affinity to Receptor-K.",
            "study_design": "COMPUTATIONAL_IN_SILICO",
            "primary_findings": "Virtual docking free energy was calculated as -8.4 kcal/mol."
        }
        claim = {
            "claim_id": "CLM_C",
            "claim_text": "Ligand-Delta in vitro significantly inhibited cell growth in experimental assay."
        }
        res = ExactClaimEvidenceMapper.map_and_verify_claim(claim, paper)
        self.assertEqual(res["verdict"], "NOT_SUPPORTED")
        self.assertFalse(res["is_authorized_for_literature_review"])
        self.assertIn("IN_SILICO_TO_EXPERIMENTAL_LEAP", res["mismatches"])

    def test_case_d_numeric_hallucination_rejection(self):
        """Case D: Paper does not report numeric value, claim invents number -> REJECT (UNGROUNDED_NUMERIC_ASSERTION)."""
        paper = {
            "ref_id": "REF_SYNTH_04",
            "title": "Qualitative observation of Compound-Omega",
            "abstract": "Compound-Omega showed moderate phenotypic alterations without dose-response curve calculation.",
            "primary_findings": "Qualitative phenotypic changes observed.",
            "quantitative_parameters": ""
        }
        claim = {
            "claim_id": "CLM_D",
            "claim_text": "Compound-Omega exhibited an IC50 of 14.8 uM and reduced growth by 65.2%."
        }
        res = ExactClaimEvidenceMapper.map_and_verify_claim(claim, paper)
        self.assertEqual(res["verdict"], "NOT_SUPPORTED")
        self.assertFalse(res["numeric_provenance"]["is_verified"])
        self.assertIn(14.8, res["numeric_provenance"]["claimed_values"])
        self.assertFalse(res["is_authorized_for_literature_review"])

    def test_case_e_null_negative_result_suppression_rejection(self):
        """Case E: Paper documents null / negative result, claim asserts significant positive efficacy -> REJECT (CONTRADICTED)."""
        paper = {
            "ref_id": "REF_SYNTH_05",
            "title": "Controlled trial of Intervention-Z in model systems",
            "abstract": "Intervention-Z failed to inhibit biomarker elevation, yielding no significant difference compared to vehicle control (p >= 0.05).",
            "primary_findings": "No significant therapeutic benefit observed; outcome was inert.",
            "has_negative_results": True
        }
        claim = {
            "claim_id": "CLM_E",
            "claim_text": "Intervention-Z demonstrates significant efficacy and effectively inhibits biomarker elevation."
        }
        res = ExactClaimEvidenceMapper.map_and_verify_claim(claim, paper)
        self.assertEqual(res["verdict"], "CONTRADICTED")
        self.assertFalse(res["is_authorized_for_literature_review"])

    def test_case_f_observational_causal_overclaim_downgrade(self):
        """Case F: Paper is observational, claim asserts definitive causal mechanism -> DOWNGRADE (CORRELATION_TO_CAUSATION)."""
        paper = {
            "ref_id": "REF_SYNTH_06",
            "title": "Cohort analysis of biomarker levels and clinical outcomes",
            "abstract": "In a prospective observational cohort study, higher levels of Biomarker-M were correlated with symptom scores.",
            "study_design": "OBSERVATIONAL_COHORT_CASE_CONTROL",
            "primary_findings": "Statistically significant correlation observed (r = 0.42)."
        }
        claim = {
            "claim_id": "CLM_F",
            "claim_text": "Biomarker-M directly causes and mechanistically drives disease symptoms."
        }
        res = ExactClaimEvidenceMapper.map_and_verify_claim(claim, paper)
        self.assertEqual(res["verdict"], "PARTIALLY_SUPPORTED")
        self.assertIn("CORRELATION_TO_CAUSATION", res["mismatches"])
        self.assertFalse(res["is_authorized_for_literature_review"])

    def test_case_g_citation_exists_but_unsupported_rejection(self):
        """Case G: Citation [1] exists in narrative text, but cited paper does not contain asserted claim -> REJECT via PostResearchCitationAuditor."""
        portfolio = [
            {
                "citation_number": 1,
                "ref_id": "REF_01",
                "title": "Investigation of Factor-A in cell culture",
                "abstract": "Factor-A regulates gene expression in vitro.",
                "intervention_agent": "Factor-A",
                "model_system": "Cell-Culture-X"
            }
        ]
        # Text cites [1] for an entirely different entity/topic
        text = "Synthetic Peptide-99 completely cures autoimmune neurodegeneration in human trials [1]."
        audit_res = PostResearchCitationAuditor.audit_claim_citations(
            proposal_text=text,
            reference_portfolio=portfolio
        )
        self.assertEqual(audit_res["overall_status"], "FAILED")
        self.assertEqual(audit_res["attribution_failures_count"], 1)
        self.assertEqual(audit_res["attribution_failures"][0]["verdict"], "NOT_SUPPORTED")

    def test_case_h_contradictory_divergent_results_preservation(self):
        """Case H: Paper contains dual divergent outcomes (efficacy at low dose, toxicity at high dose) -> PRESERVE BOTH."""
        paper = {
            "ref_id": "REF_SYNTH_08",
            "title": "Biphasic concentration dynamics of Drug-Gamma",
            "abstract": "Drug-Gamma reduced proliferation at 10 uM, but acute toxicity and cell lysis were observed at concentrations exceeding 50 uM.",
            "primary_findings": "Proliferation reduced at 10 uM; severe toxicity at 50 uM.",
            "has_negative_results": True
        }
        canonical = CanonicalPaperEvidenceRecord.build(paper)
        self.assertTrue(canonical["negative_or_null_results"]["has_negative_results"])
        self.assertEqual(canonical["evidence_directness"], "CONTRADICTORY_EVIDENCE")

    def test_case_i_multi_source_fact_blending_detected(self):
        """Case I: Claim asserts an entity completely absent from the cited source paper -> REJECT."""
        paper = {
            "ref_id": "REF_SYNTH_09",
            "title": "Study of Monotherapy-1 alone",
            "abstract": "Monotherapy-1 was administered in isolation.",
            "intervention_agent": "Monotherapy-1"
        }
        claim = {
            "claim_id": "CLM_I",
            "claim_text": "Monotherapy-1 combined with Unrelated-Adjuvant-99 produced synergistic effects.",
            "claim_entity": "unrelated-adjuvant-99"
        }
        res = ExactClaimEvidenceMapper.map_and_verify_claim(claim, paper)
        self.assertEqual(res["verdict"], "NOT_SUPPORTED")

    def test_case_j_no_boilerplate_template_hallucination(self):
        """Case J: EvidenceDrivenParagraphBuilder generates paragraph without generic boilerplate or fake numbers."""
        paper = {
            "ref_id": "REF_SYNTH_10",
            "authors": ["Researcher-Alpha", "Researcher-Beta"],
            "year": 2025,
            "title": "Preliminary observational analysis of Agent-Z",
            "intervention_agent": "Agent-Z",
            "model_system": "NOT_REPORTED",
            "study_design": "OBSERVATIONAL_COHORT_CASE_CONTROL",
            "primary_findings": "Descriptive behavioral shifts were recorded qualitatively.",
            "has_negative_results": True,
            "quantitative_parameters": ""
        }
        para = EvidenceDrivenParagraphBuilder.build_literature_paragraph(paper, citation_number=1)
        # Ensure boilerplate default strings are NOT injected
        self.assertNotIn("گروه کنترل استاندارد", para)
        self.assertNotIn("محدودیت در تنوع دوز و عدم پیگیری طولانی‌مدت", para)
        # Ensure negative/null result is explicitly reported
        self.assertIn("Null Result", para)
        self.assertIn("[1]", para)

    def test_case_k_canonical_record_schema_compliance(self):
        """Case K: Verify CanonicalPaperEvidenceRecord output satisfies Draft-07 JSON schema."""
        schema = SchemaValidator.load_schema("CANONICAL_PAPER_EVIDENCE_RECORD_SCHEMA")

        sample_paper = {
            "ref_id": "REF_SCHEMA_TEST",
            "authors": ["Smith J", "Doe A"],
            "year": 2024,
            "title": "Controlled trial of Novel-Compound in biological model",
            "intervention_agent": "Novel-Compound",
            "model_system": "Cell-Culture-X",
            "study_design": "IN_VITRO_EXPERIMENTAL",
            "primary_findings": "Demonstrated cell growth suppression.",
            "quantitative_parameters": "IC50 = 25.4 uM",
            "has_negative_results": False
        }
        canonical = CanonicalPaperEvidenceRecord.build(sample_paper)
        errs = SchemaValidator.validate(canonical, schema)
        self.assertEqual(errs, [], f"Schema validation errors: {errs}")
        self.assertEqual(len(canonical["quantitative_results"]), 1)

    def test_case_l_claim_evidence_map_schema_compliance(self):
        """Case L: Verify ExactClaimEvidenceMapper output satisfies Draft-07 JSON schema."""
        schema = SchemaValidator.load_schema("CLAIM_EVIDENCE_MAP_SCHEMA")

        sample_paper = {
            "ref_id": "REF_SCHEMA_TEST",
            "authors": ["Smith J"],
            "year": 2024,
            "title": "Controlled trial of Novel-Compound",
            "intervention_agent": "Novel-Compound",
            "model_system": "Model-System-1",
            "study_design": "IN_VITRO_EXPERIMENTAL",
            "primary_findings": "Novel-Compound suppressed cell growth by 45%.",
            "quantitative_parameters": "45%"
        }
        claim = {
            "claim_id": "CLM_TEST",
            "claim_text": "Novel-Compound in Model-System-1 suppressed cell growth by 45% [1].",
            "citation_number": 1
        }
        mapped = ExactClaimEvidenceMapper.map_and_verify_claim(claim, sample_paper)
        errs = SchemaValidator.validate(mapped, schema)
        self.assertEqual(errs, [], f"Schema validation errors: {errs}")
        self.assertEqual(mapped["verdict"], "SUPPORTED")
        self.assertTrue(mapped["is_authorized_for_literature_review"])

    def test_case_m_synthetic_e2e_research_problem_filtering(self):
        """Case M: Synthetic E2E research problem filtering:
        Given a problem targeting (Intervention-Core in Target-Model-T measuring Outcome-O),
        evaluates 5 candidate papers and verifies only genuine direct evidence passes.
        """
        problem = {
            "target_intervention": "Intervention-Core",
            "target_model": "Target-Model-T",
            "target_outcome": "Outcome-O"
        }
        candidates = [
            # 1. Genuine Direct Match
            {
                "ref_id": "P1", "title": "Intervention-Core suppresses Outcome-O in Target-Model-T",
                "intervention_agent": "Intervention-Core", "model_system": "Target-Model-T",
                "study_design": "IN_VITRO_EXPERIMENTAL", "primary_findings": "Suppresses Outcome-O."
            },
            # 2. In Silico Leap
            {
                "ref_id": "P2", "title": "Molecular docking of Intervention-Core",
                "intervention_agent": "Intervention-Core", "model_system": "In Silico Grid",
                "study_design": "COMPUTATIONAL_IN_SILICO", "primary_findings": "High binding affinity."
            },
            # 3. Model Mismatch
            {
                "ref_id": "P3", "title": "Intervention-Core in Incompatible-Model-Z",
                "intervention_agent": "Intervention-Core", "model_system": "Incompatible-Model-Z",
                "study_design": "IN_VITRO_EXPERIMENTAL", "primary_findings": "Active in Model-Z."
            },
            # 4. Botanical Mixture (Formulation Mismatch)
            {
                "ref_id": "P4", "title": "Crude botanical extract containing traces of Intervention-Core",
                "intervention_agent": "Crude Plant Extract", "model_system": "Target-Model-T",
                "study_design": "IN_VITRO_EXPERIMENTAL", "primary_findings": "Crude extract active."
            },
            # 5. Null Contradiction
            {
                "ref_id": "P5", "title": "Evaluation of Intervention-Core in Target-Model-T",
                "intervention_agent": "Intervention-Core", "model_system": "Target-Model-T",
                "study_design": "IN_VITRO_EXPERIMENTAL", "has_negative_results": True,
                "primary_findings": "No significant effect observed on Outcome-O."
            }
        ]

        # Audit all 5 candidates
        direct_matches = []
        rejected_or_divergent = []

        for p in candidates:
            rec = CanonicalPaperEvidenceRecord.build(p, problem)
            if rec["evidence_directness"] == "DIRECT_EVIDENCE":
                direct_matches.append(rec)
            else:
                rejected_or_divergent.append(rec)

        self.assertEqual(len(direct_matches), 1, "Only Paper 1 must be classified as DIRECT_EVIDENCE.")
        self.assertEqual(direct_matches[0]["bibliographic_identity"]["ref_id"], "P1")
        self.assertEqual(len(rejected_or_divergent), 4, "All 4 incompatible papers must be filtered or classified as indirect/contradictory/contextual.")

    def test_case_n_v87_core_invariants_preserved(self):
        """Case N: Enforces core architecture invariants."""
        self.assertEqual(MAX_FINAL_REFERENCES, 25, "Hard ceiling of 25 final references must remain strict.")
        self.assertTrue(NO_QUOTA_FILLING, "Zero artificial reference padding must remain active.")
        self.assertIn(ENGINE_VERSION, ["8.7.0", "9.0.0", "9.1.0", "9.2.0"], "Engine version must be synchronized to at least 8.7.0.")


if __name__ == "__main__":
    unittest.main()
