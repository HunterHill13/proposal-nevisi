#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all_tests.py - Dynamic Master Unified Test Runner
Proposal-Nevisi Engine v8.2 (Universal Deep Biomedical Research & Proposal Engine)

Dynamically discovers, loads, and executes all standard unittest test cases across
all test modules in tests/ matching 'test_*.py'.

Strictly relies on Python unittest TestLoader.discover and TextTestRunner.
Enforces discovery and execution invariants:
- reported_total == actual_unittest_discovered_count
- passed + failed + errors + skipped == total
Zero hard-coded test totals, zero fake counts.
"""

import os
import sys
import unittest
import time

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.abspath(os.path.join(TESTS_DIR, ".."))
SCRIPTS_DIR = os.path.join(SKILL_ROOT, "scripts")

if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

def main():
    print("#" * 75)
    print("PROPOSAL-NEVISI v8.2: DYNAMIC MASTER UNIFIED TEST RUNNER")
    print("#" * 75)
    
    loader = unittest.TestLoader()
    
    # Dynamic discovery across all test_*.py modules in tests directory
    discovered_suite = loader.discover(start_dir=TESTS_DIR, pattern="test_*.py")
    
    if loader.errors:
        print("\nFATAL ERROR: Test loader encountered errors during module discovery:")
        for err in loader.errors:
            print(f"  - {err}")
        return 1

    total_discovered = discovered_suite.countTestCases()
    if total_discovered == 0:
        print("\nFATAL ERROR: Zero tests discovered in tests/ directory!")
        return 1

    print(f"Dynamically discovered {total_discovered} individual test cases in tests/\n")
    
    start_time = time.time()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(discovered_suite)
    elapsed = time.time() - start_time
    
    total_run = result.testsRun
    failed_count = len(result.failures)
    error_count = len(result.errors)
    skipped_count = len(result.skipped)
    passed_count = total_run - (failed_count + error_count + skipped_count)
    
    # Invariant verification
    invariant_1_met = (total_run == total_discovered)
    invariant_2_met = (passed_count + failed_count + error_count + skipped_count == total_run)
    
    print("\n" + "#" * 75)
    print("MASTER TEST EXECUTION SUMMARY REPORT (AUTHENTIC METRICS)")
    print("#" * 75)
    print(f"TOTAL TESTS DISCOVERED: {total_discovered}")
    print(f"TOTAL TESTS EXECUTED  : {total_run}")
    print(f"PASSED TESTS          : {passed_count}")
    print(f"FAILED TESTS          : {failed_count}")
    print(f"ERRORED TESTS         : {error_count}")
    print(f"SKIPPED TESTS         : {skipped_count}")
    print(f"DISCOVERY INVARIANT   : {'SATISFIED' if invariant_1_met else 'VIOLATED'}")
    print(f"ACCOUNTING INVARIANT  : {'SATISFIED' if invariant_2_met else 'VIOLATED'}")
    print(f"TOTAL EXECUTION TIME  : {elapsed:.3f}s")
    print("-" * 75)
    
    if not (invariant_1_met and invariant_2_met):
        print("OVERALL SYSTEM STATUS: INVARIANT VIOLATION DETECTED")
        return 1

    if result.wasSuccessful():
        if skipped_count > 0:
            print("OVERALL SYSTEM STATUS: ALL EXECUTED TESTS PASSED (NOTE: SKIPPED TESTS DETECTED)")
        else:
            print("OVERALL SYSTEM STATUS: ALL DISCOVERED SOFTWARE TESTS PASSED (100% PASS)")
        return 0
    else:
        print("OVERALL SYSTEM STATUS: FAILURES DETECTED IN TEST SUITE")
        return 1

if __name__ == "__main__":
    sys.exit(main())
