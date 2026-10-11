#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_v87_on_real_data.py - Evaluate v8.7 Gates on the Real-World 25 References
"""

import sys
import json
from scripts.generic_reference_auditor import (
    CanonicalPaperEvidenceRecord,
    NumericProvenanceGate,
    ContextualBoundaryGate,
    ExactClaimEvidenceMapper,
    EvidenceDrivenParagraphBuilder
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def main():
    with open("real_world_reference_audits_detailed.json", "r", encoding="utf-8") as f:
        audits = json.load(f)

    print("=================================================================")
    print("EVALUATING v8.7 GATES ON REAL-WORLD REFERENCE PORTFOLIO")
    print("=================================================================\n")

    boundary_gate = ContextualBoundaryGate()
    numeric_gate = NumericProvenanceGate()
    claim_mapper = ExactClaimEvidenceMapper()

    flagged_intervention_mismatches = []
    flagged_formulation_mismatches = []
    flagged_model_mismatches = []

    for a in audits:
        ref_num = a["ref_num"]
        actual_int = a["actual_intervention"]
        form_ent = a["formulation_entity"]
        model = a["model_system"]
        
        paper_rec = {
            "title": a["title"],
            "model_system": model,
            "formulation_entity": form_ent,
            "study_design": a["study_design"],
            "intervention": actual_int,
            "quantitative_findings": "IC50 = 2.45 uM; non-cytotoxic; CI = 0.85" if ref_num in [1, 5, 13, 20] else "NOT_REPORTED"
        }

        # 1. Test Intervention & Formulation Boundaries
        # If proposal claims Lupeol from an unrelated paper
        test_claim = {
            "claim_text": f"لوپئول در رده سلولی A549 موجب القای آپوپتوز و مهار تکثیر سلولی می‌گردد [{ref_num}]",
            "target_model": "A549",
            "target_intervention": "Lupeol",
            "target_formulation": "PURE_CONSTITUENT"
        }

        boundary_res = boundary_gate.audit_context_boundaries(test_claim, paper_rec)
        mismatches = boundary_res["mismatches"]
        
        if "FORMULATION_MISMATCH" in mismatches:
            flagged_formulation_mismatches.append(ref_num)
        if "MODEL_MISMATCH" in mismatches:
            flagged_model_mismatches.append(ref_num)

        # 2. Test Claim-Evidence Mapping
        claim_obj = {
            "claim_id": f"CLM_{ref_num:03d}",
            "claim_text": test_claim["claim_text"],
            "target_intervention": "Lupeol",
            "target_model": "A549"
        }
        map_res = claim_mapper.map_and_verify_claim(claim_obj, paper_rec)
        verdict = map_res["verdict"]


        print(f"Ref [{ref_num:02d}] {a['authors']:<20} | {actual_int:<22} | Verdict: {verdict:<15} | Mismatches: {mismatches}")

    print("\n-----------------------------------------------------------------")
    print(f"Summary of v8.7 Detections on Real-World Data:")
    print(f"  - Formulation Mismatches detected: {len(flagged_formulation_mismatches)} papers (Refs: {flagged_formulation_mismatches})")
    print(f"  - Model Mismatches detected: {len(flagged_model_mismatches)} papers (Refs: {flagged_model_mismatches})")

if __name__ == "__main__":
    main()
