#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_v92_hardening.py - Universal 5-Pillar Architectural Hardening Test Suite
Proposal-Nevisi Engine v9.2

Tests the 5 core architectural improvements established during the /grill-me audit:
1. Pillar 1: LiveReferenceVerificationGate (Fail-Closed, PubMed/Crossref verification, caching).
2. Pillar 2: EvidenceRoleClaimBindingGate (Anti-Keyword Proximity Bias, section permission enforcement).
3. Pillar 3: SynergyMetricConfig (Single Source of Truth, theoretical Chou vs CompuSyn 5-tier scale).
4. Pillar 4: BiphasicRedoxContextRule in BiologicalMechanismAdversarialVerifier (Oncology vs Cytoprotection).
5. Pillar 5: AssayInterferencePolicy & Orthogonal Triangulation (Cell-free blank, Annexin V/PI, Clonogenic survival).

100% Domain-Agnostic: Zero hardcoded project subjects; tests universal logic.
"""

import os
import sys
import unittest
import tempfile
import json

sys.stdout.reconfigure(encoding='utf-8')

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.abspath(os.path.join(TESTS_DIR, "..", "scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from core_policies import SynergyMetricConfig, ROLE_SECTION_PERMISSIONS, AssayInterferencePolicy
from scientific_search_adapter import LiveReferenceVerificationGate
from citation_tracker import CitationTracker, EvidenceRoleClaimBindingGate
from biological_mechanism_adversarial_verifier import BiologicalMechanismAdversarialVerifier
from dynamic_protocol_designer import DynamicProtocolDesigner
from generate_compliant_proposal import ProposalGenerator
from proposal_readiness_gate import ProposalReadinessGate


class TestV92HardeningSuite(unittest.TestCase):
    """Rigorous verification suite for v9.2 5-Pillar Architectural Hardening."""

    # =========================================================================
    # PILLAR 1: LIVE REFERENCE VERIFICATION GATE
    # =========================================================================

    def test_pillar1_fixture_and_cache_verification(self):
        """Pillar 1: Verifies fixture reference and ensures cache persistence."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            gate = LiveReferenceVerificationGate(cache_dir=tmp_dir)
            ref_study = {
                "title": "A Novel Synthetic Kinase Inhibitor in Melanoma Models",
                "pmid": "31234567",
                "doi": "10.1016/j.molonc.2019.05.001",
                "mock_verified": True
            }
            res = gate.verify_single_reference(ref_study, mode="fixture")
            self.assertTrue(res["is_verified"])
            self.assertEqual(res["status"], "VERIFIED_FIXTURE")

            # Verify that entry was persisted to cache
            cached_res = gate.verify_single_reference(ref_study, mode="cached")
            self.assertTrue(cached_res["is_verified"])
            self.assertTrue(cached_res.get("from_cache"))

    def test_pillar1_title_mismatch_detection(self):
        """Pillar 1: Identifies mismatched titles as verification failures."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            gate = LiveReferenceVerificationGate(cache_dir=tmp_dir)
            # Inject a resolved entry into cache
            cache_key = "pmid:11223344"
            gate._cache[cache_key] = {
                "is_verified": True,
                "verified_title": "Mechanisms of Autophagy in Cardiac Hypertrophy",
                "verified_pmid": "11223344"
            }
            gate._save_cache()

            # Now test with completely fabricated title under the same PMID
            fabricated_ref = {
                "title": "Inhibition of Lung Cancer Cell Migration by Plant Alkaloids",
                "pmid": "11223344"
            }
            res = gate.verify_single_reference(fabricated_ref, mode="cached")
            self.assertFalse(res["is_verified"])

    def test_pillar1_collection_fail_closed_policy(self):
        """Pillar 1: Collection verification fails closed when unverified references are present."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            gate = LiveReferenceVerificationGate(cache_dir=tmp_dir)
            studies = [
                {"title": "Valid Study Alpha", "pmid": "101", "mock_verified": True},
                {"title": "Unverified Fabricated Study", "pmid": "999"}
            ]
            audit = gate.verify_study_collection(studies, mode="cached", fail_closed=True)
            self.assertFalse(audit["can_proceed"])
            self.assertEqual(audit["verified_count"], 1)
            self.assertEqual(audit["failed_count"], 1)

    # =========================================================================
    # PILLAR 2: EVIDENCE ROLE CLAIM BINDING GATE
    # =========================================================================

    def test_pillar2_role_section_permissions(self):
        """Pillar 2: Epidemiological burden papers are blocked from methodology sections."""
        bibliography = {
            "ref_epi": {
                "title": "Global Burden and Incidence of Lung Adenocarcinoma 2024",
                "evidence_role": "EPIDEMIOLOGICAL_BURDEN"
            },
            "ref_method": {
                "title": "Standard Operating Procedure for In Vitro MTT Viability",
                "evidence_role": "ASSAY_LANDMARK_PROTOCOL"
            }
        }

        # Epidemiological paper cited in Section 13 (Methodology) -> VIOLATION
        violations_sec13 = EvidenceRoleClaimBindingGate.audit_section_citations(
            section_num=13,
            citation_keys=["ref_epi"],
            bibliography=bibliography
        )
        self.assertEqual(len(violations_sec13), 1)
        self.assertEqual(violations_sec13[0].violation_type, "ROLE_SECTION_MISMATCH")

        # Epidemiological paper cited in Section 2 (Problem Statement) -> PERMITTED
        violations_sec2 = EvidenceRoleClaimBindingGate.audit_section_citations(
            section_num=2,
            citation_keys=["ref_epi"],
            bibliography=bibliography
        )
        self.assertEqual(len(violations_sec2), 0)

        # Assay protocol paper cited in Section 19 (Instruments) -> PERMITTED
        violations_sec19 = EvidenceRoleClaimBindingGate.audit_section_citations(
            section_num=19,
            citation_keys=["ref_method"],
            bibliography=bibliography
        )
        self.assertEqual(len(violations_sec19), 0)

    def test_pillar2_document_audit_integration(self):
        """Pillar 2: Multi-section document audit flags inappropriate evidence placement."""
        sections = {
            2: "شیوع فزاینده بیماری در سال‌های اخیر گزارش شده است [ref_epi].",
            13: "پروتکل آزمایشگاهی بر اساس روش استاندارد اجرا گردید [ref_epi]." # VIOLATION!
        }
        bibliography = {
            "ref_epi": {
                "title": "Epidemiology of Disease X",
                "evidence_role": "EPIDEMIOLOGICAL_BURDEN"
            }
        }
        audit = EvidenceRoleClaimBindingGate.audit_document_sections(sections, bibliography, fail_closed=True)
        self.assertFalse(audit["is_compliant"])
        self.assertFalse(audit["can_proceed"])
        self.assertEqual(audit["violations_count"], 1)

    # =========================================================================
    # PILLAR 3: SYNERGY METRIC CONFIG HARMONIZATION
    # =========================================================================

    def test_pillar3_synergy_config_narrative(self):
        """Pillar 3: SynergyMetricConfig harmonizes theoretical Chou (2006) with CompuSyn 5 tiers."""
        narrative = SynergyMetricConfig.get_unified_narrative_fa()
        self.assertIn("CI < 1.0", narrative)
        self.assertIn("هم‌افزایی / Synergism", narrative)
        self.assertIn("CompuSyn", narrative)
        self.assertIn("CI < 0.3", narrative)
        self.assertIn("هم‌افزایی قوی", narrative)
        self.assertIn("0.3 <= CI < 0.7", narrative)
        self.assertIn("0.9 <= CI <= 1.1", narrative)

    def test_pillar3_generation_incorporates_harmonized_narrative(self):
        """Pillar 3: Dual-agent proposal generates unified CI narrative in Sections 5 and 23."""
        mock_data = {
            "title_fa": "بررسی اثر همزمان داروی آلفا و بتا بر زیست‌پذیری رده سلولی",
            "framework": "EXPERIMENTAL_IN_VITRO",
            "interventions": [{"name": "ترکیب آلفا"}, {"name": "ترکیب بتا"}],
            "primary_outcomes": [{"name": "زیست‌پذیری سلولی"}]
        }
        md = ProposalGenerator.assemble_pajooheshyar_28(mock_data)
        self.assertIn("شاخص ترکیب (Combination Index; CI)", md)
        self.assertIn("CI < 0.3", md)
        self.assertIn("هم‌افزایی قوی", md)

    # =========================================================================
    # PILLAR 4: BIPHASIC REDOX CONTEXT RULE
    # =========================================================================

    def test_pillar4_oncology_antioxidant_paradox_flagged(self):
        """Pillar 4: Asserting antioxidant ROS reduction to kill cancer cells is CONTRADICTED."""
        contradictory_claim = "تیمار سلول‌های سرطانی با این ترکیب از طریق خاصیت آنتی‌اکسیدانی و کاهش ROS موجب مرگ سلولی و آپوپتوز می‌گردد."
        res = BiologicalMechanismAdversarialVerifier.check(contradictory_claim, model_context="cancer_in_vitro")
        self.assertEqual(res.status, "CONTRADICTED")
        self.assertEqual(res.inference_type, "BIPHASIC_REDOX_CHECK")
        self.assertIn("پارادوکس ردوکس", res.correction)

    def test_pillar4_oncology_pro_oxidant_cytotoxicity_verified(self):
        """Pillar 4: Asserting pro-oxidant ROS accumulation to trigger cancer apoptosis is VERIFIED."""
        valid_cancer_claim = "The compound induces pro-oxidant ROS accumulation leading to mitochondrial apoptosis in malignant cells."
        res = BiologicalMechanismAdversarialVerifier.check(valid_cancer_claim, model_context="cancer_in_vitro")
        self.assertEqual(res.status, "VERIFIED")
        self.assertEqual(res.inference_type, "BIPHASIC_REDOX_CHECK")

    def test_pillar4_normal_tissue_antioxidant_cytoprotection_verified(self):
        """Pillar 4: Asserting antioxidant ROS scavenging in normal tissue is VERIFIED."""
        valid_normal_claim = "The agent exerts antioxidant activity reducing oxidative stress and protecting normal hepatocytes against toxicity."
        res = BiologicalMechanismAdversarialVerifier.check(valid_normal_claim, model_context="normal_tissue")
        self.assertEqual(res.status, "VERIFIED")
        self.assertEqual(res.inference_type, "BIPHASIC_REDOX_CHECK")

    # =========================================================================
    # PILLAR 5: ASSAY INTERFERENCE & ORTHOGONAL TRIANGULATION
    # =========================================================================

    def test_pillar5_variable_table_in_vitro_controls(self):
        """Pillar 5: In vitro variable table mandates Cell-Free Blank and Vehicle Control."""
        model_dict = {
            "framework": "EXPERIMENTAL_IN_VITRO",
            "interventions_or_exposures": [{"name": "Test Molecule A"}],
            "primary_outcomes": [{"name": "Cell Viability"}]
        }
        variables = DynamicProtocolDesigner.generate_variable_table(model_dict)
        var_names = [v["name"] for v in variables]
        self.assertTrue(any("Cell-Free Blank" in name for name in var_names))
        self.assertTrue(any("Vehicle Control" in name for name in var_names))

    def test_pillar5_orthogonal_triangulation_protocol(self):
        """Pillar 5: Triangulation protocol incorporates primary metabolic, apoptosis, and clonogenic assays."""
        triangulation = DynamicProtocolDesigner.get_orthogonal_triangulation_protocol("EXPERIMENTAL_IN_VITRO")
        controls = triangulation["required_controls"]
        assays = triangulation["orthogonal_assays"]
        self.assertIn("CELL_FREE_BLANK", controls)
        self.assertIn("VEHICLE_CONTROL", controls)
        self.assertIn("PRIMARY_METABOLIC", assays)
        self.assertIn("APOPTOSIS_CONFIRMATION", assays)
        self.assertIn("REPRODUCTIVE_VIABILITY", assays)

    def test_pillar5_proposal_generation_sections_19_and_27(self):
        """Pillar 5: Generated proposal Sections 19 & 27 enforce Cell-Free Blank and Clonogenic Assay."""
        mock_data = {
            "title_fa": "بررسی اثر سمیت سلولی ترکیب تجربی",
            "framework": "EXPERIMENTAL_IN_VITRO",
            "interventions": [{"name": "ترکیب تجربی"}],
            "primary_outcomes": [{"name": "زیست‌پذیری سلولی"}]
        }
        md = ProposalGenerator.assemble_pajooheshyar_28(mock_data)
        # Section 19 check
        self.assertIn("Cell-Free Blank Correction", md)
        self.assertIn("Clonogenic Survival Assay", md)
        # Section 27 check
        self.assertIn("بلانک بدون سلول (Cell-Free Blank)", md)
        self.assertIn("فلوسایتومتری Annexin V-FITC / PI", md)


if __name__ == "__main__":
    unittest.main()
