#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_v140_cognitive_study_section.py - Test Suite for Proposal-Nevisi v14.0
Tests the Cognitive Study Section Swarm, Biostatistical Computational Tooling,
Subagent Persona Manifests, and Two-Tier Nested Closed-Loop Mechanics.
"""

import os
import sys
import unittest
import json

# Adjust path for script imports
SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from verify_biostatistics import BiostatisticalValidator


class TestV140BiostatisticalValidator(unittest.TestCase):
    """Verifies that BiostatisticalValidator correctly audits sample sizes across archetypes."""

    def test_health_systems_cochran_validation_pass(self):
        sample_text = (
            "حجم نمونه بر پایه فرمول کوکران با در نظر گرفتن نسبت ۵۰٪، خطای مجاز ۵٪ (d=0.05) "
            "و ضریب اطمینان ۹۵٪ (z=1.96) محاسبه شد. با اعمال ضریب اثر طرح (DEFF=1.5) به دلیل نمونه‌گیری خوشه‌ای "
            "و پیش‌بینی ۱۰٪ ریزش، تعداد نهایی نمونه‌ها برابر ۶۴۲ نفر تعیین گردید. خطای نوع اول آلفا 0.05 و توان آزمون 0.80 در نظر گرفته شد."
        )
        res = BiostatisticalValidator.verify_sample_size(sample_text, study_family="health_systems")
        self.assertEqual(res["coherence_status"], "PASS")
        self.assertTrue(res["formula_found"])
        self.assertTrue(res["alpha_specified"])
        self.assertTrue(res["power_specified"])
        self.assertEqual(res["claimed_n"], 642)
        self.assertEqual(res["nih_biostatistical_penalty"], 0.0)

    def test_health_systems_missing_formula_fail(self):
        sample_text = "در این مطالعه تعداد ۱۰۰ نفر بیمار انتخاب شدند."
        res = BiostatisticalValidator.verify_sample_size(sample_text, study_family="health_systems")
        self.assertEqual(res["coherence_status"], "FAIL")
        self.assertFalse(res["formula_found"])
        self.assertGreater(res["nih_biostatistical_penalty"], 0.0)
        self.assertTrue(any("MISSING_COCHRAN_FORMULA" in iss for iss in res["issues"]))

    def test_clinical_rct_chow_wang_pass(self):
        sample_text = (
            "بر اساس فرمول چو و وانگ (Chow & Wang) جهت مقایسه دو نسبت در دو بازوی کارآزمایی بالینی، "
            "با توان آزمون ۸۰٪ و سطح معناداری آلفا ۰.۰۵، تعداد نمونه در هر بازو ۶۴ نفر و مجموعاً ۱۲۸ بیمار برآورد شد."
        )
        res = BiostatisticalValidator.verify_sample_size(sample_text, study_family="clinical_rct")
        self.assertEqual(res["coherence_status"], "PASS")
        self.assertTrue(res["formula_found"])
        self.assertEqual(res["calculated_benchmark_n"], 128)

    def test_in_vivo_mead_equation_bounds(self):
        sample_text_pass = (
            "جهت تعیین تعداد حیوانات آزمایشگاهی از معادله تخصیص منابع مید (Mead's Resource Equation) "
            "به صورت E = N - B - T استفاده شد. با ۳ گروه مداخله، ۲ درجه آزادی بلوک و ۲۴ موش صحرایی، "
            "مقدار E=18 به دست آمد که در بازه بهینه ۱۰ تا ۲۰ راهنمای ARRIVE قرار دارد. آلفا=0.05 و توان=80% لحاظ شد."
        )
        res_pass = BiostatisticalValidator.verify_sample_size(sample_text_pass, study_family="in_vivo")
        self.assertEqual(res_pass["coherence_status"], "PASS")
        self.assertEqual(res_pass["mead_degrees_of_freedom_E"], 18)

        sample_text_fail = (
            "معادله تخصیص منابع مید به صورت E = N - B - T محاسبه شد و مقدار E=25 تعیین گردید. آلفا=0.05 و توان=0.80."
        )
        res_fail = BiostatisticalValidator.verify_sample_size(sample_text_fail, study_family="in_vivo")
        self.assertEqual(res_fail["coherence_status"], "FAIL")
        self.assertTrue(any("OUT_OF_BOUNDS" in iss for iss in res_fail["issues"]))

    def test_diagnostic_buderer_pass(self):
        sample_text = (
            "حجم نمونه بر اساس فرمول بودرر (Buderer) بر مبنای حساسیت و ویژگی پیش‌بینی‌شده با شیوع بیماری، "
            "با توان ۹۰٪ و خطای آلفا ۰.۰۵ و سطح اطمینان ۹۵٪ محاسبه گردید."
        )
        res = BiostatisticalValidator.verify_sample_size(sample_text, study_family="diagnostic")
        self.assertEqual(res["coherence_status"], "PASS")
        self.assertTrue(res["formula_found"])


class TestV140SubagentManifests(unittest.TestCase):
    """Verifies that all 7 Subagent definition markdown files are correctly configured."""

    def setUp(self):
        # tests/ -> proposal-nevisi/ -> skills/ (wait, proposal-nevisi is in .agents/skills/proposal-nevisi)
        # tests -> proposal-nevisi -> skills -> .agents -> root
        self.agents_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "agents"))

    def test_all_seven_subagents_exist(self):
        expected_agents = [
            "grant-significance-innovation.md",
            "grant-methodology-biostatistics.md",
            "grant-evidence-entailment.md",
            "grant-feasibility-logistics.md",
            "grant-ethics-lay-advocate.md",
            "grant-study-section-sro.md",
            "citation-claim-verifier.md"
        ]
        for ag in expected_agents:
            ag_path = os.path.join(self.agents_dir, ag)
            self.assertTrue(os.path.exists(ag_path), f"Agent file missing: {ag_path}")
            with open(ag_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("---", content, f"Agent missing YAML frontmatter: {ag}")
            self.assertIn("name:", content)
            self.assertIn("tools:", content)

    def test_methodology_has_run_command_tool(self):
        meth_path = os.path.join(self.agents_dir, "grant-methodology-biostatistics.md")
        with open(meth_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("run_command", content)
        self.assertIn("verify_biostatistics.py", content)


if __name__ == "__main__":
    unittest.main()
