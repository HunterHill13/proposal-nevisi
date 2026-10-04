#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
self_audit_suite.py - Backward Compatibility Shim for Benchmark Test Suite
Proposal-Nevisi Engine v8.2 (Universal Biomedical Architecture)

Delegates to tests/test_benchmark_audit.py.
"""

import os
import sys

tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tests"))
sys.path.insert(0, tests_dir)

try:
    from test_benchmark_audit import run_v7_audit, run_benchmark_audit
except ImportError:
    run_v7_audit = None
    run_benchmark_audit = None

def main():
    if run_v7_audit:
        sys.exit(run_v7_audit())
    else:
        print("Error: test_benchmark_audit module not found", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
