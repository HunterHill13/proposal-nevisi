#!/usr/bin/env python3
"""
test_v86_deep_reading_and_recall_benchmark.py - Verification Suite for Proposal-Nevisi v8.6.0

Validates:
1. Research Recall Benchmark Calculation & Status Categorization (Recall, Precision, F1, Coverage)
2. Search Miss Diagnosis Taxonomy (13 failure categories, 'We missed this relevant paper because...')
3. Deep Paper Reading Engine (Generic Evidence Sections A-E)
4. Figure-First / Table-First Evidence Extraction & Discrepancy Flag (PRIMARY_DATA_VISUAL_REQUIRES_REVIEW)
5. Methods Reverse-Engineering across diverse domains
6. Evidence Hierarchy 8-Tier Strength Classification
7. Paper-to-Claim Verification 2.0 (8-stage pipeline & 13 issue detections)
8. Post-Research / Post-Writing Citation Audit (unresolved placeholders, unused references)
9. Thematic Comparative Literature Synthesis (theme -> evidence -> comparison -> contradiction -> gap)
10. Adaptive Database Selection with Rationale & Capabilities
11. Negative Evidence Scanner & POSITIVE_EVIDENCE_DOMINANCE Detection
12. Multi-Dimensional Saturation Incompleteness Guard
13. 12-Domain Cross-Topic Recall Benchmarking
14. Core Invariants Preservation (MAX_FINAL_REFERENCES == 25, NO_QUOTA_FILLING == True)
"""

import os
import sys
import unittest
from typing import Dict, List, Any

# Ensure scripts dir is on sys.path
scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from core_policies import (
    ENGINE_VERSION, MAX_FINAL_REFERENCES, NO_QUOTA_FILLING,
    SEARCH_MISS_TAXONOMY, RECALL_BENCHMARK_STATUSES,
    DEEP_READING_SECTIONS, PRIMARY_DATA_VISUAL_REQUIRES_REVIEW,
    EVIDENCE_HIERARCHY_TIERS, CLAIM_VERIFICATION_ISSUES_V2,
    POST_CITATION_AUDIT_STATUSES, DATABASE_SPECIALIZATION_REGISTRY,
    PUBLICATION_BIAS_INDICATORS
)
from scientific_search_adapter import (
    SearchMissAnalyzer, ResearchRecallBenchmark,
    AdaptiveDatabaseSelector, NegativeEvidenceScanner,
    EvidenceBasedSaturationTracker
)
from generic_reference_auditor import (
    StructuredPaperReader, PaperToClaimVerifier, PostResearchCitationAuditor
)
from generic_evidence_synthesis import GenericEvidenceSynthesizer


class TestV86DeepReadingAndRecallBenchmark(unittest.TestCase):
    """Unified test suite for v8.6 research recall, deep reading, and evidence audit capabilities."""

    def test_01_research_recall_benchmark_metrics_and_statuses(self):
        """Tests recall benchmark calculations (Recall, Precision, F1, Coverage) and status assignment."""
        spec = {
            "topic_id": "TEST_CARDIO_01",
            "research_question": "SGLT2 inhibitors and left ventricular ejection fraction in HFpEF",
            "gold_standard_ids": ["doi:10.1056/nejmoa2107038", "doi:10.1016/s0140-6736(22)01429-5", "pmid:34449189"],
            "expected_seed_papers": ["doi:10.1056/nejmoa2107038"],
            "gold_standard_details": [
                {"id": "doi:10.1056/nejmoa2107038", "title": "Empagliflozin in Heart Failure with a Preserved Ejection Fraction", "year": 2021},
                {"id": "doi:10.1016/s0140-6736(22)01429-5", "title": "Dapagliflozin in heart failure with mildly reduced or preserved ejection fraction", "year": 2022},
                {"id": "pmid:34449189", "title": "Cardiovascular and renal outcomes with empagliflozin", "year": 2021}
            ]
        }

        # Scenario A: Full retrieval (Recall = 1.0)
        retrieved_all = [
            {"doi": "10.1056/nejmoa2107038", "title": "Empagliflozin in HFpEF", "database": "PubMed", "query_family": "DIRECT_CORE"},
            {"doi": "10.1016/s0140-6736(22)01429-5", "title": "Dapagliflozin in DELIVER", "database": "Europe PMC", "query_family": "DIRECT_CORE"},
            {"pmid": "34449189", "title": "Cardiorenal study", "database": "PubMed", "query_family": "OUTCOME_SPECIFIC"},
            {"doi": "10.1001/jama.2023.1001", "title": "Background study", "database": "Crossref", "query_family": "CONTEXTUAL_SUPPORT"}
        ]
        res_all = ResearchRecallBenchmark.evaluate_benchmark(spec, retrieved_all)
        self.assertEqual(res_all["validation_status"], "EMPIRICALLY_VALIDATED_RECALL")
        self.assertAlmostEqual(res_all["recall"], 1.0, places=2)
        self.assertAlmostEqual(res_all["precision"], 0.75, places=2)
        self.assertEqual(res_all["true_positive_count"], 3)
        self.assertEqual(res_all["false_negative_count"], 0)
        self.assertEqual(res_all["database_contribution"].get("pubmed"), 2)
        self.assertEqual(res_all["seed_paper_contribution"], 1)

        # Scenario B: Partial retrieval (1 of 3 found -> Recall = 0.333)
        retrieved_partial = [
            {"doi": "10.1056/nejmoa2107038", "title": "Empagliflozin trial", "database": "PubMed"}
        ]
        res_part = ResearchRecallBenchmark.evaluate_benchmark(spec, retrieved_partial)
        self.assertEqual(res_part["validation_status"], "PARTIALLY_VALIDATED_RECALL")
        self.assertAlmostEqual(res_part["recall"], 0.333, places=2)
        self.assertEqual(len(res_part["missed_paper_analysis"]), 2)

        # Scenario C: No gold standard provided
        spec_no_gold = {"topic_id": "EXPLORATORY_TOPIC", "gold_standard_ids": []}
        res_no_gold = ResearchRecallBenchmark.evaluate_benchmark(spec_no_gold, retrieved_all)
        self.assertEqual(res_no_gold["validation_status"], "RECALL_NOT_EMPIRICALLY_ESTABLISHED")

    def test_02_search_miss_analyzer_diagnoses_taxonomy(self):
        """Tests that SearchMissAnalyzer correctly identifies failure modes and outputs diagnostic explanations."""
        ctx = {
            "executed_queries": ["cancer immunotherapy AND clinical trial"],
            "queried_databases": ["pubmed"],
            "executed_query_families": ["DIRECT_CORE"],
            "date_window_years": 5,
            "current_year": 2026,
            "mapped_mesh_terms": ["Immunotherapy", "Neoplasms"]
        }

        # 1. Date filter failure
        target_old = {"id": "OLD_01", "title": "Seminal Trial", "year": 2018}
        diag_date = SearchMissAnalyzer.diagnose_miss(target_old, ctx)
        self.assertEqual(diag_date["primary_miss_reason"], "DATE_FILTER_FAILURE")
        self.assertTrue(diag_date["diagnostic_explanation"].startswith("We missed this relevant paper because"))
        self.assertIn("2018", diag_date["diagnostic_explanation"])

        # 2. Database coverage failure (preprint archive not queried)
        target_prep = {"id": "PREP_01", "title": "Preprint on Novel Biomarker", "abstract": "This preprint reports early findings"}
        diag_db = SearchMissAnalyzer.diagnose_miss(target_prep, ctx)
        self.assertEqual(diag_db["primary_miss_reason"], "DATABASE_COVERAGE_FAILURE")

        # 3. Deduplication error
        ctx_dedup = dict(ctx, deduplicated_ids=["target_dup_01"])
        target_dup = {"id": "target_dup_01", "title": "Deduplicated Study"}
        diag_dedup = SearchMissAnalyzer.diagnose_miss(target_dup, ctx_dedup)
        self.assertEqual(diag_dedup["primary_miss_reason"], "DEDUPLICATION_ERROR")

        # 4. Screening false negative
        ctx_screen = dict(ctx, screened_records=[{"doi": "10.1234/screen.01", "screening_verdict": "EXCLUDED", "exclusion_reason": "WRONG_OUTCOME"}])
        target_screen = {"doi": "10.1234/screen.01", "title": "Excluded Study"}
        diag_screen = SearchMissAnalyzer.diagnose_miss(target_screen, ctx_screen)
        self.assertEqual(diag_screen["primary_miss_reason"], "SCREENING_FALSE_NEGATIVE")

        # 5. Query family failure (null result unsearched)
        target_null = {"id": "NULL_01", "title": "Lack of efficacy in Phase II", "is_negative_finding": True}
        diag_null = SearchMissAnalyzer.diagnose_miss(target_null, ctx)
        self.assertEqual(diag_null["primary_miss_reason"], "QUERY_FAMILY_FAILURE")

        # 6. MeSH mapping failure
        target_mesh = {"id": "MESH_01", "title": "Specialized Syndrome", "mesh_terms": ["Cardiomyopathy, Dilated"]}
        diag_mesh = SearchMissAnalyzer.diagnose_miss(target_mesh, ctx)
        self.assertEqual(diag_mesh["primary_miss_reason"], "MESH_MAPPING_FAILURE")

        # 7. Synonym failure
        target_syn = {"id": "SYN_01", "title": "Alternate Entity Assay", "synonyms": ["Compound-X", "Agent-9"]}
        diag_syn = SearchMissAnalyzer.diagnose_miss(target_syn, ctx)
        self.assertEqual(diag_syn["primary_miss_reason"], "SYNONYM_FAILURE")

    def test_03_deep_reading_schema_sections_a_to_e(self):
        """Tests that StructuredPaperReader extracts generic evidence hierarchy Sections A-E."""
        record = {
            "title": "Randomized controlled evaluation of Bioprosthetic Heart Valve vs Mechanical Valve in Elderly Patients",
            "abstract": "We conducted an RCT with 150 patients (n=150). Administration showed 25% reduction in thromboembolic events (HR 0.75, 95% CI [0.60-0.92], p = 0.008). No major adverse device events were observed.",
            "study_design": "Randomized controlled clinical trial",
            "doi": "10.1001/jama.2024.9999",
            "evidence_directness": "DIRECT"
        }
        reading = StructuredPaperReader.read_paper(record)

        # Check existing 18 fields
        self.assertIn("reading_track", reading)
        self.assertEqual(reading["reading_track"], "CLINICAL_EPIDEMIOLOGY")
        self.assertEqual(reading["sample_size"], 150)
        self.assertIn("25% reduction", reading["observed_quantitative_effect"])
        self.assertIn("p = 0.008", reading["statistical_significance"])

        # Check v8.6 Sections A-E
        self.assertIn("study_identity", reading)
        self.assertEqual(reading["study_identity"]["sample_size"], 150)
        self.assertIn("methods", reading)
        self.assertIn("what_was_done", reading["methods"])
        self.assertIn("results", reading)
        self.assertEqual(reading["results"]["effect_direction"], "DECREASED")
        self.assertIn("interpretation", reading)
        self.assertIn("evidence_provenance", reading)
        self.assertEqual(reading["evidence_provenance"]["evidence_directness_status"], "DIRECT")
        self.assertEqual(reading["evidence_hierarchy_rating"], "DIRECT_HIGH_CONFIDENCE")

    def test_04_figure_first_visual_evidence_and_discrepancy_flag(self):
        """Tests figure-first reading and detection of visual data discrepancies with narrative claims."""
        # Case A: Abstract claims potent inhibition, but Figure 1 indicates non-significant change (p > 0.05)
        record_discrepant = {
            "title": "Investigational Agent in Renal Fibrosis",
            "abstract": "The compound exhibits potent inhibition of fibrotic collagen deposition.",
            "figures": [
                {
                    "figure_id": "Figure 1",
                    "legend": "Quantification of collagen area fraction (p > 0.05 vs vehicle control).",
                    "effect_pct": 4.5
                }
            ]
        }
        reading_disc = StructuredPaperReader.read_paper(record_discrepant)
        self.assertEqual(reading_disc["visual_discrepancy_flag"], PRIMARY_DATA_VISUAL_REQUIRES_REVIEW)
        self.assertTrue(reading_disc["figure_table_evidence"]["discrepancy_detected"])
        self.assertIn("Figure 1", reading_disc["figure_table_evidence"]["discrepancy_reason"])

        # Case B: Consistent visual evidence
        record_consistent = {
            "title": "Investigational Agent in Renal Fibrosis",
            "abstract": "The compound exhibits inhibition of collagen deposition.",
            "figures": [
                {"figure_id": "Figure 1", "legend": "Collagen area fraction (p < 0.01 vs control).", "effect_pct": 42.0}
            ]
        }
        reading_cons = StructuredPaperReader.read_paper(record_consistent)
        self.assertIsNone(reading_cons["visual_discrepancy_flag"])
        self.assertFalse(reading_cons["figure_table_evidence"]["discrepancy_detected"])

    def test_05_methods_reverse_engineering_generic(self):
        """Tests that reverse_engineer_methods dynamically captures protocol variables across different designs."""
        record_vitro = {
            "title": "In vitro MTT assessment of Novel Peptidomimetic in MCF-7 Cells",
            "abstract": "MCF-7 cell cultures were incubated with 25 uM peptide for 48 hours compared to vehicle control. Viability was measured by spectrophotometry.",
            "assay_technique": "Spectrophotometric dye reduction",
            "comparator_control": "0.1% DMSO vehicle"
        }
        methods = StructuredPaperReader.reverse_engineer_methods(record_vitro)
        self.assertEqual(methods["duration"], "48 hours")
        self.assertIn("25 uM", methods["dose_exposure"])
        self.assertEqual(methods["comparator"], "0.1% DMSO vehicle")
        self.assertEqual(methods["measurement_method"], "Spectrophotometric dye reduction")

    def test_06_evidence_hierarchy_8_tiers(self):
        """Tests evidence hierarchy tier classification across confidence levels."""
        # 1. Contradictory study
        rec_contra = {"title": "Negative finding", "evidence_polarity": "CONTRADICTS", "effect_direction": "NO_CHANGE"}
        eval_contra = StructuredPaperReader.evaluate_evidence_hierarchy(rec_contra)
        self.assertEqual(eval_contra["tier"], "CONTRADICTORY")

        # 2. Direct high confidence
        rec_high = {
            "title": "Direct Phase III RCT", "evidence_directness": "DIRECT", "evidence_role": "DIRECT_EVIDENCE",
            "risk_of_bias": "LOW", "study_design_type": "Double-blind randomized controlled trial"
        }
        eval_high = StructuredPaperReader.evaluate_evidence_hierarchy(rec_high)
        self.assertEqual(eval_high["tier"], "DIRECT_HIGH_CONFIDENCE")

        # 3. Indirect support
        rec_indirect = {"title": "Analog Study", "evidence_directness": "INDIRECT", "evidence_role": "ANALOG_EVIDENCE"}
        eval_indirect = StructuredPaperReader.evaluate_evidence_hierarchy(rec_indirect)
        self.assertEqual(eval_indirect["tier"], "INDIRECT_SUPPORT")

        # 4. Mechanistic support
        rec_mech = {"title": "Receptor Binding Pathway", "evidence_role": "MECHANISTIC_EVIDENCE"}
        eval_mech = StructuredPaperReader.evaluate_evidence_hierarchy(rec_mech)
        self.assertEqual(eval_mech["tier"], "MECHANISTIC_SUPPORT")

    def test_07_paper_to_claim_verifier_v2_pipeline(self):
        """Tests PaperToClaimVerifier 2.0 pipeline and detection of translational leap, mismatch, and selective citation."""
        paper_record = {
            "ref_id": "REF_EXP_01",
            "title": "In vitro evaluation of Compound-Z cytotoxicity in murine melanoma cells",
            "abstract": "Compound-Z (10 uM) reduced cell viability by 35% in B16F10 cells in vitro. In cross-sectional analysis, receptor expression was associated with survival.",
            "study_design_type": "in vitro cell culture assay"
        }

        # Case 1: Preclinical to clinical leap
        claim_leap = {
            "claim_id": "CLM_01",
            "claim_text": "Compound-Z cures patients with melanoma in clinical trials",
            "entity": "Compound-Z",
            "model": "human patients"
        }
        res_leap = PaperToClaimVerifier.verify_claim_v2(claim_leap, paper_record)
        self.assertIn(res_leap["entailment_status"], ["PARTIALLY_SUPPORTED", "DISCONFIRMED_DRIFT"])
        self.assertIn("PRECLINICAL_TO_CLINICAL_LEAP", res_leap["detected_issues"])
        self.assertFalse(res_leap["is_valid_support"])

        # Case 2: Model mismatch
        claim_mismatch = {
            "claim_id": "CLM_02",
            "claim_text": "Compound-Z inhibits hepatocyte injury in liver models",
            "entity": "Compound-Z",
            "model": "liver hepatocytes"
        }
        res_mismatch = PaperToClaimVerifier.verify_claim_v2(claim_mismatch, paper_record)
        self.assertIn("MODEL_MISMATCH", res_mismatch["detected_issues"])

        # Case 3: Correlation to causation
        claim_causal = {
            "claim_id": "CLM_03",
            "claim_text": "Receptor expression mechanistically drives and causes patient survival",
            "entity": "Compound-Z"
        }
        res_causal = PaperToClaimVerifier.verify_claim_v2(claim_causal, {
            "title": "Cross-sectional cohort",
            "abstract": "Receptor was associated with survival",
            "study_design_type": "observational cross-sectional study"
        })
        self.assertIn("CORRELATION_TO_CAUSATION", res_causal["detected_issues"])

        # Case 4: Verified entailment (conservative match)
        claim_valid = {
            "claim_id": "CLM_04",
            "claim_text": "Compound-Z exhibits in vitro cytotoxicity in murine B16F10 cells",
            "entity": "Compound-Z",
            "model": "murine melanoma cells"
        }
        res_valid = PaperToClaimVerifier.verify_claim_v2(claim_valid, paper_record)
        self.assertEqual(res_valid["entailment_status"], "VERIFIED_ENTAILMENT")
        self.assertTrue(res_valid["is_valid_support"])
        self.assertEqual(len(res_valid["detected_issues"]), 0)

    def test_08_post_research_citation_auditor(self):
        """Tests PostResearchCitationAuditor detecting unused references, placeholders, and missing citations."""
        portfolio = [
            {"citation_number": 1, "ref_id": "R1", "doi": "10.1001/jama.2024.1", "title": "Study 1"},
            {"citation_number": 2, "ref_id": "R2", "doi": "10.1016/lancet.2023.2", "title": "Study 2"},
            {"citation_number": 3, "ref_id": "R3", "doi": "10.1038/nature.2022.3", "title": "Unused Study 3"}
        ]

        # Text with unresolved placeholder [?] and missing reference [4]
        text_with_issues = (
            "Early intervention improves cardiac outcomes [1]. Mechanism remains under investigation [?]. "
            "Recent meta-analysis confirmed durability [4]."
        )
        audit_res = PostResearchCitationAuditor.audit_proposal_citations(text_with_issues, portfolio)

        self.assertEqual(audit_res["overall_audit_status"], "FAILED")
        issue_types = [i["type"] for i in audit_res["audit_issues"]]
        self.assertIn("UNRESOLVED_CITATION_PLACEHOLDER", issue_types)
        self.assertIn("UNUSED_REFERENCE_IN_PORTFOLIO", issue_types)
        self.assertIn("MISSING_CITATION_IN_PORTFOLIO", issue_types)
        self.assertEqual(audit_res["unused_references_count"], 2)

        # Clean text with full alignment
        clean_text = "Early intervention improves cardiac outcomes [1]. Landmark trials confirmed durability [2] and [3]."
        audit_clean = PostResearchCitationAuditor.audit_proposal_citations(clean_text, portfolio)
        self.assertEqual(audit_clean["overall_audit_status"], "PASSED")
        self.assertEqual(audit_clean["unused_references_count"], 0)

    def test_09_thematic_comparative_synthesis(self):
        """Tests theme-driven comparative synthesis generating cross-study matrices and resolving divergent findings."""
        portfolio = [
            {"ref_id": "S1", "intervention_identity": "Agent-Alpha", "biological_model": "Model-A", "effect_direction": "DECREASED", "primary_endpoint": "Cell viability", "evidence_role": "DIRECT_EVIDENCE"},
            {"ref_id": "S2", "intervention_identity": "Agent-Alpha", "biological_model": "Model-B", "effect_direction": "NO_CHANGE", "primary_endpoint": "Cell viability", "evidence_role": "DIRECT_EVIDENCE"},
            {"ref_id": "S3", "intervention_identity": "Agent-Alpha", "biological_model": "Model-A", "effect_direction": "INCREASED", "primary_endpoint": "Apoptosis pathway", "evidence_role": "MECHANISTIC_EVIDENCE"}
        ]
        synth = GenericEvidenceSynthesizer.build_thematic_comparative_synthesis({}, portfolio)

        self.assertEqual(synth["synthesis_paradigm"], "THEME_EVIDENCE_COMPARISON_CONTRADICTION_LIMITATION_GAP")
        self.assertEqual(len(synth["cross_study_comparison_matrix"]), 3)
        self.assertIn("THEME_PRIMARY_EFFICACY", synth["themes_analyzed"])
        self.assertIn("THEME_MECHANISTIC_PATHWAY", synth["themes_analyzed"])
        # Divergent pairs resolved via root cause analysis rather than majority voting
        self.assertGreaterEqual(len(synth["divergent_findings_resolved"]), 1)
        self.assertEqual(synth["divergent_findings_resolved"][0]["contradiction_resolution_tier"], "PLAUSIBLE_EXPLANATION")

    def test_10_adaptive_database_selector(self):
        """Tests that database selection dynamically adapts with explicit rationales and capability boundaries."""
        # Biomedical clinical trial
        prob_biomed = {"domain": "Cardiology", "title": "SGLT2 inhibitors in heart failure"}
        sel_biomed = AdaptiveDatabaseSelector.select_databases_for_problem(prob_biomed)
        self.assertIn("pubmed", sel_biomed["selected_databases"])
        self.assertIn("europe_pmc", sel_biomed["selected_databases"])
        self.assertIn("crossref", sel_biomed["selected_databases"])
        self.assertIn("why_this_database_was_used", sel_biomed["database_rationales"]["pubmed"])

        # Computational / Bioinformatics problem
        prob_comp = {"domain": "Computational biology", "title": "Deep learning prediction of protein folding"}
        sel_comp = AdaptiveDatabaseSelector.select_databases_for_problem(prob_comp)
        self.assertIn("openalex", sel_comp["selected_databases"])

    def test_11_negative_evidence_scanner_and_publication_bias(self):
        """Tests active scanning for negative/null evidence and detection of POSITIVE_EVIDENCE_DOMINANCE."""
        # 100% positive studies -> flags publication bias risk
        all_positive = [
            {"title": "Study 1", "effect_direction": "DECREASED", "evidence_polarity": "SUPPORTS"},
            {"title": "Study 2", "effect_direction": "DECREASED", "evidence_polarity": "SUPPORTS"},
            {"title": "Study 3", "effect_direction": "DECREASED", "evidence_polarity": "SUPPORTS"}
        ]
        scan_pos = NegativeEvidenceScanner.scan_evidence_balance(all_positive)
        self.assertEqual(scan_pos["evidence_balance_status"], "POSITIVE_EVIDENCE_DOMINANCE")
        self.assertEqual(scan_pos["publication_bias_risk"], "HIGH_PUBLICATION_BIAS_SUSPECTED")

        # Balanced set with negative study
        balanced = [
            {"title": "Study 1", "effect_direction": "DECREASED", "evidence_polarity": "SUPPORTS"},
            {"title": "Study 2", "effect_direction": "NO_CHANGE", "evidence_polarity": "NEUTRAL"}
        ]
        scan_bal = NegativeEvidenceScanner.scan_evidence_balance(balanced)
        self.assertEqual(scan_bal["evidence_balance_status"], "NEGATIVE_EVIDENCE_RECOVERED")
        self.assertEqual(scan_bal["publication_bias_risk"], "LOW_OR_BALANCED")

    def test_12_saturation_incomplete_guard(self):
        """Tests that saturation is marked INCOMPLETE if key dimensions remain unexplored despite diminishing yield."""
        # Diminishing yield reached (0 new records in batch 4) but only 1 database queried
        single_db_batches = [
            [{"id": f"R{i}", "doi": f"10.1001/r{i}", "entity": "EntityA", "outcome": "viability", "database": "pubmed"} for i in range(15)],
            [{"id": f"R{i}", "doi": f"10.1001/r{i}", "entity": "EntityA", "outcome": "viability", "database": "pubmed"} for i in range(10, 16)],
            [{"id": f"R{i}", "doi": f"10.1001/r{i}", "entity": "EntityA", "outcome": "viability", "database": "pubmed"} for i in range(5, 15)],
            [{"id": f"R{i}", "doi": f"10.1001/r{i}", "entity": "EntityA", "outcome": "viability", "database": "pubmed"} for i in range(10)]
        ]
        sat_res = EvidenceBasedSaturationTracker.evaluate_saturation(single_db_batches, saturation_threshold=0.10, min_batches_required=3)
        self.assertEqual(sat_res["saturation_status"], "SATURATION_INCOMPLETE")
        self.assertFalse(sat_res["is_saturated"])
        self.assertTrue(any("DATABASE_NOVELTY" in dim for dim in sat_res["incomplete_dimensions"]))

    def test_13_cross_topic_recall_benchmarking_12_domains(self):
        """Validates ResearchRecallBenchmark execution across 12 distinct biomedical/health domains."""
        domains = [
            ("CLINICAL_TRIAL", "SGLT2 inhibitors in heart failure with preserved ejection fraction"),
            ("DIAGNOSTIC_ACCURACY", "miRNA-21 sensitivity and specificity for early colorectal cancer"),
            ("EPIDEMIOLOGY", "Dengue virus transmission dynamics under climate change scenarios"),
            ("MEDICAL_DEVICE", "Biocompatibility and fatigue life of 3D-printed titanium orthopedic implants"),
            ("BIOMATERIALS", "Hydrogel scaffolds with controlled growth factor delivery for cartilage repair"),
            ("PHARMACOGENOMICS", "CYP2C19 loss-of-function polymorphisms and clopidogrel resistance in stroke"),
            ("COMPUTATIONAL_BIOLOGY", "AlphaFold prediction of alpha-synuclein oligomerization interfaces"),
            ("SYSTEMATIC_REVIEW", "Comparative efficacy of first-line immunotherapies in metastatic NSCLC"),
            ("OBSERVATIONAL_COHORT", "Longitudinal cognitive decline and retinal microvascular changes in diabetes"),
            ("ANIMAL_EXPERIMENT", "SYRCLE-guided evaluation of resveratrol on renal ischemia-reperfusion in rats"),
            ("QUALITATIVE_HEALTH_SERVICES", "Patient-reported barriers to telemedicine adoption in rural oncology clinics"),
            ("BASIC_LABORATORY", "Mechanistic evaluation of phytochemical caspase activation in monolayer cultures")
        ]

        for d_id, q_text in domains:
            spec = {
                "topic_id": d_id,
                "research_question": q_text,
                "gold_standard_ids": [f"doi:10.1000/{d_id.lower()}.01", f"doi:10.1000/{d_id.lower()}.02"],
                "expected_seed_papers": [f"doi:10.1000/{d_id.lower()}.01"]
            }
            retrieved = [
                {"doi": f"10.1000/{d_id.lower()}.01", "title": f"{d_id} primary study", "database": "pubmed", "query_family": "DIRECT_CORE"},
                {"doi": f"10.1000/{d_id.lower()}.02", "title": f"{d_id} validation study", "database": "europe_pmc", "query_family": "METHOD_ASSAY"}
            ]
            eval_res = ResearchRecallBenchmark.evaluate_benchmark(spec, retrieved)
            self.assertEqual(eval_res["validation_status"], "EMPIRICALLY_VALIDATED_RECALL")
            self.assertAlmostEqual(eval_res["recall"], 1.0)
            self.assertEqual(eval_res["false_negative_count"], 0)

    def test_14_v86_invariants_preserved(self):
        """Enforces that core architecture invariants remain strictly protected in v8.6.0."""
        self.assertEqual(MAX_FINAL_REFERENCES, 25, "Hard ceiling of 25 final references must be strictly preserved.")
        self.assertTrue(NO_QUOTA_FILLING, "No artificial quota filling policy must remain True.")
        self.assertTrue(ENGINE_VERSION in ["8.6.0", "8.7.0", "9.0.0", "9.1.0", "9.2.0"], "Engine version must be synchronized to at least 8.6.0.")


if __name__ == "__main__":
    unittest.main()
