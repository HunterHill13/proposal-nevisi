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

    def test_4_comprehensive_multi_flaw_remediation_and_organ_globocan(self):
        """Verifies DEFAULT_MAX_ITERATIONS >= 8, organ-aware GLOBOCAN patching, and surgical remediation of all major Reviewer 1/2/3 flaws."""
        self.assertGreaterEqual(IterativeRemediationEngine.DEFAULT_MAX_ITERATIONS, 8)

        breast_data = {
            "title_fa": "بررسی اثر هم‌افزایی متفورمین و رسوراترول بر آپوپتوز سلول‌های سرطان پستان",
            "research_title_fa": "بررسی اثر هم‌افزایی متفورمین و رسوراترول بر آپوپتوز سلول‌های سرطان پستان",
            "framework": "EXPERIMENTAL_IN_VITRO",
            "target_condition": {"name_fa": "سرطان پستان", "name_en": "Breast Neoplasms"},
            "research_problem_model": {
                "framework": "EXPERIMENTAL_IN_VITRO",
                "target_condition": {"name_fa": "سرطان پستان", "name_en": "Breast Neoplasms"},
                "interventions_or_exposures": [{"name": "متفورمین"}, {"name": "رسوراترول"}],
                "population_or_model": {"primary_system": "رده سلولی سرطان پستان"},
                "primary_outcomes": [{"name": "زیست‌پذیری سلولی"}, {"name": "آپوپتوز"}]
            },
            "studies": []
        }
        raw_md = ProposalGenerator.assemble_pajooheshyar_28(breast_data)

        # Inject multiple critical flaws and weaknesses across Sections 2, 11, 13, 19, 20, 26, 27
        flawed_md = (
            raw_md
            .replace("۲,۲۹۶,۸۴۰", "1,000")
            .replace("۲.۳۰", "1.0")
            .replace("۶۶۶,۱۰۳", "500")
            .replace("برش پروتئولیتیک", "")
            .replace("برش پروتئینی", "")
            .replace("پروکاسپاز-۳", "بیان mRNA ژن CASP3 با RT-PCR")
            .replace("Cleaved", "")
            .replace("فعالیت آنزیمی", "")
            .replace("Annexin", "")
            .replace("آنکسین", "")
            .replace("وسترن بلات", "")
            .replace("Western", "")
            .replace("Cell-Free Blank", "")
            .replace("بلانک بدون سلول", "")
            .replace("کنترل بلانک", "")
            .replace("بلانک", "")
            .replace("ToxRTool", "Cochrane RoB-2")
            .replace("NTP OHAT", "RoB-2")
            .replace("GIVIMP", "")
            .replace("ECVAM", "")
            .replace("| مستقل |", "| - |")
            .replace("| وابسته |", "| - |")
            .replace("فرضیه پیش‌بالینی", "درمان قطعی و کاهش سمیت کلیوی بیماران")
            .replace("محدودیت مدل برون‌تن", "")
            .replace("نیازمند کارآزمایی بالینی", "")
            .replace("نیازمند مطالعات in vivo", "")
            .replace("نیازمند مطالعات In Vivo", "")
            .replace("مرزهای تعمیم‌پذیری", "")
            .replace("Selectivity Index", "")
            .replace("selectivity index", "")
        )

        res = IterativeRemediationEngine.remediate_proposal(
            md_content=flawed_md,
            proposal_data=breast_data,
            output_dir=self.output_dir
        )
        self.assertTrue(res["is_approved"])
        final_md = res["final_markdown"]
        # Must restore Breast Cancer GLOBOCAN 2022 (2,296,840), NOT Lung Cancer (2,480,301)
        self.assertIn("۲,۲۹۶,۸۴۰", final_md)
        self.assertNotIn("۲,۴۸۰,۳۰۱", final_md)
        self.assertIn("| مستقل |", final_md)
        self.assertIn("| وابسته |", final_md)

    def test_5_spec_file_deep_merge_and_methodology_subagent_integration(self):
        """Verifies that MasterResearchPipeline preserves subagent studies & farsi_synthesis_summary from PROPOSAL_SPEC.json and wires MethodologyResearchSubagent."""
        import json
        from run_research_pipeline import MasterResearchPipeline

        spec_payload = {
            "keywords": ["Metformin", "Resveratrol", "Breast Neoplasms"],
            "research_problem_model": {
                "target_condition": {"name_fa": "سرطان پستان"}
            },
            "studies": [
                {
                    "pmid": "38999991",
                    "doi": "10.1000/subagent.2024.1",
                    "title": "Metformin and resveratrol synergistically induce apoptosis in breast carcinoma",
                    "authors": ["SubagentLead A", "Researcher B"],
                    "year": 2024,
                    "journal": "Breast Cancer Res",
                    "abstract": "Synergistic apoptosis with IC50 = 11.4 uM (p < 0.001).",
                    "is_full_text": True,
                    "has_full_text": True,
                    "verified": True,
                    "farsi_synthesis_summary": "پاراگراف اختصاصی سنتزشده توسط ساب‌ایجنت ارزیابی شواهد با دقت عددی کامل."
                }
            ]
        }
        spec_file = os.path.join(self.output_dir, "PROPOSAL_SPEC.json")
        with open(spec_file, "w", encoding="utf-8") as f:
            json.dump(spec_payload, f, ensure_ascii=False)

        pipe = MasterResearchPipeline(
            topic="بررسی اثر هم‌افزایی متفورمین و رسوراترول بر آپوپتوز سلول‌های سرطان پستان",
            study_family="in_vitro",
            mode="offline",
            min_refs=1,
            output_dir=self.output_dir,
            spec_path=spec_file
        )
        res = pipe.run()
        self.assertEqual(res["status"], "PASS")
        with open(res["md_path"], "r", encoding="utf-8") as f:
            md_text = f.read()
        self.assertIn("پاراگراف اختصاصی سنتزشده توسط ساب‌ایجنت ارزیابی شواهد", md_text)


if __name__ == "__main__":
    unittest.main()
