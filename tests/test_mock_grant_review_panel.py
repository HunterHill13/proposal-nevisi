#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_mock_grant_review_panel.py - Test Suite for Mock Grant Review Panel & Inter-Section Semantic Drift Gate
Proposal-Nevisi Engine v10.0
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

from mock_grant_review_panel import MockGrantReviewPanel, ReviewerScore, PanelReviewResult
from proposal_readiness_gate import ProposalReadinessGate


def get_sample_compliant_28_sections() -> str:
    """Provides a synthetic 28-section proposal text with high rigor."""
    sections = [
        "## 1. موضوع\nبررسی هم‌افزایی ترکیب ماده الف و ویروس ب در رده‌های سلولی سرطان روده بزرگ",
        "## 2. بیان مسئله\n" + ("سرطان روده بزرگ یکی از شایع‌ترین علل مرگ‌ومیر ناشی از سرطان در سراسر جهان است. " * 15),
        "## 3. مرور بر منابع\n" + ("مطالعات پیشین (Rezaei et al., 2023) نشان داده‌اند که فعال‌سازی مسیر آپوپتوز نقش کلیدی دارد. [1] " * 15),
        "## 4. اهمیت وضرورت تحقیق\n" + ("مقاومت دارویی نیازمند توسعه استراتژی‌های ترکیبی با سمیت حداقلی برای بافت نرمال است. " * 8),
        "## 5. تعریف واژه ها\nشاخص ترکیب (CI): کمی‌سازی میزان هم‌افزایی یا آنتاگونیسم بر مبنای مدل چاو-تالالای.",
        "## 6. اهداف جزیی\n۱. سنجش بقای سلولی و viability سلول‌ها\n۲. ارزیابی آپوپتوز و apoptosis ناشی از تیمار ترکیبی\n۳. تعیین مهاجرت سلولی و migration با آزمون scratch",
        "## 7. اهداف کلی\nارزیابی اثرات ضد توموری هم‌افزا در مهار رشد رده‌های سلولی سرطان",
        "## 8. اهداف کاربردی\nتوسعه پروتکل‌های پیش‌بالینی جهت کارآزمایی‌های آینده",
        "## 9. فرضیات و سوالات\nآیا ترکیب ماده الف و ویروس ب دارای اثر سینرژیک (CI < 1) بر القای مرگ برنامه‌ریزی‌شده سلول‌ها می‌باشد؟",
        "## 10. دستاورد ها\nتولید داده‌های آزمایشگاهی دقیق و ثبت پتنت فرآیندی",
        "## 11. جدول متغیر ها\nمتغیر مستقل: غلظت داروها؛ متغیر وابسته: درصد viability و نرخ آپوپتوز و مهاجرت migration.",
        "## 12. جدول زمان بندی و مراحل اجرا\n| فاز | شرح مرحله | زمان‌بندی |\n|---|---|---|\n| فاز ۱ | کشت سلولی | ماه ۱ تا ۳ |\n| فاز ۲ | آزمون‌های زیستی | ماه ۴ تا ۶ |\n| فاز ۳ | آنالیز آماری | ماه ۷ تا ۹ |",
        "## 13. روش اجرا\nطرح تجربی با در نظر گرفتن گروه‌های کنترل منفی (سلول‌های تیمار نشده)، کنترل مثبت و کنترل حلال بر روی رده‌های سلولی سرطان اجرا می‌گردد.",
        "## 14. نوع مطالعه\nبنیادی - کاربردی (In vitro experimental)",
        "## 15. جامعه مورد مطالعه\nرده‌های سلولی توموری استاندارد خریداری‌شده از انستیتو پاستور",
        "## 16. محل انجام مطالعه\nمرکز تحقیقات سلولی و مولکولی دانشکده پزشکی",
        "## 17. معیار های ورود به مطالعه\nپاساژهای بین ۳ تا ۱۰، فاقد آلودگی مایکوپلاسما",
        "## 18. معیار های خروج از مطالعه\nرشد کندتر از نرخ نرمال، آلودگی باکتریایی",
        "## 19. ابزار های گردآوری اطلاعات\nدستگاه الایزا ریدر، فلوسایتومتری، میکروسکوپ اینورت",
        "## 20. تعیین اعتبار ابزار گردآوری\nکالیبراسیون دوره‌ای تجهیزات و کنترل‌های داخلی مثبت و منفی",
        "## 21. تعیین ابزار گردآوری\nاستفاده از کیت‌های استاندارد آنکسین V و MTT با حساسیت تایید شده",
        "## 22. حجم نمونه و روش محاسبه آن\nحجم نمونه بر اساس توان آزمون ۸۰٪ و سطح خطای ۵٪ محاسبه شده و تمامی سنجش‌ها در ۳ تکرار مستقل زیستی (biological replicates) و ۳ تکرار تکنیکال (n=3) انجام می‌پذیرد تا تکرارپذیری داده‌ها و عدم خطای اندازه‌گیری تضمین گردد.",
        "## 23. روش تجزیه و تحلیل داده\nداده‌ها با آزمون Two-way ANOVA و آزمون تعقیبی Tukey در سطح معناداری P < 0.05 تحلیل می‌شوند.",
        "## 24. ملاحظلات اخلاقی در صورت نیاز\nکد اخلاق سازمانی به شماره IR.MUMS.REC.1402.120 اخذ شده و کلیه آزمایش‌ها منطبق بر موازین کدهای ۳۱ گانه اخلاق در پژوهش‌های زیست‌پزشکی و بیولوژیک و رعایت شیوه‌نامه‌های رسمی کمیته اخلاق سازمانی اجرا خواهد شد.",
        "## 25. نحوه رعایت نکات امنیتی و حفاظت پروژه در صورت نیاز\nکلیه مراحل کار با کشت سلول و ویروس در هود لامینار کلاس ۲ بیولوژیک (BSL-2) با رعایت کامل اصول ایمنی زیستی، استفاده از تجهیزات حفاظت فردی و اتوکلاو پسماندهای بیولوژیک پیش از دفع نهایی انجام خواهد شد.",
        "## 26. مشکلات و محدودیت ها\nاحتمال بروز موتاسیون‌های ثانویه یا نوسانات در نرخ تکثیر سلولی در پاساژهای بالا به عنوان محدودیت فنی مطالعه مد نظر است که با محدود کردن آزمایش‌ها به پاساژهای ۳ تا ۸ کنترل می‌گردد.",
        "## 27. روش انجام طرح، شیوه اجرایی مراحل طرح و چگونگی جمع آوری اطلاعات\nآزمون بقای MTT برای viability، آزمون آنکسین فلوسایتومتری برای apoptosis، و آزمون خراش برای migration با گروه‌های کنترل مطابق پروتکل معتبر اجرا خواهد شد.",
        "## 28. منابعی که استفاده شد\n[1] Rezaei et al. Synergistic antitumor effects. Int J Cancer 2023.\n[2] Chou TC. Drug combination studies. Pharmacol Rev 2006."
    ]
    return "\n\n".join(sections)


class TestMockGrantReviewPanel(unittest.TestCase):
    """Test cases for MockGrantReviewPanel study section evaluation."""

    def setUp(self):
        self.compliant_proposal = get_sample_compliant_28_sections()

    def test_parse_proposal_sections(self):
        """Verifies 1-to-1 parsing of 28 canonical proposal sections."""
        parsed = MockGrantReviewPanel.parse_proposal_sections(self.compliant_proposal)
        self.assertEqual(len(parsed), 28)
        self.assertIn(1, parsed)
        self.assertIn(28, parsed)
        self.assertIn("هم‌افزایی", parsed[1])
        self.assertIn("Two-way ANOVA", parsed[23])

    def test_reviewer_1_scientific_merit(self):
        """Tests Reviewer 1 evaluation of scientific merit, significance, and hypotheses."""
        parsed = MockGrantReviewPanel.parse_proposal_sections(self.compliant_proposal)
        r1 = MockGrantReviewPanel.evaluate_reviewer_1_scientific_merit(parsed)
        self.assertEqual(r1.reviewer_id, "REVIEWER_1")
        self.assertLessEqual(r1.score, 3.0)
        self.assertEqual(len(r1.critical_flaws), 0)
        self.assertGreaterEqual(len(r1.strengths), 2)

    def test_reviewer_2_methodology_and_drift(self):
        """Tests Reviewer 2 evaluation of biostatistics, replicates, and inter-section drift."""
        parsed = MockGrantReviewPanel.parse_proposal_sections(self.compliant_proposal)
        r2, drift = MockGrantReviewPanel.evaluate_reviewer_2_methodology_and_alignment(parsed)
        self.assertEqual(r2.reviewer_id, "REVIEWER_2")
        self.assertLessEqual(r2.score, 3.0)
        self.assertEqual(len(r2.critical_flaws), 0)
        self.assertFalse(drift["drift_detected"])
        self.assertEqual(drift["alignment_score"], 1.0)

    def test_inter_section_semantic_drift_detection(self):
        """Tests that aim without corresponding assay in methods triggers drift detection."""
        flawed_text = (
            "## 6. اهداف جزیی\n۱. بررسی آپوپتوز و apoptosis\n۲. بررسی مهاجرت و migration سلولی\n\n"
            "## 11. جدول متغیر ها\nمتغیر مستقل داروها، متغیر وابسته بقا و viability\n\n"
            "## 27. روش انجام طرح، شیوه اجرایی مراحل طرح و چگونگی جمع آوری اطلاعات\nتنها آزمون MTT جهت سنجش viability با کنترل منفی انجام خواهد شد و آزمایش دیگری انجام نمی‌شود.\n\n"
            "## 22. حجم نمونه و روش محاسبه آن\nتکرار سه‌گانه n=3\n\n"
            "## 23. روش تجزیه و تحلیل داده\nآزمون t-test"
        )
        parsed = MockGrantReviewPanel.parse_proposal_sections(flawed_text)
        r2, drift = MockGrantReviewPanel.evaluate_reviewer_2_methodology_and_alignment(parsed)
        
        self.assertTrue(drift["drift_detected"])
        self.assertGreater(len(drift["unaligned_aims_in_methods"]), 0)
        self.assertGreater(r2.score, 3.0)
        self.assertTrue(any("INTER_SECTION_DRIFT" in cf for cf in r2.critical_flaws))

    def test_reviewer_3_bioethics_and_feasibility(self):
        """Tests Reviewer 3 evaluation of ethics codes, biosafety, Gantt schedule, and limitations."""
        parsed = MockGrantReviewPanel.parse_proposal_sections(self.compliant_proposal)
        r3 = MockGrantReviewPanel.evaluate_reviewer_3_bioethics_and_feasibility(parsed)
        self.assertEqual(r3.reviewer_id, "REVIEWER_3")
        self.assertLessEqual(r3.score, 3.0)
        self.assertEqual(len(r3.critical_flaws), 0)
        self.assertTrue(any("کد" in s or "اخلاق" in s for s in r3.strengths))
        self.assertTrue(any("ایمنی" in s for s in r3.strengths))

    def test_full_panel_conduct_fundable(self):
        """Tests full Mock Study Section approval for a rigorous compliant proposal."""
        result = MockGrantReviewPanel.conduct_panel_review(self.compliant_proposal)
        self.assertIsInstance(result, PanelReviewResult)
        self.assertTrue(result.can_proceed)
        self.assertEqual(result.funding_verdict, "APPROVED_FUNDABLE")
        self.assertLessEqual(result.overall_score, 3.5)
        self.assertEqual(result.critical_flaws_count, 0)

    def test_report_generation_and_persistence(self):
        """Tests generation and disk persistence of MOCK_GRANT_REVIEW_REPORT.md and .json."""
        result = MockGrantReviewPanel.conduct_panel_review(self.compliant_proposal)
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file, json_file = MockGrantReviewPanel.save_reports(result, output_dir=tmpdir)
            
            self.assertTrue(os.path.exists(md_file))
            self.assertTrue(os.path.exists(json_file))
            
            with open(md_file, "r", encoding="utf-8") as f:
                md_content = f.read()
            self.assertIn("Mock Grant Review Summary Report", md_content)
            self.assertIn("Inter-Section Semantic Drift", md_content)
            
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["funding_verdict"], "APPROVED_FUNDABLE")
            self.assertIn("REVIEWER_1", data["reviewer_evaluations"])

    def test_readiness_gate_infrastructure_includes_mock_review(self):
        """Tests that ProposalReadinessGate verifies MockGrantReviewPanel in infrastructure mode."""
        res = ProposalReadinessGate.check_all(mode="PRE_GENERATION_INFRASTRUCTURE")
        self.assertTrue(res.can_proceed)
        self.assertIn("MockGrantReviewPanel", res.passed_modules)
        self.assertIn("MockGrantReviewPanel", ProposalReadinessGate.required_modules)


if __name__ == "__main__":
    unittest.main()
