#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_iterative_remediation_engine.py - Unit & Behavioral Tests for Iterative Remediation Engine
Proposal-Nevisi Engine v11.4.1 (Cognitive Multi-Agent Architecture)
"""

import os
import sys
import tempfile
import unittest

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from iterative_remediation_engine import (
    IterativeRemediationEngine, SurgicalSectionPatcher, RemediationExhaustionError
)
from generate_compliant_proposal import ProposalGenerator


class TestIterativeRemediationEngine(unittest.TestCase):
    """Test suite validating iterative closed-loop convergence and surgical patching."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_dir = self.temp_dir.name
        self.mock_proposal_data = {
            "research_title_fa": "بررسی اثر هم‌افزایی ترکیب دارویی بر مدل آزمایشگاهی بدخیم",
            "research_title_en": "Investigation of combination efficacy in cellular model",
            "study_type": "تجربی مداخله‌ای (in_vitro)",
            "primary_endpoint": "مهار رشد سلولی و القای آپوپتوز",
            "framework": "EXPERIMENTAL_IN_VITRO",
            "negative_search_strategy": "0 hits in PubMed for combination",
            "research_problem_model": {
                "target_condition": {"name_fa": "سرطان ریه", "name_en": "Lung Neoplasms"},
                "interventions_or_exposures": [{"name": "عامل آلفا"}, {"name": "عامل بتا"}],
                "population_or_model": {"primary_system": "رده سلولی بدخیم", "control_system": "سلول اپیتلیال نرمال"},
                "primary_outcomes": [{"name": "زیست‌پذیری"}, {"name": "آپوپتوز"}]
            },
            "studies": []
        }

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_surgical_section_patcher_split_and_reassemble(self):
        """Verifies splitting markdown into canonical sections and lossless reassembly."""
        sample_md = (
            "# عنوان اصلی\n\n"
            "## ۱. موضوع\nموضوع طرح پژوهشی\n\n"
            "## ۲. بیان مسئله\nبیان مسئله و بار بیماری\n\n"
            "## ۳. مرور بر منابع\nپیشینه مقالات\n"
        )
        secs = SurgicalSectionPatcher.split_into_sections(sample_md)
        self.assertIn(1, secs)
        self.assertIn(2, secs)
        self.assertIn(3, secs)
        self.assertIn("بیان مسئله و بار بیماری", secs[2]["content"])

        # Patch section 2
        patched_md = SurgicalSectionPatcher.patch_section_content(
            sample_md, 2, lambda t: t + "\nضمیمه جدید بیان مسئله"
        )
        self.assertIn("ضمیمه جدید بیان مسئله", patched_md)
        self.assertIn("پیشینه مقالات", patched_md)

    def test_iterative_remediation_convergence_on_flawed_draft(self):
        """Validates that a proposal with critical flaws undergoes surgical patching and converges to approval."""
        # Generate clean full 28-section proposal markdown
        raw_md = ProposalGenerator.assemble_pajooheshyar_28(self.mock_proposal_data)
        
        # Deliberately inject flaws: B=1 error and remove GLOBOCAN checksum
        flawed_md = raw_md.replace(
            "B = k_{blocks} - 1 = 3 - 1 = 2", "B = 1"
        ).replace(
            "E = 30 - 2 - 9 = 19", "E = 30 - 1 - 9 = 20"
        ).replace(
            "۲,۴۸۰,۳۰۱", "2,000,000"
        )

        res = IterativeRemediationEngine.remediate_proposal(
            md_content=flawed_md,
            proposal_data=self.mock_proposal_data,
            max_iterations=5,
            output_dir=self.output_dir
        )

        self.assertTrue(res["is_approved"])
        self.assertGreaterEqual(res["iterations_count"], 1)
        self.assertLessEqual(res["iterations_count"], 5)
        
        # Verify that B=2 and exact GLOBOCAN checksum were restored
        final_md = res["final_markdown"]
        self.assertIn("E = 30 - 2 - 9 = 19", final_md)
        self.assertIn("۲,۴۸۰,۳۰۱", final_md)

        # Verify audit trail artifacts
        self.assertTrue(os.path.exists(res["audit_trail_md"]))
        self.assertTrue(os.path.exists(res["audit_trail_json"]))

        with open(res["audit_trail_md"], "r", encoding="utf-8") as f:
            trail_text = f.read()
        self.assertIn("کارنامه جامع دورهای بازبینی", trail_text)
        self.assertIn("تایید قطعی و تصویب گرنت", trail_text)

    def test_circuit_breaker_fail_closed_on_unresolvable_flaws(self):
        """Verifies that unresolvable flaws trigger RemediationExhaustionError (Fail-Closed)."""
        stub_md = "## ۲۲. حجم نمونه\nمتن ناقص بدون هیچ فرمول ریاضی."
        
        # Should raise RemediationExhaustionError after max iterations
        with self.assertRaises(RemediationExhaustionError):
            IterativeRemediationEngine.remediate_proposal(
                md_content=stub_md,
                proposal_data=self.mock_proposal_data,
                max_iterations=2,
                output_dir=self.output_dir
            )


if __name__ == "__main__":
    unittest.main()
