#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Two-Loop Research Architecture & Epistemic Rigor Auditor (Pillar 10)
=============================================================================
Validates:
- ProposalResearchDossier state management, sealing, and export (JSON & MD).
- EpistemicRigorAuditor across all 6 epistemic rigor dimensions.
- Blocking gatekeeper behavior when fail_closed=True.
- Immutability of sealed dossiers.
"""

import os
import json
import tempfile
import unittest

from scripts.proposal_research_dossier import ProposalResearchDossier
from scripts.epistemic_rigor_auditor import EpistemicRigorAuditor, EpistemicRigorGateError


class TestTwoLoopDossierSuite(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def _build_valid_dossier(self) -> ProposalResearchDossier:
        dossier = ProposalResearchDossier(
            topic="اثر هم‌افزایی متفورمین و کورکومین بر مهار رشد سلول‌های سرطان کولون",
            domain="Biomedical Science / Oncology"
        )
        dossier.set_hypotheses(
            h0="ترکیب متفورمین و کورکومین تفاوت معنی‌داری در القای آپوپتوز نسبت به تک‌درمانی‌ها ایجاد نمی‌کند.",
            h1="ترکیب متفورمین و کورکومین به طور هم‌افزا و معنی‌دار موجب افزایش آپوپتوز و کاهش تکثیر سلولی می‌شود.",
            rationale="تعدیل دوگانه مسیر AMPK/mTOR و مهار NF-kB."
        )
        dossier.set_methodological_invariants(
            study_family="In Vitro Factorial Synergism",
            primary_endpoint="شاخص ترکیبی (CI) و آپوپتوز سلولی در ۴۸ ساعت",
            sample_size_formula="Resource Equation & Power Analysis (Cohen's f ANOVA)",
            target_n=24,
            statistical_test="Two-Way ANOVA with Tukey post-hoc test",
            alpha=0.05,
            power=0.85
        )
        dossier.add_biological_entity(
            name="HCT116",
            entity_type="Human Colorectal Carcinoma Cell Line",
            identifier="ATCC CCL-247 (RRID:CVCL_0291)",
            purity="STR authenticated, Mycoplasma-free",
            source="ATCC"
        )
        dossier.add_biological_entity(
            name="Metformin Hydrochloride",
            entity_type="Chemical Compound",
            identifier="CAS: 1115-70-4",
            purity=">=98% HPLC analytical standard",
            source="Sigma-Aldrich"
        )
        dossier.add_evidence_paper(
            pmid="31245678",
            doi="10.1038/s41416-019-0521-1",
            title="Metformin and curcumin synergistically inhibit colorectal cancer cell survival",
            authors=["Smith J", "Doe A", "Brown C"],
            year=2021,
            is_full_text=True,
            verified=True,
            passages=["Metformin combined with curcumin induced a 45% increase in apoptotic cell death compared to single treatments."],
            grade="High"
        )
        dossier.add_evidence_paper(
            pmid="29876543",
            doi="10.1016/j.canlet.2018.05.012",
            title="Mechanisms of dual mTOR/AMPK targeting in colon cancer",
            authors=["Taylor R", "White E"],
            year=2019,
            is_full_text=True,
            verified=True,
            passages=["Dual targeting achieved significant suppression of colony formation at sub-micromolar thresholds."],
            grade="High"
        )
        dossier.add_contradictory_finding(
            topic="اثر ضدالتهابی در برابر سمیت در دوزهای بالا",
            reported_claim_a="دوزهای بیش از ۵۰ میکرومولار کورکومین موجب القای آپوپتوز از طریق افزایش شدید ROS می‌شوند.",
            citation_a="PMID: 31245678",
            reported_claim_b="در سلول‌های نرمال روده، کورکومین تا دوز ۱۰۰ میکرومولار اثر آنتی‌اکسیدانی و محافظتی نشان می‌دهد.",
            citation_b="PMID: 29876543",
            resolution_rationale="پاسخ دوگانه ردوکس (Biphasic Redox): کورکومین در سلول‌های بدخیم با استرس اکسیداتیو بالا به صورت پرو-اکسیدان و در سلول نرمال به عنوان آنتی‌اکسیدان عمل می‌کند."
        )
        dossier.add_limitation("محدودیت ترجمان برون‌تنی (In Vitro): فراهمی زیستی پایین کورکومین در مدل‌های انسانی.")
        dossier.add_limitation("احتمال تداخل طیفی فتومتریک کورکومین در طول موج‌های ۴۵۰ تا ۵۴۰ نانومتر نیازمند بلنک بدون سلول است.")
        return dossier

    def test_dossier_creation_and_sealing_success(self):
        """Valid dossier passes epistemic rigor audit and seals successfully."""
        dossier = self._build_valid_dossier()
        self.assertFalse(dossier.is_sealed)
        self.assertIsNone(dossier.sealed_at)

        report = dossier.seal_dossier()
        self.assertTrue(dossier.is_sealed)
        self.assertIsNotNone(dossier.sealed_at)
        self.assertTrue(report["passed"])
        self.assertGreaterEqual(report["composite_score"], 80.0)
        self.assertEqual(report["seal_status"], "SEALED_LEVEL_2")

    def test_sealed_dossier_immutability(self):
        """Sealed dossier strictly prevents further modifications."""
        dossier = self._build_valid_dossier()
        dossier.seal_dossier()
        self.assertTrue(dossier.is_sealed)

        with self.assertRaises(RuntimeError):
            dossier.set_hypotheses("new h0", "new h1")

        with self.assertRaises(RuntimeError):
            dossier.add_limitation("new limitation")

        with self.assertRaises(RuntimeError):
            dossier.add_biological_entity("SW480", "Cell Line")

    def test_dossier_dual_export(self):
        """Dossier exports to valid JSON and Markdown files with full structural content."""
        dossier = self._build_valid_dossier()
        dossier.seal_dossier()

        json_path = os.path.join(self.temp_dir.name, "PROPOSAL_RESEARCH_DOSSIER.json")
        md_path = os.path.join(self.temp_dir.name, "PROPOSAL_RESEARCH_DOSSIER.md")

        dossier.export_json(json_path)
        dossier.export_markdown(md_path)

        self.assertTrue(os.path.exists(json_path))
        self.assertTrue(os.path.exists(md_path))

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data["topic"], dossier.topic)
            self.assertTrue(data["is_sealed"])
            self.assertEqual(len(data["literature_evidence"]), 2)

        with open(md_path, "r", encoding="utf-8") as f:
            md_text = f.read()
            self.assertIn("پرونده پژوهشی و پایگاه استنادی پروپوزال", md_text)
            self.assertIn("HCT116", md_text)
            self.assertIn("31245678", md_text)
            self.assertIn("پاسخ دوگانه ردوکس", md_text)

    def test_epistemic_audit_fails_on_unverified_references(self):
        """Fail-closed: unverified literature reference blocks dossier sealing."""
        dossier = self._build_valid_dossier()
        # Add an unverified reference
        dossier.add_evidence_paper(
            pmid="00000000",
            doi="",
            title="Unverified Hallucinated Study",
            authors=["Fictitious A"],
            year=2024,
            is_full_text=False,
            verified=False,
            passages=[],
            grade="Low"
        )
        with self.assertRaises(EpistemicRigorGateError):
            dossier.seal_dossier()

    def test_epistemic_audit_fails_on_missing_hypotheses(self):
        """Fail-closed: missing null hypothesis (H0) blocks dossier sealing."""
        dossier = self._build_valid_dossier()
        dossier.hypotheses["h0"] = ""  # Erase H0
        with self.assertRaises(EpistemicRigorGateError):
            dossier.seal_dossier()

    def test_epistemic_audit_fails_on_factorial_t_test_mismatch(self):
        """Fail-closed: factorial study with simple isolated t-test causes methodological coherence failure."""
        dossier = self._build_valid_dossier()
        dossier.methodological_invariants["statistical_test"] = "Independent Samples Two-Group t-Test"
        auditor = EpistemicRigorAuditor(fail_closed=False)
        report = auditor.audit_dossier(dossier.to_dict())
        dim3 = report["dimensions"]["dimension_3_methodological_coherence"]
        self.assertFalse(dim3["passed"])
        self.assertTrue(any("Methodological mismatch" in f for f in dim3["findings"]))

    def test_epistemic_audit_fails_on_insufficient_limitations(self):
        """Boundary conditions: fewer than 2 limitations penalizes dimension 4."""
        dossier = self._build_valid_dossier()
        dossier.limitations_and_boundaries = ["یک محدودیت بسیار کوتاه"]
        auditor = EpistemicRigorAuditor(fail_closed=False)
        report = auditor.audit_dossier(dossier.to_dict())
        dim4 = report["dimensions"]["dimension_4_boundary_conditions"]
        self.assertFalse(dim4["passed"])

    def test_two_loop_e2e_integration_with_proposal_generator(self):
        """End-to-End: ProposalGenerator automatically seals and exports dossier reports."""
        from generate_compliant_proposal import ProposalGenerator

        dossier = self._build_valid_dossier()
        md_out = os.path.join(self.temp_dir.name, "output_proposal.md")
        docx_out = os.path.join(self.temp_dir.name, "output_proposal.docx")

        proposal_data = {
            "research_title_fa": "بررسی اثر هم‌افزایی متفورمین و کورکومین بر سرطان کولون",
            "research_title_en": "Synergistic effect of metformin and curcumin in colon cancer",
            "study_type": "تجربی مداخله‌ای پایه (In Vitro Experimental)",
            "primary_endpoint": "درصد آپوپتوز و شاخص ترکیبی CI",
            "sample_size_justification": "بر اساس معادله منابع مید و تحلیل توان آزمون فاکتوریل",
            "target_population": "رده سلولی سرطان کولورکتال HCT116",
            "statistical_analysis_plan": "آزمون تحلیل واریانس دوطرفه (Two-Way ANOVA) به همراه آزمون تعقیبی توکی",
            "proposal_research_dossier": dossier,
            "format": "14"
        }

        res = ProposalGenerator.generate_and_save(proposal_data, md_out, docx_out, format="14")
        self.assertEqual(res["status"], "PASS")
        self.assertIsNotNone(res["dossier_audit"])
        self.assertTrue(res["dossier_audit"]["passed"])
        self.assertTrue(os.path.exists(res["dossier_json"]))
        self.assertTrue(os.path.exists(res["dossier_md"]))
        self.assertTrue(os.path.exists(docx_out))


if __name__ == "__main__":
    unittest.main()

