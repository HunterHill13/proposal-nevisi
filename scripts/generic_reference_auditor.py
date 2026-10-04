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

try:
    from core_policies import TemporalPolicyConfig
except ImportError:
    from scripts.core_policies import TemporalPolicyConfig

class GenericReferenceAuditor:
    """Universal reference auditor operating without hard-coded biological assumptions."""

    def __init__(
        self,
        current_year: Optional[int] = None,
        max_primary_age_years: int = TemporalPolicyConfig.MAX_PRIMARY_EVIDENCE_AGE_YEARS,
        min_required_references: int = 15,
        target_model: Optional[Dict[str, Any]] = None
    ):
        import datetime
        self.current_year = current_year or datetime.datetime.now().year
        self.max_primary_age = max_primary_age_years
        self.cutoff_year = self.current_year - max_primary_age_years
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

        is_retracted = verified_metadata.get("is_retracted", False) or "retracted" in verified_metadata.get("status", "").lower() or "retraction" in title_verified.lower()
        is_corrected = verified_metadata.get("is_corrected", False) or "erratum" in title_verified.lower() or "corrigendum" in title_verified.lower()

        if is_retracted:
            status = "RETRACTED"
        elif is_corrected:
            status = "CORRECTED"
        elif sim >= 0.85 and year_match:
            status = "EXACT_VERIFIED"
        elif sim >= 0.60:
            status = "MINOR_VARIATION"
        elif (local_ref.get("doi") and verified_metadata.get("doi")) and sim < 0.40:
            status = "IDENTITY_CONFLICT"
        else:
            status = "CONFLICT_OR_UNVERIFIED"

        identity_conflict = (status == "IDENTITY_CONFLICT") or (sim < 0.40 and bool(title_local and title_verified))
        if identity_conflict and status != "RETRACTED":
            status = "IDENTITY_CONFLICT"

        return {
            "ref_id": local_ref.get("ref_id"),
            "verification_status": status,
            "title_similarity": round(sim, 3),
            "year_match": year_match,
            "author_overlap": author_match,
            "doi": local_ref.get("doi"),
            "is_retracted": is_retracted,
            "is_corrected": is_corrected,
            "identity_conflict": identity_conflict,
            "core_evidence_eligible": (status in ["EXACT_VERIFIED", "MINOR_VARIATION", "CORRECTED"])
        }

    def audit_temporal_tier(self, ref: Dict[str, Any]) -> Dict[str, Any]:
        """Enforces the 6-year recency rule with exact date parsing and 7 temporal classes (Parts 2 & 3)."""
        pub_date_str = ref.get("publication_date") or ref.get("date")
        year = ref.get("year")
        date_uncertain = False

        if pub_date_str:
            match = re.match(r'^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?', str(pub_date_str).strip())
            if match:
                parsed_year = int(match.group(1))
                year = year or parsed_year
            else:
                date_uncertain = True
        elif not year:
            date_uncertain = True

        if date_uncertain and not year:
            return {
                "ref_id": ref.get("ref_id"),
                "year": None,
                "publication_date": pub_date_str,
                "temporal_tier": "DATE_UNCERTAIN",
                "temporal_class": "DATE_UNCERTAIN",
                "evidence_role": "UNCERTAIN_ROLE",
                "age_justification": "DATE_UNCERTAIN",
                "is_temporally_valid": False,
                "core_evidence_eligible": False,
                "recent_evidence_eligible": False,
                "audit_note": "Publication date and year are completely unverified/uncertain."
            }

        year = year or self.current_year
        justification = ref.get("foundational_justification", {})
        evidence_role = ref.get("evidence_role", "PRIMARY_EVIDENCE")

        if year >= self.cutoff_year:
            tier = "RECENT_PRIMARY_EVIDENCE"
            temporal_class = "CORE_RECENT_PRIMARY" if evidence_role == "PRIMARY_EVIDENCE" else "CORE_RECENT_SECONDARY"
            age_justification = "RECENT_DIRECT_EVIDENCE"
            justified = True
            core_eligible = True
            recent_eligible = True
            note = f"Published in {year} (within {self.max_primary_age}-year window)."
        else:
            tier = "FOUNDATIONAL/HISTORICAL_EVIDENCE"
            if justification.get("is_justified"):
                cat = justification.get("category", "HISTORICAL_FOUNDATION")
                age_justification = cat
                justified = True
                recent_eligible = False
                core_eligible = (evidence_role != "PRIMARY_EVIDENCE")
                if cat in ["FOUNDATIONAL_MATHEMATICAL_MODEL", "STANDARDIZED_ASSAY_METHOD", "METHODOLOGICAL_LANDMARK"]:
                    temporal_class = "FOUNDATIONAL_METHODOLOGY"
                elif cat in ["ORIGINAL_DIAGNOSTIC_CRITERIA", "LANDMARK_HISTORICAL_BENCHMARK"]:
                    temporal_class = "LANDMARK_GUIDELINE"
                elif cat in ["CLASSICAL_STATISTICAL_METHOD"]:
                    temporal_class = "CLASSICAL_METHOD"
                else:
                    temporal_class = "HISTORICAL_BACKGROUND"
                note = f"Foundational exception approved: {age_justification} - {justification.get('rationale')}"
            else:
                temporal_class = "OUT_OF_WINDOW_NON_FOUNDATIONAL"
                age_justification = "OUTDATED_DIRECT_EVIDENCE"
                justified = False
                core_eligible = False
                recent_eligible = False
                note = f"Published in {year} (< {self.cutoff_year}) without verified foundational justification. Must be separated from core recent evidence."

        return {
            "ref_id": ref.get("ref_id"),
            "year": year,
            "publication_date": pub_date_str,
            "temporal_tier": tier,
            "temporal_class": temporal_class,
            "evidence_role": evidence_role,
            "age_justification": age_justification,
            "is_temporally_valid": justified,
            "core_evidence_eligible": core_eligible,
            "recent_evidence_eligible": recent_eligible,
            "audit_note": note
        }

    @staticmethod
    def audit_publication_status(ref_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Audits retraction, correction, expression of concern, and duplication (Prompt Pt 12, 43).
        Status values: RETRACTED, CORRECTION_AVAILABLE, EXPRESSION_OF_CONCERN, DUPLICATE_PUBLICATION, STANDARD_PEER_REVIEWED.
        Retracted papers MUST be excluded from core evidence synthesis.
        """
        title = str(ref_metadata.get("title", "")).lower()
        notes = str(ref_metadata.get("notes", "")).lower()
        raw_status = str(ref_metadata.get("status", "")).lower()

        is_retracted = ref_metadata.get("is_retracted", False) or "retracted" in raw_status or "retraction" in title or "retraction notice" in notes
        is_corrected = ref_metadata.get("is_corrected", False) or "erratum" in title or "corrigendum" in title or "correction" in raw_status
        is_concern = ref_metadata.get("expression_of_concern", False) or "expression of concern" in title or "expression of concern" in notes
        is_duplicate = ref_metadata.get("is_duplicate", False) or "duplicate publication" in notes

        if is_retracted:
            pub_status = "RETRACTED"
            action = "EXCLUDE_FROM_EVIDENCE_SYNTHESIS"
        elif is_concern:
            pub_status = "EXPRESSION_OF_CONCERN"
            action = "FLAG_METHODOLOGICAL_UNCERTAINTY"
        elif is_corrected:
            pub_status = "CORRECTION_AVAILABLE"
            action = "PREFER_CORRECTED_VERSION"
        elif is_duplicate:
            pub_status = "DUPLICATE_PUBLICATION"
            action = "CLUSTER_INTO_PRIMARY_STUDY_FAMILY"
        else:
            pub_status = "STANDARD_PEER_REVIEWED"
            action = "RETAIN_FOR_SYNTHESIS"

        return {
            "ref_id": ref_metadata.get("ref_id", ref_metadata.get("doi", "UNKNOWN")),
            "publication_status": pub_status,
            "action_required": action,
            "is_eligible_for_synthesis": pub_status != "RETRACTED",
            "is_corrected": is_corrected,
            "is_retracted": is_retracted
        }

    @staticmethod
    def resolve_effective_publication_date(ref_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Resolves between online publication date, print issue date, preprint date, and correction date (Prompt Pt 11)."""
        print_year = ref_metadata.get("year")
        online_date = ref_metadata.get("online_publication_date") or ref_metadata.get("epub_date")
        preprint_date = ref_metadata.get("preprint_date")
        correction_date = ref_metadata.get("correction_date")

        effective_year = print_year
        resolution_rule = "PRINT_ISSUE_YEAR"
        if online_date:
            try:
                y = int(str(online_date)[:4])
                effective_year = min(print_year or y, y)
                resolution_rule = "EARLIEST_OF_PRINT_OR_ONLINE"
            except (ValueError, TypeError):
                pass

        return {
            "effective_year": effective_year,
            "resolution_rule": resolution_rule,
            "has_correction_date": bool(correction_date),
            "is_preprint": bool(preprint_date and not print_year)
        }

    @staticmethod
    def resolve_database_disagreement(records: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Resolves metadata discrepancies across PubMed, Crossref, OpenAlex, and Europe PMC (Prompt Pt 31)."""
        authority_hierarchy = ["PubMed", "Crossref", "Europe PMC", "OpenAlex"]
        canonical_record = {}
        discrepancies = []

        fields = ["title", "year", "journal", "authors", "is_retracted"]
        for f in fields:
            observed_values = {}
            for db, rec in records.items():
                if f in rec and rec[f] is not None:
                    observed_values[db] = rec[f]

            unique_vals = set(str(v).strip().lower() for v in observed_values.values())
            if len(unique_vals) > 1:
                # Disagreement detected
                discrepancies.append({
                    "field": f,
                    "observed_across_databases": observed_values
                })

            # Pick highest authority
            selected_val = None
            selected_db = None
            for auth in authority_hierarchy:
                if auth in observed_values:
                    selected_val = observed_values[auth]
                    selected_db = auth
                    break
            if selected_val is not None:
                canonical_record[f] = selected_val

        return {
            "canonical_metadata": canonical_record,
            "has_discrepancies": len(discrepancies) > 0,
            "discrepancies_logged": discrepancies,
            "resolution_policy": "HIERARCHICAL_AUTHORITY_PUBMED_CROSSREF_EPMC_OPENALEX"
        }

    def audit_citation_placement(self, proposal_text: str, atomic_claims: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Audits that citations are placed immediately after relevant scientific assertions (Prompt Pt 34)."""
        misplaced_citations = []
        for clm in atomic_claims:
            cid = clm.get("claim_id", "")
            clm_text = clm.get("claim_text", "")
            # Verify that claim text in proposal is immediately followed by a citation bracket
            # e.g., 'claim statement [1]'
            pos = proposal_text.find(clm_text)
            if pos != -1:
                subsequent_snippet = proposal_text[pos + len(clm_text): pos + len(clm_text) + 30]
                if not re.search(r'\[\d+\]', subsequent_snippet):
                    misplaced_citations.append({
                        "claim_id": cid,
                        "claim_text": clm_text,
                        "issue": "CITATION_NOT_IMMEDIATELY_ADJACENT"
                    })

        return {
            "misplaced_citations_count": len(misplaced_citations),
            "misplaced_incidents": misplaced_citations,
            "placement_status": "COMPLIANT" if len(misplaced_citations) == 0 else "REVIEW_REQUIRED"
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

    @staticmethod
    def audit_evidence_retrieval_tier(study_evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Audits evidence retrieval tiers ensuring sensitive numerical claims come from verified sources (Phase 35).
        Tiers: FULL_TEXT_VERIFIED, ABSTRACT_VERIFIED, METADATA_ONLY, UNVERIFIED.
        """
        tier_counts = {"FULL_TEXT_VERIFIED": 0, "ABSTRACT_VERIFIED": 0, "METADATA_ONLY": 0, "UNVERIFIED": 0}
        sensitive_claims_demoted = []

        for s in study_evidence:
            tier = s.get("retrieval_tier") or ("FULL_TEXT_VERIFIED" if s.get("fulltext_available") else ("ABSTRACT_VERIFIED" if s.get("abstract") else "METADATA_ONLY"))
            if tier not in tier_counts:
                tier = "UNVERIFIED"
            tier_counts[tier] += 1

            # Numerical claims require at least ABSTRACT_VERIFIED or FULL_TEXT_VERIFIED
            has_quant = bool(s.get("quantitative_parameters") or s.get("dose_concentration_range"))
            if has_quant and tier in ["METADATA_ONLY", "UNVERIFIED"]:
                sensitive_claims_demoted.append({
                    "study_id": s.get("study_id"),
                    "tier": tier,
                    "reason": "QUANTITATIVE_CLAIM_FROM_METADATA_ONLY"
                })

            # Abstract-only cannot sustain granular methodology, subgroup, or deep parameter claims (Part 10)
            has_granular = bool(s.get("requires_full_text") or s.get("subgroup_analysis_extracted") or s.get("unreported_in_abstract"))
            if has_granular and tier in ["ABSTRACT_VERIFIED", "METADATA_ONLY", "UNVERIFIED"]:
                sensitive_claims_demoted.append({
                    "study_id": s.get("study_id"),
                    "tier": tier,
                    "reason": "GRANULAR_PARAMETRIC_CLAIM_REQUIRES_FULL_TEXT"
                })

        return {
            "tier_distribution": tier_counts,
            "total_studies_audited": len(study_evidence),
            "sensitive_claims_demoted": sensitive_claims_demoted,
            "is_tier_compliant": len(sensitive_claims_demoted) == 0,
            "full_text_proportion": round(tier_counts["FULL_TEXT_VERIFIED"] / max(len(study_evidence), 1), 3)
        }

    @staticmethod
    def audit_missing_data_policy(data_dict: Dict[str, Any], required_fields: List[str]) -> Dict[str, Any]:
        """Enforces that unmeasured/unknown parameters use approved explicit statuses (Phase 36).
        Approved: NOT_REPORTED, UNKNOWN, NOT_APPLICABLE, UNVERIFIED.
        Prohibits plausible guessing.
        """
        APPROVED_MISSING_MARKERS = {"NOT_REPORTED", "UNKNOWN", "NOT_APPLICABLE", "UNVERIFIED"}
        missing_fields = []
        compliant_markers = []

        for f in required_fields:
            val = data_dict.get(f)
            if val is None or val == "":
                missing_fields.append(f)
            elif str(val).upper() in APPROVED_MISSING_MARKERS:
                compliant_markers.append({f: str(val).upper()})

        is_clean = len(missing_fields) == 0
        return {
            "is_missing_data_compliant": is_clean,
            "unassigned_empty_fields": missing_fields,
            "explicitly_acknowledged_missing": compliant_markers,
            "status": "COMPLIANT" if is_clean else "NON_COMPLIANT_SILENT_EMPTY_FIELDS",
            "rule": "Parameters without empirical evidence must explicitly specify NOT_REPORTED, UNKNOWN, or NOT_APPLICABLE."
        }

    @classmethod
    def generate_evidence_delta_report(
        cls,
        previous_corpus: List[Dict[str, Any]],
        current_corpus: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generates an incremental evidence delta report for living research updates (Prompt Pt 25).
        Categorizes articles into: NEW_STUDIES, UPDATED_STUDIES, CORRECTED_STUDIES, RETRACTED_STUDIES, UNCHANGED_STUDIES.
        """
        prev_map = {s.get("doi") or s.get("study_id") or s.get("title"): s for s in previous_corpus}
        curr_map = {s.get("doi") or s.get("study_id") or s.get("title"): s for s in current_corpus}

        new_studies = []
        updated_studies = []
        corrected_studies = []
        retracted_studies = []
        unchanged_studies = []

        for key, curr_s in curr_map.items():
            if key not in prev_map:
                new_studies.append(curr_s.get("study_id", key))
            else:
                prev_s = prev_map[key]
                if curr_s.get("is_retracted") and not prev_s.get("is_retracted"):
                    retracted_studies.append(curr_s.get("study_id", key))
                elif curr_s.get("is_corrected") and not prev_s.get("is_corrected"):
                    corrected_studies.append(curr_s.get("study_id", key))
                elif curr_s != prev_s:
                    updated_studies.append(curr_s.get("study_id", key))
                else:
                    unchanged_studies.append(curr_s.get("study_id", key))

        return {
            "delta_status": "DELTA_COMPUTED",
            "total_previous": len(previous_corpus),
            "total_current": len(current_corpus),
            "new_studies_count": len(new_studies),
            "new_studies": new_studies,
            "updated_studies_count": len(updated_studies),
            "updated_studies": updated_studies,
            "corrected_studies_count": len(corrected_studies),
            "corrected_studies": corrected_studies,
            "retracted_studies_count": len(retracted_studies),
            "retracted_studies": retracted_studies,
            "unchanged_studies_count": len(unchanged_studies),
            "unchanged_studies": unchanged_studies
        }

    def audit_core_evidence_recency(
        self,
        core_claims: List[Dict[str, Any]],
        references: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Audits that core primary scientific claims are supported by recent evidence within 6-year window (Part 4).
        Historical or foundational references are permitted for background/methodology, but core direct claims
        must have active recent empirical support.
        """
        ref_map = {r.get("ref_id"): r for r in references}
        claims_lacking_recent_support = []
        verified_core_claims = []

        for claim in core_claims:
            cid = claim.get("claim_id", "CLM_UNKNOWN")
            ctext = claim.get("claim_text", "")
            cited_refs = claim.get("supporting_reference_ids", [])
            is_core_claim = claim.get("is_core_claim", True)

            if not is_core_claim:
                continue

            has_recent = False
            for rid in cited_refs:
                r = ref_map.get(rid)
                if r:
                    audit_res = self.audit_temporal_tier(r)
                    if audit_res.get("recent_evidence_eligible", False) and audit_res.get("temporal_class") == "CORE_RECENT_PRIMARY":
                        has_recent = True
                        break

            if has_recent:
                verified_core_claims.append(cid)
            else:
                claims_lacking_recent_support.append({
                    "claim_id": cid,
                    "claim_text": ctext,
                    "cited_reference_ids": cited_refs,
                    "issue": "CORE_CLAIM_LACKS_RECENT_PRIMARY_SUPPORT"
                })

        all_compliant = (len(claims_lacking_recent_support) == 0)
        return {
            "audit_type": "CORE_EVIDENCE_RECENCY_AUDIT",
            "status": "COMPLIANT" if all_compliant else "NON_COMPLIANT_OUTDATED_CORE_CLAIMS",
            "is_compliant": all_compliant,
            "total_core_claims_evaluated": len(verified_core_claims) + len(claims_lacking_recent_support),
            "verified_recent_claims_count": len(verified_core_claims),
            "claims_lacking_recent_support_count": len(claims_lacking_recent_support),
            "claims_lacking_recent_support": claims_lacking_recent_support,
            "rule": f"All core direct claims must be substantiated by primary studies published within {self.max_primary_age} years (>= {self.cutoff_year})."
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
