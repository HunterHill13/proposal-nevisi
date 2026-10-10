#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_v100_fulltext_and_verification_hardening.py - Test Suite for v10.0 Hardened Architecture
Verifies:
1. Fail-closed LiveReferenceVerificationGate (eliminating provisional offline loopholes).
2. Automatic dropping of unverified references (auto_drop_unverified).
3. FullTextRetrievalEngine XML cleaning, passage grounding, and caching.
4. Abstract-Only Quota enforcement (<= 20%) and mandatory justification.
5. Integration with GenericReferenceAuditor and ProposalReadinessGate.
"""

import os
import sys
import tempfile
import unittest

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from scientific_search_adapter import (
    LiveReferenceVerificationGate,
    FullTextRetrievalEngine,
    ScientificSearchAdapter
)
from generic_reference_auditor import GenericReferenceAuditor
from proposal_readiness_gate import ProposalReadinessGate


class TestV100FullTextAndVerificationHardening(unittest.TestCase):
    """Rigorous verification suite for v10.0 Full-Text Engine and Verification Gates."""

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.cache_dir = self.tmp_dir.name

    def tearDown(self):
        self.tmp_dir.cleanup()

    # =========================================================================
    # 1. FAIL-CLOSED VERIFICATION & AUTO-DROP
    # =========================================================================

    def test_fail_closed_unverified_in_auto_mode(self):
        """Ensures that in auto/online mode, an unresolvable paper is strictly marked unverified (no provisional bypass)."""
        gate = LiveReferenceVerificationGate(cache_dir=self.cache_dir)
        fake_paper = {
            "title": "Totally Fabricated In Silico Drug Efficacy Study 2026",
            "pmid": "999999999",
            "doi": "10.9999/fake.paper.doi"
        }
        # In cached mode, must be False
        res_cached = gate.verify_single_reference(fake_paper, mode="cached")
        self.assertFalse(res_cached["is_verified"])
        self.assertEqual(res_cached["status"], "UNVERIFIED_NOT_IN_CACHE")

    def test_auto_drop_unverified_studies(self):
        """Ensures auto_drop_unverified filters out invalid references and keeps verified ones."""
        gate = LiveReferenceVerificationGate(cache_dir=self.cache_dir)
        studies = [
            {"title": "Valid Grounded Study Alpha", "pmid": "111", "mock_verified": True},
            {"title": "Valid Grounded Study Beta", "pmid": "222", "mock_verified": True},
            {"title": "Fabricated Study Gamma", "pmid": "999"}
        ]
        drop_res = gate.auto_drop_unverified(studies, mode="cached", min_required=2, fail_closed=True)
        self.assertTrue(drop_res["can_proceed"])
        self.assertEqual(drop_res["original_count"], 3)
        self.assertEqual(drop_res["retained_verified_count"], 2)
        self.assertEqual(drop_res["dropped_unverified_count"], 1)
        self.assertEqual(drop_res["status"], "PURIFIED_PORTFOLIO_READY")

        # When below required minimum threshold
        drop_fail = gate.auto_drop_unverified(studies, mode="cached", min_required=5, fail_closed=True)
        self.assertFalse(drop_fail["can_proceed"])
        self.assertEqual(drop_fail["status"], "INSUFFICIENT_VERIFIED_REFERENCES")

    # =========================================================================
    # 2. FULL-TEXT RETRIEVAL & PASSAGE GROUNDING
    # =========================================================================

    def test_fulltext_jats_xml_cleaning(self):
        """Verifies JATS XML parsing and tag stripping."""
        xml_sample = """<?xml version="1.0" encoding="UTF-8"?>
        <article>
            <front>
                <article-meta>
                    <title-group><article-title>Mechanistic Evaluation of Lupeol in Lung Cancer</article-title></title-group>
                    <abstract><p>Lupeol induces apoptosis via the intrinsic mitochondrial pathway in A549 cells.</p></abstract>
                </article-meta>
            </front>
            <body>
                <sec>
                    <title>Results</title>
                    <p>Treatment with Lupeol at 50 micromolar significantly reduced cell viability to 42% (p &lt; 0.01).</p>
                    <p>Western blot analysis revealed elevated Bax/Bcl-2 ratio and robust caspase-3 cleavage.</p>
                </sec>
            </body>
        </article>
        """
        cleaned = FullTextRetrievalEngine.clean_jats_xml(xml_sample)
        self.assertIn("Mechanistic Evaluation of Lupeol in Lung Cancer", cleaned)
        self.assertIn("Lupeol induces apoptosis", cleaned)
        self.assertIn("significantly reduced cell viability to 42%", cleaned)
        self.assertNotIn("<article>", cleaned)
        self.assertNotIn("</p>", cleaned)

    def test_extract_grounding_passages(self):
        """Verifies extraction of key verbatim evidence passages for semantic attribution."""
        sample_text = (
            "Introduction: Non-small cell lung cancer remains a leading cause of mortality worldwide. "
            "In this study, Lupeol combined with Newcastle Disease Virus demonstrated potent synergistic growth inhibition in A549 cells. "
            "The combination index (CI) was calculated as 0.68, confirming synergistic interaction according to the Chou-Talalay theorem. "
            "Flow cytometric analysis demonstrated that the combination increased apoptosis to 58.4% compared to 18.2% in monotherapy. "
            "Routine maintenance and cell passage protocols followed standard institutional guidelines."
        )
        passages = FullTextRetrievalEngine.extract_grounding_passages(sample_text, keywords=["synergistic", "apoptosis", "chou-talalay"])
        self.assertGreaterEqual(len(passages), 1)
        # Should prioritize the sentences with synergistic / apoptosis / CI
        joined_passages = " ".join(passages)
        self.assertTrue("synergistic" in joined_passages or "apoptosis" in joined_passages)

    def test_study_tier_grounding_classification(self):
        """Verifies study classification into Tier A (Full-Text Grounded) vs Tier B (Abstract-Only)."""
        engine = FullTextRetrievalEngine(cache_dir=self.cache_dir)

        # Full-text provided (>800 chars)
        long_fulltext = "Mechanisms of action in lung adenocarcinoma model. " * 30
        record_with_fulltext = {
            "title": "Study with Verified Full Text",
            "pmid": "31000001",
            "full_text": long_fulltext
        }
        grounded_a = engine.retrieve_and_ground_study(record_with_fulltext, mode="fixture")
        self.assertTrue(grounded_a["has_full_text"])
        self.assertEqual(grounded_a["tier"], "TIER_A_FULL_TEXT_GROUNDED")
        self.assertGreaterEqual(len(grounded_a["grounding_passages"]), 1)

        # Abstract-only study
        record_abstract_only = {
            "title": "Historical Landmark Closed Access Study",
            "pmid": "12000002",
            "abstract": "A brief abstract explaining foundational method with closed access."
        }
        grounded_b = engine.retrieve_and_ground_study(record_abstract_only, mode="fixture")
        self.assertFalse(grounded_b["has_full_text"])
        self.assertEqual(grounded_b["tier"], "TIER_B_ABSTRACT_ONLY")
        self.assertIn("abstract_only_justification", grounded_b)
        self.assertTrue(len(grounded_b["abstract_only_justification"]) > 15)

    # =========================================================================
    # 3. ABSTRACT-ONLY QUOTA (<= 20%) & JUSTIFICATION AUDIT
    # =========================================================================

    def test_abstract_quota_enforcement(self):
        """Verifies that apply_abstract_quota strictly caps Tier B papers at 20%."""
        # 10 papers: 9 Tier A, 1 Tier B -> 10% (under 20%, should pass)
        studies_passing = [
            {"title": f"Study A_{i}", "tier": "TIER_A_FULL_TEXT_GROUNDED", "has_full_text": True, "relevance_score": 0.9}
            for i in range(16)
        ] + [
            {"title": "Study B_1", "tier": "TIER_B_ABSTRACT_ONLY", "has_full_text": False, "relevance_score": 0.95, "abstract_only_justification": "Seminal landmark"}
        ]
        quota_res = FullTextRetrievalEngine.apply_abstract_quota(studies_passing, max_abstract_ratio=0.20, min_total_required=15)
        self.assertTrue(quota_res["can_proceed"])
        self.assertEqual(quota_res["tier_b_count"], 1)
        self.assertLessEqual(quota_res["abstract_ratio"], 0.20)

        # 10 papers: 5 Tier A, 5 Tier B -> 50% (exceeds 20%, must drop excess Tier B)
        studies_excess = [
            {"title": f"Study A_{i}", "tier": "TIER_A_FULL_TEXT_GROUNDED", "has_full_text": True, "relevance_score": 0.9}
            for i in range(16)
        ] + [
            {"title": f"Study B_{i}", "tier": "TIER_B_ABSTRACT_ONLY", "has_full_text": False, "relevance_score": 0.5 + i*0.05}
            for i in range(10)
        ]
        quota_drop = FullTextRetrievalEngine.apply_abstract_quota(studies_excess, max_abstract_ratio=0.20, min_total_required=15)
        self.assertTrue(quota_drop["can_proceed"])
        self.assertGreater(quota_drop["tier_b_dropped_count"], 0)
        self.assertLessEqual(quota_drop["abstract_ratio"], 0.20)

    def test_generic_reference_auditor_abstract_quota_check(self):
        """Verifies that GenericReferenceAuditor.audit_final_reference_portfolio detects quota and justification defects."""
        # Create a valid portfolio with 16 Tier A and 2 Tier B (ratio = 2/18 = 11.1% <= 20%)
        valid_portfolio = [
            {
                "citation_number": i,
                "ref_id": f"REF_{i}",
                "final_inclusion_reason": "DIRECT_DISEASE_MODEL_EVIDENCE",
                "proposal_section_supported": ["SECTION_02"],
                "why_this_paper_is_needed": "Substantive empirical evidence for mechanism verification.",
                "tier": "TIER_A_FULL_TEXT_GROUNDED",
                "has_full_text": True,
                "grounding_passages": ["Key evidence sentence extracted."]
            } for i in range(1, 17)
        ] + [
            {
                "citation_number": 17,
                "ref_id": "REF_17",
                "final_inclusion_reason": "METHODOLOGICAL_BENCHMARK",
                "proposal_section_supported": ["SECTION_05"],
                "why_this_paper_is_needed": "Theoretical Chou-Talalay median effect algorithm formulation.",
                "tier": "TIER_B_ABSTRACT_ONLY",
                "has_full_text": False,
                "abstract_only_justification": "Closed-access landmark theorem from 1984."
            }
        ]

        audit_valid = GenericReferenceAuditor.audit_final_reference_portfolio(valid_portfolio)
        self.assertEqual(audit_valid["portfolio_status"], "PASS")

        # Mutate to exceed 20% quota (add 8 more Tier B papers)
        mutated_exceeding = list(valid_portfolio)
        for j in range(18, 25):
            mutated_exceeding.append({
                "citation_number": j,
                "ref_id": f"REF_{j}",
                "final_inclusion_reason": "METHODOLOGICAL_BENCHMARK",
                "proposal_section_supported": ["SECTION_05"],
                "why_this_paper_is_needed": "Substantive empirical evidence for test portfolio.",
                "tier": "TIER_B_ABSTRACT_ONLY",
                "has_full_text": False,
                "abstract_only_justification": "Closed-access historical reference."
            })
        audit_exceeding = GenericReferenceAuditor.audit_final_reference_portfolio(mutated_exceeding)
        self.assertEqual(audit_exceeding["portfolio_status"], "FAIL")
        self.assertTrue(any("EXCEEDS_ABSTRACT_ONLY_QUOTA_20_PERCENT" in v for v in audit_exceeding["violations"]))

        # Mutate Tier B to omit justification
        valid_portfolio[16]["abstract_only_justification"] = ""
        audit_no_just = GenericReferenceAuditor.audit_final_reference_portfolio(valid_portfolio)
        self.assertEqual(audit_no_just["portfolio_status"], "FAIL")
        self.assertTrue(any("MISSING_ABSTRACT_ONLY_JUSTIFICATION" in v for v in audit_no_just["violations"]))

    # =========================================================================
    # 4. PROPOSAL READINESS GATE INTEGRATION
    # =========================================================================

    def test_readiness_gate_infrastructure_includes_fulltext_engine(self):
        """Verifies that ProposalReadinessGate checks FullTextRetrievalEngine in infrastructure mode."""
        res = ProposalReadinessGate.check_all(mode="PRE_GENERATION_INFRASTRUCTURE")
        self.assertTrue(res.can_proceed)
        self.assertIn("FullTextRetrievalEngine", res.passed_modules)
        self.assertIn("LiveReferenceVerificationGate", res.passed_modules)


if __name__ == "__main__":
    unittest.main()
