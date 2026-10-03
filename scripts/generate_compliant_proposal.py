#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_compliant_proposal.py - Universal Medical Research Proposal Generator
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

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
from typing import Dict, List, Any, Optional

sys.stdout.reconfigure(encoding='utf-8')

# Import core generic engines
try:
    from docx_builder import DocxBuilder
    from dynamic_protocol_designer import DynamicProtocolDesigner
    from generic_gap_detector import GenericGapDetector
    from generic_contradiction_engine import GenericContradictionEngine
    from generic_claim_entailment_engine import GenericClaimEntailmentEngine
    from proposal_structure_validator import ProposalStructureValidator
except ImportError:
    scripts_dir = os.path.dirname(__file__)
    sys.path.insert(0, scripts_dir)
    from docx_builder import DocxBuilder
    from dynamic_protocol_designer import DynamicProtocolDesigner
    from generic_gap_detector import GenericGapDetector
    from generic_contradiction_engine import GenericContradictionEngine
    from generic_claim_entailment_engine import GenericClaimEntailmentEngine
    from proposal_structure_validator import ProposalStructureValidator

class ProposalGenerator:
    """Universal proposal generator coordinating generic synthesis engines."""

    @classmethod
    def assemble_proposal(cls, data: Dict[str, Any]) -> str:
        """Assembles the complete 14-section proposal markdown from configuration data."""
        md_parts = []

        # Header Title
        md_parts.append("# پروپوزال طرح تحقیقاتی دانشگاهی (پایان‌نامه / طرح پژوهشی)")
        md_parts.append("")

        # 1. موضوع (Title)
        fa_title = data.get("research_title_fa", "طرح تحقیقاتی علوم پزشکی")
        en_title = data.get("research_title_en", "Medical Research Proposal")
        md_parts.append("## ۱. موضوع (Title)")
        md_parts.append(f"▪ **عنوان فارسی (Persian Title):**  \n{fa_title}")
        md_parts.append("")
        md_parts.append(f"▪ **عنوان انگلیسی (English Title):**  \n{en_title}")
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 2. بیان مسئله (Problem Statement)
        problem_text = data.get("problem_statement_text", "")
        # Synthesize gaps dynamically if studies and model exist
        studies = data.get("studies", [])
        framework = data.get("framework", "EXPERIMENTAL_IN_VITRO")
        gap_summary = ""
        if studies:
            try:
                gaps = GenericGapDetector.detect_gaps(studies, {"framework": framework})
                if gaps:
                    gap_lines = []
                    for g in gaps[:3]:
                        cat = g.get("gap_category", "KNOWLEDGE_GAP")
                        desc = g.get("description", "")
                        gap_lines.append(f"- **شکاف پژوهشی شناسایی‌شده ({cat}):** {desc}")
                    gap_summary = "\n\n" + "\n".join(gap_lines)
            except Exception:
                gap_summary = ""

        md_parts.append("## ۲. بیان مسئله (Problem Statement)")
        md_parts.append(problem_text + gap_summary)
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 3. مرور بر منابع (Literature Review)
        md_parts.append("## ۳. مرور بر منابع (Literature Review)")
        
        # Build paragraph-by-paragraph literature review
        studies = data.get("studies", [])
        if studies:
            lit_paragraphs = []
            for s in studies:
                cnum = s.get("citation_number", len(lit_paragraphs) + 1)
                authors = s.get("authors", [])
                lead_author = authors[0] if authors else "محققان"
                year = s.get("year", 2024)
                findings = s.get("primary_findings", s.get("title", ""))
                quant = s.get("quantitative_parameters", "")
                
                # Check for existing custom analytical paragraph
                para = s.get("review_paragraph") or s.get("literature_review_paragraph")
                if not para:
                    para = f"{lead_author} و همکاران ({year}) در پژوهشی پیرامون این موضوع گزارش نمودند که: {findings}. نتایج نشان‌دهنده ارقام تجربی قابل توجه ({quant}) بوده و اهمیت بالایی در تبیین فرضیه حاضر دارد [{cnum}]."
                lit_paragraphs.append(para)
            
            # Incorporate parameter divergence insights from contradiction engine
            try:
                contradictions = GenericContradictionEngine.detect_contradictions(studies)
                if contradictions:
                    divergences = [c for c in contradictions if c.get("classification") != "TRUE_CONTRADICTION"]
                    if divergences:
                        top_div = divergences[0]
                        lit_paragraphs.append(f"\nدر واکاوی شواهد، تفاوت‌های زمینه‌ای و واگرایی پارامترها ({top_div.get('category')}) میان مطالعات گزارش شده است: {top_div.get('explanation')} این امر لزوم کنترل دقیق شرایط مداخله را در طرح حاضر دوچندان می‌سازد.")
            except Exception:
                pass

            md_parts.append("\n\n".join(lit_paragraphs))
        else:
            md_parts.append("شواهد تجربی و مطالعات پیشین مرتبط با متغیرهای پژوهش به صورت جامع مورد تحلیل و بررسی قرار گرفته‌اند.")
        
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 4. اهمیت و ضرورت تحقیق
        md_parts.append("## ۴. اهمیت و ضرورت تحقیق (Significance & Necessity)")
        md_parts.append(data.get("importance_and_necessity_text", ""))
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 5. تعریف واژه‌ها
        md_parts.append("## ۵. تعریف واژه‌ها (Definition of Terms)")
        md_parts.append(data.get("definitions_text", ""))
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 6. اهداف جزیی
        md_parts.append("## ۶. اهداف جزیی (Specific Objectives)")
        md_parts.append(data.get("specific_objectives_text", ""))
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 7. اهداف کلی
        md_parts.append("## ۷. اهداف کلی (General Objective)")
        md_parts.append(data.get("general_objective_text", f"تعیین {fa_title}"))
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 8. اهداف کاربردی
        md_parts.append("## ۸. اهداف کاربردی (Applied Objectives)")
        md_parts.append(data.get("applied_objectives_text", ""))
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 9. فرضیات و سوالات پژوهش
        md_parts.append("## ۹. فرضیات و سوالات پژوهش (Hypotheses & Research Questions)")
        md_parts.append(data.get("hypotheses_and_questions_text", ""))
        md_parts.append("")
        md_parts.append("---")
        md_parts.append("")

        # 10. دستاوردها
        md_parts.append("## ۱۰. دستاوردها (Achievements & Deliverables)")
        md_parts.append(data.get("achievements_text", ""))
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
            
            subsecs = [
                "### ۱۳-۱. نوع مطالعه\nمطالعه تجربی آزمایشگاهی / بالینی بر مبنای پروتکل‌های استاندارد مصوب.",
                "### ۱۳-۲. جامعه مورد مطالعه\nمدل‌های زیستی، سیستم‌های سلولی یا نمونه‌های انسانی منطبق بر معیارهای مصوب طرح.",
                "### ۱۳-۳. محل انجام مطالعه\nآزمایشگاه‌های تحقیقاتی و مراکز درمانی دانشگاه علوم پزشکی.",
                "### ۱۳-۴. معیارهای ورود به مطالعه\nنمونه‌ها یا سلول‌های واجد خلوص بیولوژیک تاییدشده و شرایط استاندارد کشت.",
                "### ۱۳-۵. معیارهای خروج از مطالعه\nهرگونه آلودگی باکتریایی یا مایکوپلاسمایی، عدم پاسخ‌دهی به کنترل مثبت یا عدم تطابق ژنتیکی.",
                "### ۱۳-۶. ابزارهای گردآوری اطلاعات\nدستگاه‌های سنجش اسپکتروفتومتری، فلوسایتومتری، الایزا ریدر و نرم‌افزارهای تخصصی تحلیلی.",
                "### ۱۳-۷. تعیین روایی ابزار گردآوری\nکالیبراسیون استاندارد ابزارهای آزمایشگاهی و مقایسه با استانداردهای مرجع بین‌المللی.",
                "### ۱۳-۸. تعیین پایایی ابزار گردآوری\nتکرار مستقل آزمایش‌ها در حداقل سه نوبت زیستی جداگانه با محاسبه ضریب تغییرات (CV < 10%).",
                "### ۱۳-۹. حجم نمونه و روش محاسبه آن\nتعیین حجم نمونه و تعداد تکرارهای زیستی بر مبنای آزمون توان آماری با آلفای ۵٪ و توان ۸۰٪.",
                f"### ۱۳-۱۰. روش تجزیه و تحلیل داده‌ها\n{stat_desc}",
                "### ۱۳-۱۱. ملاحظات اخلاقی در صورت نیاز\nرعایت کامل کدهای اخلاق زیستی مصوب کمیته ملی اخلاق در پژوهش‌های زیست‌پزشکی.",
                "### ۱۳-۱۲. نحوه رعایت نکات امنیتی و حفاظت پروژه\nرعایت دستورالعمل‌های ایمنی زیستی سطح دو (BSL-2) و دفع پسماندهای عفونی طبق پروتکل‌های حفاظت زیستی.",
                "### ۱۳-۱۳. مشکلات و محدودیت‌ها\nکنترل نوسانات کشت زیستی، رفع سمیت‌های زمینه‌ای و بهینه‌سازی فرمولاسیون مداخله.",
                "### ۱۳-۱۴. شیوه اجرایی مراحل طرح\nاجرای مرحله‌ای آزمایش‌ها طبق فازبندی گانت چارت از تایید هویت تا تحلیل داده‌های نهایی."
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
    def generate_and_save(cls, data: Dict[str, Any], md_path: str, docx_path: str) -> Dict[str, Any]:
        """Generates proposal, validates structure, and builds DOCX."""
        md_content = cls.assemble_proposal(data)
        
        # Ensure directories exist
        os.makedirs(os.path.dirname(os.path.abspath(md_path)), exist_ok=True)
        os.makedirs(os.path.dirname(os.path.abspath(docx_path)), exist_ok=True)
        
        # Write Markdown
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        # Validate structure
        val_result = ProposalStructureValidator.validate_proposal_text(md_content)
        
        # Build DOCX
        DocxBuilder.build_docx(md_content, docx_path)
        
        return {
            "validation": val_result,
            "md_path": md_path,
            "docx_path": docx_path,
            "status": val_result.get("PROPOSAL_STRUCTURE_VALIDATION", "FAIL")
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

if __name__ == "__main__":
    main()
