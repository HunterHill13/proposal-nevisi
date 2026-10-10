#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_pre_emptive_risk_of_bias_mitigator.py - Test Suite for Pre-emptive Risk of Bias Mitigation Engine
Proposal-Nevisi Engine v10.2
"""

import os
import sys
import json
import unittest
import tempfile
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from pre_emptive_risk_of_bias_mitigator import (
    PreEmptiveRiskOfBiasMitigator,
    BiasDomainEvaluation,
    RiskOfBiasAuditResult
)
from proposal_readiness_gate import ProposalReadinessGate


def get_sample_low_risk_proposal() -> str:
    """Provides a synthetic 28-section proposal with rigorous bias mitigation across all 5 domains."""
    sections = [
        "## 1. موضوع\nبررسی پیشگیرانه اثرات فارماکولوژیک دارو بر مهار تکثیر سلول‌ها",
        "## 6. اهداف جزیی\n۱. تعیین دوز بهینه دارو در مهار تکثیر\n۲. بررسی نرخ آپوپتوز و مرگ برنامه‌ریزی‌شده سلول‌ها",
        "## 13. روش اجرا\nتخصیص شرایط آزمایشی به چاهک‌های پلیت به صورت تصادفی ساختاریافته (Randomized Block Design) و با کدگذاری نمونه‌ها (Coded Vials / Allocation Concealment) توسط ناظر مستقل انجام می‌پذیرد. همچنین سنجش پیامدها با کورسازی ارزیاب و اپراتور دستگاه نسبت به گروه‌ها (Blinded Outcome Assessment) صورت خواهد گرفت. شرایط محیطی انکوباتور در تمام پلیت‌ها یکنواخت است.",
        "## 14. نوع مطالعه\nتجربی آزمایشگاهی برون‌تن (In Vitro Experimental)",
        "## 15. جامعه مورد مطالعه\nرده سلولی استاندارد تهیه شده از انستیتو پاستور ایران",
        "## 16. محل انجام مطالعه\nآزمایشگاه تحقیقات سلولی و مولکولی دانشگاه",
        "## 17. معیار های ورود به مطالعه\nسلول‌های با زیست‌پذیری بالای ۹۵ درصد و فاقد آلودگی مایکوپلاسما",
        "## 18. معیار های خروج از مطالعه\n- حذف چاهک‌های دارای نقص فنی آشکار مطابق معیارهای از پیش تعریف‌شده بدون انتخاب گزینشی داده‌ها.\n- شناسایی و مدیریت داده‌های پرت (Outliers) بر مبنای آزمون آماری گرابز (Grubbs' Test) در سطح معناداری ۰.۰۱ و عدم اعمال حذف سلیقه‌ای.",
        "## 19. ابزار های گردآوری اطلاعات\nدستگاه اسپکتروفتومتر الایزا ریدر مجهز به سیستم خوانش خودکار و فلوسایتومتری",
        "## 20. تعیین اعتبار ابزار گردآوری\nکالیبراسیون دوره‌ای دستگاه‌ها و کورسازی اپراتور ارزیاب نسبت به ماهیت گروه‌های آزمایشی",
        "## 21. تعیین ابزار گردآوری\nاستفاده از کیت‌های استاندارد آنکسین V در ۳ تکرار بیولوژیک مستقل",
        "## 22. حجم نمونه و روش محاسبه آن\nحجم نمونه با رابطه کوهن برای توان آزمون ۸۰٪ و آلفای ۵٪ محاسبه شد",
        "## 23. روش تجزیه و تحلیل داده\nآنالیز با Two-way ANOVA و مدیریت داده‌های پرت و گمشده با آزمون‌های نرمال بودن داده‌ها",
        "## 24. ملاحظلات اخلاقی در صورت نیاز\nکد اخلاق سازمانی اخذ شده و تعهد به پیش‌ثبت پروتکل مطالعه (Pre-registration) در سامانه پژوهشیار و پلتفرم دسترسی آزاد OSF پیش از شروع فاز آزمایشگاهی قید گردیده است.",
        "## 25. نحوه رعایت نکات امنیتی و حفاظت پروژه در صورت نیاز\nرعایت کامل موازین ایمنی زیستی در سطح BSL-2",
        "## 26. مشکلات و محدودیت ها\nکنترل سوگیری موقعیت چاهک‌ها با چیدمان تصادفی پلیت‌ها و مهار تبخیر حاشیه‌ای (Edge Effect)",
        "## 27. روش انجام طرح، شیوه اجرایی مراحل طرح و چگونگی جمع آوری اطلاعات\nپروتکل با گروه‌های کنترل منفی و شاهد با رعایت اصول کورسازی و تخصیص تصادفی اجرا خواهد شد."
    ]
    return "\n\n".join(sections)


class TestPreEmptiveRiskOfBiasMitigator(unittest.TestCase):
    """Test suite for Pre-emptive Risk of Bias Mitigation Engine."""

    def setUp(self):
        self.compliant_proposal = get_sample_low_risk_proposal()

    def test_parse_sections(self):
        """Verifies section parsing and mapping."""
        sections = PreEmptiveRiskOfBiasMitigator.parse_sections(self.compliant_proposal)
        self.assertIn(1, sections)
        self.assertIn(13, sections)
        self.assertIn(18, sections)
        self.assertIn(24, sections)

    def test_evaluate_selection_bias_low_risk(self):
        """Tests Domain 1 evaluation for low risk (randomization + concealment)."""
        sections = PreEmptiveRiskOfBiasMitigator.parse_sections(self.compliant_proposal)
        d1 = PreEmptiveRiskOfBiasMitigator.evaluate_selection_bias(sections)
        self.assertEqual(d1.domain_id, "DOMAIN_1_SELECTION_BIAS")
        self.assertEqual(d1.risk_level, "LOW_RISK")
        self.assertGreater(len(d1.strengths), 0)

    def test_evaluate_performance_bias_low_risk(self):
        """Tests Domain 2 evaluation for environmental and plate layout uniformity."""
        sections = PreEmptiveRiskOfBiasMitigator.parse_sections(self.compliant_proposal)
        d2 = PreEmptiveRiskOfBiasMitigator.evaluate_performance_bias(sections)
        self.assertEqual(d2.domain_id, "DOMAIN_2_PERFORMANCE_BIAS")
        self.assertEqual(d2.risk_level, "LOW_RISK")

    def test_evaluate_detection_bias_low_risk(self):
        """Tests Domain 3 evaluation for blinded outcome assessment."""
        sections = PreEmptiveRiskOfBiasMitigator.parse_sections(self.compliant_proposal)
        d3 = PreEmptiveRiskOfBiasMitigator.evaluate_detection_bias(sections)
        self.assertEqual(d3.domain_id, "DOMAIN_3_DETECTION_BIAS")
        self.assertEqual(d3.risk_level, "LOW_RISK")

    def test_evaluate_attrition_bias_low_risk(self):
        """Tests Domain 4 evaluation for handling exclusions and outliers."""
        sections = PreEmptiveRiskOfBiasMitigator.parse_sections(self.compliant_proposal)
        d4 = PreEmptiveRiskOfBiasMitigator.evaluate_attrition_bias(sections)
        self.assertEqual(d4.domain_id, "DOMAIN_4_ATTRITION_BIAS")
        self.assertEqual(d4.risk_level, "LOW_RISK")

    def test_evaluate_reporting_bias_low_risk(self):
        """Tests Domain 5 evaluation for pre-registration."""
        sections = PreEmptiveRiskOfBiasMitigator.parse_sections(self.compliant_proposal)
        d5 = PreEmptiveRiskOfBiasMitigator.evaluate_reporting_bias(sections)
        self.assertEqual(d5.domain_id, "DOMAIN_5_REPORTING_BIAS")
        self.assertEqual(d5.risk_level, "LOW_RISK")

    def test_full_proposal_audit_low_risk(self):
        """Tests full audit yielding overall LOW_RISK."""
        result = PreEmptiveRiskOfBiasMitigator.audit_proposal(self.compliant_proposal)
        self.assertIsInstance(result, RiskOfBiasAuditResult)
        self.assertTrue(result.is_acceptable)
        self.assertEqual(result.overall_risk, "LOW_RISK")
        self.assertEqual(len(result.high_risk_domains), 0)

    def test_high_risk_flagged_on_unmitigated_proposal(self):
        """Tests that omitting blinding, randomization and exclusion criteria flags HIGH_RISK."""
        hollow_proposal = (
            "## 1. موضوع\nآزمایش ساده\n\n"
            "## 13. روش اجرا\nمحلول روی سلول‌ها ریخته می‌شود بدون هیچ تمهید دیگری."
        )
        result = PreEmptiveRiskOfBiasMitigator.audit_proposal(hollow_proposal)
        self.assertFalse(result.is_acceptable)
        self.assertEqual(result.overall_risk, "HIGH_RISK")
        self.assertGreater(len(result.high_risk_domains), 0)

    def test_report_generation_and_persistence(self):
        """Tests saving RISK_OF_BIAS_MITIGATION_REPORT.md and .json."""
        result = PreEmptiveRiskOfBiasMitigator.audit_proposal(self.compliant_proposal)
        with tempfile.TemporaryDirectory() as tmpdir:
            md_path, json_path = PreEmptiveRiskOfBiasMitigator.save_reports(result, output_dir=tmpdir)
            
            self.assertTrue(os.path.exists(md_path))
            self.assertTrue(os.path.exists(json_path))
            
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("Pre-emptive Risk of Bias Mitigation Report", content)
            self.assertIn("Selection Bias", content)
            
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertTrue(data["is_acceptable"])
            self.assertEqual(data["overall_risk"], "LOW_RISK")

    def test_readiness_gate_infrastructure_includes_rob_mitigator(self):
        """Verifies ProposalReadinessGate checks PreEmptiveRiskOfBiasMitigator in Phase 1."""
        res = ProposalReadinessGate.check_all(mode="PRE_GENERATION_INFRASTRUCTURE")
        self.assertTrue(res.can_proceed)
        self.assertIn("PreEmptiveRiskOfBiasMitigator", res.passed_modules)
        self.assertIn("PreEmptiveRiskOfBiasMitigator", ProposalReadinessGate.required_modules)


if __name__ == "__main__":
    unittest.main()
