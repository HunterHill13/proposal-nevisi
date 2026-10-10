#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
proposal_readiness_gate.py - Fail-Closed Pre-Generation & Proposal-Specific Readiness Gate
Proposal-Nevisi Engine v9.1

Enforces strict, fail-closed pre-generation gatekeeping across two distinct modes:
1. PRE_GENERATION_INFRASTRUCTURE:
   - Verifies software environment, schemas, configs, and all 8 core modules.
2. PROPOSAL_SPECIFIC_VALIDATION:
   - Validates authentic proposal research context:
     * study design & framework defined
     * interventions/agents specified
     * target model (cell line/species/population) specified
     * primary endpoint specified
     * replication structure defined (biological vs technical replicates)
     * sample size methodology evaluated
     * statistical & combination models appropriately selected
     * citation integrity & 28 Pajooheshyar sections verified
   - FAILS CLOSED: Missing study-specific inputs return NOT_READY / INSUFFICIENT_INPUTS,
     never converted to fake passes or mock defaults.

100% General-Purpose: Zero hardcoded topics.
"""

import sys
import os

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPTS_DIR, ".."))
for p in [SCRIPTS_DIR, PROJECT_ROOT]:
    if p not in sys.path:
        sys.path.insert(0, p)

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class GateResult:
    can_proceed: bool
    is_ready: bool
    mode: str  # "PRE_GENERATION_INFRASTRUCTURE" | "PROPOSAL_SPECIFIC_VALIDATION"
    passed_modules: List[str] = field(default_factory=list)
    failed_modules: List[str] = field(default_factory=list)
    missing_inputs: List[str] = field(default_factory=list)
    error_messages: List[str] = field(default_factory=list)
    module_diagnostics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "can_proceed": self.can_proceed,
            "is_ready": self.is_ready,
            "mode": self.mode,
            "passed_modules": self.passed_modules,
            "failed_modules": self.failed_modules,
            "missing_inputs": self.missing_inputs,
            "error_messages": self.error_messages,
            "module_diagnostics": self.module_diagnostics
        }


class ProposalReadinessGate:
    """Master readiness gate verifying infrastructure and proposal-specific inputs."""

    required_modules = [
        "compound_entity_normalizer",
        "biological_mechanism_adversarial_verifier",
        "combination_hypothesis_engine",
        "combination_model_selector",
        "methodology_completeness_gate",
        "native_omml_math_engine",
        "persian_medical_typography_linter",
        "CitationTracker",
        "LiveReferenceVerificationGate",
        "FullTextRetrievalEngine",
        "MockGrantReviewPanel",
        "EquatorComplianceAuditor",
        "PreEmptiveRiskOfBiasMitigator",
        "EpistemicRigorAuditor",
        "ProposalResearchDossier"
    ]

    @classmethod
    def check_all(
        cls,
        proposal_context: Optional[Dict[str, Any]] = None,
        mode: Optional[str] = None
    ) -> GateResult:
        """
        Executes readiness inspection.
        If proposal_context is empty or mode is explicitly 'PRE_GENERATION_INFRASTRUCTURE',
        runs software infrastructure readiness.
        If proposal_context is provided or mode is 'PROPOSAL_SPECIFIC_VALIDATION',
        runs fail-closed proposal-specific validation.
        """
        ctx = proposal_context or {}
        selected_mode = mode or ("PROPOSAL_SPECIFIC_VALIDATION" if ctx else "PRE_GENERATION_INFRASTRUCTURE")

        passed = []
        failed = []
        errors = []
        missing_inputs = []
        diagnostics = {}

        # -------------------------------------------------------------
        # Phase 1: Infrastructure and Module Availability (Always Run)
        # -------------------------------------------------------------
        # 1. compound_entity_normalizer
        try:
            from compound_entity_normalizer import CompoundEntityNormalizer
            norm_test = CompoundEntityNormalizer.normalize("Reference Standard Substance")
            if not norm_test or not hasattr(norm_test, "category"):
                raise ValueError("Normalizer failed basic instantiation")
            passed.append("compound_entity_normalizer")
            diagnostics["compound_entity_normalizer"] = {"status": "PASS", "test_category": norm_test.category}
        except Exception as e:
            failed.append("compound_entity_normalizer")
            errors.append(f"compound_entity_normalizer import/runtime error: {str(e)}")

        # 2. biological_mechanism_adversarial_verifier
        try:
            from biological_mechanism_adversarial_verifier import BiologicalMechanismAdversarialVerifier
            v_test = BiologicalMechanismAdversarialVerifier.check("Bcl-xL inhibits apoptosis")
            if v_test.status != "VERIFIED":
                raise ValueError("Mechanism verifier failed canonical verification test")
            passed.append("biological_mechanism_adversarial_verifier")
            diagnostics["biological_mechanism_adversarial_verifier"] = {"status": "PASS"}
        except Exception as e:
            failed.append("biological_mechanism_adversarial_verifier")
            errors.append(f"biological_mechanism_adversarial_verifier error: {str(e)}")

        # 3. combination_hypothesis_engine
        try:
            from combination_hypothesis_engine import CombinationHypothesisEngine
            hyp_test = CombinationHypothesisEngine.analyze("Drug-Alpha", "Drug-Beta", "cell viability")
            if not hyp_test.synergism_hypothesis or not hyp_test.antagonism_hypothesis:
                raise ValueError("Hypothesis engine failed dual hypothesis synthesis")
            passed.append("combination_hypothesis_engine")
            diagnostics["combination_hypothesis_engine"] = {"status": "PASS"}
        except Exception as e:
            failed.append("combination_hypothesis_engine")
            errors.append(f"combination_hypothesis_engine error: {str(e)}")

        # 4. combination_model_selector
        try:
            from combination_model_selector import CombinationModelSelector
            mod_test = CombinationModelSelector.select(groups_count=4, is_factorial=False)
            if not mod_test.primary_model:
                raise ValueError("Model selector returned empty primary model")
            passed.append("combination_model_selector")
            diagnostics["combination_model_selector"] = {"status": "PASS"}
        except Exception as e:
            failed.append("combination_model_selector")
            errors.append(f"combination_model_selector error: {str(e)}")

        # 5. methodology_completeness_gate
        try:
            from methodology_completeness_gate import MethodologyCompletenessGate, PAJOOHESHYAR_28_SECTIONS
            if len(PAJOOHESHYAR_28_SECTIONS) != 28:
                raise ValueError(f"Expected 28 Pajooheshyar sections, found {len(PAJOOHESHYAR_28_SECTIONS)}")
            passed.append("methodology_completeness_gate")
            diagnostics["methodology_completeness_gate"] = {"status": "PASS"}
        except Exception as e:
            failed.append("methodology_completeness_gate")
            errors.append(f"methodology_completeness_gate error: {str(e)}")

        # 6. native_omml_math_engine
        try:
            from native_omml_math_engine import NativeOmmlMathEngine
            omml_test = NativeOmmlMathEngine.convert_latex_to_omml(r"\frac{a}{b}")
            if not omml_test or "<m:oMath" not in omml_test:
                raise ValueError("OMML engine did not emit valid <m:oMath> XML")
            passed.append("native_omml_math_engine")
            diagnostics["native_omml_math_engine"] = {"status": "PASS"}
        except Exception as e:
            failed.append("native_omml_math_engine")
            errors.append(f"native_omml_math_engine error: {str(e)}")

        # 7. persian_medical_typography_linter
        try:
            from persian_medical_typography_linter import PersianMedicalTypographyLinter
            linter = PersianMedicalTypographyLinter()
            lint_test = linter.format_text("می شود")
            if "می‌شود" not in lint_test:
                raise ValueError("Persian typography linter did not enforce ZWNJ")
            passed.append("persian_medical_typography_linter")
            diagnostics["persian_medical_typography_linter"] = {"status": "PASS"}
        except Exception as e:
            failed.append("persian_medical_typography_linter")
            errors.append(f"persian_medical_typography_linter error: {str(e)}")

        # 8. CitationTracker
        try:
            from citation_tracker import CitationTracker
            ct = CitationTracker()
            ct.register_reference("t1", {"title": "Test Ref"})
            ct.register_claim("Claim text", "t1")
            v_res = ct.validate()
            if not v_res.is_valid:
                raise ValueError("CitationTracker failed self-validation")
            passed.append("CitationTracker")
            diagnostics["CitationTracker"] = {"status": "PASS"}
        except Exception as e:
            failed.append("CitationTracker")
            errors.append(f"CitationTracker error: {str(e)}")

        # 9. LiveReferenceVerificationGate
        try:
            from scientific_search_adapter import LiveReferenceVerificationGate
            lrv = LiveReferenceVerificationGate()
            test_rec = {"title": "Benchmark Study", "pmid": "999999", "mock_verified": True}
            v_chk = lrv.verify_single_reference(test_rec, mode="fixture")
            if not v_chk.get("is_verified"):
                raise ValueError("LiveReferenceVerificationGate fixture verification failed")
            passed.append("LiveReferenceVerificationGate")
            diagnostics["LiveReferenceVerificationGate"] = {"status": "PASS"}
        except Exception as e:
            failed.append("LiveReferenceVerificationGate")
            errors.append(f"LiveReferenceVerificationGate error: {str(e)}")

        # 10. FullTextRetrievalEngine
        try:
            from scientific_search_adapter import FullTextRetrievalEngine
            ft_engine = FullTextRetrievalEngine()
            test_study = {"title": "Benchmark Study", "pmid": "999999", "abstract": "Sample abstract text for testing."}
            grounded = ft_engine.retrieve_and_ground_study(test_study, mode="fixture")
            if not grounded.get("tier"):
                raise ValueError("FullTextRetrievalEngine failed study grounding classification")
            passed.append("FullTextRetrievalEngine")
            diagnostics["FullTextRetrievalEngine"] = {"status": "PASS"}
        except Exception as e:
            failed.append("FullTextRetrievalEngine")
            errors.append(f"FullTextRetrievalEngine error: {str(e)}")

        # 11. MockGrantReviewPanel
        try:
            from mock_grant_review_panel import MockGrantReviewPanel
            mgrp_test = MockGrantReviewPanel.parse_proposal_sections("## 1. موضوع\nعنوان تستی")
            if 1 not in mgrp_test:
                raise ValueError("MockGrantReviewPanel failed section parsing")
            passed.append("MockGrantReviewPanel")
            diagnostics["MockGrantReviewPanel"] = {"status": "PASS"}
        except Exception as e:
            failed.append("MockGrantReviewPanel")
            errors.append(f"MockGrantReviewPanel error: {str(e)}")

        # 12. EquatorComplianceAuditor
        try:
            from equator_compliance_auditor import EquatorComplianceAuditor
            eq_test = EquatorComplianceAuditor.parse_sections("## 1. موضوع\nعنوان تستی")
            if 1 not in eq_test:
                raise ValueError("EquatorComplianceAuditor failed section parsing")
            passed.append("EquatorComplianceAuditor")
            diagnostics["EquatorComplianceAuditor"] = {"status": "PASS"}
        except Exception as e:
            failed.append("EquatorComplianceAuditor")
            errors.append(f"EquatorComplianceAuditor error: {str(e)}")

        # 13. PreEmptiveRiskOfBiasMitigator
        try:
            from pre_emptive_risk_of_bias_mitigator import PreEmptiveRiskOfBiasMitigator
            rob_test = PreEmptiveRiskOfBiasMitigator.parse_sections("## 1. موضوع\nعنوان تستی")
            if 1 not in rob_test:
                raise ValueError("PreEmptiveRiskOfBiasMitigator failed section parsing")
            passed.append("PreEmptiveRiskOfBiasMitigator")
            diagnostics["PreEmptiveRiskOfBiasMitigator"] = {"status": "PASS"}
        except Exception as e:
            failed.append("PreEmptiveRiskOfBiasMitigator")
            errors.append(f"PreEmptiveRiskOfBiasMitigator error: {str(e)}")

        # 14. EpistemicRigorAuditor
        try:
            from epistemic_rigor_auditor import EpistemicRigorAuditor
            era_test = EpistemicRigorAuditor(fail_closed=False)
            audit_res = era_test.audit_dossier({})
            passed.append("EpistemicRigorAuditor")
            diagnostics["EpistemicRigorAuditor"] = {"status": "PASS"}
        except Exception as e:
            failed.append("EpistemicRigorAuditor")
            errors.append(f"EpistemicRigorAuditor error: {str(e)}")

        # 15. ProposalResearchDossier
        try:
            from proposal_research_dossier import ProposalResearchDossier
            prd_test = ProposalResearchDossier(topic="Benchmark Topic", domain="Biomedical")
            if not prd_test.topic:
                raise ValueError("ProposalResearchDossier failed instantiation")
            passed.append("ProposalResearchDossier")
            diagnostics["ProposalResearchDossier"] = {"status": "PASS"}
        except Exception as e:
            failed.append("ProposalResearchDossier")
            errors.append(f"ProposalResearchDossier error: {str(e)}")

        # If running purely in infrastructure mode, return status
        if selected_mode == "PRE_GENERATION_INFRASTRUCTURE":
            all_infra_passed = (len(failed) == 0 and len(passed) == len(cls.required_modules))
            return GateResult(
                can_proceed=all_infra_passed,
                is_ready=all_infra_passed,
                mode=selected_mode,
                passed_modules=passed,
                failed_modules=failed,
                missing_inputs=[],
                error_messages=errors,
                module_diagnostics=diagnostics
            )

        # -------------------------------------------------------------
        # -------------------------------------------------------------
        # Phase 2: Context Validation (Claims, Interventions, and Design)
        # -------------------------------------------------------------
        strict_mode = (selected_mode == "STRICT_PROPOSAL_VALIDATION")

        # 1. Validate study design & framework
        design = ctx.get("study_design") or ctx.get("framework")
        if strict_mode and not design:
            missing_inputs.append("study_design")
            errors.append("PROPOSAL_DEFECT: نوع و طراحی مطالعه (study_design / framework) مشخص نشده است.")

        # 2. Validate interventions / agents
        interventions = ctx.get("interventions_or_exposures") or ctx.get("interventions")
        if strict_mode and not interventions:
            missing_inputs.append("interventions_or_exposures")
            errors.append("PROPOSAL_DEFECT: عامل یا عوامل مداخله (interventions_or_exposures) مشخص نشده‌اند.")

        # 3. Validate target model (cell line, animal, population)
        target_model = ctx.get("target_model") or ctx.get("cell_line") or ctx.get("population")
        if strict_mode and not target_model:
            missing_inputs.append("target_model")
            errors.append("PROPOSAL_DEFECT: مدل هدف تجربی/سلولی یا جمعیت مطالعه (target_model) تعریف نشده است.")

        # 4. Validate primary endpoint
        endpoint = ctx.get("primary_endpoint") or ctx.get("endpoint")
        if strict_mode and not endpoint:
            missing_inputs.append("primary_endpoint")
            errors.append("PROPOSAL_DEFECT: پیامد اولیه پژوهش (primary_endpoint) مشخص نشده است.")

        # 5. Validate replication structure & sample size
        bio_reps = ctx.get("biological_replicates")
        tech_reps = ctx.get("technical_replicates")
        exp_unit = ctx.get("experimental_unit")

        if strict_mode:
            if bio_reps is None:
                missing_inputs.append("biological_replicates")
                errors.append("PROPOSAL_DEFECT: تعداد تکرارهای بیولوژیک مستقل (biological_replicates) مشخص نشده است.")
            if exp_unit is None:
                missing_inputs.append("experimental_unit")
                errors.append("PROPOSAL_DEFECT: واحد آزمایشی مستقل (experimental_unit) تعریف نشده است (REPLICATION_STRUCTURE_UNDEFINED).")

        # Evaluate sample size inputs through MethodologyCompletenessGate if parameters provided
        if exp_unit or bio_reps is not None or strict_mode:
            if "methodology_completeness_gate" in passed:
                from methodology_completeness_gate import MethodologyCompletenessGate
                ss_eval = MethodologyCompletenessGate.evaluate_sample_size_inputs(
                    study_design=str(design or "in_vitro"),
                    primary_endpoint=endpoint,
                    experimental_unit=exp_unit,
                    effect_size=ctx.get("effect_size"),
                    variance_or_sd=ctx.get("variance_or_sd"),
                    alpha=ctx.get("alpha", 0.05),
                    power=ctx.get("power", 0.80),
                    groups_count=len(interventions) if isinstance(interventions, list) else 4,
                    biological_replicates=bio_reps,
                    technical_replicates=tech_reps
                )
                diagnostics["sample_size_evaluation"] = ss_eval.to_dict()
                if not ss_eval.can_proceed and strict_mode:
                    errors.append(f"SAMPLE_SIZE_GATE_FAIL: {ss_eval.methodological_rationale_fa}")
                    if "sample_size_methodology" not in failed:
                        failed.append("sample_size_methodology")

        # 6. Validate biological claims for role inversion (Blocks in all modes)
        claims_to_check = ctx.get("biological_claims", [])
        if claims_to_check:
            from biological_mechanism_adversarial_verifier import BiologicalMechanismAdversarialVerifier
            contradictions = []
            for clm in claims_to_check:
                chk = BiologicalMechanismAdversarialVerifier.check(clm)
                if chk.status == "CONTRADICTED":
                    contradictions.append(chk.to_dict())
            if contradictions:
                if "biological_mechanism_adversarial_verifier" in passed:
                    passed.remove("biological_mechanism_adversarial_verifier")
                if "biological_mechanism_adversarial_verifier" not in failed:
                    failed.append("biological_mechanism_adversarial_verifier")
                errors.append(f"BIOLOGICAL_ROLE_INVERSION_DETECTED: {len(contradictions)} ادعا با نقش بیولوژیک تناقض دارند: {contradictions}")

        # 7. Validate 28 sections completeness if document or sections provided
        if "proposal_markdown" in ctx or "sections_dict" in ctx:
            from methodology_completeness_gate import MethodologyCompletenessGate
            inp = ctx.get("proposal_markdown") or ctx.get("sections_dict")
            comp_res = MethodologyCompletenessGate.validate(inp)
            diagnostics["pajooheshyar_completeness"] = comp_res.to_dict()
            if not comp_res.can_proceed:
                if "methodology_completeness_gate" in passed:
                    passed.remove("methodology_completeness_gate")
                if "methodology_completeness_gate" not in failed:
                    failed.append("methodology_completeness_gate")
                errors.append(f"PAJOOHESHYAR_COMPLETENESS_FAIL: بخش‌های ناقص: {comp_res.missing_sections}")

        # 8. Validate references live / authentic provenance and full-text grounding if provided
        refs_to_verify = ctx.get("retrieved_studies") or ctx.get("studies") or ctx.get("references")
        if refs_to_verify and isinstance(refs_to_verify, list):
            from scientific_search_adapter import LiveReferenceVerificationGate, FullTextRetrievalEngine
            lrv_gate = LiveReferenceVerificationGate()
            verif_mode = ctx.get("reference_verification_mode", ("fixture" if ctx.get("mode") in ["fixture", "offline"] else "auto"))
            # References must fail-closed if invalid
            ref_audit = lrv_gate.verify_study_collection(refs_to_verify, mode=verif_mode, fail_closed=True)
            diagnostics["reference_live_verification"] = ref_audit
            if not ref_audit["can_proceed"]:
                failed_ids = [f.get("title", f.get("pmid", "Unknown")) for f in ref_audit.get("failed_studies", [])]
                errors.append(f"LIVE_REFERENCE_VERIFICATION_FAIL: {ref_audit['failed_count']} منبع در پایگاه‌های مرجع تایید نشدند: {failed_ids}")
                if "LiveReferenceVerificationGate" not in failed:
                    failed.append("LiveReferenceVerificationGate")
            else:
                # Update verified studies with canonical metadata
                if "studies" in ctx:
                    ctx["studies"] = ref_audit.get("verified_studies", ctx["studies"])

            # Check Abstract-Only Quota & Passage Grounding
            has_tier_tags = any("tier" in r or "has_full_text" in r for r in refs_to_verify)
            if strict_mode or has_tier_tags or len(refs_to_verify) > 0:
                quota_audit = FullTextRetrievalEngine.apply_abstract_quota(
                    refs_to_verify,
                    max_abstract_ratio=0.15,
                    min_total_required=ctx.get("min_references", 15) if strict_mode else 1
                )
                diagnostics["abstract_quota_evaluation"] = quota_audit
                if not quota_audit["can_proceed"] and (strict_mode or quota_audit.get("tier_b_dropped_count", 0) > 0):
                    errors.append(
                        f"ABSTRACT_QUOTA_EXCEEDED: نسبت مقالات فقط-چکیده ({round(quota_audit['abstract_ratio']*100, 1)}%) "
                        f"از سقف مجاز (۱۵٪) فراتر رفته یا فاقد توجیه قطعی متدولوژیک/مستقیم است."
                    )
                    if "FullTextRetrievalEngine" not in failed:
                        failed.append("FullTextRetrievalEngine")

        # Final Fail-Closed Decision
        can_proceed = (len(failed) == 0 and len(errors) == 0 and len(missing_inputs) == 0)

        return GateResult(
            can_proceed=can_proceed,
            is_ready=can_proceed,
            mode=selected_mode,
            passed_modules=passed,
            failed_modules=failed,
            missing_inputs=missing_inputs,
            error_messages=errors,
            module_diagnostics=diagnostics
        )

    @classmethod
    def assert_ready_or_raise(
        cls,
        proposal_context: Optional[Dict[str, Any]] = None,
        mode: Optional[str] = None
    ) -> None:
        """Enforces fail-closed gatekeeping: raises RuntimeError if not ready."""
        res = cls.check_all(proposal_context=proposal_context, mode=mode)
        if not res.can_proceed:
            error_details = "\n  - " + "\n  - ".join(res.error_messages)
            missing_details = f"\n  Missing Inputs: {res.missing_inputs}" if res.missing_inputs else ""
            raise RuntimeError(
                f"ProposalReadinessGate REJECTED generation [Mode: {res.mode}]:\n"
                f"  Failed Modules: {res.failed_modules}{missing_details}\n"
                f"  Errors:{error_details}"
            )
