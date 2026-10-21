#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_biomedical_concept_graph.py - Unit Tests for BiomedicalConceptGraph
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

from biomedical_concept_graph import BiomedicalConceptGraph


class TestBiomedicalConceptGraph(unittest.TestCase):
    """Exhaustive tests for biological entity-relationship extraction and claim grounding."""

    def setUp(self):
        self.cg = BiomedicalConceptGraph(topic_context="Olaparib and AZD6738 in TNBC")

    def test_entity_registration(self):
        """Verifies canonical entity ID generation and synonym merging."""
        e1 = self.cg.register_entity("DRUG", "Olaparib", synonyms=["AZD2281", "Lynparza"], mesh_id="D000068877")
        self.assertEqual(e1, "DRUG:OLAPARIB")
        self.assertIn("Lynparza", self.cg.entities[e1]["synonyms"])

        # Re-register with more synonyms
        e2 = self.cg.register_entity("DRUG", "Olaparib", synonyms=["KU-0059436"])
        self.assertEqual(e1, e2)
        self.assertIn("KU-0059436", self.cg.entities[e1]["synonyms"])

    def test_relationship_and_bipartite_claim_binding(self):
        """Verifies directed edges and bipartite binding to supporting papers."""
        d = self.cg.register_entity("DRUG", "Olaparib")
        t = self.cg.register_entity("TARGET", "PARP1")
        p = self.cg.register_entity("PATHWAY", "DNA_Repair")

        r1 = self.cg.add_relationship(
            source_id=d,
            relation_type="INHIBITS",
            target_id=t,
            supporting_paper_id="PMID:35000001",
            quantitative_metrics={"ic50": "5.2 nM"},
            abstract_evidence_span="Olaparib potently inhibited PARP1 with an IC50 of 5.2 nM."
        )

        r2 = self.cg.add_relationship(
            source_id=t,
            relation_type="PARTICIPATES_IN",
            target_id=p,
            supporting_paper_id="PMID:25000001"
        )

        self.assertEqual(len(self.cg.relationships), 2)
        self.assertIn("PMID:35000001", self.cg.paper_claims)
        self.assertEqual(self.cg.paper_claims["PMID:35000001"][0]["metrics"]["ic50"], "5.2 nM")

    def test_abstract_parsing_and_metric_extraction(self):
        """Verifies automated extraction of biological claims and metrics from abstract text."""
        abstract = (
            "Triple-negative breast cancer remains difficult to treat. In this study, we investigated "
            "the combination of Olaparib and AZD6738. Olaparib inhibited PARP1 with an IC50 of 12.4 nM. "
            "Furthermore, co-treatment of Olaparib and AZD6738 synergistically suppressed cell proliferation "
            "with a combination index CI of 0.45, overcoming homologous recombination proficiency."
        )
        known = {
            "DRUG": ["Olaparib", "AZD6738"],
            "TARGET": ["PARP1", "ATR"],
            "DISEASE": ["Triple-negative breast cancer"]
        }

        claims = self.cg.ingest_paper_abstract(
            paper_id="PMID:39000001",
            title="Overcoming resistance in TNBC",
            abstract=abstract,
            known_entities=known
        )

        self.assertTrue(len(claims) >= 1)
        # Check if synergy relationship between Olaparib and AZD6738 was captured
        synergy_found = False
        for c in self.cg.relationships:
            if c["relation"] == "SYNERGIZES_WITH":
                synergy_found = True
                self.assertAlmostEqual(c["metrics"].get("ci_value", 0.0), 0.45, places=2)
        self.assertTrue(synergy_found, "Abstract parser must detect SYNERGIZES_WITH with CI=0.45")

    def test_multi_hop_pathfinding(self):
        """Verifies discovery of multi-hop causal paths from drug to disease."""
        d = self.cg.register_entity("DRUG", "Olaparib")
        t = self.cg.register_entity("TARGET", "PARP1")
        p = self.cg.register_entity("PATHWAY", "Base_Excision_Repair")
        dis = self.cg.register_entity("DISEASE", "Breast_Neoplasms")

        self.cg.add_relationship(d, "INHIBITS", t)
        self.cg.add_relationship(t, "PARTICIPATES_IN", p)
        self.cg.add_relationship(p, "DYSREGULATED_IN", dis)

        paths = self.cg.find_mechanistic_paths(d, dis, max_hops=3)
        self.assertEqual(len(paths), 1)
        self.assertEqual(len(paths[0]), 3)
        self.assertEqual(paths[0][0]["source"], d)
        self.assertEqual(paths[0][-1]["target"], dis)

    def test_claim_entailment_query(self):
        """Verifies query_claim_entailment returns True for grounded assertions and False otherwise."""
        d = self.cg.register_entity("DRUG", "Olaparib")
        t = self.cg.register_entity("TARGET", "PARP1")
        self.cg.add_relationship(d, "INHIBITS", t, supporting_paper_id="PMID:1001", quantitative_metrics={"ic50": "5 nM"})

        # Grounded claim
        entailed = self.cg.query_claim_entailment("Olaparib", "INHIBITS", "PARP1")
        self.assertTrue(entailed["is_entailed"])
        self.assertIn("PMID:1001", entailed["supporting_papers"])

        # Ungrounded claim
        unentailed = self.cg.query_claim_entailment("Aspirin", "INHIBITS", "EGFR")
        self.assertFalse(unentailed["is_entailed"])

    def test_json_persistence(self):
        """Verifies serialization and export to BIOMEDICAL_CONCEPT_GRAPH.json."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = os.path.join(tmpdir, "BIOMEDICAL_CONCEPT_GRAPH.json")
            self.cg.register_entity("DRUG", "TestDrug")
            self.cg.save_json(out_file)
            self.assertTrue(os.path.exists(out_file))

            with open(out_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["topic_context"], "Olaparib and AZD6738 in TNBC")
            self.assertEqual(data["total_entities"], 1)


if __name__ == "__main__":
    unittest.main()
