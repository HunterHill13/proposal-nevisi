#!/usr/bin/env python3
"""
generic_reference_auditor.py - Topic-Agnostic Bibliographic, Temporal & Citation Auditor
Proposal-Nevisi Engine v8.1 (Universal Biomedical Architecture)

Performs field-level verification against Crossref/PubMed, audits temporal boundaries,
validates foundational justifications, and strictly detects citation padding.
"""

import re
import json
import difflib
from typing import Dict, List, Any, Optional, Tuple

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
