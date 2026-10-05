#!/usr/bin/env python3
"""
generic_claim_entailment_engine.py - Dynamic Claim-Evidence Entailment & Causal Gate
Proposal-Nevisi Engine v8.2 (Universal Biomedical Architecture)

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
    r'\bcures\b', r'\bcured\b', r'\bcuring\b',
    r'\btreats\b', r'\btreated\b',
    r'\beliminates\b', r'\beliminated\b',
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

    INJECTION_PATTERNS = [
        r'ignore\s+(?:all\s+)?(?:previous\s+)?instructions',
        r'system\s+prompt',
        r'override\s+all\s+rules',
        r'<script[\s>]',
        r'javascript:',
        r'data:\s*text/html',
        r'<\|im_start\|>system',
        r'\[SYSTEM\]',
        r'<<<SYSTEM>>>',
        r'style\s*=\s*["\']display\s*:\s*none',
        r'eval\s*\(\s*atob\s*\(',
        r'base64\s*,\s*[A-Za-z0-9+/=]{10,}',
        r'دستورات\s+قبلی\s+را\s+نادیده\s+بگیر',
        r'قوانین\s+سیستم\s+را\s+لغو\s+کن',
        r'پرامپت\s+(?:سیستم|قبلی)\s+را\s+(?:پاک|حذف|نادیده)'
    ]

    ZERO_WIDTH_CHARS = [
        '\u200b', '\u200c', '\u200d', '\ufeff', '\u2060', '\u00ad'
    ]

    @classmethod
    def sanitize_text(cls, text: str, trust_boundary: str = "SOURCE_DOCUMENT") -> Dict[str, Any]:
        """Detects prompt injection or hostile payloads across trust boundaries while protecting legitimate scientific terms (Phase 15)."""
        is_suspicious = False
        flagged_patterns = []
        
        # Check zero-width hidden characters
        has_zero_width = any(c in text for c in cls.ZERO_WIDTH_CHARS)
        if has_zero_width:
            is_suspicious = True
            flagged_patterns.append("ZERO_WIDTH_CHARACTER_OBFUSCATION")

        cleaned = text
        for c in cls.ZERO_WIDTH_CHARS:
            cleaned = cleaned.replace(c, '')

        for pat in cls.INJECTION_PATTERNS:
            if re.search(pat, cleaned, re.IGNORECASE):
                is_suspicious = True
                flagged_patterns.append(pat)
                cleaned = re.sub(pat, "[SANITIZED_PROMPT_INJECTION]", cleaned, flags=re.IGNORECASE)

        return {
            "trust_boundary": trust_boundary,
            "is_suspicious": is_suspicious,
            "flagged_patterns": flagged_patterns,
            "sanitized_text": cleaned,
            "security_status": "POTENTIAL_INJECTION_FLAGGED" if is_suspicious else "CLEAN"
        }

    @classmethod
    def parse_and_normalize_citations(cls, text: str) -> Dict[str, Any]:
        """Parses citations across bracketed numbers [1], ranges [1-3], lists [1,2,5], and author-year formats (Phase 13)."""
        citation_indices = set()
        author_citations = []

        # 1. Bracketed numerical citations: [1], [1-3], [1–3], [1, 2, 5], [1,2,5]
        bracket_matches = re.findall(r'\[([0-9\s,\-–—]+)\]', text)
        for bm in bracket_matches:
            parts = [p.strip() for p in re.split(r'[,،]', bm) if p.strip()]
            for p in parts:
                range_match = re.match(r'^(\d+)\s*[\-–—]\s*(\d+)$', p)
                if range_match:
                    start_idx = int(range_match.group(1))
                    end_idx = int(range_match.group(2))
                    if start_idx <= end_idx and (end_idx - start_idx) <= 50:
                        for idx in range(start_idx, end_idx + 1):
                            citation_indices.add(idx)
                    else:
                        citation_indices.add(start_idx)
                        citation_indices.add(end_idx)
                elif p.isdigit():
                    citation_indices.add(int(p))

        # 2. Author-year citations: (Author et al., 2024) or Author et al. (2024)
        author_matches = re.findall(r'(?:([A-Z][a-z]+(?:\s+et\s+al\.?)?)[,\s]+\(?(\d{4})\)?)', text)
        for auth, yr in author_matches:
            author_citations.append({"author": auth.strip(), "year": int(yr)})

        sorted_indices = sorted(list(citation_indices))
        return {
            "raw_text": text,
            "numerical_citations": sorted_indices,
            "author_citations": author_citations,
            "total_citations_found": len(sorted_indices) + len(author_citations),
            "normalized_citation_string": f"[{','.join(str(i) for i in sorted_indices)}]" if sorted_indices else ""
        }

    @classmethod
    def audit_numerical_provenance(
        cls,
        claim_val: float,
        source_record: Dict[str, Any],
        tolerance: float = 0.05
    ) -> Dict[str, Any]:
        """Audits numerical traceability from claim back to source record with formula and unit verification (Phase 12)."""
        orig_val = source_record.get("original_value")
        unit_source = str(source_record.get("unit", "")).strip().lower()
        unit_claim = str(source_record.get("claim_unit", unit_source)).strip().lower()
        formula = source_record.get("transformation_formula")
        rounding = source_record.get("rounding_places", 2)
        has_source = bool(source_record.get("source_location") or source_record.get("study_id"))

        issues = []
        if not has_source:
            issues.append("MISSING_SOURCE")

        if orig_val is None:
            issues.append("MISSING_ORIGINAL_VALUE")
            calc_val = None
        else:
            calc_val = float(orig_val)
            if formula:
                if formula == "PERCENT_TO_RATIO":
                    calc_val = float(orig_val) / 100.0
                elif formula == "RATIO_TO_PERCENT":
                    calc_val = float(orig_val) * 100.0
                elif formula == "MOLAR_TO_MICROMOLAR":
                    calc_val = float(orig_val) * 1e6
                elif formula == "MICROMOLAR_TO_MOLAR":
                    calc_val = float(orig_val) / 1e6
                elif formula == "NATURAL_LOG_TO_HR":
                    import math
                    calc_val = math.exp(float(orig_val))
                elif formula == "INVALID_FORMULA":
                    issues.append("WRONG_FORMULA")
                else:
                    calc_val = float(orig_val)

            if unit_source != unit_claim and not formula:
                issues.append("WRONG_UNIT")

            if calc_val is not None:
                calc_rounded = round(calc_val, rounding)
                if abs(claim_val - calc_rounded) > tolerance and abs(claim_val - calc_val) > tolerance:
                    issues.append("WRONG_CONVERSION_OR_ROUNDING")

        is_valid = len(issues) == 0
        return {
            "claim_value": claim_val,
            "original_value": orig_val,
            "unit_source": unit_source,
            "unit_claim": unit_claim,
            "transformation_formula": formula,
            "calculated_value": calc_val,
            "is_provenance_verified": is_valid,
            "provenance_status": "VERIFIED_NUMERICAL_PROVENANCE" if is_valid else "NUMERICAL_DISCREPANCY_FLAGGED",
            "detected_issues": issues
        }

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

    @classmethod
    def cross_check_article_sections(
        cls,
        abstract_text: str,
        results_text: str,
        discussion_text: str,
        conclusion_text: str
    ) -> Dict[str, Any]:
        """Cross-checks consistency between Abstract, Results, Discussion, and Conclusion (Phase 15).
        Flags overclaims, mismatches, and subgroup overgeneralizations.
        """
        flags = []
        abs_l = abstract_text.lower()
        res_l = results_text.lower()
        disc_l = discussion_text.lower()
        conc_l = conclusion_text.lower()

        # 1. Abstract / Results Mismatch (e.g. significance claimed in abstract but not in results)
        if ("statistically significant" in abs_l or "significant improvement" in abs_l) and ("p > 0.05" in res_l or "not significant" in res_l):
            flags.append({
                "type": "ABSTRACT_RESULT_MISMATCH",
                "detail": "Abstract claims significant effect whereas results document non-significant outcome (p > 0.05)."
            })

        # 2. Discussion Overgeneralization
        if any(w in disc_l for w in ["cures all", "universal benefit", "completely eradicates"]) and not any(w in res_l for w in ["100% cure", "complete eradication"]):
            flags.append({
                "type": "DISCUSSION_OVERGENERALIZATION",
                "detail": "Discussion claims universal efficacy unsupported by granular numerical data in Results section."
            })

        # 3. Conclusion Overclaim
        if any(w in conc_l for w in ["proves beyond doubt", "conclusively established as standard of care"]) and any(w in disc_l for w in ["preliminary", "underpowered", "limited sample"]):
            flags.append({
                "type": "CONCLUSION_OVERCLAIM",
                "detail": "Conclusion asserts definitive practice changes despite Discussion explicitly acknowledging preliminary limitations."
            })

        # 4. Subgroup Generalization
        if "subgroup" in res_l and ("post-hoc" in res_l or "exploratory" in res_l):
            if not ("subgroup" in conc_l or "exploratory" in conc_l):
                flags.append({
                    "type": "SUBGROUP_GENERALIZATION",
                    "detail": "Exploratory subgroup finding in Results is presented as a general primary outcome in Conclusion."
                })

        return {
            "is_consistent": len(flags) == 0,
            "mismatch_count": len(flags),
            "flagged_inconsistencies": flags,
            "audit_verdict": "ARTICLE_SECTIONS_CONSISTENT" if len(flags) == 0 else "SECTION_DISCREPANCIES_DETECTED"
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
        """Evaluates 7-level scientific entailment while strictly separating citation linkage, source traceability, and entailment (Phase 11)."""
        study_design = source_study.get("study_design", "UNKNOWN")
        causal_check = cls.detect_causal_overclaim(claim_text, study_design)

        # 1. Citation Linkage
        has_study_id = bool(source_study.get("study_id"))
        citation_linkage = {
            "is_linked": has_study_id,
            "study_id": source_study.get("study_id")
        }

        # 2. Source Traceability
        loc = source_study.get("source_location") or next((f.get("source_location") for f in supporting_facts if f.get("source_location")), None)
        source_traceability = {
            "is_traceable": bool(loc),
            "recorded_location": loc,
            "retrieval_tier": source_study.get("retrieval_tier", "PEER_REVIEWED_DATABASE")
        }

        # 3. Scientific Entailment
        if not supporting_facts:
            entailment_status = "UNSUPPORTED"
            directness = "NO_EVIDENCE"
        else:
            has_contradiction = any(
                f.get("direction") in ["CONTRADICTS", "OPPOSING", "NEGATIVE"] or
                f.get("directness") == "CONTRADICTED" or
                "contradict" in str(f.get("text_or_data", "")).lower()
                for f in supporting_facts
            )
            has_direct = any(f.get("directness") == "DIRECT_EVIDENCE" for f in supporting_facts)
            has_indirect = any(f.get("directness") in ["INDIRECT_EVIDENCE", "INFERENCE"] for f in supporting_facts)
            has_hypothesis = any(f.get("directness") == "HYPOTHESIS" for f in supporting_facts)

            if has_contradiction:
                entailment_status = "CONTRADICTED"
                directness = "CONTRADICTED"
            elif has_direct:
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
            "citation_linkage": citation_linkage,
            "source_traceability": source_traceability,
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
        has_combo_assay = bool(
            source_study.get("quantitative_combination_index_extracted") or
            source_study.get("combo_index_extracted") or
            source_study.get("is_combination_study") or
            "combination" in str(source_study.get("study_design", "")).lower()
        )
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

    @classmethod
    def build_claim_provenance_map(cls, proposal_claims: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Constructs an exhaustive CLAIM_PROVENANCE_MAP (Prompt Pt 10, 39).
        Enforces 6-level strict chain:
        Proposal sentence -> Atomic claim -> Evidence passage -> Study -> DOI/PMID/identifier -> Database/source.
        Prohibits numerical claims without full granular provenance.
        """
        provenance_records = []
        untraced_numerical_claims = []

        for item in proposal_claims:
            sentence = item.get("sentence", "")
            cid = item.get("claim_id", "CLM_01")
            claim_text = item.get("claim_text", sentence)
            passage = item.get("evidence_passage", item.get("passage", ""))
            study_id = item.get("study_id", item.get("study", ""))
            doi = item.get("doi", item.get("pmid", ""))
            db_source = item.get("database_source", "PubMed/Crossref")

            has_numbers = bool(cls.extract_numbers(claim_text))
            is_fully_traceable = bool(sentence and claim_text and passage and study_id and doi)

            if has_numbers and not is_fully_traceable:
                untraced_numerical_claims.append({
                    "claim_id": cid,
                    "claim_text": claim_text,
                    "missing_provenance": "NUMERICAL_CLAIM_LACKS_COMPLETE_PASSAGE_OR_IDENTIFIER"
                })

            provenance_records.append({
                "proposal_sentence": sentence,
                "atomic_claim_id": cid,
                "atomic_claim_text": claim_text,
                "evidence_passage": passage,
                "study_identifier": study_id,
                "citation_doi_or_pmid": doi,
                "originating_database": db_source,
                "has_numbers": has_numbers,
                "is_traceable": is_fully_traceable
            })

        all_numerical_traceable = (len(untraced_numerical_claims) == 0)

        return {
            "total_claims_mapped": len(provenance_records),
            "fully_traceable_count": sum(1 for p in provenance_records if p["is_traceable"]),
            "untraced_numerical_claims_count": len(untraced_numerical_claims),
            "untraced_numerical_claims": untraced_numerical_claims,
            "provenance_compliance_status": "COMPLIANT" if all_numerical_traceable else "NON_COMPLIANT_UNTRACED_NUMBERS",
            "provenance_map": provenance_records
        }

    @staticmethod
    def audit_numerical_transformations(transformations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Audits mathematical transformations (percentages, means, CIs, effect sizes, unit conversions) (Prompt Pt 17).
        Guarantees original value, formula, and calculated value are fully traceable.
        """
        verified_transforms = []
        invalid_transforms = []

        for t in transformations:
            orig = t.get("original_value")
            formula = t.get("formula")
            final_val = t.get("final_value")
            unit_from = t.get("unit_from")
            unit_to = t.get("unit_to")

            if orig is not None and formula and final_val is not None:
                verified_transforms.append({
                    "transformation_id": t.get("transformation_id", "TR_01"),
                    "original_value": orig,
                    "unit_from": unit_from,
                    "formula": formula,
                    "final_value": final_val,
                    "unit_to": unit_to,
                    "is_traceable": True
                })
            else:
                invalid_transforms.append({
                    "transformation": t,
                    "reason": "MISSING_ORIGINAL_VALUE_OR_FORMULA"
                })

        return {
            "total_transformations_audited": len(transformations),
            "verified_count": len(verified_transforms),
            "invalid_count": len(invalid_transforms),
            "is_audit_clean": len(invalid_transforms) == 0,
            "transformations": verified_transforms,
            "audit_note": "All numerical conversions are mathematically traceable." if len(invalid_transforms) == 0 else "Untraced mathematical transformations detected."
        }

    @classmethod
    def build_claim_citation_matrix(
        cls,
        claims: List[Dict[str, Any]],
        evidence_corpus: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Constructs a CLAIM_CITATION_MATRIX mapping paragraph claims to immediate supporting evidence (Part 13)."""
        study_map = {s.get("study_id") or s.get("doi"): s for s in evidence_corpus}
        matrix_rows = []
        unlinked_claims = []

        for c in claims:
            cid = c.get("claim_id", "CLM_01")
            text = c.get("claim_text", "")
            s_id = c.get("study_id") or c.get("source_study_id")
            s_rec = study_map.get(s_id)

            if s_rec:
                matrix_rows.append({
                    "claim_id": cid,
                    "claim_text": text,
                    "study_id": s_id,
                    "doi": s_rec.get("doi", "NOT_REPORTED"),
                    "year": s_rec.get("year", "NOT_REPORTED"),
                    "study_design": s_rec.get("study_design", "NOT_REPORTED"),
                    "entailment_level": c.get("entailment_level", "DIRECTLY_SUPPORTED"),
                    "source_location": s_rec.get("source_location", "NOT_REPORTED")
                })
            else:
                unlinked_claims.append(cid)

        is_complete = (len(unlinked_claims) == 0)
        return {
            "matrix_type": "CLAIM_CITATION_MATRIX",
            "total_claims": len(claims),
            "linked_claims_count": len(matrix_rows),
            "unlinked_claims_count": len(unlinked_claims),
            "unlinked_claim_ids": unlinked_claims,
            "is_matrix_complete": is_complete,
            "matrix": matrix_rows
        }

    @classmethod
    def audit_evidence_to_text_density(
        cls,
        text_word_count: int,
        cited_evidence_count: int,
        min_density_ratio: float = 0.015
    ) -> Dict[str, Any]:
        """Audits EVIDENCE_TO_TEXT_DENSITY ensuring text is grounded in substantive evidence corpus (Part 39).
        Calculates citations per 100 words. Prevents thin text padding unsupported by evidence.
        """
        ratio = (cited_evidence_count / max(text_word_count, 1))
        citations_per_hundred_words = round(ratio * 100, 2)
        is_adequate = (ratio >= min_density_ratio)

        return {
            "audit_type": "EVIDENCE_TO_TEXT_DENSITY_AUDIT",
            "text_word_count": text_word_count,
            "cited_evidence_count": cited_evidence_count,
            "density_ratio": round(ratio, 4),
            "citations_per_hundred_words": citations_per_hundred_words,
            "min_required_ratio": min_density_ratio,
            "status": "DENSE_EVIDENCE_GROUNDED" if is_adequate else "THIN_EVIDENCE_PADDING_SUSPECTED",
            "is_density_compliant": is_adequate,
            "recommendation": "Text density meets scientific citation grounding standards." if is_adequate else "Text length is disproportionately large compared to cited evidence; strengthen empirical grounding."
        }

    @classmethod
    def audit_citation_to_claims(
        cls,
        claims: List[Dict[str, Any]],
        reference_records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """v8.3 Citation-to-Claim Audit (Section 10):
        Verifies every scientific assertion against supporting references and evidence relationships.
        Enforces that unsupported overclaims (such as direct synergy without direct combination data)
        are flagged for REVISION or REJECTION.
        """
        ref_map = {}
        for r in reference_records:
            for field in ["ref_id", "pmid", "doi", "citation_number"]:
                val = r.get(field)
                if val:
                    ref_map[str(val).strip().lower()] = r

        audited_claims = []
        rejected_claims = []
        revised_claims = []
        accepted_claims = []

        for clm in claims:
            cid = clm.get("claim_id", "CLM_UNKNOWN")
            ctext = clm.get("claim_text", "")
            supp_refs = clm.get("supporting_references", [])
            
            # Map supporting references to records
            matched_records = []
            for sr in supp_refs:
                key = str(sr).strip().lower()
                if key in ref_map:
                    matched_records.append(ref_map[key])


            # Evaluate synergy claim strictness
            is_synergy = bool(re.search(r'\b(?:synergistic|synergy|cooperative|supra-additive)\b', ctext, re.IGNORECASE))
            
            support_strength = "UNSUPPORTED"
            ev_rel = "INDIRECT"
            status = "ACCEPT"
            reason = "Supported by empirical reference."

            if not matched_records:
                status = "REJECT"
                reason = "No verified supporting reference provided in portfolio."
                support_strength = "UNSUPPORTED"
            elif is_synergy:
                # Synergy claim requires direct combination evidence
                has_direct_synergy = any(r.get("synergy_evidence") == "DIRECT" for r in matched_records)
                has_analog_synergy = any(r.get("synergy_evidence") == "ANALOGOUS" for r in matched_records)
                
                if has_direct_synergy:
                    support_strength = "DIRECT"
                    ev_rel = "DIRECT"
                    status = "ACCEPT"
                    reason = "Direct combination evidence with quantitative synergy assessment."
                elif has_analog_synergy:
                    support_strength = "ANALOGOUS"
                    ev_rel = "CLOSE_ANALOG"
                    status = "REVISE"
                    reason = "Direct combination evidence not identified; claim must use cautious analogous language."
                else:
                    support_strength = "INSUFFICIENT"
                    ev_rel = "INDIRECT"
                    status = "REJECT"
                    reason = "Synergy cannot be inferred from separate monotherapy studies."
            else:
                # Non-synergy claims
                best_rel = "INDIRECT"
                for mr in matched_records:
                    mr_rel = mr.get("evidence_relationship", "INDIRECT")
                    if mr_rel == "DIRECT":
                        best_rel = "DIRECT"
                        break
                    elif mr_rel == "CLOSE_ANALOG" and best_rel != "DIRECT":
                        best_rel = "CLOSE_ANALOG"
                    elif mr_rel == "MECHANISTIC_SUPPORT" and best_rel not in ["DIRECT", "CLOSE_ANALOG"]:
                        best_rel = "MECHANISTIC_SUPPORT"
                    elif mr_rel == "METHOD_SUPPORT" and best_rel not in ["DIRECT", "CLOSE_ANALOG", "MECHANISTIC_SUPPORT"]:
                        best_rel = "METHOD_SUPPORT"

                ev_rel = best_rel
                support_strength = "DIRECT" if best_rel == "DIRECT" else ("PARTIAL" if best_rel in ["CLOSE_ANALOG", "MECHANISTIC_SUPPORT"] else "INDIRECT")
                status = "ACCEPT" if best_rel in ["DIRECT", "CLOSE_ANALOG", "MECHANISTIC_SUPPORT", "METHOD_SUPPORT"] else "REVISE"

            item = {
                "claim_id": cid,
                "claim_text": ctext,
                "supporting_references": supp_refs,
                "support_strength": support_strength,
                "evidence_relationship": ev_rel,
                "status": status,
                "audit_note": reason
            }
            audited_claims.append(item)
            if status == "ACCEPT":
                accepted_claims.append(item)
            elif status == "REVISE":
                revised_claims.append(item)
            else:
                rejected_claims.append(item)

        return {
            "audit_type": "CITATION_TO_CLAIM_AUDIT",
            "total_claims_audited": len(claims),
            "accepted_count": len(accepted_claims),
            "revised_count": len(revised_claims),
            "rejected_count": len(rejected_claims),
            "all_passed": len(rejected_claims) == 0,
            "audited_claims": audited_claims,
            "rejected_claims": rejected_claims,
            "revised_claims": revised_claims
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
