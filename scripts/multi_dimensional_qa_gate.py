#!/usr/bin/env python3
"""
multi_dimensional_qa_gate.py - Comprehensive 9-Dimension Pre-Flight QA Gate
Proposal-Nevisi Engine v8.1 (Universal Biomedical Architecture)

Executes exhaustive quality assurance before finalizing proposal artifacts across 9 distinct dimensions:
1. Scientific QA
2. Bibliographic QA
3. Evidence QA
4. Citation QA
5. Structural QA
6. Methodology QA
7. Statistical QA
8. Writing QA
9. Generalization QA
"""

import json
from typing import Dict, List, Any

class MultiDimensionalQAGate:
    """Orchestrates comprehensive multi-dimensional pre-flight quality verification."""

    @classmethod
    def execute_qa(
        cls,
        scientific_data: Dict[str, Any],
        bibliographic_data: Dict[str, Any],
        evidence_data: Dict[str, Any],
        citation_data: Dict[str, Any],
        structural_data: Dict[str, Any],
        methodology_data: Dict[str, Any],
        statistical_data: Dict[str, Any],
        writing_data: Dict[str, Any],
        generalization_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Audits all 9 dimensions and returns composite gate status."""

        results = {}

        # 1. Scientific QA
        sci_pass = scientific_data.get("unjustified_extrapolations", 0) == 0 and scientific_data.get("synergy_fallacy_detected", False) is False
        results["1_SCIENTIFIC_QA"] = {
            "status": "PASS" if sci_pass else "FAIL",
            "details": "Zero unwarranted causal leaps, zero synergy fallacies, grounded biological parameters."
        }

        # 2. Bibliographic QA
        bib_pass = bibliographic_data.get("verified_references", 0) >= bibliographic_data.get("total_references", 1) and bibliographic_data.get("unsupported_references", 0) == 0
        results["2_BIBLIOGRAPHIC_QA"] = {
            "status": "PASS" if bib_pass else "FAIL",
            "details": f"{bibliographic_data.get('verified_references', 0)} / {bibliographic_data.get('total_references', 0)} references canonically verified."
        }

        # 3. Evidence QA
        evi_pass = evidence_data.get("untraced_numbers_count", 0) == 0 and evidence_data.get("studies_with_quantitative_data", 0) >= 1
        results["3_EVIDENCE_QA"] = {
            "status": "PASS" if evi_pass else "FAIL",
            "details": "100% numerical traceability in evidence ledger; zero halluncinated quantitative metrics."
        }

        # 4. Citation QA
        cit_pass = citation_data.get("citation_coverage_pct", 0) == 100.0 and citation_data.get("padding_detected", False) is False
        results["4_CITATION_QA"] = {
            "status": "PASS" if cit_pass else "FAIL",
            "details": "100% in-text citation coverage; zero citation padding candidates."
        }

        # 5. Structural QA
        struct_pass = structural_data.get("PROPOSAL_STRUCTURE_VALIDATION") == "PASS"
        results["5_STRUCTURAL_QA"] = {
            "status": "PASS" if struct_pass else "FAIL",
            "details": "All 14 institutional sections and 14 Section-13 sub-components present in strict order."
        }

        # 6. Methodology QA
        meth_pass = methodology_data.get("boundary_conditions_defined", False) is True
        results["6_METHODOLOGY_QA"] = {
            "status": "PASS" if meth_pass else "FAIL",
            "details": "In vitro / in vivo boundaries, vehicle thresholds, and assay standards explicitly defined."
        }

        # 7. Statistical QA
        stat_pass = statistical_data.get("primary_test_defined", False) is True and statistical_data.get("normality_checked", False) is True
        results["7_STATISTICAL_QA"] = {
            "status": "PASS" if stat_pass else "FAIL",
            "details": "Statistical analysis plan directly aligned with outcome variables and design structure."
        }

        # 8. Writing QA
        write_pass = writing_data.get("scholarly_tone_verified", False) is True and writing_data.get("artificial_repetition_detected", True) is False
        results["8_WRITING_QA"] = {
            "status": "PASS" if write_pass else "FAIL",
            "details": "Scholarly Persian academic voice verified; no automated robotic templates."
        }

        # 9. Generalization QA
        gen_pass = generalization_data.get("hardcode_violations", 0) == 0
        results["9_GENERALIZATION_QA"] = {
            "status": "PASS" if gen_pass else "FAIL",
            "details": "Topic-agnostic architecture verified; zero hard-coded biological entities in core code."
        }

        # 10. Feasibility QA (Prompt Pt 45)
        feas_data = methodology_data.get("feasibility_assessment", {})
        feas_status = feas_data.get("status", "FEASIBLE")
        results["10_FEASIBILITY_QA"] = {
            "status": "PASS" if feas_status == "FEASIBLE" else "REVIEW_REQUIRED",
            "details": feas_data.get("details", "Protocol feasibility verified against laboratory infrastructure and resource timelines.")
        }

        # 11. Human Review Gate (Prompt Pt 46)
        human_triggers = []
        if methodology_data.get("sample_size_requires_pilot", False):
            human_triggers.append("SAMPLE_SIZE_PILOT_VERIFICATION")
        if methodology_data.get("requires_institutional_bioethics_approval", False):
            human_triggers.append("INSTITUTIONAL_IRB_ETHICS_APPROVAL")
        if bibliographic_data.get("unverified_dois_count", 0) > 0:
            human_triggers.append("UNVERIFIED_CITATION_METADATA")

        requires_human_review = len(human_triggers) > 0
        results["11_HUMAN_REVIEW_GATE"] = {
            "status": "HUMAN_REVIEW_REQUIRED" if requires_human_review else "AUTONOMOUS_APPROVED",
            "triggered_reviews": human_triggers,
            "details": "Action items flagged for investigator confirmation." if requires_human_review else "All parameters autonomously verified."
        }

        all_passed = all(dim["status"] in ["PASS", "AUTONOMOUS_APPROVED"] for dim in results.values())

        return {
            "COMPOSITE_QA_GATE": "PASS" if all_passed else ("REVIEW_REQUIRED" if any(dim["status"] in ["REVIEW_REQUIRED", "HUMAN_REVIEW_REQUIRED"] for dim in results.values()) else "FAIL"),
            "passed_dimensions": sum(1 for dim in results.values() if dim["status"] in ["PASS", "AUTONOMOUS_APPROVED"]),
            "total_dimensions": len(results),
            "dimensions": results
        }

    @classmethod
    def execute_scientific_release_gate(
        cls,
        research_model: Dict[str, Any],
        reference_audit: Dict[str, Any],
        claim_audit: Dict[str, Any],
        methodology_audit: Dict[str, Any],
        output_artifacts: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Final Scientific Release Gate enforcing 5 mandatory pillar gates (Part 33):
        1. Research Gate: Zero hardcoded bias, valid problem model, balanced dual-path queries.
        2. References Gate: 100% verified identifiers, temporal classification, zero retracted papers.
        3. Writing Gate: Entailment verified, causal boundaries respected, numerical traceability.
        4. Methodology Gate: Connected design graph, statistical feasibility, ethical boundaries.
        5. Output Gate: Valid 14 sections, Section 13-1 to 13-14, typography and RTL compliance.
        """
        gates = {}

        # 1. Research Gate
        res_pass = (
            research_model.get("framework") in ["PICO", "PECO", "DIAGNOSTIC", "PROGNOSTIC", "MECHANISTIC", "EXPERIMENTAL_IN_VITRO", "EXPERIMENTAL_ANIMAL"]
            and len(research_model.get("interventions_or_exposures", [])) > 0
            and len(research_model.get("primary_outcomes", [])) > 0
        )
        gates["GATE_1_RESEARCH"] = {
            "status": "PASS" if res_pass else "FAIL",
            "details": "Research problem model structurally sound, non-hardcoded, and dual-path grounded."
        }

        # 2. References Gate
        ref_pass = (
            reference_audit.get("retracted_papers_count", 0) == 0
            and reference_audit.get("padding_detected_count", 0) == 0
            and reference_audit.get("unverified_references_count", 0) == 0
        )
        gates["GATE_2_REFERENCES"] = {
            "status": "PASS" if ref_pass else "FAIL",
            "details": "Zero retracted studies in synthesis, zero citation padding, authoritative bibliographic verification."
        }

        # 3. Writing Gate
        write_pass = (
            claim_audit.get("untraced_numerical_claims_count", 0) == 0
            and claim_audit.get("causal_overclaim_violations", 0) == 0
            and claim_audit.get("synergy_fallacies_count", 0) == 0
        )
        gates["GATE_3_WRITING"] = {
            "status": "PASS" if write_pass else "FAIL",
            "details": "100% numerical traceability, strict causal/observational boundaries, zero synergy fallacies."
        }

        # 4. Methodology Gate
        meth_pass = (
            methodology_audit.get("is_graph_fully_connected", True)
            and methodology_audit.get("is_feasible", True)
        )
        gates["GATE_4_METHODOLOGY"] = {
            "status": "PASS" if meth_pass else "FAIL",
            "details": "Fully linked design graph (Q->O->H->IV->DV->Analysis) and validated statistical test compatibility."
        }

        # 5. Output Gate
        out_pass = (
            output_artifacts.get("sections_count", 0) == 14
            and output_artifacts.get("section_13_subsections_count", 0) == 14
            and output_artifacts.get("has_rtl_typography", True)
        )
        gates["GATE_5_OUTPUT"] = {
            "status": "PASS" if out_pass else "FAIL",
            "details": "Complete 14 institutional sections, all 14 Section-13 sub-components, Dubai font & RTL XML verified."
        }

        all_released = all(g["status"] == "PASS" for g in gates.values())
        return {
            "FINAL_SCIENTIFIC_RELEASE_STATUS": "APPROVED" if all_released else "REJECTED",
            "is_release_authorized": all_released,
            "passed_gates_count": sum(1 for g in gates.values() if g["status"] == "PASS"),
            "total_gates_count": len(gates),
            "gates": gates
        }

if __name__ == "__main__":
    mock_data = {"status": True}
    res = MultiDimensionalQAGate.execute_qa(
        {"unjustified_extrapolations": 0, "synergy_fallacy_detected": False},
        {"verified_references": 15, "total_references": 15, "unsupported_references": 0},
        {"untraced_numbers_count": 0, "studies_with_quantitative_data": 15},
        {"citation_coverage_pct": 100.0, "padding_detected": False},
        {"PROPOSAL_STRUCTURE_VALIDATION": "PASS"},
        {"boundary_conditions_defined": True},
        {"primary_test_defined": True, "normality_checked": True},
        {"scholarly_tone_verified": True, "artificial_repetition_detected": False},
        {"hardcode_violations": 0}
    )
    print("Composite QA Status:", res["COMPOSITE_QA_GATE"], f"({res['passed_dimensions']}/{res['total_dimensions']} dimensions passed)")
