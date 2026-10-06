#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
combination_hypothesis_engine.py - Parallel Combination Hypotheses & Evidence Balancer
Proposal-Nevisi Engine v9.0 (Layer 1: Scientific Accuracy)

Eliminates Positive-Evidence Bias (unilateral synergy assumption) by constructing
parallel hypotheses (Synergism vs Antagonism vs Additive) for drug/biologic combinations.
Partitions empirical evidence, calculates evidence balance scores, and issues publication bias warnings.

100% General-Purpose: Zero hardcoded entity names.
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class CombinationHypothesisAnalysis:
    entity_a: str
    entity_b: str
    target: str
    synergism_hypothesis: str
    antagonism_hypothesis: str
    additive_null_hypothesis: str
    synergism_evidence: List[Dict[str, Any]] = field(default_factory=list)
    antagonism_evidence: List[Dict[str, Any]] = field(default_factory=list)
    neutral_evidence: List[Dict[str, Any]] = field(default_factory=list)
    evidence_balance_score: float = 0.5  # positive / total
    recommended_framing: str = "neutral"  # "synergism" | "antagonism" | "neutral"
    bias_warnings: List[str] = field(default_factory=list)
    framing_narrative_persian: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_a": self.entity_a,
            "entity_b": self.entity_b,
            "target": self.target,
            "synergism_hypothesis": self.synergism_hypothesis,
            "antagonism_hypothesis": self.antagonism_hypothesis,
            "additive_null_hypothesis": self.additive_null_hypothesis,
            "synergism_evidence_count": len(self.synergism_evidence),
            "antagonism_evidence_count": len(self.antagonism_evidence),
            "neutral_evidence_count": len(self.neutral_evidence),
            "synergism_evidence": self.synergism_evidence,
            "antagonism_evidence": self.antagonism_evidence,
            "neutral_evidence": self.neutral_evidence,
            "evidence_balance_score": self.evidence_balance_score,
            "recommended_framing": self.recommended_framing,
            "bias_warnings": self.bias_warnings,
            "framing_narrative_persian": self.framing_narrative_persian
        }

class CombinationHypothesisEngine:
    """Universal engine evaluating dual interaction hypotheses and evidence balance."""

    SYNERGISM_PATTERNS = [
        r'\bsynerg(?:y|istic|ism)\b',
        r'\bcooperat(?:ive|ion)\b',
        r'\bpotentiat(?:e|ion)\b',
        r'\bsensitiz(?:e|ation)\b',
        r'\bCI\s*<\s*(?:1|0\.9|0\.8)\b',
        r'\bcombination\s+index\s*<\s*1\b',
        r'\bsupra-?additive\b',
        r'هم‌?افزایی',
        r'سینرژی',
        r'اثر\s+هم‌?افزا',
        r'تقویت\s+کننده'
    ]

    ANTAGONISM_PATTERNS = [
        r'\bantagoni(?:sm|stic)\b',
        r'\bcompetit(?:ive|ion)\b',
        r'\binterfer(?:e|ence)\b',
        r'\bdecreased\s+efficacy\b',
        r'\bCI\s*>\s*(?:1|1\.1|1\.2)\b',
        r'\bcombination\s+index\s*>\s*1\b',
        r'\bsub-?additive\b',
        r'\bprotective\s+antagonism\b',
        r'آنتاگونیسم',
        r'تداخل\s+منفی',
        r'اثر\s+کاهنده',
        r'مهار\s+متقابل'
    ]

    @classmethod
    def analyze(
        cls,
        entity_a: str,
        entity_b: str,
        target: str = "cell_viability",
        retrieved_evidence: Optional[List[Any]] = None
    ) -> CombinationHypothesisAnalysis:
        """
        Builds dual hypotheses and evaluates balance across retrieved evidence records.
        """
        a_str = str(entity_a).strip()
        b_str = str(entity_b).strip()
        tgt_str = str(target).strip()

        # 1. Parallel hypothesis construction
        hyp_synergy = (
            f"مواجهه همزمان با {a_str} و {b_str} واجد اثر هم‌افزایی (Synergism; CI < 1.0) "
            f"بر مهار {tgt_str} بوده و بازده کشندگی سلولی را بیش از حاصل‌جمع اثرات تک‌عاملی افزایش می‌دهد."
        )
        hyp_antagonism = (
            f"مواجهه همزمان با {a_str} و {b_str} ممکن است به دلیل تداخل در مسیرهای سیگنال‌دهی، رقابت بر سر جذب، "
            f"یا اشباع سیستم، واجد اثر آنتاگونیستی (Antagonism; CI > 1.0) یا خنثی بر {tgt_str} باشد."
        )
        hyp_additive = (
            f"مواجهه همزمان صرفاً منطبق بر مدل جمع‌پذیر بیولوژیک (Additive effect; CI ≈ 1.0) است و برهم‌کنش معنی‌داری ایجاد نمی‌کند."
        )

        evidence_list = retrieved_evidence or []
        synergy_ev = []
        antagonism_ev = []
        neutral_ev = []

        # 2. Partition evidence
        for item in evidence_list:
            item_dict = item.to_dict() if hasattr(item, "to_dict") else (item if isinstance(item, dict) else {"raw": str(item)})
            text_rep = (
                str(item_dict.get("title", "")) + " " +
                str(item_dict.get("abstract", "")) + " " +
                str(item_dict.get("primary_findings", "")) + " " +
                str(item_dict.get("claim_text", ""))
            ).lower()

            is_syn = any(re.search(p, text_rep, re.IGNORECASE) for p in cls.SYNERGISM_PATTERNS)
            is_ant = any(re.search(p, text_rep, re.IGNORECASE) for p in cls.ANTAGONISM_PATTERNS)

            if is_syn and not is_ant:
                synergy_ev.append(item_dict)
            elif is_ant and not is_syn:
                antagonism_ev.append(item_dict)
            elif is_syn and is_ant:
                # Discrepant or dose-dependent
                synergy_ev.append(item_dict)
                antagonism_ev.append(item_dict)
            else:
                neutral_ev.append(item_dict)

        total_informative = len(synergy_ev) + len(antagonism_ev)
        warnings = []

        if total_informative == 0:
            balance_score = 0.5
            recommended_framing = "neutral"
            narrative = (
                f"با توجه به فقدان مطالعات تجربی مستقیم پیرامون هم‌افزایی {a_str} و {b_str} در منابع مورد جستجو، "
                f"هر دو فرضیه هم‌افزایی (Synergy) و آنتاگونیسم (Antagonism) به عنوان احتمالات معتبر در نظر گرفته شده "
                f"و فرضیه‌سازی با لحن بی‌طرفانه و مبتنی بر سنجش تجربی CI تدوین می‌گردد."
            )
        else:
            balance_score = round(len(synergy_ev) / total_informative, 3)

            # Check for Positive Evidence Dominance Warning
            if len(synergy_ev) > 0 and len(antagonism_ev) == 0:
                warnings.append(
                    "POSITIVE_EVIDENCE_DOMINANCE_WARNING: کلیه شواهد بازیابی‌شده حاکی از اثرات مثبت هستند. "
                    "احتمال سوگیری انتشار (Publication Bias) بالاست؛ پروتکل مطالعه باید آزمون‌های دقیق تفکیک آنتاگونیسم را شامل شود."
                )

            if balance_score >= 0.70:
                recommended_framing = "synergism"
                narrative = (
                    f"شواهد موجود به نفع فرضیه هم‌افزایی برهم‌کنش (وزن شواهد مثبت: {int(balance_score*100)}٪) هستند؛ "
                    f"با این وجود، احتمال رخداد اثرات آنتاگونیستی در غلظت‌های نامتعادل در طراحی آزمون مد نظر قرار گرفته است."
                )
            elif balance_score <= 0.30:
                recommended_framing = "antagonism"
                narrative = (
                    f"شواهد پژوهشی نشان‌دهنده غلبه پدیده‌های تداخلی یا آنتاگونیستی میان مداخلات هستند؛ "
                    f"لذا طراحی پروتکل باید بر ارزیابی غلظت‌های حداقلی جهت اجتناب از اثرات متضاد متمرکز گردد."
                )
            else:
                recommended_framing = "neutral"
                narrative = (
                    f"شواهد متناقض و برابری از اثرات هم‌افزا و آنتاگونیستی گزارش شده است؛ "
                    f"لذا بررسی بی‌طرفانه دوز-پاسخ و تعیین دقیق ایزوبولوگرام جهت تشخیص پنجره درمانی الزامی است."
                )

        return CombinationHypothesisAnalysis(
            entity_a=a_str,
            entity_b=b_str,
            target=tgt_str,
            synergism_hypothesis=hyp_synergy,
            antagonism_hypothesis=hyp_antagonism,
            additive_null_hypothesis=hyp_additive,
            synergism_evidence=synergy_ev,
            antagonism_evidence=antagonism_ev,
            neutral_evidence=neutral_ev,
            evidence_balance_score=balance_score,
            recommended_framing=recommended_framing,
            bias_warnings=warnings,
            framing_narrative_persian=narrative
        )

combination_hypothesis_engine = CombinationHypothesisEngine
