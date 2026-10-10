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

if __name__ == "__main__":
    unittest.main()
