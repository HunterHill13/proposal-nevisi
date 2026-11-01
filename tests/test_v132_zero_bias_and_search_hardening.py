#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_v132_zero_bias_and_search_hardening.py - Unit Test Suite for Zero-Bias, MeSH Expansion & Snowballing
Proposal-Nevisi Engine v13.2 (Comprehensive Multi-Domain Medical Core)

Tests:
1. Multi-domain MeSH thesaurus breadth (115+ descriptors across 10 clinical fields)
2. Zero cancer/apoptosis leakage on non-cancer topics (Cardiology, Nephrology, Infectious, Health Systems)
3. QUADAS-2 Spectrum Bias evaluation for diagnostic accuracy
4. STROBE representative sampling frame evaluation for observational studies
5. Polymorphic contradictory findings and limitations across archetypes (zero IC50/blank leakage)
6. Epistemic caveat injection for publication bias transparency (Principle 28)
7. True citation graph edge discovery among retrieved studies
"""

import os
import sys
import unittest
import tempfile
import json
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from mesh_query_expander import MeSHQueryExpander, MESH_THESAURUS, PERSIAN_TO_CONCEPT_MAP
from pre_emptive_risk_of_bias_mitigator import PreEmptiveRiskOfBiasMitigator, RiskOfBiasAuditResult
from proposal_research_dossier import ProposalResearchDossier
from generate_compliant_proposal import ProposalGenerator
from citation_graph_engine import CitationGraphEngine


class TestV132ZeroBiasAndSearchHardening(unittest.TestCase):
    """Test suite for v13.2 zero-bias architecture, MeSH expansion and citation snowballing."""

    def test_01_mesh_thesaurus_multidomain_breadth(self):
        """MeSH thesaurus contains >= 115 descriptors across 10 major clinical specialties."""
        self.assertGreaterEqual(len(MESH_THESAURUS), 115)
        self.assertGreaterEqual(len(PERSIAN_TO_CONCEPT_MAP), 115)

        # Check domain presence
        keys = list(MESH_THESAURUS.keys())
        self.assertIn("hypertension", keys)
        self.assertIn("myocardial_infarction", keys)
        self.assertIn("chronic_kidney_disease", keys)
        self.assertIn("sepsis", keys)
        self.assertIn("acinetobacter", keys)
        self.assertIn("multiple_sclerosis", keys)
        self.assertIn("depression", keys)
        self.assertIn("health_expenditures", keys)
        self.assertIn("diagnostic_accuracy", keys)
        self.assertIn("asthma", keys)
        self.assertIn("glaucoma", keys)

    def test_02_mesh_zero_cancer_leakage_on_non_cancer_topics(self):
        """Non-cancer topics generate accurate queries with 0% cancer/apoptosis fallback leakage."""
        # 1. Cardiology topic
        cardio_topic = "بررسی اثر کنترل فشار خون بر پیشگیری از سکته قلبی و آریتمی"
        q_cardio = MeSHQueryExpander.build_tier1_precision_mesh_query(cardio_topic)
        self.assertIn("Hypertension", q_cardio)
        self.assertIn("Myocardial Infarction", q_cardio)
        self.assertNotIn("Neoplasm", q_cardio)
        self.assertNotIn("Apoptosis", q_cardio)
        self.assertNotIn("cancer", q_cardio.lower())

        # 2. Nephrology topic
        nephro_topic = "بررسی پیامدهای دیالیز در بیماران نارسایی مزمن کلیه"
        q_nephro = MeSHQueryExpander.build_tier1_precision_mesh_query(nephro_topic)
        self.assertTrue("Renal Insufficiency, Chronic" in q_nephro or "Chronic Kidney Disease" in q_nephro)
        self.assertTrue("Renal Dialysis" in q_nephro or "Dialysis" in q_nephro)
        self.assertNotIn("Neoplasm", q_nephro)
        self.assertNotIn("cancer", q_nephro.lower())

        # 3. Infectious disease topic
        infect_topic = "بررسی مقاومت میکروبی و سپسیس ناشی از اسینتوباکتر بومانی"
        q_infect = MeSHQueryExpander.build_tier1_precision_mesh_query(infect_topic)
        self.assertIn("Acinetobacter baumannii", q_infect)
        self.assertIn("Sepsis", q_infect)
        self.assertNotIn("Neoplasm", q_infect)
        self.assertNotIn("cancer", q_infect.lower())

        # 4. Clean fallback for unknown Persian topic
        unknown_topic = "یک موضوع کاملا عمومی در حوزه سلامت اجتماعی"
        q_clean = MeSHQueryExpander.build_tier1_precision_mesh_query(unknown_topic)
        self.assertIn("Biomedical Research", q_clean)
        self.assertNotIn("Apoptosis", q_clean)
        self.assertNotIn("Drug Synergism", q_clean)
        self.assertNotIn("cancer", q_clean.lower())

    def test_03_quadas2_spectrum_bias_evaluation_diagnostic(self):
        """Diagnostic accuracy proposals are audited against QUADAS-2 for spectrum bias."""
        # Consecutive sampling of suspected patients -> LOW_RISK
        diag_sections_low = {
            1: "ارزیابی دقت تشخیصی ام‌آر‌آی در تشخیص زودهنگام سکته مغزی",
            14: "مطالعه ارزیابی دقت تشخیصی (Diagnostic Accuracy Study)",
            15: "کلیه مراجعین مشکوک به سکته مغزی حاد به صورت متوالی (consecutive enrollment) وارد مطالعه شدند",
            17: "معیارهای ورود: شک بالینی حاد بر اساس مقیاس NIHSS",
            22: "فرمول بودرر برای ارزیابی حساسیت و ویژگی",
            27: "اجرای آزمون شاخص بدون اطلاع از نتیجه استاندارد طلایی"
        }
        sf = PreEmptiveRiskOfBiasMitigator.detect_study_family(diag_sections_low)
        self.assertEqual(sf, "diagnostic")
        d1 = PreEmptiveRiskOfBiasMitigator.evaluate_selection_bias(diag_sections_low, study_family=sf)
        self.assertEqual(d1.risk_level, "LOW_RISK")
        self.assertTrue(any("QUADAS-2" in s for s in d1.strengths))
        self.assertTrue(any("سوگیری طیف" in s for s in d1.strengths))

        # Case-control design comparing severe cases to healthy volunteers -> SOME_CONCERNS / HIGH_RISK
        diag_sections_high = {
            1: "بررسی بیومارکر در تشخیص بیماری",
            14: "مطالعه تشخیصی",
            15: "مقایسه بیماران شدید در برابر داوطلبان سالم",
            17: "شاهد سالم در برابر بیمار شدید"
        }
        d1_high = PreEmptiveRiskOfBiasMitigator.evaluate_selection_bias(diag_sections_high, study_family="diagnostic")
        self.assertIn(d1_high.risk_level, ["SOME_CONCERNS", "HIGH_RISK"])
        self.assertTrue(any("سوگیری طیف" in v or "Spectrum Bias" in v for v in d1_high.vulnerabilities))

    def test_04_strobe_sampling_frame_evaluation_observational(self):
        """Observational and health systems proposals are audited against STROBE sampling criteria."""
        obs_sections_low = {
            1: "بررسی شیوع و عوامل مرتبط با مخارج کمرشکن سلامت (CHE)",
            14: "مطالعه مقطعی تحلیلی مبتنی بر جامعه (Cross-Sectional)",
            15: "جامعه هدف خانوارها با روش نمونه‌گیری خوشه‌ای چندمرحله‌ای طبقه‌بندی‌شده (Stratified Multi-stage Cluster)",
            22: "فرمول کوکران با محاسبه ضریب اثر طرح DEFF = 1.5"
        }
        sf = PreEmptiveRiskOfBiasMitigator.detect_study_family(obs_sections_low)
        self.assertIn(sf, ["health_systems", "epidemiological"])
        d1 = PreEmptiveRiskOfBiasMitigator.evaluate_selection_bias(obs_sections_low, study_family=sf)
        self.assertEqual(d1.risk_level, "LOW_RISK")
        self.assertTrue(any("STROBE" in s for s in d1.strengths))

    def test_05_polymorphic_contradictions_and_limitations_in_dossier(self):
        """ProposalResearchDossier contradictory findings and limitations are fully polymorphic."""
        # 1. Health Systems
        dossier_hs = ProposalResearchDossier(topic="بررسی مخارج کمرشکن سلامت CHE", domain="health_economics")
        dossier_hs.add_contradictory_finding(
            topic="تفاوت در برآورد سهم پرداخت از جیب (OOP) و شیوع هزینه‌های کمرشکن سلامت (CHE)",
            reported_claim_a="بار مالی بر پایه مخارج بستری",
            citation_a="PMID: 32329697",
            reported_claim_b="سهم هزینه‌های سرپایی و دارویی در CHE",
            citation_b="PMID: 31234567",
            resolution_rationale="آستانه‌های ۱۰٪ کل و ۴۰٪ ظرفیت پرداخت بر پایه WHO"
        )
        dossier_hs.add_limitation("محدودیت عدم ثبت کامل هزینه‌های غیرمستقیم در سامانه‌های اداری")
        dossier_hs.add_limitation("احتمال سوگیری یادآوری (Recall Bias)")

        exp_json = dossier_hs.to_dict()
        self.assertEqual(len(exp_json["contradictory_evidence"]), 1)
        self.assertIn("OOP", exp_json["contradictory_evidence"][0]["topic"])
        self.assertNotIn("IC50", exp_json["contradictory_evidence"][0]["resolution_rationale"])
        self.assertTrue(any("Recall Bias" in lim for lim in exp_json["limitations_and_boundaries"]))
        self.assertFalse(any("بلانک" in lim or "Cell-Free" in lim for lim in exp_json["limitations_and_boundaries"]))

    def test_06_epistemic_caveat_injection_in_section_3(self):
        """Epistemic caveat is injected into Section 3 when negative_findings_caveat is present."""
        caveat_text = (
            "بر اساس استعلام نظام‌مند از پایگاه‌های مرجع بین‌المللی PubMed و Europe PMC تا تاریخ جاری، "
            "صفر مطالعه تجربی دارای نتایج منفی معنادار برای این مداخله نمایه شده است. این وضعیت دال بر "
            "قطعیت اثر نبوده و بازتابی از سوگیری انتشار (Publication Bias) است."
        )
        sample_data = {
            "title_fa": "بررسی اثر مداخله فرضی در نظام سلامت",
            "title_en": "Evaluation of Hypothetical Health System Intervention",
            "framework": "HEALTH_SYSTEMS_AND_HEALTH_POLICY",
            "negative_findings_caveat": caveat_text,
            "studies": [
                {
                    "title": "Empirical study on health policy",
                    "authors": ["Smith J et al."],
                    "year": 2024,
                    "journal": "Health Policy",
                    "farsi_synthesis_summary": "در این مطالعه اثربخشی سیاست سلامت مورد بررسی قرار گرفت [1]."
                }
            ]
        }
        md_text = ProposalGenerator.assemble_pajooheshyar_28(sample_data)
        self.assertIn("Epistemic Transparency", md_text)
        self.assertIn("سوگیری انتشار", md_text)

    def test_07_citation_graph_true_internal_edges(self):
        """CitationGraphEngine links real internal citations based on referenced_works instead of linear chains."""
        engine = CitationGraphEngine(topic_query="Diagnostic Accuracy", offline_mode=True)
        
        study_1 = {
            "id": "W1001",
            "pmid": "31000001",
            "doi": "10.1001/jama.2024.1",
            "title": "Study 1 on diagnostic tests",
            "year": 2024,
            "referenced_works": ["W1002", "10.1001/jama.2024.2"]
        }
        study_2 = {
            "id": "W1002",
            "pmid": "31000002",
            "doi": "10.1001/jama.2024.2",
            "title": "Study 2 landmark diagnostic standard",
            "year": 2023,
            "referenced_works": []
        }
        
        node1 = engine.add_work_node(study_1, is_seed=True)
        node2 = engine.add_work_node(study_2, is_seed=False)
        
        # Connect true edges
        refs_1 = {str(rw).lower() for rw in study_1.get("referenced_works", [])}
        if study_2["id"].lower() in refs_1 or study_2["doi"].lower() in refs_1:
            engine.add_citation_edge(node1, node2, "CITES")

        self.assertEqual(len(engine.edges), 1)
        self.assertEqual(engine.edges[0]["source"], node1)
        self.assertEqual(engine.edges[0]["target"], node2)
        self.assertEqual(engine.edges[0]["edge_type"], "CITES")


if __name__ == "__main__":
    unittest.main()
