#!/usr/bin/env python3
"""
test_hard_code_leakage.py - Static Analysis & Anti-Hard-Coding Leakage Gate
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

Asserts that core generic scripts contain ZERO hard-coded biological entities,
cell lines, or cancer-specific keywords.
"""

import os
import re
import sys

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))

GENERIC_SCRIPTS = [
    "research_problem_model.py",
    "generic_search_planner.py",
    "generic_comparability_engine.py",
    "generic_contradiction_engine.py",
    "generic_claim_entailment_engine.py",
    "generic_reference_auditor.py",
    "generic_study_family_detector.py",
    "generic_evidence_synthesis.py",
    "generic_study_relationships.py",
    "generic_gap_detector.py",
    "proposal_structure_validator.py",
    "dynamic_protocol_designer.py",
    "multi_dimensional_qa_gate.py",
    "project_organizer.py"
]

FORBIDDEN_HARDCODED_TERMS = [
    r'\blupeol\b',
    r'\bnewcastle disease virus\b',
    r'\bndv\b',
    r'\baf2240\b',
    r'\ba549\b',
    r'\bmrc-5\b',
    r'\b4t1\b',
    r'\bchou-talalay\b',
    r'\blung cancer\b'
]

def run_leakage_audit() -> bool:
    print("=" * 70)
    print("RUNNING STATIC ANALYSIS: HARD-CODED DOMAIN LEAKAGE AUDIT")
    print("=" * 70)

    total_violations = 0

    for script_name in GENERIC_SCRIPTS:
        script_path = os.path.join(SCRIPTS_DIR, script_name)
        if not os.path.exists(script_path):
            print(f"[FAIL] Script not found: {script_name}")
            total_violations += 1
            continue

        with open(script_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Ignore lines in `if __name__ == "__main__":` demo blocks
        in_demo_block = False
        script_violations = 0

        for line_num, line in enumerate(lines, 1):
            if 'if __name__ == "__main__":' in line:
                in_demo_block = True
            if in_demo_block:
                continue

            # Strip comments and docstrings
            stripped = line.split('#')[0].strip()
            if not stripped:
                continue

            for term_regex in FORBIDDEN_HARDCODED_TERMS:
                match = re.search(term_regex, stripped, re.IGNORECASE)
                if match:
                    print(f"[LEAKAGE] {script_name}:{line_num} contains hardcoded '{match.group(0)}':")
                    print(f"    Line {line_num}: {stripped}")
                    script_violations += 1
                    total_violations += 1

        if script_violations == 0:
            print(f"[PASS] {script_name}: 0 hardcoded domain entities found.")

    print("-" * 70)
    if total_violations == 0:
        print("[PASS] HARD-CODE AUDIT: Zero domain leakages in core generic scripts.")
        return True
    else:
        print(f"[FAIL] HARD-CODE AUDIT: {total_violations} domain leakages detected.")
        return False

if __name__ == "__main__":
    success = run_leakage_audit()
    sys.exit(0 if success else 1)
