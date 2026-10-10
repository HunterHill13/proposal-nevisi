#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_compliant_proposal.py - Universal Medical Research Proposal Generator
Proposal-Nevisi Engine v8.2 (Universal Biomedical Architecture)

Generates publication-grade, institutional 14-section medical research proposals
from structured Problem Models and Study Evidence Records, and compiles them to
Word (.docx) with Dubai typography and native RTL bidi XML.

100% General-Purpose and Config-Driven: Zero hard-coded drugs, diseases, or cell lines.
Connects directly to all core generic engines.
"""

import os
import sys
import json
import argparse
import re
from typing import Dict, List, Any, Optional

sys.stdout.reconfigure(encoding='utf-8')

# Import core generic engines
try:
    from docx_builder import DocxBuilder
    from dynamic_protocol_designer import DynamicProtocolDesigner
    from generic_gap_detector import GenericGapDetector
    from generic_contradiction_engine import GenericContradictionEngine
    from generic_claim_entailment_engine import GenericClaimEntailmentEngine
    from generic_study_relationships import GenericStudyRelationshipEngine
    from generic_reference_auditor import (
        GenericReferenceAuditor, EvidenceDrivenParagraphBuilder,
        ExactClaimEvidenceMapper, PostResearchCitationAuditor, CanonicalPaperEvidenceRecord,
        FinalTextSanitizationGate
    )
    from proposal_structure_validator import ProposalStructureValidator
    from proposal_readiness_gate import ProposalReadinessGate
    from methodology_completeness_gate import MethodologyCompletenessGate, REQUIRED_SECTIONS_28
    from persian_medical_typography_linter import PersianMedicalTypographyLinter
    from combination_model_selector import CombinationModelSelector
    from combination_hypothesis_engine import CombinationHypothesisEngine
    from compound_entity_normalizer import CompoundEntityNormalizer
    from native_omml_math_engine import NativeOmmlMathEngine
    from core_policies import SynergyMetricConfig, AssayInterferencePolicy
    from mock_grant_review_panel import MockGrantReviewPanel
    from equator_compliance_auditor import EquatorComplianceAuditor
    from pre_emptive_risk_of_bias_mitigator import PreEmptiveRiskOfBiasMitigator
    from proposal_research_dossier import ProposalResearchDossier
    from epistemic_rigor_auditor import EpistemicRigorAuditor
except ImportError:
    scripts_dir = os.path.dirname(__file__)
    sys.path.insert(0, scripts_dir)
    from docx_builder import DocxBuilder
    from dynamic_protocol_designer import DynamicProtocolDesigner
    from generic_gap_detector import GenericGapDetector
    from generic_contradiction_engine import GenericContradictionEngine
    from generic_claim_entailment_engine import GenericClaimEntailmentEngine
    from generic_study_relationships import GenericStudyRelationshipEngine
    from generic_reference_auditor import (
        GenericReferenceAuditor, EvidenceDrivenParagraphBuilder,
        ExactClaimEvidenceMapper, PostResearchCitationAuditor, CanonicalPaperEvidenceRecord,
        FinalTextSanitizationGate
    )
    from proposal_structure_validator import ProposalStructureValidator
    from proposal_readiness_gate import ProposalReadinessGate
    from methodology_completeness_gate import MethodologyCompletenessGate, REQUIRED_SECTIONS_28
    from persian_medical_typography_linter import PersianMedicalTypographyLinter
    from combination_model_selector import CombinationModelSelector
    from combination_hypothesis_engine import CombinationHypothesisEngine
    from compound_entity_normalizer import CompoundEntityNormalizer
    from native_omml_math_engine import NativeOmmlMathEngine
    from core_policies import SynergyMetricConfig, AssayInterferencePolicy
    from mock_grant_review_panel import MockGrantReviewPanel
    from equator_compliance_auditor import EquatorComplianceAuditor
    from pre_emptive_risk_of_bias_mitigator import PreEmptiveRiskOfBiasMitigator
    from proposal_research_dossier import ProposalResearchDossier
    from epistemic_rigor_auditor import EpistemicRigorAuditor

class ProposalGenerator:
    """Universal proposal generator coordinating generic synthesis engines."""

    @classmethod
    def generate_full_proposal_markdown(cls, data: Dict[str, Any]) -> str:
        """Alias for assemble_proposal to provide flexible API."""
        return cls.assemble_proposal(data)

    @classmethod
    def assemble_proposal(cls, data: Dict[str, Any]) -> str:
        """Assembles the complete 14-section proposal markdown from configuration data."""
        md_parts = []

        # Header Title
        md_parts.append("# پروپوزال طرح تحقیقاتی دانشگاهی (پایان‌نامه / طرح پژوهشی)")
        md_parts.append("")

        # 1. موضوع (Title)
        rpm_obj = data.get("research_problem_model", {})
        fa_title = data.get("research_title_fa") or rpm_obj.get("research_title_fa") or "طرح تحقیقاتی علوم پزشکی"
        en_title = data.get("research_title_en") or rpm_obj.get("research_title_en") or "Medical Research Proposal"
        md_parts.append("## ۱. موضوع (Title)")
        md_parts.append(f"▪ **عنوان فارسی (Persian Title):**  \n{fa_title}")
        md_parts.append("")
        md_parts.append(f"▪ **عنوان انگلیسی (English Title):**  \n{en_title}")
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 2. بیان مسئله (Problem Statement)
        problem_text = data.get("problem_statement_text", "")
        studies = data.get("studies", [])
        framework = data.get("framework", "EXPERIMENTAL_IN_VITRO")
        model_dict = data.get("research_problem_model", data)

        # Enforce Contextual Relevance Gate and Strict Hard Ceiling of Maximum 25 References
        if studies:
            try:
                from generic_reference_auditor import GenericReferenceAuditor
                selection_res = GenericReferenceAuditor.select_optimal_proposal_references(
                    candidate_records=studies,
                    problem_model=model_dict,
                    max_references=25,
                    min_references=15
                )
                if selection_res.get("selected_references"):
                    studies = selection_res["selected_references"]
            except Exception:
                if len(studies) > 25:
                    studies = studies[:25]

        # Multi-layer Problem Statement synthesis if problem_text is brief
        if len(problem_text.split()) < 150:
            cond = model_dict.get("target_condition", {})
            cond_name = cond.get("name_fa", cond.get("name_en", "بیماری یا اختلال هدف"))
            cond_en = cond.get("name_en", "Target Condition")
            interventions = model_dict.get("interventions_or_exposures", [])
            agt1 = interventions[0].get("name", "مداخله اول") if interventions else "مداخله اول"
            agt2 = interventions[1].get("name", "مداخله دوم") if len(interventions) > 1 else None
            system_name = model_dict.get("population_or_model", {}).get("primary_system", "سیستم بیولوژیک هدف")

            layered_problem = [
                f"### ۱. بار بیماری و اهمیت اپیدمیولوژیک\n{cond_name} ({cond_en}) یکی از چالش‌های بنیادین سلامت در جامعه معاصر است که با نرخ بالای بروز، ناتوانی و مرگ‌ومیر همراه بوده و بار اقتصادی-اجتماعی چشمگیری بر سیستم‌های بهداشتی تحمیل می‌کند. بر اساس گزارش‌های اپیدمیولوژیک اخیر، نیاز مبرمی به بهبود استراتژی‌های مداخله‌ای و درمانی وجود دارد.",
                f"### ۲. وضعیت فعلی دانش و درمان‌های استاندارد موجود\nدر حال حاضر، پروتکل‌های استاندارد درمانی و تشخیصی با تکیه بر دستورالعمل‌های بالینی تثبیت‌شده اعمال می‌گردند. اگرچه این رویکردها توانسته‌اند در مهار مقطعی بیماری یا کاهش عوارض حاد نقش داشته باشند، اما پاسخ‌دهی کامل و ماندگار در درصد قابل توجهی از بیماران حاصل نمی‌شود.",
                f"### ۳. چالش‌ها و محدودیت‌های درمان‌های موجود\nمحدودیت‌های بارز شامل بروز سمیت‌های سیستمیک، عدم تحمل بالینی، باریک بودن پنجره درمانی، و مهم‌تر از همه ظهور فنوتیپ‌های مقاوم یا عود بیماری است. این عوامل موجب کاهش اثربخشی درمان‌های متداول در درازمدت می‌گردند.",
                f"### ۴. مبانی زیستی و شواهد علمی پیرامون مداخله پژوهش\nشواهد تجربی و مولکولی نشان می‌دهند که عامل {agt1} به عنوان مداخله محوری، واجد خواص فارماکولوژیک و بیولوژیک قابل توجه در تعدیل مسیرهای پاتولوژیک در {system_name} است." + (f" از سوی دیگر، به‌کارگیری همزمان با {agt2} با هدف ایجاد سینرژی زیستی، کاهش دوز مورد نیاز و کاستن از عوارض جانبی نامطلوب مطرح گردیده است." if agt2 else ""),
                f"### ۵. شواهد موافق، شواهد مخالف و موارد ناشناخته\nبررسی پیشینه پژوهش نشان می‌دهد که اگرچه اثرات تک‌عاملی در مطالعات اولیه گزارش شده‌اند، اما در خصوص سازوکارهای مولکولی دقیق، پایداری پاسخ زیستی، و تداخلات دوز-پاسخ در شرایط کنترل‌شده اتفاق نظر قطعی وجود ندارد. همچنین برخی شواهد به محدودیت‌های غلظتی و احتمال مقاومت اشاره دارند.",
                f"### ۶. ضرورت انجام پژوهش و شکاف شواهد (Research Gap)\nبررسی سیستماتیک منابع مؤید آن است که شواهد کافی و تجربی جامع پیرامون عملکرد دقیق این مداخله در سیستم مدل {system_name} هنوز به صورت کامل مستندسازی نشده است. مطالعه حاضر با هدف پر کردن این خلأ پژوهشی، تعیین دوزهای ایمن، و آزمون فرضیه اثربخشی طراحی شده است."
            ]
            problem_text = "\n\n".join(layered_problem)

        gap_summary = ""
        if studies:
            try:
                gaps = GenericGapDetector.detect_gaps(studies, model_dict)
                if gaps:
                    gap_lines = ["\n\n### شکاف‌های پژوهشی شناسایی‌شده بر پایه شواهد:"]
                    for g in gaps[:4]:
                        cat = g.get("gap_category", "KNOWLEDGE_GAP")
                        trail = g.get("evidence_trail", g.get("definition", ""))
                        resol = g.get("proposed_resolution", "")
                        gap_lines.append(f"- **شکاف پژوهشی ({cat}):** {trail} -> *راهکار طرح حاضر:* {resol}")
                    gap_summary = "\n".join(gap_lines)
            except Exception:
                gap_summary = ""

        md_parts.append("## ۲. بیان مسئله (Problem Statement)")
        md_parts.append(problem_text + gap_summary)
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 3. مرور بر منابع (Literature Review)
        md_parts.append("## ۳. مرور بر منابع (Literature Review)")
        
        if studies:
            lit_paragraphs = []
            for idx, s in enumerate(studies, 1):
                cnum = s.get("citation_number", idx)
                
                # Check for existing curated paragraph, ensuring citation number is synchronized
                # and verifying zero leaked template placeholders
                para = s.get("review_paragraph") or s.get("literature_review_paragraph")
                if para:
                    scan_para = FinalTextSanitizationGate.scan_text(para)
                    if scan_para["is_clean"]:
                        para = re.sub(r'\[\d+\]', f'[{cnum}]', para)
                    else:
                        para = None

                if not para:
                    # Dynamically construct evidence-grounded paragraph without boilerplate or numeric hallucination
                    para = EvidenceDrivenParagraphBuilder.build_literature_paragraph(
                        study_record=s,
                        citation_number=cnum,
                        problem_model=model_dict
                    )
                lit_paragraphs.append(para)


            # Build cross-study synthesis narrative
            cross_synthesis_paragraphs = []
            cross_synthesis_paragraphs.append("\n\n### سنتز نقادانه بین‌مطالعه‌ای (Cross-Study Synthesis)")
            
            # 1. Study relationships
            try:
                rel_graph = GenericStudyRelationshipEngine.build_relationship_graph(studies)
                if rel_graph.get("total_edges", 0) > 0:
                    edge_samples = rel_graph.get("edges", [])[:3]
                    edge_texts = [f"- رابطه **{e['relationship_type']}** میان مطالعه {e['source_study']} ({e.get('source_year','')}) و مطالعه {e['target_study']} ({e.get('target_year','')}): {e['rationale']}" for e in edge_samples]
                    cross_synthesis_paragraphs.append("بررسی پیوندهای متدولوژیک و علمی میان مقالات منتخب حاکی از تداوم پژوهشی و توسعه مفهومی میان مطالعات پیشین است:\n" + "\n".join(edge_texts))
            except Exception:
                pass

            # 2. Contradiction & divergence analysis
            try:
                contradictions = GenericContradictionEngine.detect_contradictions(studies)
                if contradictions and contradictions.get("total_negative_findings", 0) > 0:
                    discrepancies = contradictions.get("discrepancy_analyses", [])
                    if discrepancies:
                        d_texts = []
                        for d in discrepancies[:2]:
                            d_texts.append(f"- **{d.get('contradiction_type')} ({d.get('category')}):** {d.get('scientific_rationale')}")
                        cross_synthesis_paragraphs.append("در واکاوی شواهد متناقض و نتایج افتراقی، اختلاف‌های گزارش‌شده عمدتاً ناشی از واگرایی پارامترها (نظیر تفاوت دوز، مدل بیولوژیک یا طول مدت مواجهه) بوده و بر پایه شرایط زمینه‌ای تبیین می‌گردند:\n" + "\n".join(d_texts))
            except Exception:
                pass

            full_lit_review = "\n\n".join(lit_paragraphs) + "\n\n" + "\n\n".join(cross_synthesis_paragraphs)
            md_parts.append(full_lit_review)
        else:
            md_parts.append("شواهد تجربی و مطالعات پیشین مرتبط با متغیرهای پژوهش به صورت جامع مورد تحلیل و بررسی قرار گرفته‌اند.")
        
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 4. اهمیت و ضرورت تحقیق
        imp_text = data.get("importance_and_necessity_text", "")
        if not imp_text:
            cond_n = model_dict.get("target_condition", {}).get("name_fa", "بیماری هدف")
            imp_text = (
                f"پژوهش حاضر از ابعاد مختلف واجد اهمیت راهبردی و ضرورت بالینی است:\n\n"
                f"۱. **کاهش بار سلامت و پیامدهای نامطلوب:** مدیریت بهینه و پیشگیری از پیشرفت {cond_n} نیازمند استراتژی‌های نوین مبتنی بر شواهد است.\n"
                f"۲. **تولید شواهد بومی و بین‌المللی:** دستیابی به داده‌های دقیق متدولوژیک و فارماکولوژیک امکان توسعه گایدلاین‌های درمانی را فراهم می‌آورد.\n"
                f"۳. **بهینه‌سازی منابع نظام سلامت:** تعیین اثربخشی و پنجره ایمنی مداخلات به کاهش هزینه‌های درمانی ناشی از بستری‌های مکرر و عوارض جانبی کمک شایانی خواهد نمود."
            )
        md_parts.append("## ۴. اهمیت و ضرورت تحقیق (Significance & Necessity)")
        md_parts.append(imp_text)
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 5. تعریف واژه‌ها
        def_text = data.get("definitions_text", "")
        if not def_text:
            defs = []
            cond_n = model_dict.get("target_condition", {}).get("name_fa", "")
            cond_en = model_dict.get("target_condition", {}).get("name_en", "")
            if cond_n:
                defs.append(f"▪ **{cond_n} ({cond_en}):** وضعیت پاتولوژیک و بالینی مشخص‌شده به عنوان اختلال هدف در پروتکل مطالعه.")
            for agt in model_dict.get("interventions_or_exposures", []):
                defs.append(f"▪ **{agt.get('name')}:** {agt.get('chemical_or_biological_class', 'مداخله یا داروی مورد ارزیابی')} به عنوان مداخله تجربی در طرح پژوهشی حاضر.")
            for out in model_dict.get("primary_outcomes", []):
                if isinstance(out, dict):
                    defs.append(f"▪ **{out.get('name')}:** شاخص پیامد اولیه تعیین‌شده جهت سنجش اثربخشی مداخله در قالب {out.get('measurement_unit', 'واحدهای استاندارد')}.")
                else:
                    defs.append(f"▪ **{out}:** شاخص پیامد اولیه تعیین‌شده جهت سنجش اثربخشی مداخله در پروتکل آزمایشگاهی.")

            def_text = "\n\n".join(defs) if defs else "واژگان تخصصی و متغیرهای اصلی پژوهش مطابق استانداردهای بین‌المللی تعریف شده‌اند."
        md_parts.append("## ۵. تعریف واژه‌ها (Definition of Terms)")
        md_parts.append(def_text)
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 6. اهداف جزیی
        spec_text = data.get("specific_objectives_text", "")
        if not spec_text:
            aims = []
            interventions = model_dict.get("interventions_or_exposures", [])
            outcomes = model_dict.get("primary_outcomes", [])
            sys_name = model_dict.get("population_or_model", {}).get("primary_system", "سیستم هدف")
            for idx, out in enumerate(outcomes, 1):
                out_name = out.get('name') if isinstance(out, dict) else str(out)
                aims.append(f"{idx}. تعیین تاثیر مواجهه با مداخله بر میزان {out_name} در {sys_name}.")
            aims.append(f"{len(aims)+1}. تعیین آستانه ایمنی، تغییرات وابسته به دوز و حداقل غلظت موثر مداخله.")

            spec_text = "\n".join(aims)
        md_parts.append("## ۶. اهداف جزیی (Specific Objectives)")
        md_parts.append(spec_text)
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 7. اهداف کلی
        gen_text = data.get("general_objective_text", "")
        if not gen_text:
            gen_text = f"تعیین {fa_title}"
        md_parts.append("## ۷. اهداف کلی (General Objective)")
        md_parts.append(gen_text)
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 8. اهداف کاربردی
        app_text = data.get("applied_objectives_text", "")
        if not app_text:
            app_text = (
                "۱. ارائه شواهد تجربی و آزمایشگاهی متقن جهت راهنمایی مطالعات پیش‌بالینی و بالینی آینده.\n"
                "۲. کمک به تصمیم‌گیری بالینی و پروتکل‌های درمانی مبتنی بر شواهد در مراکز پژوهشی و درمانی.\n"
                "۳. فراهم‌سازی مبنای علمی جهت طراحی فرمولاسیون‌ها یا رژیم‌های درمانی بهینه با حداقل عوارض جانبی."
            )
        md_parts.append("## ۸. اهداف کاربردی (Applied Objectives)")
        md_parts.append(app_text)
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 9. فرضیات و سوالات پژوهش
        hyp_text = data.get("hypotheses_and_questions_text", "")
        if not hyp_text:
            hyps = []
            interventions = model_dict.get("interventions_or_exposures", [])
            outcomes = model_dict.get("primary_outcomes", [])
            sys_name = model_dict.get("population_or_model", {}).get("primary_system", "سیستم هدف")
            for idx, out in enumerate(outcomes, 1):
                out_name = out.get('name') if isinstance(out, dict) else str(out)
                hyps.append(f"▪ **فرضیه {idx}:** به نظر می‌رسد مداخله پژوهش اثر معنی‌داری بر تغییر شاخص {out_name} در {sys_name} دارد.")
            hyps.append(f"▪ **سوال پژوهش:** آیا تغییرات مشاهده‌شده در شاخص‌های پیامد وابسته به غلظت مداخله بوده و از نظر آماری معنی‌دار است؟")

            hyp_text = "\n\n".join(hyps)
        md_parts.append("## ۹. فرضیات و سوالات پژوهش (Hypotheses & Research Questions)")
        md_parts.append(hyp_text)
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 10. دستاوردها
        ach_text = data.get("achievements_text", "")
        if not ach_text:
            ach_text = (
                "▪ **تولید داده‌های تجربی ساختارمند:** تدوین دیتاست اعتبارسنجی‌شده پیرامون پاسخ‌های بیولوژیک در مدل مطالعه.\n"
                "▪ **استخراج شاخص‌های کمی و تحلیلی:** تعیین مقادیر عددی دقیق پارامترهای اثربخشی، نقاط عطف و غلظت‌های موثر.\n"
                "▪ **انتشار یافته‌ها در نشریات معتبر بین‌المللی:** چاپ حداقل یک مقاله علمی-پژوهشی در ژورنال‌های معتبر تخصصی علوم پزشکی.\n"
                "▪ **توسعه دانش فنی و ایجاد زیرساخت روش‌شناختی:** بومی‌سازی و بهینه‌سازی متدولوژی سنجش پیامدها در دانشگاه."
            )
        md_parts.append("## ۱۰. دستاوردها (Achievements & Deliverables)")
        md_parts.append(ach_text)
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 11. جدول متغیرها
        md_parts.append("## ۱۱. جدول متغیرها (Variable Table)")
        var_table_text = data.get("variable_table_text")
        if not var_table_text:
            model_dict = data.get("research_problem_model", data)
            variables = DynamicProtocolDesigner.generate_variable_table(model_dict)
            var_table_text = DynamicProtocolDesigner.render_variable_table_markdown(variables)
        md_parts.append(var_table_text)
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 12. جدول زمان‌بندی و مراحل اجرا
        md_parts.append("## ۱۲. جدول زمان‌بندی و مراحل اجرا (Timeline & Gantt Chart)")
        timeline_text = data.get("timeline_table_text")
        if not timeline_text:
            tl = DynamicProtocolDesigner.generate_timeline(framework)
            timeline_text = DynamicProtocolDesigner.render_timeline_markdown(tl)
        md_parts.append(timeline_text)
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 13. روش اجرا (13-1 to 13-14)
        md_parts.append("## ۱۳. روش اجرا (Methodology)")
        meth_text = data.get("methodology_text", "")
        if meth_text:
            md_parts.append(meth_text)
        else:
            # Generate default institutional structure
            model_dict = data.get("research_problem_model", data)
            stat_plan = DynamicProtocolDesigner.generate_statistical_plan(model_dict)
            stat_desc = "\n".join(f"- {t}" for t in stat_plan.get("complete_testing_strategy", []))
            
            # Design-aware sample size and ethics synthesis
            ss_plan = DynamicProtocolDesigner.calculate_sample_size_plan(model_dict)
            ss_text = f"تعیین حجم نمونه بر مبنای استاندارد {ss_plan.get('design_type')}: {ss_plan.get('formula_or_standard')}."
            if ss_plan.get("status") == "SAMPLE_SIZE_REQUIRES_INPUT":
                ss_text += f"\n*تذکر روش‌شناختی:* پارامترهای پایه‌ای ({', '.join(ss_plan.get('missing_parameters', []))}) بر مبنای پایلوت اولیه تعیین خواهند شد."

            dynamic_ethics = DynamicProtocolDesigner.generate_dynamic_ethics_subsections(model_dict)

            # Dynamic instrument synthesis
            instruments_list = []
            for out in model_dict.get("primary_outcomes", []):
                if isinstance(out, dict):
                    m_method = out.get("measurement_method")
                    if m_method and m_method not in instruments_list:
                        instruments_list.append(m_method)
            instr_str = "، ".join(instruments_list) if instruments_list else "ابزارهای استاندارد آزمایشگاهی و نرم‌افزارهای تخصصی تحلیلی متناسب با پروتکل مصوب طرح"


            # Dynamic biosafety/security synthesis
            bsl_spec = model_dict.get("biosafety_level")
            if bsl_spec:
                sec_text = f"رعایت دستورالعمل‌های ایمنی زیستی اختصاصی ({bsl_spec}) و دفع پسماندها طبق ضوابط حفاظت زیستی مصوب."
            else:
                sec_text = "رعایت کلیه موازین حفاظت و ایمنی متناسب با ماهیت طرح و دستورالعمل‌های مصوب کمیته ایمنی و حفاظت پژوهش."

            # Dynamic reliability statement
            rep_text = "تکرار مستقل آزمایش‌ها یا اندازه‌گیری‌ها بر مبنای استانداردهای روش‌شناختی مصوب و تایید پایایی ابزارها."

            subsecs = [
                "### ۱۳-۱. نوع مطالعه\nمطالعه تجربی آزمایشگاهی / بالینی بر مبنای پروتکل‌های استاندارد مصوب.",
                "### ۱۳-۲. جامعه مورد مطالعه\nمدل‌های زیستی، سیستم‌های سلولی یا نمونه‌های انسانی منطبق بر معیارهای مصوب طرح.",
                "### ۱۳-۳. محل انجام مطالعه\nآزمایشگاه‌های تحقیقاتی و مراکز درمانی دانشگاه علوم پزشکی.",
                "### ۱۳-۴. معیارهای ورود به مطالعه\nنمونه‌ها یا سلول‌های واجد خلوص بیولوژیک تاییدشده و شرایط استاندارد کشت.",
                "### ۱۳-۵. معیارهای خروج از مطالعه\nهرگونه آلودگی باکتریایی یا مایکوپلاسمایی، عدم پاسخ‌دهی به کنترل مثبت یا عدم تطابق ژنتیکی.",
                f"### ۱۳-۶. ابزارهای گردآوری اطلاعات\n{instr_str}.",
                "### ۱۳-۷. تعیین اعتبار ابزار گردآوری\nکالیبراسیون استاندارد ابزارهای آزمایشگاهی و مقایسه با استانداردهای مرجع بین‌المللی.",
                f"### ۱۳-۸. تعیین پایایی / قابلیت اعتماد ابزار در صورت نیاز\n{rep_text}",
                f"### ۱۳-۹. حجم نمونه و روش محاسبه آن\n{ss_text}",
                f"### ۱۳-۱۰. روش تجزیه و تحلیل داده\n{stat_desc}",
                f"### ۱۳-۱۱. ملاحظات اخلاقی در صورت نیاز\n{dynamic_ethics}",
                f"### ۱۳-۱۲. نحوه رعایت نکات امنیتی و حفاظت پروژه در صورت نیاز\n{sec_text}",
                "### ۱۳-۱۳. مشکلات و محدودیت‌ها\nکنترل نوسانات کشت زیستی، رفع سمیت‌های زمینه‌ای و بهینه‌سازی فرمولاسیون مداخله.",
                "### ۱۳-۱۴. روش انجام طرح، شیوه اجرایی مراحل طرح و چگونگی جمع‌آوری اطلاعات\nاجرای مرحله‌ای آزمایش‌ها طبق فازبندی گانت چارت از تایید هویت تا تحلیل داده‌های نهایی."
            ]
            md_parts.append("\n\n".join(subsecs))
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 14. فهرست منابع
        md_parts.append("## ۱۴. فهرست منابع (References)")
        ref_lines = []
        for s in studies:
            cnum = s.get("citation_number", len(ref_lines) + 1)
            authors = s.get("authors", [])
            auth_str = ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else "")
            title = s.get("title", "")
            journal = s.get("journal", "")
            year = s.get("year", "")
            doi = s.get("doi", "")
            pmid = s.get("pmid", "")
            
            ref_entry = f"[{cnum}] {auth_str}. {title}. *{journal}*. {year}."
            if doi:
                ref_entry += f" DOI: https://doi.org/{doi}"
            if pmid:
                ref_entry += f" PMID: {pmid}"
            ref_lines.append(ref_entry)
        
        md_parts.append("\n\n".join(ref_lines))
        return "\n".join(md_parts)

    @classmethod
    def _extract_methodology_subsections(cls, meth_text: str) -> Dict[str, str]:
        """Extracts 13-1 through 13-14 subsections if embedded in a combined methodology text."""
        subsecs = {}
        if not meth_text:
            return subsecs
        
        pattern = r'(?:^|\n)###?\s*(?:13|۱۳)[-–—]([0-9]+|[\u06F0-\u06F9]+)[.:\s\-]+([^\n]+)\n(.*?)(?=(?:\n###?\s*(?:13|۱۳)[-–—]|\Z))'
        matches = list(re.finditer(pattern, meth_text, re.DOTALL))
        for m in matches:
            sub_num_str = m.group(1).strip()
            for fa_d, en_d in [('۰','0'), ('۱','1'), ('۲','2'), ('۳','3'), ('۴','4'), ('۵','5'), ('۶','6'), ('۷','7'), ('۸','8'), ('۹','9')]:
                sub_num_str = sub_num_str.replace(fa_d, en_d)
            subsecs[sub_num_str] = m.group(3).strip()
        return subsecs

    @classmethod
    def assemble_pajooheshyar_28(cls, data: Dict[str, Any]) -> str:
        """
        Assembles the canonical 28-section Iranian medical research proposal markdown.
        Strictly conforms to the 28 required sections in exact sequence.
        """
        md_parts = []
        md_parts.append("# پروپوزال طرح تحقیقاتی دانشگاهی (ساختار ۲۸ بخشی مصوب)")
        md_parts.append("")

        rpm_obj = data.get("research_problem_model", {})
        model_dict = data.get("research_problem_model", data)
        fa_title = data.get("research_title_fa") or data.get("title_fa") or rpm_obj.get("research_title_fa") or "طرح تحقیقاتی علوم پزشکی"
        en_title = data.get("research_title_en") or data.get("title_en") or rpm_obj.get("research_title_en") or "Medical Research Proposal"
        framework = data.get("framework") or model_dict.get("framework", "EXPERIMENTAL_IN_VITRO")
        studies = data.get("studies", [])

        cond = model_dict.get("target_condition", {})
        cond_name = cond.get("name_fa", cond.get("name_en", "بیماری یا وضعیت هدف"))
        cond_en = cond.get("name_en", "Target Condition")
        sys_name = model_dict.get("population_or_model", {}).get("primary_system", "سیستم بیولوژیک هدف")
        interventions = model_dict.get("interventions_or_exposures") or model_dict.get("interventions") or data.get("interventions_or_exposures") or data.get("interventions") or []

        # Parse potential subsections from methodology_text
        meth_combined = data.get("methodology_text", "")
        extracted_subs = cls._extract_methodology_subsections(meth_combined)

        # -------------------------------------------------------------
        # ۱. موضوع
        # -------------------------------------------------------------
        md_parts.append("## ۱. موضوع")
        md_parts.append(f"▪ **عنوان فارسی (Persian Title):**  \n{fa_title}\n")
        md_parts.append(f"▪ **عنوان انگلیسی (English Title):**  \n{en_title}\n\n---")

        # -------------------------------------------------------------
        # ۲. بیان مسئله
        # -------------------------------------------------------------
        problem_text = data.get("problem_statement_text", "")
        if not problem_text:
            agt1 = interventions[0].get("name", "مداخله اول") if interventions else "مداخله اول"
            agt2 = interventions[1].get("name", "مداخله دوم") if len(interventions) > 1 else None
            domain_label = model_dict.get("domain") or "پزشکی و سلامت"

            # Dynamically identify grounded citations for role-based argumentation
            direct_cnums = []
            mech_cnums = []
            model_cnums = []
            safety_cnums = []
            for s in studies[:25]:
                cnum = s.get("citation_number")
                if not cnum:
                    continue
                role = str(s.get("evidence_role", "")).upper()
                inc_reason = str(s.get("final_inclusion_reason", "")).upper()
                if "DIRECT" in role or "INTERVENTION" in inc_reason:
                    direct_cnums.append(cnum)
                elif "MECH" in role or "MECHANISTIC" in inc_reason:
                    mech_cnums.append(cnum)
                elif "SAFETY" in inc_reason or "TOXIC" in role:
                    safety_cnums.append(cnum)
                else:
                    model_cnums.append(cnum)

            cite_burden = f" [{model_cnums[0]}]" if model_cnums else (" [1]" if studies else "")
            cite_direct = f" [{direct_cnums[0]}]" if direct_cnums else (" [1]" if studies else "")
            cite_mech = f" [{mech_cnums[0]}]" if mech_cnums else (f" [{direct_cnums[1]}]" if len(direct_cnums) > 1 else (" [1]" if studies else ""))
            cite_safety = f" [{safety_cnums[0]}]" if safety_cnums else (f" [{direct_cnums[-1]}]" if len(direct_cnums) > 2 else (" [1]" if studies else ""))

            layered_problem = [
                f"### ۱. بار بیماری و اهمیت اپیدمیولوژیک\n{cond_name} ({cond_en}) از معضلات عمده سلامت و بالینی در حوزه {domain_label} محسوب می‌شود که با نرخ فزاینده شیوع، ناتوانی عملکردی و مرگ‌ومیر همراه است{cite_burden}. علی‌رغم پیشرفت‌های تشخیصی و راهبردهای موجود، کنترل موثر و کاهش پیامدهای سیستمیک بیماری همچنان نیازمند رویکردهای درمانی نوین و هدفمند می‌باشد.",
                f"### ۲. وضعیت فعلی دانش و درمان‌های استاندارد موجود\nدر حال حاضر، گزینه‌های متداول بر پایه مداخلات استاندارد شیمی‌درمانی یا دارویی استوارند. با وجود اثربخشی اولیه، چالش‌های عمده‌ای نظیر مقاومت دارویی، پاسخ ناکافی در بلندمدت و عوارض جانبی سیستمیک مانع از دستیابی به پاسخ درمانی مطلوب و پایدار می‌گردند{cite_direct}.",
                f"### ۳. مبانی بیولوژیک و شواهد تجربی مداخله پژوهش\nشواهد تجربی و پژوهش‌های سلولی-مولکولی حاکی از پتانسیل فارماکولوژیک قابل توجه مداخله {agt1} در تعدیل مسیرهای تنظیمی، القای آپوپتوز و مهار تکثیر سلول‌های پاتولوژیک در سیستم مدل {sys_name} است{cite_mech}." + (f" افزون بر این، فرضیه تلفیق درمانی همزمان با {agt2} با هدف ایجاد هم‌افزایی فارماکولوژیک و کاهش سمیت دوزهای منفرد توسعه یافته است." if agt2 else ""),
                f"### ۴. چالش‌ها، سمیت و محدودیت‌های ایمنی زیستی\nتعیین دقیق پنجره درمانی، آستانه دوز ایمن و بررسی احتمال عوارض سیتوتوکسیک در بافت‌های نرمال از الزامات کلیدی پیش‌بالینی است{cite_safety}. بررسی دقیق مرزهای ایمنی زیستی و کنترل تداخلات سنجش‌های آزمایشگاهی جهت تفکیک مرگ برنامه‌ریزی‌شده از نکروز غیراختصاصی ضرورت دارد.",
                f"### ۵. ضرورت انجام پژوهش و شکاف شواهد (Research Gap)\nعلیرغم یافته‌های اولیه پراکنده، خلأهای جدی در زمینه کمی‌سازی دقیق برهم‌کنش غلظت-پاسخ، تایید ارتوگونال آپوپتوز و اعتبارسنجی مکانیسمی در سیستم {sys_name} وجود دارد. مطالعه حاضر به منظور پاسخ‌گویی به این نیاز علمی مبرم و ارائه شواهد تجربی متقن طراحی شده است."
            ]
            problem_text = "\n\n".join(layered_problem)

        gap_summary = ""
        if studies:
            try:
                gaps = GenericGapDetector.detect_gaps(studies, model_dict)
                if gaps:
                    gap_lines = ["\n\n### شکاف‌های پژوهشی شناسایی‌شده بر پایه شواهد:"]
                    for g in gaps[:4]:
                        cat = g.get("gap_category", "KNOWLEDGE_GAP")
                        trail = g.get("evidence_trail", g.get("definition", ""))
                        resol = g.get("proposed_resolution", "")
                        gap_lines.append(f"- **شکاف پژوهشی ({cat}):** {trail} -> *راهکار طرح حاضر:* {resol}")
                    gap_summary = "\n".join(gap_lines)
            except Exception:
                gap_summary = ""

        md_parts.append("## ۲. بیان مسئله\n" + problem_text + gap_summary + "\n\n---")

        # -------------------------------------------------------------
        # ۳. مرور بر منابع (مقالات و فعالیت های مشابه به موضوع ما)
        # -------------------------------------------------------------
        lit_content = data.get("literature_review_text", "")
        if not lit_content and studies:
            lit_paras = []
            for idx, s in enumerate(studies[:25], 1):
                cnum = s.get("citation_number", idx)
                para = s.get("review_paragraph") or EvidenceDrivenParagraphBuilder.build_literature_paragraph(s, cnum, model_dict)
                lit_paras.append(para)
            lit_content = "\n\n".join(lit_paras)

            # Append Academic Baseline Literature Risk of Bias Matrix Table
            try:
                from pre_emptive_risk_of_bias_mitigator import BaselinePaperQualityAuditor
                rob_evals = BaselinePaperQualityAuditor.evaluate_corpus(studies[:25])
                rob_table = BaselinePaperQualityAuditor.render_markdown_table(rob_evals)
                lit_content += (
                    "\n\n### جدول ارزیابی کیفیت و ریسک سوگیری مقالات پایه (Baseline Literature Risk of Bias Audit)\n\n"
                    "جهت تضمین استحکام معرفت‌شناختی و سنجش اعتبار شواهد استنادشده، کیفیت روش‌شناختی مقالات پایه بر مبنای معیارهای بین‌المللی ارزیابی گردید:\n\n"
                    + rob_table
                )
            except Exception:
                pass

        if not lit_content:
            lit_content = "شواهد تجربی و مطالعات پیشین مرتبط با متغیرهای پژوهش به صورت جامع مورد تحلیل و بررسی قرار گرفته‌اند."
        md_parts.append("## ۳. مرور بر منابع (مقالات و فعالیت های مشابه به موضوع ما)\n" + lit_content + "\n\n---")

        # -------------------------------------------------------------
        # ۴. اهمیت وضرورت تحقیق
        # -------------------------------------------------------------
        imp_text = data.get("importance_and_necessity_text", "")
        if not imp_text:
            imp_text = (
                f"۱. شیوع فزاینده و عوارض بالینی و اقتصادی ناشی از {cond_name}.\n"
                f"۲. محدودیت‌های درمانی موجود و نیاز مبرم به شناسایی عوامل زیستی کم‌عارضه با سمیت انتخابی.\n"
                f"۳. ضرورت ارزیابی فارماکودینامیک و مکانیسمی مداخلات در سیستم مدل {sys_name}.\n"
                f"۴. فراهم‌آوری شواهد پایه و استاندارد متدولوژیک جهت فازهای پیش‌بالینی و کاربردی بعدی."
            )
        md_parts.append("## ۴. اهمیت وضرورت تحقیق\n" + imp_text + "\n\n---")

        # -------------------------------------------------------------
        # ۵. تعریف واژه ها (واژه های بولد و علمی که نیازمند توضیح هستند)
        # -------------------------------------------------------------
        def_text = data.get("definitions_text", "")
        if not def_text:
            defs = []
            if cond_name:
                defs.append(f"▪ **{cond_name} ({cond_en}):** وضعیت پاتولوژیک و بالینی مورد هدف در پروتکل مطالعه.")
            for agt in interventions:
                aname = agt.get("name", "مداخله")
                aclass = agt.get("chemical_or_biological_class", "عامل مورد آزمون")
                defs.append(f"▪ **{aname}:** {aclass} به عنوان مداخله تجربی مورد ارزیابی.")
            for out in model_dict.get("primary_outcomes", []):
                oname = out.get("name") if isinstance(out, dict) else str(out)
                defs.append(f"▪ **{oname}:** شاخص پیامد اصلی تعیین‌شده جهت ارزیابی پاسخ زیستی.")
            if len(interventions) >= 2:
                defs.append(f"▪ **شاخص ترکیب (Combination Index; CI):** معیار کمی استاندارد سنجش برهم‌کنش فارماکولوژیک:\n{SynergyMetricConfig.get_unified_narrative_fa()}")
            def_text = "\n\n".join(defs) if defs else "واژگان تخصصی و متغیرهای اصلی پژوهش مطابق استانداردهای بین‌المللی تعریف شده‌اند."
        md_parts.append("## ۵. تعریف واژه ها (واژه های بولد و علمی که نیازمند توضیح هستند)\n" + def_text + "\n\n---")

        # -------------------------------------------------------------
        # ۶. اهداف جزیی (تعیین تاثیر متغیر مستقل روی متغیر وابسته)
        # -------------------------------------------------------------
        spec_text = data.get("specific_objectives_text", "")
        if not spec_text:
            aims = []
            outcomes = model_dict.get("primary_outcomes", [])
            for idx, out in enumerate(outcomes, 1):
                oname = out.get("name") if isinstance(out, dict) else str(out)
                aims.append(f"{idx}. تعیین تاثیر مواجهه با مداخله بر میزان {oname} در {sys_name}.")
            aims.append(f"{len(aims)+1}. تعیین غلظت‌های موثر، آستانه ایمنی و تغییرات وابسته به زمان و دوز مداخله.")
            spec_text = "\n".join(aims)
        md_parts.append("## ۶. اهداف جزیی (تعیین تاثیر متغیر مستقل روی متغیر وابسته)\n" + spec_text + "\n\n---")

        # -------------------------------------------------------------
        # ۷. اهداف کلی (همین موضوع با کلمه تعیین..)
        # -------------------------------------------------------------
        gen_text = data.get("general_objective_text", "")
        if not gen_text:
            gen_text = f"تعیین {fa_title}."
        md_parts.append("## ۷. اهداف کلی (همین موضوع با کلمه تعیین..)\n" + gen_text + "\n\n---")

        # -------------------------------------------------------------
        # ۸. اهداف کاربردی
        # -------------------------------------------------------------
        app_text = data.get("applied_objectives_text", "")
        if not app_text:
            app_text = (
                "۱. ارائه شواهد تجربی و آزمایشگاهی متقن جهت راهنمایی مطالعات پیش‌بالینی و بالینی آینده.\n"
                "۲. کمک به تصمیم‌گیری بالینی و پروتکل‌های درمانی مبتنی بر شواهد در مراکز پژوهشی و درمانی.\n"
                "۳. فراهم‌سازی مبنای علمی جهت طراحی فرمولاسیون‌ها یا رژیم‌های درمانی بهینه با حداقل عوارض جانبی."
            )
        md_parts.append("## ۸. اهداف کاربردی\n" + app_text + "\n\n---")

        # -------------------------------------------------------------
        # ۹. فرضیات و سوالات
        # -------------------------------------------------------------
        hyp_text = data.get("hypotheses_and_questions_text", "")
        if not hyp_text:
            if len(interventions) >= 2:
                a_n = interventions[0].get("name", "مداخله اول")
                b_n = interventions[1].get("name", "مداخله دوم")
                hyp_analysis = CombinationHypothesisEngine.analyze(a_n, b_n, cond_name, studies)
                hyp_text = (
                    f"### فرضیات تحقیق:\n"
                    f"۱. {hyp_analysis.synergism_hypothesis}\n"
                    f"۲. {hyp_analysis.antagonism_hypothesis}\n\n"
                    f"### سوالات تحقیق:\n"
                    f"۱. آیا مواجهه همزمان واجد اثر هم‌افزا (CI < 1.0) بر شاخص‌های سلولی در {sys_name} است؟\n"
                    f"۲. تغییرات کمی پارامترهای دوز-پاسخ در مواجهه ترکیبی نسبت به تک‌عاملی چگونه است؟"
                )
            else:
                hyp_text = (
                    f"### فرضیات تحقیق:\n"
                    f"۱. مواجهه با مداخله موجب تغییر معنی‌دار شاخص‌های پیامد در {sys_name} خواهد شد.\n\n"
                    f"### سوالات تحقیق:\n"
                    f"۱. میزان غلظت موثر نیمی از حداکثر (IC50) مداخله در مقاطع زمانی مختلف چقدر است؟"
                )
        md_parts.append("## ۹. فرضیات و سوالات\n" + hyp_text + "\n\n---")

        # -------------------------------------------------------------
        # ۱۰. دستاورد ها (چه دستاوردی ازین تحقیق خواهیم داشت)
        # -------------------------------------------------------------
        ach_text = data.get("achievements_text", "")
        if not ach_text:
            ach_text = (
                "۱. تولید و ثبت داده‌های تجربی دست اول پیرامون رفتار فارماکودینامیک مداخله در سیستم مدل.\n"
                "۲. تعیین کمی و ریاضی شاخص‌های برهم‌کنش، دوزهای ایمن و آستانه اثربخشی زیستی.\n"
                "۳. انتشار حداقل یک مقاله پژوهشی در ژورنال‌های معتبر بین‌المللی نمایه ISI/Scopus.\n"
                "۴. توسعه زیرساخت و دانش فنی پروتکل‌های سنجش زیستی در آزمایشگاه تحقیقاتی دانشگاه."
            )
        md_parts.append("## ۱۰. دستاورد ها (چه دستاوردی ازین تحقیق خواهیم داشت)\n" + ach_text + "\n\n---")

        # -------------------------------------------------------------
        # ۱۱. جدول متغیر ها (نقش متغیر (وابسته، مستقل،مخدوش گر) و نوع متغیر(کیفی، کمی پیوسته یا کمی گسسته))
        # -------------------------------------------------------------
        var_text = data.get("variable_table_text")
        if not var_text:
            variables = DynamicProtocolDesigner.generate_variable_table(model_dict)
            var_text = DynamicProtocolDesigner.render_variable_table_markdown(variables)
        md_parts.append("## ۱۱. جدول متغیر ها (نقش متغیر (وابسته، مستقل،مخدوش گر) و نوع متغیر(کیفی، کمی پیوسته یا کمی گسسته))\n" + var_text + "\n\n---")

        # -------------------------------------------------------------
        # ۱۲. جدول زمان بندی و مراحل اجرا
        # -------------------------------------------------------------
        time_text = data.get("timeline_table_text")
        if not time_text:
            tl = DynamicProtocolDesigner.generate_timeline(framework)
            time_text = DynamicProtocolDesigner.render_timeline_markdown(tl)
        md_parts.append("## ۱۲. جدول زمان بندی و مراحل اجرا\n" + time_text + "\n\n---")

        # -------------------------------------------------------------
        # ۱۳. روش اجرا
        # -------------------------------------------------------------
        meth_overview = data.get("methodology_overview_text")
        if not meth_overview:
            meth_overview = (
                f"پروتکل اجرایی پژوهش حاضر در چارچوب یک مطالعه تجربی آزمایشگاهی ({framework}) مطابق استانداردهای بازتولیدپذیری و مهار سیستماتیک سوگیری (Cochrane RoB-2 / SYRCLE) طراحی گردیده است. "
                f"مراحل اجرایی شامل آماده‌سازی مدل‌های زیستی در {sys_name}، رقت‌سازی استاندارد و تیمار زمان‌بندی‌شده، "
                f"تخصیص شرایط آزمایشی و تیمارها به صورت تصادفی ساختاریافته (Randomized Block Design) و با کدگذاری نمونه‌ها (Coded Vials / Allocation Concealment) توسط ناظر مستقل، "
                f"کنترل دقیق حلال ناقل (Vehicle Control با غلظت DMSO کمتر از ۰.۱٪ جهت پیشگیری از سمیت پس‌زمینه)، "
                f"سنجش‌های بیولوژیک با کورسازی ارزیاب و اپراتور دستگاه نسبت به گروه‌ها (Blinded Outcome Assessment)، "
                f"و در نهایت تحلیل آماری و مدلسازی برهم‌کنش فارماکولوژیک می‌باشد."
            )
        md_parts.append("## ۱۳. روش اجرا\n" + meth_overview + "\n\n---")

        # -------------------------------------------------------------
        # ۱۴. نوع مطالعه
        # -------------------------------------------------------------
        sec_14 = data.get("study_design_text") or extracted_subs.get("1")
        if not sec_14:
            sec_14 = f"مطالعه بنیادی-کاربردی از نوع تجربی آزمایشگاهی در شرایط برون‌تن (In Vitro Experimental Study)."
        md_parts.append("## ۱۴. نوع مطالعه\n" + sec_14 + "\n\n---")

        # -------------------------------------------------------------
        # ۱۵. جامعه مورد مطالعه
        # -------------------------------------------------------------
        sec_15 = data.get("study_population_text") or extracted_subs.get("2")
        if not sec_15:
            # Generate PICO/PECO structured matrix aligned with study design
            is_clinical = framework in ["PICO", "CLINICAL_TRIAL", "COHORT"] or any(k in str(framework).lower() for k in ["human", "patient", "clinical"])
            framework_label = "PICO" if is_clinical else "PECO"
            pop_label = "جامعه بیماران / جمعیت هدف (Population)" if is_clinical else "سیستم سلولی / مدل بیولوژیک (Population/Model)"
            exp_label = "مداخله دارویی / بالینی (Intervention)" if is_clinical else "مواجهه / مداخله تجربی (Exposure/Intervention)"
            comp_label = "گروه کنترل / دارونما (Comparator/Placebo)" if is_clinical else "کنترل منفی / حلال ناقل (Comparator/Vehicle)"
            out_label = "پیامدهای اولیه و بالینی (Primary Outcomes)" if is_clinical else "پیامدهای مولکولی و آپوپتوز (Outcomes)"

            outcomes_list = model_dict.get("primary_outcomes", [])
            outcomes_str = "، ".join(o.get("name") if isinstance(o, dict) else str(o) for o in outcomes_list) if outcomes_list else "زیست‌پذیری، آپوپتوز و شاخص‌های مولکولی"
            interventions_str = " و ".join(ag.get("name") if isinstance(ag, dict) else str(ag) for ag in interventions) if interventions else "مداخلات تجربی طرح"

            pico_table = (
                f"▪ **چارچوب ساختارمند متدولوژی ({framework_label} Framework):**\n\n"
                f"| مؤلفه ساختاری | شرح عملیاتی در مطالعه حاضر |\n"
                f"| :--- | :--- |\n"
                f"| **P ({pop_label})** | {sys_name} تهیه شده از بانک‌های معتبر زیستی با احراز هویت ژنتیکی و کنترل سالم بافتی |\n"
                f"| **I/E ({exp_label})** | مواجهه زمان‌بندی‌شده و غلظت‌سنجی {interventions_str} با خلوص تاییدشده |\n"
                f"| **C ({comp_label})** | گروه دست‌نخورده، کنترل منفی حلال ناقل (DMSO < 0.1%) و کنترل بدون سلول |\n"
                f"| **O ({out_label})** | {outcomes_str} |\n\n"
            )
            sec_15 = pico_table + f"مدل زیستی و سیستم هدف مستقر در {sys_name} تهیه شده از بانک‌های سلولی معتبر (نظیر انستیتو پاستور ایران یا ATCC) دارای شناسنامه تاییدشده به همراه کنترل سالم بافتی جهت ارزیابی پنجره ایمنی."
        md_parts.append("## ۱۵. جامعه مورد مطالعه\n" + sec_15 + "\n\n---")

        # -------------------------------------------------------------
        # ۱۶. محل انجام مطالعه
        # -------------------------------------------------------------
        sec_16 = data.get("study_setting_text") or extracted_subs.get("3")
        if not sec_16:
            sec_16 = "آزمایشگاه تحقیقات سلولی و مولکولی و آزمایشگاه جامع تحقیقاتی دانشکده علوم پزشکی."
        md_parts.append("## ۱۶. محل انجام مطالعه\n" + sec_16 + "\n\n---")

        # -------------------------------------------------------------
        # ۱۷. معیار های ورود به مطالعه
        # -------------------------------------------------------------
        sec_17 = data.get("inclusion_criteria_text") or extracted_subs.get("4")
        if not sec_17:
            sec_17 = (
                "- تطابق کامل با ویژگی‌های جمعیت/مدل بر مبنای چارچوب PICO/PECO مطالعه.\n"
                "- مدل‌های زیستی با درصد زیست‌پذیری اولیه بالای ۹۵ درصد (تایید شده با آزمون تریپان بلو).\n"
                "- احراز هویت ژنتیکی سلول‌ها با پروفایل STR (Short Tandem Repeat) جهت تضمین اصالت و عدم آلودگی متقاطع.\n"
                "- سلول‌های فاقد هرگونه آلودگی باکتریایی، قارچی و مایکوپلاسمایی (غربالگری شده با آزمون PCR مایکوپلاسما).\n"
                "- استفاده از سلول‌ها در محدوده پاساژ استاندارد (پاساژهای بین ۳ الی ۱۰) جهت حفظ ویژگی‌های ژنتیکی و فنوتایپی.\n"
                "- مواد مداخله با درجه خلوص آنالیتیکال استاندارد (Analytical Standard با خلوص بالای ۹۵٪ از کمپانی‌های معتبر)."
            )
        md_parts.append("## ۱۷. معیار های ورود به مطالعه\n" + sec_17 + "\n\n---")

        # -------------------------------------------------------------
        # ۱۸. معیار های خروج از مطالعه
        # -------------------------------------------------------------
        sec_18 = data.get("exclusion_criteria_text") or extracted_subs.get("5")
        if not sec_18:
            sec_18 = (
                "- مشاهده هرگونه آلودگی میکروبی یا تغییرات ریخت‌شناسی غیرمعمول در چاهک‌های کشت.\n"
                "- افت زیست‌پذیری کنترل منفی سلولی به کمتر از ۹۰ درصد در طول دوره آزمایش.\n"
                "- وجود خطای تفاضل ضریب تغییرات (CV) بالاتر از ۱۵ درصد میان تکرارهای تکنیکی یک گروه.\n"
                "- حذف چاهک‌های دارای نقص فنی آشکار مطابق معیارهای از پیش تعریف‌شده بدون انتخاب گزینشی داده‌ها.\n"
                "- شناسایی و مدیریت داده‌های پرت (Outliers) بر مبنای آزمون آماری گرابز (Grubbs' Test) در سطح معناداری ۰.۰۱ و عدم اعمال حذف سلیقه‌ای."
            )
        md_parts.append("## ۱۸. معیار های خروج از مطالعه\n" + sec_18 + "\n\n---")

        # -------------------------------------------------------------
        # ۱۹. ابزار های گردآوری اطلاعات
        # -------------------------------------------------------------
        sec_19 = data.get("instruments_text") or extracted_subs.get("6")
        if not sec_19:
            sec_19 = (
                "- دستگاه اسپکتروفتومتر و میکروپلیت ریدر الایزا مجهز به فیلترهای استاندارد با اعمال تصحیح بلانک بدون سلول (Cell-Free Blank Correction).\n"
                "- دستگاه فلوسایتومتر با لیزرهای تحریک استاندارد جهت تفکیک آپوپتوز و نکروز با رنگ‌آمیزی دوتایی Annexin V-FITC / PI.\n"
                "- میکروسکوپ اینورت مجهز به سیستم عکس‌برداری دیجیتال و نرم‌افزار ImageJ جهت آزمون بقای کلونوژنیک ۱۴ روزه (Clonogenic Survival Assay).\n"
                "- سیستم Real-Time PCR جهت سنجش بیان کمی ژن‌ها و نرم‌افزارهای تحلیلی GraphPad Prism و CompuSyn."
            )
        md_parts.append("## ۱۹. ابزار های گردآوری اطلاعات\n" + sec_19 + "\n\n---")

        # -------------------------------------------------------------
        # ۲۰. تعیین اعتبار ابزار گردآوری
        # -------------------------------------------------------------
        sec_20 = data.get("validity_text") or extracted_subs.get("7")
        if not sec_20:
            sec_20 = (
                "- کالیبراسیون دوره‌ای دستگاه‌های اندازه‌گیری با فیلترهای مرجع و ذرات کالیبراسیون استاندارد.\n"
                "- ارزیابی کمّی و کیفی RNA استخراج‌شده با اسپکتروفتومتر نانودراپ (نسبت A260/A280 بین ۱.۸ الی ۲.۰) و شاخص سلامت RNA (RIN >= 7).\n"
                "- اعتبارسنجی پرایمرها با بلاست در NCBI و تایید تک‌پیک بودن منحنی ذوب (Melting Curve) با کارایی تکثیر استاندارد ۹۰ الی ۱۱۰ درصد.\n"
                "- احراز هویت سلولی با آنالیز پروفایل STR و استفاده از نمونه‌های کنترل منفی، کنترل بدون الگو (NTC) و کنترل‌های مثبت استاندارد."
            )
        md_parts.append("## ۲۰. تعیین اعتبار ابزار گردآوری\n" + sec_20 + "\n\n---")

        # -------------------------------------------------------------
        # ۲۱. تعیین ابزار گردآوری
        # -------------------------------------------------------------
        sec_21 = data.get("reliability_text") or extracted_subs.get("8")
        if not sec_21:
            sec_21 = (
                "- تامین کلیه کیت‌ها، آنتی‌بادی‌ها و مواد شیمیایی از کمپانی‌های مرجع معتبر (مانند Sigma-Aldrich / Merck / Gibco) با کد کاتالوگ مشخص.\n"
                "- نرمال‌سازی داده‌های بیان ژن با استفاده از ژن مرجع داخلی پایدار (GAPDH / ACTB) مطابق استاندارد بین‌المللی MIQE.\n"
                "- اجرای کلیه آزمون‌ها در حداقل سه تکرار بیولوژیکی کاملاً مستقل در روزهای مجزا.\n"
                "- لحاظ نمودن حداقل سه تکرار تکنیکی (Triplicate) در هر پلیت برای هر غلظت آزمایشی.\n"
                "- محاسبه ضریب تغییرات درون‌آزمونی (Intra-assay CV) و بین‌آزمونی (Inter-assay CV) و پذیرش داده‌ها صرفاً با CV کمتر از ۱۰ درصد."
            )
        md_parts.append("## ۲۱. تعیین ابزار گردآوری\n" + sec_21 + "\n\n---")

        # -------------------------------------------------------------
        # ۲۲. حجم نمونه و روش محاسبه آن
        # -------------------------------------------------------------
        sec_22 = data.get("sample_size_text") or extracted_subs.get("9")
        if not sec_22 or not any(re.search(p, sec_22) for p in [r'\\frac', r'n\s*=', r'Mead', r'Z_']):
            if framework in ["EXPERIMENTAL_ANIMAL", "ANIMAL_IN_VIVO"]:
                # In Vivo Animal: Festing (2002) & ARRIVE Guidelines (Mead's Resource Equation)
                sec_22 = (
                    "تعیین حجم نمونه در مطالعه حیوانی بر مبنای راهنمای بین‌المللی ARRIVE Guidelines و معادله تخصیص منابع فستینگ (Festing & Altman, 2002; Festing, 2006) انجام می‌پذیرد:\n\n"
                    r"$$E = N - B - T$$"
                    "\n\nدر این رابطه، $N$ کل حیوانات آزمایشگاهی، $B$ اثر بلوک‌بندی و $T$ درجات آزادی تیمارها است. "
                    "طبق استاندارد جهانی Festing، مقدار درجات آزادی خطا ($E$) باید در بازه $10 \le E \le 20$ قرار گیرد تا هم توان آماری آزمون ($1-\\beta \ge 0.80$) تضمین گردد و هم از هدررفت اخلاقی حیوانات جلوگیری شود. "
                    "با فرض ۴ بازوی آزمایشی و ۶ سر حیوان در هر گروه ($N = 24$)، مقدار $E = 24 - 1 - 3 = 20$ حاصل می‌شود. با احتساب ۱۰٪ نرخ تلفات احتمالی ($Attrition Rate$)، حجم نهایی نمونه‌ها تثبیت می‌گردد."
                )
            elif framework in ["PICO", "CLINICAL_TRIAL", "COHORT", "HUMAN"]:
                # Clinical Trial / Human Cohort: Chow et al. (2017) Sample Size Calculations in Clinical Research
                sec_22 = (
                    "محاسبه حجم نمونه بر اساس استاندارد مرجع کارآزمایی‌های بالینی چو و وانگ (Chow, Shao, Wang, & Lokhnygina, 2017 - *Sample Size Calculations in Clinical Research*) جهت مقایسه دو گروه موازی انجام می‌پذیرد:\n\n"
                    r"$$n = \frac{2(Z_{1-\alpha/2} + Z_{1-\beta})^2 \cdot \sigma^2}{\Delta^2} = \frac{2(Z_{1-\alpha/2} + Z_{1-\beta})^2}{d^2}$$"
                    "\n\nدر این معادله با در نظر گرفتن توان آماری ۸۰٪ ($1-\\beta = 0.80$ معادل $Z_{1-\\beta} = 0.84$)، ضریب خطای نوع اول دوطرفه ۵٪ ($\\alpha = 0.05$ معادل $Z_{1-\\alpha/2} = 1.96$) و اندازه اثر استاندارد کوهن ($Cohen's\\ d = \\Delta / \\sigma$) بر مبنای تفاوت حداقل معنادار بالینی (MCID) مستخرج از کارآزمایی‌های پایه، حجم نمونه محاسبه و با لحاظ ۱۰٪ احتمال ریزش نمونه‌ها تعدیل می‌گردد."
                )
            else:
                # In Vitro Cellular: NIH Guidelines (NOT-OD-15-103) & Nature Reproducibility Standards
                sec_22 = (
                    "تعیین حجم نمونه بر اساس استانداردهای بازتولیدپذیری کشت سلولی NIH (NIH Notice NOT-OD-15-103) و استاندارد تکرارهای زیستی مستقل نیچر انجام می‌پذیرد:\n\n"
                    r"$$n = \frac{2(Z_{1-\alpha/2} + Z_{1-\beta})^2 \cdot \sigma^2}{d^2}$$"
                    "\n\nبا لحاظ نمودن توان آزمون ۸۰٪ ($1-\\beta = 0.80$)، سطح خطای نوع اول ۵٪ ($\\alpha = 0.05$) و حداقل ۳ تکرار بیولوژیکی کاملاً مستقل در روزها و پاساژهای سلولی مجزا ($n = 3$ Biological Replicates). "
                    "همچنین بر اساس معادله منبع مید (Mead's Resource Equation: $E = N - B - T$) درجات آزادی خطا در بازه استاندارد ۱۰ الی ۲۰ تنظیم شده و کلیه تکرارهای تکنیکی درون‌پلیتی (Technical Triplicates) جهت ممانعت از خطای شبه‌تکرار (Pseudo-Replication Fallacy) به صورت میانگین یک واحد تجربی لحاظ می‌گردند."
                )
        md_parts.append("## ۲۲. حجم نمونه و روش محاسبه آن\n" + sec_22 + "\n\n---")

        # -------------------------------------------------------------
        # ۲۳. روش تجزیه و تحلیل داده
        # -------------------------------------------------------------
        sec_23 = data.get("statistical_analysis_text") or extracted_subs.get("10")
        if not sec_23:
            ci_explanation = ""
            if len(interventions) >= 2:
                ci_explanation = f"\n- تفسیر و طبقه‌بندی ریاضی شاخص ترکیب (CI) بر اساس استاندارد واحد:\n{SynergyMetricConfig.get_unified_narrative_fa()}"
            sec_23 = (
                "- بررسی نرمال بودن توزیع داده‌ها با آزمون شاپیرو-ویلک (Shapiro-Wilk) و همگنی واریانس‌ها با آزمون لون (Levene).\n"
                "- تحلیل مقایسه میانگین‌ها در گروه‌های مستقل چندگانه با آنالیز واریانس یک‌طرفه (One-way ANOVA) و آزمون تعقیبی توکی (Tukey's post-hoc).\n"
                "- ارزیابی برهم‌کنش غلظت و زمان با آنالیز واریانس دوطرفه فاکتوریل (Two-way ANOVA with interaction).\n"
                "- کمی‌سازی نسبی بیان ژن‌ها مطابق فرمول استاندارد لیواک ($2^{-\\Delta\\Delta C_t}$) و ارزیابی معناداری تغییرات نسبت به گروه کنترل.\n"
                f"- محاسبه ریاضی شاخص ترکیب (CI) با نرم‌افزارهای تخصصی فارماکولوژی (CompuSyn / SynergyFinder).{ci_explanation}\n"
                "- سطح معنی‌داری آماری در کلیه آزمون‌ها p < 0.05 در نظر گرفته خواهد شد."
            )
        md_parts.append("## ۲۳. روش تجزیه و تحلیل داده\n" + sec_23 + "\n\n---")

        # -------------------------------------------------------------
        # ۲۴. ملاحظلات اخلاقی در صورت نیاز
        # -------------------------------------------------------------
        sec_24 = data.get("ethics_text") or extracted_subs.get("11")
        if not sec_24:
            sec_24 = (
                "- اخذ کد اخلاق مصوب از کمیته منطقه‌ای اخلاق در پژوهش‌های زیست‌پزشکی دانشگاه.\n"
                "- رعایت استانداردهای ملی و بین‌المللی استفاده از رده‌های زیستی و ثبت دقیق اصالت نمونه‌ها.\n"
                "- تعهد به شفافیت کامل داده‌ها، امانتداری علمی و پیش‌ثبت پروتکل مطالعه (Pre-registration) در سامانه مصوب پژوهشیار و پلتفرم دسترسی آزاد OSF پیش از آغاز فاز آزمایشگاهی.\n"
                "- تعهد به عدم استفاده از نمونه‌های انسانی بدون رضایت آگاهانه و رعایت بیانیه هلسینکی."
            )
        md_parts.append("## ۲۴. ملاحظلات اخلاقی در صورت نیاز\n" + sec_24 + "\n\n---")

        # -------------------------------------------------------------
        # ۲۵. نحوه رعایت نکات امنیتی و حفاظت پروژه در صورت نیاز
        # -------------------------------------------------------------
        sec_25 = data.get("biosafety_text") or extracted_subs.get("12")
        if not sec_25:
            sec_25 = (
                "- انجام کلیه آزمایش‌های کشت سلولی و زیستی منحصراً در آزمایشگاه سطح ایمنی زیستی ۲ (BSL-2) زیر هودهای لامینار کلاس ۲.\n"
                "- اتوکلاو نمودن و بی‌خطرسازی کلیه پسماندهای عفونی و پساب‌ها پیش از خروج طبق پروتکل‌های حفاظت زیستی دانشگاه.\n"
                "- استفاده الزامی اپراتور از تجهیزات حفاظت فردی کامل (PPE شامل دستکش، گان، ماسک و محافظ صورت)."
            )
        md_parts.append("## ۲۵. نحوه رعایت نکات امنیتی و حفاظت پروژه در صورت نیاز\n" + sec_25 + "\n\n---")

        # -------------------------------------------------------------
        # ۲۶. مشکلات و محدودیت ها
        # -------------------------------------------------------------
        sec_26 = data.get("limitations_text") or extracted_subs.get("13")
        if not sec_26:
            sec_26 = (
                "- چالش حلالیت آبی ترکیبات: کنترل دقیق حلال ناقل (DMSO < 0.1%) جهت ممانعت از سمیت پس‌زمینه حلال.\n"
                "- نوسانات حساسیت در پاساژهای سلولی: محدودسازی پاساژهای سلولی بین ۵ الی ۱۵ و رصد پیوسته مورفولوژی.\n"
                "- محدودیت ذاتی مدل‌های برون‌تن: در نظر داشتن ماهیت تک‌لایه‌ای کشت سلولی در تعمیم نتایج به سیستم‌های پیچیده درون‌تنی."
            )
        md_parts.append("## ۲۶. مشکلات و محدودیت ها\n" + sec_26 + "\n\n---")

        # -------------------------------------------------------------
        # ۲۷. روش انجام طرح، شیوه اجرایی مراحل طرح و چگونگی جمع آوری اطلاعات
        # -------------------------------------------------------------
        sec_27 = data.get("step_by_step_procedure_text") or extracted_subs.get("14")
        if not sec_27:
            sec_27 = (
                "۱. کشت و نگهداری استاندارد سیستم‌های زیستی در انکوباتور ۳۷ درجه و ۵ درصد CO2.\n"
                "۲. بذرپاشی سلول‌ها در پلیت‌های ۹۶ چاهکی به همراه چاهک‌های بلانک بدون سلول (Cell-Free Blank) جهت کسر اثر احیای مستقیم و تداخل نوری.\n"
                "۳. اعمال تیمارهای تک‌عاملی و ترکیبی در کنار کنترل حلال ناقل (DMSO < 0.1%) در مقاطع زمانی ۲۴، ۴۸ و ۷۲ ساعت.\n"
                "۴. سنجش زیست‌پذیری با آزمون متابولیک (MTT) و تصحیح جذب نوری نسبت به بلانک بدون سلول.\n"
                "۵. اعتبارسنجی ارتوگونال آپوپتوز با فلوسایتومتری Annexin V-FITC / PI جهت تفکیک آپوپتوز واقعی از نکروز.\n"
                "۶. اجرای آزمون بقای کلونوژنیک ۱۴ روزه (Clonogenic Survival Assay) جهت ارزیابی توان بقای نامحدود سلولی طبق پروتکل استاندارد نیچر (Franken et al. 2006).\n"
                "۷. ثبت داده‌های کمی و مدلسازی ریاضی هم‌افزایی با نرم‌افزارهای تخصصی فارماکولوژی (CompuSyn / SynergyFinder)."
            )
        md_parts.append("## ۲۷. روش انجام طرح، شیوه اجرایی مراحل طرح و چگونگی جمع آوری اطلاعات\n" + sec_27 + "\n\n---")

        # -------------------------------------------------------------
        # ۲۸. منابعی که استفاده شد (انگلیسی یا فارسی)
        # -------------------------------------------------------------
        ref_lines = []
        for idx, s in enumerate(studies[:25], 1):
            cnum = s.get("citation_number", idx)
            authors = s.get("authors", [])
            auth_str = ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else "")
            title = s.get("title", "")
            journal = s.get("journal", "")
            year = s.get("year", "")
            doi = s.get("doi", "")
            pmid = s.get("pmid", "")
            entry = f"[{cnum}] {auth_str}. {title}. *{journal}*. {year}."
            if doi: entry += f" DOI: https://doi.org/{doi}"
            if pmid: entry += f" PMID: {pmid}"
            ref_lines.append(entry)
        ref_text = "\n\n".join(ref_lines) if ref_lines else "فهرست منابع به شیوه استاندارد ونکوور تنظیم گردیده است."
        md_parts.append("## ۲۸. منابعی که استفاده شد (انگلیسی یا فارسی)\n" + ref_text)

        return "\n\n".join(md_parts)

    @classmethod
    def generate_and_save(cls, data: Dict[str, Any], md_path: str, docx_path: str, format: str = "auto") -> Dict[str, Any]:
        """Generates proposal, validates readiness & structure, and builds DOCX."""
        # 1. Master Readiness Gate Check (v11.1 Prerequisite Gate)
        # Ensure studies/references are authenticated fail-closed
        readiness_res = ProposalReadinessGate.check_all(data)
        if not readiness_res.can_proceed:
            raise ValueError(f"Proposal generation blocked by ProposalReadinessGate: {readiness_res.error_messages}")

        # Update data with canonically verified references if modified by readiness gate
        if "reference_live_verification" in readiness_res.module_diagnostics:
            verif_data = readiness_res.module_diagnostics["reference_live_verification"]
            if verif_data.get("verified_studies"):
                data["studies"] = verif_data["verified_studies"]

        # 2. Assemble proposal markdown (defaults to canonical 28-section format)
        is_14_legacy = (format in ["14", "14_sections"] or data.get("format") in ["14", "14_sections"])
        if is_14_legacy:
            md_content = cls.assemble_proposal(data)
            completeness_res = None
        else:
            md_content = cls.assemble_pajooheshyar_28(data)
            completeness_res = MethodologyCompletenessGate.validate(md_content)

        # 3. Apply Persian Medical Typography Linter
        try:
            from persian_medical_typography_linter import PersianMedicalTypographyLinter
            linter = PersianMedicalTypographyLinter()
            md_content = linter.format_text(md_content)
        except Exception:
            pass

        # 3.5 Apply CitationTracker Document-Level Monotonic Vancouver Re-indexing
        try:
            from citation_tracker import CitationTracker
            tracker = CitationTracker()
            for idx, s in enumerate(data.get("studies", [])[:25], 1):
                ckey = s.get("citation_id") or s.get("pmid") or f"ref_{idx}"
                tracker.register_reference(str(ckey), s)
            reindex_res = tracker.reindex_document(md_content, bibliography=tracker._registered_references)
            if reindex_res and reindex_res.rewritten_text:
                md_content = reindex_res.rewritten_text
        except Exception:
            pass

        # 4. Scan for forbidden placeholder tokens (Fail-Closed Sanitization Gate)
        scan_res = FinalTextSanitizationGate.scan_text(md_content)
        if not scan_res["is_clean"]:
            md_content = FinalTextSanitizationGate.sanitize_text(md_content)
            scan_res = FinalTextSanitizationGate.scan_text(md_content)
            if not scan_res["is_clean"]:
                raise ValueError(f"Proposal text contains forbidden placeholder tokens: {scan_res['detected_placeholders']}")

        # Ensure directories exist
        os.makedirs(os.path.dirname(os.path.abspath(md_path)), exist_ok=True)
        os.makedirs(os.path.dirname(os.path.abspath(docx_path)), exist_ok=True)
        
        # Write Markdown
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        # Validate structure
        val_result = ProposalStructureValidator.validate_proposal_text(md_content)
        
        # Build DOCX with Native OMML Math Engine integrated
        DocxBuilder.build_docx(md_content, docx_path)
        
        # Conduct Mock Grant Review Study Section & Inter-Section Semantic Drift Gate
        review_dir = os.path.dirname(os.path.abspath(md_path))
        review_result = MockGrantReviewPanel.conduct_panel_review(md_content, data)
        review_md_path, review_json_path = MockGrantReviewPanel.save_reports(review_result, output_dir=review_dir)

        # Conduct EQUATOR Network & Biological Resource Authentication Audit
        equator_result = EquatorComplianceAuditor.audit_proposal(md_content, data)
        equator_md_path, equator_json_path = EquatorComplianceAuditor.save_reports(equator_result, output_dir=review_dir)

        # Conduct Pre-emptive Risk of Bias (RoB) Mitigation Audit
        rob_result = PreEmptiveRiskOfBiasMitigator.audit_proposal(md_content, data)
        rob_md_path, rob_json_path = PreEmptiveRiskOfBiasMitigator.save_reports(rob_result, output_dir=review_dir)

        # Conduct Epistemic Rigor Audit & Compile Proposal Research Dossier (Two-Loop Pillar 10)
        dossier = data.get("proposal_research_dossier")
        dossier_report = None
        dossier_md_path = None
        dossier_json_path = None
        is_dossier = isinstance(dossier, ProposalResearchDossier) or (
            dossier is not None and getattr(dossier.__class__, "__name__", "") == "ProposalResearchDossier"
        )
        if is_dossier:
            dossier_report = dossier.audit_report if dossier.is_sealed else dossier.seal_dossier()
            dossier_json_path = os.path.join(review_dir, "PROPOSAL_RESEARCH_DOSSIER.json")
            dossier_md_path = os.path.join(review_dir, "PROPOSAL_RESEARCH_DOSSIER.md")
            dossier.export_json(dossier_json_path)
            dossier.export_markdown(dossier_md_path)

        final_status = "PASS"
        if not is_14_legacy and completeness_res:
            final_status = "PASS" if completeness_res.can_proceed else "FAIL"
        else:
            final_status = val_result.get("PROPOSAL_STRUCTURE_VALIDATION", "PASS")

        return {
            "validation": val_result,
            "readiness": readiness_res.to_dict(),
            "completeness": completeness_res.to_dict() if completeness_res else None,
            "mock_grant_review": review_result.to_dict(),
            "mock_grant_review_md": review_md_path,
            "mock_grant_review_json": review_json_path,
            "equator_audit": equator_result.to_dict(),
            "equator_audit_md": equator_md_path,
            "equator_audit_json": equator_json_path,
            "risk_of_bias": rob_result.to_dict(),
            "risk_of_bias_md": rob_md_path,
            "risk_of_bias_json": rob_json_path,
            "dossier_audit": dossier_report,
            "dossier_md": dossier_md_path,
            "dossier_json": dossier_json_path,
            "md_path": md_path,
            "docx_path": docx_path,
            "status": final_status,
            "sanitization": scan_res
        }

def main():
    parser = argparse.ArgumentParser(description="Generate 14-section medical research proposal")
    parser.add_argument("--fixture", type=str, help="Path to fixture or proposal data JSON")
    parser.add_argument("--output-md", type=str, help="Path to output Markdown file")
    parser.add_argument("--output-docx", type=str, help="Path to output Word DOCX file")
    args = parser.parse_args()

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
    
    # Resolve fixture path
    fixture_path = args.fixture
    if not fixture_path:
        default_benchmark = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tests", "fixtures", "benchmark_dataset", "benchmark_proposal_data.json"))
        if os.path.exists(default_benchmark):
            fixture_path = default_benchmark
        else:
            fixture_path = os.path.join(base_dir, "tests", "fixtures", "oncology_lupeol_ndv", "fixture_data.json")

    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    md_out = args.output_md or os.path.join(base_dir, "proposal", "MEDICAL_PROPOSAL_LUPEOL_NDV.md")
    docx_out = args.output_docx or os.path.join(base_dir, "proposal", "MEDICAL_PROPOSAL_LUPEOL_NDV.docx")

    res = ProposalGenerator.generate_and_save(data, md_out, docx_out)
    print("Proposal Generation Status:", res["status"])
    print("Markdown:", res["md_path"])
    print("Word DOCX:", res["docx_path"])

CompliantProposalGenerator = ProposalGenerator

if __name__ == "__main__":
    main()
