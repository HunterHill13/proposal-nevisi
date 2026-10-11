#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_v114_adversarial_immunization.py - Test Suite for 10 Adversarial AI Review Immunization Gates
Proposal-Nevisi Engine v11.4 (Cognitive Multi-Agent Architecture)

Verifies that the proposal generator and mock grant study section immunize against all 10
methodological, biostatistical, biochemical, and bibliographical flaws identified by external AI critics:
1. DOI Digit Drift & Title Mismatch Verification (LiveDoiCrossrefVerifier)
2. Exact GLOBOCAN 2022 Checksum Gate (Bray et al., CA Cancer J Clin 2024: 2,480,301 cases & 1,817,172 deaths)
3. Cochrane RoB-2 In Vitro Misapplication Guard (ToxRTool / NTP OHAT Quality Framework)
4. Mead's Equation vs Statistical Power Separation & Block DF (B = k - 1 = 2, E = 19, G*Power 85.2%)
5. Chou-Talalay 2-Phase Protocol Guard (Monotherapy 5-7 point curves for IC50 before combination)
6. Apoptosis Positive Control Guard (Staurosporine 1 uM validation)
7. Caspase-3 mRNA Transcriptional Priming vs Active Cleavage / Annexin V/PI Guard
8. Translational Extrapolation Guard (In Vitro Cytotoxicity -> Clinical Patient Toxicity Boundary)
9. Epistemic Modesty & Database-Scoped Novelty Guard (Anti-Cosmic Absolutes)
10. Molecular Heterogeneity Rationale & ATCC Standard Culture Media
11. Full End-to-End Proposal Immunization (MockGrantReviewPanel 100% Fundable with 0 Critical Flaws)
"""

import os
import sys
import unittest
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from mock_grant_review_panel import MockGrantReviewPanel
from pre_emptive_risk_of_bias_mitigator import PreEmptiveRiskOfBiasMitigator, BaselinePaperQualityAuditor
from generic_reference_auditor import LiveDoiCrossrefVerifier
from generate_compliant_proposal import ProposalGenerator


class TestV114AdversarialImmunization(unittest.TestCase):
    """Test suite verifying the 10 adversarial review immunization gates."""

    def test_1_doi_drift_detection_and_crossref_verification(self):
        """Pillar 1: Detects title mismatch when a DOI points to an unrelated publication."""
        # Prime verified cache with a known paper
        LiveDoiCrossrefVerifier._VERIFIED_CACHE["10.1016/j.ijbiomac.2026.153306"] = {
            "doi": "10.1016/j.ijbiomac.2026.153306",
            "title": "Application of Monascus pigments in textile dyeing",
            "year": 2026,
            "authors": ["Zhang", "Wang"],
            "journal": "International Journal of Biological Macromolecules",
            "verified": True
        }

        # Reference claiming to be about biological polysaccharide but citing the textile DOI
        mismatched_ref = {
            "doi": "10.1016/j.ijbiomac.2026.153306",
            "title": "Sulfated polysaccharide induces apoptosis in malignant cancer cells",
            "year": 2026
        }
        audit_res = LiveDoiCrossrefVerifier.audit_reference_doi(mismatched_ref)
        self.assertFalse(audit_res["is_valid"])
        self.assertEqual(audit_res["status"], "CRITICAL_DOI_MISMATCH")
        self.assertLess(audit_res["similarity"], 0.40)

        # Matching title
        matching_ref = {
            "doi": "10.1016/j.ijbiomac.2026.153306",
            "title": "Application of Monascus pigments in textile dyeing",
            "year": 2026
        }
        matching_audit = LiveDoiCrossrefVerifier.audit_reference_doi(matching_ref)
        self.assertTrue(matching_audit["is_valid"])
        self.assertEqual(matching_audit["status"], "VERIFIED_ACCURATE")

    def test_2_globocan_2022_checksum_audit(self):
        """Pillar 2: Verifies exact 2022 GLOBOCAN figures and flags outdated 2020 statistics."""
        # Outdated 2020 epidemiology
        sections_outdated = {
            2: "بر اساس گزارش GLOBOCAN 2020، سالانه ۲.۲ میلیون مورد جدید ابتلا ثبت شده است."
        }
        r1_outdated = MockGrantReviewPanel.evaluate_reviewer_1_scientific_merit(sections_outdated)
        self.assertTrue(any("OUTDATED_EPIDEMIOLOGY" in w for w in r1_outdated.weaknesses))

        # Accurate 2022 epidemiology (Bray et al., 2024: 2,480,301 cases)
        sections_accurate = {
            2: "بر اساس آخرین گزارش رسمی IARC GLOBOCAN 2022 (Bray et al. 2024)، سالانه ۲,۴۸۰,۳۰۱ مورد جدید (۲.۴۸ میلیون) و ۱,۸۱۷,۱۷۲ مرگ ثبت شده است." * 10,
            4: "اهمیت و ضرورت تحقیق به تفصیل تبیین شده است." * 15,
            9: "فرضیه پژوهش بر وجود هم‌افزایی معنادار متمرکز است."
        }
        r1_accurate = MockGrantReviewPanel.evaluate_reviewer_1_scientific_merit(sections_accurate)
        self.assertFalse(any("OUTDATED_EPIDEMIOLOGY" in w for w in r1_accurate.weaknesses))
        self.assertTrue(any("GLOBOCAN 2022" in s for s in r1_accurate.strengths))

    def test_3_rob2_in_vitro_misapplication_guard(self):
        """Pillar 3: Rejects Cochrane RoB-2 on in vitro cell culture and enforces ToxRTool / NTP OHAT."""
        # Proposal claiming in vitro study but applying Cochrane RoB-2
        sections_flawed = {
            13: "روش اجرا بر روی کشت سلول انجام می‌شود.",
            14: "نوع مطالعه: برون‌تن (In Vitro Experimental).",
            20: "ارزیابی سوگیری با ابزار Cochrane RoB-2 انجام می‌پذیرد."
        }
        r2, _ = MockGrantReviewPanel.evaluate_reviewer_2_methodology_and_alignment(sections_flawed)
        self.assertTrue(any("ROB2_IN_VITRO_MISAPPLICATION" in f for f in r2.critical_flaws))

        # PreEmptiveRiskOfBiasMitigator also catches the misapplication
        audit_res = PreEmptiveRiskOfBiasMitigator.audit_proposal(sections_flawed)
        self.assertTrue(any("ROB2_IN_VITRO_MISAPPLICATION" in h for h in audit_res.high_risk_domains))

        # When ToxRTool is applied, it passes cleanly
        toxr_res = PreEmptiveRiskOfBiasMitigator.evaluate_in_vitro_toxrtool_quality({
            13: "کشت سلولی با خلوص بالای ۹۵٪ ماده استاندارد و کنترل حلال ناقل DMSO < 0.1% انجام می‌شود.",
            15: "سلول‌ها دارای پروفایل STR و فاقد مایکوپلاسما در پاساژ ۳ الی ۱۰ هستند.",
            20: "استفاده از کنترل بلانک بدون سلول (Cell-Free Blank) و کنترل مثبت استاروسپورین.",
            26: "کنترل سوگیری موقعیت چاهک‌ها با چیدمان تصادفی پلیت و مهار Edge Effect.",
            27: "حداقل ۳ تکرار بیولوژیک مستقل در روزهای مجزا و مدیریت داده‌های پرت با آزمون گرابز (Grubbs)."
        })
        self.assertTrue(toxr_res["is_compliant"])
        self.assertEqual(toxr_res["overall_category"], "CATEGORY_1_RELIABLE_WITHOUT_RESTRICTION")

    def test_4_mead_power_and_block_df_audit(self):
        """Pillar 4: Decouples Mead's heuristic from Statistical Power and audits block df (B = 2)."""
        # Flawed Section 22: asserts B = 1 for 3 days and claims Mead proves power > 80%
        sections_flawed = {
            22: "در معادله مید با ۳ روز کاری مستقل، درجات آزادی بلوک B = 1 لحاظ گردیده و فرمول مید تضمین‌کننده توان بالای ۸۰٪ است."
        }
        r2, _ = MockGrantReviewPanel.evaluate_reviewer_2_methodology_and_alignment(sections_flawed)
        self.assertTrue(any("BIOSTATISTICAL_BLOCK_DF_ERROR" in f for f in r2.critical_flaws))
        self.assertTrue(any("BIOSTATISTICAL_MEAD_POWER_CONFLATION" in f for f in r2.critical_flaws))

        # Rigorous Section 22: B = 3 - 1 = 2, E = 19, power calculated separately via G*Power
        sections_rigorous = {
            13: "گروه‌های کنترل منفی و حلال ناقل در طرح آزمایش لحاظ شده‌اند.",
            22: (
                "تعیین حجم نمونه بر مبنای معادله تخصیص منابع مید (E = N - B - T) صورت گرفته است: "
                "با ۳ روز کاری مستقل درجات آزادی بلوک B = 3 - 1 = 2، درجات تیمار T = 9 و کل N = 30، "
                "درجات آزادی خطا E = 30 - 2 - 9 = 19 حاصل می‌شود. "
                "همچنین تحلیل مستقل توان آزمون با نرم‌افزار G*Power برای مدل Two-Way Factorial ANOVA "
                "با اندازه اثر f = 0.40 و خطای ۵٪ توان آماری ۸۵.۲٪ را تضمین می‌کند."
            ),
            23: "تحلیل داده‌ها با Two-Way ANOVA و آزمون تعقیبی Tukey انجام می‌شود."
        }
        r2_clean, _ = MockGrantReviewPanel.evaluate_reviewer_2_methodology_and_alignment(sections_rigorous)
        self.assertFalse(any("BIOSTATISTICAL_BLOCK_DF_ERROR" in f for f in r2_clean.critical_flaws))
        self.assertFalse(any("BIOSTATISTICAL_MEAD_POWER_CONFLATION" in f for f in r2_clean.critical_flaws))
        self.assertTrue(any("تفکیک دقیق معادله تخصیص منابع مید" in s for s in r2_clean.strengths))

    def test_5_chou_talalay_2_phase_protocol_audit(self):
        """Pillar 5: Mandates Phase 1 single-agent dose-response curve prior to combination modeling."""
        # Flawed: Jumped straight to combination without Phase 1 monotherapy
        sections_flawed = {
            13: "گروه‌های کنترل در نظر گرفته شده‌اند.",
            27: "سنجش هم‌افزایی چاو-تالالای (Chou-Talalay) با نرم‌افزار CompuSyn مستقیماً در ۱۰ غلظت ترکیبی انجام می‌شود."
        }
        r2, _ = MockGrantReviewPanel.evaluate_reviewer_2_methodology_and_alignment(sections_flawed)
        self.assertTrue(any("CHOU_TALALAY_PROTOCOL_INCOMPLETE" in w for w in r2.weaknesses))

        # Rigorous: Formulates Phase 1 monotherapy curve before Phase 2 combination
        sections_rigorous = {
            13: "گروه‌های کنترل لحاظ شده‌اند.",
            27: (
                "فاز اول (تک‌دارویی و منحنی‌های دوز-پاسخ منفرد): ارزیابی رقت متوالی ۵ الی ۷ نقطه‌ای جهت استخراج IC50 منفرد، شیب m و Dm. "
                "فاز دوم: سنجش هم‌افزایی Chou-Talalay با نسبت ثابت هم‌توان در CompuSyn."
            )
        }
        r2_clean, _ = MockGrantReviewPanel.evaluate_reviewer_2_methodology_and_alignment(sections_rigorous)
        self.assertFalse(any("CHOU_TALALAY_PROTOCOL_INCOMPLETE" in w for w in r2_clean.weaknesses))
        self.assertTrue(any("پروتکل دوفازی استاندارد Chou-Talalay" in s for s in r2_clean.strengths))

    def test_6_apoptosis_positive_control_audit(self):
        """Pillar 6: Mandates explicit positive control (e.g. Staurosporine) in apoptosis assays."""
        # Apoptosis assay without positive control
        sections_flawed = {
            13: "کنترل منفی در نظر گرفته شده است.",
            27: "سنجش آپوپتوز و apoptosis با رنگ‌آمیزی Annexin V-FITC انجام می‌پذیرد."
        }
        r2, _ = MockGrantReviewPanel.evaluate_reviewer_2_methodology_and_alignment(sections_flawed)
        self.assertTrue(any("APOPTOSIS_POSITIVE_CONTROL_MISSING" in w for w in r2.weaknesses))

        # Apoptosis assay with Staurosporine positive control
        sections_rigorous = {
            13: "کنترل منفی و کنترل مثبت استاروسپورین در نظر گرفته شده است.",
            27: "سنجش آپوپتوز با فلوسایتومتری Annexin V به همراه کنترل مثبت استاندارد (استاروسپورین ۱ میکرومولار) انجام می‌پذیرد."
        }
        r2_clean, _ = MockGrantReviewPanel.evaluate_reviewer_2_methodology_and_alignment(sections_rigorous)
        self.assertFalse(any("APOPTOSIS_POSITIVE_CONTROL_MISSING" in w for w in r2_clean.weaknesses))
        self.assertTrue(any("کنترل مثبت استاندارد آپوپتوز" in s for s in r2_clean.strengths))

    def test_7_caspase3_mrna_vs_active_cleavage_audit(self):
        """Pillar 7: Prevents equating CASP3 mRNA with functional apoptosis without cleavage/Annexin."""
        # Flawed: Claims qPCR CASP3 mRNA proves apoptosis without protein cleavage
        sections_flawed = {
            13: "گروه کنترل در نظر گرفته شده است.",
            27: "بررسی آپوپتوز از طریق سنجش افزایش بیان ژن کاسپاز-۳ (CASP3) با تکنیک Real-Time RT-PCR اثبات می‌گردد."
        }
        r2, _ = MockGrantReviewPanel.evaluate_reviewer_2_methodology_and_alignment(sections_flawed)
        self.assertTrue(any("CASPASE3_MRNA_INSUFFICIENCY" in f for f in r2.critical_flaws))

        # Rigorous: Integrates active proteolytic cleavage or Annexin V/PI
        sections_rigorous = {
            13: "گروه‌های کنترل در نظر گرفته شده‌اند.",
            27: "سنجش آپوپتوز از طریق برش پروتئینی پروکاسپاز-۳ به قطعات فعال و ارزیابی ارتوگونال با فلوسایتومتری Annexin V در کنار RT-PCR انجام می‌شود."
        }
        r2_clean, _ = MockGrantReviewPanel.evaluate_reviewer_2_methodology_and_alignment(sections_rigorous)
        self.assertFalse(any("CASPASE3_MRNA_INSUFFICIENCY" in f for f in r2_clean.critical_flaws))
        self.assertTrue(any("فعال‌سازی کاسپاز-۳ از طریق برش پروتئینی" in s for s in r2_clean.strengths))

    def test_8_translational_over_extrapolation_audit(self):
        """Pillar 8: Blocks unjustified claims of clinical patient organ toxicity reduction from in vitro data."""
        # Flawed: In vitro study claiming co-treatment cures nephrotoxicity in clinical patients
        sections_flawed = {
            1: "بررسی هم‌افزایی داروها در مهار تکثیر سلول‌ها",
            14: "نوع مطالعه: درون‌تن سلولی (In Vitro Experimental).",
            26: "این ترکیب سیتوتوکسیک در آینده باعث کاهش سمیت کلیوی بیماران و کاهش عوارض در بیماران تحت شیمی‌درمانی خواهد شد."
        }
        r1 = MockGrantReviewPanel.evaluate_reviewer_1_scientific_merit(sections_flawed)
        self.assertTrue(any("TRANSLATIONAL_OVER_EXTRAPOLATION" in f for f in r1.critical_flaws))

        # Rigorous: Hedged as a preclinical in vitro hypothesis with translational boundaries
        sections_rigorous = {
            1: "بررسی هم‌افزایی داروها در مهار تکثیر سلول‌ها",
            14: "نوع مطالعه: برون‌تن (In Vitro Experimental).",
            26: "اثبات اثرات در شرایط برون‌تن صرفاً یک فرضیه پیش‌بالینی اولیه و شاخص انتخاب‌پذیری است و بررسی کاهش عوارض نیازمند مطالعات in vivo و کارآزمایی بالینی آینده است."
        }
        r1_clean = MockGrantReviewPanel.evaluate_reviewer_1_scientific_merit(sections_rigorous)
        self.assertFalse(any("TRANSLATIONAL_OVER_EXTRAPOLATION" in f for f in r1_clean.critical_flaws))

    def test_9_epistemic_modesty_novelty_audit(self):
        """Pillar 9: Flags cosmic/unbounded claims and rewards database-scoped negative search logs."""
        # Cosmic absolute claim
        sections_flawed = {
            2: "این ترکیب برای اولین بار در کل دنیا مورد بررسی قرار می‌گیرد و در جهان وجود ندارد."
        }
        r1 = MockGrantReviewPanel.evaluate_reviewer_1_scientific_merit(sections_flawed)
        self.assertTrue(any("UNBOUNDED_EPISTEMIC_NOVELTY" in w for w in r1.weaknesses))

        # Scoped database claim with negative search query
        sections_rigorous = {
            2: "بر اساس استعلام نظام‌مند از پایگاه‌های PubMed و Europe PMC تا تاریخ جاری با استراتژی جستجو: `Query -> 0 hits`، هیچ پیشینه قبلی منتشر نشده است." * 5
        }
        r1_clean = MockGrantReviewPanel.evaluate_reviewer_1_scientific_merit(sections_rigorous)
        self.assertFalse(any("UNBOUNDED_EPISTEMIC_NOVELTY" in w for w in r1_clean.weaknesses))

    def test_10_molecular_heterogeneity_and_atcc_media(self):
        """Pillar 10: Rewards articulation of molecular heterogeneity and standard ATCC culture media."""
        sections = {
            15: (
                "جامعه مطالعه شامل رده‌های سلولی استاندارد ATCC است. "
                "مبنای تبارشناسی ژنتیکی: رده واجد موتاسیون فعال‌کننده KRAS و پروتئین p53 وحشی در مقایسه با رده فاقد p53 (p53-null). "
                "محیط‌های کشت استاندارد مصوب ATCC شامل F-12K، EMEM و RPMI-1640 با ۱۰٪ FBS لحاظ شده است."
            )
        }
        r1 = MockGrantReviewPanel.evaluate_reviewer_1_scientific_merit(sections)
        self.assertTrue(any("تبارشناسی ژنتیکی و ناهمگونی مولکولی" in s for s in r1.strengths))

    def test_11_full_generated_proposal_immunized_end_to_end(self):
        """Pillar 11: Generated 28-section proposal passes MockGrantReviewPanel with 0 critical flaws."""
        data = {
            "title_fa": "بررسی اثر هم‌افزایی داروی فرضی الف با مداخله ب در رده‌های سلولی بدخیم",
            "title_en": "Evaluation of Synergistic Antitumor Interaction between Drug A and Intervention B",
            "framework": "EXPERIMENTAL_IN_VITRO",
            "domain": "oncology",
            "target_condition": {"name_fa": "سرطان ریه", "name_en": "Lung Cancer"},
            "interventions": [{"name": "ترکیب تجربی الف"}, {"name": "مداخله درمانی ب"}],
            "population_or_model": {"primary_system": "رده‌های سلولی استاندارد کارسینوما"},
            "studies": [
                {
                    "citation_number": 1,
                    "title": "Synergistic cytotoxic evaluation in oncology cell models",
                    "authors": ["Rezaei M", "Karimi A"],
                    "year": 2024,
                    "journal": "Oncology Letters",
                    "evidence_role": "DIRECT_INTERVENTION",
                    "final_inclusion_reason": "DIRECT_COMBINATION"
                },
                {
                    "citation_number": 2,
                    "title": "Theoretical basis of combination index and median effect principle",
                    "authors": ["Chou TC"],
                    "year": 2006,
                    "journal": "Pharmacological Reviews",
                    "evidence_role": "METHODOLOGICAL_SYNERGY",
                    "final_inclusion_reason": "METHODOLOGICAL_FOUNDATION"
                }
            ]
        }

        md_proposal = ProposalGenerator.assemble_pajooheshyar_28(data)
        self.assertIn("۲,۴۸۰,۳۰۱", md_proposal)
        self.assertIn("E = 30 - 2 - 9 = 19", md_proposal)
        self.assertIn("G*Power", md_proposal)
        self.assertIn("استاروسپورین", md_proposal)
        self.assertIn("فاز اول", md_proposal)
        self.assertIn("پروکاسپاز-۳", md_proposal)

        # Conduct full panel review
        panel_result = MockGrantReviewPanel.conduct_panel_review(md_proposal)
        self.assertEqual(panel_result.critical_flaws_count, 0)
        self.assertTrue(panel_result.can_proceed)
        self.assertLessEqual(panel_result.overall_score, 3.5)
        self.assertEqual(panel_result.funding_verdict, "APPROVED_FUNDABLE")

    def test_12_persian_editorial_hygiene_and_bidi_typography(self):
        """Pillar 12: Guards against raw Boolean syntax, English gap labels, Cat 3 RoB false positives, and Persian digits in English bibliography."""
        from persian_medical_typography_linter import PersianMedicalTypographyLinter

        data = {
            "title_fa": "بررسی اثر هم‌افزایی داروی اول و داروی دوم در رده سلولی",
            "framework": "EXPERIMENTAL_IN_VITRO",
            "studies": [
                {
                    "pmid": "38572751",
                    "doi": "10.3322/caac.21834",
                    "title": "Global cancer statistics 2022: GLOBOCAN estimates of incidence and mortality worldwide for 36 cancers in 185 countries",
                    "authors": ["Bray F", "Laversanne M"],
                    "year": 2024,
                    "journal": "CA Cancer J Clin",
                    "abstract": "Global cancer statistics and incidence.",
                    "verified": True
                }
            ],
            "research_problem_model": {
                "framework": "EXPERIMENTAL_IN_VITRO",
                "target_condition": {"name_fa": "سرطان ریه", "name_en": "Lung Cancer"},
                "population_or_model": {"primary_system": "رده سلولی هدف"},
                "interventions_or_exposures": [{"name": "داروی اول"}, {"name": "داروی دوم"}]
            }
        }
        md = ProposalGenerator.assemble_pajooheshyar_28(data)
        linter = PersianMedicalTypographyLinter()
        md_linted = linter.format_text("آپوپتوز (Apoptosis) در سلول بررسی شد.\n" + md)

        # 1. No raw Boolean query syntax in Section 2
        self.assertNotIn("[Mesh]", md_linted)
        self.assertNotIn("[Title/Abstract]", md_linted)
        self.assertIn("صفر یافته (0 hits)", md_linted)

        # 2. No English gap enum or English gap sentences in Section 2
        self.assertNotIn("MODEL_GAP", md_linted)
        self.assertNotIn("COMBINATION_GAP", md_linted)
        self.assertNotIn("Only 0 studies", md_linted)

        # 3. No false Cat 3 invalid label or ugly 55-char mid-word truncated English title in Section 3
        self.assertNotIn("غیرمعتبر (Cat 3)", md_linted)
        self.assertNotIn("estimates of in...", md_linted)
        self.assertIn("Bray F و همکاران", md_linted)

        # 4. English bibliography in Section 28 keeps ASCII digits and no duplicate parenthetical English
        ref_lines = [line for line in md_linted.splitlines() if line.startswith("[1]")]
        self.assertEqual(len(ref_lines), 1)
        self.assertIn("2022", ref_lines[0])
        self.assertIn("2024", ref_lines[0])
        self.assertNotIn("۲۰۲۲", ref_lines[0])
        self.assertNotIn("آپوپتوز (Apoptosis) (Apoptosis)", md_linted)


if __name__ == "__main__":
    unittest.main()
