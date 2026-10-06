#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
proposal_readiness_gate.py - Master Pre-Generation Readiness & Integrity Gate
Proposal-Nevisi Engine v9.0

Enforces the non-negotiable architectural requirement:
Zero proposals can be generated unless all 8 core v9.0 scientific, structural,
and typographic modules pass verification.

100% General-Purpose: Zero hardcoded topics.
"""

import sys
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class GateResult:
    can_proceed: bool
    is_ready: bool
    passed_modules: List[str] = field(default_factory=list)
    failed_modules: List[str] = field(default_factory=list)
    error_messages: List[str] = field(default_factory=list)
    module_diagnostics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "can_proceed": self.can_proceed,
            "is_ready": self.is_ready,
            "passed_modules": self.passed_modules,
            "failed_modules": self.failed_modules,
            "error_messages": self.error_messages,
            "module_diagnostics": self.module_diagnostics
        }

class ProposalReadinessGate:
    """Master readiness gate verifying all required v9.0 modules before generation."""

    required_modules = [
        "compound_entity_normalizer",
        "biological_mechanism_adversarial_verifier",
        "combination_hypothesis_engine",
        "combination_model_selector",
        "methodology_completeness_gate",
        "native_omml_math_engine",
        "persian_medical_typography_linter",
        "CitationTracker"
    ]

    @classmethod
    def check_all(cls, proposal_context: Dict[str, Any]) -> GateResult:
        """
        Executes exhaustive readiness inspection across all 8 mandatory modules.
        Stops generation if any module fails or context has scientific/structural defects.
        """
        passed = []
        failed = []
        errors = []
        diagnostics = {}

        # 1. compound_entity_normalizer
        try:
            from compound_entity_normalizer import CompoundEntityNormalizer
            interventions = proposal_context.get("interventions_or_exposures", [])
            norm_results = []
            for agt in interventions:
                norm = CompoundEntityNormalizer.normalize(agt)
                norm_results.append(norm.to_dict())
            diagnostics["compound_entity_normalizer"] = {"status": "PASS", "normalized_agents": norm_results}
            passed.append("compound_entity_normalizer")
        except Exception as e:
            failed.append("compound_entity_normalizer")
            errors.append(f"compound_entity_normalizer failure: {str(e)}")

        # 2. biological_mechanism_adversarial_verifier
        try:
            from biological_mechanism_adversarial_verifier import BiologicalMechanismAdversarialVerifier
            # Scan sample claims or problem statement if present
            claims_to_check = proposal_context.get("biological_claims", [])
            prob_stmt = proposal_context.get("problem_statement_text", "")
            if prob_stmt and not claims_to_check:
                # Extract sentence claims containing key biological keywords
                sentences = [s.strip() for s in prob_stmt.split('.') if len(s.strip()) > 10]
                claims_to_check = sentences[:5]

            mech_contradictions = []
            for clm in claims_to_check:
                chk = BiologicalMechanismAdversarialVerifier.check(clm)
                if chk.status == "CONTRADICTED":
                    mech_contradictions.append(chk.to_dict())

            if mech_contradictions:
                failed.append("biological_mechanism_adversarial_verifier")
                errors.append(f"Biological role inversion detected in {len(mech_contradictions)} claims: {mech_contradictions}")
            else:
                passed.append("biological_mechanism_adversarial_verifier")
                diagnostics["biological_mechanism_adversarial_verifier"] = {"status": "PASS", "contradictions_found": 0}
        except Exception as e:
            failed.append("biological_mechanism_adversarial_verifier")
            errors.append(f"biological_mechanism_adversarial_verifier failure: {str(e)}")

        # 3. combination_hypothesis_engine
        try:
            from combination_hypothesis_engine import CombinationHypothesisEngine
            interventions = proposal_context.get("interventions_or_exposures", [])
            if len(interventions) >= 2:
                a_name = interventions[0].get("name", "Agent-A") if isinstance(interventions[0], dict) else str(interventions[0])
                b_name = interventions[1].get("name", "Agent-B") if isinstance(interventions[1], dict) else str(interventions[1])
                hyp_analysis = CombinationHypothesisEngine.analyze(
                    entity_a=a_name,
                    entity_b=b_name,
                    target=proposal_context.get("target_condition", {}).get("name_en", "Target System"),
                    retrieved_evidence=proposal_context.get("studies", [])
                )
                diagnostics["combination_hypothesis_engine"] = {
                    "status": "PASS",
                    "balance_score": hyp_analysis.evidence_balance_score,
                    "framing": hyp_analysis.recommended_framing,
                    "warnings": hyp_analysis.bias_warnings
                }
            else:
                diagnostics["combination_hypothesis_engine"] = {"status": "PASS", "note": "Monotherapy or single exposure"}
            passed.append("combination_hypothesis_engine")
        except Exception as e:
            failed.append("combination_hypothesis_engine")
            errors.append(f"combination_hypothesis_engine failure: {str(e)}")

        # 4. combination_model_selector
        try:
            from combination_model_selector import CombinationModelSelector
            stat_res = CombinationModelSelector.select(
                study_design=proposal_context.get("framework", "in_vitro"),
                outcome_type="continuous",
                groups_count=4 if len(proposal_context.get("interventions_or_exposures", [])) >= 2 else 2
            )
            diagnostics["combination_model_selector"] = {"status": "PASS", "selected_model": stat_res.primary_model}
            passed.append("combination_model_selector")
        except Exception as e:
            failed.append("combination_model_selector")
            errors.append(f"combination_model_selector failure: {str(e)}")

        # 5. methodology_completeness_gate
        try:
            from methodology_completeness_gate import MethodologyCompletenessGate
            # If proposal text or 28 sections provided, validate completeness
            if "proposal_markdown" in proposal_context:
                gate_chk = MethodologyCompletenessGate.validate(proposal_context["proposal_markdown"])
                if not gate_chk.can_proceed:
                    failed.append("methodology_completeness_gate")
                    errors.append(f"Pajooheshyar completeness failed. Missing: {gate_chk.missing_sections}, Needing Formula: {gate_chk.sections_needing_formula}")
                else:
                    passed.append("methodology_completeness_gate")
                    diagnostics["methodology_completeness_gate"] = {"status": "PASS", "score": gate_chk.compliance_score}
            elif "sections_dict" in proposal_context:
                gate_chk = MethodologyCompletenessGate.validate(proposal_context["sections_dict"])
                if not gate_chk.can_proceed:
                    failed.append("methodology_completeness_gate")
                    errors.append(f"Pajooheshyar completeness failed. Missing: {gate_chk.missing_sections}, Needing Formula: {gate_chk.sections_needing_formula}")
                else:
                    passed.append("methodology_completeness_gate")
                    diagnostics["methodology_completeness_gate"] = {"status": "PASS", "score": gate_chk.compliance_score}
            else:
                # Pre-generation check: ensure module is loaded and operational
                passed.append("methodology_completeness_gate")
                diagnostics["methodology_completeness_gate"] = {"status": "PASS", "stage": "PRE_GENERATION_READY"}
        except Exception as e:
            failed.append("methodology_completeness_gate")
            errors.append(f"methodology_completeness_gate failure: {str(e)}")

        # 6. native_omml_math_engine
        try:
            from native_omml_math_engine import NativeOmmlMathEngine
            test_omml = NativeOmmlMathEngine.convert_latex_to_omml(r"\frac{a}{b}")
            test_uni = NativeOmmlMathEngine.convert_latex_to_unicode(r"\alpha \pm \beta")
            if not test_omml or not test_uni:
                raise ValueError("OMML engine returned empty output on standard test expression")
            diagnostics["native_omml_math_engine"] = {"status": "PASS", "unicode_sample": test_uni}
            passed.append("native_omml_math_engine")
        except Exception as e:
            failed.append("native_omml_math_engine")
            errors.append(f"native_omml_math_engine failure: {str(e)}")

        # 7. persian_medical_typography_linter
        try:
            from persian_medical_typography_linter import PersianMedicalTypographyLinter
            linter = PersianMedicalTypographyLinter()
            test_lint = linter.format_text("می شود")
            if "می‌شود" not in test_lint:
                raise ValueError("Persian typography linter failed to apply standard ZWNJ")
            diagnostics["persian_medical_typography_linter"] = {"status": "PASS"}
            passed.append("persian_medical_typography_linter")
        except Exception as e:
            failed.append("persian_medical_typography_linter")
            errors.append(f"persian_medical_typography_linter failure: {str(e)}")

        # 8. CitationTracker
        try:
            from citation_tracker import CitationTracker
            tracker = CitationTracker()
            # If context includes claims and references, validate them
            studies = proposal_context.get("studies", [])
            for s in studies:
                cid = s.get("citation_id") or s.get("pmid") or s.get("ref_id") or str(s.get("citation_number", ""))
                if cid:
                    tracker.register_reference(str(cid), s)

            claims = proposal_context.get("claims", [])
            for c in claims:
                txt = c.get("text", "")
                cid = c.get("citation_id", "")
                tracker.register_claim(txt, cid)

            if claims or studies:
                val = tracker.validate()
                if not val.is_valid:
                    failed.append("CitationTracker")
                    errors.extend(val.error_messages)
                else:
                    passed.append("CitationTracker")
                    diagnostics["CitationTracker"] = {"status": "PASS", "ordered_refs": len(val.ordered_citation_ids)}
            else:
                passed.append("CitationTracker")
                diagnostics["CitationTracker"] = {"status": "PASS", "stage": "INITIALIZED"}
        except Exception as e:
            failed.append("CitationTracker")
            errors.append(f"CitationTracker failure: {str(e)}")

        can_proceed = (len(failed) == 0 and len(passed) == len(cls.required_modules))

        return GateResult(
            can_proceed=can_proceed,
            is_ready=can_proceed,
            passed_modules=passed,
            failed_modules=failed,
            error_messages=errors,
            module_diagnostics=diagnostics
        )

proposal_readiness_gate = ProposalReadinessGate
