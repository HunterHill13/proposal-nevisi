#!/usr/bin/env python3
"""
test_generalization.py - Multi-Domain Biomedical Pipeline Generalization Tests
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

Validates that the complete engine runs smoothly across oncology, cardiology,
infectious diseases, and diagnostics without code alterations.
"""

import os
import sys
import json

TESTS_DIR = os.path.dirname(__file__)
FIXTURES_DIR = os.path.join(TESTS_DIR, "fixtures")
SCRIPTS_DIR = os.path.abspath(os.path.join(TESTS_DIR, "..", "scripts"))
sys.path.insert(0, SCRIPTS_DIR)

from research_problem_model import ProblemModelBuilder
from generic_search_planner import GenericSearchPlanner
from generic_study_family_detector import StudyFamilyDetector
from generic_comparability_engine import GenericComparabilityEngine
from generic_contradiction_engine import GenericContradictionEngine
from generic_claim_entailment_engine import GenericClaimEntailmentEngine
from generic_reference_auditor import GenericReferenceAuditor
from generic_evidence_synthesis import GenericEvidenceSynthesizer

FIXTURE_DIRS = [
    "oncology_lupeol_ndv",
    "cardiovascular_sglt2",
    "infectious_antiviral",
    "diagnostic_biomarker"
]

def test_all_fixtures() -> bool:
    print("=" * 70)
    print("RUNNING MULTI-DOMAIN GENERALIZATION EVALUATION")
    print("=" * 70)

    total_fixtures = len(FIXTURE_DIRS)
    passed_fixtures = 0

    for fix_name in FIXTURE_DIRS:
        print(f"\n[EVALUATING DOMAIN FIXTURE]: {fix_name}")
        fix_path = os.path.join(FIXTURES_DIR, fix_name, "fixture_data.json")
        if not os.path.exists(fix_path):
            print(f"  [FAIL] Missing fixture file: {fix_path}")
            continue

        with open(fix_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        try:
            # 1. Problem Model
            model = ProblemModelBuilder.create_from_specification(data["research_problem_model"])
            print(f"  - Model initialized: ID={model.model_id}, Domain={model.domain}, Framework={model.framework}")

            # 2. Search Planner
            planner = GenericSearchPlanner(model)
            matrix = planner.build_query_matrix()
            supp_count = matrix["dual_path_execution"]["supporting_search_count"]
            contra_count = matrix["dual_path_execution"]["contradicting_search_count"]
            print(f"  - Query Matrix: {supp_count} Supporting Queries, {contra_count} Contradicting Queries")
            assert supp_count > 0, "Supporting queries must be > 0"
            assert contra_count > 0, "Contradicting queries must be > 0"

            # 3. Study Family Detection
            studies = data.get("studies", [])
            fam_data = StudyFamilyDetector.cluster_studies(studies)
            print(f"  - Study Families: {fam_data['unique_evidence_families']} families from {fam_data['total_studies_evaluated']} studies")

            # 4. Comparability
            comp = GenericComparabilityEngine.evaluate_cohort(studies)
            print(f"  - Comparability: {comp['summary']['total_pairs_evaluated']} pairs evaluated (High={comp['summary']['high_comparability_count']})")

            # 5. Contradiction & Negative Engine
            neg_findings = []
            for s in studies:
                neg_findings.extend(s.get("negative_or_null_findings", []))
            contra_report = GenericContradictionEngine.build_contradiction_report(neg_findings, matrix["search_boundary"])
            print(f"  - Contradiction status: {contra_report['contradiction_status']}")

            # 6. Evidence Synthesis
            syn = GenericEvidenceSynthesizer.evaluate_claim_synthesis(
                f"CLM_{model.domain.upper()}_PRIMARY",
                f"{model.interventions_or_exposures[0].name} addresses {model.target_condition.name_en}",
                studies,
                []
            )
            print(f"  - Synthesis Certainty: {syn['overall_evidence_certainty']}, Verdict: {syn['synthesis_verdict']}")

            # 7. Reference Audit
            auditor = GenericReferenceAuditor(min_required_references=1)
            for s in studies:
                tier_res = auditor.audit_temporal_tier(s)
                assert tier_res["is_temporally_valid"], f"Temporal invalidity in {s['study_id']}"
            print("  - Temporal & Reference validation: PASSED")

            print(f"  [PASS] Domain fixture '{fix_name}' verified successfully.")
            passed_fixtures += 1

        except Exception as e:
            print(f"  [FAIL] Exception processing fixture '{fix_name}': {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "-" * 70)
    print(f"GENERALIZATION SUMMARY: {passed_fixtures}/{total_fixtures} DOMAIN FIXTURES PASSED")
    print("-" * 70)
    return passed_fixtures == total_fixtures

if __name__ == "__main__":
    success = test_all_fixtures()
    sys.exit(0 if success else 1)
