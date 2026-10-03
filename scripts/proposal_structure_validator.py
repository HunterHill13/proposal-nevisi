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
from typing import Dict, List, Any, Tuple

MANDATORY_14_SECTIONS = [
    (1, "موضوع", [r"موضوع", r"عنوان"]),
    (2, "بیان مسئله", [r"بیان\s*مس[ئأه]له"]),
    (3, "مرور بر منابع", [r"مرور\s*بر\s*منابع", r"پیشینه\s*پژوهش"]),
    (4, "اهمیت و ضرورت تحقیق", [r"اهمیت\s*و\s*ضرورت"]),
    (5, "تعریف واژه‌ها", [r"تعریف\s*واژه"]),
    (6, "اهداف جزیی", [r"اهداف\s*جز[ئیی]"]),
    (7, "اهداف کلی", [r"هدف\s*کلی", r"اهداف\s*کلی"]),
    (8, "اهداف کاربردی", [r"اهداف\s*کاربردی"]),
    (9, "فرضیات و سوالات", [r"فرضی[اه]ت\s*و\s*س[وؤ]الات", r"فرضیه‌ها\s*و\s*پرسش‌ها"]),
    (10, "دستاوردها", [r"دستاوردها"]),
    (11, "جدول متغیرها", [r"جدول\s*متغیرها", r"متغیرها"]),
    (12, "جدول زمان‌بندی و مراحل اجرا", [r"جدول\s*زمان[\s\-]*بندی", r"مراحل\s*اجرا"]),
    (13, "روش اجرا", [r"روش\s*اجرا", r"متدولوژی"]),
    (14, "منابع مورد استفاده", [r"منابع\s*(?:مورد\s*استفاده)?", r"فهرست\s*منابع"])
]

MANDATORY_SUBSECTIONS_13 = [
    ("13-1", "نوع مطالعه", [r"نوع\s*مطالعه"]),
    ("13-2", "جامعه مورد مطالعه", [r"جامعه\s*مورد\s*مطالعه"]),
    ("13-3", "محل انجام مطالعه", [r"محل\s*انجام"]),
    ("13-4", "معیارهای ورود به مطالعه", [r"معیارهای\s*ورود"]),
    ("13-5", "معیارهای خروج از مطالعه", [r"معیارهای\s*خروج"]),
    ("13-6", "ابزارهای گردآوری اطلاعات", [r"ابزارهای\s*گردآوری"]),
    ("13-7", "تعیین اعتبار ابزار گردآوری", [r"اعتبار\s*ابزار", r"روایی"]),
    ("13-8", "تعیین پایایی / ابزار گردآوری", [r"پایایی", r"تعیین\s*ابزار"]),
    ("13-9", "حجم نمونه و روش محاسبه آن", [r"حجم\s*نمونه"]),
    ("13-10", "روش تجزیه و تحلیل داده", [r"تجزیه\s*و\s*تحلیل\s*داده", r"تحلیل\s*آماری"]),
    ("13-11", "ملاحظات اخلاقی در صورت نیاز", [r"ملاحظات\s*اخلاقی"]),
    ("13-12", "نکات امنیتی و حفاظت زیستی", [r"حفاظت\s*(?:زیستی|پروژه)", r"نکات\s*امنیتی"]),
    ("13-13", "مشکلات و محدودیت‌ها", [r"مشکلات\s*و\s*محدودیت"]),
    ("13-14", "شیوه اجرایی و مراحل طرح", [r"شیوه\s*اجرایی", r"مراحل\s*طرح"])
]

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

        passed = (len(missing_sections) == 0 and len(missing_subsections) == 0 and not ordering_violated and has_var_table and has_timeline)

        status_str = "PASS" if passed else "FAIL"

        return {
            "PROPOSAL_STRUCTURE_VALIDATION": status_str,
            "all_14_sections_present": len(missing_sections) == 0,
            "all_subsections_13_present": len(missing_subsections) == 0,
            "section_ordering_intact": not ordering_violated,
            "variable_table_present": has_var_table,
            "timeline_schedule_present": has_timeline,
            "missing_sections": missing_sections,
            "missing_subsections_13": missing_subsections,
            "section_audit_details": section_status
        }

if __name__ == "__main__":
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
    ### 13-7. تعیین اعتبار ابزار گردآوری
    ### 13-8. تعیین ابزار گردآوری
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
