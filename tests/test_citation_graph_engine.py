#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_citation_graph_engine.py - Unit & Integration Tests for CitationGraphEngine
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

from citation_graph_engine import CitationGraphEngine


class TestCitationGraphEngine(unittest.TestCase):
    """Exhaustive unit test suite for CitationGraphEngine."""

    def setUp(self):
        self.engine = CitationGraphEngine(offline_mode=True, topic_query="PARP inhibitor resistance in TNBC")

        # Create a realistic offline synthetic citation network
        # P1 (Seed: 2022 landmark trial)
        self.p1 = self.engine.add_work_node({
            "id": "PMID:35000001",
            "pmid": "35000001",
            "doi": "10.1038/s41586-022-0001",
            "title": "Olaparib synthetic lethality in BRCA-mutant breast cancer",
            "year": 2022,
            "citation_count": 450,
            "referenced_works": ["PMID:30000001", "PMID:25000001"],
            "category": "HIGHLY_CITED_FOUNDATIONAL"
        }, is_seed=True)

        # P2 (Foundational: 2015 historical bedrock)
        self.p2 = self.engine.add_work_node({
            "id": "PMID:25000001",
            "pmid": "25000001",
            "doi": "10.1056/NEJMoa1500001",
            "title": "Historical identification of PARP1 DNA repair dependencies",
            "year": 2015,
            "citation_count": 1200,
            "referenced_works": [],
            "category": "HISTORICAL_LANDMARK"
        }, is_seed=False)

        # P3 (Intermediate: 2018 methodology benchmark)
        self.p3 = self.engine.add_work_node({
            "id": "PMID:30000001",
            "pmid": "30000001",
            "doi": "10.1158/2159-8290.CD-18-0001",
            "title": "Quantitative clonogenic and RAD51 foci formation assay benchmark",
            "year": 2018,
            "citation_count": 320,
            "referenced_works": ["PMID:25000001"],
            "category": "KEY_METHODOLOGICAL"
        }, is_seed=False)

        # P4 (Contemporaneous: 2025 recent state-of-the-art trial)
        self.p4 = self.engine.add_work_node({
            "id": "PMID:39000001",
            "pmid": "39000001",
            "doi": "10.1016/j.cell.2025.01.001",
            "title": "Overcoming ATR-mediated Olaparib resistance with synergistic combinations",
            "year": 2025,
            "citation_count": 15,
            "referenced_works": ["PMID:30000001", "PMID:25000001"],
            "category": "RECENT_HIGH_IMPACT"
        }, is_seed=False)

        # Connect citation edges
        self.engine.add_citation_edge("PMID:35000001", "PMID:30000001", "CITES")
        self.engine.add_citation_edge("PMID:35000001", "PMID:25000001", "CITES")
        self.engine.add_citation_edge("PMID:30000001", "PMID:25000001", "CITES")
        self.engine.add_citation_edge("PMID:39000001", "PMID:30000001", "CITES")
        self.engine.add_citation_edge("PMID:39000001", "PMID:25000001", "CITES")

    def test_seed_registration(self):
        """Verifies that seed papers are registered and tagged accurately."""
        self.assertIn("PMID:35000001", self.engine.seed_ids)
        self.assertTrue(self.engine.nodes["PMID:35000001"]["is_seed"])
        self.assertFalse(self.engine.nodes["PMID:25000001"]["is_seed"])

    def test_bibliographic_coupling(self):
        """Verifies that papers sharing references are bibliographically coupled."""
        couplings = self.engine.compute_bibliographic_coupling(threshold=0.1)
        self.assertTrue(len(couplings) > 0)
        # P1 and P4 share both PMID:30000001 and PMID:25000001
        p1_p4_found = False
        for c in couplings:
            if (c["source"] == "PMID:35000001" and c["target"] == "PMID:39000001") or \
               (c["source"] == "PMID:39000001" and c["target"] == "PMID:35000001"):
                p1_p4_found = True
                self.assertAlmostEqual(c["similarity"], 1.0, places=2)
        self.assertTrue(p1_p4_found, "P1 and P4 must display near 1.0 bibliographic coupling")

    def test_adamic_adar_proximity(self):
        """Verifies Adamic/Adar link prediction elevates shared specific references."""
        scores = self.engine.compute_adamic_adar_proximity()
        self.assertTrue(len(scores) > 0)
        # Check that P4 received an adamic_adar score relative to seed P1
        p4_score = self.engine.nodes["PMID:39000001"]["scores"].get("adamic_adar_proximity", 0.0)
        self.assertGreater(p4_score, 0.0)

    def test_personalized_pagerank(self):
        """Verifies that Personalized PageRank concentrates authority on foundational roots."""
        ppr = self.engine.compute_personalized_pagerank(alpha=0.15)
        self.assertEqual(len(ppr), 4)
        # Foundational paper P2 (cited by all three other papers) should hold substantial PageRank
        self.assertGreater(ppr["PMID:25000001"], ppr["PMID:39000001"])

    def test_hits_scores(self):
        """Verifies Kleinberg HITS separates authorities from hubs."""
        auth, hub = self.engine.compute_hits_scores()
        # P2 has highest authority because everyone cites it
        self.assertGreaterEqual(auth["PMID:25000001"], auth["PMID:35000001"])
        # P4 cites P3 and P2, so it acts as a hub
        self.assertGreater(hub["PMID:39000001"], hub["PMID:25000001"])

    def test_hummon_doreian_main_path(self):
        """Verifies Main Path Analysis traces the trajectory from root to recent."""
        main_path = self.engine.compute_hummon_doreian_main_path()
        self.assertTrue(len(main_path) >= 2)
        # Root should be historical P2 or P3, not recent P4
        self.assertNotEqual(main_path[0], "PMID:39000001")

    def test_candidate_ranking(self):
        """Verifies that non-seed candidates are ranked with composite scores."""
        self.engine.compute_personalized_pagerank()
        self.engine.compute_hits_scores()
        self.engine.compute_adamic_adar_proximity()
        candidates = self.engine.rank_frontier_candidates(top_k=5)
        self.assertTrue(len(candidates) > 0)
        # None of the ranked candidates should be the seed paper
        for cand in candidates:
            self.assertNotEqual(cand["id"], "PMID:35000001")

    def test_zero_hallucination_integrity_audit(self):
        """Verifies fail-closed integrity validation against fake or corrupt nodes."""
        audit = self.engine.verify_graph_integrity()
        self.assertTrue(audit["is_valid"])
        self.assertEqual(len(audit["violations"]), 0)

        # Inject corrupt node without DOI/PMID
        self.engine.nodes["CORRUPT_NODE"] = {"id": "CORRUPT_NODE", "title": "Fake study"}
        audit2 = self.engine.verify_graph_integrity()
        self.assertFalse(audit2["is_valid"])
        self.assertTrue(any("lacks persistent identifier" in v for v in audit2["violations"]))

    def test_json_schema_export(self):
        """Verifies complete serialization and round-trip JSON persistence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = os.path.join(tmpdir, "LITERATURE_CITATION_GRAPH.json")
            self.engine.save_json(out_file)
            self.assertTrue(os.path.exists(out_file))

            with open(out_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.assertEqual(data["metadata"]["topic_query"], "PARP inhibitor resistance in TNBC")
            self.assertEqual(len(data["nodes"]), 4)
            self.assertTrue(len(data["edges"]) >= 5)
            self.assertIn("PMID:35000001", data["metadata"]["seed_ids"])

    def test_cytoscape_html_generation(self):
        """Verifies that standalone Cytoscape HTML is generated with embedded JSON and UI elements."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_html = os.path.join(tmpdir, "LITERATURE_CITATION_GRAPH.html")
            self.engine.generate_cytoscape_html(out_html)
            self.assertTrue(os.path.exists(out_html))

            with open(out_html, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn("<!DOCTYPE html>", content)
            self.assertIn("cytoscape.min.js", content)
            self.assertIn("PMID:35000001", content)
            self.assertIn("PMID:25000001", content)
            self.assertIn("btn-fit", content)
            self.assertIn("sidebar", content)
            self.assertIn("cose", content)


if __name__ == "__main__":
    unittest.main()
