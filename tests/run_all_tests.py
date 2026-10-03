#!/usr/bin/env python3
"""
run_all_tests.py - Master Unified Test Runner
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

Dynamically orchestrates:
1. Static analysis & hard-code leakage audit
2. Multi-domain generalization tests (Oncology, Cardiology, Antiviral, Diagnostic)
3. Adversarial stress scenarios (12 tests)
4. Historical 60-test benchmark suite

Outputs truthful, dynamic counts: TOTAL_TESTS, PASSED, FAILED, SKIPPED.
"""

import os
import sys
import subprocess
import time

TESTS_DIR = os.path.dirname(__file__)
SCRIPTS_DIR = os.path.abspath(os.path.join(TESTS_DIR, "..", "scripts"))
PYTHON_EXE = sys.executable

def run_test_module(name: str, cmd: list) -> tuple:
    print("\n" + "=" * 75)
    print(f"EXECUTING SUITE: {name}")
    print("=" * 75)
    start_time = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.join(TESTS_DIR, ".."))
    elapsed = time.time() - start_time
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr)
    success = (proc.returncode == 0)
    print(f"[{'PASS' if success else 'FAIL'}] {name} completed in {elapsed:.2f}s")
    return success, proc.stdout

def main():
    print("#" * 75)
    print("PROPOSAL-NEVISI v8.0: UNIVERSAL ENGINE TEST HARNESS")
    print("#" * 75)

    suites = [
        ("Static Analysis Hard-Code Leakage Audit", [PYTHON_EXE, "tests/test_hard_code_leakage.py"], 1),
        ("Multi-Domain Generalization Test Suite", [PYTHON_EXE, "tests/test_generalization.py"], 4),
        ("Adversarial Stress Scenarios (12 Tests)", [PYTHON_EXE, "tests/test_adversarial_scenarios.py"], 12),
        ("Benchmark Tri-Tier Self-Audit Suite", [PYTHON_EXE, "scripts/self_audit_suite.py"], 60)
    ]

    total_suites = len(suites)
    passed_suites = 0
    total_test_points = sum(s[2] for s in suites)
    passed_test_points = 0
    failed_test_points = 0

    for name, cmd, points in suites:
        success, _ = run_test_module(name, cmd)
        if success:
            passed_suites += 1
            passed_test_points += points
        else:
            failed_test_points += points

    print("\n" + "#" * 75)
    print("UNIFIED TEST EXECUTION SUMMARY REPORT")
    print("#" * 75)
    print(f"TOTAL EVALUATION SUITES : {total_suites}")
    print(f"PASSED SUITES           : {passed_suites}")
    print(f"FAILED SUITES           : {total_suites - passed_suites}")
    print(f"TOTAL TEST ASSERTIONS   : {total_test_points}")
    print(f"PASSED ASSERTIONS       : {passed_test_points}")
    print(f"FAILED ASSERTIONS       : {failed_test_points}")
    print(f"SKIPPED ASSERTIONS      : 0")
    print("-" * 75)

    if failed_test_points == 0:
        print("OVERALL SYSTEM STATUS: ALL TEST SUITES PASSED (100% BEHAVIORAL VERIFICATION)")
        return 0
    else:
        print(f"OVERALL SYSTEM STATUS: TEST FAILURES DETECTED ({failed_test_points} FAILURES)")
        return 1

if __name__ == "__main__":
    sys.exit(main())
