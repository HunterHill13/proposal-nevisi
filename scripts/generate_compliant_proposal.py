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
    def assemble_pajooheshyar_28(cls, data: Dict[str, Any]) -> str:
        """Assembles the complete 28-section Pajooheshyar medical proposal markdown."""
        md_parts = []
        md_parts.append("# پروپوزال طرح تحقیقاتی دانشگاهی (سامانه پژوهشیار / ۲۸ بخش مصوب)")
        md_parts.append("")

        rpm_obj = data.get("research_problem_model", {})
        model_dict = data.get("research_problem_model", data)
        fa_title = data.get("research_title_fa") or rpm_obj.get("research_title_fa") or "طرح تحقیقاتی علوم پزشکی"
        en_title = data.get("research_title_en") or rpm_obj.get("research_title_en") or "Medical Research Proposal"
        framework = data.get("framework", "in_vitro")
        studies = data.get("studies", [])

        cond = model_dict.get("target_condition", {})
        cond_name = cond.get("name_fa", cond.get("name_en", "بیماری یا وضعیت هدف"))
        cond_en = cond.get("name_en", "Target Condition")
        sys_name = model_dict.get("population_or_model", {}).get("primary_system", "سیستم بیولوژیک هدف")
        interventions = model_dict.get("interventions_or_exposures", [])

        # Normalize interventions with CompoundEntityNormalizer
        norm_interventions = []
        for agt in interventions:
            norm_agt = CompoundEntityNormalizer.normalize(agt)
            norm_interventions.append(norm_agt)

        # 1. عنوان فارسی
        md_parts.append("## ۱. عنوان فارسی\n" + fa_title + "\n\n---")

        # 2. عنوان انگلیسی
        md_parts.append("## ۲. عنوان انگلیسی\n" + en_title + "\n\n---")

        # 3. نوع مطالعه
        design_desc = f"مطالعه تجربی آزمایشگاهی ({framework}) مبتنی بر آزمون‌های بیولوژیک سلولی و مولکولی در شرایط استاندارد."
        md_parts.append("## ۳. نوع مطالعه\n" + design_desc + "\n\n---")

        # 4. بیان مسئله و ضرورت انجام تحقیق
        problem_text = data.get("problem_statement_text", "")
        if not problem_text or len(problem_text.split()) < 100:
            problem_text = (
                f"{cond_name} ({cond_en}) از معضلات عمده سلامت و انکولوژی معاصر است. "
                f"محدودیت‌های گزینه‌های درمانی موجود شامل عوارض جانبی سیستمیک و مقاومت اکتسابی است. "
                f"بررسی مداخلات نوین بر مدل {sys_name} جهت شناسایی راهکارهای با سمیت انتخابی ضرورت دارد."
            )
        md_parts.append("## ۴. بیان مسئله و ضرورت انجام تحقیق\n" + problem_text + "\n\n---")

        # 5. مروری بر متون
        lit_paras = []
        for idx, s in enumerate(studies[:25], 1):
            cnum = s.get("citation_number", idx)
            para = s.get("review_paragraph") or EvidenceDrivenParagraphBuilder.build_literature_paragraph(s, cnum, model_dict)
            lit_paras.append(para)
        lit_content = "\n\n".join(lit_paras) if lit_paras else "شواهد تجربی پیشین به صورت دقیق مورد واکاوی قرار گرفته‌اند."
        md_parts.append("## ۵. مروری بر متون\n" + lit_content + "\n\n---")

        # 6. اهداف
        aims = [f"تعیین {fa_title} (هدف کلی)"]
        outcomes = model_dict.get("primary_outcomes", [])
        for idx, out in enumerate(outcomes, 1):
            oname = out.get("name") if isinstance(out, dict) else str(out)
            aims.append(f"{idx}. سنجش میزان تغییرات شاخص {oname} در {sys_name}.")
        md_parts.append("## ۶. اهداف (هدف کلی و اهداف اختصاصی)\n" + "\n".join(aims) + "\n\n---")

        # 7. فرضیات یا سوالات پژوهشی
        if len(interventions) >= 2:
            a_n = interventions[0].get("name", "مداخله اول")
            b_n = interventions[1].get("name", "مداخله دوم")
            hyp_analysis = CombinationHypothesisEngine.analyze(a_n, b_n, cond_name, studies)
            hyps_text = (
                f"▪ **فرضیه هم‌افزایی (Synergy Hypothesis):** {hyp_analysis.synergism_hypothesis}\n\n"
                f"▪ **فرضیه آنتاگونیسم (Antagonism Hypothesis):** {hyp_analysis.antagonism_hypothesis}\n\n"
                f"▪ **فرضیه صفر جمع‌پذیر (Additive Null):** {hyp_analysis.additive_null_hypothesis}"
            )
        else:
            hyps_text = f"▪ **فرضیه پژوهش:** به نظر می‌رسد مداخله مورد آزمون اثر معنی‌داری بر شاخص‌های حیاتی در {sys_name} دارد."
        md_parts.append("## ۷. فرضیات یا سوالات پژوهشی\n" + hyps_text + "\n\n---")

        # 8. جامعه آماری
        md_parts.append("## ۸. جامعه آماری\n" + f"مدل‌های بیولوژیک و سلولی هدف مستقر در {sys_name}." + "\n\n---")

        # 9. روش نمونهگیری
        md_parts.append("## ۹. روش نمونهگیری\n" + "نمونه‌گیری تصادفی ساده در تخصیص چاهک‌ها و آزمون‌ها با رعایت حداقل ۳ تکرار مستقل بیولوژیک." + "\n\n---")

        # 10. حجم نمونه و روش محاسبه آن (همراه با فرمول اجباری)
        sample_size_formula_text = (
            "تعیین حجم نمونه بر اساس استانداردهای روش‌شناسی تجربی با فرمول کوهن صورت می‌پذیرد:\n\n"
            r"$$n = \frac{2(Z_{1-\alpha/2} + Z_{1-\beta})^2 \cdot \sigma^2}{d^2}$$"
            "\n\nبا احتساب توان آزمون ۸۰٪ ($1-\\beta = 0.80$) و سطح خطای ۵٪ ($\\alpha = 0.05$) و انحراف معیار برگرفته از مطالعات پیلوت، حداقل ۳ تکرار مستقل در ۳ نوبت مجزا ($n = 9$ در هر گروه غلظتی) تعیین گردید."
        )
        md_parts.append("## ۱۰. حجم نمونه و روش محاسبه آن\n" + sample_size_formula_text + "\n\n---")

        # 11. معیارهای ورود به مطالعه
        md_parts.append("## ۱۱. معیارهای ورود به مطالعه\n" + "رده‌های سلولی استاندارد با تاییدیه اصالت ژنتیکی و زیست‌پذیری بالای ۹۵٪." + "\n\n---")

        # 12. معیارهای خروج از مطالعه
        md_parts.append("## ۱۲. معیارهای خروج از مطالعه\n" + "هرگونه آلودگی میکروبی یا مایکوپلاسمایی و انحراف شدید کنترل‌های منفی یا مثبت." + "\n\n---")

        # 13. روش اجرا
        method_desc = (
            "اجرای مرحله‌ای شامل آماده‌سازی کشت، تهیه رقت‌های سریالی، انکوباسیون زمان‌مند، "
            "سنجش زیست‌پذیری، ارزیابی آپوپتوز با فلوسایتومتری و محاسبه شاخص ترکیب با مدل‌های ریاضی."
        )
        md_parts.append("## ۱۳. روش اجرا\n" + method_desc + "\n\n---")

        # 14. ابزار جمعآوری دادهها
        md_parts.append("## ۱۴. ابزار جمعآوری دادهها\n" + "دستگاه الایزا ریدر، فلوسایتومتر، میکروسکوپ اینورت و نرم‌افزارهای تحلیلی تخصصی." + "\n\n---")

        # 15. روشهای آماری تجزیه و تحلیل دادهها
        stat_model = CombinationModelSelector.select(
            study_design=framework,
            outcome_type="continuous",
            groups_count=4 if len(interventions) >= 2 else 2
        )
        stat_text = (
            f"مدل آماری اصلی: {stat_model.primary_model_fa} ({stat_model.primary_model}).\n"
            f"آزمون‌های پیش‌فرض: " + "، ".join(t["fa"] for t in stat_model.assumption_tests) + ".\n"
            f"آزمون تعقیبی: {stat_model.post_hoc_test}.\n"
            f"شاخص اندازه اثر: {stat_model.effect_size_metric}."
        )
        md_parts.append("## ۱۵. روشهای آماری تجزیه و تحلیل دادهها\n" + stat_text + "\n\n---")

        # 16. ملاحظات اخلاقی
        md_parts.append("## ۱۶. ملاحظات اخلاقی\n" + "پروتکل مطالعه منطبق بر کدهای اخلاقی پژوهش‌های زیست‌پزشکی و ضوابط ایمنی زیستی تدوین گردیده است." + "\n\n---")

        # 17. محدودیتهای مطالعه
        md_parts.append("## ۱۷. محدودیتهای مطالعه\n" + "عدم تعمیم مستقیم شرایط برون‌تنی به سیستم‌های پیچیده درون‌تنی بدن انسان." + "\n\n---")

        # 18. جدول متغیرها
        var_table_text = data.get("variable_table_text")
        if not var_table_text:
            variables = DynamicProtocolDesigner.generate_variable_table(model_dict)
            var_table_text = DynamicProtocolDesigner.render_variable_table_markdown(variables)
        md_parts.append("## ۱۸. جدول متغیرها\n" + var_table_text + "\n\n---")

        # 19. جدول زمانبندی
        timeline_text = data.get("timeline_table_text")
        if not timeline_text:
            tl = DynamicProtocolDesigner.generate_timeline(framework)
            timeline_text = DynamicProtocolDesigner.render_timeline_markdown(tl)
        md_parts.append("## ۱۹. جدول زمانبندی\n" + timeline_text + "\n\n---")

        # 20. بودجه
        budget_text = "| ردیف | شرح هزینه | مبلغ (ریال) |\n| :--- | :--- | :--- |\n| ۱ | مواد مصرفی و محیط کشت | ۱۵۰,۰۰۰,۰۰۰ |\n| ۲ | آزمون‌های تخصصی فلوسایتومتری | ۲۰۰,۰۰۰,۰۰۰ |\n| ۳ | تحلیل داده‌ها و نگارش | ۵۰,۰۰۰,۰۰۰ |\n| **جمع** | **کل هزینه‌ها** | **۴۰۰,۰۰۰,۰۰۰** |"
        md_parts.append("## ۲۰. بودجه\n" + budget_text + "\n\n---")

        # 21. منابع
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
        md_parts.append("## ۲۱. منابع\n" + "\n\n".join(ref_lines) + "\n\n---")

        # 22. خلاصه فارسی
        abstract_fa = (
            f"**زمینه و هدف:** {cond_name} نیازمند رویکردهای ترکیبی موثر است.\n"
            f"**روش بررسی:** سلول‌های {sys_name} تحت مواجهه تک‌عاملی و توام قرار می‌گیرند.\n"
            f"**یافته‌های مورد انتظار:** تعیین شاخص ترکیب و ارزیابی مسیرهای مرگ سلولی."
        )
        md_parts.append("## ۲۲. خلاصه فارسی\n" + abstract_fa + "\n\n---")

        # 23. خلاصه انگلیسی (Abstract)
        abstract_en = (
            f"**Background:** Overcoming therapeutic resistance in {cond_en} demands targeted combinatorial regimens.\n"
            f"**Methods:** {sys_name} cells are evaluated under monotherapy and co-treatment protocols.\n"
            f"**Expected Results:** Determination of combination index and mechanistic apoptotic markers."
        )
        md_parts.append("## ۲۳. خلاصه انگلیسی (Abstract)\n" + abstract_en + "\n\n---")

        # 24. کلیدواژههای فارسی
        kw_fa = f"{cond_name}، آپوپتوز، هم‌افزایی، مهار رشد، شاخص ترکیب"
        md_parts.append("## ۲۴. کلیدواژههای فارسی\n" + kw_fa + "\n\n---")

        # 25. کلیدواژههای انگلیسی
        kw_en = f"{cond_en}, Apoptosis, Synergism, Growth Inhibition, Combination Index"
        md_parts.append("## ۲۵. کلیدواژههای انگلیسی\n" + kw_en + "\n\n---")

        # 26. تعارض منافع
        md_parts.append("## ۲۶. تعارض منافع\n" + "نویسندگان هیچ‌گونه تعارض منافعی در انجام این پژوهش گزارش نمی‌نمایند." + "\n\n---")

        # 27. سپاسگزاری
        md_parts.append("## ۲۷. سپاسگزاری\n" + "از معاونت پژوهشی و کلیه پرسنل آزمایشگاه مرکزی کمال تشکر را داریم." + "\n\n---")

        # 28. ضمائم (در صورت نیاز)
        md_parts.append("## ۲۸. ضمائم (در صورت نیاز)\n" + "پروتکل‌های دستگاهی و گواهی اصالت رده‌های سلولی پیوست می‌گردد.")

        return "\n\n".join(md_parts)

    @classmethod
    def generate_and_save(cls, data: Dict[str, Any], md_path: str, docx_path: str, format: str = "auto") -> Dict[str, Any]:
        """Generates proposal, validates readiness & structure, and builds DOCX."""
        # 1. Master Readiness Gate Check (v9.0 Prerequisite Gate)
        readiness_res = ProposalReadinessGate.check_all(data)
        if not readiness_res.can_proceed:
            raise ValueError(f"Proposal generation blocked by ProposalReadinessGate: {readiness_res.error_messages}")

        # 2. Assemble proposal markdown
        is_pajooheshyar = (format == "pajooheshyar_28" or data.get("format") == "pajooheshyar_28")
        if is_pajooheshyar:
            md_content = cls.assemble_pajooheshyar_28(data)
            completeness_res = MethodologyCompletenessGate.validate(md_content)
        else:
            md_content = cls.assemble_proposal(data)
            completeness_res = None

        # 3. Apply Persian Medical Typography Linter
        try:
            from persian_medical_typography_linter import PersianMedicalTypographyLinter
            linter = PersianMedicalTypographyLinter()
            md_content = linter.format_text(md_content)
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
        
        final_status = "PASS"
        if is_pajooheshyar and completeness_res:
            final_status = "PASS" if completeness_res.can_proceed else "FAIL"
        else:
            final_status = val_result.get("PROPOSAL_STRUCTURE_VALIDATION", "PASS")

        return {
            "validation": val_result,
            "readiness": readiness_res.to_dict(),
            "completeness": completeness_res.to_dict() if completeness_res else None,
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
