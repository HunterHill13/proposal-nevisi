#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
persian_medical_typography_linter.py - Persian Medical Typography & Orthography Linter
Proposal-Nevisi Engine v9.0 (Layer 4: Formatting & Typesetting)

Enforces standard academic Persian orthography:
- Zero-Width Non-Joiner (ZWNJ / نیم‌فاصله) for verbal prefixes and noun suffixes
- Persian numeral normalization while protecting DOIs, PMIDs, URLs, citations [1], and math
- First-mention Latin translation insertion for critical medical terminology
- Extensible via typography_rules.yaml

100% General-Purpose: Zero hardcoded project subjects.
"""

import os
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

EN_TO_FA_DIGITS = {
    '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
    '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'
}

def to_persian_digits(num_str: str) -> str:
    """Converts ASCII digits to Persian Unicode digits."""
    return "".join(EN_TO_FA_DIGITS.get(c, c) for c in str(num_str))

@dataclass
class LintResult:
    original_text: str
    formatted_text: str
    transformations_count: int
    rule_applications: List[Dict[str, Any]] = field(default_factory=list)
    is_modified: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "transformations_count": self.transformations_count,
            "is_modified": self.is_modified,
            "rule_applications": self.rule_applications,
            "formatted_text": self.formatted_text
        }

class PersianMedicalTypographyLinter:
    """Lints and standardizes Persian scientific prose with configurable orthography rules."""

    DEFAULT_RULES = {
        "zwnj_rules": [
            {"pattern": r'\bمی\s+([آ-ی])', "replacement": r'می‌\1', "description": "نیم‌فاصله بعد از پیشوند می"},
            {"pattern": r'\bنمی\s+([آ-ی])', "replacement": r'نمی‌\1', "description": "نیم‌فاصله بعد از پیشوند نمی"},
            {"pattern": r'([آ-ی])\s+های\b', "replacement": r'\1‌های', "description": "نیم‌فاصله قبل از پسوند های"},
            {"pattern": r'([آ-ی])\s+ها\b', "replacement": r'\1‌ها', "description": "نیم‌فاصله قبل از پسوند ها"},
            {"pattern": r'([آ-ی])\s+تر\b', "replacement": r'\1‌تر', "description": "نیم‌فاصله قبل از پسوند تر"},
            {"pattern": r'([آ-ی])\s+ترین\b', "replacement": r'\1‌ترین', "description": "نیم‌فاصله قبل از پسوند ترین"},
            {"pattern": r'([آ-ی])\s+ای\b', "replacement": r'\1‌ای', "description": "نیم‌فاصله قبل از پسوند ای"}
        ],
        "digit_rules": {"enabled": True},
        "medical_terms": [
            {"pattern": r'\bآپوپتوز\b', "replacement": "آپوپتوز (Apoptosis)", "apply_once": True, "description": "درج معادل لاتین آپوپتوز در اولین ذکر"},
            {"pattern": r'\bانکولیتیک\b', "replacement": "انکولیتیک (Oncolytic)", "apply_once": True, "description": "درج معادل لاتین انکولیتیک در اولین ذکر"},
            {"pattern": r'\bسیتوتوکسیسیته\b', "replacement": "سیتوتوکسیسیته (Cytotoxicity)", "apply_once": True, "description": "درج معادل لاتین سیتوتوکسیسیته در اولین ذکر"},
            {"pattern": r'\bهم‌افزایی\b', "replacement": "هم‌افزایی (Synergism)", "apply_once": True, "description": "درج معادل لاتین هم‌افزایی در اولین ذکر"},
            {"pattern": r'\bآنتاگونیسم\b', "replacement": "آنتاگونیسم (Antagonism)", "apply_once": True, "description": "درج معادل لاتین آنتاگونیسم در اولین ذکر"}
        ]
    }

    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.seen_medical_terms = set()

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        target_path = config_path
        if not target_path:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            cand_path = os.path.join(script_dir, "typography_rules.yaml")
            if os.path.exists(cand_path):
                target_path = cand_path

        if target_path and os.path.exists(target_path) and HAS_YAML:
            try:
                with open(target_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, dict):
                        return data
            except Exception:
                pass
        return self.DEFAULT_RULES

    def reset_first_mention_tracker(self):
        """Resets the state of seen terms across new documents."""
        self.seen_medical_terms.clear()

    def format_text(self, text: str) -> str:
        """Shortcut applying all typography and formatting rules."""
        return self.lint(text).formatted_text

    def lint(self, text: str) -> LintResult:
        """
        Lints text and applies ZWNJ, numeral conversion, and first-mention medical expansions.
        Protects math expressions, DOIs, URLs, and citation brackets from unwanted modification.
        """
        if not text:
            return LintResult(original_text="", formatted_text="", transformations_count=0)

        current_text = str(text)
        transform_count = 0
        rule_logs = []

        # 1. Protect tokens that should never be converted (Math, DOIs, URLs, Citations)
        protected_tokens: List[str] = []
        def _protect(match):
            idx = len(protected_tokens)
            protected_tokens.append(match.group(0))
            return f"__TYPO_PROT_{idx}__"

        # Protect Display & Inline Math ($$...$$, $...$, \[...\], \(...\))
        current_text = re.sub(r'\$\$[^$]+\$\$|\$[^$\n]+\$', _protect, current_text)
        current_text = re.sub(r'\\\[[\s\S]+?\\\]|\\\([\s\S]+?\\\)', _protect, current_text)
        # Protect URLs & DOIs
        current_text = re.sub(r'https?://[^\s]+|10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', _protect, current_text)
        # Protect Citation brackets e.g. [1], [2, 3], [1-4]
        current_text = re.sub(r'\[\d+(?:[\s,\-–]+\d+)*\]', _protect, current_text)
        # Protect PMIDs
        current_text = re.sub(r'PMID:\s*\d+', _protect, current_text)
        # Protect English text and mathematical notation inside parentheses e.g. (Apoptosis), (p < 0.05), (CI = 0.45)
        current_text = re.sub(r'\([A-Za-z0-9_\-\s,\./%α-ωΑ-Ω→⇌⇄<>=\+\^±]+\)', _protect, current_text)

        # 2. Apply ZWNJ Rules
        zwnj_rules = self.config.get("zwnj_rules", self.DEFAULT_RULES["zwnj_rules"])
        for r in zwnj_rules:
            pat = r.get("pattern", "")
            repl = r.get("replacement", "")
            desc = r.get("description", "")
            if pat:
                new_text, n_subs = re.subn(pat, repl, current_text)
                if n_subs > 0:
                    transform_count += n_subs
                    rule_logs.append({"rule": desc, "count": n_subs})
                    current_text = new_text

        # 3. Apply Medical Terminology Rules (First Mention Only)
        medical_rules = self.config.get("medical_terms", self.DEFAULT_RULES["medical_terms"])
        for r in medical_rules:
            pat = r.get("pattern", "")
            repl = r.get("replacement", "")
            desc = r.get("description", "")
            apply_once = r.get("apply_once", True)

            if pat:
                # Check if already has parentheses e.g. "آپوپتوز (Apoptosis)"
                if pat in self.seen_medical_terms and apply_once:
                    continue

                # Search and replace only the first occurrence if apply_once
                def _term_sub(m):
                    term_matched = m.group(0)
                    if apply_once:
                        if pat in self.seen_medical_terms:
                            return term_matched
                        self.seen_medical_terms.add(pat)
                    return repl

                new_text, n_subs = re.subn(pat, _term_sub, current_text, count=1 if apply_once else 0)
                if n_subs > 0:
                    transform_count += n_subs
                    rule_logs.append({"rule": desc, "count": n_subs})
                    current_text = new_text

        # 4. Apply Digit Conversion to Persian Numerals in Persian prose
        if self.config.get("digit_rules", {}).get("enabled", True):
            # Only match standalone numbers or numbers surrounded by Persian letters/spaces
            # Avoid replacing inside formulas with operators =, <, >, ±, etc.
            digit_pattern = re.compile(r'(?<![=<>±×÷/a-zA-Z_])\b([0-9]+)\b(?![=<>±×÷/a-zA-Z_])')
            def _digit_sub(m):
                return to_persian_digits(m.group(1))

            new_text, n_subs = digit_pattern.subn(_digit_sub, current_text)
            if n_subs > 0:
                transform_count += n_subs
                rule_logs.append({"rule": "تبدیل اعداد انگلیسی به فارسی در متن", "count": n_subs})
                current_text = new_text

        # 5. Restore Protected Tokens
        for idx, orig in enumerate(protected_tokens):
            current_text = current_text.replace(f"__TYPO_PROT_{idx}__", orig)

        return LintResult(
            original_text=text,
            formatted_text=current_text,
            transformations_count=transform_count,
            rule_applications=rule_logs,
            is_modified=(transform_count > 0)
        )

persian_medical_typography_linter = PersianMedicalTypographyLinter()
