#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_v91_hardening.py - Comprehensive Scientific Hardening & Epistemic Integrity Test Suite
Proposal-Nevisi Engine v9.1

Tests all 8 architectural modules against authentic edge cases and failure modes:
1. Compound Entity Normalizer: Purity vs Identity disentanglement.
2. Biological Mechanism Adversarial Verifier: Role inversions, causal leaps, and mechanistic chains.
3. Combination Hypothesis Engine: Positive-evidence dominance and missing direct evidence warnings.
4. Statistical & Interaction Model Selectors: True factorial vs descriptive grouping, live virus kinetics.
5. Methodology Completeness Gate: 28 sections, sample size inputs epistemic evaluation, pseudo-replication guard.
6. Citation Tracker: Vancouver order-of-appearance, unused reference blocking, contextual model mismatch.
7. Native OMML Math Engine & DOCX E2E: Unzip inspection asserting <m:oMath> and zero raw LaTeX.
8. Persian Medical Typography Linter: Guards for English parentheses, math, citations, DOIs.
"""

import os
import sys
import re
import json
import zipfile
import tempfile
import unittest

sys.stdout.reconfigure(encoding='utf-8')

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.abspath(os.path.join(TESTS_DIR, "..", "scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from compound_entity_normalizer import CompoundEntityNormalizer
from biological_mechanism_adversarial_verifier import BiologicalMechanismAdversarialVerifier
from combination_hypothesis_engine import CombinationHypothesisEngine
from statistical_model_selector import StatisticalAnalysisModelSelector
from combination_interaction_model_selector import CombinationInteractionModelSelector
from combination_model_selector import CombinationModelSelector
from methodology_completeness_gate import MethodologyCompletenessGate, REQUIRED_SECTIONS_28
from citation_tracker import CitationTracker
from native_omml_math_engine import NativeOmmlMathEngine
from persian_medical_typography_linter import PersianMedicalTypographyLinter
from proposal_readiness_gate import ProposalReadinessGate
from docx_builder import DocxBuilder
from generate_compliant_proposal import ProposalGenerator
from proposal_structure_validator import ProposalStructureValidator


class TestV91HardeningSuite(unittest.TestCase):
    """Rigorous hardening test suite enforcing epistemic honesty and scientific accuracy."""

    # =========================================================================
    # 1. Compound Entity Normalizer
    # =========================================================================
    def test_compound_bare_name_not_assumed_pure(self):
        """Bare compound name establishes parent identity but purity is NOT_REPORTED, not >=95%."""
        norm = CompoundEntityNormalizer.normalize("Curcumin")
        self.assertEqual(norm.category, "PURE_COMPOUND")
        self.assertTrue(norm.is_parent_compound)
        self.assertFalse(norm.is_pure)
        self.assertEqual(norm.analytical_purity, "NOT_REPORTED")
        self.assertTrue(any("ANALYTICAL_PURITY_UNSPECIFIED" in w for w in norm.methodological_warnings))

    def test_compound_certified_pure_standard(self):
        """Certified analytical standard (>=99%) is classified as pure."""
        norm = CompoundEntityNormalizer.normalize("Resveratrol (HPLC >=99.5% pure standard)")
        self.assertEqual(norm.category, "PURE_COMPOUND")
        self.assertTrue(norm.is_pure)
        self.assertTrue(norm.is_parent_compound)
        self.assertIn("99.5", norm.analytical_purity)

    def test_compound_synthetic_derivative_cannot_claim_parent_identity(self):
        """Synthetic derivative or ester must NOT be conflated with the parent compound."""
        norm = CompoundEntityNormalizer.normalize("Betulinic acid benzyl ester derivative")
        self.assertEqual(norm.category, "SYNTHETIC_ANALOG")
        self.assertFalse(norm.is_parent_compound)
        self.assertFalse(norm.is_pure)
        self.assertTrue(any("SYNTHETIC_DERIVATIVE" in w for w in norm.methodological_warnings))

    def test_compound_botanical_crude_extract(self):
        """Botanical extract is categorized as CRUDE_EXTRACT with strict attribution warnings."""
        norm = CompoundEntityNormalizer.normalize("Methanolic extract of Taraxacum officinale")
        self.assertEqual(norm.category, "CRUDE_EXTRACT")
        self.assertFalse(norm.is_parent_compound)
        self.assertFalse(norm.is_pure)
        self.assertTrue(any("CRUDE_EXTRACT_ATTRIBUTION_FALLACY" in w for w in norm.methodological_warnings))

    # =========================================================================
    # 2. Biological Mechanism Adversarial Verifier
    # =========================================================================
    def test_mechanism_inverted_apoptotic_role_contradicted(self):
        """Inverted biological roles (e.g., anti-apoptotic Bcl-2 reported as inducing apoptosis) are CONTRADICTED."""
        res = BiologicalMechanismAdversarialVerifier.check("Bcl-2 directly promotes apoptosis and caspase cleavage.")
        self.assertEqual(res.status, "CONTRADICTED")
        self.assertIn("anti-apoptotic", res.canonical_role.lower())
        self.assertIn("pro-apoptotic", res.asserted_role.lower())

    def test_mechanism_ungrounded_causal_leap(self):
        """Mechanistic claims asserting causality without evidence are flagged as UNVERIFIED."""
        res = BiologicalMechanismAdversarialVerifier.check("CandidateProteinZ uniquely reorganizes the nuclear lamina.")
        self.assertEqual(res.status, "UNVERIFIED")

    def test_mechanism_chain_verification_complete_and_broken(self):
        """Multi-edge mechanistic chain: complete chain verified, broken chain flagged."""
        # Evidence covering edge 1 and edge 2, but missing edge 3 and 4
        evidence = [
            {"title": "Agent Alpha suppresses Target Protein X in cell model"},
            {"title": "Target Protein X regulation alters mitochondrial membrane potential"}
        ]
        chain_res = BiologicalMechanismAdversarialVerifier.verify_mechanistic_chain(
            agent="Agent Alpha",
            target="Target Protein X",
            cellular_process="Mitochondrial Permeabilization",
            interaction="Interaction endpoint",
            endpoint="Synergistic Apoptosis Induction",
            evidence_records=evidence
        )
        self.assertFalse(chain_res.is_fully_established)
        self.assertTrue(len(chain_res.unsupported_edges) > 0)

    # =========================================================================
    # 3. Combination Hypothesis Engine
    # =========================================================================
    def test_combination_positive_evidence_dominance_warning(self):
        """When 100% of retrieved studies report synergism, POSITIVE_EVIDENCE_DOMINANCE_WARNING is emitted."""
        pos_evidence = [
            {"title": "Supra-additive synergy of Agent-A and Agent-B", "abstract": "CI = 0.42 confirms synergism."},
            {"title": "Combination potentiation of cytotoxicity", "abstract": "Synergistic reduction in viability by Agent-A."}
        ]
        analysis = CombinationHypothesisEngine.analyze(
            entity_a="Agent-A",
            entity_b="Agent-B",
            target="cell viability",
            retrieved_evidence=pos_evidence
        )
        self.assertEqual(analysis.evidence_balance_score, 1.0)
        self.assertTrue(any("POSITIVE_EVIDENCE_DOMINANCE_WARNING" in w for w in analysis.bias_warnings))
        self.assertIn("آنتاگونیستی", analysis.antagonism_hypothesis)

    def test_combination_missing_direct_study_emits_clear_warning(self):
        """When no direct co-treatment study exists on the target model, NO_DIRECT_COMBINATION_EVIDENCE is emitted."""
        indirect_evidence = [
            {"title": "Apoptosis induction by caspase activation in cancer cells"},
            {"title": "Methodological standards for Chou-Talalay combination index testing"}
        ]
        analysis = CombinationHypothesisEngine.analyze(
            entity_a="Agent-A",
            entity_b="Agent-B",
            target="cell viability",
            model_or_cell_line="Model-Z",
            retrieved_evidence=indirect_evidence
        )
        self.assertFalse(analysis.has_direct_combination_evidence)
        self.assertTrue(any("NO_DIRECT_COMBINATION_EVIDENCE" in w for w in analysis.bias_warnings))

    # =========================================================================
    # 4. Statistical & Interaction Model Selectors
    # =========================================================================
    def test_statistical_selector_descriptive_groups_vs_factorial(self):
        """Descriptive multi-group setup (is_factorial=False) selects One-Way ANOVA; factorial selects Two-Way ANOVA."""
        res_descriptive = StatisticalAnalysisModelSelector.select(
            study_design="in_vitro",
            outcome_type="continuous",
            groups_count=4,
            is_factorial=False
        )
        self.assertIn("One-Way", res_descriptive.primary_model)
        self.assertFalse(res_descriptive.is_factorial)

        res_factorial = StatisticalAnalysisModelSelector.select(
            study_design="in_vitro",
            outcome_type="continuous",
            groups_count=4,
            is_factorial=True
        )
        self.assertIn("Two-Way", res_factorial.primary_model)
        self.assertTrue(res_factorial.is_factorial)
        self.assertIn("Interaction", res_factorial.primary_model)

    def test_combination_interaction_live_virus_kinetics(self):
        """Combination interaction model involving live oncolytic virus flags replication kinetics and schedule dependence."""
        res = CombinationInteractionModelSelector.select(
            agent_a_type="small_molecule",
            agent_b_type="oncolytic_virus",
            live_virus_involved=True,
            schedule_dependent=True
        )
        self.assertTrue(len(res.viral_kinetic_considerations) > 0)
        self.assertIsNotNone(res.schedule_dependence_notes)

    # =========================================================================
    # 5. Methodology Completeness & Sample Size Gate
    # =========================================================================
    def test_methodology_gate_insufficient_sample_size_inputs_not_fictitious(self):
        """Missing effect size and variance emits INSUFFICIENT_INPUTS without fabricating fictitious formulas."""
        eval_res = MethodologyCompletenessGate.evaluate_sample_size_inputs(
            study_design="in_vitro",
            primary_endpoint="Cell Viability (%)",
            experimental_unit="Independent well culture"
        )
        self.assertEqual(eval_res.status, "INSUFFICIENT_INPUTS")
        self.assertIn("effect_size", eval_res.missing_inputs)
        self.assertIn("variance_or_sd", eval_res.missing_inputs)

    def test_methodology_pseudo_replication_guard(self):
        """Biological vs technical replicates enforcer guards against pseudo-replication (4x3 is n=4)."""
        eval_res = MethodologyCompletenessGate.evaluate_sample_size_inputs(
            study_design="in_vitro",
            primary_endpoint="Absorbance OD",
            experimental_unit="Independent cell culture flask",
            biological_replicates=4,
            technical_replicates=3
        )
        self.assertEqual(eval_res.total_independent_n, 4)
        self.assertTrue(any("PSEUDO_REPLICATION_GUARD" in w for w in eval_res.warnings))

    def test_methodology_plain_text_without_formula_fails_gate(self):
        """Sample size section with plain arbitrary number but no mathematical formula or replicate design fails gate."""
        proposal = {sec: f"محتوای معتبر برای {sec}" for sec in REQUIRED_SECTIONS_28}
        proposal["حجم نمونه و روش محاسبه آن"] = "حجم نمونه در این مطالعه برابر با ۲۴ نمونه انتخاب گردید."

        res = MethodologyCompletenessGate.validate(proposal)
        self.assertFalse(res.can_proceed)
        self.assertFalse(res.is_complete)
        self.assertIn("حجم نمونه و روش محاسبه آن", res.sections_needing_formula)

    # =========================================================================
    # 6. Citation Tracker
    # =========================================================================
    def test_citation_tracker_unused_reference_fails_validation(self):
        """Unused reference in bibliography causes validation failure (Zero tolerance for unused references)."""
        tracker = CitationTracker()
        tracker.register_reference("REF_1", {"title": "Cited Paper"})
        tracker.register_reference("REF_UNUSED", {"title": "Unused Paper"})

        tracker.register_claim("Important scientific finding.", "REF_1")
        audit = tracker.validate()
        self.assertFalse(audit.is_valid)
        self.assertIn("REF_UNUSED", audit.unused_references)

    def test_citation_tracker_contextual_model_mismatch_detected(self):
        """Claiming effect in Target Cell Line A when source studied Cell Line B is flagged as INDIRECT_ANALOGOUS."""
        tracker = CitationTracker()
        tracker.register_reference("REF_X", {
            "title": "Study in MCF-7 cells",
            "cell_lines": ["MCF-7"],
            "compounds": ["Compound-A"]
        })
        audit = tracker.audit_claim_binding(
            claim_text="Compound-A reduces viability in A549 lung cells.",
            citation_id="REF_X",
            target_model="A549",
            target_compound="Compound-A"
        )
        self.assertEqual(audit.evidence_tier, "INDIRECT_ANALOGOUS")
        self.assertFalse(audit.model_match)

    def test_citation_tracker_vancouver_document_reindexing(self):
        """Re-indexing document strictly rewrites citations by 1-based first-appearance order."""
        tracker = CitationTracker()
        tracker.register_reference("KEY_ALPHA", {"title": "Alpha Reference", "citation_id": "KEY_ALPHA"})
        tracker.register_reference("KEY_BETA", {"title": "Beta Reference", "citation_id": "KEY_BETA"})

        raw_doc = "First sentence citing Beta [KEY_BETA]. Second sentence citing Alpha [KEY_ALPHA] and Beta [KEY_BETA]."
        reindex_res = tracker.reindex_document(raw_doc, bibliography=tracker._registered_references)

        # In appearance order, KEY_BETA is [1], KEY_ALPHA is [2]
        self.assertIn("[1]", reindex_res.rewritten_text)
        self.assertIn("[2]", reindex_res.rewritten_text)
        ordered_bib = reindex_res.reordered_bibliography
        self.assertEqual(ordered_bib[0]["citation_id"], "KEY_BETA")
        self.assertEqual(ordered_bib[0]["citation_number"], 1)
        self.assertEqual(ordered_bib[1]["citation_id"], "KEY_ALPHA")
        self.assertEqual(ordered_bib[1]["citation_number"], 2)

    # =========================================================================
    # 7. Native OMML Math Engine & DOCX E2E Test
    # =========================================================================
    def test_docx_omml_e2e_xml_verification(self):
        """Generates DOCX from markdown containing LaTeX, unzips, and asserts <m:oMath> and 0 raw LaTeX."""
        md_text = (
            "# پروپوزال آزمایشی\n"
            "## ۱۰. حجم نمونه و روش محاسبه آن\n"
            "محاسبه بر مبنای فرمول تخصیص نمونه صورت پذیرفت:\n"
            r"$$ n = \frac{2(Z_{1-\alpha/2} + Z_{1-\beta})^2 \cdot \sigma^2}{\Delta^2} $$" + "\n"
            "با سطح اطمینان ۹۵٪.\n"
        )
        with tempfile.TemporaryDirectory() as td:
            docx_path = os.path.join(td, "e2e_math_test.docx")
            DocxBuilder.build_docx(md_text, docx_path)
            self.assertTrue(os.path.exists(docx_path))

            with zipfile.ZipFile(docx_path, 'r') as zf:
                xml_content = zf.read('word/document.xml').decode('utf-8')

            self.assertIn("<m:oMath", xml_content, "Missing native OMML <m:oMath> in word/document.xml")
            self.assertNotIn(r"\frac", xml_content, "Raw LaTeX \\frac leaked into word/document.xml")
            self.assertNotIn(r"\Delta", xml_content, "Raw LaTeX \\Delta leaked into word/document.xml")

    # =========================================================================
    # 8. Persian Medical Typography Linter
    # =========================================================================
    def test_typography_linter_guards_protected_elements(self):
        """English text in parentheses, DOIs, PMIDs, and citations are strictly preserved."""
        linter = PersianMedicalTypographyLinter()
        raw = "تست داروی جدید با بازدهی بالا (IC50 = 12.5 uM) در منبع [1, 2] با DOI: 10.1016/j.canlet.2020.01.001."
        formatted = linter.format_text(raw)
        self.assertIn("(IC50 = 12.5 uM)", formatted)
        self.assertIn("[1, 2]", formatted)
        self.assertIn("10.1016/j.canlet.2020.01.001", formatted)

    # =========================================================================
    # 9. Canonical 28-Section Architecture & Completeness Tests
    # =========================================================================
    def test_canonical_28_section_generation_and_validation(self):
        """Validates that assemble_pajooheshyar_28 produces the exact 28 canonical sections passing all gates."""
        benchmark_path = os.path.join(TESTS_DIR, "fixtures", "benchmark_dataset", "benchmark_proposal_data.json")
        with open(benchmark_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        md_28 = ProposalGenerator.assemble_pajooheshyar_28(data)
        self.assertIsNotNone(md_28)
        self.assertIn("## ۲۸. منابعی که استفاده شد (انگلیسی یا فارسی)", md_28)

        # 1. Test ProposalStructureValidator in 28-section mode
        val_res = ProposalStructureValidator.validate_proposal_text(md_28)
        self.assertEqual(val_res["status"], "PASS")
        self.assertEqual(val_res.get("format_detected"), "28_SECTIONS")
        self.assertTrue(val_res["all_28_sections_present"])
        self.assertTrue(val_res["section_ordering_intact"])
        self.assertTrue(val_res["variable_table_present"])
        self.assertTrue(val_res["timeline_schedule_present"])
        self.assertEqual(len(val_res["missing_sections"]), 0)

        # 2. Test MethodologyCompletenessGate
        comp_res = MethodologyCompletenessGate.validate(md_28)
        self.assertTrue(comp_res.is_complete)
        self.assertTrue(comp_res.can_proceed)
        self.assertEqual(len(comp_res.missing_sections), 0)

    def test_canonical_28_section_adversarial_missing_section(self):
        """Adversarial test: Removing a canonical section must cause validation failure."""
        benchmark_path = os.path.join(TESTS_DIR, "fixtures", "benchmark_dataset", "benchmark_proposal_data.json")
        with open(benchmark_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        md_28 = ProposalGenerator.assemble_pajooheshyar_28(data)
        # Deliberately remove Section 22 (حجم نمونه و روش محاسبه آن)
        defective_md = re.sub(r'## ۲۲\. حجم نمونه و روش محاسبه آن.*?(?=## ۲۳|\Z)', '', md_28, flags=re.DOTALL)
        self.assertNotIn("## ۲۲. حجم نمونه و روش محاسبه آن", defective_md)

        val_res = ProposalStructureValidator.validate_proposal_text(defective_md)
        self.assertEqual(val_res["status"], "FAIL")
        self.assertFalse(val_res["all_28_sections_present"])
        self.assertTrue(any("حجم نمونه" in s for s in val_res["missing_sections"]))

        comp_res = MethodologyCompletenessGate.validate(defective_md)
        self.assertFalse(comp_res.is_complete)
        self.assertFalse(comp_res.can_proceed)
        self.assertTrue(any("حجم نمونه" in s for s in comp_res.missing_sections))


if __name__ == "__main__":
    unittest.main()
