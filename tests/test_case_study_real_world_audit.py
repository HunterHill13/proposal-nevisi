#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_case_study_real_world_audit.py - Case Study Epistemic Audit (Lupeol + NDV + A549)
Proposal-Nevisi Engine v9.1 (Architectural Verification of Epistemic Honesty)

Validates the 4 critical epistemic behaviors on the real-world case study:
1. Purity Disentanglement: Lupeol is normalized without assuming purity unless stated.
2. Viral Dynamics: NDV co-treatment evaluates viral replication kinetics and schedule dependence.
3. Contextual Boundary: Model mismatches (e.g. mouse TC-1 vs human A549) are flagged as INDIRECT_ANALOGOUS.
4. Epistemic Humility: Factual absence of direct co-treatment on A549 emits NO_DIRECT_COMBINATION_EVIDENCE.
"""

import sys
import os
import unittest

sys.stdout.reconfigure(encoding='utf-8')

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.abspath(os.path.join(TESTS_DIR, "..", "scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from compound_entity_normalizer import CompoundEntityNormalizer
from combination_interaction_model_selector import CombinationInteractionModelSelector
from citation_tracker import CitationTracker
from combination_hypothesis_engine import CombinationHypothesisEngine
from proposal_readiness_gate import ProposalReadinessGate


class TestCaseStudyRealWorldAudit(unittest.TestCase):
    """Case study epistemic integrity assertions on Lupeol + NDV + A549."""

    def test_lupeol_purity_disentanglement(self):
        """1. Lupeol is normalized without assuming purity unless explicitly stated."""
        # Case A: Bare name without purity stated -> is_parent_compound=True, is_pure=False, analytical_purity='NOT_REPORTED'
        bare_norm = CompoundEntityNormalizer.normalize("Lupeol")
        self.assertTrue(bare_norm.is_parent_compound)
        self.assertFalse(bare_norm.is_pure)
        self.assertEqual(bare_norm.analytical_purity, "NOT_REPORTED")
        self.assertTrue(any("ANALYTICAL_PURITY_UNSPECIFIED" in w for w in bare_norm.methodological_warnings))

        # Case B: Explicitly stated purity -> is_pure=True, analytical_purity != 'NOT_REPORTED'
        pure_norm = CompoundEntityNormalizer.normalize("Lupeol (purity >= 98%, HPLC)")
        self.assertTrue(pure_norm.is_pure)
        self.assertIn("98%", pure_norm.analytical_purity)

        # Case C: Plant extract containing lupeol -> EXTRACT, is_pure=False
        extract_norm = CompoundEntityNormalizer.normalize("Crataeva nurvala stem bark ethanolic extract containing lupeol")
        self.assertIn(extract_norm.category, ["STANDARDIZED_EXTRACT", "CRUDE_EXTRACT"])
        self.assertFalse(extract_norm.is_pure)

        # Case D: Synthetic derivative -> is_pure=False
        deriv_norm = CompoundEntityNormalizer.normalize("Lupeol linoleate")
        self.assertIn(deriv_norm.category, ["DERIVATIVE", "SYNTHETIC_ANALOG"])
        self.assertFalse(deriv_norm.is_pure)

    def test_ndv_live_virus_kinetics_and_schedule_dependence(self):
        """2. NDV co-treatment evaluates viral replication kinetics and schedule dependence."""
        result = CombinationInteractionModelSelector.select(
            agent_a_type="small_molecule",
            agent_b_type="oncolytic_virus",
            dose_matrix_type="checkerboard",
            num_dose_levels_a=5,
            num_dose_levels_b=5,
            live_virus_involved=True,
            schedule_dependent=True
        )

        # Must flag viral kinetic considerations
        self.assertTrue(len(result.viral_kinetic_considerations) >= 2)
        kinetics_text = " ".join(result.viral_kinetic_considerations)
        self.assertIn("تکثیر دینامیک ویروسی", kinetics_text)
        self.assertIn("تداخل احتمالی ضدویروسی", kinetics_text)

        # Must flag schedule dependence notes
        self.assertIsNotNone(result.schedule_dependence_notes)
        self.assertIn("ترتیب زمانی مواجهه", result.schedule_dependence_notes)

    def test_species_and_cell_line_mismatch_flagged_indirect_analogous(self):
        """3. Mismatches (e.g. mouse TC-1 vs human A549) are flagged as INDIRECT_ANALOGOUS."""
        tracker = CitationTracker()
        ref_tc1 = {
            "title": "Lupeol suppresses tumor growth in TC-1 mouse lung cancer model",
            "abstract": "We evaluated lupeol in murine TC-1 lung carcinoma cells in vitro and in C57BL/6 mice.",
            "cell_lines": ["TC-1"],
            "compounds": ["Lupeol"],
            "model": "Murine TC-1 cell line"
        }
        tracker.register_reference("REF-TC1", ref_tc1)

        # Assert claim on human A549 cell line backed by TC-1 study
        audit = tracker.audit_claim_binding(
            claim_text="Lupeol inhibits cell proliferation and induces cell cycle arrest in A549 lung cancer cells.",
            citation_id="REF-TC1",
            target_compound="Lupeol",
            target_model="A549",
            target_endpoint="proliferation"
        )

        self.assertTrue(audit.compound_match, "Compound Lupeol should match")
        self.assertFalse(audit.model_match, "Model A549 should NOT match TC-1")
        self.assertEqual(audit.evidence_tier, "INDIRECT_ANALOGOUS")
        self.assertFalse(audit.is_direct_support, "Direct support must be False for model mismatch")
        self.assertTrue(any("MODEL_MISMATCH" in w for w in audit.warnings))

    def test_factual_absence_of_direct_combination_emits_no_direct_combination_evidence(self):
        """4. Factual absence of direct co-treatment on A549 emits NO_DIRECT_COMBINATION_EVIDENCE."""
        # Simulated corpus containing only single-agent studies
        corpus = [
            {
                "title": "Lupeol induces mitochondrial apoptosis in human lung adenocarcinoma A549 cells",
                "abstract": "Lupeol treatment inhibited A549 cell viability with IC50 of 45 uM via Bax upregulation.",
                "primary_findings": "Lupeol monotherapy induces apoptosis in A549 cells."
            },
            {
                "title": "Oncolytic Newcastle disease virus AF2240 strain induces apoptosis in A549 cells",
                "abstract": "NDV infected A549 lung cancer cells and caused viral oncolysis.",
                "primary_findings": "NDV monotherapy induces oncolysis in A549."
            },
            {
                "title": "Chou-Talalay median effect equation for quantification of drug synergism",
                "abstract": "Theoretical foundations of combination index CI < 1.",
                "primary_findings": "Methodological CI algorithms."
            }
        ]

        analysis = CombinationHypothesisEngine.analyze(
            entity_a="Lupeol",
            entity_b="Newcastle Disease Virus",
            target="A549 cell growth inhibition",
            retrieved_evidence=corpus,
            model_or_cell_line="A549"
        )

        self.assertFalse(analysis.has_direct_combination_evidence)
        self.assertEqual(analysis.direct_combination_evidence_count, 0)
        
        has_warning = any("NO_DIRECT_COMBINATION_EVIDENCE" in w for w in analysis.bias_warnings)
        self.assertTrue(has_warning, "Expected NO_DIRECT_COMBINATION_EVIDENCE warning when no direct co-treatment study exists")
        self.assertEqual(analysis.recommended_framing, "neutral")

    def test_integrated_system_readiness(self):
        """5. Integrated ProposalReadinessGate confirms all 8 modules pass verification."""
        gate_res = ProposalReadinessGate.check_all(mode="PRE_GENERATION_INFRASTRUCTURE")
        self.assertTrue(gate_res.is_ready)
        self.assertEqual(len(gate_res.failed_modules), 0)


if __name__ == "__main__":
    unittest.main()
