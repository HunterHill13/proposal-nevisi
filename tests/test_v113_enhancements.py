#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_v113_enhancements.py - Rigorous Verification Suite for v11.3 Enhancements:
1. MeSH Query Expander: Two-tier cascaded search logic (MeSH Precision vs Free-Text Fallback).
2. PICO/PECO Matrix: Structural presence in Section 15 without altering canonical 28 sections.
3. Multi-Model Power Calculations: Study-design specific formulas (ARRIVE/Festing, NIH in vitro, Chow clinical).
"""

import os
import sys
import unittest

TESTS_DIR = os.path.dirname(__file__)
SCRIPTS_DIR = os.path.abspath(os.path.join(TESTS_DIR, "..", "scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from mesh_query_expander import MeSHQueryExpander
from generate_compliant_proposal import ProposalGenerator
from methodology_completeness_gate import MethodologyCompletenessGate

class TestV113Enhancements(unittest.TestCase):
    """Verifies MeSH expansion, PICO structural fidelity, and sample size rigor."""

    def test_mesh_tier1_precision_query(self):
        """Tier 1 creates structured Boolean query with [MeSH Terms] and [Title/Abstract]."""
        topic = "بررسی اثر هم‌افزایی متفورمین بر آپوپتوز سلول‌های سرطانی کولورکتال"
        q = MeSHQueryExpander.build_tier1_precision_mesh_query(topic, ["metformin"])
        self.assertIn("Colorectal Neoplasms", q)
        self.assertIn("[MeSH Terms]", q)
        self.assertIn("Apoptosis", q)
        self.assertIn("metformin", q)

    def test_mesh_tier2_fallback_query(self):
        """Tier 2 fallback produces clean free-text keywords for high recall."""
        topic = "بررسی آپوپتوز و اتوفاژی در بیماری آلزایمر"
        q = MeSHQueryExpander.build_tier2_fallback_query(topic)
        self.assertTrue(len(q) > 10)
        self.assertIn("Alzheimer", q)
        self.assertIn("Apoptosis", q)

    def test_pico_peco_matrix_in_section_15(self):
        """Section 15 contains PECO/PICO markdown table while keeping canonical 28-section numbering intact."""
        sample_data = {
            "title_fa": "مطالعه مداخله فرضی در رده سلولی HCT116",
            "title_en": "Hypothetical Intervention Study in HCT116",
            "framework": "EXPERIMENTAL_IN_VITRO",
            "research_problem_model": {
                "framework": "EXPERIMENTAL_IN_VITRO",
                "target_condition": {"name_fa": "سرطان کولون", "name_en": "Colorectal Neoplasms"},
                "population_or_model": {"primary_system": "رده سلولی HCT116"},
                "interventions_or_exposures": [{"name": "ترکیب فرضی A"}],
                "primary_outcomes": [{"name": "زیست‌پذیری سلولی"}, {"name": "درصد آپوپتوز"}]
            }
        }
        md = ProposalGenerator.assemble_pajooheshyar_28(sample_data)
        
        # Verify Section 15 header is preserved
        self.assertIn("## ۱۵. جامعه مورد مطالعه", md)
        self.assertIn("PECO Framework", md)
        self.assertIn("| **P (سیستم سلولی / مدل بیولوژیک (Population/Model))** |", md)
        self.assertIn("| **O (پیامدهای مولکولی و آپوپتوز (Outcomes))** |", md)

        # Validate gate still passes 100%
        gate_res = MethodologyCompletenessGate.validate(md)
        self.assertTrue(gate_res.is_complete)
        self.assertEqual(gate_res.compliance_score, 100.0)

    def test_sample_size_formula_study_diversity(self):
        """Section 22 generates design-tailored formulas with authoritative citations."""
        # 1. Animal In Vivo -> Festing (2002) & ARRIVE
        animal_data = {
            "title_fa": "مطالعه حیوانی اثر محافظتی ترکیب X",
            "framework": "EXPERIMENTAL_ANIMAL",
            "research_problem_model": {
                "framework": "EXPERIMENTAL_ANIMAL",
                "population_or_model": {"primary_system": "رت‌های نژاد ویستار"}
            }
        }
        animal_md = ProposalGenerator.assemble_pajooheshyar_28(animal_data)
        self.assertIn("ARRIVE Guidelines", animal_md)
        self.assertIn("Festing", animal_md)
        self.assertIn("E = N - B - T", animal_md)

        # 2. Clinical Human -> Chow et al. (2017)
        clinical_data = {
            "title_fa": "کارآزمایی بالینی مداخله Y در بیماران دیابتی",
            "framework": "PICO",
            "research_problem_model": {
                "framework": "PICO",
                "population_or_model": {"primary_system": "بیماران مبتلا به دیابت نوع ۲"}
            }
        }
        clinical_md = ProposalGenerator.assemble_pajooheshyar_28(clinical_data)
        self.assertIn("Chow", clinical_md)
        self.assertIn(r"\Delta^2", clinical_md)
        self.assertIn("MCID", clinical_md)

        # 3. In Vitro Cellular -> NIH Reproducibility Guidelines
        cell_data = {
            "title_fa": "مطالعه آزمایشگاهی سمیت سلولی ترکیب Z",
            "framework": "EXPERIMENTAL_IN_VITRO",
            "research_problem_model": {
                "framework": "EXPERIMENTAL_IN_VITRO",
                "population_or_model": {"primary_system": "سلول‌های کشت اولیه"}
            }
        }
        cell_md = ProposalGenerator.assemble_pajooheshyar_28(cell_data)
        self.assertIn("NIH Notice NOT-OD-15-103", cell_md)
        self.assertIn("Pseudo-Replication", cell_md)

    def test_baseline_paper_quality_auditor_and_section_3_rob_table(self):
        """BaselinePaperQualityAuditor evaluates papers and renders markdown matrix table in Section 3."""
        from pre_emptive_risk_of_bias_mitigator import BaselinePaperQualityAuditor
        from proposal_research_dossier import ProposalResearchDossier

        papers = [
            {
                "pmid": "31111111",
                "doi": "10.1016/j.biopha.2021.01",
                "title": "Randomized double-blind evaluation of compound against baseline control with triplicate runs",
                "abstract": "We conducted a randomized double-blind trial. Vehicle control was used. Results showed p < 0.01 in triplicate experiments.",
                "passages": ["Assays performed in independent triplicate with vehicle control."]
            },
            {
                "pmid": "32222222",
                "doi": "10.1016/j.biopha.2021.02",
                "title": "Preliminary brief observation report",
                "abstract": "Brief notes recorded under laboratory observation.",
                "passages": []
            }
        ]

        # 1. Direct Auditor test
        evals = BaselinePaperQualityAuditor.evaluate_corpus(papers)
        self.assertEqual(len(evals), 2)
        self.assertEqual(evals[0]["domains"]["d1_randomization"], "LOW_RISK")
        self.assertEqual(evals[0]["domains"]["d2_blinding"], "LOW_RISK")
        self.assertEqual(evals[0]["domains"]["d3_controls_rigor"], "LOW_RISK")
        self.assertEqual(evals[0]["overall_rob"], "LOW_RISK")
        self.assertEqual(evals[1]["overall_rob"], "HIGH_RISK")

        tbl = BaselinePaperQualityAuditor.render_markdown_table(evals)
        self.assertIn("ریسک کلی سوگیری", tbl)
        self.assertIn("31111111", tbl)

        # 2. Dossier Integration test
        dossier = ProposalResearchDossier(topic="تست سوگیری")
        for p in papers:
            dossier.add_evidence_paper(
                pmid=p["pmid"],
                doi=p["doi"],
                title=p["title"],
                authors=["Author X"],
                year=2021,
                is_full_text=True,
                verified=True,
                passages=p["passages"]
            )
        rob_dossier = dossier.audit_baseline_literature_quality()
        self.assertEqual(len(rob_dossier), 2)
        dossier_dict = dossier.to_dict()
        self.assertIn("literature_rob_evaluations", dossier_dict)

        # 3. Section 3 Integration in generated proposal
        prop_data = {
            "title_fa": "طرح آزمایشی",
            "studies": papers,
            "research_problem_model": {
                "target_condition": {"name_fa": "بیماری هدف", "name_en": "Disease Target"},
                "population_or_model": {"primary_system": "مدل هدف"},
                "interventions_or_exposures": [{"name": "ترکیب T"}]
            }
        }
        prop_md = ProposalGenerator.assemble_pajooheshyar_28(prop_data)
        self.assertIn("Baseline Literature Risk of Bias Audit", prop_md)
        self.assertIn("31111111", prop_md)

    def test_pipeline_filters_off_topic_candidates(self):
        """Pipeline filters out irrelevant or biologically incompatible papers using GenericReferenceAuditor."""
        from generic_reference_auditor import GenericReferenceAuditor

        candidate_records = [
            {
                "pmid": "99999991",
                "doi": "10.1000/vet1",
                "title": "Bovine mastitis in dairy cattle herd lactation",
                "abstract": "Investigation of dairy cows milk yield and udder infections in veterinary agriculture.",
                "year": 2023
            },
            {
                "pmid": "99999992",
                "doi": "10.1000/cancer1",
                "title": "Therapeutic compound induces apoptotic death in cancer cells",
                "abstract": "Treatment inhibited growth and induced cell apoptosis in experimental model with p < 0.01.",
                "year": 2023
            }
        ]
        problem_model = {
            "domain": "oncology",
            "target_condition": {"name_en": "cancer", "name_fa": "سرطان"},
            "population_or_model": {"primary_system": "cancer cells"},
            "interventions_or_exposures": [{"name": "compound"}]
        }

        sel_res = GenericReferenceAuditor.select_optimal_proposal_references(
            candidate_records=candidate_records,
            problem_model=problem_model,
            max_references=10,
            min_references=1,
            no_quota_filling=False
        )

        selected_pmids = [s.get("pmid") for s in sel_res["selected_references"]]
        self.assertNotIn("99999991", selected_pmids, "Off-topic veterinary paper must be strictly rejected")
        self.assertIn("99999992", selected_pmids, "On-topic target paper must be selected")
        
        # Verify exclusion recorded in funnel
        excluded_ids = [e.get("ref_id") for e in sel_res.get("excluded_candidates", [])]
        self.assertTrue(any("10.1000/vet1" in str(eid) or "mastitis" in str(eid).lower() for eid in excluded_ids))

    def test_section_2_evidence_argumentation_and_citations(self):
        """Section 2 synthesizes layered evidence-grounded problem statement with valid citations and research gaps."""
        studies = [
            {
                "citation_number": 1,
                "pmid": "31000001",
                "doi": "10.1000/sample1",
                "title": "Direct cellular efficacy of therapeutic compound",
                "authors": ["Author Alpha", "Author Beta"],
                "year": 2022,
                "evidence_role": "DIRECT_EVIDENCE",
                "final_inclusion_reason": "INTERVENTION_EFFICACY_EVIDENCE"
            },
            {
                "citation_number": 2,
                "pmid": "31000002",
                "doi": "10.1000/sample2",
                "title": "Molecular signaling and apoptotic pathway induction",
                "authors": ["Author Gamma"],
                "year": 2023,
                "evidence_role": "MECHANISTIC_EVIDENCE",
                "final_inclusion_reason": "MECHANISTIC_RATIONALE"
            }
        ]
        prop_data = {
            "title_fa": "بررسی اثر درمانی مداخله تجربی در مدل بیماری",
            "title_en": "Evaluation of experimental intervention in disease model",
            "studies": studies,
            "research_problem_model": {
                "domain": "oncology",
                "target_condition": {"name_fa": "بیماری هدف", "name_en": "Target Disease"},
                "population_or_model": {"primary_system": "سلول‌های هدف"},
                "interventions_or_exposures": [{"name": "مداخله زیستی Alpha"}]
            }
        }
        md = ProposalGenerator.assemble_pajooheshyar_28(prop_data)

        # 1. Section 2 presence and citations
        self.assertIn("## ۲. بیان مسئله", md)
        self.assertIn("[1]", md)
        self.assertIn("شکاف‌های پژوهشی شناسایی‌شده", md)

        # 2. Section 28 presence and synchronization
        self.assertIn("## ۲۸. منابعی که استفاده شد", md)
        self.assertIn("[1] Author Alpha", md)
        self.assertIn("[2] Author Gamma", md)

        # 3. PostResearchCitationAuditor validates citation integrity
        from generic_reference_auditor import PostResearchCitationAuditor
        cite_audit = PostResearchCitationAuditor.audit_proposal_citations(md, studies)
        self.assertEqual(cite_audit["unresolved_placeholders_count"], 0)
        self.assertEqual(cite_audit["total_citations_in_text"], 2)


if __name__ == "__main__":
    unittest.main()
