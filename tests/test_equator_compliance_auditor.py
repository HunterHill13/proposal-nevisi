#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_equator_compliance_auditor.py - Test Suite for EQUATOR Network & Biological Resource Authentication Auditor
Proposal-Nevisi Engine v10.1
"""

import os
import sys
import json
import unittest
import tempfile
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from equator_compliance_auditor import EquatorComplianceAuditor, EquatorAuditResult
from proposal_readiness_gate import ProposalReadinessGate


def get_sample_compliant_proposal() -> str:
    """Provides a synthetic 28-section proposal text compliant with EQUATOR GCCP and MIQE."""
    sections = [
        "## 1. موضوع\nبررسی برهم‌کنش فارماکولوژیک و بیان ژن آپوپتوز در رده‌های سلولی سرطان",
        "## 6. اهداف جزیی\n۱. سنجش بقای سلولی و viability\n۲. بررسی سطح بیان ژن Bax و Bcl-2 با Real-Time PCR (qPCR)",
        "## 13. روش اجرا\nطرح تجربی با کنترل منفی و کنترل حلال ناقل (Vehicle Control با غلظت DMSO کمتر از ۰.۱٪) اجرا می‌شود.",
        "## 14. نوع مطالعه\nمطالعه تجربی برون‌تن در شرایط کشت سلولی (In Vitro Experimental Study)",
        "## 15. جامعه مورد مطالعه\nرده سلولی سرطان روده بزرگ خریداری شده از بانک سلولی انستیتو پاستور ایران با شناسنامه معتبر.",
        "## 16. محل انجام مطالعه\nآزمایشگاه جامع تحقیقاتی دانشگاه علوم پزشکی",
        "## 17. معیار های ورود به مطالعه\n- احراز هویت ژنتیکی سلول‌ها با آنالیز پروفایل STR (Short Tandem Repeat).\n- تایید عدم آلودگی به مایکوپلاسما با آزمون PCR مایکوپلاسما.\n- استفاده از سلول‌ها در محدوده پاساژهای بین ۳ تا ۱۰.\n- مواد دارویی با خلوص آنالیتیکال استاندارد بالای ۹۵٪.",
        "## 19. ابزار های گردآوری اطلاعات\nدستگاه اسپکتروفتومتر نانودراپ، دستگاه Real-Time PCR و الایزا ریدر با تصحیح بلانک بدون سلول.",
        "## 20. تعیین اعتبار ابزار گردآوری\n- سنجش خلوص و سلامت RNA با نانودراپ (نسبت A260/A280 بین ۱.۸ تا ۲.۰) و شاخص سلامت RNA (RIN >= 7).\n- اعتبارسنجی پرایمرها با بلاست و تایید تک‌پیک بودن منحنی ذوب (Melting Curve) با کارایی تکثیر استاندارد ۹۰ الی ۱۱۰ درصد.\n- احراز هویت سلولی با تست STR.",
        "## 21. تعیین ابزار گردآوری\n- تامین کیت‌ها از کمپانی Sigma-Aldrich با کد کاتالوگ مشخص.\n- نرمال‌سازی داده‌های بیان ژن با استفاده از ژن مرجع داخلی GAPDH مطابق استاندارد MIQE.\n- اجرای آزمایش‌ها در ۳ تکرار بیولوژیک مستقل.",
        "## 22. حجم نمونه و روش محاسبه آن\nحجم نمونه با رابطه کوهن در ۳ تکرار بیولوژیک مستقل n=3 محاسبه گردید.",
        "## 23. روش تجزیه و تحلیل داده\nآنالیز آماری با Two-way ANOVA و کمی‌سازی نسبی بیان ژن با متد استاندارد لیواک 2^-DeltaDeltaCt انجام می‌پذیرد.",
        "## 24. ملاحظلات اخلاقی در صورت نیاز\nکد اخلاق سازمانی IR.MUMS.REC.1402.120 اخذ شده است.",
        "## 25. نحوه رعایت نکات امنیتی و حفاظت پروژه در صورت نیاز\nکار در سطح ایمنی زیستی ۲ (BSL-2) زیر هود لامینار با اتوکلاو پسماندها.",
        "## 26. مشکلات و محدودیت ها\nکنترل سمیت حلال DMSO در غلظت کمتر از ۰.۱٪ به عنوان راهکار مهار محدودیت مد نظر است.",
        "## 27. روش انجام طرح، شیوه اجرایی مراحل طرح و چگونگی جمع آوری اطلاعات\nپروتکل با گروه‌های کنترل منفی و شاهد حلال DMSO مطابق گایدلاین‌های بازتولیدپذیری اجرا خواهد شد."
    ]
    return "\n\n".join(sections)


class TestEquatorComplianceAuditor(unittest.TestCase):
    """Test suite for EQUATOR Network and Biological Resource Authentication."""

    def setUp(self):
        self.compliant_proposal = get_sample_compliant_proposal()

    def test_detect_applicable_guidelines(self):
        """Verifies multi-domain automatic guideline detection."""
        sections = EquatorComplianceAuditor.parse_sections(self.compliant_proposal)
        guidelines = EquatorComplianceAuditor.detect_applicable_guidelines(sections)
        
        self.assertIn("OECD_GCCP_CELL_CULTURE", guidelines)
        self.assertIn("MIQE_QPCR_STANDARDS", guidelines)
        self.assertIn("REAGENT_CHEMICAL_AUTHENTICATION", guidelines)

    def test_detect_animal_guidelines(self):
        """Verifies detection of ARRIVE 2.0 for in vivo animal studies."""
        animal_text = (
            "## 14. نوع مطالعه\nمطالعه تجربی بر روی حیوانات آزمایشگاهی (In Vivo)\n\n"
            "## 15. جامعه مورد مطالعه\nتعداد ۴۰ سر موش سوری نر بالغ نژاد C57BL/6"
        )
        sections = EquatorComplianceAuditor.parse_sections(animal_text)
        guidelines = EquatorComplianceAuditor.detect_applicable_guidelines(sections)
        self.assertIn("ARRIVE_2_0_ANIMAL_STUDIES", guidelines)

    def test_audit_gccp_cell_culture(self):
        """Tests individual OECD GCCP criteria (STR, Mycoplasma, Passage, Provenance)."""
        sections = EquatorComplianceAuditor.parse_sections(self.compliant_proposal)
        checks = EquatorComplianceAuditor.audit_gccp_cell_culture(sections)
        
        self.assertEqual(len(checks), 4)
        for c in checks:
            self.assertTrue(c.is_met, f"GCCP check failed: {c.criterion_en}")

    def test_audit_miqe_qpcr(self):
        """Tests individual MIQE criteria (RNA RIN, Primers, Reference Gene GAPDH, 2^-ddCt)."""
        sections = EquatorComplianceAuditor.parse_sections(self.compliant_proposal)
        checks = EquatorComplianceAuditor.audit_miqe_qpcr(sections)
        
        self.assertEqual(len(checks), 4)
        for c in checks:
            self.assertTrue(c.is_met, f"MIQE check failed: {c.criterion_en}")

    def test_audit_reagent_chemical_authentication(self):
        """Tests chemical purity, vehicle control (DMSO), and vendor sourcing."""
        sections = EquatorComplianceAuditor.parse_sections(self.compliant_proposal)
        checks = EquatorComplianceAuditor.audit_reagent_chemical_authentication(sections)
        
        self.assertEqual(len(checks), 3)
        for c in checks:
            self.assertTrue(c.is_met, f"Reagent auth check failed: {c.criterion_en}")

    def test_full_proposal_audit_compliant(self):
        """Tests full audit yielding compliance score >= 80% and 0 critical deficits."""
        result = EquatorComplianceAuditor.audit_proposal(self.compliant_proposal)
        self.assertIsInstance(result, EquatorAuditResult)
        self.assertTrue(result.is_compliant)
        self.assertGreaterEqual(result.compliance_score, 80.0)
        self.assertEqual(len(result.critical_deficits), 0)

    def test_critical_deficits_flagged_when_missing_auth(self):
        """Tests that omitting cell authentication and mycoplasma yields critical deficits."""
        hollow_proposal = (
            "## 14. نوع مطالعه\nکشت سلول\n\n"
            "## 15. جامعه مورد مطالعه\nسلول‌های سرطانی\n\n"
            "## 17. معیار های ورود به مطالعه\nسلول‌های زنده"
        )
        result = EquatorComplianceAuditor.audit_proposal(hollow_proposal)
        self.assertFalse(result.is_compliant)
        self.assertGreater(len(result.critical_deficits), 0)

    def test_report_generation_and_persistence(self):
        """Tests generation and disk persistence of EQUATOR_COMPLIANCE_AUDIT.md and .json."""
        result = EquatorComplianceAuditor.audit_proposal(self.compliant_proposal)
        with tempfile.TemporaryDirectory() as tmpdir:
            md_path, json_path = EquatorComplianceAuditor.save_reports(result, output_dir=tmpdir)
            
            self.assertTrue(os.path.exists(md_path))
            self.assertTrue(os.path.exists(json_path))
            
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("EQUATOR Network Compliance Report", content)
            self.assertIn("OECD_GCCP", content)
            
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertTrue(data["is_compliant"])
            self.assertGreaterEqual(data["compliance_score"], 80.0)

    def test_readiness_gate_infrastructure_includes_equator_auditor(self):
        """Verifies ProposalReadinessGate checks EquatorComplianceAuditor in Phase 1."""
        res = ProposalReadinessGate.check_all(mode="PRE_GENERATION_INFRASTRUCTURE")
        self.assertTrue(res.can_proceed)
        self.assertIn("EquatorComplianceAuditor", res.passed_modules)
        self.assertIn("EquatorComplianceAuditor", ProposalReadinessGate.required_modules)


if __name__ == "__main__":
    unittest.main()
