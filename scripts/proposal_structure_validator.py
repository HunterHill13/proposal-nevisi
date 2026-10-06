#!/usr/bin/env python3
"""
proposal_structure_validator.py - Strict Institutional 14-Section Proposal Structure Gate
Proposal-Nevisi Engine v8.2 (Universal Biomedical Architecture)

Validates that proposal documents (Markdown and compiled DOCX) strictly adhere
to the institutional Iranian medical research structure without section merging,
omission, or ordering drift.
"""

import os
import re
import sys
from typing import Dict, List, Any, Optional
try:
    from core_policies import MANDATORY_28_SECTIONS, MANDATORY_14_SECTIONS, MANDATORY_SUBSECTIONS_13, SECTION_CONTENT_EXPECTATIONS
except ImportError:
    from scripts.core_policies import MANDATORY_28_SECTIONS, MANDATORY_14_SECTIONS, MANDATORY_SUBSECTIONS_13, SECTION_CONTENT_EXPECTATIONS

class ProposalStructureValidator:
    """Validates structural integrity, ordering, and presence of all required sections."""

    @classmethod
    def is_28_section_format(cls, text: str) -> bool:
        """Determines if the proposal text follows the canonical 28-section structure."""
        if re.search(r"(?:^|\n)##?\s*(?:28|۲۸)[\.\-:]?", text):
            return True
        if re.search(r"(?:^|\n)##?\s*(?:14|۱۴)[\.\-:]?\s*(?:نوع\s*مطالعه|study\s*type)", text):
            return True
        if re.search(r"(?:^|\n)##?\s*(?:27|۲۷)[\.\-:]?", text):
            return True
        return False

    @classmethod
    def validate_proposal_text(cls, text: str) -> Dict[str, Any]:
        """Audits markdown proposal text for adherence (supporting 28-section canonical and 14-section legacy)."""
        if cls.is_28_section_format(text):
            return cls.validate_28_section_text(text)
        return cls.validate_14_section_text(text)

    @classmethod
    def validate_28_section_text(cls, text: str) -> Dict[str, Any]:
        """Audits markdown proposal text for canonical 28-section adherence."""
        section_status = []
        last_index = -1
        ordering_violated = False

        PERSIAN_DIGITS = {str(i): "".join("۰۱۲۳۴۵۶۷۸۹"[int(d)] for d in str(i)) for i in range(1, 35)}

        # 1. Audit 28 Top-level sections
        for num, name, patterns in MANDATORY_28_SECTIONS:
            p_num = PERSIAN_DIGITS.get(str(num), str(num))
            pattern_regex = rf"(?:^|\n)##?\s*(?:{num}|{p_num})[\.\-:\s]+[^\n]*?(?:{'|'.join(patterns)})"
            match = re.search(pattern_regex, text, re.IGNORECASE)
            if match:
                found_pos = match.start()
                if found_pos < last_index:
                    ordering_violated = True
                last_index = found_pos
                section_status.append({"section_num": num, "name": name, "found": True, "pos": found_pos})
            else:
                section_status.append({"section_num": num, "name": name, "found": False, "pos": -1})

        missing_sections = [s["name"] for s in section_status if not s["found"]]

        # 2. Check Variable Table and Timeline
        has_var_table = bool(re.search(r"\|\s*نام\s*متغیر\s*\|", text) or re.search(r"\|\s*متغیر\s*\|", text))
        has_timeline = bool(re.search(r"\|\s*فاز[^\n\|]*\|", text) or re.search(r"\|\s*مرحله[^\n\|]*\|", text) or re.search(r"گانت", text) or re.search(r"زمان[\s\-\u200c]*بندی", text))

        # 3. Content Depth Audit
        words = text.split()
        total_word_count = len(words)

        sec_2_match = re.search(r"(?:^|\n)##?\s*(?:2|۲)[\.\-:]?\s*بیان\s*مس[ئأه]له", text)
        sec_3_match = re.search(r"(?:^|\n)##?\s*(?:3|۳)[\.\-:]?\s*مرور\s*بر\s*منابع", text)
        sec_4_match = re.search(r"(?:^|\n)##?\s*(?:4|۴)[\.\-:]?\s*اهمیت\s*و\s*ضرورت", text)

        sec_2_words = 0
        if sec_2_match and sec_3_match:
            sec_2_text = text[sec_2_match.end():sec_3_match.start()]
            sec_2_words = len(sec_2_text.split())

        sec_3_words = 0
        if sec_3_match and sec_4_match:
            sec_3_text = text[sec_3_match.end():sec_4_match.start()]
            sec_3_words = len(sec_3_text.split())

        # 4. Reference count in Section 28 (Ceiling: 25, Floor: 15)
        sec_28_text = ""
        sec_28_match = re.search(r"(?:^|\n)##?\s*(?:28|۲۸)[\.\-:]?\s*(?:منابع|references)", text, re.IGNORECASE)
        if sec_28_match:
            sec_28_text = text[sec_28_match.end():]
        ref_entries = re.findall(r'(?:^|\n)\s*\[\s*\d+\s*\]', sec_28_text)
        ref_count = len(ref_entries)

        ref_count_valid = True
        ref_violation = None
        if sec_28_match and ref_count > 0:
            if ref_count > 25:
                ref_count_valid = False
                ref_violation = f"EXCEEDS_MAX_REFERENCE_CEILING_25 (Count: {ref_count}, Ceiling: 25)"
            elif ref_count < 15:
                ref_count_valid = False
                ref_violation = f"BELOW_MIN_REFERENCE_FLOOR_15 (Count: {ref_count}, Floor: 15)"

        # 5. Check Section 3 for prohibited artificial axis headers
        has_artificial_axis_headers = False
        if sec_3_match and sec_4_match:
            sec_3_body = text[sec_3_match.end():sec_4_match.start()]
            if re.search(r'###\s*محور\s+', sec_3_body) or re.search(r'###\s*Axis\s+', sec_3_body, re.IGNORECASE):
                has_artificial_axis_headers = True

        passed = (
            len(missing_sections) == 0 and
            not ordering_violated and
            has_var_table and
            has_timeline and
            (ref_count_valid or not sec_28_match) and
            not has_artificial_axis_headers
        )

        status_str = "PASS" if passed else "FAIL"

        return {
            "status": status_str,
            "PROPOSAL_STRUCTURE_VALIDATION": status_str,
            "format_detected": "28_SECTIONS",
            "all_28_sections_present": len(missing_sections) == 0,
            "all_14_sections_present": True,
            "all_subsections_13_present": True,
            "section_ordering_intact": not ordering_violated,
            "variable_table_present": has_var_table,
            "timeline_schedule_present": has_timeline,
            "reference_count": ref_count,
            "reference_count_valid": ref_count_valid,
            "reference_ceiling_violation": ref_violation,
            "has_artificial_axis_headers": has_artificial_axis_headers,
            "total_word_count": total_word_count,
            "problem_statement_word_count": sec_2_words,
            "literature_review_word_count": sec_3_words,
            "missing_sections": missing_sections,
            "missing_subsections_13": [],
            "section_audit_details": section_status
        }

    @classmethod
    def validate_14_section_text(cls, text: str) -> Dict[str, Any]:
        """Audits markdown proposal text for 14-section adherence."""
        section_status = []
        last_index = -1
        ordering_violated = False

        PERSIAN_DIGITS = {
            "1": "۱", "2": "۲", "3": "۳", "4": "۴", "5": "۵",
            "6": "۶", "7": "۷", "8": "۸", "9": "۹", "10": "۱۰",
            "11": "۱۱", "12": "۱۲", "13": "۱۳", "14": "۱۴"
        }

        # 1. Audit 14 Top-level sections
        for num, name, patterns in MANDATORY_14_SECTIONS:
            p_num = PERSIAN_DIGITS.get(str(num), str(num))
            pattern_regex = rf"(?:^|\n)##?\s*(?:{num}|{p_num})[\.\-:\s]+[^\n]*?(?:{'|'.join(patterns)})"
            match = re.search(pattern_regex, text, re.IGNORECASE)
            if match:
                found_pos = match.start()
                if found_pos < last_index:
                    ordering_violated = True
                last_index = found_pos
                section_status.append({"section_num": num, "name": name, "found": True, "pos": found_pos})
            else:
                section_status.append({"section_num": num, "name": name, "found": False, "pos": -1})

        missing_sections = [s["name"] for s in section_status if not s["found"]]

        # 2. Audit Section 13 Sub-sections
        sec_13_text = ""
        sec_13_match = re.search(r"(?:^|\n)##?\s*(?:13|۱۳)[\.\-:]?\s*(?:روش\s*اجرا|متدولوژی)", text)
        sec_14_match = re.search(r"(?:^|\n)##?\s*(?:14|۱۴)[\.\-:]?\s*(?:منابع|فهرست\s*منابع)", text)
        if sec_13_match:
            start_pos = sec_13_match.end()
            end_pos = sec_14_match.start() if sec_14_match else len(text)
            sec_13_text = text[start_pos:end_pos]

        subsec_status = []
        for sub_id, sub_name, patterns in MANDATORY_SUBSECTIONS_13:
            p_sub_id = sub_id.replace("13-", "۱۳-")
            for en_d, fa_d in [("1", "۱"), ("2", "۲"), ("3", "۳"), ("4", "۴"), ("5", "۵"), ("6", "۶"), ("7", "۷"), ("8", "۸"), ("9", "۹"), ("0", "۰")]:
                p_sub_id = p_sub_id.replace(en_d, fa_d)
            pattern_regex = rf"(?:^|\n)###?\s*(?:{sub_id}|{p_sub_id})[\.\-:\s]+[^\n]*?(?:{'|'.join(patterns)})"
            found = bool(re.search(pattern_regex, sec_13_text, re.IGNORECASE))
            subsec_status.append({"subsection_id": sub_id, "name": sub_name, "found": found})

        missing_subsections = [s["name"] for s in subsec_status if not s["found"]]

        # 3. Check Variable Table and Timeline
        has_var_table = bool(re.search(r"\|\s*نام\s*متغیر\s*\|", text) or re.search(r"\|\s*متغیر\s*\|", text))
        has_timeline = bool(re.search(r"\|\s*فاز[^\n\|]*\|", text) or re.search(r"\|\s*مرحله[^\n\|]*\|", text) or re.search(r"گانت", text) or re.search(r"زمان[\s\-\u200c]*بندی", text))

        # 4. Content Depth Audit (Minimum Word Counts & Substantive Proportions)
        words = text.split()
        total_word_count = len(words)
        
        # Word counts per section
        sec_2_match = re.search(r"(?:^|\n)##?\s*(?:2|۲)[\.\-:]?\s*بیان\s*مس[ئأه]له", text)
        sec_3_match = re.search(r"(?:^|\n)##?\s*(?:3|۳)[\.\-:]?\s*مرور\s*بر\s*منابع", text)
        sec_4_match = re.search(r"(?:^|\n)##?\s*(?:4|۴)[\.\-:]?\s*اهمیت\s*و\s*ضرورت", text)
        
        sec_2_words = 0
        if sec_2_match and sec_3_match:
            sec_2_text = text[sec_2_match.end():sec_3_match.start()]
            sec_2_words = len(sec_2_text.split())
            
        sec_3_words = 0
        if sec_3_match and sec_4_match:
            sec_3_text = text[sec_3_match.end():sec_4_match.start()]
            sec_3_words = len(sec_3_text.split())
        
        # 5. Reference count and Section 14 ceiling audit (Strict 15-25 References)
        sec_14_text = ""
        sec_14_match = re.search(r"(?:^|\n)##?\s*(?:14|۱۴)[\.\-:]?\s*(?:منابع|فهرست\s*منابع|references)", text, re.IGNORECASE)
        if sec_14_match:
            sec_14_text = text[sec_14_match.end():]
        ref_entries = re.findall(r'(?:^|\n)\s*\[\s*\d+\s*\]', sec_14_text)
        ref_count = len(ref_entries)
        
        ref_count_valid = True
        ref_violation = None
        if sec_14_match and ref_count > 0:
            if ref_count > 25:
                ref_count_valid = False
                ref_violation = f"EXCEEDS_MAX_REFERENCE_CEILING_25 (Count: {ref_count}, Ceiling: 25)"
            elif ref_count < 15:
                ref_count_valid = False
                ref_violation = f"BELOW_MIN_REFERENCE_FLOOR_15 (Count: {ref_count}, Floor: 15)"

        # 6. Check Section 3 for prohibited artificial axis grouping headers
        has_artificial_axis_headers = False
        if sec_3_match and sec_4_match:
            sec_3_body = text[sec_3_match.end():sec_4_match.start()]
            if re.search(r'###\s*محور\s+', sec_3_body) or re.search(r'###\s*Axis\s+', sec_3_body, re.IGNORECASE):
                has_artificial_axis_headers = True

        passed = (
            len(missing_sections) == 0 and
            len(missing_subsections) == 0 and
            not ordering_violated and
            has_var_table and
            has_timeline and
            (ref_count_valid or not sec_14_match) and
            not has_artificial_axis_headers
        )

        status_str = "PASS" if passed else "FAIL"

        return {
            "status": status_str,
            "PROPOSAL_STRUCTURE_VALIDATION": status_str,
            "all_14_sections_present": len(missing_sections) == 0,
            "all_subsections_13_present": len(missing_subsections) == 0,
            "section_ordering_intact": not ordering_violated,
            "variable_table_present": has_var_table,
            "timeline_schedule_present": has_timeline,
            "reference_count": ref_count,
            "reference_count_valid": ref_count_valid,
            "reference_ceiling_violation": ref_violation,
            "has_artificial_axis_headers": has_artificial_axis_headers,
            "total_word_count": total_word_count,
            "problem_statement_word_count": sec_2_words,
            "literature_review_word_count": sec_3_words,
            "missing_sections": missing_sections,
            "missing_subsections_13": missing_subsections,
            "section_audit_details": section_status
        }

    @classmethod
    def validate_proposal_consistency(cls, model_or_proposal_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Validates directed consistency graph across Title -> Question -> Objectives -> Hypotheses -> Variables -> Outcomes -> Design -> Analysis -> Conclusion Scope (Part 12)."""
        title = model_or_proposal_dict.get("research_title_fa") or model_or_proposal_dict.get("research_title_en") or ""
        cond = model_or_proposal_dict.get("target_condition", {})
        cond_name = cond.get("name_en") or cond.get("name_fa") or ""
        interventions = model_or_proposal_dict.get("interventions_or_exposures", [])
        outcomes = model_or_proposal_dict.get("primary_outcomes", [])
        framework = model_or_proposal_dict.get("framework", "")
        stat_plan = model_or_proposal_dict.get("statistical_analysis_plan", {})
        
        flags = []
        checks = {}

        # 1. Condition reflected in title
        has_cond_in_title = bool(cond_name and (cond_name.lower() in title.lower() or any(w.lower() in title.lower() for w in cond_name.split() if len(w) > 3)))
        checks["condition_in_title"] = has_cond_in_title or len(title) == 0
        if not checks["condition_in_title"]:
            flags.append("TITLE_CONDITION_MISMATCH")

        # 2. Interventions aligned with objectives/hypotheses
        agent_names = [a.get("name", "") for a in interventions if a.get("name")]
        checks["interventions_specified"] = len(agent_names) > 0 or framework in ["OBSERVATIONAL", "PECO"]
        if not checks["interventions_specified"]:
            flags.append("MISSING_INTERVENTIONS_IN_EXPERIMENTAL_GRAPH")

        # 3. Outcomes defined and linked
        outcome_names = [o.get("name", "") for o in outcomes if o.get("name")]
        checks["outcomes_specified"] = len(outcome_names) > 0
        if not checks["outcomes_specified"]:
            flags.append("MISSING_PRIMARY_OUTCOMES_GRAPH")

        # 4. Statistical plan matches framework
        primary_test = str(stat_plan.get("primary_analysis", ""))
        test_matches_design = True
        if framework == "DIAGNOSTIC" and "حساسیت" not in primary_test and "sensitivity" not in primary_test.lower() and "roc" not in primary_test.lower():
            test_matches_design = False
            flags.append("DIAGNOSTIC_FRAMEWORK_ANALYSIS_MISMATCH")
        elif framework == "PICO" and "itt" not in primary_test.lower() and "قصد درمان" not in primary_test and "cox" not in primary_test.lower() and "anova" not in primary_test.lower() and "t-test" not in primary_test.lower():
            test_matches_design = False
            flags.append("CLINICAL_TRIAL_ANALYSIS_MISMATCH")

        checks["statistical_analysis_aligned"] = test_matches_design

        is_consistent = len(flags) == 0

        return {
            "consistency_status": "GRAPH_CONSISTENT" if is_consistent else "CONSISTENCY_BREACH",
            "is_internally_consistent": is_consistent,
            "consistency_checks": checks,
            "detected_inconsistencies": flags,
            "directed_graph_path": "Title -> Question -> Objectives -> Hypotheses -> Variables -> Outcomes -> Design -> Analysis -> Conclusion Scope"
        }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            target_text = f.read()
        res = ProposalStructureValidator.validate_proposal_text(target_text)
        print("Validation Status:", res["PROPOSAL_STRUCTURE_VALIDATION"])
        if res["PROPOSAL_STRUCTURE_VALIDATION"] != "PASS":
            print("Missing sections:", res["missing_sections"])
            print("Missing subsections:", res["missing_subsections_13"])
            print("Ordering intact:", res["section_ordering_intact"])
    else:
        demo_text = """
        # 1. موضوع تحقیق
        ## 2. بیان مسئله
        ## 3. مرور بر منابع
        ## 4. اهمیت و ضرورت تحقیق
        ## 5. تعریف واژه‌ها
        ## 6. اهداف جزیی
        ## 7. اهداف کلی
        ## 8. اهداف کاربردی
        ## 9. فرضیات و سوالات
        ## 10. دستاوردها
        ## 11. جدول متغیرها
        | نام متغیر | نقش متغیر | نوع متغیر | تعریف عملیاتی | نحوه اندازه‌گیری |
        | متغیر A | مستقل | کیفی | تعریف | روش |
        ## 12. جدول زمان‌بندی و مراحل اجرا
        | فاز | ماه |
        | ۱ | ۲ |
        ## 13. روش اجرا
        ### 13-1. نوع مطالعه
        ### 13-2. جامعه مورد مطالعه
        ### 13-3. محل انجام مطالعه
        ### 13-4. معیارهای ورود به مطالعه
        ### 13-5. معیارهای خروج از مطالعه
        ### 13-6. ابزارهای گردآوری اطلاعات
        ### 13-7. تعیین روایی ابزار
        ### 13-8. تعیین پایایی ابزار
        ### 13-9. حجم نمونه و روش محاسبه آن
        ### 13-10. روش تجزیه و تحلیل داده
        ### 13-11. ملاحظات اخلاقی در صورت نیاز
        ### 13-12. نحوه رعایت نکات امنیتی و حفاظت پروژه
        ### 13-13. مشکلات و محدودیت‌ها
        ### 13-14. شیوه اجرایی مراحل طرح
        ## 14. فهرست منابع
        [1] Author et al.
        """
        res = ProposalStructureValidator.validate_proposal_text(demo_text)
        print("Demo Validation Status:", res["PROPOSAL_STRUCTURE_VALIDATION"])
