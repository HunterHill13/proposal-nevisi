#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_scientific_academic_humanizer.py - Test Suite for Scientific Academic Humanizer
Verifies:
1. DataInvariantGate protection of numbers, p-values, citations, genes, and units.
2. PersianAIClicheEngine detection and replacement of 30+ Persian AI cliches.
3. BurstinessEngine sentence length variance and rhythm calibration.
4. Selective narrative section humanization and audit report generation.
5. Fail-closed rollback mechanism upon any invariant mutation.
"""

import os
import sys
import json
import unittest
import tempfile

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from scientific_academic_humanizer import (
    DataInvariantGate,
    PersianAIClicheEngine,
    BurstinessEngine,
    ScientificAcademicHumanizer,
    HumanizationResult
)


class TestScientificAcademicHumanizer(unittest.TestCase):
    """Unit tests for the anti-AI-detection scientific humanization engine."""

    def setUp(self):
        self.humanizer = ScientificAcademicHumanizer(target_burstiness=8.0)

    def test_data_invariant_gate_numbers_and_stats(self):
        """DataInvariantGate strictly extracts and verifies numeric and statistical invariants."""
        orig = "در این مطالعه ۲۴ موش صحرایی با دوز 15 mg/kg تیمار شدند (p < 0.05, CI: 0.78-0.92) و بقای سلولی 95% بود."
        same = "در این مطالعه ۲۴ موش صحرایی با دوز 15 mg/kg تیمار شدند (p < 0.05, CI: 0.78-0.92) و بقای سلولی 95% بود."
        passed, violations = DataInvariantGate.verify(orig, same)
        self.assertTrue(passed)
        self.assertEqual(len(violations), 0)

        # Missing number
        mutated_num = "در این مطالعه ۲۵ موش صحرایی با دوز 15 mg/kg تیمار شدند (p < 0.05, CI: 0.78-0.92) و بقای سلولی 95% بود."
        passed_mut, violations_mut = DataInvariantGate.verify(orig, mutated_num)
        self.assertFalse(passed_mut)
        self.assertTrue(any("Missing numbers" in v for v in violations_mut))

    def test_data_invariant_gate_citations_and_pmids(self):
        """Citations [1], PMIDs, and DOIs are strictly guarded."""
        orig = "بر اساس مطالعه محققان [1, 2] و گزارش PMID: 34567890 با شناسه 10.1016/j.canlet.2023.01.012 اثر اثبات شد."
        safe_mod = "شواهد بالینی [1, 2] و گزارش PMID: 34567890 با شناسه 10.1016/j.canlet.2023.01.012 موید اثربخشی است."
        passed, violations = DataInvariantGate.verify(orig, safe_mod)
        self.assertTrue(passed)

        # Citation dropped
        bad_mod = "شواهد بالینی [1] و گزارش با شناسه 10.1016/j.canlet.2023.01.012 موید اثربخشی است."
        passed_bad, violations_bad = DataInvariantGate.verify(orig, bad_mod)
        self.assertFalse(passed_bad)

    def test_persian_ai_cliche_replacement(self):
        """Persian AI cliches are eradicated and substituted with operational academic phrases."""
        text = "در این راستا، شایان ذکر است که داروی مورد نظر نقش بسزایی دارد و حائز اهمیت است."
        engine = PersianAIClicheEngine()
        sanitized, replaced = engine.replace_cliches(text)

        self.assertNotIn("در این راستا", sanitized)
        self.assertNotIn("شایان ذکر است", sanitized)
        self.assertNotIn("نقش بسزایی دارد", sanitized)
        self.assertNotIn("حائز اهمیت است", sanitized)
        self.assertGreaterEqual(len(replaced), 4)

    def test_em_dash_replacement(self):
        """Em-dashes (—) are converted to standard Persian punctuation."""
        text = "لوپئول — یک تری‌ترپنوئید طبیعی — آپوپتوز را تحریک می‌کند."
        engine = PersianAIClicheEngine()
        sanitized, replaced = engine.replace_cliches(text)
        self.assertNotIn("—", sanitized)

    def test_burstiness_computation(self):
        """BurstinessEngine accurately computes sentence length standard deviation."""
        # Monotonic sentences of identical word length
        uniform_text = "سلول‌های سرطانی در محیط کشت مناسب رشد می‌کنند. " \
                       "پروتکل درمانی در شرایط آزمایشگاهی اجرا می‌گردد. " \
                       "تیمار دارویی در غلظت‌های مشخص اعمال می‌گردد."
        sigma_low = BurstinessEngine.compute_burstiness(uniform_text)

        # Varied sentences: 3 words, 25 words, 7 words
        varied_text = "یافته‌ها قاطع است. " \
                      "به‌منظور ارزیابی دقیق مسیرهای پیام‌رسانی بیوشیمیایی و پایداری آپوپتوز، " \
                      "سلول‌های تحت تیمار با آنتی‌بادی‌های اختصاصی در فواصل زمانی مختلفانکوبه گردیدند و میزان بیان پروتئین سنجیده شد. " \
                      "این نتایج فرضیه را تایید نمود."
        sigma_high = BurstinessEngine.compute_burstiness(varied_text)

        self.assertGreater(sigma_high, sigma_low)

    def test_humanize_text_end_to_end(self):
        """ScientificAcademicHumanizer end-to-end humanization passes invariant checks."""
        input_text = (
            "در این راستا، بیان مسئله به بررسی سرطان کولون می‌پردازد. "
            "شایان ذکر است که نرخ بقای ۵ ساله بیماران کمتر از 14% است [1]. "
            "به طور کلی، داروی سیس‌پلاتین با دوز 50 mg/kg نقش بسزایی دارد و حائز اهمیت است."
        )
        res = self.humanizer.humanize_text(input_text)
        self.assertTrue(res.invariant_check_passed)
        self.assertNotIn("در این راستا", res.humanized_text)
        self.assertNotIn("شایان ذکر است", res.humanized_text)
        self.assertNotIn("نقش بسزایی دارد", res.humanized_text)
        self.assertIn("14%", res.humanized_text)
        self.assertIn("50 mg/kg", res.humanized_text)
        self.assertIn("[1]", res.humanized_text)

    def test_selective_proposal_markdown_sections(self):
        """Proposal markdown is parsed and only targeted narrative sections are humanized."""
        md_text = (
            "# پروپوزال طرح پژوهشی\n\n"
            "## ۱. موضوع (Title)\n"
            "▪ **عنوان فارسی:** بررسی اثر سینرژیک بربرین\n\n"
            "## ۳. بیان مسئله (Problem Statement)\n"
            "در این راستا، بیماری سرطان معده یکی از معضلات بالینی است. "
            "شایان ذکر است که میزان مرگ‌ومیر سالانه ۳۰ درصد می‌باشد [2].\n\n"
            "## ۲۸. منابع\n"
            "[1] Smith J, et al. Oncology 2024; 15: 112-120.\n"
            "[2] Doe A, et al. Cancer Res 2023; 10: 45-50.\n"
        )

        humanized_md, audit = self.humanizer.humanize_proposal_markdown(
            md_text,
            format_type="28",
            target_sections=[3]
        )

        # Section 3 should be humanized
        self.assertNotIn("در این راستا", humanized_md)
        self.assertNotIn("شایان ذکر است", humanized_md)
        self.assertIn("۳۰ درصد", humanized_md)
        self.assertIn("[2]", humanized_md)

        # Section 1 & Section 28 must remain completely intact
        self.assertIn("## ۱. موضوع (Title)", humanized_md)
        self.assertIn("## ۲۸. منابع", humanized_md)
        self.assertIn("Smith J, et al.", humanized_md)

        # Audit report checks
        self.assertEqual(audit["invariant_gate_verdict"], "VERIFIED_100_PERCENT")
        self.assertGreaterEqual(audit["total_cliches_purged"], 2)

    def test_audit_report_saving(self):
        """Audit report exports to valid JSON and Markdown files."""
        report_data = {
            "timestamp": "2026-10-19 20:30:00",
            "target_sections": [3, 4],
            "document_burstiness_before": 4.5,
            "document_burstiness_after": 8.9,
            "target_burstiness": 8.5,
            "total_cliches_purged": 5,
            "invariant_gate_verdict": "VERIFIED_100_PERCENT",
            "invariant_violations": [],
            "section_breakdown": {
                "section_3": {"burstiness_before": 4.2, "burstiness_after": 9.1, "cliches_replaced": 3, "invariant_passed": True}
            },
            "sample_cliche_purges": [
                {"rule_id": "c1_dar_in_rasta", "description": "حذف در این راستا", "matched": "در این راستا", "replacement": "بدین منظور"}
            ]
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            json_p, md_p = ScientificAcademicHumanizer.save_audit_report(report_data, tmpdir)
            self.assertTrue(os.path.exists(json_p))
            self.assertTrue(os.path.exists(md_p))
            with open(json_p, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                self.assertEqual(loaded["total_cliches_purged"], 5)


if __name__ == "__main__":
    unittest.main()
