#!/usr/bin/env python3
"""
generic_claim_entailment_engine.py - Dynamic Claim-Evidence Entailment & Causal Gate
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

Decomposes scientific prose into atomic claims, audits 7-level entailment against source evidence,
enforces causal vs correlational language boundaries, and checks numerical traceability.
"""

import re
import json
from typing import Dict, List, Any, Optional

CAUSAL_VERBS = [
    r'\bcauses\b', r'\bcaused\b', r'\bcausing\b',
    r'\bdrives\b', r'\bdriven\b', r'\bdriving\b',
    r'\binduces\b', r'\binduced\b', r'\binducing\b',
    r'\btriggers\b', r'\btriggered\b', r'\btriggering\b',
    r'\bis responsible for\b', r'\bleads directly to\b'
]

OBSERVATIONAL_DESIGNS = [
    "OBSERVATIONAL_COHORT_CASE_CONTROL",
    "CROSS_SECTIONAL",
    "ECOLOGICAL_STUDY",
    "CASE_SERIES"
]

class GenericClaimEntailmentEngine:
    """Audits scientific claim entailment, overclaim risks, and numerical traceability."""

    @staticmethod
    def detect_causal_overclaim(claim_text: str, source_study_design: str) -> Optional[Dict[str, str]]:
        """Flags unwarranted causal claims derived from observational designs."""
        text_lower = claim_text.lower()
        if source_study_design in OBSERVATIONAL_DESIGNS:
            for pattern in CAUSAL_VERBS:
                if re.search(pattern, text_lower):
                    return {
                        "flag": "OVERCLAIM_CAUSAL_INFERENCE_FROM_OBSERVATIONAL_DATA",
                        "detected_verb": pattern.replace(r'\b', ''),
                        "recommendation": "Replace causal phrasing with correlational language (e.g., 'is associated with', 'correlates with')."
                    }
        return None

    @staticmethod
    def extract_numbers(text: str) -> List[str]:
        """Extracts numerical quantities and percentages from claim strings."""
        return re.findall(r'\b\d+(?:\.\d+)?(?:%|(?:\s*(?:µM|uM|mM|mg/kg|Gy|h|hours|fold|CI|p)))?', text)

    @classmethod
    def evaluate_claim_entailment(
        cls,
        claim_id: str,
        claim_text: str,
        source_study: Dict[str, Any],
        supporting_facts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Evaluates 7-level entailment status for an atomic claim."""
        study_design = source_study.get("study_design", "UNKNOWN")
        causal_check = cls.detect_causal_overclaim(claim_text, study_design)

        if not supporting_facts:
            entailment_status = "UNSUPPORTED"
            directness = "NO_EVIDENCE"
        else:
            # Check fact directness
            has_direct = any(f.get("directness") == "DIRECT_EVIDENCE" for f in supporting_facts)
            has_indirect = any(f.get("directness") in ["INDIRECT_EVIDENCE", "INFERENCE"] for f in supporting_facts)
            has_hypothesis = any(f.get("directness") == "HYPOTHESIS" for f in supporting_facts)

            if has_direct:
                entailment_status = "DIRECTLY_SUPPORTED"
                directness = "DIRECT"
            elif has_indirect:
                entailment_status = "INDIRECTLY_SUPPORTED"
                directness = "INDIRECT"
            elif has_hypothesis:
                entailment_status = "HYPOTHESIS_ONLY"
                directness = "SPECULATIVE"
            else:
                entailment_status = "PARTIALLY_SUPPORTED"
                directness = "PARTIAL"

        # Check numbers in claim against facts
        claim_numbers = cls.extract_numbers(claim_text)
        untraced_numbers = []
        if supporting_facts:
            fact_texts = " ".join([str(f.get("text_or_data", "")) for f in supporting_facts])
            for num in claim_numbers:
                core_num = re.findall(r'\d+(?:\.\d+)?', num)
                if core_num and core_num[0] not in fact_texts:
                    untraced_numbers.append(num)

        return {
            "claim_id": claim_id,
            "claim_text": claim_text,
            "source_study_id": source_study.get("study_id"),
            "entailment_status": entailment_status,
            "directness": directness,
            "causal_overclaim_warning": causal_check,
            "numerical_traceability": {
                "claim_numbers_found": claim_numbers,
                "untraced_numbers": untraced_numbers,
                "hallucination_risk": len(untraced_numbers) > 0
            }
        }


if __name__ == "__main__":
    study_obs = {"study_id": "STUDY_OBS_01", "study_design": "OBSERVATIONAL_COHORT_CASE_CONTROL"}
    fact = {"directness": "DIRECT_EVIDENCE", "text_or_data": "Risk ratio 1.45, p=0.01"}
    
    # Overclaim test
    res = GenericClaimEntailmentEngine.evaluate_claim_entailment(
        "CLM_01", "Elevated biomarker X causes cardiovascular mortality (RR = 1.45).",
        study_obs, [fact]
    )
    print("Claim 1 Status:", res["entailment_status"])
    print("Overclaim Flag:", res["causal_overclaim_warning"])
    print("Hallucination Risk:", res["numerical_traceability"]["hallucination_risk"])
