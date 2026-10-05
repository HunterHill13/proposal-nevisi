#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_v85_advanced_research_engine.py - Comprehensive Verification Suite for v8.5 Research Engine
Proposal-Nevisi Engine v8.5 (Universal Biomedical Architecture)

Validates all 12 key capabilities upgraded from external research workflows (AIPOCH & K-Dense):
1. 16 Query Families & MeSH Controlled Vocabulary Mapping
2. Controlled vs Free-Text Yield Comparison
3. Multi-Directional Citation Chasing (Backward, Forward, Lateral) & Provenance
4. 8-Category Seed Paper Discovery & Non-Automatic Inclusion Policy
5. 7-Dimension Evidence-Based Saturation & False Saturation Guard
6. Multi-Source Database Diversity Tracking (PubMed, Europe PMC, OpenAlex, Crossref)
7. 4-Track Structured Paper Reader & 18-Field Deterministic Extraction
8. 6-Type Citation Drift Detection & Paper-to-Claim Entailment
9. Triple-Check Duplicate Detection & Identifier Canonicalization
10. 3-Tier Contradiction Explanation Partitioning (Demonstrated, Plausible, Unresolved)
11. Reproducible Research Run Manifest & SHA-256 Checksum
12. Multi-Domain Topic Generalization & Invariant Preservation (<= 25 Refs, No Quota-Filling)
"""

import os
import sys
import json
import unittest
from typing import Dict, List, Any

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from core_policies import (
    MAX_FINAL_REFERENCES, MIN_FINAL_REFERENCES, NO_QUOTA_FILLING,
    SEARCH_FAMILIES_ONTOLOGY, SATURATION_DIMENSIONS, SEED_PAPER_CATEGORIES,
    CITATION_CHASE_DIRECTIONS, CITATION_DRIFT_TYPES,
    STRUCTURED_PAPER_READING_TRACKS, CONTRADICTION_EXPLANATION_LEVELS
)
from generic_search_planner import GenericSearchPlanner, MeSHMapper, QueryFamilySearchPlanner
from scientific_search_adapter import (
    ScientificSearchAdapter, SeedPaperDiscoveryEngine,
    CitationChasingEngine, EvidenceBasedSaturationTracker,
    ResearchRunManifest
)
from generic_reference_auditor import (
    GenericReferenceAuditor, StructuredPaperReader, PaperToClaimVerifier
)
from generic_contradiction_engine import GenericContradictionEngine
from research_problem_model import ProblemModelBuilder


class TestV85AdvancedResearchEngine(unittest.TestCase):
    """Rigorous verification suite for Proposal-Nevisi v8.5 external research integration."""

    def setUp(self):
        self.sample_spec = {
            "model_id": "RPM_V85_TEST_CARDIO_001",
            "research_title_fa": "بررسی اثر محافظتی مولکول پپتیدی فرضی X در مدل تجربی ایسکمی قلبی",
            "research_title_en": "Cardioprotective Evaluation of Peptide X in Ischemia-Reperfusion Model",
            "domain": "cardiology",
            "framework": "MECHANISTIC",
            "target_condition": {
                "name_en": "Myocardial Ischemia Reperfusion Injury",
                "name_fa": "آسیب خون‌رسانی مجدد ایسکمی قلبی",
                "mesh_term": "Myocardial Ischemia",
                "synonyms": ["Cardiac Ischemia"]
            },
            "population_or_model": {
                "model_type": "CELL_CULTURE_IN_VITRO",
                "primary_system": "H9c2 Cardiomyoblasts",
                "secondary_systems": [],
                "normal_control_system": "Vehicle treated controls"
            },
            "interventions_or_exposures": [
                {
                    "name": "Cardioprotective Peptide X",
                    "chemical_or_biological_class": "Synthetic Peptide",
                    "role": "PRIMARY_AGENT",
                    "mesh_terms": [],
                    "synonyms": ["CP-101"]
                }
            ],
            "comparators": [{"name": "Saline Vehicle", "type": "VEHICLE_CONTROL"}],
            "primary_outcomes": [{"name": "Cell Viability and Apoptosis Inhibition", "type": "VIABILITY", "measurement_unit": "% viable cells"}],
            "hypothesized_mechanisms": [{"pathway_name": "Mitochondrial Protection", "target_molecules": ["Bcl-2", "Bax"], "expected_modulation": "UPREGULATION"}],
            "controlled_vocabulary": {"primary_mesh": ["Myocardial Ischemia"], "all_synonyms": ["CP-101"], "exclusion_terms": []}
        }
        self.problem_model = ProblemModelBuilder.create_from_specification(self.sample_spec)

    # =========================================================================
    # 1. QUERY FAMILIES & MESH CONTROLLED VOCABULARY
    # =========================================================================

    def test_search_families_ontology_completeness(self):
        """Verifies all 16 query families exist in SEARCH_FAMILIES_ONTOLOGY."""
        self.assertEqual(len(SEARCH_FAMILIES_ONTOLOGY), 16)
        expected_families = [
            "EXACT_CONCEPT_COMBINATION", "SYNONYM_EXPANDED_COMBINATION",
            "CONTROLLED_VOCABULARY_MESH", "POPULATION_MODEL_SPECIFIC",
            "INTERVENTION_SPECIFIC", "OUTCOME_SPECIFIC", "MECHANISM_SPECIFIC",
            "STUDY_DESIGN_SPECIFIC", "METHODOLOGY_ASSAY_SPECIFIC",
            "NEGATIVE_NULL_RESULT", "HISTORICAL_FOUNDATIONAL",
            "RECENT_EMERGING_LITERATURE", "TERMINOLOGY_VARIANT",
            "ACRONYM_ABBREVIATION", "ALTERNATIVE_SPELLING_HYPHENATION",
            "CITATION_DERIVED_DISCOVERY"
        ]
        for fam in expected_families:
            self.assertIn(fam, SEARCH_FAMILIES_ONTOLOGY)

    def test_mesh_mapper_lookup_and_controlled_fallback(self):
        """Tests MeSHMapper controlled vocabulary lookup and free-text fallback."""
        mapper = MeSHMapper()
        # Direct lookup for known condition
        res = mapper.map_term("heart failure")
        self.assertIn("Heart Failure", res["mesh_terms"])
        self.assertFalse(res["was_fallback"])

        # Concept query with hybrid MeSH and Title/Abstract
        query_str = mapper.to_concept_query("heart failure")
        self.assertIn("[MeSH Terms]", query_str)
        self.assertIn("[Title/Abstract]", query_str)

        # Free-text syntax fallback for unmapped custom concept
        unmapped_res = mapper.map_term("xyz123 uncharacterized synthetic entity 999")
        self.assertTrue(unmapped_res["was_fallback"])

    def test_controlled_vs_freetext_comparison(self):
        """Tests MeSH vs free-text retrieval yield and overlap comparison."""
        mock_mesh_recs = [
            {"pmid": "101", "title": "Heart Failure Mechanisms in H9c2"},
            {"pmid": "102", "title": "Myocardial Protection Protocols"}
        ]
        mock_free_recs = [
            {"pmid": "102", "title": "Myocardial Protection Protocols"},
            {"pmid": "103", "title": "Peptide X Cardiomyocyte Viability"}
        ]
        comparison = QueryFamilySearchPlanner.compare_controlled_vs_freetext(
            mesh_results=mock_mesh_recs,
            freetext_results=mock_free_recs
        )
        self.assertEqual(comparison["mesh_yield"], 2)
        self.assertEqual(comparison["freetext_yield"], 2)
        self.assertEqual(comparison["overlap_count"], 1)
        self.assertEqual(comparison["total_combined_unique"], 3)
        self.assertEqual(comparison["mesh_unique_gain"], 1)
        self.assertEqual(comparison["freetext_unique_gain"], 1)

    def test_query_family_planner_execution(self):
        """Tests dynamic query family selection and execution across applicable families."""
        planner = QueryFamilySearchPlanner(problem_model=self.problem_model)
        plan = planner.build_plan()
        self.assertGreaterEqual(plan["total_families_selected"], 8)
        self.assertIn("EXACT_CONCEPT_COMBINATION", plan["selected_families"])
        self.assertIn("NEGATIVE_NULL_RESULT", plan["selected_families"])

        # Execute in mock/offline mode
        exec_res = planner.execute_query_families(mode="offline")
        self.assertEqual(exec_res["execution_status"], "COMPLETED_OFFLINE")
        self.assertGreaterEqual(len(exec_res["family_results"]), 8)

    # =========================================================================
    # 2. CITATION CHASING & PROVENANCE
    # =========================================================================

    def test_citation_chasing_multi_directional_provenance(self):
        """Tests backward, forward, and lateral citation chaining with explicit discovery provenance."""
        seed = {
            "doi": "10.1016/j.cardio.2023.01.001",
            "pmid": "35001122",
            "title": "Landmark cardioprotective study",
            "authors": ["Smith John", "Doe Jane"],
            "cited_references": [
                {"doi": "10.1016/j.method.1995.05.002", "title": "Foundational cardiac cell isolation method"}
            ],
            "citing_papers": [
                {"doi": "10.1016/j.cardio.2024.08.005", "title": "Subsequent replication of peptide efficacy"}
            ]
        }
        corpus_pool = [
            {"doi": "10.1016/j.cardio.2022.03.003", "title": "Lateral study by Smith John on cardiac peptides", "authors": ["Smith John"]}
        ]

        result = CitationChasingEngine.chase_citations(
            seed_papers=[seed],
            directions=["BACKWARD", "FORWARD", "LATERAL"],
            max_depth=1,
            network_corpus=corpus_pool
        )

        self.assertEqual(result["chasing_status"], "CHASING_COMPLETE")
        self.assertEqual(result["total_candidates_discovered"], 3)
        self.assertEqual(result["chasing_statistics_by_direction"]["BACKWARD"], 1)
        self.assertEqual(result["chasing_statistics_by_direction"]["FORWARD"], 1)
        self.assertEqual(result["chasing_statistics_by_direction"]["LATERAL"], 1)

        # Inspect discovery paths
        candidates = result["discovered_candidates"]
        backward_c = next(c for c in candidates if c["discovery_direction"] == "BACKWARD")
        self.assertEqual(backward_c["discovery_method"], "CITATION_CHASING_BACKWARD")
        self.assertEqual(backward_c["chain_depth"], 1)
        self.assertEqual(backward_c["discovery_path"][0], "SEED:10.1016/j.cardio.2023.01.001")
        self.assertEqual(backward_c["discovery_path"][1], "BACKWARD")

    # =========================================================================
    # 3. SEED PAPER DISCOVERY & NON-AUTOMATIC INCLUSION
    # =========================================================================

    def test_seed_paper_discovery_engine_categories(self):
        """Verifies SeedPaperDiscoveryEngine categorizes papers into 8 distinct anchor categories."""
        papers = [
            {"title": "Systematic review and meta-analysis of peptide cardioprotection", "study_design": "Systematic Review", "year": 2021},
            {"title": "International clinical consensus guideline for myocardial infarction", "study_design": "Clinical Guideline", "year": 2022},
            {"title": "Original mathematical model for enzyme kinetics", "year": 1985},
            {"title": "Seminal landmark discovery of reperfusion injury", "cited_by_count": 500, "year": 2010},
            {"title": "State-of-the-art therapeutic trial in acute ischemia", "year": 2024},
            {"title": "Standard bioassay protocol for tetrazolium dye reduction", "study_design": "Methodology", "year": 2015},
            {"title": "Peptide X showed no significant effect in heart failure models", "year": 2023},
            {"title": "Exploratory pilot investigation of peptide analogs", "year": 2020}
        ]

        categories = [SeedPaperDiscoveryEngine.categorize_seed_paper(p) for p in papers]
        self.assertEqual(categories[0], "SYSTEMATIC_REVIEW_META_ANALYSIS")
        self.assertEqual(categories[1], "CLINICAL_PRACTICE_GUIDELINE")
        self.assertEqual(categories[2], "HISTORICAL_LANDMARK")
        self.assertEqual(categories[3], "HIGHLY_CITED_FOUNDATIONAL")
        self.assertEqual(categories[4], "RECENT_HIGH_IMPACT")
        self.assertEqual(categories[5], "KEY_METHODOLOGICAL")
        self.assertEqual(categories[6], "CONTRADICTORY_NULL_RESULT")
        self.assertEqual(categories[7], "EXPLORATORY_ANCHOR")

    def test_seed_papers_not_automatically_final_references(self):
        """Enforces that candidate seed papers must undergo screening and are NOT automatic inclusions."""
        seed = {"doi": "10.1000/seed1", "title": "Seed paper anchor", "year": 2022}
        registered = SeedPaperDiscoveryEngine.register_seed(seed)
        self.assertTrue(registered["is_seed_paper"])
        self.assertEqual(registered["final_portfolio_eligibility"], "REQUIRES_SCREENING")
        self.assertIn("must undergo relevance and eligibility screening", registered["status_note"])

    # =========================================================================
    # 4. MULTI-DIMENSIONAL SATURATION & FALSE SATURATION GUARD
    # =========================================================================

    def test_multi_dimensional_saturation_diminishing_returns(self):
        """Tests EvidenceBasedSaturationTracker across 7 dimensions under diminishing marginal returns."""
        # 4 successive batches where new unique records drop significantly
        batches = [
            {
                "database": "PubMed",
                "status": "EXECUTED",
                "records": [
                    {"doi": f"10.1000/rec_{i}", "entity": "Peptide X", "primary_endpoint": "Viability"}
                    for i in range(1, 20)
                ]
            },
            {
                "database": "Europe PMC",
                "status": "EXECUTED",
                "records": [
                    {"doi": f"10.1000/rec_{i}", "entity": "Peptide X", "primary_endpoint": "Apoptosis"}
                    for i in range(15, 25)  # 5 new
                ]
            },
            {
                "database": "OpenAlex",
                "status": "EXECUTED",
                "records": [
                    {"doi": f"10.1000/rec_{i}", "entity": "Peptide X", "primary_endpoint": "Viability"}
                    for i in range(20, 26)  # 1 new
                ]
            },
            {
                "database": "Crossref",
                "status": "EXECUTED",
                "records": [
                    {"doi": f"10.1000/rec_{i}", "entity": "Peptide X", "primary_endpoint": "Viability"}
                    for i in range(22, 27)  # 1 new out of 5 -> marginal yield 0.20 or less
                ]
            }
        ]

        report = EvidenceBasedSaturationTracker.evaluate_saturation(batches, min_batches_required=3, saturation_threshold=0.25)
        self.assertEqual(report["false_saturation_guard"], "PASSED")
        self.assertIn(report["saturation_status"], ["SATURATED", "EXPANDING"])
        self.assertGreaterEqual(report["total_unique_records"], 20)
        self.assertIn("RECORD_NOVELTY", report["dimension_assessments"])
        self.assertIn("ENTITY_NOVELTY", report["dimension_assessments"])

    def test_false_saturation_guard_triggered_on_errors(self):
        """Enforces that empty/failed search batches trigger FALSE_SATURATION_GUARD and do NOT claim saturation."""
        batches = [
            {"database": "PubMed", "status": "EXECUTED", "records": [{"doi": "10.1000/1"}]},
            {"database": "Europe PMC", "status": "ERROR", "records": []},
            {"database": "OpenAlex", "status": "NOT_EXECUTED", "records": []}
        ]
        report = EvidenceBasedSaturationTracker.evaluate_saturation(batches, min_batches_required=3)
        self.assertEqual(report["saturation_status"], "FALSE_SATURATION_GUARD_TRIGGERED")
        self.assertFalse(report["is_saturated"])

    # =========================================================================
    # 5. DATABASE DIVERSITY METRICS
    # =========================================================================

    def test_database_diversity_computation(self):
        """Tests per-database queries, retrieval, unique contribution, and portfolio diversity."""
        search_log = [
            {"database": "PubMed", "hits_retrieved": 10},
            {"database": "Europe PMC", "hits_retrieved": 8},
            {"database": "OpenAlex", "hits_retrieved": 6},
            {"database": "Crossref", "hits_retrieved": 5}
        ]
        unique_recs = [
            {"doi": "10.1/1", "retrieval_sources": ["PubMed"]},
            {"doi": "10.1/2", "retrieval_sources": ["Europe PMC", "PubMed"]},
            {"doi": "10.1/3", "retrieval_sources": ["OpenAlex"]},
            {"doi": "10.1/4", "retrieval_sources": ["Crossref"]}
        ]
        selected_refs = [
            {"doi": "10.1/1", "retrieval_sources": ["PubMed"]},
            {"doi": "10.1/3", "retrieval_sources": ["OpenAlex"]}
        ]

        diversity = ScientificSearchAdapter.compute_database_diversity(
            search_log=search_log,
            unique_records=unique_recs,
            selected_references=selected_refs
        )

        self.assertEqual(diversity["active_databases_count"], 4)
        self.assertEqual(diversity["database_diversity_score"], 1.0)
        self.assertEqual(diversity["per_database_metrics"]["PubMed"]["records_returned"], 10)
        self.assertEqual(diversity["per_database_metrics"]["PubMed"]["selected_final"], 1)

    # =========================================================================
    # 6. STRUCTURED PAPER READER (18 FIELDS ACROSS 4 TRACKS)
    # =========================================================================

    def test_structured_paper_reader_tracks(self):
        """Tests reading track classification across the 4 specialized tracks."""
        rec_clinical = {"title": "Randomized placebo-controlled trial in 150 patients with myocardial infarction"}
        rec_comp = {"title": "Deep learning in silico pipeline for molecular dynamics screening"}
        rec_exp = {"title": "In vitro cellular viability and cytotoxicity assays in cardiomyocyte cell culture"}
        rec_hybrid = {"title": "Computational docking followed by in vitro experimental validation"}

        self.assertEqual(StructuredPaperReader.classify_reading_track(rec_clinical), "CLINICAL_EPIDEMIOLOGY")
        self.assertEqual(StructuredPaperReader.classify_reading_track(rec_comp), "COMPUTATIONAL_BIOINFORMATICS")
        self.assertEqual(StructuredPaperReader.classify_reading_track(rec_exp), "BASIC_EXPERIMENTAL")
        self.assertEqual(StructuredPaperReader.classify_reading_track(rec_hybrid), "HYBRID")

    def test_structured_paper_reader_18_fields_and_regex(self):
        """Tests deterministic extraction of all 18 structured fields including quantitative regexes."""
        sample_paper = {
            "title": "Cardioprotective peptide X promotes cell survival and inhibits apoptosis in H9c2 cardiomyocytes",
            "abstract": "In vitro study evaluating peptide X at 25 μM compared with vehicle control. Sample size of 12 biological replicates (n=12) demonstrated 65% inhibition of apoptosis (p < 0.01) with IC50 = 14.5 μM."
        }
        reading = StructuredPaperReader.read_paper(sample_paper)

        # Verify all 18 fields exist
        expected_fields = [
            "reading_track", "intervention_identity", "intervention_dose_or_exposure",
            "comparator_control", "biological_model", "cell_line_or_strain",
            "sample_size", "primary_endpoint", "assay_technique",
            "observed_quantitative_effect", "effect_direction", "statistical_significance",
            "adverse_or_offtarget_effects", "methodological_limitations",
            "funding_or_coi_declared", "study_design_type",
            "reproducibility_parameters", "raw_text_provenance"
        ]
        for field in expected_fields:
            self.assertIn(field, reading, f"Missing field: {field}")

        # Verify quantitative regex extraction
        self.assertEqual(reading["sample_size"], 12)
        self.assertIn("65%", reading["observed_quantitative_effect"])
        self.assertEqual(reading["effect_direction"], "DECREASED")
        self.assertIn("p < 0.01", reading["statistical_significance"])
        self.assertIn("25 μM", reading["intervention_dose_or_exposure"])
        self.assertEqual(reading["comparator_control"], "Vehicle control")

    # =========================================================================
    # 7. CITATION DRIFT DETECTION & PAPER-TO-CLAIM VERIFICATION
    # =========================================================================

    def test_citation_drift_overstatement(self):
        """Detects OVERSTATEMENT when in vitro study is cited as clinical trial efficacy in humans."""
        paper = {
            "title": "In vitro evaluation of peptide X in cardiomyocyte cell lines",
            "abstract": "Monolayer cell culture assays demonstrated reduced caspase-3."
        }
        claim = {
            "claim_text": "Peptide X has proven clinical efficacy in human patients suffering from acute infarction.",
            "entity": "Peptide X",
            "model": "human patients"
        }
        audit = PaperToClaimVerifier.verify_claim(claim, paper)
        self.assertEqual(audit["drift_type"], "OVERSTATEMENT")
        self.assertEqual(audit["verification_verdict"], "CONDITIONAL_SUPPORT")
        self.assertTrue(any("clinical" in r for r in audit["drift_reasons"]))

    def test_citation_drift_passing_mention(self):
        """Detects CITATION_DRIFT when cited paper never tested the claimed entity."""
        paper = {
            "title": "Evaluation of ischemic preconditioning in rat hearts",
            "abstract": "Preconditioning protocols improved mitochondrial function."
        }
        claim = {
            "claim_text": "Peptide X significantly prevents ischemic injury.",
            "entity": "peptide x"
        }
        audit = PaperToClaimVerifier.verify_claim(claim, paper)
        self.assertEqual(audit["drift_type"], "CITATION_DRIFT")
        self.assertEqual(audit["verification_verdict"], "DRIFT_DETECTED")

    def test_citation_drift_context_mismatch(self):
        """Detects CONTEXT_MISMATCH when organ/tissue systems are mismatched without analogy."""
        paper = {
            "title": "Effects of peptide X on dermal fibroblast wound healing in skin",
            "abstract": "Assays in skin keratinocytes demonstrated accelerated closure."
        }
        claim = {
            "claim_text": "Peptide X suppresses renal fibrosis.",
            "entity": "peptide x",
            "model": "renal tissue"
        }
        audit = PaperToClaimVerifier.verify_claim(claim, paper)
        self.assertEqual(audit["drift_type"], "CONTEXT_MISMATCH")
        self.assertEqual(audit["verification_verdict"], "DRIFT_DETECTED")

    def test_citation_drift_correlation_to_causation(self):
        """Detects CORRELATION_TO_CAUSATION when observational studies are cited as mechanistic cause."""
        paper = {
            "title": "Cross-sectional cohort association between peptide levels and cardiovascular risk",
            "study_design": "Observational cross-sectional study"
        }
        claim = {
            "claim_text": "Peptide X mechanistically drives cardioprotection and causes infarct shrinkage.",
            "entity": "peptide",
            "is_causal": True
        }
        audit = PaperToClaimVerifier.verify_claim(claim, paper)
        self.assertEqual(audit["drift_type"], "CORRELATION_TO_CAUSATION")
        self.assertEqual(audit["verification_verdict"], "CONDITIONAL_SUPPORT")

    def test_citation_drift_selective_citation(self):
        """Detects SELECTIVE_CITATION when negative/null results are cited as positive evidence."""
        paper = {
            "title": "Peptide X was inert and had no effect on cardiomyocyte apoptosis",
            "abstract": "Peptide X treatment showed no significant difference compared to vehicle control."
        }
        claim = {
            "claim_text": "Peptide X significantly inhibits apoptotic cell death.",
            "entity": "peptide x"
        }
        audit = PaperToClaimVerifier.verify_claim(claim, paper)
        self.assertEqual(audit["drift_type"], "SELECTIVE_CITATION")
        self.assertEqual(audit["verification_verdict"], "DRIFT_DETECTED")

    def test_citation_drift_no_drift_valid_support(self):
        """Validates NO_DRIFT when claim conservatively matches empirical findings."""
        paper = {
            "title": "Peptide X reduces hypoxia-induced death in H9c2 cardiomyocytes",
            "abstract": "In vitro MTT assays showed 45% viability recovery."
        }
        claim = {
            "claim_text": "Peptide X reduces hypoxia-induced cell death in in vitro cardiomyocyte cultures.",
            "entity": "peptide x",
            "model": "in vitro cardiomyocyte"
        }
        audit = PaperToClaimVerifier.verify_claim(claim, paper)
        self.assertEqual(audit["drift_type"], "NO_DRIFT")
        self.assertEqual(audit["verification_verdict"], "VALID_SUPPORT")

    # =========================================================================
    # 8. ENHANCED TRIPLE-CHECK DEDUPLICATION
    # =========================================================================

    def test_enhanced_duplicate_detection(self):
        """Tests DOI, PMID, and fuzzy normalized title deduplication."""
        rec1 = {"doi": "https://doi.org/10.1016/j.cardio.2023.01", "pmid": "12345", "title": "Cardioprotection by Peptide X", "year": 2023}
        rec2 = {"doi": "10.1016/J.CARDIO.2023.01", "title": "Cardioprotection by Peptide X", "year": 2023}
        is_dup, reason = GenericReferenceAuditor.detect_duplicate_pair(rec1, rec2)
        self.assertTrue(is_dup)
        self.assertEqual(reason, "IDENTICAL_DOI")

        # Fuzzy title with year match
        rec3 = {"title": "Cardioprotection by Peptide X in Ischemia-Reperfusion", "year": 2023}
        rec4 = {"title": "Cardioprotection by Peptide X in Ischemia Reperfusion", "year": 2023}
        is_dup2, reason2 = GenericReferenceAuditor.detect_duplicate_pair(rec3, rec4)
        self.assertTrue(is_dup2)
        self.assertEqual(reason2, "FUZZY_TITLE_MATCH")

        # Distinct DOIs
        rec5 = {"doi": "10.1016/j.cardio.2023.01"}
        rec6 = {"doi": "10.1016/j.cardio.2023.99"}
        is_dup3, reason3 = GenericReferenceAuditor.detect_duplicate_pair(rec5, rec6)
        self.assertFalse(is_dup3)
        self.assertEqual(reason3, "DISTINCT_DOIS")

    # =========================================================================
    # 9. 3-TIER CONTRADICTION EXPLANATION PARTITIONING
    # =========================================================================

    def test_contradiction_3_tier_explanation(self):
        """Verifies contradiction engine partitions explanations into 3 distinct scientific tiers."""
        study_a = {
            "study_id": "STUDY_A",
            "context_parameters": {"dose": "10 uM", "exposure_time": "24h"}
        }
        study_b = {
            "study_id": "STUDY_B",
            "context_parameters": {"dose": "50 uM", "exposure_time": "72h"}
        }

        # Dose discrepancy gives DEMONSTRATED_EXPLANATION
        engine = GenericContradictionEngine()
        disc = engine.analyze_discrepancy(study_a, study_b)
        self.assertEqual(disc["explanation_level"], "DEMONSTRATED_EXPLANATION")
        self.assertIsNotNone(disc["demonstrated_explanation"])

        # Identical parameters with unexplained divergence gives UNRESOLVED_UNCERTAINTY
        study_c = {
            "study_id": "STUDY_C",
            "context_parameters": {"dose": "10 uM", "exposure_time": "24h"}
        }
        disc_unresolved = engine.analyze_discrepancy(study_a, study_c)
        self.assertEqual(disc_unresolved["explanation_level"], "UNRESOLVED_UNCERTAINTY")
        self.assertIsNotNone(disc_unresolved["unresolved_uncertainty"])

    # =========================================================================
    # 10. REPRODUCIBLE RESEARCH RUN MANIFEST
    # =========================================================================

    def test_research_run_manifest_generation(self):
        """Tests generation of complete reproducible manifest with SHA-256 checksum."""
        manifest = ResearchRunManifest.generate_manifest(
            problem_model=self.problem_model,
            execution_mode="OFFLINE_TEST",
            query_families=[{"family": "EXACT_CONCEPT_COMBINATION", "query": "Peptide X AND Ischemia"}],
            seed_papers=[{"doi": "10.1000/seed1", "title": "Seed paper 1", "seed_category": "RECENT_HIGH_IMPACT"}],
            chasing_summary={"total_candidates_discovered": 5},
            database_diversity={"database_diversity_score": 1.0},
            saturation_summary={"saturation_status": "SATURATED"},
            screening_funnel={"total_retrieved": 50, "final_eligible": 20},
            selected_references=[
                {
                    "citation_number": 1,
                    "doi": "10.1000/ref1",
                    "title": "Selected paper",
                    "year": 2023,
                    "final_inclusion_reason": "DIRECT_PRIMARY_EVIDENCE",
                    "evidence_role": "DIRECT_PRIMARY"
                }
            ],
            engine_version="8.5.0"
        )

        self.assertEqual(manifest["engine_version"], "8.5.0")
        self.assertEqual(manifest["manifest_type"], "RESEARCH_RUN_MANIFEST")
        self.assertEqual(len(manifest["seed_papers"]), 1)
        self.assertEqual(manifest["final_portfolio_count"], 1)
        self.assertTrue(len(manifest["reproducibility_checksum"]) == 64)  # Valid SHA-256

    # =========================================================================
    # 11. INVARIANT PRESERVATION (<= 25 REFS, NO QUOTA-FILLING)
    # =========================================================================

    def test_invariants_preserved(self):
        """Enforces MAX_FINAL_REFERENCES == 25 and NO_QUOTA_FILLING == True invariants."""
        self.assertEqual(MAX_FINAL_REFERENCES, 25)
        self.assertTrue(NO_QUOTA_FILLING)
        self.assertEqual(MIN_FINAL_REFERENCES, 15)


if __name__ == "__main__":
    unittest.main()
