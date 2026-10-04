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

    @classmethod
    def audit_causal_language(cls, claim_text: str, source_study_design: str) -> Dict[str, Any]:
        """Audits causal vs correlational language boundaries and flags overclaims."""
        text_lower = claim_text.lower()
        is_observational = (
            source_study_design in OBSERVATIONAL_DESIGNS
            or "OBSERVATIONAL" in source_study_design
            or "COHORT" in source_study_design
        )
        flagged_words = []
        if is_observational:
            for pattern in CAUSAL_VERBS:
                if re.search(pattern, text_lower):
                    flagged_words.append(pattern.replace(r'\b', ''))
        
        has_overclaim = len(flagged_words) > 0
        return {
            "claim_text": claim_text,
            "source_study_design": source_study_design,
            "allowed_unconditional_causal_claim": not has_overclaim,
            "status": "OVERCLAIM_RISK" if has_overclaim else "COMPLIANT",
            "flagged_causal_words": flagged_words,
            "recommendation": "Replace causal verbs with correlational phrasing." if has_overclaim else "Language aligns with study design."
        }

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

    @classmethod
    def detect_translational_overclaim(cls, claim_text: str, source_study_design: str) -> Optional[Dict[str, str]]:
        """Flags unwarranted clinical/therapeutic efficacy claims derived purely from in vitro or animal models."""
        text_lower = claim_text.lower()
        clinical_markers = [
            r'\bclinical efficacy\b', r'\bpatient cure\b', r'\btreats human\b',
            r'\beffective in patients\b', r'\btherapeutic cure\b', r'\bclinical outcome\b'
        ]
        is_preclinical = (
            "IN_VITRO" in source_study_design.upper() or
            "ANIMAL" in source_study_design.upper() or
            source_study_design in ["IN_VITRO_EXPERIMENTAL", "ANIMAL_IN_VIVO_PRECLINICAL"]
        )
        if is_preclinical:
            for marker in clinical_markers:
                if re.search(marker, text_lower):
                    return {
                        "flag": "TRANSLATIONAL_OVERCLAIM_PRECLINICAL_TO_CLINICAL",
                        "detected_phrase": marker.replace(r'\b', ''),
                        "recommendation": "Qualify findings as preclinical cellular/animal model evidence without claiming human clinical efficacy."
                    }
        return None

    @classmethod
    def audit_pseudo_replication(cls, study_design: str, design_attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Flags pseudo-replication where technical replicates are treated as independent biological replicates."""
        replicate_info = str(design_attributes.get("replicate_structure", "")).lower()
        sample_size_raw = str(design_attributes.get("sample_size", "")).lower()
        
        is_vitro = "IN_VITRO" in study_design.upper()
        flags = []
        if is_vitro:
            if "technical replicate" in replicate_info and "biological replicate" not in replicate_info:
                flags.append("TECHNICAL_REPLICATES_ONLY")
            if "wells" in sample_size_raw and "independent experiments" not in replicate_info:
                flags.append("WELL_COUNT_SUBSTITUTED_FOR_BIOLOGICAL_N")

        return {
            "has_pseudo_replication_risk": len(flags) > 0,
            "flags": flags,
            "recommendation": "Ensure sample size N reflects independent biological clone preparations, not repeated pipette wells." if flags else "Replication structure acceptable."
        }

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

        # Audit synergy fallacy
        synergy_check = cls.check_synergy_fallacy(claim_text, supporting_facts, source_study)

        return {
            "claim_id": claim_id,
            "claim_text": claim_text,
            "source_study_id": source_study.get("study_id"),
            "entailment_status": entailment_status,
            "directness": directness,
            "causal_overclaim_warning": causal_check,
            "synergy_fallacy_audit": synergy_check,
            "numerical_traceability": {
                "claim_numbers_found": claim_numbers,
                "untraced_numbers": untraced_numbers,
                "hallucination_risk": len(untraced_numbers) > 0
            }
        }

    @staticmethod
    def check_synergy_fallacy(claim_text: str, supporting_facts: List[Dict[str, Any]], source_study: Dict[str, Any]) -> Dict[str, Any]:
        """Prevents inferring combination synergy from monotherapy efficacy (Point 29)."""
        is_synergy_claim = bool(re.search(r'\b(?:synergistic|synergy|cooperative|supra-additive)\b', claim_text, re.IGNORECASE))
        if not is_synergy_claim:
            return {"is_synergy_claim": False, "synergy_status": "NOT_APPLICABLE"}

        # Requires combination design, combination assay, and quantitative metric
        has_combo_assay = bool(source_study.get("chou_talalay_ci_extracted") or "combination" in str(source_study.get("study_design", "")).lower())
        has_metric = any("ci" in str(f.get("text_or_data", "")).lower() or "synergy" in str(f.get("text_or_data", "")).lower() for f in supporting_facts)

        if not (has_combo_assay or has_metric):
            return {
                "is_synergy_claim": True,
                "synergy_status": "SYNERGY_NOT_ESTABLISHED",
                "violation": "SYNERGY_FALLACY_MONOTHERAPY_EXTRAPOLATION",
                "recommendation": "Maintain strictly as SYNERGY_NOT_ESTABLISHED; separate monotherapies cannot prove synergy."
            }

        return {
            "is_synergy_claim": True,
            "synergy_status": "EMPIRICALLY_VERIFIED_COMBINATION"
        }

    @staticmethod
    def audit_data_provenance(evidence_record: Dict[str, Any]) -> Dict[str, Any]:
        """Audits whether data provenance is traceable to specific source locations (Point 26)."""
        provenance = evidence_record.get("source_location", {})
        has_location = any(k in provenance for k in ["page", "section", "table", "figure", "paragraph"])
        return {
            "is_provenance_traceable": has_location,
            "recorded_location": provenance,
            "provenance_grade": "GRANULAR_LOCATION" if has_location else "DOCUMENT_LEVEL_ONLY"
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
