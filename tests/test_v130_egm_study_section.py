#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_v130_egm_study_section.py - Unit Test Suite for EGM-Powered Grant Study Section
Proposal-Nevisi Engine v13.0 (Elephant-Goldfish Hybrid Architecture)

Tests:
1. Section parser for Pajooheshyar markdown
2. 5 Goldfish lenses (Significance, Methodology, Evidence, Feasibility, Ethics)
3. SRO Swarm Synthesis & NIH 1-9 Scoring Rubric
4. Full Integration with MockGrantReviewPanel & IterativeRemediationEngine
5. Deliverables generation (EGM_GRANT_STUDY_SECTION_REPORT.md & .json)
"""

import os
import sys
import unittest
import tempfile
import shutil
import json

scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from egm_study_section_subagents import (
    EGMStudySectionCoordinator,
    EGMStudySectionResult,
    GoldfishReviewerResult,
    GoldfishFinding
)
from mock_grant_review_panel import MockGrantReviewPanel, PanelReviewResult
from iterative_remediation_engine import IterativeRemediationEngine
from generate_compliant_proposal import ProposalGenerator


class TestV130EGMStudySection(unittest.TestCase):
    """Test suite for EGM-powered grant review swarm."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_egm_v130_")
        self.sample_complete_proposal = """
## ۱. موضوع
ارزیابی اثربخشی راهکارهای مداخله‌ای در کاهش هزینه‌های کمرشکن سلامت (CHE) در بیماران مبتلا به نئوپلاسم

## ۲. بیان مسئله
بیماری‌های انکولوژی بار اقتصادی و بالینی فزاینده‌ای بر نظام‌های سلامت تحمیل می‌کنند. بر اساس آمارهای معتبر سالانه هزینه‌های سرسام‌آور درمان منجر به رخداد هزینه‌های کمرشکن سلامت (Catastrophic Health Expenditure - CHE) در خانوارهای مبتلا می‌گردد. داده‌های بروز و شیوع بر اساس گزارش‌های ملی سلامت نشان‌دهنده لزوم سیاست‌گذاری جامع است.

## ۳. مرور بر منابع
مطالعات مقطعی و طولی نشان داده‌اند که هزینه‌های بستری و داروهای نوترکیب نقش اساسی در افزایش پرداخت از جیب دارند [PMID: 32329697]. همچنین شواهد پیشین بیانگر نابرابری در بهره‌مندی از خدمات تشخیصی می‌باشند [PMID: 31234567].

## ۴. اهمیت و ضرورت تحقیق
نوآوری و اهمیت این طرح در شناسایی عوامل پیش‌بینی‌کننده بار مالی و هدایت بسته‌های حمایتی بیمه پایه و تکمیلی به منظور دستیابی به پوشش همگانی سلامت است.

## ۹. فرضیات و سوالات
- فرضیه اول (H1): میانگین پرداخت از جیب (OOP) در بیماران دارای بیمه تکمیلی به طور معناداری کمتر از بیماران فاقد بیمه است.
- سوال پژوهش: عوامل دموگرافیک چه میزان بر نسبت شانس مواجهه با مخارج کمرشکن تاثیرگذارند؟

## ۱۱. جدول متغیر ها
| نام متغیر | نقش متغیر | مقیاس سنجش | تعریف عملیاتی |
| :--- | :--- | :--- | :--- |
| وقوع CHE | وابسته | کیفی دوحالته | مخارج سلامت >= ۴۰٪ ظرفیت پرداخت |
| پرداخت از جیب (OOP) | وابسته | کمی پیوسته | کل مبالغ پرداختی توسط بیمار |
| پوشش بیمه‌ای | مستقل | کیفی اسمی | داشتن بیمه پایه یا تکمیلی |

## ۱۲. جدول زمان بندی و مراحل اجرا
| ردیف | شرح مرحله | ماه ۱-۲ | ماه ۳-۴ | ماه ۵-۶ |
| :---: | :--- | :---: | :---: | :---: |
| ۱ | نمونه‌گیری و تکمیل پرسشنامه‌ها | ███ | | |
| ۲ | استخراج داده‌های مالی از سامانه HIS | | ███ | |
| ۳ | آنالیز رگرسیون چندمتغیره و گزارش نهایی | | | ███ |

## ۱۳. روش اجرا
طرح مقطعی تحلیلی در مراکز درمانی تابعه دانشگاه انجام خواهد شد.

## ۱۴. نوع مطالعه
مقطعی تحلیلی (Cross-Sectional Analytical Study)

## ۱۵. جامعه مورد مطالعه
کلیه بیماران مبتلا به سرطان مراجعه‌کننده به بیمارستان‌های آموزشی در طول سال پژوهش.

## ۱۶. محل انجام مطالعه
بیمارستان‌های آموزشی-درمانی و مراکز انکولوژی تابعه دانشگاه علوم پزشکی.

## ۱۷. معیارهای ورود به مطالعه
تشخیص قطعی پاتولوژیک، دریافت حداقل یک دوره درمان، و تمایل آگاهانه به مشارکت.

## ۱۸. معیارهای خروج از مطالعه
عدم تکمیل بخش اصلی پرسشنامه یا انصراف داوطلبانه از مطالعه.

## ۱۹. ابزارهای گردآوری اطلاعات
پرسشنامه استاندارد سلامت جهانی (WHO World Health Survey) و استخراج صورت‌حساب‌های سامانه اطلاعات بیمارستانی (HIS).

## ۲۰. تعیین اعتبار ابزار گردآوری
محاسبه ضریب روایی محتوا (CVI) و نسبت روایی محتوا (CVR) با مشارکت پنل متخصصین.

## ۲۱. تعیین پایایی ابزار گردآوری
آزمون پایایی با ضریب آلفای کرونباخ با ضریب اطمینان بالای ۰.۸۵ و بازآزمایی.

## ۲۲. حجم نمونه و روش محاسبه آن
محاسبه حجم نمونه بر اساس فرمول کوکران برای جوامع با نسبت مشخص با آلفای ۰.۰۵ و ضریب اثر طرح DEFF=1.5 برابر ۶۴۲ خانوار برآورد گردید:
$n = \frac{z^2 p (1-p)}{d^2} \times DEFF$

## ۲۳. روش تجزیه و تحلیل داده
تجزیه و تحلیل داده‌ها با رگرسیون لجستیک چندمتغیره (Multivariable Logistic Regression) برای برآورد نسبت‌های شانس تعدیل‌شده (AOR) با فاصله اطمینان ۹۵٪ در نرم‌افزار Stata/SPSS انجام می‌پذیرد.

## ۲۴. ملاحظات اخلاقی در صورت نیاز
رعایت کلیه موازین بیانیه هلسینکی، اخذ رضایت‌نامه کتبی آگاهانه، و تصویب طرح در کمیته اخلاق در پژوهش‌های زیست‌پزشکی دانشگاه.

## ۲۵. نحوه رعایت نکات امنیتی و حفاظت پروژه در صورت نیاز
اطلاعات شخصی افراد با کدگذاری محرمانه و رمزنگاری AES-256 ذخیره و فایل‌های کاغذی به صورت کاملاً ایمن نگهداری می‌شوند.

## ۲۶. محدودیت‌های احتمالی پژوهش
سوگیری یادآوری (Recall Bias) در هزینه‌های خارج بیمارستانی کنترل می‌گردد.

## ۲۷. مراحل تفصیلی پروتکل
۱. غربالگری پرونده‌ها، ۲. مصاحبه و ثبت هزینه‌ها، ۳. کنترل داده با سامانه مالی، ۴. آنالیز نهایی.
"""

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_01_egm_section_parser(self):
        """Test 1: Parser extracts canonical Pajooheshyar section numbers."""
        sections = EGMStudySectionCoordinator.parse_proposal_sections(self.sample_complete_proposal)
        self.assertIn(1, sections)
        self.assertIn(2, sections)
        self.assertIn(22, sections)
        self.assertIn(23, sections)
        self.assertIn(24, sections)
        self.assertTrue(len(sections) >= 20)

    def test_02_egm_significance_innovation_evaluator(self):
        """Test 2: Lens 1 (egm-zoom-out) evaluates significance, burden and novelty."""
        sections = EGMStudySectionCoordinator.parse_proposal_sections(self.sample_complete_proposal)
        res = EGMStudySectionCoordinator.evaluate_significance_and_innovation(sections, {})
        self.assertEqual(res.status, "completed")
        self.assertEqual(res.egm_lens, "egm-zoom-out")
        self.assertTrue(res.nih_score <= 2.5)
        self.assertTrue(len(res.strengths) >= 1)

    def test_03_egm_methodology_biostatistics_evaluator(self):
        """Test 3: Lens 2 (egm-design) evaluates methodology, sample size, and statistics."""
        sections = EGMStudySectionCoordinator.parse_proposal_sections(self.sample_complete_proposal)
        res = EGMStudySectionCoordinator.evaluate_methodology_and_biostatistics(sections, {})
        self.assertEqual(res.status, "completed")
        self.assertEqual(res.egm_lens, "egm-design")
        # Sample size and regression are both present, so no blockers
        self.assertEqual(len(res.blockers), 0)
        self.assertTrue(res.nih_score <= 2.5)

    def test_04_egm_evidence_entailment_evaluator(self):
        """Test 4: Lens 3 (egm-codebase-details) checks literature citations."""
        sections = EGMStudySectionCoordinator.parse_proposal_sections(self.sample_complete_proposal)
        res = EGMStudySectionCoordinator.evaluate_evidence_entailment(sections, {})
        self.assertEqual(res.status, "completed")
        self.assertEqual(res.egm_lens, "egm-codebase-details")
        self.assertEqual(len(res.blockers), 0)

    def test_05_egm_feasibility_and_ethics_evaluators(self):
        """Test 5: Lens 4 (readiness) & Lens 5 (comprehension) evaluate logistics and bioethics."""
        sections = EGMStudySectionCoordinator.parse_proposal_sections(self.sample_complete_proposal)
        res_feas = EGMStudySectionCoordinator.evaluate_feasibility_and_logistics(sections, {})
        res_eth = EGMStudySectionCoordinator.evaluate_ethics_and_lay_comprehension(sections, {})
        self.assertEqual(res_feas.status, "completed")
        self.assertEqual(res_eth.status, "completed")
        self.assertEqual(len(res_eth.blockers), 0)

    def test_06_egm_sro_synthesis_and_nih_scoring(self):
        """Test 6: SRO Swarm Compiler normalizes findings and assigns NIH impact score."""
        study_res = EGMStudySectionCoordinator.conduct_full_study_section_review(
            self.sample_complete_proposal, {}
        )
        self.assertIsInstance(study_res, EGMStudySectionResult)
        self.assertTrue(1.0 <= study_res.overall_nih_score <= 9.0)
        self.assertEqual(study_res.funding_verdict, "APPROVED_FUNDABLE")
        self.assertTrue(study_res.can_proceed)
        self.assertTrue(study_res.percentile >= 80.0)

    def test_07_egm_report_generation_and_saving(self):
        """Test 7: Generates markdown report and persists files to disk."""
        study_res = EGMStudySectionCoordinator.conduct_full_study_section_review(
            self.sample_complete_proposal, {}
        )
        md_text = EGMStudySectionCoordinator.generate_report_markdown(study_res, "طرح سلامت")
        self.assertIn("کارنامه رسمی نشست داوری گرنت‌های پزشکی", md_text)
        self.assertIn("NIH Impact Score", md_text)
        self.assertIn("egm-zoom-out", md_text)

        md_path, json_path = EGMStudySectionCoordinator.save_reports(study_res, self.test_dir, "طرح آزمایشی")
        self.assertTrue(os.path.exists(md_path))
        self.assertTrue(os.path.exists(json_path))

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("overall_nih_score", data)
        self.assertIn("reviewer_results", data)

    def test_08_mock_grant_review_panel_egm_integration(self):
        """Test 8: MockGrantReviewPanel executes Tier 1 and Tier 2 with EGM study section."""
        panel_res = MockGrantReviewPanel.conduct_panel_review(self.sample_complete_proposal, {})
        self.assertIsInstance(panel_res, PanelReviewResult)
        self.assertIsNotNone(panel_res.egm_study_section)
        self.assertIn("overall_nih_score", panel_res.egm_study_section)

        md_path, json_path = MockGrantReviewPanel.save_reports(panel_res, self.test_dir)
        self.assertTrue(os.path.exists(md_path))
        self.assertTrue(os.path.exists(json_path))
        # Ensure EGM deliverables are also created
        egm_md = os.path.join(self.test_dir, "EGM_GRANT_STUDY_SECTION_REPORT.md")
        egm_json = os.path.join(self.test_dir, "EGM_GRANT_STUDY_SECTION_REPORT.json")
        self.assertTrue(os.path.exists(egm_md))
        self.assertTrue(os.path.exists(egm_json))

    def test_09_iterative_remediation_egm_issue_ingestion(self):
        """Test 9: IterativeRemediationEngine ingests EGM findings and executes patches."""
        # Inject deliberate flaw into sample proposal
        flawed_md = self.sample_complete_proposal.replace(
            "محاسبه حجم نمونه بر اساس فرمول کوکران برای جوامع با نسبت مشخص با آلفای ۰.۰۵ و ضریب اثر طرح DEFF=1.5 برابر ۶۴۲ خانوار برآورد گردید:\n$n = \\frac{z^2 p (1-p)}{d^2} \\times DEFF$",
            "حجم نمونه به دلخواه ۱۰ نفر انتخاب شد."
        )
        data = {
            "title_fa": "ارزیابی اثربخشی راهکارهای مداخله‌ای در کاهش هزینه‌های کمرشکن سلامت (CHE) در بیماران مبتلا به نئوپلاسم",
            "research_title_fa": "ارزیابی اثربخشی راهکارهای مداخله‌ای در کاهش هزینه‌های کمرشکن سلامت (CHE) در بیماران مبتلا به نئوپلاسم",
            "framework": "HEALTH_SYSTEMS_AND_HEALTH_POLICY",
            "domain": "health_economics_and_policy",
            "max_iterations": 10
        }
        remediation_res = IterativeRemediationEngine.remediate_proposal(
            md_content=flawed_md,
            proposal_data=data,
            max_iterations=10,
            output_dir=self.test_dir
        )
        self.assertIn("final_markdown", remediation_res)
        self.assertIn("audit_trail", remediation_res)
        self.assertTrue(remediation_res["is_approved"])
        self.assertLessEqual(remediation_res["final_review"]["overall_score"], 1.5)
        self.assertEqual(remediation_res["final_review"]["critical_flaws_count"], 0)

    def test_10_end_to_end_generator_egm_artifacts(self):
        """Test 10: ProposalGenerator produces compliant proposal with EGM reports."""
        md_file = os.path.join(self.test_dir, "proposal.md")
        docx_file = os.path.join(self.test_dir, "proposal.docx")
        data = {
            "title_fa": "بررسی هزینه‌های کمرشکن سلامت (CHE) در سرطان در ایران",
            "research_title_fa": "بررسی هزینه‌های کمرشکن سلامت (CHE) در سرطان در ایران",
            "title_en": "Evaluation of Catastrophic Health Expenditure in Cancer",
            "framework": "HEALTH_SYSTEMS_AND_HEALTH_POLICY",
            "domain": "health_economics_and_policy",
            "max_iterations": 10
        }
        res = ProposalGenerator.generate_and_save(data, md_file, docx_file, format="28")
        self.assertEqual(res["status"], "PASS")
        self.assertTrue(os.path.exists(md_file))
        self.assertTrue(os.path.exists(docx_file))

        egm_md = os.path.join(self.test_dir, "EGM_GRANT_STUDY_SECTION_REPORT.md")
        egm_json = os.path.join(self.test_dir, "EGM_GRANT_STUDY_SECTION_REPORT.json")
        self.assertTrue(os.path.exists(egm_md))
        self.assertTrue(os.path.exists(egm_json))


if __name__ == "__main__":
    unittest.main()
