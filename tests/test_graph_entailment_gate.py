#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_graph_entailment_gate.py - Unit Tests for GraphEntailmentGate
Proposal-Nevisi v12.0
"""

import os
import sys
import unittest
import tempfile
import json

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.abspath(os.path.join(TESTS_DIR, "..", "scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from graph_entailment_gate import GraphEntailmentGate


class TestGraphEntailmentGate(unittest.TestCase):
    """Exhaustive tests for anti-hallucination and anti-fluff verification."""

    def setUp(self):
        # Synthetic mock citation and concept graphs
        self.mock_citation_graph = {
            "nodes": [
                {
                    "id": "PMID:35000001",
                    "pmid": "35000001",
                    "doi": "10.1038/s41586-022-0001",
                    "title": "Olaparib trial"
                },
                {
                    "id": "PMID:25000001",
                    "pmid": "25000001",
                    "doi": "10.1056/nejmoa1500001",
                    "title": "PARP1 bedrock"
                }
            ]
        }
        self.mock_concept_graph = {
            "entities": [
                {"canonical_name": "Olaparib", "synonyms": ["AZD2281"]},
                {"canonical_name": "PARP1", "synonyms": []},
                {"canonical_name": "Breast Cancer", "synonyms": ["TNBC"]}
            ]
        }
        self.gate = GraphEntailmentGate(self.mock_citation_graph, self.mock_concept_graph)

    def test_verified_citation_accepted(self):
        """Sentence citing a verified, indexed PMID and DOI is accepted."""
        sent = "Olaparib monotherapy demonstrated significant clinical efficacy in homologous recombination-deficient tumors [PMID: 35000001]."
        res = self.gate.audit_sentence(sent)
        self.assertEqual(res["status"], "ACCEPT")
        self.assertIn("PMID:35000001", res["verified_citations"])
        self.assertEqual(len(res["invalid_citations"]), 0)

    def test_fabricated_citation_rejected(self):
        """Sentence citing a non-existent, fabricated PMID is strictly rejected fail-closed."""
        sent = "Recent clinical data reported a 95% response rate in refractory carcinomas [PMID: 99999999]."
        res = self.gate.audit_sentence(sent)
        self.assertEqual(res["status"], "REJECT")
        self.assertIn("PMID:99999999", res["invalid_citations"])
        self.assertTrue(any("Unverified or fabricated" in r for r in res["reasons"]))

    def test_generic_fluff_rejected(self):
        """Low-information generic AI boilerplate sentences are detected and rejected."""
        sent = "Cancer is a major public health challenge worldwide and plays a crucial role in modern medicine."
        res = self.gate.audit_sentence(sent)
        self.assertEqual(res["status"], "REJECT")
        self.assertTrue(res["is_fluff"])
        self.assertTrue(any("Generic low-information AI boilerplate" in r for r in res["reasons"]))

    def test_persian_fluff_rejected(self):
        """Persian AI clichés without numbers are flagged as fluff."""
        sent = "سرطان یکی از بزرگ‌ترین چالش‌های سلامت جهان است و مطالعات بسیاری نشان داده‌اند که باید تحقیق کرد."
        res = self.gate.audit_sentence(sent)
        self.assertEqual(res["status"], "REJECT")
        self.assertTrue(res["is_fluff"])

    def test_dense_scientific_claim_accepted(self):
        """Quantitative sentence with biological entities and verified citations receives high density score."""
        sent = "Co-administration of Olaparib (10 µM) reduced PARP1 catalytic activity by 78.4% (p < 0.01) [PMID: 35000001]."
        res = self.gate.audit_sentence(sent)
        self.assertEqual(res["status"], "ACCEPT")
        self.assertFalse(res["is_fluff"])
        self.assertGreater(res["density_score"], 0.70)

    def test_full_proposal_audit_report_generation(self):
        """Verifies section audits and audit report persistence."""
        sections = {
            "Section_03_Background": (
                "Olaparib demonstrated potent target engagement against PARP1 [PMID: 35000001]. "
                "Cancer is a major public health challenge worldwide."
            ),
            "Section_27_Methodology": (
                "Clonogenic survival will be quantified across serial dilutions with Vehicle Control."
            )
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            out_audit = os.path.join(tmpdir, "claim_entailment_audit.json")
            report = self.gate.audit_full_proposal(sections, output_audit_path=out_audit)
            self.assertTrue(os.path.exists(out_audit))

            with open(out_audit, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.assertEqual(data["overall_summary"]["total_sections_audited"], 2)
            self.assertEqual(data["overall_summary"]["total_fluff_detected"], 1)
            self.assertEqual(data["sections"]["Section_03_Background"]["rejected_count"], 1)


if __name__ == "__main__":
    unittest.main()
