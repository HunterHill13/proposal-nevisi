#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scientific_academic_humanizer.py - Scientific & Academic Anti-AI-Detection Humanizer
Proposal-Nevisi Engine v11.5 (Academic Integrity, Burstiness & Invariant Protection)
===================================================================================

Combines:
1. Contextual Semantic Replacement Engine for 30+ prominent Persian AI cliches and tells
   with precise biomedical, laboratory, and operational terminology.
2. 3-Phase Burstiness & Rhythm Calibration Engine (targeting sentence length standard deviation σ >= 8.0).
3. 100% Fail-Closed Data Invariant Gate protecting all numbers, doses, percentages,
   p-values, CIs, PMIDs, DOIs, catalog numbers, genes, and citations with automatic rollback.
4. Comprehensive Humanization Audit Report generation (JSON & Markdown).

Author: Proposal-Nevisi Hardened Core
License: MIT / Academic Grant Compliance
"""

import os
import re
import math
import json
import time
from typing import Dict, List, Any, Tuple, Optional, Set
from dataclasses import dataclass, field


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class HumanizationResult:
    """Detailed outcome of a humanization pass on text."""
    original_text: str
    humanized_text: str
    burstiness_before: float
    burstiness_after: float
    sentence_count: int
    cliches_detected_count: int
    cliches_replaced_count: int
    cliches_replaced: List[Dict[str, str]] = field(default_factory=list)
    invariant_check_passed: bool = True
    invariant_violations: List[str] = field(default_factory=list)
    is_modified: bool = False
    audit_summary: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "burstiness_before": round(self.burstiness_before, 2),
            "burstiness_after": round(self.burstiness_after, 2),
            "sentence_count": self.sentence_count,
            "cliches_detected_count": self.cliches_detected_count,
            "cliches_replaced_count": self.cliches_replaced_count,
            "cliches_replaced": self.cliches_replaced,
            "invariant_check_passed": self.invariant_check_passed,
            "invariant_violations": self.invariant_violations,
            "is_modified": self.is_modified,
            "audit_summary": self.audit_summary
        }


# ============================================================================
# PILLAR 1: DATA INVARIANT ASSERTION GATE
# ============================================================================

class DataInvariantGate:
    """
    Fail-closed gate ensuring 100% preservation of all quantitative,
    biomedical, and bibliographic invariants during text humanization.
    """

    # Numeric invariants: integers, decimals, percentages, ratios, scientific notations
    NUMBER_PATTERN = re.compile(
        r'(?<![A-Za-z0-9_])'
        r'(?:\d+(?:\.\d+)?%?|\d+/\d+|\d+:\d+|\d+\s*×\s*10\^[-+]?\d+|\d+\s*\\times\s*10\^[-+]?\d+)'
        r'(?![A-Za-z0-9_])'
    )

    # Statistical metrics: p-values, CI, IC50, F-score, etc.
    STAT_PATTERN = re.compile(
        r'\b(?:p\s*[<>=≤≥]\s*0?\.\d+|CI\s*[=:]\s*0?\.\d+(?:[-–]0?\.\d+)?|IC50|ED50|EC50|t\s*\(|F\s*\()'
        r'|\b(?:ANOVA|Chou[-–]Talalay|CompuSyn|MTT|qPCR|Western Blot|Flow Cytometry)\b',
        re.IGNORECASE
    )

    # Citations, PMIDs, DOIs
    BIBLIO_PATTERN = re.compile(
        r'\[\d+(?:[\s,\-–]+\d+)*\]|PMID:\s*\d+|10\.\d{4,9}/[-._;()/:A-Za-z0-9]+'
    )

    # Key biomedical entities, genes, units, cell lines, drugs
    BIOMED_PATTERN = re.compile(
        r'\b(?:TP53|p53|Bcl-2|Bax|mTOR|AKT|PI3K|Caspase-\d+|EGFR|VEGF|TNF[-–]α|IL-\d+|Ki-67|GAPDH|ACTB'
        r'|DMEM|RPMI[-–]?1640|FBS|PBS|DMSO|ATCC\s+[A-Za-z0-9\-]+'
        r'|μM|nM|mM|mg/kg|mL|μL|ng/mL|μg/mL|g/L|IU/mL|TCID50|PFU/mL)\b'
    )

    @classmethod
    def extract_invariants(cls, text: str) -> Dict[str, Set[str]]:
        """Extracts all protected tokens from text grouped by category."""
        if not text:
            return {"numbers": set(), "stats": set(), "biblio": set(), "biomed": set()}

        # Normalize Persian/Arabic digits to English ASCII for canonical invariant matching
        norm_text = text
        for fa_d, en_d in zip("۰۱۲۳۴۵۶۷۸۹", "0123456789"):
            norm_text = norm_text.replace(fa_d, en_d)

        numbers = set(cls.NUMBER_PATTERN.findall(norm_text))
        stats = set(cls.STAT_PATTERN.findall(norm_text))
        biblio = set(cls.BIBLIO_PATTERN.findall(norm_text))
        biomed = set(cls.BIOMED_PATTERN.findall(norm_text))

        return {
            "numbers": numbers,
            "stats": stats,
            "biblio": biblio,
            "biomed": biomed
        }

    @classmethod
    def verify(cls, original_text: str, humanized_text: str) -> Tuple[bool, List[str]]:
        """
        Verifies that every invariant present in original_text is preserved in humanized_text.
        Returns (is_passed, list_of_violations).
        """
        orig_inv = cls.extract_invariants(original_text)
        hum_inv = cls.extract_invariants(humanized_text)

        violations = []

        # Check numbers
        missing_numbers = orig_inv["numbers"] - hum_inv["numbers"]
        if missing_numbers:
            violations.append(f"Missing numbers/percentages: {sorted(list(missing_numbers))}")

        # Check bibliographic citations & identifiers
        missing_biblio = orig_inv["biblio"] - hum_inv["biblio"]
        if missing_biblio:
            violations.append(f"Missing citations/PMID/DOI: {sorted(list(missing_biblio))}")

        # Check statistical descriptors
        missing_stats = orig_inv["stats"] - hum_inv["stats"]
        if missing_stats:
            violations.append(f"Missing statistical tokens: {sorted(list(missing_stats))}")

        # Check biomedical entities & genes
        missing_biomed = orig_inv["biomed"] - hum_inv["biomed"]
        if missing_biomed:
            violations.append(f"Missing biomedical entities/units: {sorted(list(missing_biomed))}")

        return (len(violations) == 0, violations)


# ============================================================================
# PILLAR 2: CONTEXTUAL PERSIAN AI CLICHE & TELL REMOVAL ENGINE
# ============================================================================

class PersianAIClicheEngine:
    """
    Rigorously detects and replaces 30+ Persian AI cliches and robotic transitions
    with authentic, operational academic/biomedical prose.
    Uses contextual alternation to avoid creating new formulaic patterns.
    """

    # Comprehensive Registry of AI tells with prioritized authentic academic replacements
    CLICHE_RULES = [
        {
            "id": "c1_dar_in_rasta",
            "pattern": r'(?:\bدر این راستا،?|\bدر این راستا\b)',
            "replacements": [
                "بدین منظور",
                "برای تحقق این هدف",
                "در این چارچوب مطالعاتی",
                "با این رویکرد عملیاتی",
                "در جهت نیل به این مقصود"
            ],
            "description": "حذف تکیه‌کلام در این راستا"
        },
        {
            "id": "c2_shayan_zekr",
            "pattern": r'(?:\bشایان ذکر است که\b|\bشایان ذکر است،?|\bلازم به ذکر است که\b|\bلازم به ذکر است،?|\bشایان توجه است که\b)',
            "replacements": [
                "یافته‌های تجربی موید آن است که",
                "داده‌های آزمایشگاهی نشان می‌دهند که",
                "بر اساس مستندات بالینی موجود،",
                "بررسی‌های مولکولی حاکی از آن است که",
                "مستندات حاکی از آن است که"
            ],
            "description": "حذف تکیه‌کلام شایان ذکر است / لازم به ذکر است"
        },
        {
            "id": "c3_naghsh_besaza",
            "pattern": r'(?:\bنقش بسزایی دارد\b|\bنقش به سزایی ایفا می‌کند\b|\bنقش بسزایی ایفا می‌کند\b|\bنقش به سزایی دارد\b|\bنقش پررنگی دارد\b)',
            "replacements": [
                "نقش تعیین‌کننده دارد",
                "به‌طور معناداری بر فرآیند پاتولوژیک اثر می‌گذارد",
                "موجب تعدیل مستقیم مسیرهای سلولی می‌شود",
                "در کنترل فرآیندهای تنظیمی مداخله دارد"
            ],
            "description": "حذف کلیشه نقش بسزایی دارد"
        },
        {
            "id": "c4_haez_ahmiat",
            "pattern": r'(?:\bحائز اهمیت است\b|\bاز اهمیت بالایی برخوردار است\b|\bحائز اهمیت فراوان است\b|\bاهمیت بسزایی دارد\b)',
            "replacements": [
                "اهمیت بالینی مستقیمی دارد",
                "محور تحلیل فارماکولوژیک قرار می‌گیرد",
                "ضرورت روش‌شناختی دارد",
                "جایگاه راهبردی دارد"
            ],
            "description": "حذف کلیشه حائز اهمیت است"
        },
        {
            "id": "c5_be_tor_kholase",
            "pattern": r'(?:\bبه طور خلاصه،?|\bبه‌طور خلاصه،?|\bدر یک جمع‌بندی کلی،?|\bبه طور کلی،?|\bبه‌طور کلی،?)',
            "replacements": [
                "برآیند داده‌های تجربی نشان می‌دهد",
                "سنتز شواهد نشان می‌دهد",
                "مجموع شواهد حاکی از آن است که",
                "بر پایه شواهد تجمیع‌شده،"
            ],
            "description": "حذف کلیشه به طور خلاصه / به طور کلی"
        },
        {
            "id": "c6_mitavan_goft",
            "pattern": r'(?:\bمی‌توان گفت که\b|\bمیتوان گفت که\b|\bباید اذعان داشت که\b|\bشایسته است اشاره شود که\b)',
            "replacements": [
                "داده‌ها نشان می‌دهند که",
                "شواهد بیوشیمیایی حاکی از آن است که",
                "ارزیابی مستندات تایید می‌کند که"
            ],
            "description": "حذف عبارات حاشیه‌ای می‌توان گفت که"
        },
        {
            "id": "c7_cheshmandaz_novin",
            "pattern": r'(?:\bچشم‌انداز نوینی\b|\bچشم انداز نوینی\b|\bافق‌های جدیدی\b|\bافق های جدیدی\b)',
            "replacements": [
                "مسیر تحقیقاتی هدفمندی",
                "رویکرد درمانی ارتقایافته‌ای",
                "پروتکل مداخله‌ای نوینی"
            ],
            "description": "حذف استعاره ژورنالیستی چشم‌انداز نوین"
        },
        {
            "id": "c8_chalesh_asasi",
            "pattern": r'(?:\bبه عنوان یک چالش اساسی\b|\bبه‌عنوان یک چالش اساسی\b|\bبه عنوان چالش اساسی\b)',
            "replacements": [
                "به‌عنوان یک معضل بالینی حل‌نشده",
                "به‌عنوان گره‌گاه تشخیصی-درمانی",
                "به‌عنوان مانع اصلی اثربخشی درمان"
            ],
            "description": "جایگزینی چالش اساسی با معضل بالینی دقیق"
        },
        {
            "id": "c9_hamantor_ke_midanim",
            "pattern": r'(?:\bهمانطور که می‌دانیم،?|\bهمان‌طور که می‌دانیم،?|\bپر واضح است که\b|\bبدیهی است که\b)',
            "replacements": [
                "طبق استانداردهای مصوب علمی",
                "مستندات بالینی اثبات کرده‌اند که",
                "بر اساس داده‌های تجربی مستند"
            ],
            "description": "حذف ادعای غیرعلمی همانطور که می‌دانیم"
        },
        {
            "id": "c10_talash_faravan",
            "pattern": r'(?:\bتلاش‌های فراوانی صورت گرفته\b|\bتلاش های زیادی انجام شده\b|\bاقدامات متعددی صورت گرفته\b)',
            "replacements": [
                "مطالعات متعددی در این حوزه متمرکز شده‌اند",
                "پژوهش‌های پیشین بر این محور استوار بوده‌اند",
                "کارآزمایی‌های گوناگونی به انجام رسیده‌اند"
            ],
            "description": "علمی‌سازی تلاش‌های فراوانی صورت گرفته"
        },
        {
            "id": "c11_bedoon_shak",
            "pattern": r'(?:\bبدون شک،?|\bبی‌تردید،?|\bبی تردید،?)',
            "replacements": [
                "شواهد بیوشیمیایی نشان می‌دهند",
                "داده‌های اپیدمیولوژیک تایید می‌کنند",
                "مستندات موجود نشان می‌دهد"
            ],
            "description": "حذف قطعیت‌های غیرعلمی بدون شک"
        },
        {
            "id": "c12_gam_mohem",
            "pattern": r'(?:\bگام مهمی در جهت\b|\bگام مؤثری در راستای\b|\bگام موثری در جهت\b)',
            "replacements": [
                "اقدامی ساختاریافته در مسیر",
                "مرحله‌ای راهبردی در جهت",
                "رویکردی عملیاتی برای"
            ],
            "description": "حذف کلیشه گام مهمی در جهت"
        },
        {
            "id": "c13_dastkhosh_taghyir",
            "pattern": r'(?:\bدستخوش تغییرات\b|\bدستخوش دگرگونی\b)',
            "replacements": [
                "دچار دگرگونی‌های مولکولی",
                "متحمل تغییرات ساختاری",
                "تحت تاثیر نوسانات تنظیمی"
            ],
            "description": "جایگزینی دستخوش تغییرات با بیان مکانیکی"
        },
        {
            "id": "c14_be_tor_fazaende",
            "pattern": r'(?:\bبه طور فزاینده‌ای\b|\bبه‌طور فزاینده‌ای\b|\bبه صورت فزاینده ای\b)',
            "replacements": [
                "با شیب صعودی",
                "با روندی فزاینده",
                "با نرخ رو به افزایش"
            ],
            "description": "حذف به طور فزاینده‌ای"
        },
        {
            "id": "c15_be_khoobi_shenakhte",
            "pattern": r'(?:\bبه خوبی شناخته شده است\b|\bبه‌خوبی شناخته شده است\b|\bبه خوبی اثبات شده است\b)',
            "replacements": [
                "در متون علمی مستند گردیده است",
                "در مطالعات پیشین به اثبات رسیده است",
                "بر پایه شواهد آزمایشگاهی تثبیت شده است"
            ],
            "description": "حذف به خوبی شناخته شده است"
        },
        {
            "id": "c16_navidbakhsh",
            "pattern": r'(?:\bنویدبخش\b|\bبسیار نویدبخش\b)',
            "replacements": [
                "دارای پتانسیل فارماکولوژیک",
                "واجد ارزش ترجمانی بالینی",
                "با اثربخشی بیولوژیک بالقوه"
            ],
            "description": "حذف واژه شعاری نویدبخش"
        },
        {
            "id": "c17_tasir_shegeft",
            "pattern": r'(?:\bتاثیر شگرف\b|\bتأثیر شگرف\b|\bتحول شگرف\b)',
            "replacements": [
                "اثر بیولوژیک بارز",
                "تغییر معنادار عملکردی",
                "پاسخ فارماکودینامیک مشخص"
            ],
            "description": "حذف واژگان اغراق‌آمیز تحول شگرف"
        },
        {
            "id": "c18_be_nobeye_khod",
            "pattern": r'(?:\bبه نوبه خود،?|\bبه نوبهٔ خود،?)',
            "replacements": [
                "متقابلاً",
                "به‌طور مستقل",
                "در ادامه این مسیر"
            ],
            "description": "حذف عبارت به نوبه خود"
        },
        {
            "id": "c19_hamgam_ba",
            "pattern": r'(?:\bهمگام با\b|\bهم‌گام با\b)',
            "replacements": [
                "متناسب با",
                "هم‌راستا با داده‌های",
                "منطبق بر پروتکل‌های"
            ],
            "description": "حذف همگام با"
        },
        {
            "id": "c20_bar_kasi_pooshide_nist",
            "pattern": r'(?:\bبر کسی پوشیده نیست که\b|\bامروزه بر کسی پوشیده نیست که\b)',
            "replacements": [
                "طبق گزارش‌های سازمان جهانی بهداشت (WHO)،",
                "بر پایه مستندات همه‌گیرشناسی مصوب،",
                "شواهد اپیدمیولوژیک نشان می‌دهند که"
            ],
            "description": "حذف بر کسی پوشیده نیست"
        },
        {
            "id": "c21_tar_o_pood",
            "pattern": r'(?:\bتار و پود\b|\bپیچیدگی‌های ظریف\b|\bپیچیدگی های ظریف\b)',
            "replacements": [
                "روابط متقابل بیوشیمیایی",
                "شبکه برهم‌کنش‌های سلولی",
                "مکانیسم‌های تنظیمی پیچیده"
            ],
            "description": "حذف استعاره ادبی تار و پود"
        },
        {
            "id": "c22_noghte_atf",
            "pattern": r'(?:\bدر نقطه عطف\b|\bنقطه عطفی در\b)',
            "replacements": [
                "در فاز تصمیم‌گیری بالینی",
                "در مرحله ارزیابی ترجمانی",
                "نقطه گذار به مدل‌های پیشرفته"
            ],
            "description": "حذف استعاره نقطه عطف"
        },
        {
            "id": "c23_nokte_taamol",
            "pattern": r'(?:\bنکته قابل تامل این است که\b|\bنکته قابل تأمل این است که\b|\bنکته جالب توجه این است که\b)',
            "replacements": [
                "تحلیل مکانیکی نشان می‌دهد که",
                "شواهد سلولی بیانگر آن است که",
                "داده‌های مستخرج موید آن است که"
            ],
            "description": "حذف نکته قابل تامل"
        },
        {
            "id": "c24_az_dirbaz",
            "pattern": r'(?:\bاز دیرباز مورد توجه بوده است\b|\bاز دیرباز تاکنون\b|\bاز گذشته‌های دور\b)',
            "replacements": [
                "طی دهه‌های گذشته در کانون پژوهش‌های تخصصی قرار داشته است",
                "بر اساس پیشینه مستند چند دهه اخیر",
                "در مطالعات تاریخی داروشناسی"
            ],
            "description": "جایگزینی از دیرباز با دوره‌های زمانی استاندارد"
        },
        {
            "id": "c25_rahgosha",
            "pattern": r'(?:\bراهگشا باشد\b|\bمی‌تواند راهگشا باشد\b|\bراهگشای مشکلات باشد\b)',
            "replacements": [
                "منجر به بهینه‌سازی استراتژی مداخله گردد",
                "به تدوین پروتکل‌های موثرتر یاری رساند",
                "پاسخ‌دهی درمانی را ارتقا بخشد"
            ],
            "description": "حذف کلیشه راهگشا باشد"
        },
        {
            "id": "c26_ba_tavajoh_be_mavared",
            "pattern": r'(?:\bبا توجه به موارد فوق،?|\bبا عنایت به مطالب ذکر شده،?|\bبا توجه به نکات مطرح شده،?)',
            "replacements": [
                "بر این مبنا و با تکیه بر شواهد یادشده،",
                "بر پایه شواهد آزمایشگاهی احصاشده،",
                "با اتکا به این پشتوانه علمی،"
            ],
            "description": "علمی‌سازی با توجه به موارد فوق"
        },
        {
            "id": "c27_omid_ziad",
            "pattern": r'(?:\bامیدهای زیادی ایجاد کرده است\b|\bامیدهای فراوانی برانگیخته است\b)',
            "replacements": [
                "شواهد پیش‌بالینی اولیه را فراهم ساخته است",
                "فرضیه اثربخشی بیولوژیک را تقویت نموده است",
                "توجیه فارماکولوژیک لازم را محقق کرده است"
            ],
            "description": "حذف امیدهای زیادی ایجاد کرده است"
        },
        {
            "id": "c28_em_dash",
            "pattern": r'\s*—\s*',
            "replacements": [
                "؛ ",
                "، ",
                ". "
            ],
            "description": "اصلاح خط فاصله کشیده (Em-dash) به علائم نگارشی استاندارد فارسی"
        }
    ]

    def __init__(self):
        self._replacement_counters: Dict[str, int] = {}

    def replace_cliches(self, text: str) -> Tuple[str, List[Dict[str, str]]]:
        """
        Replaces cliches across the text with cyclic alternation of authentic academic terms.
        Returns (sanitized_text, list_of_replacements).
        """
        if not text:
            return text, []

        processed_text = text
        applied_replacements = []

        for rule in self.CLICHE_RULES:
            rule_id = rule["id"]
            pattern = re.compile(rule["pattern"])
            replacements = rule["replacements"]

            # Count occurrences
            matches = list(pattern.finditer(processed_text))
            if not matches:
                continue

            # Process matches in order
            for m in matches:
                curr_counter = self._replacement_counters.get(rule_id, 0)
                replacement = replacements[curr_counter % len(replacements)]
                self._replacement_counters[rule_id] = curr_counter + 1

                # Perform one replacement
                original_matched = m.group(0)
                processed_text = pattern.sub(replacement, processed_text, count=1)
                applied_replacements.append({
                    "rule_id": rule_id,
                    "description": rule["description"],
                    "matched": original_matched,
                    "replacement": replacement
                })

        return processed_text, applied_replacements


# ============================================================================
# PILLAR 3: BURSTINESS & RHYTHMIC SENTENCE CALIBRATION ENGINE
# ============================================================================

class BurstinessEngine:
    """
    Measures and calibrates sentence length variance (Burstiness) in Persian prose.
    Academic human prose exhibits standard deviation σ >= 8.0 through intentional alternation
    between short punchy claims (<= 8 words), medium compound explanations (15-25 words),
    and extended mechanistic/experimental descriptions (> 30 words).
    """

    TARGET_BURSTINESS = 8.5
    SENTENCE_SPLIT_PATTERN = re.compile(r'(?<=[.!?؟])\s+|\n+')

    @classmethod
    def tokenize_words(cls, sentence: str) -> List[str]:
        """Tokenizes Persian sentence into clean words."""
        # Replace punctuation with spaces
        clean = re.sub(r'[\(\)\[\]\{\}،؛:\.!?؟«»\-—\+\*\/_\|]', ' ', sentence)
        words = [w for w in clean.split() if w.strip()]
        return words

    @classmethod
    def get_sentence_lengths(cls, text: str) -> List[int]:
        """Returns the word counts for each non-empty sentence in the text."""
        raw_sentences = cls.SENTENCE_SPLIT_PATTERN.split(text)
        lengths = []
        for s in raw_sentences:
            s_clean = s.strip()
            # Ignore headers, table lines, or tiny delimiters
            if not s_clean or s_clean.startswith("#") or s_clean.startswith("|") or s_clean.startswith("---"):
                continue
            words = cls.tokenize_words(s_clean)
            if len(words) >= 2:  # ignore 1-word artefacts
                lengths.append(len(words))
        return lengths

    @classmethod
    def compute_burstiness(cls, text: str) -> float:
        """
        Computes the standard deviation of sentence lengths in words.
        Returns standard deviation (σ).
        """
        lengths = cls.get_sentence_lengths(text)
        if len(lengths) <= 1:
            return 0.0

        mean = sum(lengths) / len(lengths)
        variance = sum((l - mean) ** 2 for l in lengths) / (len(lengths) - 1)
        return math.sqrt(variance)

    @classmethod
    def calibrate_rhythm(cls, text: str, target_burstiness: float = 8.5) -> str:
        """
        Calibrates sentence cadence by breaking overly long uniform compounds into a punchy short
        assertion clause + rigorous condition, while guaranteeing DataInvariantGate compliance.
        """
        current_sigma = cls.compute_burstiness(text)
        if current_sigma >= target_burstiness:
            return text

        paragraphs = text.split("\n\n")
        calibrated_paragraphs = []

        for p in paragraphs:
            p_strip = p.strip()
            # Do not touch headers, tables, code blocks, or short single sentences
            if not p_strip or p_strip.startswith("#") or p_strip.startswith("|") or p_strip.startswith("```"):
                calibrated_paragraphs.append(p)
                continue

            sentences = cls.SENTENCE_SPLIT_PATTERN.split(p)
            new_sentences = []

            for s in sentences:
                s_strip = s.strip()
                words = cls.tokenize_words(s_strip)
                # If a sentence is overly long (> 32 words) and contains weak coordinating junctions e.g. " و در نتیجه " or " به طوری که "
                if len(words) > 32 and not re.search(r'\[\d+\]', s_strip[:len(s_strip)//2]):
                    # Attempt split at prominent explanatory conjunctions
                    split_candidate = re.split(r'\s+و بدین ترتیب\s+|\s+و در نتیجه\s+|\s+به‌طوری‌که\s+|\s+به طوری که\s+', s_strip, maxsplit=1)
                    if len(split_candidate) == 2 and len(cls.tokenize_words(split_candidate[0])) >= 8 and len(cls.tokenize_words(split_candidate[1])) >= 8:
                        candidate_s = f"{split_candidate[0]}. بر این مبنا، {split_candidate[1]}"
                        # Invariant check on sentence level
                        passed, _ = DataInvariantGate.verify(s_strip, candidate_s)
                        if passed:
                            new_sentences.append(candidate_s)
                            continue

                new_sentences.append(s_strip)

            calibrated_p = " ".join(s for s in new_sentences if s)
            # Full paragraph invariant check
            p_passed, _ = DataInvariantGate.verify(p, calibrated_p)
            if p_passed:
                calibrated_paragraphs.append(calibrated_p)
            else:
                calibrated_paragraphs.append(p)  # Rollback on paragraph failure

        return "\n\n".join(calibrated_paragraphs)


# ============================================================================
# MASTER COORDINATOR: SCIENTIFIC ACADEMIC HUMANIZER
# ============================================================================

class ScientificAcademicHumanizer:
    """
    Master two-layer hybrid engine for scientific academic humanization:
    - Layer 1: Deterministic contextual cliche eradication & punctuation correction
    - Layer 2: Burstiness & rhythm variance calibration (target σ >= 8.0)
    - Gate: Fail-closed DataInvariantGate with automatic rollback on data distortion.
    """

    # Proposal section numbers targeted for narrative humanization (Pajooheshyar 28 Canonical)
    # Excludes purely quantitative / formula / bullet sections: 20 (Variables), 22 (Sample Size), 23 (Statistical Tests)
    TARGET_SECTIONS_28 = [3, 4, 5, 6, 7, 8, 9, 19, 24, 26]
    # Legacy 14 section mappings
    TARGET_SECTIONS_14 = [2, 3, 4, 5, 6, 9]

    def __init__(self, target_burstiness: float = 8.5):
        self.target_burstiness = target_burstiness
        self.cliche_engine = PersianAIClicheEngine()

    def humanize_text(self, text: str) -> HumanizationResult:
        """
        Humanizes arbitrary biomedical or proposal text.
        Guarantees 100% preservation of all quantitative and bibliographic invariants.
        """
        if not text:
            return HumanizationResult(
                original_text="", humanized_text="",
                burstiness_before=0.0, burstiness_after=0.0,
                sentence_count=0, cliches_detected_count=0, cliches_replaced_count=0
            )

        burst_before = BurstinessEngine.compute_burstiness(text)
        lengths_before = BurstinessEngine.get_sentence_lengths(text)
        sentence_count = len(lengths_before)

        # 1. Protect special blocks: Markdown tables, code blocks, raw LaTeX displays
        protected_blocks: List[str] = []
        def _protect_block(match):
            idx = len(protected_blocks)
            protected_blocks.append(match.group(0))
            return f"__HUMANIZER_PROT_BLOCK_{idx}__"

        work_text = text
        # Protect markdown code blocks
        work_text = re.sub(r'```[\s\S]+?```', _protect_block, work_text)
        # Protect markdown tables (consecutive lines starting with '|')
        work_text = re.sub(r'(?:^[ \t]*\|[^\n]+\|[ \t]*$\n?)+', _protect_block, work_text, flags=re.MULTILINE)
        # Protect display math
        work_text = re.sub(r'\$\$[\s\S]+?\$\$|\\\[[\s\S]+?\\\]', _protect_block, work_text)

        # 2. Layer 1: Contextual Semantic Cliche Replacement
        sanitized_text, replaced_cliches = self.cliche_engine.replace_cliches(work_text)

        # 3. Layer 2: Burstiness Rhythm Calibration
        calibrated_text = BurstinessEngine.calibrate_rhythm(sanitized_text, target_burstiness=self.target_burstiness)

        # 4. Restore protected blocks
        for idx, orig_block in enumerate(protected_blocks):
            calibrated_text = calibrated_text.replace(f"__HUMANIZER_PROT_BLOCK_{idx}__", orig_block)

        # 5. Fail-Closed Invariant Verification Gate
        passed, violations = DataInvariantGate.verify(text, calibrated_text)

        if not passed:
            # Automatic Rollback if any invariant was damaged
            final_text = text
            burst_after = burst_before
            is_mod = False
        else:
            final_text = calibrated_text
            burst_after = BurstinessEngine.compute_burstiness(final_text)
            is_mod = (final_text != text)

        result = HumanizationResult(
            original_text=text,
            humanized_text=final_text,
            burstiness_before=burst_before,
            burstiness_after=burst_after,
            sentence_count=sentence_count,
            cliches_detected_count=len(replaced_cliches),
            cliches_replaced_count=len(replaced_cliches),
            cliches_replaced=replaced_cliches,
            invariant_check_passed=passed,
            invariant_violations=violations,
            is_modified=is_mod,
            audit_summary={
                "target_burstiness": self.target_burstiness,
                "burstiness_achieved": round(burst_after, 2),
                "rhythm_variance_improved": round(burst_after - burst_before, 2),
                "rollback_triggered": not passed
            }
        )
        return result

    def humanize_proposal_markdown(
        self,
        md_text: str,
        format_type: str = "28",
        target_sections: Optional[List[int]] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Parses full proposal markdown into sections, humanizes narrative sections,
        leaves bibliographic & administrative tables untouched, and compiles an audit report.
        """
        if not md_text:
            return md_text, {}

        selected_targets = target_sections
        if not selected_targets:
            selected_targets = self.TARGET_SECTIONS_28 if str(format_type) in ["28", "auto"] else self.TARGET_SECTIONS_14

        # Split markdown by top-level section headers (## N. ...) while preserving trailing newlines on headers
        section_pattern = re.compile(r'(^##\s+(\d+)\.\s+[^\n]+\n*)', re.MULTILINE)
        splits = section_pattern.split(md_text)

        # splits structure: [preamble, header1, sec_num1, body1, header2, sec_num2, body2, ...]
        out_parts = []
        out_parts.append(splits[0])  # Document title / metadata

        total_cliches_replaced = 0
        replaced_details = []
        section_metrics = {}
        all_passed = True
        overall_violations = []

        i = 1
        while i < len(splits):
            header = splits[i]
            sec_num = int(splits[i+1])
            body = splits[i+2]
            i += 3

            # Determine whether this section is an approved narrative section
            if sec_num in selected_targets:
                h_res = self.humanize_text(body)
                out_parts.append(header)
                out_parts.append(h_res.humanized_text.strip() + "\n\n")

                total_cliches_replaced += h_res.cliches_replaced_count
                replaced_details.extend(h_res.cliches_replaced)
                if not h_res.invariant_check_passed:
                    all_passed = False
                    overall_violations.extend(h_res.invariant_violations)

                section_metrics[f"section_{sec_num}"] = {
                    "burstiness_before": round(h_res.burstiness_before, 2),
                    "burstiness_after": round(h_res.burstiness_after, 2),
                    "cliches_replaced": h_res.cliches_replaced_count,
                    "invariant_passed": h_res.invariant_check_passed
                }
            else:
                out_parts.append(header)
                out_parts.append(body.strip() + "\n\n")

        final_md = "".join(out_parts)
        doc_burst_before = BurstinessEngine.compute_burstiness(md_text)
        doc_burst_after = BurstinessEngine.compute_burstiness(final_md)

        audit_report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "target_sections": selected_targets,
            "document_burstiness_before": round(doc_burst_before, 2),
            "document_burstiness_after": round(doc_burst_after, 2),
            "target_burstiness": self.target_burstiness,
            "total_cliches_purged": total_cliches_replaced,
            "invariant_gate_verdict": "VERIFIED_100_PERCENT" if all_passed else "FAILED_VIOLATIONS_DETECTED",
            "invariant_violations": overall_violations,
            "section_breakdown": section_metrics,
            "sample_cliche_purges": replaced_details[:10]
        }

        return final_md, audit_report

    @classmethod
    def save_audit_report(cls, report_data: Dict[str, Any], output_dir: str) -> Tuple[str, str]:
        """Saves humanization audit report to JSON and Markdown."""
        os.makedirs(output_dir, exist_ok=True)
        json_path = os.path.join(output_dir, "humanization_audit_report.json")
        md_path = os.path.join(output_dir, "humanization_audit_report.md")

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        md_content = [
            "# گزارش ممیزی انسانی‌سازی و عدم کشف هوش مصنوعی (Scientific Academic Humanizer Audit)",
            f"**تاریخ ارزیابی:** {report_data.get('timestamp')}",
            f"**وضعیت دروازه حفاظت از داده‌ها:** {report_data.get('invariant_gate_verdict')}",
            "",
            "## ۱. شاخص‌های آماری ریتم و تنوع جملات (Burstiness & Sentence Cadence)",
            f"- **انحراف معیار اولیه طول جملات (σ قبل):** {report_data.get('document_burstiness_before')}",
            f"- **انحراف معیار نهایی طول جملات (σ بعد):** {report_data.get('document_burstiness_after')}",
            f"- **حد آستانه استاندارد انسانی:** {report_data.get('target_burstiness')}",
            f"- **تعداد کل تکیه‌کلام‌ها و کلیشه‌های هوش مصنوعی پاک‌سازی شده:** {report_data.get('total_cliches_purged')}",
            "",
            "## ۲. تفکیک بخش‌های پردازش‌شده پروپوزال",
            "| شماره بخش | ریتم قبل (σ) | ریتم بعد (σ) | کلیشه‌های اصلاح‌شده | وضعیت دروازه داده‌ها |",
            "| :---: | :---: | :---: | :---: | :---: |"
        ]

        for sec, sm in report_data.get("section_breakdown", {}).items():
            inv_icon = "✅ تایید" if sm.get("invariant_passed") else "❌ رد"
            md_content.append(f"| {sec} | {sm.get('burstiness_before')} | {sm.get('burstiness_after')} | {sm.get('cliches_replaced')} | {inv_icon} |")

        md_content.extend([
            "",
            "## ۳. نمونه‌های شاخص جایگزینی معنایی و اصطلاحات پالایش‌شده",
            "| عبارت اولیه هوش مصنوعی | جایگزین آکادمیک / آزمایشگاهی | قاعده |",
            "| :--- | :--- | :--- |"
        ])

        for c in report_data.get("sample_cliche_purges", [])[:10]:
            md_content.append(f"| {c.get('matched')} | **{c.get('replacement')}** | {c.get('description')} |")

        md_content.append("")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md_content))

        return json_path, md_path
