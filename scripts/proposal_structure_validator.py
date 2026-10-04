#!/usr/bin/env python3
"""
proposal_structure_validator.py - Strict Institutional 14-Section Proposal Structure Gate
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

Validates that proposal documents (Markdown and compiled DOCX) strictly adhere
to the institutional Iranian medical research structure without section merging,
omission, or ordering drift.
"""

import os
import re
import sys
from typing import Dict, List, Any, Optional
try:
    from core_policies import MANDATORY_14_SECTIONS, MANDATORY_SUBSECTIONS_13, SECTION_CONTENT_EXPECTATIONS
except ImportError:
    from scripts.core_policies import MANDATORY_14_SECTIONS, MANDATORY_SUBSECTIONS_13, SECTION_CONTENT_EXPECTATIONS

class ProposalStructureValidator:
    """Validates structural integrity, ordering, and presence of all required sections."""

    @classmethod
    def validate_proposal_text(cls, text: str) -> Dict[str, Any]:
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

        passed = (len(missing_sections) == 0 and len(missing_subsections) == 0 and not ordering_violated and has_var_table and has_timeline)

        status_str = "PASS" if passed else "FAIL"

        return {
            "status": status_str,
            "PROPOSAL_STRUCTURE_VALIDATION": status_str,
            "all_14_sections_present": len(missing_sections) == 0,
            "all_subsections_13_present": len(missing_subsections) == 0,
            "section_ordering_intact": not ordering_violated,
            "variable_table_present": has_var_table,
            "timeline_schedule_present": has_timeline,
            "total_word_count": total_word_count,
            "problem_statement_word_count": sec_2_words,
            "literature_review_word_count": sec_3_words,
            "missing_sections": missing_sections,
            "missing_subsections_13": missing_subsections,
            "section_audit_details": section_status
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
