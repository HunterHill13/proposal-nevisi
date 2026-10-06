#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
combination_hypothesis_engine.py - Context-Aware Parallel Combination Hypotheses & Evidence Balancer
Proposal-Nevisi Engine v9.1 (Layer 1: Scientific Accuracy)

Eliminates superficial keyword-counting bias by evaluating evidence directness:
- Disentangles direct combination evidence from monotherapies and indirect background.
- Categorizes evidence across 6 rigorous tiers:
  * DIRECT_COMBINATION_EVIDENCE
  * DIRECT_SINGLE_AGENT_EVIDENCE
  * CLOSE_ANALOG
  * MECHANISTIC_SUPPORT
  * METHODOLOGICAL_SUPPORT
  * INDIRECT_BACKGROUND
- Emits explicit 'NO_DIRECT_COMBINATION_EVIDENCE' when co-treatment has not been directly studied.
- Weights evidence by directness and quality rather than raw volume of irrelevant papers.
- Enforces parallel hypotheses ($H_1$: Synergy vs $H_2$: Antagonism/Additivity) with publication bias warnings.

100% General-Purpose: Zero hardcoded entity names.
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class ClassifiedEvidenceRecord:
    title: str
    tier: str  # DIRECT_COMBINATION_EVIDENCE, DIRECT_SINGLE_AGENT_EVIDENCE, CLOSE_ANALOG, MECHANISTIC_SUPPORT, METHODOLOGICAL_SUPPORT, INDIRECT_BACKGROUND
    interaction_polarity: str  # SYNERGY, ANTAGONISM, ADDITIVE, NEUTRAL, NOT_APPLICABLE
    weight: float
    directness_notes: str
    source_id: Optional[str] = None

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
    evidence_balance_score: float = 0.5  # weighted positive / total weighted informative
    recommended_framing: str = "neutral"  # "synergism" | "antagonism" | "neutral"
    has_direct_combination_evidence: bool = False
    direct_combination_evidence_count: int = 0
    evidence_tiers_breakdown: Dict[str, int] = field(default_factory=dict)
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
            "has_direct_combination_evidence": self.has_direct_combination_evidence,
            "direct_combination_evidence_count": self.direct_combination_evidence_count,
            "evidence_tiers_breakdown": self.evidence_tiers_breakdown,
            "synergism_evidence": self.synergism_evidence,
            "antagonism_evidence": self.antagonism_evidence,
            "neutral_evidence": self.neutral_evidence,
            "evidence_balance_score": self.evidence_balance_score,
            "recommended_framing": self.recommended_framing,
            "bias_warnings": self.bias_warnings,
            "framing_narrative_persian": self.framing_narrative_persian
        }


class CombinationHypothesisEngine:
    """Universal engine evaluating dual interaction hypotheses and evidence directness."""

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

    TIER_WEIGHTS = {
        "DIRECT_COMBINATION_EVIDENCE": 1.0,
        "CLOSE_ANALOG": 0.40,
        "DIRECT_SINGLE_AGENT_EVIDENCE": 0.20,
        "MECHANISTIC_SUPPORT": 0.20,
        "METHODOLOGICAL_SUPPORT": 0.05,
        "INDIRECT_BACKGROUND": 0.0
    }

    @classmethod
    def analyze(
        cls,
        entity_a: str,
        entity_b: str,
        target: str = "cell_viability",
        retrieved_evidence: Optional[List[Any]] = None,
        model_or_cell_line: Optional[str] = None
    ) -> CombinationHypothesisAnalysis:
        """
        Builds dual hypotheses and evaluates context-aware evidence directness.
        """
        a_str = str(entity_a).strip()
        b_str = str(entity_b).strip()
        tgt_str = str(target).strip()
        model_str = str(model_or_cell_line).strip() if model_or_cell_line else ""

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

        tiers_counts = {
            "DIRECT_COMBINATION_EVIDENCE": 0,
            "DIRECT_SINGLE_AGENT_EVIDENCE": 0,
            "CLOSE_ANALOG": 0,
            "MECHANISTIC_SUPPORT": 0,
            "METHODOLOGICAL_SUPPORT": 0,
            "INDIRECT_BACKGROUND": 0
        }

        weighted_pos = 0.0
        weighted_neg = 0.0
        direct_combination_count = 0

        a_lower = a_str.lower()
        b_lower = b_str.lower()
        model_lower = model_str.lower() if model_str else ""

        # 2. Context-aware evidence evaluation
        for item in evidence_list:
            item_dict = item.to_dict() if hasattr(item, "to_dict") else (item if isinstance(item, dict) else {"raw": str(item)})
            text_rep = (
                str(item_dict.get("title", "")) + " " +
                str(item_dict.get("abstract", "")) + " " +
                str(item_dict.get("primary_findings", "")) + " " +
                str(item_dict.get("claim_text", ""))
            ).lower()

            has_a = a_lower in text_rep
            has_b = b_lower in text_rep
            has_model = (model_lower in text_rep) if model_lower else True

            # Determine Tier
            if has_a and has_b and has_model:
                tier = "DIRECT_COMBINATION_EVIDENCE"
                direct_combination_count += 1
            elif has_a and has_b:
                tier = "CLOSE_ANALOG"
            elif has_a or has_b:
                tier = "DIRECT_SINGLE_AGENT_EVIDENCE"
            elif any(w in text_rep for w in ["apoptosis", "caspase", "bcl", "akt", "pathway", "signaling", "momp"]):
                tier = "MECHANISTIC_SUPPORT"
            elif any(w in text_rep for w in ["chou-talalay", "isobologram", "bliss", "loewe", "combination index"]):
                tier = "METHODOLOGICAL_SUPPORT"
            else:
                tier = "INDIRECT_BACKGROUND"

            tiers_counts[tier] = tiers_counts.get(tier, 0) + 1
            weight = cls.TIER_WEIGHTS.get(tier, 0.0)

            # Polarity detection
            is_syn = any(re.search(p, text_rep, re.IGNORECASE) for p in cls.SYNERGISM_PATTERNS)
            is_ant = any(re.search(p, text_rep, re.IGNORECASE) for p in cls.ANTAGONISM_PATTERNS)

            if is_syn and not is_ant:
                synergy_ev.append(item_dict)
                weighted_pos += weight
            elif is_ant and not is_syn:
                antagonism_ev.append(item_dict)
                weighted_neg += weight
            elif is_syn and is_ant:
                synergy_ev.append(item_dict)
                antagonism_ev.append(item_dict)
                weighted_pos += (weight * 0.5)
                weighted_neg += (weight * 0.5)
            else:
                neutral_ev.append(item_dict)

        has_direct_evidence = (direct_combination_count > 0)
        total_weighted = weighted_pos + weighted_neg
        warnings = []

        if not has_direct_evidence:
            warnings.append(
                "NO_DIRECT_COMBINATION_EVIDENCE: هیچ مطالعه تجربی مستقیمی پیرامون ترکیب همزمان این دو مداخله "
                f"({a_str} + {b_str}) در مدل مورد نظر یافت نشد. "
                "شواهد موجود صرفاً غیرمستقیم، تک‌عاملی یا مکانیسمی هستند؛ گزاره هم‌افزایی باید به عنوان فرضیه آزمون‌نشده تدوین گردد."
            )

        if total_weighted <= 0.05:
            # When no informative evidence exists, balance score defaults to 0.5 (neutral)
            balance_score = 0.5
            recommended_framing = "neutral"
            narrative = (
                f"با توجه به فقدان یا ناچیز بودن شواهد پیرامون اثر همزمان {a_str} و {b_str} در منابع مورد جستجو، "
                f"هر دو فرضیه هم‌افزایی (Synergy) و آنتاگونیسم (Antagonism) به عنوان احتمالات علمی هم‌تراز در نظر گرفته شده "
                f"و فرضیه‌سازی با لحن بی‌طرفانه تدوین گردید."
            )
        else:
            balance_score = round(weighted_pos / total_weighted, 3)

            # Check for Positive Evidence Dominance Warning
            if weighted_pos > 0 and weighted_neg == 0:
                warnings.append(
                    "POSITIVE_EVIDENCE_DOMINANCE_WARNING: کلیه شواهد بازیابی‌شده حاکی از اثرات هم‌افزا هستند. "
                    "احتمال سوگیری انتشار (Publication Bias) بالاست؛ پروتکل مطالعه باید آزمون‌های دقیق تفکیک آنتاگونیسم را شامل شود."
                )

            if balance_score >= 0.70:
                recommended_framing = "synergism"
                narrative = (
                    f"شواهد موجود به نفع فرضیه هم‌افزایی برهم‌کنش (وزن شواهد مثبت مستقیم/انتقالی: {int(balance_score*100)}٪) هستند؛ "
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
                    f"لذا بررسی بی‌طرفانه دوز-پاسخ و تعیین دقیق شاخص ترکیب (CI) جهت تشخیص پنجره درمانی الزامی است."
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
            has_direct_combination_evidence=has_direct_evidence,
            direct_combination_evidence_count=direct_combination_count,
            evidence_tiers_breakdown=tiers_counts,
            bias_warnings=warnings,
            framing_narrative_persian=narrative
        )
