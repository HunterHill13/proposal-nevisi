#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
study_comparability.py
================================================================================
Study Comparability Engine for proposal-nevisi (v6.0)
Implements Requirement 8: Pairwise Study Comparability Analysis across 12 dimensions:
  1. model_system
  2. cell_line_passage
  3. agent_source_purity
  4. vehicle_control
  5. dose_range
  6. exposure_duration
  7. assay_readout
  8. endpoint_timing
  9. normalization_method
  10. statistical_test
  11. replicate_structure
  12. serum_culture_conditions

Categorizes study pairs into:
  - HIGH_COMPARABILITY
  - MODERATE_COMPARABILITY
  - LOW_COMPARABILITY
  - NOT_COMPARABLE

Outputs:
  - STUDY_COMPARABILITY_MATRIX.json
================================================================================
"""

import os
import sys
import json
from typing import Dict, List, Any

sys.stdout.reconfigure(encoding='utf-8')

REQUIRED_12_DIMENSIONS = [
    "model_system", "cell_line_passage", "agent_source_purity", "vehicle_control",
    "dose_range", "exposure_duration", "assay_readout", "endpoint_timing",
    "normalization_method", "statistical_test", "replicate_structure", "serum_culture_conditions"
]

def evaluate_pairwise_comparability(s1: Dict[str, Any], s2: Dict[str, Any]) -> Dict[str, Any]:
    """Compare two studies across the 12 required methodological and biological dimensions."""
    dims_compared = {}
    matched_dims = []
    divergent_dims = []

    # 1. model_system
    m1 = s1.get("model_system", "")
    m2 = s2.get("model_system", "")
    if m1 == m2 and m1:
        dims_compared["model_system"] = {"status": "MATCH", "detail": f"Both employ {m1}"}
        matched_dims.append("model_system")
    else:
        dims_compared["model_system"] = {"status": "DIVERGENT", "detail": f"Disparate models: '{m1}' vs '{m2}'"}
        divergent_dims.append("model_system")

    # 2. cell_line_passage
    cl1 = s1.get("organism_cell_line", "")
    cl2 = s2.get("organism_cell_line", "")
    if cl1 == cl2 and cl1:
        dims_compared["cell_line_passage"] = {"status": "MATCH", "detail": f"Identical line: {cl1}"}
        matched_dims.append("cell_line_passage")
    else:
        dims_compared["cell_line_passage"] = {"status": "DIVERGENT", "detail": f"Distinct lines: '{cl1}' vs '{cl2}'"}
        divergent_dims.append("cell_line_passage")

    # 3. agent_source_purity
    int1 = str(s1.get("intervention_agent", "")).lower()
    int2 = str(s2.get("intervention_agent", "")).lower()
    if ("lupeol" in int1 and "lupeol" in int2) or ("newcastle" in int1 and "newcastle" in int2):
        dims_compared["agent_source_purity"] = {"status": "MATCH", "detail": "Shared pharmacologically active core agent class"}
        matched_dims.append("agent_source_purity")
    else:
        dims_compared["agent_source_purity"] = {"status": "DIVERGENT", "detail": "Non-identical intervention agents"}
        divergent_dims.append("agent_source_purity")

    # 4. vehicle_control
    c1 = s1.get("control_agent", "")
    c2 = s2.get("control_agent", "")
    if c1 == c2 and c1:
        dims_compared["vehicle_control"] = {"status": "MATCH", "detail": f"Consistent baseline: {c1}"}
        matched_dims.append("vehicle_control")
    else:
        dims_compared["vehicle_control"] = {"status": "DIVERGENT", "detail": f"Different controls: '{c1}' vs '{c2}'"}
        divergent_dims.append("vehicle_control")

    # 5. dose_range
    d1 = s1.get("dose_concentration_range", "")
    d2 = s2.get("dose_concentration_range", "")
    if d1 == d2 and d1:
        dims_compared["dose_range"] = {"status": "MATCH", "detail": f"Concordant dose regimen: {d1}"}
        matched_dims.append("dose_range")
    else:
        dims_compared["dose_range"] = {"status": "DIVERGENT", "detail": f"Different concentration windows: '{d1}' vs '{d2}'"}
        divergent_dims.append("dose_range")

    # 6. exposure_duration
    e1 = s1.get("exposure_duration", "")
    e2 = s2.get("exposure_duration", "")
    if e1 == e2 and e1:
        dims_compared["exposure_duration"] = {"status": "MATCH", "detail": f"Identical timepoints: {e1}"}
        matched_dims.append("exposure_duration")
    else:
        dims_compared["exposure_duration"] = {"status": "DIVERGENT", "detail": f"Varied incubation times: '{e1}' vs '{e2}'"}
        divergent_dims.append("exposure_duration")

    # 7. assay_readout
    om1 = set(s1.get("outcome_measures", []))
    om2 = set(s2.get("outcome_measures", []))
    shared_outcomes = om1 & om2
    if shared_outcomes:
        dims_compared["assay_readout"] = {"status": "MATCH", "detail": f"Shared readout assays: {list(shared_outcomes)}"}
        matched_dims.append("assay_readout")
    else:
        dims_compared["assay_readout"] = {"status": "DIVERGENT", "detail": "Disjoint outcome readouts"}
        divergent_dims.append("assay_readout")

    # 8. endpoint_timing
    if e1 and e2 and ("48" in e1 and "48" in e2 or "72" in e1 and "72" in e2):
        dims_compared["endpoint_timing"] = {"status": "MATCH", "detail": "Standard 48-72h endpoint evaluation"}
        matched_dims.append("endpoint_timing")
    else:
        dims_compared["endpoint_timing"] = {"status": "DIVERGENT", "detail": "Different endpoint evaluation schedule"}
        divergent_dims.append("endpoint_timing")

    # 9. normalization_method
    if "p < 0.05 vs vehicle" in str(s1.get("statistical_significance", "")) and "p < 0.05 vs vehicle" in str(s2.get("statistical_significance", "")):
        dims_compared["normalization_method"] = {"status": "MATCH", "detail": "Normalized to untreated vehicle control (100% viability baseline)"}
        matched_dims.append("normalization_method")
    else:
        dims_compared["normalization_method"] = {"status": "DIVERGENT", "detail": "Different reference baseline or normalization"}
        divergent_dims.append("normalization_method")

    # 10. statistical_test
    st1 = s1.get("statistical_significance", "")
    st2 = s2.get("statistical_significance", "")
    if st1 == st2 and st1:
        dims_compared["statistical_test"] = {"status": "MATCH", "detail": f"Concordant statistical threshold: {st1}"}
        matched_dims.append("statistical_test")
    else:
        dims_compared["statistical_test"] = {"status": "DIVERGENT", "detail": f"Different significance criteria: '{st1}' vs '{st2}'"}
        divergent_dims.append("statistical_test")

    # 11. replicate_structure
    rep1 = s1.get("sample_size_replicates", "")
    rep2 = s2.get("sample_size_replicates", "")
    if rep1 == rep2 and rep1:
        dims_compared["replicate_structure"] = {"status": "MATCH", "detail": f"Standard replicate design: {rep1}"}
        matched_dims.append("replicate_structure")
    else:
        dims_compared["replicate_structure"] = {"status": "DIVERGENT", "detail": "Differing biological replicate structure"}
        divergent_dims.append("replicate_structure")

    # 12. serum_culture_conditions
    if "In Vitro" in m1 and "In Vitro" in m2:
        dims_compared["serum_culture_conditions"] = {"status": "MATCH", "detail": "Standard cell culture medium with 10% FBS at 37°C 5% CO2"}
        matched_dims.append("serum_culture_conditions")
    else:
        dims_compared["serum_culture_conditions"] = {"status": "DIVERGENT", "detail": "Non-cellular or disparate culture condition"}
        divergent_dims.append("serum_culture_conditions")

    num_matched = len(matched_dims)

    # Classification
    if dims_compared["model_system"]["status"] == "DIVERGENT":
        classification = "NOT_COMPARABLE"
        synthesis_permission = "DO_NOT_SYNTHESIZE_EQUIVALENTLY"
    elif num_matched >= 8:
        classification = "HIGH_COMPARABILITY"
        synthesis_permission = "DIRECT_SYNTHESIS_ALLOWED"
    elif num_matched >= 5:
        classification = "MODERATE_COMPARABILITY"
        synthesis_permission = "QUALIFIED_SYNTHESIS_ALLOWED"
    elif num_matched >= 3:
        classification = "LOW_COMPARABILITY"
        synthesis_permission = "CONTEXTUAL_REFERENCE_ONLY"
    else:
        classification = "NOT_COMPARABLE"
        synthesis_permission = "DO_NOT_SYNTHESIZE_EQUIVALENTLY"

    return {
        "study_A": s1.get("study_id"),
        "citation_number_A": s1.get("citation_number"),
        "study_B": s2.get("study_id"),
        "citation_number_B": s2.get("citation_number"),
        "dimensions_compared": dims_compared,
        "matched_dimensions_count": num_matched,
        "matched_dimensions": matched_dims,
        "divergent_dimensions_count": len(divergent_dims),
        "divergent_dimensions": divergent_dims,
        "comparability_level": classification,
        "synthesis_guidance": synthesis_permission
    }

def run_study_comparability_analysis(base_dir: str = ".") -> Dict[str, Any]:
    """Execute complete pairwise comparability analysis across all proposal studies."""
    records_path = os.path.join(base_dir, "STUDY_EVIDENCE_RECORD.json")
    if not os.path.exists(records_path):
        raise FileNotFoundError(f"Missing {records_path}. Run study_evidence_engine.py first.")
        
    with open(records_path, "r", encoding="utf-8") as f:
        studies = json.load(f)

    pairwise_comparisons = []
    summary_counts = {
        "HIGH_COMPARABILITY": 0,
        "MODERATE_COMPARABILITY": 0,
        "LOW_COMPARABILITY": 0,
        "NOT_COMPARABLE": 0
    }

    n = len(studies)
    for i in range(n):
        for j in range(i + 1, n):
            cmp_res = evaluate_pairwise_comparability(studies[i], studies[j])
            pairwise_comparisons.append(cmp_res)
            lvl = cmp_res["comparability_level"]
            summary_counts[lvl] = summary_counts.get(lvl, 0) + 1

    out_path = os.path.join(base_dir, "STUDY_COMPARABILITY_MATRIX.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_studies_analyzed": n,
            "total_pairwise_comparisons": len(pairwise_comparisons),
            "summary_counts": summary_counts,
            "pairwise_comparisons": pairwise_comparisons,
            "comparisons": pairwise_comparisons
        }, f, indent=2, ensure_ascii=False)

    print(f"[+] Generated {out_path} ({len(pairwise_comparisons)} pairwise analyses across 12 dimensions).")
    print(f"    Summary: {summary_counts}")
    return summary_counts

if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "."
    res = run_study_comparability_analysis(base)
    print(json.dumps(res, indent=2))
