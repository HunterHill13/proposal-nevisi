#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_v121_multidomain_polymorphism.py - Unit & Integration Tests for Domain Polymorphism v12.1
Proposal-Nevisi v12.1

Verifies that non-laboratory research topics (Health Systems, Health Policy,
Health Economics [CHE/OOP], Observational Epidemiology, Clinical Trials):
1. Are correctly identified by MethodologyResearchSubagent.
2. Derive cohesive, domain-appropriate protocols (Cochran formula, survey tools,
   HIS verification, Stata/R, multivariable logistic regression, Kakwani index)
   WITHOUT hardcoded cell culture, MTT/CCK-8, or apoptosis assays.
3. BiomedicalConceptGraph extracts CHE, OOP, ICER, QALY, OR, RR, HR metrics
   and health economics relations (EVALUATES_BURDEN, COST_EFFECTIVE_FOR).
4. MasterResearchPipeline auto-detects non-lab topics and generates compliant
   research problem models and canonical proposal sections.
"""

import os
import sys
import unittest
import tempfile
import json

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.abspath(os.path.join(TESTS_DIR, "..", "scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from methodology_research_subagent import MethodologyResearchSubagent
from biomedical_concept_graph import BiomedicalConceptGraph
from run_research_pipeline import MasterResearchPipeline
from generate_compliant_proposal import CompliantProposalGenerator


class TestV121MultiDomainPolymorphism(unittest.TestCase):
    """Test suite for domain-polymorphic multi-archetype support."""

    def test_01_archetype_identification(self):
        """Verifies accurate archetype detection across 6 study domains."""
        # 1. Health Systems / Health Economics
        t_che = "بررسی هزینه‌های کمرشکن سلامت (CHE) و پرداخت از جیب (OOP) در بیماران مبتلا به سرطان در ایران"
        self.assertEqual(
            MethodologyResearchSubagent.identify_study_archetype(t_che),
            "HEALTH_SYSTEMS_AND_HEALTH_POLICY"
        )

        # 2. Observational Epidemiology
        t_epi = "بررسی مقطعی شیوع عوامل خطر بیماری‌های قلبی عروقی در جامعه شهری"
        self.assertEqual(
            MethodologyResearchSubagent.identify_study_archetype(t_epi),
            "EPIDEMIOLOGICAL_OBSERVATIONAL"
        )

        # 3. Clinical Trial
        t_rct = "کارآزمایی بالینی تصادفی دو سو کور فاز ۳ جهت مقایسه اثربخشی داروی الف با دارونما در بیماران"
        self.assertEqual(
            MethodologyResearchSubagent.identify_study_archetype(t_rct),
            "CLINICAL_TRIAL_OR_COHORT"
        )

        # 4. In Vivo Animal Model
        t_vivo = "بررسی اثر محافظتی عصبی ترکیب الف در موش‌های مدل بیماری پارکینسون"
        self.assertEqual(
            MethodologyResearchSubagent.identify_study_archetype(t_vivo),
            "IN_VIVO_ANIMAL_MODEL"
        )

        # 5. In Vitro Cellular Combination
        t_vitro = "ارزیابی هم‌افزایی فارماکولوژیک لوپئول و داروی سیس‌پلاتین در رده سلولی A549"
        self.assertEqual(
            MethodologyResearchSubagent.identify_study_archetype(t_vitro),
            "IN_VIVO_ANIMAL_MODEL" if "موش" in t_vitro else "IN_VITRO_CELLULAR_COMBINATION"
        )

    def test_02_health_systems_cohesive_protocol(self):
        """Verifies MethodologyResearchSubagent derives a pure health economics protocol."""
        res = MethodologyResearchSubagent.derive_cohesive_protocol(
            topic="بررسی هزینه‌های کمرشکن سلامت (CHE) و پرداخت از جیب (OOP) در بیماران سرطانی",
            target_model="بیماران مبتلا به سرطان و خانوارهای تحت تکفل",
            interventions=["هزینه‌های کمرشکن سلامت (CHE)", "پرداخت از جیب (OOP)"]
        )

        self.assertEqual(res.archetype, "HEALTH_SYSTEMS_AND_HEALTH_POLICY")
        self.assertEqual(res.coherence_score, 1.0)

        sec22 = res.formatted_sections_fa[22]
        self.assertIn("Cochran's Formula", res.sample_size_biostatistics["sample_size_formula_name"])
        self.assertIn("فرمول کوکران", sec22)
        self.assertIn("DEFF = 1.5", sec22)
        self.assertIn("642", sec22)
        self.assertNotIn("Mead's Resource Equation", sec22)
        self.assertNotIn("n = 3 Biological Replicates", sec22)

        sec23 = res.formatted_sections_fa[23]
        self.assertIn("رگرسیون لجستیک چندمتغیره", sec23)
        self.assertIn("شاخص تمرکز", sec23)
        self.assertIn("Stata", sec23)
        self.assertNotIn("Two-Way Factorial ANOVA", sec23)
        self.assertNotIn("CompuSyn", sec23)

        sec27 = res.formatted_sections_fa[27]
        self.assertIn("پرسشنامه استاندارد سلامت جهانی (WHO WHS)", sec27)
        self.assertIn("سامانه اطلاعات بیمارستانی (HIS)", sec27)
        self.assertNotIn("MTT", sec27)
        self.assertNotIn("فلوسایتومتری", sec27)

    def test_03_concept_graph_health_systems_metrics_extraction(self):
        """Verifies BiomedicalConceptGraph extracts CHE, OOP, ICER, and QALY metrics."""
        cg = BiomedicalConceptGraph(topic_context="Catastrophic Health Expenditures in Cancer")
        abstract_text = (
            "In this study of cancer patients, the incidence of catastrophic health expenditure CHE reached 28.5% "
            "at the 40% capacity to pay threshold. Out-of-pocket OOP health expenditures accounted for 48.2% of total costs. "
            "Multivariable analysis revealed that lack of supplementary insurance was significantly associated with higher risk of CHE "
            "with an odds ratio OR: 2.85 (95% CI: 1.45-5.60). Inpatient chemotherapy was a major driver that increased cost significantly. "
            "The incremental cost-effectiveness ratio ICER was $15,400/QALY, demonstrating favorable economic value."
        )

        claims = cg.ingest_paper_abstract(
            paper_id="PMID:41000001",
            title="Economic burden and catastrophic health expenditures among oncology patients",
            abstract=abstract_text
        )

        self.assertTrue(len(claims) >= 1)
        found_metrics = {}
        for r in cg.relationships:
            found_metrics.update(r.get("metrics", {}))

        self.assertIn("che_rate", found_metrics)
        self.assertEqual(found_metrics["che_rate"], "28.5%")
        self.assertIn("oop_rate", found_metrics)
        self.assertEqual(found_metrics["oop_rate"], "48.2%")
        self.assertIn("odds_ratio", found_metrics)
        self.assertIn("2.85", found_metrics["odds_ratio"])
        self.assertIn("icer", found_metrics)
        self.assertIn("15,400/QALY", found_metrics["icer"])

    def test_04_concept_graph_health_systems_relations(self):
        """Verifies extraction of EVALUATES_BURDEN and COST_EFFECTIVE_FOR relation types."""
        cg = BiomedicalConceptGraph(topic_context="Health Systems Financial Protection")
        cg.register_entity("POLICY", "Universal_Health_Coverage")
        cg.register_entity("BURDEN", "Catastrophic_Expenditure")

        r = cg.add_relationship(
            source_id="POLICY:UNIVERSAL_HEALTH_COVERAGE",
            relation_type="EVALUATES_BURDEN",
            target_id="BURDEN:CATASTROPHIC_EXPENDITURE",
            supporting_paper_id="PMID:42000001",
            quantitative_metrics={"che_rate": "12.4%"}
        )
        self.assertEqual(r["relation"], "EVALUATES_BURDEN")
        self.assertIn("EVALUATES_BURDEN", BiomedicalConceptGraph.RELATION_TYPES)
        self.assertIn("COST_EFFECTIVE_FOR", BiomedicalConceptGraph.RELATION_TYPES)
        self.assertIn("INCREASES_COST", BiomedicalConceptGraph.RELATION_TYPES)

    def test_05_pipeline_auto_detects_health_systems_study_family(self):
        """Verifies MasterResearchPipeline auto-detects health_systems from topic string."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pipeline = MasterResearchPipeline(
                topic="بررسی هزینه‌های کمرشکن سلامت (CHE) و پرداخت از جیب (OOP) در بیماران مبتلا به سرطان در ایران",
                study_family="in_vitro",  # default parameter, should be auto-corrected!
                output_dir=tmpdir,
                mode="mock"
            )
            self.assertEqual(pipeline.study_family, "health_systems")

    def test_06_pipeline_builds_health_systems_problem_model(self):
        """Verifies research problem model synthesis for health systems."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pipeline = MasterResearchPipeline(
                topic="بررسی هزینه‌های کمرشکن سلامت (CHE) و پرداخت از جیب (OOP) در بیماران مبتلا به سرطان در ایران",
                study_family="health_systems",
                output_dir=tmpdir,
                mode="mock"
            )
            kw_info = pipeline.extract_keywords()
            rpm = pipeline.build_research_problem_model(kw_info)

            self.assertEqual(rpm["framework"], "HEALTH_SYSTEMS_AND_HEALTH_POLICY")
            self.assertEqual(rpm["domain"], "health_economics_and_policy")
            self.assertIn("جامعه خانوارها و بیماران", rpm["population_or_model"]["primary_system"])
            self.assertTrue(any("CHE" in o["name"] for o in rpm["primary_outcomes"]))
            self.assertTrue(any("OOP" in o["name"] for o in rpm["primary_outcomes"]))

    def test_07_proposal_generator_sections_22_and_23_health_systems(self):
        """Verifies Sections 22 and 23 in generated markdown contain Cochran formula and logistic regression."""
        cohesive_proto = MethodologyResearchSubagent.derive_cohesive_protocol(
            topic="بررسی هزینه‌های کمرشکن سلامت (CHE) و پرداخت از جیب (OOP) در بیماران مبتلا به سرطان",
            target_model="بیماران سرطانی و خانوارها"
        )
        data = {
            "title_fa": "بررسی هزینه‌های کمرشکن سلامت (CHE) و پرداخت از جیب (OOP) در بیماران مبتلا به سرطان",
            "framework": "HEALTH_SYSTEMS_AND_HEALTH_POLICY",
            "domain": "health_economics_and_policy",
            "cohesive_protocol": cohesive_proto.to_dict(),
            "target_condition": {"name_fa": "سرطان", "name_en": "Neoplasms"},
            "population_or_model": {"primary_system": "بیماران مبتلا به سرطان و خانوارها"},
            "interventions": [{"name": "CHE"}, {"name": "OOP"}],
            "primary_outcomes": [{"name": "شیوع CHE"}, {"name": "سهم OOP"}],
            "studies": []
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            md_path = os.path.join(tmpdir, "proposal.md")
            docx_path = os.path.join(tmpdir, "proposal.docx")

            md_content = CompliantProposalGenerator.assemble_pajooheshyar_28(data)
            self.assertIn("## ۲۲. حجم نمونه و روش محاسبه آن", md_content)
            self.assertIn("فرمول کوکران", md_content)
            self.assertIn("DEFF = 1.5", md_content)
            self.assertIn("642", md_content)
            self.assertNotIn("Mead's Resource Equation", md_content)

            self.assertIn("## ۲۳. روش تجزیه و تحلیل داده", md_content)
            self.assertIn("رگرسیون لجستیک چندمتغیره", md_content)
            self.assertIn("شاخص تمرکز", md_content)
            self.assertNotIn("CompuSyn", md_content)
            self.assertNotIn("Two-way Factorial ANOVA", md_content)

    def test_08_end_to_end_pipeline_health_systems(self):
        """Verifies full autonomous pipeline execution on health systems topic with all 4 graph artifacts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            spec_payload = {
                "topic": "بررسی هزینه‌های کمرشکن سلامت (CHE) و پرداخت از جیب (OOP) در بیماران مبتلا به سرطان در ایران",
                "keywords": ["CHE", "Out-of-Pocket", "Cancer", "Iran"],
                "studies": [
                    {
                        "pmid": "38111111",
                        "doi": "10.1000/healthpolicy.2024.1",
                        "title": "Catastrophic health expenditure and impoverishment in cancer patients",
                        "authors": ["Rezaei S", "Karami M"],
                        "year": 2024,
                        "journal": "BMC Health Serv Res",
                        "abstract": "Catastrophic health expenditures reached 28.5% at the 40% capacity to pay threshold with OOP accounting for 48.2% of total costs.",
                        "is_full_text": True,
                        "has_full_text": True,
                        "verified": True,
                        "farsi_synthesis_summary": "در مطالعه رضایی و همکاران (۲۰۲۴) شیوع CHE برابر با ۲۸.۵ درصد برآورد گردید."
                    }
                ]
            }
            spec_file = os.path.join(tmpdir, "PROPOSAL_SPEC.json")
            with open(spec_file, "w", encoding="utf-8") as f:
                json.dump(spec_payload, f, ensure_ascii=False)

            pipe = MasterResearchPipeline(
                topic="بررسی هزینه‌های کمرشکن سلامت (CHE) و پرداخت از جیب (OOP) در بیماران مبتلا به سرطان در ایران",
                output_dir=tmpdir,
                mode="offline",
                min_refs=1,
                max_refs=5,
                spec_path=spec_file
            )
            res = pipe.run()

            self.assertEqual(res["status"], "PASS")
            self.assertEqual(pipe.study_family, "health_systems")

            # Verify all 4 graph & audit artifacts exist
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "LITERATURE_CITATION_GRAPH.json")))
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "LITERATURE_CITATION_GRAPH.html")))
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "BIOMEDICAL_CONCEPT_GRAPH.json")))
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "claim_entailment_audit.json")))
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "proposal.md")))
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "proposal.docx")))

            with open(os.path.join(tmpdir, "proposal.md"), "r", encoding="utf-8") as f:
                md_text = f.read()

            self.assertIn("فرمول کوکران", md_text)
            self.assertIn("642", md_text)
            self.assertIn("رگرسیون لجستیک چندمتغیره", md_text)
            self.assertNotIn("CompuSyn", md_text)
            self.assertNotIn("سنجش زیست‌پذیری با آزمون متابولیک (MTT)", md_text)


if __name__ == "__main__":
    unittest.main()
