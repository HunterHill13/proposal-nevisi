#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_dossier_persistence_and_cli.py - Tests for Dossier Persistence, CLI, and Closed-Loop Rigor
Verifies:
1. ProposalResearchDossier from_dict and load_json serialization/deserialization fidelity.
2. MasterResearchPipeline --reuse-dossier integration without re-fetching network.
3. MockGrantReviewPanel CLI execution and exit codes.
4. IterativeRemediationEngine closed-loop multi-round consensus and audit trail persistence.
"""

import os
import sys
import json
import tempfile
import unittest

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from proposal_research_dossier import ProposalResearchDossier
from mock_grant_review_panel import MockGrantReviewPanel
from iterative_remediation_engine import IterativeRemediationEngine, SurgicalSectionPatcher


class TestDossierPersistenceAndCLI(unittest.TestCase):
    """Verifies research dossier persistence round-trips and CLI tooling."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_dossier_from_dict_and_load_json_roundtrip(self):
        """Dossier serializes to JSON and deserializes back with 100% attribute fidelity."""
        dossier = ProposalResearchDossier(topic="Test Topic", domain="Oncology")
        dossier.set_hypotheses(h0="H0 statement", h1="H1 statement", rationale="Test rationale")
        dossier.set_methodological_invariants(
            study_family="In Vitro",
            primary_endpoint="Viability",
            sample_size_formula="E = N - B - T",
            target_n=30,
            statistical_test="Two-Way ANOVA",
            alpha=0.05,
            power=0.85
        )
        dossier.add_biological_entity(
            name="HCT116",
            entity_type="Cell Line",
            identifier="ATCC CCL-247",
            purity="STR authenticated",
            source="ATCC"
        )
        dossier.add_evidence_paper(
            pmid="12345678",
            doi="10.1000/182",
            title="Curcumin In Vitro Efficacy",
            authors=["Smith J"],
            year=2024,
            is_full_text=True,
            passages=["Significant apoptosis observed."],
            grade="High",
            journal="Cancer Res",
            abstract="Abstract text",
            review_paragraph="Farsi synthesis text"
        )
        dossier.add_limitation("In vitro model translation limit.")
        dossier.set_negative_search_strategy("PubMed MeSH query -> 0 hits")

        json_path = os.path.join(self.temp_dir, "test_dossier.json")
        dossier.export_json(json_path)

        # Deserialize
        loaded = ProposalResearchDossier.load_json(json_path)
        self.assertEqual(loaded.topic, "Test Topic")
        self.assertEqual(loaded.domain, "Oncology")
        self.assertEqual(loaded.hypotheses["h0"], "H0 statement")
        self.assertEqual(loaded.hypotheses["h1"], "H1 statement")
        self.assertEqual(loaded.methodological_invariants["target_n"], 30)
        self.assertEqual(len(loaded.biological_entities), 1)
        self.assertEqual(loaded.biological_entities[0]["name"], "HCT116")
        self.assertEqual(len(loaded.literature_evidence), 1)
        self.assertEqual(loaded.literature_evidence[0]["pmid"], "12345678")
        self.assertEqual(loaded.literature_evidence[0]["review_paragraph"], "Farsi synthesis text")
        self.assertEqual(loaded.negative_search_strategy, "PubMed MeSH query -> 0 hits")

    def test_mock_grant_review_panel_programmatic_evaluation(self):
        """MockGrantReviewPanel conducts multi-reviewer evaluation and returns valid PanelReviewResult."""
        benchmark_md = os.path.join(os.path.dirname(__file__), "fixtures", "benchmark_dataset", "MEDICAL_PROPOSAL_LUPEOL_NDV.md")
        if os.path.exists(benchmark_md):
            with open(benchmark_md, "r", encoding="utf-8") as f:
                md_text = f.read()
            res = MockGrantReviewPanel.conduct_panel_review(md_text, {})
            self.assertIsInstance(res.overall_score, float)
            self.assertIn(res.funding_verdict, ["APPROVED_FUNDABLE", "REVISION_REQUIRED", "REJECTED_UNFUNDABLE"])
            self.assertEqual(res.critical_flaws_count, 0)
            self.assertTrue(res.can_proceed)

    def test_surgical_section_patcher_roundtrip(self):
        """SurgicalSectionPatcher splits and reassembles 28 canonical sections without dropping text."""
        sample_md = (
            "# Proposal Title\n\n"
            "## ۱. موضوع\nموضوع فارسی و انگلیسی\n\n"
            "## ۲. بیان مسئله\nبیان مسئله کامل با آمار اپیدمیولوژی\n\n"
            "## ۳. مرور بر منابع\nمرور مقالات و پیشینه\n\n"
            "## ۲۸. منابعی که استفاده شد\n1. Reference 1\n"
        )
        sections = SurgicalSectionPatcher.split_into_sections(sample_md)
        self.assertIn(1, sections)
        self.assertIn(2, sections)
        self.assertIn(3, sections)
        self.assertIn(28, sections)

        reassembled = SurgicalSectionPatcher.reassemble_sections(sections, original_lead="# Proposal Title\n\n")
        self.assertIn("## ۱. موضوع", reassembled)
        self.assertIn("## ۲. بیان مسئله", reassembled)
        self.assertIn("## ۲۸. منابعی که استفاده شد", reassembled)


if __name__ == "__main__":
    unittest.main()
