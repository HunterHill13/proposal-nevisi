#!/usr/bin/env python3
"""
generic_reference_auditor.py - Topic-Agnostic Bibliographic, Temporal & Citation Auditor
Proposal-Nevisi Engine v8.2 (Universal Biomedical Architecture)

Performs field-level verification against Crossref/PubMed, audits temporal boundaries,
validates foundational justifications, and strictly detects citation padding.
"""

import re
import json
import difflib
from typing import Dict, List, Any, Optional, Tuple

try:
    from core_policies import (
        TemporalPolicyConfig, MAX_FINAL_REFERENCES, MIN_FINAL_REFERENCES,
        ContextualRelevanceConfig, FINAL_INCLUSION_REASON_CATEGORIES, PROPOSAL_SECTIONS_FOR_EVIDENCE
    )
except ImportError:
    from scripts.core_policies import (
        TemporalPolicyConfig, MAX_FINAL_REFERENCES, MIN_FINAL_REFERENCES,
        ContextualRelevanceConfig, FINAL_INCLUSION_REASON_CATEGORIES, PROPOSAL_SECTIONS_FOR_EVIDENCE
    )

class GenericReferenceAuditor:
    """Universal reference auditor operating without hard-coded biological assumptions."""

    def __init__(
        self,
        current_year: Optional[int] = None,
        max_primary_age_years: int = TemporalPolicyConfig.MAX_PRIMARY_EVIDENCE_AGE_YEARS,
        min_required_references: int = 15,
        target_model: Optional[Dict[str, Any]] = None,
        current_date: Optional[Any] = None
    ):
        import datetime
        self.current_date = current_date or datetime.date.today()
        self.current_year = current_year or self.current_date.year
        self.max_primary_age = max_primary_age_years
        self.cutoff_year = self.current_year - max_primary_age_years
        self.cutoff_date = TemporalPolicyConfig.get_cutoff_date(self.current_date)
        self.min_required_references = min_required_references
    def audit_bibliographic_fields(self, local_ref: Dict[str, Any], verified_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Compares local citation record with authoritative Crossref/PubMed data with normalized author identity, DOI consistency, and publication status (Phases 9 & 10)."""
        title_local = local_ref.get("title", "").strip().lower()
        title_verified = verified_metadata.get("title", "").strip().lower()

        sim = difflib.SequenceMatcher(None, title_local, title_verified).ratio() if (title_local and title_verified) else 0.0

        year_local = local_ref.get("year")
        year_verified = verified_metadata.get("year")
        year_match = (year_local == year_verified) if (year_local and year_verified) else False
        year_divergence = abs(int(year_local) - int(year_verified)) if (year_local and year_verified) else 0

        # Normalized author matching (last name + initial check)
        def parse_authors(auth_list: List[Any]) -> List[Tuple[str, str]]:
            res = []
            for a in auth_list:
                if not a:
                    continue
                parts = str(a).strip().lower().split()
                if parts:
                    surname = re.sub(r'[^a-z]', '', parts[-1])
                    initial = parts[0][0] if len(parts[0]) > 0 else ""
                    res.append((surname, initial))
            return res

        authors_local = parse_authors(local_ref.get("authors", []))
        authors_verified = parse_authors(verified_metadata.get("authors", []))
        
        author_surnames_local = [s for s, _ in authors_local]
        author_surnames_ver = [s for s, _ in authors_verified]
        author_match = any(s in author_surnames_ver for s in author_surnames_local) if (author_surnames_local and author_surnames_ver) else False

        is_retracted = (
            verified_metadata.get("is_retracted", False) or
            "retracted" in verified_metadata.get("status", "").lower() or
            "retraction" in title_verified.lower() or
            "retraction notice" in title_verified.lower()
        )
        is_corrected = (
            verified_metadata.get("is_corrected", False) or
            "erratum" in title_verified.lower() or
            "corrigendum" in title_verified.lower()
        )
        is_expression_of_concern = (
            verified_metadata.get("is_expression_of_concern", False) or
            "expression of concern" in title_verified.lower() or
            "editorial concern" in verified_metadata.get("status", "").lower()
        )
        is_duplicate = verified_metadata.get("is_duplicate", False)

        doi_local = str(local_ref.get("doi", "")).strip().lower()
        doi_verified = str(verified_metadata.get("doi", "")).strip().lower()

        identity_conflict = False
        if is_retracted:
            status = "RETRACTED"
        elif is_duplicate:
            status = "DUPLICATE"
        elif is_expression_of_concern:
            status = "EXPRESSION_OF_CONCERN"
        elif is_corrected:
            status = "CORRECTED"
        elif (doi_local and doi_verified and doi_local == doi_verified and sim < 0.40):
            # Same DOI claimed, but completely different title -> IDENTITY_CONFLICT
            status = "IDENTITY_CONFLICT"
            identity_conflict = True
        elif sim >= 0.85 and year_divergence > 2 and not author_match:
            # Same title, but different paper (mismatched years and different authors)
            status = "IDENTITY_CONFLICT"
            identity_conflict = True
        elif sim >= 0.85 and year_match and (author_match or not authors_local):
            status = "EXACT_VERIFIED"
        elif sim >= 0.60:
            status = "MINOR_VARIATION"
        elif sim < 0.40 and bool(title_local and title_verified):
            status = "IDENTITY_CONFLICT"
            identity_conflict = True
        else:
            status = "CONFLICT_OR_UNVERIFIED"

        eligible = (status in ["EXACT_VERIFIED", "MINOR_VARIATION", "CORRECTED", "EXPRESSION_OF_CONCERN"] and not identity_conflict and not is_retracted and not is_duplicate)

        return {
            "ref_id": local_ref.get("ref_id"),
            "verification_status": status,
            "title_similarity": round(sim, 3),
            "year_match": year_match,
            "author_overlap": author_match,
            "doi": local_ref.get("doi"),
            "is_retracted": is_retracted,
            "is_corrected": is_corrected,
            "corrected_version_available": verified_metadata.get("corrected_version_available", True) if is_corrected else None,
            "is_expression_of_concern": is_expression_of_concern,
            "uncertainty_flag": is_expression_of_concern,
            "identity_conflict": identity_conflict,
            "core_evidence_eligible": eligible
        }

    def audit_temporal_tier(self, ref: Dict[str, Any]) -> Dict[str, Any]:
        """Enforces the 6-year recency rule with calendar precision, leap-year safety, and anti-cheating foundational validation (Phases 7 & 8)."""
        import datetime

        pub_date_str = (
            ref.get("online_publication_date") or
            ref.get("epub_date") or
            ref.get("publication_date") or
            ref.get("print_publication_date") or
            ref.get("date")
        )
        year = ref.get("year")
        parsed_date = None
        date_precision = "DATE_UNCERTAIN"

        if pub_date_str:
            str_clean = str(pub_date_str).strip()
            # Try full YYYY-MM-DD
            m_full = re.match(r'^(\d{4})-(\d{2})-(\d{2})', str_clean)
            if m_full:
                try:
                    parsed_date = datetime.date(int(m_full.group(1)), int(m_full.group(2)), int(m_full.group(3)))
                    year = parsed_date.year
                    date_precision = "EXACT_DATE"
                except ValueError:
                    date_precision = "DATE_UNCERTAIN"
            else:
                # Try YYYY-MM
                m_month = re.match(r'^(\d{4})-(\d{2})', str_clean)
                if m_month:
                    try:
                        y_val = int(m_month.group(1))
                        m_val = int(m_month.group(2))
                        if 1 <= m_val <= 12:
                            year = y_val
                            date_precision = "MONTH_PRECISION"
                            parsed_date = datetime.date(y_val, m_val, 1)
                        else:
                            date_precision = "DATE_UNCERTAIN"
                    except ValueError:
                        date_precision = "DATE_UNCERTAIN"
                else:
                    # Try YYYY
                    m_year = re.match(r'^(\d{4})', str_clean)
                    if m_year:
                        year = int(m_year.group(1))
                        date_precision = "YEAR_PRECISION"
                        parsed_date = None  # Do NOT invent Jan 1
                    else:
                        date_precision = "DATE_UNCERTAIN"
        elif year:
            try:
                year = int(year)
                date_precision = "YEAR_PRECISION"
                parsed_date = None  # Do NOT invent Jan 1
            except (ValueError, TypeError):
                date_precision = "DATE_UNCERTAIN"

        if date_precision == "DATE_UNCERTAIN" or (parsed_date is None and year is None):
            return {
                "ref_id": ref.get("ref_id"),
                "year": None,
                "publication_date": pub_date_str,
                "parsed_date": None,
                "date_precision": "DATE_UNCERTAIN",
                "cutoff_date": str(self.cutoff_date),
                "age_in_days": None,
                "age_in_years": None,
                "temporal_tier": "DATE_UNCERTAIN",
                "temporal_class": "DATE_UNCERTAIN",
                "evidence_role": "UNCERTAIN_ROLE",
                "age_justification": "DATE_UNCERTAIN",
                "is_temporally_valid": False,
                "core_evidence_eligible": False,
                "recent_evidence_eligible": False,
                "foundational_exception": False,
                "foundational_category": None,
                "justification": None,
                "justification_confidence": "ZERO",
                "justification_source": None,
                "audit_note": "Publication date and year are completely unverified/uncertain."
            }

        # Determine recency based on precision
        if date_precision == "EXACT_DATE":
            is_recent = parsed_date >= self.cutoff_date
            age_days = (self.current_date - parsed_date).days
            age_years = round(age_days / 365.25, 2)
            parsed_date_str = str(parsed_date)
        elif date_precision == "MONTH_PRECISION":
            # Compare Year and Month
            is_recent = (parsed_date.year > self.cutoff_date.year) or (parsed_date.year == self.cutoff_date.year and parsed_date.month >= self.cutoff_date.month)
            age_days = (self.current_date - parsed_date).days
            age_years = round(age_days / 365.25, 2)
            parsed_date_str = f"{parsed_date.year:04d}-{parsed_date.month:02d}"
        else: # YEAR_PRECISION
            # Strictly calendar year based: does not fake exact date
            is_recent = (year >= self.cutoff_year)
            age_years = self.current_year - year
            age_days = int(age_years * 365.25)
            parsed_date_str = str(year)

        justification_dict = ref.get("foundational_justification") or {}
        evidence_role = ref.get("evidence_role", "PRIMARY_EVIDENCE")

        if is_recent:
            tier = "RECENT_PRIMARY_EVIDENCE"
            temporal_class = "CORE_RECENT_PRIMARY" if evidence_role == "PRIMARY_EVIDENCE" else "CORE_RECENT_SECONDARY"
            age_justification = "RECENT_DIRECT_EVIDENCE"
            justified = True
            core_eligible = True
            recent_eligible = True
            foundational_exception = False
            cat = None
            conf = "HIGH"
            source = "RECENCY_TIMELINESS_WINDOW"
            note = f"Published in {parsed_date_str} ({age_years} years old; within {self.max_primary_age}-year cutoff window)."
            provenance = None
        else:
            tier = "FOUNDATIONAL/HISTORICAL_EVIDENCE"
            has_justification = bool(justification_dict.get("is_justified"))
            cat = justification_dict.get("category")
            rationale = str(justification_dict.get("rationale", "")).strip()
            
            # Anti-cheating check: missing modern alternative assessment must be UNKNOWN, not defaulted to True
            no_modern_raw = justification_dict.get("no_modern_alternative_exists")
            if no_modern_raw is None:
                modern_alt_assessment = "UNKNOWN"
            else:
                modern_alt_assessment = "TRUE" if bool(no_modern_raw) else "FALSE"

            intended_section = justification_dict.get("section_scope", "BACKGROUND_OR_METHODOLOGY")
            citation_count = justification_dict.get("citation_count")
            citation_count_source = justification_dict.get("citation_count_source") or "UNVERIFIED"

            is_valid_category = cat in TemporalPolicyConfig.APPROVED_FOUNDATIONAL_CATEGORIES
            is_substantive_rationale = len(rationale) >= 15

            # Verified citation count rule: landmark exceptions require >= 100 citations or canonical seminal methodology
            has_verified_citations = (
                (isinstance(citation_count, (int, float)) and citation_count >= 100)
                or (citation_count is None and cat in ["FOUNDATIONAL_MATHEMATICAL_MODEL", "STANDARDIZED_ASSAY_METHOD", "METHODOLOGICAL_LANDMARK", "CLASSICAL_STATISTICAL_METHOD"])
                or justification_dict.get("seminal_methodology", False) is True
            )

            is_fake_foundational = (
                not is_valid_category or
                not is_substantive_rationale or
                not has_verified_citations or
                evidence_role == "PRIMARY_DIRECT_EFFICACY" or
                "routine" in rationale.lower() or
                "standard observational" in rationale.lower()
            )

            provenance = {
                "category": cat,
                "rationale": rationale,
                "source": justification_dict.get("justification_source", "PEER_REVIEWED_CONSENSUS"),
                "verification_status": "APPROVED" if (has_justification and not is_fake_foundational) else "REJECTED_UNJUSTIFIED",
                "citation_count": citation_count,
                "citation_count_source": citation_count_source,
                "modern_alternative_assessment": modern_alt_assessment,
                "reviewer_confidence": "VERIFIED_HIGH" if (has_justification and not is_fake_foundational) else "ZERO"
            }

            if has_justification and not is_fake_foundational:
                age_justification = cat
                justified = True
                recent_eligible = False
                foundational_exception = True
                conf = "VERIFIED_FOUNDATIONAL_EXCEPTION"
                source = justification_dict.get("justification_source", "PEER_REVIEWED_CONSENSUS")
                core_eligible = (evidence_role != "PRIMARY_EVIDENCE" and intended_section != "CORE_PRIMARY_RESULTS")

                if cat in ["FOUNDATIONAL_MATHEMATICAL_MODEL", "STANDARDIZED_ASSAY_METHOD", "METHODOLOGICAL_LANDMARK"]:
                    temporal_class = "FOUNDATIONAL_METHODOLOGY"
                elif cat in ["ORIGINAL_DIAGNOSTIC_CRITERIA", "LANDMARK_HISTORICAL_BENCHMARK"]:
                    temporal_class = "LANDMARK_GUIDELINE"
                elif cat in ["CLASSICAL_STATISTICAL_METHOD"]:
                    temporal_class = "CLASSICAL_METHOD"
                else:
                    temporal_class = "HISTORICAL_BACKGROUND"
                note = f"Foundational exception approved: {age_justification} ({rationale})."
            else:
                temporal_class = "OUT_OF_WINDOW_NON_FOUNDATIONAL"
                age_justification = "OUTDATED_DIRECT_EVIDENCE"
                justified = False
                core_eligible = False
                recent_eligible = False
                foundational_exception = False
                conf = "REJECTED_UNJUSTIFIED"
                source = "TEMPORAL_RECENCY_BREACH"
                note = f"Published in {parsed_date_str} (outside {self.max_primary_age}-year window) without verified citation/seminal justification. Prohibited from core evidence."

        return {
            "ref_id": ref.get("ref_id"),
            "year": year,
            "publication_date": pub_date_str,
            "parsed_date": parsed_date_str,
            "date_precision": date_precision,
            "cutoff_date": str(self.cutoff_date),
            "age_in_days": age_days,
            "age_in_years": age_years,
            "temporal_tier": tier,
            "temporal_class": temporal_class,
            "evidence_role": evidence_role,
            "age_justification": age_justification,
            "is_temporally_valid": justified,
            "core_evidence_eligible": core_eligible,
            "recent_evidence_eligible": recent_eligible,
            "foundational_exception": foundational_exception,
            "foundational_category": cat,
            "justification": justification_dict if foundational_exception else None,
            "justification_confidence": conf,
            "justification_source": source,
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

    @classmethod
    def _extract_model_dict(cls, problem_model: Any) -> Dict[str, Any]:
        """Extracts problem model dictionary from dict, schema, or object."""
        if problem_model is None:
            return {}
        if hasattr(problem_model, "to_dict") and callable(problem_model.to_dict):
            return problem_model.to_dict()
        if isinstance(problem_model, dict):
            if "research_problem_model" in problem_model:
                return problem_model["research_problem_model"]
            return problem_model
        res = {}
        for attr in ["domain", "framework", "target_condition", "population_or_model", "interventions_or_exposures", "primary_outcomes", "hypothesized_mechanisms", "controlled_vocabulary"]:
            if hasattr(problem_model, attr):
                val = getattr(problem_model, attr)
                if hasattr(val, "to_dict"):
                    val = val.to_dict()
                res[attr] = val
        return res

    @classmethod
    def audit_contextual_relevance(cls, record: Dict[str, Any], problem_model: Any) -> Dict[str, Any]:
        """Evaluates contextual relevance across 8 dimensions (direct, model, intervention, outcome,
        mechanistic, methodological, transferability, overall).
        Strictly rejects keyword-matching papers situated in disconnected or incompatible biological contexts
        (e.g., veterinary livestock reproduction, agricultural crop agronomy) when the problem model is human biomedical.
        """
        p_dict = cls._extract_model_dict(problem_model)
        domain = str(p_dict.get("domain", "")).lower()
        
        cond_dict = p_dict.get("target_condition", {})
        cond_names = []
        if isinstance(cond_dict, dict):
            if cond_dict.get("name_en"): cond_names.append(str(cond_dict["name_en"]).lower())
            if cond_dict.get("name_fa"): cond_names.append(str(cond_dict["name_fa"]).lower())
            cond_names.extend([str(s).lower() for s in cond_dict.get("synonyms", []) if s])
        elif isinstance(cond_dict, str):
            cond_names.append(cond_dict.lower())
            
        pop_dict = p_dict.get("population_or_model", {})
        primary_sys = str(pop_dict.get("primary_system", "")).lower() if isinstance(pop_dict, dict) else str(pop_dict).lower()
        
        interventions = p_dict.get("interventions_or_exposures", [])
        agent_names = []
        for ag in interventions:
            if isinstance(ag, dict):
                if ag.get("name"): agent_names.append(str(ag["name"]).lower())
                agent_names.extend([str(s).lower() for s in ag.get("synonyms", []) if s])
            elif isinstance(ag, str):
                agent_names.append(ag.lower())
                
        outcomes = []
        for o in p_dict.get("primary_outcomes", []):
            if isinstance(o, dict) and o.get("name"):
                outcomes.append(str(o["name"]).lower())
            elif isinstance(o, str):
                outcomes.append(o.lower())
                
        mechanisms = []
        for m in p_dict.get("hypothesized_mechanisms", []):
            if isinstance(m, dict):
                if m.get("pathway_name"): mechanisms.append(str(m["pathway_name"]).lower())
                mechanisms.extend([str(t).lower() for t in m.get("target_molecules", []) if t])
            elif isinstance(m, str):
                mechanisms.append(m.lower())

        # Record attributes
        title = str(record.get("title", "")).lower()
        abstract = str(record.get("abstract", "")).lower()
        model_sys = str(record.get("model_system", record.get("organism_cell_line", ""))).lower()
        t_cond = str(record.get("target_condition", "")).lower()
        endpoints = str(record.get("endpoints_evaluated", "")).lower()
        findings = str(record.get("primary_findings", "")).lower()
        design = str(record.get("study_design", "")).lower()
        combined_text = f"{title} {abstract} {model_sys} {t_cond} {endpoints} {findings} {design}"

        # 1. Biological Incompatibility Gate
        is_target_veterinary_repro = any(k in f"{domain} {primary_sys} {' '.join(cond_names)}" for k in ["veterinary", "livestock", "semen", "sperm", "ram", "buck", "bull", "boar", "stallion", "breeding", "agronomy", "crop"])
        
        DISCONNECTED_INDICATORS = [
            "semen", "spermatozoa", "cryopreservation of semen", "cryopreserved semen",
            "cryopreserved bucks", "bucks semen", "buck semen", "ram semen", "bull semen",
            "boar semen", "stallion semen", "livestock breeding", "artificial insemination",
            "crop yield", "plant fertilizer", "soil salinity", "timber preservation",
            "aquaculture feeding", "broiler chicken feed", "poultry weight gain",
            "silkworm breeding", "cotton fiber yield", "grain harvest preservation"
        ]
        
        found_incompatible = None
        if not is_target_veterinary_repro:
            for ind in DISCONNECTED_INDICATORS:
                if ind in combined_text:
                    found_incompatible = ind
                    break
        
        # Check foundational methodology exception
        just = record.get("foundational_justification") or {}
        cat = just.get("category")
        is_foundational_method = bool(just.get("is_justified")) and cat in [
            "FOUNDATIONAL_MATHEMATICAL_MODEL", "STANDARDIZED_ASSAY_METHOD",
            "METHODOLOGICAL_LANDMARK", "CLASSICAL_STATISTICAL_METHOD"
        ]
        
        if found_incompatible and not is_foundational_method:
            return {
                "ref_id": record.get("ref_id", record.get("doi", "UNKNOWN")),
                "is_contextually_relevant": False,
                "rejection_reason": "REJECT_LOW_CONTEXTUAL_RELEVANCE",
                "rejection_category": "INCOMPATIBLE_BIOLOGICAL_SYSTEM",
                "relevance_tier": "IRRELEVANT",
                "matched_incompatible_indicator": found_incompatible,
                "rationale": f"Evaluated biological context ('{found_incompatible}') is disparate from target research problem model ({domain}). Pure chemical keyword match without contextual relevance is prohibited.",
                "scores": {
                    "biological_topic_alignment": 0.0,
                    "condition_phenotype_alignment": 0.0,
                    "primary_agent_alignment": 0.5,
                    "comparator_second_agent_alignment": 0.0,
                    "experimental_model_population_alignment": 0.0,
                    "outcome_alignment": 0.0,
                    "mechanistic_pathway_alignment": 0.0,
                    "study_design_alignment": 0.0,
                    "research_question_fit": 0.0,
                    "proposal_section_utility": 0.0,
                    "direct_relevance": 0.0,
                    "model_relevance": 0.0,
                    "intervention_relevance": 0.5,
                    "outcome_relevance": 0.0,
                    "mechanistic_relevance": 0.0,
                    "methodological_relevance": 0.0,
                    "transferability": 0.0,
                    "overall_relevance": 0.07
                }
            }

        # 2. Evaluate 10 Universal Relevance Dimensions
        # Dimension 1: biological_topic_alignment
        bio_align = 1.0 if not found_incompatible else 0.0
        if any(k in combined_text for k in [domain, "biomedical", "medicine", "clinical", "therapeutic", "cellular", "molecular", "pharmacolog", "in_vitro", "in vitro", "in_vivo", "in vivo"] + cond_names):
            bio_align = 1.0
        elif is_foundational_method:
            bio_align = 1.0
        else:
            bio_align = 0.5
            
        # Dimension 2: condition_phenotype_alignment
        has_cond = any(c in combined_text for c in cond_names if len(c) > 3) if cond_names else True
        cond_align = 1.0 if has_cond else (0.5 if any(k in combined_text for k in ["disease", "syndrome", "pathology", "tumor", "carcinoma", "infection", "disorder", "dysfunction", "cancer", "neoplasm", "oncolog"]) else 0.1)
        
        # Dimension 3: primary_agent_alignment
        has_agent = any(a in combined_text for a in agent_names) if agent_names else True
        prim_agent = 1.0 if has_agent else 0.2
        
        # Dimension 4: comparator_second_agent_alignment
        has_comp = bool(record.get("comparator")) or ("control" in combined_text) or (len(agent_names) > 1 and any(agent_names[1] in combined_text for _ in [1]))
        comp_agent = 1.0 if has_comp else 0.3
        
        # Dimension 5: experimental_model_population_alignment
        has_model = False
        if is_foundational_method:
            model_align = 1.0
        else:
            # Clean primary_sys terms: exclude generic ubiquitous words ('cell', 'line', 'type', 'human', 'model')
            if primary_sys:
                sys_terms = [t.strip().lower() for t in primary_sys.split() if len(t.strip()) > 3 and t.strip().lower() not in ["cell", "line", "type", "with", "from", "human", "model", "primary"]]
                for t in sys_terms:
                    # check exact term or trimmed root (e.g., cardiomyocytes -> cardiomyocyte, systems -> system)
                    root = t[:-1] if t.endswith("s") else t
                    if re.search(r'\b' + re.escape(root), combined_text):
                        has_model = True
                        break
            if not has_model and any(re.search(r'\b' + re.escape(k) + r'\b', combined_text) for k in [
                "human cell line", "cancer cell line", "cell culture model", "cell culture system", 
                "in vitro cancer model", "cellular oncology models", "cellular oncology model", 
                "murine xenograft", "clinical trial patients", "in_vitro", "in vitro"
            ]):
                has_model = True
            model_align = 1.0 if has_model else 0.2
        
        # Dimension 6: outcome_alignment
        has_outcome = any(o in combined_text for o in outcomes if len(o) > 3) if outcomes else False
        outcome_align = 1.0 if has_outcome else (0.5 if any(k in combined_text for k in ["viability", "apoptosis", "survival", "toxicity", "efficacy", "inhibition", "expression"]) else 0.1)
        
        # Dimension 7: mechanistic_pathway_alignment
        has_mech = any(m in combined_text for m in mechanisms if len(m) > 3) if mechanisms else False
        mech_align = 1.0 if has_mech else (0.5 if any(k in combined_text for k in ["pathway", "signaling", "phosphorylation", "receptor", "caspase", "cleavage", "activation"]) else 0.1)
        
        # Dimension 8: study_design_alignment
        has_method = is_foundational_method or any(k in combined_text for k in ["assay", "method", "protocol", "synergy", "isobologram", "ic50", "combination index", "median effect", "rct", "experimental", "in vitro", "in vivo"])
        design_align = 1.0 if has_method else 0.4
        
        # Dimension 9: research_question_fit
        if is_foundational_method:
            q_fit = 1.0
        elif has_agent and has_cond and has_model:
            q_fit = 1.0
        elif has_agent and (has_cond or (has_model and (has_outcome or has_mech))):
            q_fit = 0.7
        elif has_agent or has_cond:
            q_fit = 0.3
        else:
            q_fit = 0.1
            
        # Dimension 10: proposal_section_utility
        if is_foundational_method:
            sec_utility = 1.0
        elif has_agent and has_cond:
            sec_utility = 1.0
        elif has_agent and (has_outcome or has_mech or has_model):
            sec_utility = 0.6
        elif has_cond:
            sec_utility = 0.5
        else:
            sec_utility = 0.1
        
        # Weighted Overall Relevance Calculation
        overall_rel = round(
            (bio_align * 0.15) +
            (cond_align * 0.20) +
            (prim_agent * 0.15) +
            (comp_agent * 0.05) +
            (model_align * 0.15) +
            (outcome_align * 0.10) +
            (mech_align * 0.05) +
            (design_align * 0.05) +
            (q_fit * 0.05) +
            (sec_utility * 0.05),
            2
        )
        
        # Critical Non-Negotiable Gate: If a paper lacks both the target condition and the biological model/outcomes,
        # pure chemical keyword presence alone CANNOT yield an acceptable score.
        if not is_foundational_method and not has_cond and not has_model:
            overall_rel = min(overall_rel, 0.30)
        
        # Backwards compatible legacy aliases
        direct_rel = 1.0 if (has_agent and has_cond) else (0.6 if (has_agent or has_cond) else 0.2)
        model_rel = model_align
        intervention_rel = prim_agent
        outcome_rel = outcome_align
        mechanistic_rel = mech_align
        method_rel = design_align
        transferability = 1.0 if (direct_rel >= 0.6 or is_foundational_method) else 0.4
        
        # 6-Tier Relevance Classification
        if is_foundational_method or (design_align >= 0.75 and method_rel >= 0.75 and not has_cond and not has_agent):
            relevance_tier = "METHOD_RELEVANT"
            is_relevant = True
        elif overall_rel >= 0.80:
            relevance_tier = "DIRECTLY_RELEVANT"
            is_relevant = True
        elif overall_rel >= 0.65:
            relevance_tier = "HIGHLY_RELEVANT"
            is_relevant = True
        elif overall_rel >= 0.50:
            relevance_tier = "INDIRECTLY_RELEVANT"
            is_relevant = True
        elif overall_rel >= 0.35:
            relevance_tier = "BACKGROUND_ONLY"
            is_relevant = True
        else:
            relevance_tier = "IRRELEVANT"
            is_relevant = False
            
        rejection_reason = None if is_relevant else "REJECT_LOW_CONTEXTUAL_RELEVANCE"
        rejection_category = None if is_relevant else "LOW_OVERALL_ALIGNMENT"
        rationale = (
            f"Contextual alignment verified across target intervention, condition, and biological model (Tier: {relevance_tier}, Score: {overall_rel})."
            if is_relevant else
            f"Overall contextual relevance score ({overall_rel}) below acceptance threshold; classified as IRRELEVANT."
        )
        
        return {
            "ref_id": record.get("ref_id", record.get("doi", "UNKNOWN")),
            "is_contextually_relevant": is_relevant,
            "relevance_tier": relevance_tier,
            "rejection_reason": rejection_reason,
            "rejection_category": rejection_category,
            "matched_incompatible_indicator": None,
            "rationale": rationale,
            "scores": {
                "biological_topic_alignment": bio_align,
                "condition_phenotype_alignment": cond_align,
                "primary_agent_alignment": prim_agent,
                "comparator_second_agent_alignment": comp_agent,
                "experimental_model_population_alignment": model_align,
                "outcome_alignment": outcome_align,
                "mechanistic_pathway_alignment": mech_align,
                "study_design_alignment": design_align,
                "research_question_fit": q_fit,
                "proposal_section_utility": sec_utility,
                "direct_relevance": direct_rel,
                "model_relevance": model_rel,
                "intervention_relevance": intervention_rel,
                "outcome_relevance": outcome_rel,
                "mechanistic_relevance": mechanistic_rel,
                "methodological_relevance": method_rel,
                "transferability": transferability,
                "overall_relevance": overall_rel
            }
        }

    @classmethod
    def score_reference(cls, record: Dict[str, Any], problem_model: Any, target_claims: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Calculates multi-factor score across 14 scientific and methodological criteria (0-10 each)."""
        relevance_audit = cls.audit_contextual_relevance(record, problem_model)
        rel_scores = relevance_audit.get("scores", {})
        
        # 1. direct_relevance (0-10)
        s_direct = int(rel_scores.get("direct_relevance", 0.5) * 10)
        # 2. model_relevance (0-10)
        s_model = int(rel_scores.get("model_relevance", 0.5) * 10)
        # 3. intervention_relevance (0-10)
        s_interv = int(rel_scores.get("intervention_relevance", 0.5) * 10)
        # 4. comparator_relevance (0-10)
        has_comp = bool(record.get("comparator")) or ("control" in str(record.get("abstract", "")).lower())
        s_comp = 10 if has_comp else 6
        # 5. outcome_relevance (0-10)
        s_outcome = int(rel_scores.get("outcome_relevance", 0.5) * 10)
        # 6. mechanistic_relevance (0-10)
        s_mech = int(rel_scores.get("mechanistic_relevance", 0.5) * 10)
        # 7. methodological_quality (0-10)
        rob_dict = record.get("risk_of_bias", {})
        overall_rob = rob_dict.get("overall_rob", "MODERATE_RISK")
        if overall_rob == "LOW_RISK":
            s_qual = 10
        elif overall_rob == "MODERATE_RISK":
            s_qual = 7
        else:
            s_qual = 4
        if record.get("quantitative_parameters"):
            s_qual = min(10, s_qual + 1)
        # 8. recency (0-10)
        year = record.get("year")
        current_year = TemporalPolicyConfig.CURRENT_OPERATING_YEAR
        just = record.get("foundational_justification") or {}
        is_foundational = bool(just.get("is_justified"))
        if year:
            try:
                age = current_year - int(year)
                if age <= 3:
                    s_recency = 10
                elif age <= 6:
                    s_recency = 8
                elif is_foundational:
                    s_recency = 6
                else:
                    s_recency = 0
            except (ValueError, TypeError):
                s_recency = 2
        else:
            s_recency = 2
        # 9. directness_of_evidence (0-10)
        design = str(record.get("study_design", "")).upper()
        if any(k in design for k in ["RCT", "EXPERIMENTAL", "IN_VITRO", "IN_VIVO", "CLINICAL"]):
            s_directness = 10
        elif any(k in design for k in ["COHORT", "CASE_CONTROL"]):
            s_directness = 8
        elif any(k in design for k in ["SYSTEMATIC_REVIEW", "META_ANALYSIS"]):
            s_directness = 7
        else:
            s_directness = 4
        # 10. uniqueness_non_redundancy (0-10)
        s_unique = 9 if not record.get("is_duplicate") else 2
        # 11. necessity_for_specific_claim (0-10)
        claims_supp = record.get("claims_supported", [])
        s_necessity = 10 if claims_supp else 6
        # 12. sentence_support_fidelity (0-10)
        entailment = record.get("entailment_level", "DIRECTLY_SUPPORTED")
        if entailment == "DIRECTLY_SUPPORTED":
            s_fidelity = 10
        elif entailment == "PARTIALLY_SUPPORTED":
            s_fidelity = 7
        elif entailment == "INFERRED":
            s_fidelity = 4
        else:
            s_fidelity = 0
        # 13. scientific_authority (0-10)
        s_auth = 8
        if record.get("doi") and (record.get("pmid") or record.get("openalex_id")):
            s_auth = 10
        # 14. reliable_metadata (0-10)
        if record.get("is_retracted"):
            s_meta = 0
        elif record.get("is_expression_of_concern"):
            s_meta = 3
        else:
            s_meta = 10

        factors = {
            "direct_relevance": s_direct,
            "model_relevance": s_model,
            "intervention_relevance": s_interv,
            "comparator_relevance": s_comp,
            "outcome_relevance": s_outcome,
            "mechanistic_relevance": s_mech,
            "methodological_quality": s_qual,
            "recency": s_recency,
            "directness_of_evidence": s_directness,
            "uniqueness_non_redundancy": s_unique,
            "necessity_for_specific_claim": s_necessity,
            "sentence_support_fidelity": s_fidelity,
            "scientific_authority": s_auth,
            "reliable_metadata": s_meta
        }
        total_score = round(sum(factors.values()) * (100.0 / 140.0), 1)
        
        return {
            "ref_id": record.get("ref_id", record.get("doi", "UNKNOWN")),
            "composite_score": total_score,
            "factor_scores": factors,
            "is_contextually_relevant": relevance_audit.get("is_contextually_relevant", True),
            "relevance_audit": relevance_audit
        }

    @classmethod
    def select_optimal_proposal_references(
        cls,
        candidate_records: List[Dict[str, Any]],
        problem_model: Any,
        max_references: int = MAX_FINAL_REFERENCES,
        min_references: int = MIN_FINAL_REFERENCES,
        total_retrieved_in_corpus: Optional[int] = None
    ) -> Dict[str, Any]:
        """Filters, audits, ranks, and selects the optimal balanced reference portfolio
        under a strict hard ceiling of maximum 25 references.
        Separates deep search corpus from final proposal references and tracks a 5-stage screening funnel.
        """
        auditor = cls()
        excluded = []
        scored_candidates = []

        for r in candidate_records:
            ref_id = r.get("ref_id", r.get("doi", r.get("title", "UNKNOWN")))
            
            # 1. Retraction / Conflict check
            if r.get("is_retracted"):
                excluded.append({"ref_id": ref_id, "reason": "REJECT_RETRACTED", "details": "Article is retracted."})
                continue
            if r.get("is_duplicate"):
                excluded.append({"ref_id": ref_id, "reason": "REJECT_DUPLICATE", "details": "Duplicate record cluster."})
                continue

            # 2. Contextual Relevance Gate (Rejects off-topic biological contexts)
            rel_audit = cls.audit_contextual_relevance(r, problem_model)
            if not rel_audit.get("is_contextually_relevant"):
                excluded.append({
                    "ref_id": ref_id,
                    "reason": rel_audit.get("rejection_reason", "REJECT_LOW_CONTEXTUAL_RELEVANCE"),
                    "category": rel_audit.get("rejection_category", "LOW_OVERALL_ALIGNMENT"),
                    "details": rel_audit.get("rationale")
                })
                continue

            # 3. Temporal Policy Gate
            temp_audit = auditor.audit_temporal_tier(r)
            if not temp_audit.get("is_temporally_valid"):
                excluded.append({
                    "ref_id": ref_id,
                    "reason": "REJECT_TEMPORAL_BREACH",
                    "details": temp_audit.get("audit_note", "Exceeds 6-year window without valid foundational exception.")
                })
                continue

            # 4. Multi-Factor Scoring
            score_data = cls.score_reference(r, problem_model)
            scored_candidates.append({
                "record": r,
                "score": score_data["composite_score"],
                "score_details": score_data
            })

        # Calculate 5-Stage Screening Funnel metrics
        total_retrieved = total_retrieved_in_corpus if total_retrieved_in_corpus is not None else len(candidate_records)
        retracted_or_dup_count = len([e for e in excluded if e["reason"] in ["REJECT_RETRACTED", "REJECT_DUPLICATE"]])
        total_topic_screened = max(0, total_retrieved - retracted_or_dup_count)
        relevance_rejected_count = len([e for e in excluded if "RELEVANCE" in e["reason"] or e.get("category") == "INCOMPATIBLE_BIOLOGICAL_SYSTEM"])
        total_study_relevant = max(0, total_topic_screened - relevance_rejected_count)
        total_eligible = len(scored_candidates)

        # Sort by score descending
        scored_candidates.sort(key=lambda x: x["score"], reverse=True)

        # 5. Classify by Scientific Axes
        axis_core = []      # Target: 8-10
        axis_mech = []      # Target: 5-8
        axis_model = []     # Target: 3-5
        axis_method = []    # Target: 2-3
        axis_safety = []    # Target: 2-3

        for sc in scored_candidates:
            rec = sc["record"]
            just = rec.get("foundational_justification") or {}
            findings = str(rec.get("primary_findings", rec.get("title", ""))).lower()
            endpoints = str(rec.get("endpoints_evaluated", "")).lower()
            role = str(rec.get("evidence_role", "")).upper()
            design = str(rec.get("study_design", "")).upper()

            if just.get("category") in ["FOUNDATIONAL_MATHEMATICAL_MODEL", "STANDARDIZED_ASSAY_METHOD", "METHODOLOGICAL_LANDMARK", "CLASSICAL_STATISTICAL_METHOD"] or "METHOD" in design:
                axis_method.append(sc)
            elif any(k in findings for k in ["toxicity", "safe", "null", "no effect", "adverse", "limit", "resistance"]) or any(k in endpoints for k in ["toxicity", "safety", "hemolysis"]):
                axis_safety.append(sc)
            elif any(k in findings for k in ["pathway", "signaling", "caspase", "apoptosis", "mechanism", "cleavage", "phosphorylation", "bax", "bcl-2", "survivin"]):
                axis_mech.append(sc)
            elif "model" in role.lower() or "characterization" in role.lower() or "epidemiol" in role.lower() or any(k in findings for k in ["cell line", "expression", "overexpression", "baseline"]):
                axis_model.append(sc)
            else:
                axis_core.append(sc)

        # 6. Balanced Selection up to max_references (max 25)
        selected_sc = []
        selected_ids = set()

        def add_from_axis(axis_list, target_count):
            added = 0
            for item in axis_list:
                rid = item["record"].get("ref_id", item["record"].get("doi"))
                if rid not in selected_ids and len(selected_sc) < max_references:
                    selected_sc.append(item)
                    selected_ids.add(rid)
                    added += 1
                    if added >= target_count:
                        break

        # Allocate balanced quotas
        add_from_axis(axis_core, 9)
        add_from_axis(axis_mech, 6)
        add_from_axis(axis_model, 4)
        add_from_axis(axis_method, 3)
        add_from_axis(axis_safety, 3)

        # Fill remaining slots up to max_references with remaining highest scored candidates
        for sc in scored_candidates:
            if len(selected_sc) >= max_references:
                break
            rid = sc["record"].get("ref_id", sc["record"].get("doi"))
            if rid not in selected_ids:
                selected_sc.append(sc)
                selected_ids.add(rid)

        # Build final selected records re-indexed 1..N with mandatory inclusion justifications
        final_selected_records = []
        for idx, sc in enumerate(selected_sc, 1):
            rec_orig = sc["record"]
            # Determine explicit inclusion reason and supported proposal section
            if sc in axis_method:
                default_inc = "METHODOLOGICAL_BENCHMARK"
                default_sec = ["SECTION_3_LITERATURE_REVIEW", "SECTION_13_METHODOLOGY"]
                default_why = "Provides canonical assay protocol and validated mathematical/experimental formulation essential for proposal execution."
            elif sc in axis_safety:
                default_inc = "SAFETY_SELECTIVITY_BOUNDARY"
                default_sec = ["SECTION_2_PROBLEM_STATEMENT", "SECTION_3_LITERATURE_REVIEW", "SECTION_4_NECESSITY"]
                default_why = "Establishes non-toxic biological boundaries, selectivity index, and vehicle tolerability limits."
            elif sc in axis_mech:
                default_inc = "MECHANISTIC_RATIONALE"
                default_sec = ["SECTION_2_PROBLEM_STATEMENT", "SECTION_3_LITERATURE_REVIEW", "SECTION_9_HYPOTHESES_QUESTIONS"]
                default_why = "Provides molecular evidence for signaling pathways, apoptosis mediators, and intracellular target modulation."
            elif sc in axis_model:
                default_inc = "DIRECT_DISEASE_MODEL_EVIDENCE"
                default_sec = ["SECTION_2_PROBLEM_STATEMENT", "SECTION_3_LITERATURE_REVIEW", "SECTION_11_VARIABLE_TABLE"]
                default_why = "Characterizes baseline disease phenotype, target tissue characteristics, and baseline experimental system behavior."
            else:
                default_inc = "INTERVENTION_EFFICACY_EVIDENCE"
                default_sec = ["SECTION_2_PROBLEM_STATEMENT", "SECTION_3_LITERATURE_REVIEW", "SECTION_4_NECESSITY", "SECTION_6_SPECIFIC_OBJECTIVES"]
                default_why = "Provides direct empirical evidence for single or combination intervention efficacy and therapeutic response."

            r_copy = dict(rec_orig)
            r_copy["citation_number"] = idx
            r_copy["selection_score"] = sc["score"]
            r_copy["final_inclusion_reason"] = r_copy.get("final_inclusion_reason") or default_inc
            r_copy["proposal_section_supported"] = r_copy.get("proposal_section_supported") or default_sec
            r_copy["why_this_paper_is_needed"] = r_copy.get("why_this_paper_is_needed") or default_why
            final_selected_records.append(r_copy)

        return {
            "selection_status": "OPTIMAL_SELECTION_COMPLETE",
            "screening_funnel": {
                "stage_1_retrieved_broad_corpus": total_retrieved,
                "stage_2_topic_screened": total_topic_screened,
                "stage_3_study_relevant": total_study_relevant,
                "stage_4_claim_entailed_eligible": total_eligible,
                "stage_5_final_proposal_selected": len(final_selected_records)
            },
            "total_candidates_evaluated": len(candidate_records),
            "total_selected": len(final_selected_records),
            "max_reference_ceiling": max_references,
            "min_reference_floor": min_references,
            "meets_quotas": min_references <= len(final_selected_records) <= max_references,
            "selected_references": final_selected_records,
            "excluded_candidates_count": len(excluded),
            "excluded_candidates": excluded,
            "axis_distribution": {
                "core_direct": len([s for s in selected_sc if s in axis_core]),
                "mechanistic": len([s for s in selected_sc if s in axis_mech]),
                "model_pathology": len([s for s in selected_sc if s in axis_model]),
                "methodological": len([s for s in selected_sc if s in axis_method]),
                "safety_null": len([s for s in selected_sc if s in axis_safety])
            }
        }

    @classmethod
    def audit_final_reference_portfolio(
        cls,
        references: List[Dict[str, Any]],
        max_references: int = MAX_FINAL_REFERENCES,
        min_references: int = MIN_FINAL_REFERENCES
    ) -> Dict[str, Any]:
        """Audits the final reference portfolio to enforce:
        1. Hard ceiling of <= 25 references.
        2. Floor of >= 15 references.
        3. Mandatory presence of final_inclusion_reason, proposal_section_supported, and why_this_paper_is_needed.
        4. Zero retracted, duplicate, or identity-conflicted papers.
        5. Sequential citation numbering without gaps.
        """
        violations = []
        count = len(references)

        if count > max_references:
            violations.append(f"EXCEEDS_MAX_REFERENCE_CEILING_25: Reference count ({count}) exceeds maximum ceiling ({max_references}).")
        elif count < min_references:
            violations.append(f"BELOW_MIN_REFERENCE_FLOOR_15: Reference count ({count}) is below minimum floor ({min_references}).")

        seen_nums = []
        for idx, ref in enumerate(references, 1):
            ref_id = ref.get("ref_id", ref.get("doi", f"REF_{idx}"))
            
            # Check retracted / duplicate
            if ref.get("is_retracted"):
                violations.append(f"RETRACTED_ARTICLE_IN_PORTFOLIO: Reference {ref_id} is retracted.")
            if ref.get("is_duplicate"):
                violations.append(f"DUPLICATE_ARTICLE_IN_PORTFOLIO: Reference {ref_id} is a duplicate.")

            # Check mandatory inclusion justifications
            inc_reason = ref.get("final_inclusion_reason")
            if not inc_reason or inc_reason not in FINAL_INCLUSION_REASON_CATEGORIES:
                violations.append(f"INVALID_INCLUSION_REASON: Reference {ref_id} missing valid final_inclusion_reason.")

            sec_supp = ref.get("proposal_section_supported")
            if not sec_supp or not isinstance(sec_supp, list) or len(sec_supp) == 0:
                violations.append(f"MISSING_SUPPORTED_SECTIONS: Reference {ref_id} missing proposal_section_supported.")

            why_needed = ref.get("why_this_paper_is_needed")
            if not why_needed or len(str(why_needed).strip()) < 15:
                violations.append(f"MISSING_WHY_NEEDED_JUSTIFICATION: Reference {ref_id} missing substantive why_this_paper_is_needed.")

            c_num = ref.get("citation_number")
            if c_num is not None:
                seen_nums.append(c_num)

        # Check numbering
        if seen_nums and seen_nums != list(range(1, count + 1)):
            violations.append(f"NON_SEQUENTIAL_CITATION_NUMBERING: Expected 1..{count}, found {seen_nums[:5]}...")

        passed = len(violations) == 0
        return {
            "portfolio_status": "PASS" if passed else "FAIL",
            "PORTFOLIO_AUDIT": "PASS" if passed else "FAIL",
            "total_references": count,
            "max_reference_ceiling": max_references,
            "min_reference_floor": min_references,
            "violations_count": len(violations),
            "violations": violations
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
