#!/usr/bin/env python3
"""
generic_reference_auditor.py - Topic-Agnostic Bibliographic, Temporal & Citation Auditor
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

Performs field-level verification against Crossref/PubMed, audits temporal boundaries,
validates foundational justifications, and strictly detects citation padding.
"""

import re
import json
import difflib
from typing import Dict, List, Any, Optional

class GenericReferenceAuditor:
    """Universal reference auditor operating without hard-coded biological assumptions."""

    def __init__(
        self,
        current_year: int = 2026,
        max_primary_age_years: int = 6,
        min_required_references: int = 15,
        target_model: Optional[Dict[str, Any]] = None
    ):
        self.current_year = current_year
        self.max_primary_age = max_primary_age_years
        self.cutoff_year = current_year - max_primary_age_years
        self.min_required_references = min_required_references
        self.target_model = target_model or {}

    def audit_bibliographic_fields(self, local_ref: Dict[str, Any], verified_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Compares local citation record with authoritative Crossref/PubMed data."""
        title_local = local_ref.get("title", "").strip().lower()
        title_verified = verified_metadata.get("title", "").strip().lower()

        sim = difflib.SequenceMatcher(None, title_local, title_verified).ratio() if (title_local and title_verified) else 0.0

        year_local = local_ref.get("year")
        year_verified = verified_metadata.get("year")
        year_match = (year_local == year_verified) if (year_local and year_verified) else False

        authors_local = [a.lower() for a in local_ref.get("authors", [])]
        authors_verified = [a.lower() for a in verified_metadata.get("authors", [])]
        author_match = any(a in " ".join(authors_verified) for a in authors_local) if authors_local else False

        if sim >= 0.85 and year_match:
            status = "EXACT_VERIFIED"
        elif sim >= 0.60:
            status = "MINOR_VARIATION"
        else:
            status = "CONFLICT_OR_UNVERIFIED"

        return {
            "ref_id": local_ref.get("ref_id"),
            "verification_status": status,
            "title_similarity": round(sim, 3),
            "year_match": year_match,
            "author_overlap": author_match,
            "doi": local_ref.get("doi")
        }

    def audit_temporal_tier(self, ref: Dict[str, Any]) -> Dict[str, Any]:
        """Enforces the 6-year recency rule with explicit foundational justification requirements."""
        year = ref.get("year", self.current_year)
        justification = ref.get("foundational_justification", {})

        if year >= self.cutoff_year:
            tier = "RECENT_PRIMARY_EVIDENCE"
            justified = True
            note = f"Published in {year} (within {self.max_primary_age}-year window)."
        else:
            tier = "FOUNDATIONAL/HISTORICAL_EVIDENCE"
            if justification.get("is_justified"):
                justified = True
                note = f"Foundational exception approved: {justification.get('category')} - {justification.get('rationale')}"
            else:
                justified = False
                note = f"Published in {year} (< {self.cutoff_year}) without verified foundational justification."

        return {
            "ref_id": ref.get("ref_id"),
            "year": year,
            "temporal_tier": tier,
            "is_temporally_valid": justified,
            "audit_note": note
        }

    def audit_citation_padding(
        self,
        reference_set: List[Dict[str, Any]],
        proposal_text: str,
        claim_map: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """Strictly detects unused references, citation padding, and missing text markers."""
        padding_detected = []
        valid_refs = []

        # Find all cited indices in proposal text like [1], [2], [1-3]
        cited_indices = set()
        matches = re.findall(r'\[(\d+(?:[,\s–-]+\d+)*)\]', proposal_text)
        for m in matches:
            for part in re.split(r'[,–-]', m):
                part = part.strip()
                if part.isdigit():
                    cited_indices.add(int(part))

        for idx, ref in enumerate(reference_set, 1):
            ref_id = ref.get("ref_id", f"REF_{idx}")
            is_cited_in_text = (idx in cited_indices)
            claims_supported = claim_map.get(ref_id, ref.get("claims_supported", []))

            has_claims = len(claims_supported) > 0

            if not is_cited_in_text:
                padding_detected.append({
                    "ref_id": ref_id,
                    "index": idx,
                    "reason": "NOT_CITED_IN_PROPOSAL_TEXT",
                    "details": f"Reference [ {idx} ] exists in bibliography but has zero inline citations."
                })
            elif not has_claims:
                padding_detected.append({
                    "ref_id": ref_id,
                    "index": idx,
                    "reason": "ZERO_SUPPORTED_CLAIMS",
                    "details": f"Reference [ {idx} ] is cited in text but maps to zero validated claims."
                })
            else:
                valid_refs.append(ref_id)

        meets_min = len(valid_refs) >= self.min_required_references

        return {
            "total_references_evaluated": len(reference_set),
            "valid_active_references": len(valid_refs),
            "padding_detected_count": len(padding_detected),
            "padding_incidents": padding_detected,
            "meets_minimum_quota": meets_min,
            "minimum_quota_target": self.min_required_references,
            "overall_status": "PASS" if (len(padding_detected) == 0 and meets_min) else "FAIL"
        }


if __name__ == "__main__":
    auditor = GenericReferenceAuditor(current_year=2026, min_required_references=2)
    sample_refs = [
        {"ref_id": "R1", "year": 2024, "title": "Modern cardiology trial", "claims_supported": ["CLM_1"]},
        {"ref_id": "R2", "year": 1984, "title": "Classical method", "claims_supported": ["CLM_2"],
         "foundational_justification": {"is_justified": True, "category": "FOUNDATIONAL_MATHEMATICAL_MODEL", "rationale": "Defines median effect equation"}},
        {"ref_id": "R3", "year": 2022, "title": "Unused paper", "claims_supported": []}
    ]
    text = "Recent evidence demonstrates cardiac benefits [1]. Classical equations were applied [2]."
    padding_report = auditor.audit_citation_padding(sample_refs, text, {"R1": ["CLM_1"], "R2": ["CLM_2"]})
    print("Padding Audit Status:", padding_report["overall_status"])
    print("Padding Incidents:", len(padding_report["padding_incidents"]))
