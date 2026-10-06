#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_v90_adversarial.py - Adversarial Stress Test Suite for Proposal-Nevisi v9.0
Verifies that newly introduced v9.0 modules correctly detect and reject
scientific inversions, bias, missing methodology sections, and citation orphans.

100% General-Purpose: Adheres strictly to the v9.0 Ground Rules.
"""

import os
import sys
import unittest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.abspath(os.path.join(TESTS_DIR, "..", "scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from compound_entity_normalizer import CompoundEntityNormalizer
from citation_tracker import CitationTracker
from methodology_completeness_gate import MethodologyCompletenessGate, REQUIRED_SECTIONS_28
from biological_mechanism_adversarial_verifier import BiologicalMechanismAdversarialVerifier
from combination_hypothesis_engine import CombinationHypothesisEngine
from combination_model_selector import CombinationModelSelector
from native_omml_math_engine import NativeOmmlMathEngine
from persian_medical_typography_linter import PersianMedicalTypographyLinter
from proposal_readiness_gate import ProposalReadinessGate

class TestV90AdversarialSuite(unittest.TestCase):
    """Adversarial stress testing across all 8 v9.0 modules and the master readiness gate."""

    # -------------------------------------------------------------------------
    # 1. Biological Mechanism Adversarial Verifier
    # -------------------------------------------------------------------------
    def test_adv_01_biological_mechanism_inversion_detected(self):
        """Adversarial Test 1: Inverted biological role (Bcl-xL induces apoptosis) -> CONTRADICTED."""
        inverted_claim = "Bcl-xL induces apoptosis by activating downstream executioner caspases."
        result = BiologicalMechanismAdversarialVerifier.check(inverted_claim, context_section="بیان مسئله")

        self.assertEqual(result.status, "CONTRADICTED")
        self.assertIsNotNone(result.correction)
        self.assertIn("anti-apoptotic", result.correction.lower())
        self.assertGreater(result.confidence, 0.90)

    def test_adv_01b_biological_mechanism_correct_and_unverified(self):
        """Adversarial Test 1b: Correct role -> VERIFIED; unknown entity -> UNVERIFIED."""
        correct_claim = "Bax triggers apoptosis via mitochondrial outer membrane permeabilization."
        res_correct = BiologicalMechanismAdversarialVerifier.check(correct_claim)
        self.assertEqual(res_correct.status, "VERIFIED")

        unknown_claim = "HypotheticalFactorX induces cellular senescence."
        res_unknown = BiologicalMechanismAdversarialVerifier.check(unknown_claim)
        self.assertEqual(res_unknown.status, "UNVERIFIED")

    # -------------------------------------------------------------------------
    # 2. Combination Hypothesis Engine (Positive-Evidence Bias)
    # -------------------------------------------------------------------------
    def test_adv_02_positive_evidence_bias_warning_emitted(self):
        """Adversarial Test 2: Input with only positive evidence -> POSITIVE_EVIDENCE_DOMINANCE_WARNING."""
        only_positive_evidence = [
            {"title": "Marked synergism of Agent-A and Agent-B in cell viability reduction", "abstract": "CI was 0.45."},
            {"title": "Co-treatment potentiates apoptosis supra-additively", "abstract": "Combination index confirmed synergy."}
        ]

        analysis = CombinationHypothesisEngine.analyze(
            entity_a="Agent-Alpha",
            entity_b="Agent-Beta",
            target="cellular viability",
            retrieved_evidence=only_positive_evidence
        )

        self.assertEqual(analysis.evidence_balance_score, 1.0)
        self.assertEqual(analysis.recommended_framing, "synergism")
        # Must issue positive dominance / publication bias warning
        self.assertTrue(any("POSITIVE_EVIDENCE_DOMINANCE_WARNING" in w for w in analysis.bias_warnings))
        # Must still formulate the parallel antagonism hypothesis
        self.assertIn("آنتاگونیستی", analysis.antagonism_hypothesis)

    def test_adv_02b_combination_hypothesis_balanced_evidence(self):
        """Adversarial Test 2b: Mixed evidence -> NEUTRAL framing with both hypotheses balanced."""
        mixed_evidence = [
            {"title": "Synergistic cytotoxicity of combination", "abstract": "CI < 0.8."},
            {"title": "Antagonistic competitive interaction observed", "abstract": "CI > 1.3 antagonistic inhibition."}
        ]
        analysis = CombinationHypothesisEngine.analyze(
            entity_a="Agent-Alpha",
            entity_b="Agent-Beta",
            target="cellular viability",
            retrieved_evidence=mixed_evidence
        )
        self.assertEqual(analysis.recommended_framing, "neutral")
        self.assertEqual(analysis.evidence_balance_score, 0.5)

    # -------------------------------------------------------------------------
    # 3. Compound Entity Normalizer
    # -------------------------------------------------------------------------
    def test_adv_03_crude_extract_normalization_and_warnings(self):
        """Adversarial Test 3: Methanolic plant extract -> CRUDE_EXTRACT with attribution warnings."""
        raw_entity = "عصاره متانولی برگ Ficus carica"
        norm = CompoundEntityNormalizer.normalize(raw_entity)

        self.assertEqual(norm.category, "CRUDE_EXTRACT")
        self.assertTrue(norm.is_mixture)
        self.assertFalse(norm.is_pure)
        self.assertEqual(norm.dosage_unit_recommendation, "mass_concentration_ug_ml")
        self.assertTrue(any("CRUDE_EXTRACT_ATTRIBUTION_FALLACY" in w for w in norm.methodological_warnings))

    def test_adv_03b_pure_compound_and_derivative_normalization(self):
        """Adversarial Test 3b: Pure substance (>=98%) and synthetic analog."""
        pure_entity = "Compound-Z (Analytical standard >=99% purity)"
        norm_pure = CompoundEntityNormalizer.normalize(pure_entity)
        self.assertEqual(norm_pure.category, "PURE_COMPOUND")
        self.assertTrue(norm_pure.is_pure)

        analog_entity = "Compound-Z methyl ester derivative"
        norm_analog = CompoundEntityNormalizer.normalize(analog_entity)
        self.assertEqual(norm_analog.category, "SYNTHETIC_ANALOG")
        self.assertTrue(any("SYNTHETIC_DERIVATIVE" in w for w in norm_analog.methodological_warnings))

    # -------------------------------------------------------------------------
    # 4. Methodology Completeness Gate (Pajooheshyar 28 Sections)
    # -------------------------------------------------------------------------
    def test_adv_04_missing_sample_size_formula_blocks_generation(self):
        """Adversarial Test 4: Proposal without mathematical sample size formula -> CANNOT PROCEED."""
        # Proposal with all sections present, but sample size section lacks formula
        incomplete_proposal = {sec: f"محتوای استاندارد برای {sec}" for sec in REQUIRED_SECTIONS_28}
        # Incomplete sample size: just plain text without formula
        incomplete_proposal["حجم نمونه و روش محاسبه آن"] = "حجم نمونه در این مطالعه برابر با ۳۰ نمونه تعیین گردید."

        res = MethodologyCompletenessGate.validate(incomplete_proposal)
        self.assertFalse(res.can_proceed)
        self.assertFalse(res.is_complete)
        self.assertIn("حجم نمونه و روش محاسبه آن", res.sections_needing_formula)

    def test_adv_04b_full_compliance_with_cohen_formula_passes(self):
        """Adversarial Test 4b: Complete proposal with Cohen/Mead formula -> CAN PROCEED."""
        complete_proposal = {sec: f"محتوای تفصیلی برای {sec}" for sec in REQUIRED_SECTIONS_28}
        complete_proposal["حجم نمونه و روش محاسبه آن"] = (
            r"محاسبه بر مبنای فرمول کوهن: $n = \frac{2(Z_{1-\alpha/2} + Z_{1-\beta})^2 \cdot \sigma^2}{d^2}$ "
            "با توان آزمون ۸۰٪ و سطح خطای ۵٪ انجام پذیرفت."
        )

        res = MethodologyCompletenessGate.validate(complete_proposal)
        self.assertTrue(res.can_proceed)
        self.assertTrue(res.is_complete)
        self.assertEqual(len(res.missing_sections), 0)
        self.assertEqual(len(res.sections_needing_formula), 0)

    # -------------------------------------------------------------------------
    # 5. Native OMML Math Engine
    # -------------------------------------------------------------------------
    def test_adv_05_complex_latex_converted_without_raw_leakage(self):
        """Adversarial Test 5: Complex LaTeX expression converts to OMML and clean Unicode."""
        complex_latex = r"$\frac{\hat{p}_1-\hat{p}_2}{\sqrt{\bar{p}(1-\bar{p})(\frac{1}{n_1}+\frac{1}{n_2})}}$"
        
        # Test Unicode conversion
        unicode_result = NativeOmmlMathEngine.convert_latex_to_unicode(complex_latex)
        self.assertNotIn(r"\frac", unicode_result)
        self.assertNotIn(r"\sqrt", unicode_result)
        self.assertNotIn("$", unicode_result)
        self.assertIn("√", unicode_result)

        # Test OMML XML generation
        omml_xml = NativeOmmlMathEngine.convert_latex_to_omml(complex_latex)
        self.assertIn("m:oMath", omml_xml)
        self.assertIn("m:f", omml_xml)
        self.assertIn("m:rad", omml_xml)

    # -------------------------------------------------------------------------
    # 6. CitationTracker (Integrity & Orphan Detection)
    # -------------------------------------------------------------------------
    def test_adv_06_orphaned_claims_and_unused_references_flagged(self):
        """Adversarial Test 6: Unlinked claim and uncited reference fail validation."""
        tracker = CitationTracker()
        tracker.register_reference("REF_01", {"title": "Study on Primary Agent", "year": 2024})
        tracker.register_reference("REF_02_UNUSED", {"title": "Unused Reference Study", "year": 2023})

        # Register claim with valid citation
        tracker.register_claim("Agent-Alpha reduces cell viability by 50% [1].", "REF_01")
        # Register claim without citation (Orphan)
        tracker.register_claim("The combination exhibits dramatic unproven synergy.", None)

        val = tracker.validate()
        self.assertFalse(val.is_valid)
        self.assertEqual(val.orphaned_claims_count, 1)
        self.assertEqual(val.unused_references_count, 1)
        self.assertIn("REF_02_UNUSED", val.unused_references)

    def test_adv_06b_vancouver_order_of_appearance_enforced(self):
        """Adversarial Test 6b: References re-indexed strictly by order of appearance."""
        tracker = CitationTracker()
        tracker.register_reference("REF_LATE", {"title": "Second Cited Study"})
        tracker.register_reference("REF_EARLY", {"title": "First Cited Study"})

        # Cite REF_EARLY first, then REF_LATE
        tracker.register_claim("First claim citing early paper.", "REF_EARLY")
        tracker.register_claim("Second claim citing late paper.", "REF_LATE")

        ordered = tracker.get_ordered_references()
        self.assertEqual(len(ordered), 2)
        self.assertEqual(ordered[0]["citation_id"], "REF_EARLY")
        self.assertEqual(ordered[0]["citation_number"], 1)
        self.assertEqual(ordered[1]["citation_id"], "REF_LATE")
        self.assertEqual(ordered[1]["citation_number"], 2)

    # -------------------------------------------------------------------------
    # 7. Combination Model Selector
    # -------------------------------------------------------------------------
    def test_adv_07_statistical_model_selection_design_alignment(self):
        """Adversarial Test 7: Factorial in vitro vs Survival cohort."""
        # 2x2 Factorial In Vitro
        res_factorial = CombinationModelSelector.select(
            study_design="in_vitro",
            outcome_type="continuous",
            groups_count=4,
            repeated_measures=False
        )
        self.assertIn("Two-Way", res_factorial.primary_model)
        self.assertIn("Interaction", res_factorial.primary_model)
        self.assertIn("Tukey", res_factorial.post_hoc_test)

        # Survival Analysis
        res_survival = CombinationModelSelector.select(
            study_design="cohort",
            outcome_type="survival",
            covariates=["age", "tumor_stage"]
        )
        self.assertIn("Cox Proportional Hazards", res_survival.primary_model)
        self.assertIn("Hazard Ratio", res_survival.effect_size_metric)

    # -------------------------------------------------------------------------
    # 8. Persian Medical Typography Linter
    # -------------------------------------------------------------------------
    def test_adv_08_persian_typography_zwnj_and_term_expansion(self):
        """Adversarial Test 8: ZWNJ, English numbers in prose, and first-mention term expansion."""
        linter = PersianMedicalTypographyLinter()
        linter.reset_first_mention_tracker()

        raw_text = "می شود و سلول های توموری با آپوپتوز در 5 روز مهار می شود و آپوپتوز ادامه می یابد."
        res = linter.lint(raw_text)

        formatted = res.formatted_text
        # Verify ZWNJ
        self.assertIn("می‌شود", formatted)
        self.assertIn("سلول‌های", formatted)
        self.assertNotIn("می شود", formatted)
        self.assertNotIn("سلول های", formatted)

        # Verify Digit conversion in prose
        self.assertIn("۵", formatted)
        self.assertNotIn(" 5 ", formatted)

        # Verify First mention has Latin term, second mention does NOT duplicate
        self.assertIn("آپوپتوز (Apoptosis)", formatted)
        self.assertEqual(formatted.count("(Apoptosis)"), 1)

    # -------------------------------------------------------------------------
    # 9. Proposal Readiness Gate
    # -------------------------------------------------------------------------
    def test_adv_09_readiness_gate_comprehensive_validation(self):
        """Adversarial Test 9: ReadinessGate passes on valid context, blocks on defective input."""
        valid_context = {
            "research_title_fa": "بررسی اثرات داروی فرضی",
            "framework": "in_vitro",
            "interventions_or_exposures": [
                {"name": "Agent-Alpha", "purity": ">=98%"},
                {"name": "Agent-Beta", "purity": ">=95%"}
            ],
            "biological_claims": [
                "Bax activation promotes apoptosis."
            ]
        }
        res_valid = ProposalReadinessGate.check_all(valid_context)
        self.assertTrue(res_valid.can_proceed)
        self.assertEqual(len(res_valid.passed_modules), len(ProposalReadinessGate.required_modules))
        self.assertEqual(len(res_valid.failed_modules), 0)

        # Defective context: role inversion in claim
        defective_context = {
            "interventions_or_exposures": [{"name": "Agent-Alpha"}],
            "biological_claims": [
                "Bcl-xL induces apoptosis and cell destruction."
            ]
        }
        res_defective = ProposalReadinessGate.check_all(defective_context)
        self.assertFalse(res_defective.can_proceed)
        self.assertIn("biological_mechanism_adversarial_verifier", res_defective.failed_modules)

if __name__ == "__main__":
    unittest.main()
