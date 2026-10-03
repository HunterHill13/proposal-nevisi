#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_hard_code_leakage.py - Comprehensive Static Analysis & Anti-Hard-Coding Leakage Gate
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

Scans ALL Python scripts in scripts/ without manual whitelisting.
Inspects 100% of lines: including code, docstrings, comments, and __main__ blocks.
Asserts that zero case-study specific biological entities, drugs, cell lines,
or assay methods are hardcoded in the core architecture.
"""

import os
import re
import sys
import unittest

sys.stdout.reconfigure(encoding='utf-8')

TESTS_DIR = os.path.dirname(__file__)
SCRIPTS_DIR = os.path.abspath(os.path.join(TESTS_DIR, "..", "scripts"))

FORBIDDEN_HARDCODED_TERMS = [
    r'\blupeol\b',
    r'\bnewcastle disease virus\b',
    r'\bndv\b',
    r'\baf2240\b',
    r'\ba549\b',
    r'\bmrc-5\b',
    r'\b4t1\b',
    r'\bchou-talalay\b',
    r'\blung cancer\b',
    r'\bmtt\b'
]

class TestHardCodeLeakage(unittest.TestCase):
    """Dynamic static analysis test case scanning all scripts in scripts/."""
    pass

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
