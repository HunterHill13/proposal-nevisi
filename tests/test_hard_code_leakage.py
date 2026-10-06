#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_hard_code_leakage.py - Comprehensive Static Analysis & Anti-Hard-Coding Leakage Gate
Proposal-Nevisi Engine v8.2 (Universal Biomedical Architecture)

Scans ALL Python scripts in scripts/ without manual whitelisting.
Inspects 100% of lines: including code, docstrings, comments, and __main__ blocks.
Asserts that zero case-study specific biological entities, drugs, cell lines,
or assay methods are hardcoded in the core architecture.
"""

import os
import re
import sys
import json
import unittest

sys.stdout.reconfigure(encoding='utf-8')

TESTS_DIR = os.path.dirname(__file__)
SCRIPTS_DIR = os.path.abspath(os.path.join(TESTS_DIR, "..", "scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

FORBIDDEN_HARDCODED_TERMS = [
    r'\blupeol\b',
    r'\bnewcastle disease virus\b',
    r'\bndv\b',
    r'\baf2240\b',
    r'\ba549\b',
    r'\bmrc-5\b',
    r'\b4t1\b',
    r'\blung cancer\b',
    r'\bcurcumin\b',
    r'\bhepg2\b',
    r'\bmcf-7\b',
    r'\bdoxorubicin\b',
    r'\bcisplatin\b',
    r'\bpaxlovid\b'
]

class TestHardCodeLeakage(unittest.TestCase):
    """Dynamic static analysis and semantic generalization test case scanning all scripts in scripts/."""

    def test_semantic_generalization_model_independence(self):
        """Semantic Generalization Audit: Core engines must operate dynamically on arbitrary domain models."""
        from research_problem_model import ProblemModelBuilder
        from dynamic_protocol_designer import DynamicProtocolDesigner
        from generic_search_planner import GenericSearchPlanner

        arbitrary_spec = {
            "model_id": "RPM_ARBITRARY_NEURO_001",
            "research_title_fa": "بررسی اثرات داروی فرضی X در مدل تجربی بیماری پارکینسون",
            "research_title_en": "Evaluation of Hypothetical Neuroprotectant X in Parkinsonian Model",
            "domain": "neurology",
            "framework": "MECHANISTIC",
            "target_condition": {
                "name_en": "Parkinson Disease",
                "name_fa": "بیماری پارکینسون",
                "mesh_term": "Parkinson Disease",
                "synonyms": ["Paralysis Agitans"]
            },
            "population_or_model": {
                "model_type": "CELL_CULTURE_IN_VITRO",
                "primary_system": "SH-SY5Y neuroblastoma cell line",
                "secondary_systems": [],
                "normal_control_system": "Vehicle treated controls"
            },
            "interventions_or_exposures": [
                {
                    "name": "Neuroprotectant X",
                    "chemical_or_biological_class": "Small Molecule Kinase Modulator",
                    "role": "PRIMARY_AGENT",
                    "mesh_terms": [],
                    "synonyms": ["NX-101"]
                }
            ],
            "comparators": [{"name": "0.05% Saline Vehicle", "type": "VEHICLE_CONTROL"}],
            "primary_outcomes": [{"name": "Dopaminergic Neuron Viability", "type": "VIABILITY", "measurement_unit": "% viable neurons"}],
            "hypothesized_mechanisms": [{"pathway_name": "Alpha-Synuclein Autophagy", "target_molecules": ["LC3B", "p62"], "expected_modulation": "UPREGULATION"}],
            "controlled_vocabulary": {"primary_mesh": ["Parkinson Disease"], "all_synonyms": ["NX-101"], "exclusion_terms": []}
        }
        model = ProblemModelBuilder.create_from_specification(arbitrary_spec)
        self.assertEqual(model.domain, "neurology")
        
        # Test DynamicProtocolDesigner operates without domain bias
        var_table = DynamicProtocolDesigner.generate_variable_table(arbitrary_spec)
        self.assertTrue(any("Neuroprotectant X" in v["name"] for v in var_table))
        self.assertTrue(any("Dopaminergic Neuron Viability" in v["name"] for v in var_table))
        
        # Test Search Planner generates domain-specific queries without hardcoded oncology terms
        planner = GenericSearchPlanner(model)
        matrix = planner.build_query_matrix()
        self.assertEqual(matrix["domain"], "neurology")
        all_q_text = json.dumps(matrix).lower()
        self.assertNotIn("cancer", all_q_text)
        self.assertNotIn("tumor", all_q_text)
        self.assertIn("parkinson", all_q_text)
        self.assertIn("neuroprotectant x", all_q_text)

def _make_leakage_test(script_filename):
    def test_method(self):
        script_path = os.path.join(SCRIPTS_DIR, script_filename)
        self.assertTrue(os.path.exists(script_path), f"Script {script_filename} must exist")
        
        with open(script_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        violations = []
        for term_regex in FORBIDDEN_HARDCODED_TERMS:
            matches = re.findall(term_regex, content, re.IGNORECASE)
            if matches:
                violations.extend(matches)

        self.assertEqual(
            len(violations), 0,
            f"Script '{script_filename}' contains {len(violations)} hardcoded domain entity violations: {set(violations)}"
        )
    test_method.__doc__ = f"Static analysis leakage audit for scripts/{script_filename}"
    return test_method

# Dynamically discover all .py files in scripts/ and register a test method for each
all_scripts = sorted([f for f in os.listdir(SCRIPTS_DIR) if f.endswith(".py")])
for script_name in all_scripts:
    clean_name = script_name.replace(".py", "").replace("-", "_")
    test_func_name = f"test_leakage_audit_{clean_name}"
    setattr(TestHardCodeLeakage, test_func_name, _make_leakage_test(script_name))

if __name__ == "__main__":
    unittest.main()
