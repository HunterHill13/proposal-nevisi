#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_v142_seven_archetypes_and_forensic_fixes.py - Release Verification Suite for Proposal-Nevisi v14.2.0

Covers:
1. Canonical 7 archetypes + usability polymorphism across classifier, subagent, protocol designer,
   proposal generator, EQUATOR auditor, RoB mitigator, biostatistics validator, EGM & Mock panels.
2. Fail-closed behavior on unrecognized "unknown" study inputs.
3. Heading parser immunity against ### subheadings (e.g. ### ۱. بار بیماری) and 14-sec ### ۱۳-۱.
4. DocxBuilder 3-branch callout box rendering & dynamic cover metadata extraction (14-sec vs 28-sec).
5. MeSHQueryExpander <= 3 semantic AND blocks invariant & stopword hygiene.
6. Parent scripts/verify_biostatistics.py thin delegating shim verification.
"""

import os
import sys
import subprocess
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
SKILL_ROOT = TESTS_DIR.parent
SCRIPTS_DIR = SKILL_ROOT / "scripts"
REPO_ROOT = SKILL_ROOT.parent.parent.parent

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from docx import Document

import core_policies
from core_policies import (
    NIH_APPROVAL_SCORE_CEILING,
    classify_study_archetype,
    parse_proposal_sections,
)
from methodology_research_subagent import MethodologyResearchSubagent
from dynamic_protocol_designer import DynamicProtocolDesigner
from generate_compliant_proposal import ProposalGenerator
from methodology_completeness_gate import MethodologyCompletenessGate, SAMPLE_SIZE_FORMULA_PATTERNS
from equator_compliance_auditor import EquatorComplianceAuditor
from pre_emptive_risk_of_bias_mitigator import PreEmptiveRiskOfBiasMitigator, BaselinePaperQualityAuditor
from verify_biostatistics import BiostatisticalValidator
from egm_study_section_subagents import EGMStudySectionCoordinator, EGMStudySectionResult
from mock_grant_review_panel import MockGrantReviewPanel
from docx_builder import add_callout_box, extract_proposal_metadata
from mesh_query_expander import MeSHQueryExpander


class TestV142SevenArchetypesAndForensicFixes(unittest.TestCase):
    """Comprehensive v14.2.0 regression and polymorphism test suite."""

    def test_01_classify_all_seven_archetypes_plus_usability_and_unknown(self):
        cases = [
            ("ارزیابی مواجهه با هزینه‌های کمرشکن سلامت (CHE) در خانوارها", "health_systems"),
            ("مطالعه مقطعی شیوع و عوامل خطر دیابت نوع ۲ در بزرگسالان", "epidemiological"),
            ("کارآزمایی بالینی تصادفی دوسوکور بررسی اثر امپاگلیفلوزین بر HbA1c", "clinical_rct"),
            ("ارزیابی اثر محافظت عصبی پروبیوتیک در موش‌های نر ویستار مدل آسیب ایسکمیک", "in_vivo"),
            ("بررسی اثر سمیت سلولی عصاره استاندارد در رده سلولی کشت شده در محیط برون‌تن", "in_vitro"),
            ("تعیین دقت تشخیصی، حساسیت و ویژگی بیومارکر سرمی و منحنی ROC در پنومونی", "diagnostic"),
            ("مرور دامنه‌ای (Scoping Review) و سنتز شواهد مداخلات تله‌مدیسین با PRISMA-ScR و JBI", "scoping_review"),
            ("ارزیابی کاربردپذیری (Usability) سامانه سلامت دیجیتال با روش اکتشافی نیلسن و مقیاس SUS", "usability"),
            ("پروژه عمومی توصیف وضعیت پژوهش بدون شاخص طراحی مطالعه", "unknown"),
        ]
        for text, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(classify_study_archetype(text), expected)

    def test_02_subheading_immunity_and_14_section_parsing(self):
        md = (
            "## ۱. موضوع\n"
            "▪ **عنوان فارسی:** عنوان اصیل اول\n"
            "▪ **عنوان انگلیسی:** Authentic First Title\n\n"
            "## ۲. بیان مسئله\n"
            "### ۱. بار بیماری و اپیدمیولوژی\n"
            "توضیح بار بیماری که نباید روی بخش اول بنشیند.\n\n"
            "## ۱۳. روش اجرا\n"
            "### ۱۳-۱. نوع مطالعه\n"
            "مطالعه مقطعی تحلیلی\n"
            "### ۱۳-۹. حجم نمونه و روش محاسبه آن\n"
            "فرمول کوکران n = 384\n\n"
            "## ۲۲. حجم نمونه و روش محاسبه آن\n"
            "فرمول PRISMA-ScR و اشباع شواهد در جستجوی جامع\n"
        )
        secs = parse_proposal_sections(md)
        self.assertIn("عنوان اصیل اول", secs[1])
        self.assertNotIn("توضیح بار بیماری", secs[1])
        self.assertIn("بار بیماری", secs[2])

        egm_secs = EGMStudySectionCoordinator.parse_proposal_sections(md)
        self.assertIn("عنوان اصیل اول", egm_secs[1])
        self.assertNotIn("توضیح بار بیماری", egm_secs[1])

        gate_secs = MethodologyCompletenessGate._extract_sections_from_markdown(md)
        self.assertIn("عنوان اصیل اول", gate_secs["موضوع"])
        self.assertNotIn("توضیح بار بیماری", gate_secs["موضوع"])
        self.assertIn("مطالعه مقطعی تحلیلی", gate_secs["نوع مطالعه"])

    def test_03_fail_closed_unknown_archetype_across_modules(self):
        unknown_topic = "بررسی کلی یک موضوع عمومی بدون تعیین طرح پژوهش"
        self.assertEqual(MethodologyResearchSubagent.identify_study_archetype(unknown_topic), "UNKNOWN_STUDY_ARCHETYPE")

        proto = MethodologyResearchSubagent.derive_cohesive_protocol(unknown_topic)
        self.assertEqual(proto.archetype, "UNKNOWN_STUDY_ARCHETYPE")
        self.assertEqual(proto.formatted_sections_fa, {})

        unknown_md = ProposalGenerator.assemble_pajooheshyar_28({"title_fa": unknown_topic})
        self.assertNotIn("Chou-Talalay", unknown_md)
        self.assertNotIn("MTT", unknown_md)

        bio_res = BiostatisticalValidator.verify_sample_size("n = 25 با فرمول نامشخص", "unknown")
        self.assertEqual(bio_res["coherence_status"], "UNVERIFIED")
        self.assertGreater(bio_res["nih_biostatistical_penalty"], 0.0)

        eq_res = EquatorComplianceAuditor.audit_proposal("## 1. موضوع\nموضوع نامشخص عمومی")
        self.assertFalse(eq_res.is_compliant)
        self.assertGreater(len(eq_res.critical_deficits), 0)

    def test_04_scoping_review_and_usability_polymorphic_generation_and_reviews(self):
        scoping_data = {
            "title_fa": "مرور دامنه‌ای (Scoping Review) کاربردهای تله‌مدیسین در مدیریت دیابت بر پایه PRISMA-ScR و JBI",
            "title_en": "Scoping Review of Telemedicine in Diabetes Care",
            "framework": "SCOPING_REVIEW",
            "study_family": "scoping_review",
            "target_condition": {"name_fa": "دیابت نوع ۲", "name_en": "Type 2 Diabetes"},
            "interventions_or_exposures": [{"name": "تله‌مدیسین"}],
            "population_or_model": {"primary_system": "بیماران مبتلا به دیابت نوع ۲"},
            "primary_outcomes": [{"name": "پوشش شواهد و پیامدهای بالینی"}],
            "studies": [
                {
                    "citation_number": 1,
                    "title": "Telemedicine scoping review in primary diabetes management",
                    "authors": ["Ahmadi R"],
                    "year": 2024,
                    "journal": "Journal of Telemedicine",
                    "pmid": "39111111",
                    "evidence_role": "DIRECT_INTERVENTION",
                    "final_inclusion_reason": "DIRECT_EVIDENCE",
                }
            ],
        }
        scoping_md = ProposalGenerator.assemble_pajooheshyar_28(scoping_data)
        self.assertIn("PRISMA-ScR", scoping_md)
        self.assertNotIn("MTT", scoping_md)
        self.assertNotIn("استاروسپورین", scoping_md)

        eq_scoping = EquatorComplianceAuditor.audit_proposal(scoping_md, {"study_family": "scoping_review"})
        self.assertEqual(eq_scoping.applicable_guidelines, ["PRISMA_SCR_JBI"])
        self.assertTrue(eq_scoping.is_compliant)

        rob_scoping = PreEmptiveRiskOfBiasMitigator.audit_proposal(scoping_md, {"study_family": "scoping_review"})
        self.assertTrue(rob_scoping.is_acceptable)
        self.assertNotIn("ToxRTool", rob_scoping.executive_summary_fa)

        egm_scoping = EGMStudySectionCoordinator.conduct_full_study_section_review(scoping_md, scoping_data)
        self.assertEqual(egm_scoping.total_blockers, 0)
        self.assertLessEqual(egm_scoping.overall_nih_score, NIH_APPROVAL_SCORE_CEILING)
        self.assertEqual(egm_scoping.funding_verdict, "APPROVED_FUNDABLE")
        rep_md = EGMStudySectionCoordinator.generate_report_markdown(egm_scoping, scoping_data["title_fa"])
        self.assertIn("Structural Completeness Index", rep_md)
        self.assertIn("NIH Impact Score", rep_md)
        self.assertNotIn("رتبه درصدی مصوب", rep_md)

        panel_scoping = MockGrantReviewPanel.conduct_panel_review(scoping_md, scoping_data)
        self.assertEqual(panel_scoping.critical_flaws_count, 0)
        self.assertEqual(panel_scoping.funding_verdict, "APPROVED_FUNDABLE")

        ux_data = {
            "title_fa": "ارزیابی کاربردپذیری (Usability) اپلیکیشن پایش سلامت با مدل نیلسن و مقیاس SUS",
            "title_en": "Usability Evaluation of Digital Health Application",
            "framework": "USABILITY_AND_DIGITAL_HEALTH",
            "study_family": "usability",
            "target_condition": {"name_fa": "فشار خون بالا", "name_en": "Hypertension"},
            "interventions_or_exposures": [{"name": "اپلیکیشن موبایل سلامت"}],
            "population_or_model": {"primary_system": "کاربران و بیماران سرپایی"},
            "primary_outcomes": [{"name": "نمره کاربردپذیری SUS"}],
            "studies": scoping_data["studies"],
        }
        ux_md = ProposalGenerator.assemble_pajooheshyar_28(ux_data)
        self.assertIn("Nielsen", ux_md)
        self.assertIn("SUS", ux_md)

        eq_ux = EquatorComplianceAuditor.audit_proposal(ux_md, {"study_family": "usability"})
        self.assertEqual(eq_ux.applicable_guidelines, ["USABILITY_NIELSEN_SUS"])
        self.assertTrue(eq_ux.is_compliant)

        rob_ux = PreEmptiveRiskOfBiasMitigator.audit_proposal(ux_md, {"study_family": "usability"})
        self.assertTrue(rob_ux.is_acceptable)

        egm_ux = EGMStudySectionCoordinator.conduct_full_study_section_review(ux_md, ux_data)
        self.assertEqual(egm_ux.total_blockers, 0)
        self.assertLessEqual(egm_ux.overall_nih_score, NIH_APPROVAL_SCORE_CEILING)

        panel_ux = MockGrantReviewPanel.conduct_panel_review(ux_md, ux_data)
        self.assertEqual(panel_ux.critical_flaws_count, 0)
        self.assertEqual(panel_ux.funding_verdict, "APPROVED_FUNDABLE")

    def test_05_remaining_archetypes_equator_biostat_and_rob(self):
        # Clinical RCT
        eq_rct = EquatorComplianceAuditor.detect_applicable_guidelines({14: "کارآزمایی بالینی تصادفی دوسوکور"})
        self.assertEqual(eq_rct, ["CONSORT_2010"])
        plan_rct = DynamicProtocolDesigner.calculate_sample_size_plan("CLINICAL_TRIAL")
        self.assertEqual(plan_rct["design_type"], "CLINICAL_TRIAL")

        # Diagnostic
        eq_diag = EquatorComplianceAuditor.detect_applicable_guidelines({14: "مطالعه دقت تشخیصی، حساسیت و ویژگی STARD"})
        self.assertEqual(eq_diag, ["STARD_2015"])

        # Epidemiological
        eq_epi = EquatorComplianceAuditor.detect_applicable_guidelines({14: "مطالعه مقطعی شیوع عوامل خطر STROBE"})
        self.assertEqual(eq_epi, ["STROBE_STATEMENT"])

        # Short snippet cell culture without non-lab markers still detects OECD_GCCP_CELL_CULTURE
        eq_cell = EquatorComplianceAuditor.detect_applicable_guidelines({14: "کشت سلول"})
        self.assertIn("OECD_GCCP_CELL_CULTURE", eq_cell)

        # Single-argument backwards compatibility on RoB D3/D4/D5 and "Selection Bias" title
        secs = {
            6: "تعیین زیست‌پذیری سلولی",
            13: "کورسازی ارزیاب با اسپکتروفتومتر",
            18: "معیار خروج شامل آلودگی میکروبی چاهک کشت و بررسی داده‌های پرت است " * 3,
            23: "تحلیل داده‌های پرت با آزمون گرابز",
        }
        d1 = PreEmptiveRiskOfBiasMitigator.evaluate_selection_bias(secs)
        self.assertIn("Selection Bias", d1.domain_title_en)
        self.assertEqual(PreEmptiveRiskOfBiasMitigator.evaluate_detection_bias(secs).domain_id, "DOMAIN_3_DETECTION_BIAS")
        self.assertEqual(PreEmptiveRiskOfBiasMitigator.evaluate_attrition_bias(secs).domain_id, "DOMAIN_4_ATTRITION_BIAS")
        self.assertEqual(PreEmptiveRiskOfBiasMitigator.evaluate_reporting_bias(secs).domain_id, "DOMAIN_5_REPORTING_BIAS")

        # DynamicProtocolDesigner alpha=None on SCOPING_REVIEW & USABILITY statistical plan
        ux_stat = DynamicProtocolDesigner.generate_statistical_plan({"framework": "USABILITY"})
        self.assertIsNone(ux_stat["alpha_threshold"])
        scoping_plan = DynamicProtocolDesigner.calculate_sample_size_plan("SCOPING_REVIEW")
        self.assertIsNone(scoping_plan["alpha"])

        # BaselinePaperQualityAuditor scoping review table adaptation
        tbl = BaselinePaperQualityAuditor.render_markdown_table(
            [{"pmid": "39111111", "title": "Telemedicine Scoping Study", "domains": {"d1_randomization": "LOW_RISK", "d2_blinding": "LOW_RISK", "d3_controls_rigor": "LOW_RISK", "d4_replication_reporting": "LOW_RISK"}, "overall_rob": "LOW_RISK"}],
            framework="SCOPING_REVIEW",
        )
        self.assertIn("مطابقت با هدف/PCC", tbl)
        self.assertNotIn("تصادفی‌سازی", tbl)

    def test_06_biostatistics_ascii_22_usability_exemption_and_parent_shim(self):
        md_ascii_22 = "## 22. حجم نمونه و روش محاسبه آن\nمدل نیلسن و لاندائور $1 - (1 - L)^n$ با ۱۰ ارزیاب و پرسشنامه SUS با ۳۰ کاربر."
        extracted = BiostatisticalValidator.parse_section_22(md_ascii_22)
        self.assertIn("نیلسن", extracted)

        res_ux = BiostatisticalValidator.verify_sample_size(extracted, "usability")
        self.assertEqual(res_ux["coherence_status"], "PASS")
        self.assertEqual(res_ux["issues"], [])

        res_review = BiostatisticalValidator.verify_sample_size(
            "چهارچوب PRISMA-ScR و JBI با جستجو در PubMed و Scopus تا اشباع شواهد.",
            "scoping_review",
        )
        self.assertEqual(res_review["coherence_status"], "PASS")

        # Comparative usability still audits alpha & power
        res_ux_comp = BiostatisticalValidator.verify_sample_size(
            "مدل نیلسن $1-(1-L)^n$ با مقایسه دو گروه کنترل و آزمون t-test.",
            "usability",
        )
        self.assertEqual(res_ux_comp["coherence_status"], "FAIL")

        # Parent delegating shim executes identically
        shim_path = REPO_ROOT / "scripts" / "verify_biostatistics.py"
        self.assertTrue(shim_path.exists())
        proc = subprocess.run(
            [
                sys.executable,
                str(shim_path),
                "--study-family",
                "scoping_review",
                "--section22",
                "بر پایه PRISMA-ScR و JBI در PubMed تا اشباع شواهد.",
                "--json",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        self.assertIn('"coherence_status": "PASS"', proc.stdout)

    def test_07_docx_builder_three_branch_callouts_and_dynamic_cover_metadata(self):
        doc = Document()
        p1 = add_callout_box(doc, "> [!NOTE] با وجود صفر مطالعه در شواهد منفی، سوگیری انتشار پایش شد.")
        p2 = add_callout_box(doc, "> [!NOTE] **نکته اجرایی اختصاصی**: ثبت کد اخلاق پیش از نمونه‌گیری الزامی است.")
        p3 = add_callout_box(doc, "> [!NOTE] یک یادداشت روش‌شناختی عمومی درباره نحوه پایش.")
        self.assertIn("شفافیت معرفتی پیرامون سوگیری انتشار (Publication Bias):", p1.text)
        self.assertIn("◄ نکته اجرایی اختصاصی:", p2.text)
        self.assertIn("◄ یادداشت روش‌شناختی:", p3.text)

        md_14 = "\n".join(
            [
                "## ۱. موضوع\n"
                "▪ **عنوان فارسی (Persian Title):**  \nارزیابی کاربردپذیری سامانه پایش دیابت\n"
                "▪ **عنوان انگلیسی (English Title):**  \nUsability Evaluation of Diabetes Monitoring App",
            ]
            + [f"## {i}. بخش نمونه\nمتن بخش {i}" for i in range(2, 14)]
            + [
                "## ۱۴. منابع\n"
                "[1] Test Author. 2024.",
            ]
        )
        meta_14 = extract_proposal_metadata(md_14)
        self.assertEqual(meta_14["fa_title"], "ارزیابی کاربردپذیری سامانه پایش دیابت")
        self.assertEqual(meta_14["english_title"], "Usability Evaluation of Diabetes Monitoring App")
        self.assertEqual(meta_14["archetype_key"], "usability")
        self.assertIn("14 بخشی", meta_14["sections_count_label"].replace("۱۴", "14"))

        md_28 = "\n".join(
            [
                "## ۱. موضوع\n▪ **عنوان فارسی:** بررسی هزینه‌های کمرشکن سلامت (CHE)\n▪ **عنوان انگلیسی:** Evaluation of Catastrophic Health Expenditure",
                "## ۱۴. نوع مطالعه\nمطالعه مقطعی در اقتصاد سلامت (CHE & OOP)",
                "## ۱۶. محل انجام مطالعه\nبیمارستان‌های آموزشی منتخب دانشگاه علوم پزشکی شیراز",
            ]
            + [f"## {i}. بخش\nمتن نمونه" for i in range(2, 29) if i not in (14, 16)]
        )
        meta_28 = extract_proposal_metadata(md_28)
        self.assertEqual(meta_28["archetype_key"], "health_systems")
        self.assertIn("اقتصاد سلامت", meta_28["domain_label"])
        self.assertIn("شیراز", meta_28["study_location"])
        self.assertIn("۲۸ بخش", meta_28["sections_count_label"])

    def test_08_mesh_query_expander_three_block_cap_and_stopwords(self):
        q1 = MeSHQueryExpander.build_tier1_precision_mesh_query(
            "مرور دامنه‌ای (scoping review) و ارزیابی diabetes، obesity، metformin و inflammation با PCR",
            custom_agents=["Metformin", "Berberine", "بررسی", "scoping"],
        )
        self.assertLessEqual(q1.count(" AND "), 2)
        self.assertNotIn('"بررسی"', q1)
        self.assertNotIn('"scoping"', q1.lower())

        q2 = MeSHQueryExpander.build_tier2_fallback_query(
            "evaluation of diabetes, obesity, metformin and inflammation usability review",
            custom_agents=["Metformin", "Berberine", "usability", "ارزیابی"],
        )
        self.assertLessEqual(q2.count(" AND "), 2)
        self.assertNotIn('"evaluation"', q2.lower())
        self.assertNotIn('"usability"', q2.lower())


if __name__ == "__main__":
    unittest.main()
