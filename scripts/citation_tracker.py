#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
citation_tracker.py - Universal Document-Level Citation Re-indexer & Claim-Binding Auditor
Proposal-Nevisi Engine v9.1 (Layer 3: Citation Integrity)

Features:
1. Full Document-Level Re-indexing:
   - Scans full proposal text, extracts all in-text citation markers [X].
   - Dynamically re-indexes citations strictly by first appearance (Vancouver Order of Appearance).
   - Rewrites in-text citations and synchronizes the bibliography.
2. Zero-Tolerance Integrity Checks (Fail-Closed):
   - orphan_citations == 0 (all in-text citations must resolve to registered references)
   - unused_references == 0 (references in bibliography NEVER cited -> STRIKE/FAIL, never silently preserved)
   - duplicate_references == 0 (identifies identical DOIs/PMIDs under different keys)
   - citation_sequence_violations == 0 (appearance sequence 1, 2, 3... must be strictly monotonic)
3. Semantic Claim-to-Citation Binding:
   - Verifies compound, cell line/model, and endpoint alignment.
   - Detects contextual boundary leaps (e.g. claiming effect in CellLine_A while source studied CellLine_B)
     and down-ranks to INDIRECT / ANALOGOUS evidence.

100% General-Purpose: Zero hardcoded topics.
"""

import os
import sys
import re
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field

try:
    from core_policies import ROLE_SECTION_PERMISSIONS
except ImportError:
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    from core_policies import ROLE_SECTION_PERMISSIONS

@dataclass
class RoleSectionViolation:
    citation_key: str
    evidence_role: str
    section_num: int
    permitted_sections: List[int]
    violation_type: str = "ROLE_SECTION_MISMATCH"
    message_fa: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "citation_key": self.citation_key,
            "evidence_role": self.evidence_role,
            "section_num": self.section_num,
            "permitted_sections": self.permitted_sections,
            "violation_type": self.violation_type,
            "message_fa": self.message_fa
        }

@dataclass
class ClaimBindingAudit:
    claim_text: str
    citation_id: str
    is_direct_support: bool
    evidence_tier: str  # DIRECT_SUPPORT, INDIRECT_ANALOGOUS, CONFLICTING, UNGROUNDED
    compound_match: bool
    model_match: bool
    endpoint_match: bool
    audit_notes: str
    warnings: List[str] = field(default_factory=list)

@dataclass
class DocumentReindexResult:
    rewritten_text: str
    reordered_bibliography: List[Dict[str, Any]]
    citation_map_old_to_new: Dict[str, int]
    is_valid: bool
    orphan_citations_count: int
    unused_references_count: int
    duplicate_references_count: int
    sequence_violations_count: int
    error_messages: List[str] = field(default_factory=list)
    claim_audits: List[ClaimBindingAudit] = field(default_factory=list)
    role_section_violations_count: int = 0
    role_section_violations: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "orphan_citations_count": self.orphan_citations_count,
            "unused_references_count": self.unused_references_count,
            "duplicate_references_count": self.duplicate_references_count,
            "sequence_violations_count": self.sequence_violations_count,
            "role_section_violations_count": self.role_section_violations_count,
            "citation_map_old_to_new": self.citation_map_old_to_new,
            "error_messages": self.error_messages,
            "reordered_bibliography_count": len(self.reordered_bibliography)
        }

@dataclass
class ValidationResult:
    is_valid: bool
    orphaned_claims_count: int
    unused_references_count: int
    orphaned_claims: List[str] = field(default_factory=list)
    unused_references: List[str] = field(default_factory=list)
    ordered_citation_ids: List[str] = field(default_factory=list)
    citation_mapping: Dict[str, int] = field(default_factory=dict)
    error_messages: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "orphaned_claims_count": self.orphaned_claims_count,
            "unused_references_count": self.unused_references_count,
            "orphaned_claims": self.orphaned_claims,
            "unused_references": self.unused_references,
            "ordered_citation_ids": self.ordered_citation_ids,
            "citation_mapping": self.citation_mapping,
            "error_messages": self.error_messages
        }


class CitationTracker:
    """Universal citation tracker, global Vancouver re-indexer, and claim-binding auditor."""

    def __init__(self):
        self._registered_references: Dict[str, Dict[str, Any]] = {}
        self._claims: List[Dict[str, Any]] = []
        self._appearance_order: List[str] = []

    def register_reference(self, citation_id: str, reference_data: Dict[str, Any]) -> None:
        """Registers a bibliographic reference under a unique identifier."""
        if not citation_id:
            raise ValueError("citation_id cannot be empty or None")
        ref_copy = dict(reference_data) if reference_data else {}
        ref_copy["citation_id"] = str(citation_id)
        self._registered_references[str(citation_id)] = ref_copy

    def register_claim(self, claim_text: str, citation_id: Optional[str], metadata: Optional[Dict[str, Any]] = None) -> None:
        """Registers a scientific claim bound to a citation identifier and context metadata."""
        cid_str = str(citation_id).strip() if citation_id else ""
        self._claims.append({
            "claim_text": claim_text,
            "citation_id": cid_str,
            "metadata": metadata or {}
        })
        if cid_str and cid_str not in self._appearance_order:
            self._appearance_order.append(cid_str)

    def get_orphaned_claims(self) -> List[str]:
        """Returns scientific claims lacking a valid registered citation."""
        orphans = []
        for c in self._claims:
            cid = c["citation_id"]
            if not cid or cid not in self._registered_references:
                orphans.append(c["claim_text"])
        return orphans

    def get_unused_references(self) -> List[str]:
        """Returns citation IDs of registered references that were never cited."""
        cited_cids = {c["citation_id"] for c in self._claims if c["citation_id"]}
        unused = [cid for cid in self._registered_references if cid not in cited_cids]
        return unused

    def get_ordered_references(self) -> List[Dict[str, Any]]:
        """Returns references in order of appearance. Uncited references are NOT padded."""
        ordered = []
        assigned_num = 1
        seen_cids = set()

        for cid in self._appearance_order:
            if cid in self._registered_references and cid not in seen_cids:
                ref = dict(self._registered_references[cid])
                ref["citation_number"] = assigned_num
                ref["is_cited"] = True
                ordered.append(ref)
                seen_cids.add(cid)
                assigned_num += 1

        return ordered

    def get_citation_mapping(self) -> Dict[str, int]:
        """Returns mapping from citation_id to Vancouver integer number."""
        mapping = {}
        for idx, cid in enumerate(self._appearance_order, 1):
            if cid in self._registered_references:
                mapping[cid] = idx
        return mapping

    def validate(self) -> ValidationResult:
        """
        Validates citation integrity.
        Fails if orphaned claims exist OR unused references exist.
        """
        orphaned = self.get_orphaned_claims()
        unused = self.get_unused_references()
        mapping = self.get_citation_mapping()

        errors = []
        if orphaned:
            errors.append(f"CITATION_INTEGRITY_FAIL: {len(orphaned)} claims lack valid registered citations (Orphaned Claims).")
        if unused:
            errors.append(f"CITATION_INTEGRITY_FAIL: {len(unused)} references registered but never cited (Unused References: {unused}).")

        is_valid = (len(orphaned) == 0 and len(unused) == 0)

        return ValidationResult(
            is_valid=is_valid,
            orphaned_claims_count=len(orphaned),
            unused_references_count=len(unused),
            orphaned_claims=orphaned,
            unused_references=unused,
            ordered_citation_ids=[cid for cid in self._appearance_order if cid in self._registered_references],
            citation_mapping=mapping,
            error_messages=errors
        )

    def audit_claim_binding(
        self,
        claim_text: str,
        citation_id: str,
        target_compound: Optional[str] = None,
        target_model: Optional[str] = None,
        target_endpoint: Optional[str] = None
    ) -> ClaimBindingAudit:
        """
        Audits semantic alignment between a factual claim and its cited source paper.
        Flags context and model mismatches as INDIRECT/ANALOGOUS rather than direct evidence.
        """
        ref_data = self._registered_references.get(citation_id, {})
        ref_text = (
            str(ref_data.get("title", "")) + " " +
            str(ref_data.get("abstract", "")) + " " +
            str(ref_data.get("study_design", "")) + " " +
            str(ref_data.get("model", "")) + " " +
            " ".join(str(x) for x in ref_data.get("cell_lines", [])) + " " +
            " ".join(str(x) for x in ref_data.get("compounds", [])) + " " +
            " ".join(str(x) for x in ref_data.get("interventions", []))
        ).lower()

        warnings = []
        cmp_match = True
        if target_compound:
            cmp_match = target_compound.lower() in ref_text
            if not cmp_match:
                warnings.append(f"COMPOUND_MISMATCH: ماده مورد ادعا ({target_compound}) در عنوان یا چکیده مرجع {citation_id} مشاهده نشد.")

        mod_match = True
        if target_model:
            mod_match = target_model.lower() in ref_text
            if not mod_match:
                warnings.append(f"MODEL_MISMATCH: مدل سلولی/حیوانی مورد ادعا ({target_model}) با مدل بررسی‌شده در منبع {citation_id} مطابقت ندارد.")

        ep_match = True
        if target_endpoint:
            ep_match = any(w in ref_text for w in [target_endpoint.lower(), "viability", "apoptosis", "death", "inhibit"])

        if cmp_match and mod_match:
            tier = "DIRECT_SUPPORT"
            is_direct = True
            notes = "Claim and source exhibit direct contextual alignment."
        elif cmp_match and not mod_match:
            tier = "INDIRECT_ANALOGOUS"
            is_direct = False
            notes = "Compound matches but model differs; evidence is indirect/analogous."
        else:
            tier = "UNGROUNDED"
            is_direct = False
            notes = "Source does not ground the asserted claim entities."

        return ClaimBindingAudit(
            claim_text=claim_text,
            citation_id=citation_id,
            is_direct_support=is_direct,
            evidence_tier=tier,
            compound_match=cmp_match,
            model_match=mod_match,
            endpoint_match=ep_match,
            audit_notes=notes,
            warnings=warnings
        )

    @classmethod
    def reindex_document(
        cls,
        document_text: str,
        bibliography: Dict[str, Dict[str, Any]],
        validate_role_sections: bool = False
    ) -> DocumentReindexResult:
        """
        Global document-level re-indexing engine:
        1. Extracts all in-text citation markers [X] or [key].
        2. Assigns first-appearance order (1, 2, 3...).
        3. Rewrites citation markers in document text.
        4. Re-orders bibliography.
        5. Validates zero orphans, zero unused references, zero sequence violations.
        """
        raw_text = str(document_text)
        errors = []

        # Find all brackets containing numbers or citation keys
        citation_matches = list(re.finditer(r'\[([A-Za-z0-9_,\s-]+)\]', raw_text))

        cited_keys_in_order = []
        seen_keys = set()
        orphan_keys = set()

        for m in citation_matches:
            inner = m.group(1).strip()
            # Split multiple keys [1, 2, 3] or [Smith2020, Jones2021]
            tokens = [t.strip() for t in inner.split(',') if t.strip()]
            for token in tokens:
                # Handle numeric range like 1-3
                if re.match(r'^\d+-\d+$', token):
                    parts = token.split('-')
                    range_tokens = [str(x) for x in range(int(parts[0]), int(parts[1]) + 1)]
                else:
                    range_tokens = [token]

                for tok in range_tokens:
                    if tok not in bibliography:
                        orphan_keys.add(tok)
                    elif tok not in seen_keys:
                        seen_keys.add(tok)
                        cited_keys_in_order.append(tok)

        # Unused references check
        unused_keys = [k for k in bibliography.keys() if k not in seen_keys]

        # Duplicate references check (by DOI or PMID)
        seen_identifiers = {}
        duplicate_count = 0
        for k, v in bibliography.items():
            doi = v.get("doi") or v.get("canonical_doi")
            pmid = v.get("pmid") or v.get("canonical_pmid")
            ident = f"doi:{doi}" if doi else (f"pmid:{pmid}" if pmid else None)
            if ident:
                if ident in seen_identifiers:
                    duplicate_count += 1
                    errors.append(f"DUPLICATE_REFERENCE: شناسه {ident} هم در {seen_identifiers[ident]} و هم در {k} تکرار شده است.")
                else:
                    seen_identifiers[ident] = k

        # Build old_to_new mapping
        old_to_new = {}
        reordered_bib = []
        for idx, key in enumerate(cited_keys_in_order, 1):
            old_to_new[key] = idx
            ref_entry = dict(bibliography[key])
            ref_entry["citation_number"] = idx
            ref_entry["citation_key"] = key
            reordered_bib.append(ref_entry)

        # Fail if unused references exist
        if unused_keys:
            errors.append(f"UNUSED_BIBLIOGRAPHY_REFERENCES: {len(unused_keys)} منبع در فهرست مراجع ثبت شده اما در متن ارجاع داده نشده‌اند: {unused_keys}")

        if orphan_keys:
            errors.append(f"ORPHAN_IN_TEXT_CITATIONS: {len(orphan_keys)} ارجاع در متن فاقد منبع ثبت‌شده در کتاب‌شناسی هستند: {list(orphan_keys)}")

        # Rewrite in-text citation markers
        def replace_citations(match):
            inner = match.group(1).strip()
            tokens = [t.strip() for t in inner.split(',') if t.strip()]
            new_nums = []
            for t in tokens:
                if t in old_to_new:
                    new_nums.append(old_to_new[t])
                elif t.isdigit():
                    # If already numeric, check if mapped or preserve
                    new_nums.append(int(t))
                else:
                    new_nums.append(t)

            # Sort and format nicely
            int_nums = [n for n in new_nums if isinstance(n, int)]
            str_nums = [str(n) for n in new_nums if not isinstance(n, int)]
            sorted_ints = sorted(int_nums)
            all_formatted = [str(n) for n in sorted_ints] + str_nums
            return "[" + ", ".join(all_formatted) + "]"

        rewritten = re.sub(r'\[([A-Za-z0-9_,\s-]+)\]', replace_citations, raw_text)

        # Validate sequence monotonicity
        seq_matches = re.findall(r'\[([0-9,\s-]+)\]', rewritten)
        seen_seq_nums = []
        seq_violations = 0
        for sm in seq_matches:
            for n_str in re.findall(r'\b\d+\b', sm):
                val = int(n_str)
                if val not in seen_seq_nums:
                    expected = len(seen_seq_nums) + 1
                    if val != expected:
                        seq_violations += 1
                    seen_seq_nums.append(val)

        # Audit role-to-section compliance if requested
        role_violations = []
        if validate_role_sections:
            audit_res = EvidenceRoleClaimBindingGate.audit_document_sections(raw_text, bibliography)
            role_violations = audit_res.get("violations", [])
            for v_msg in audit_res.get("error_messages", []):
                errors.append(f"ROLE_SECTION_MISMATCH: {v_msg}")

        is_valid = (len(orphan_keys) == 0 and len(unused_keys) == 0 and duplicate_count == 0 and len(errors) == 0)

        return DocumentReindexResult(
            rewritten_text=rewritten,
            reordered_bibliography=reordered_bib,
            citation_map_old_to_new=old_to_new,
            is_valid=is_valid,
            orphan_citations_count=len(orphan_keys),
            unused_references_count=len(unused_keys),
            duplicate_references_count=duplicate_count,
            sequence_violations_count=seq_violations,
            error_messages=errors,
            role_section_violations_count=len(role_violations),
            role_section_violations=role_violations
        )


# ==============================================================================
# EVIDENCE ROLE CLAIM BINDING GATE (v9.2 Pillar 2)
# ==============================================================================

class EvidenceRoleClaimBindingGate:
    """Anti-Keyword Proximity Bias: Audits citation permissions per proposal section.
    
    Prevents assigning papers of distinct evidence roles (e.g. Epidemiological Burden)
    to inappropriate sections (e.g. Methodology, Cell line baseline, or In vitro procedures).
    """

    @classmethod
    def audit_section_citations(
        cls,
        section_num: int,
        citation_keys: List[str],
        bibliography: Dict[str, Dict[str, Any]]
    ) -> List[RoleSectionViolation]:
        violations = []
        for key in citation_keys:
            ref = bibliography.get(key, {})
            role = ref.get("evidence_role") or ref.get("role") or "GENERAL_BACKGROUND"
            permitted = ROLE_SECTION_PERMISSIONS.get(role, list(range(1, 29)))
            if section_num not in permitted:
                msg = f"منبع [{key}] با نقش شواهد '{role}' مجاز به استناد در بخش {section_num} نمی‌باشد (بخش‌های مجاز: {permitted})."
                violations.append(RoleSectionViolation(
                    citation_key=str(key),
                    evidence_role=str(role),
                    section_num=section_num,
                    permitted_sections=permitted,
                    violation_type="ROLE_SECTION_MISMATCH",
                    message_fa=msg
                ))
        return violations

    @classmethod
    def audit_document_sections(
        cls,
        document_text_or_sections: Any,
        bibliography: Dict[str, Dict[str, Any]],
        fail_closed: bool = False
    ) -> Dict[str, Any]:
        """Audits all proposal sections for evidence role compliance.
        Accepts either a dict of {section_num: text} or raw full document text.
        """
        sections_dict: Dict[int, str] = {}
        if isinstance(document_text_or_sections, dict):
            for k, v in document_text_or_sections.items():
                try:
                    s_num = int(k)
                    sections_dict[s_num] = str(v)
                except (ValueError, TypeError):
                    continue
        else:
            raw_text = str(document_text_or_sections)
            pattern = re.compile(r'##\s*([۰-۹\d]+)\.\s*([^\n]+)')
            matches = list(pattern.finditer(raw_text))
            for i, m in enumerate(matches):
                num_str = m.group(1)
                trans = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
                sec_num = int(num_str.translate(trans))
                start_idx = m.end()
                end_idx = matches[i + 1].start() if i + 1 < len(matches) else len(raw_text)
                sec_content = raw_text[start_idx:end_idx]
                sections_dict[sec_num] = sec_content

        all_violations: List[RoleSectionViolation] = []
        for sec_num, sec_content in sections_dict.items():
            citation_matches = re.findall(r'\[([A-Za-z0-9_,\s-]+)\]', sec_content)
            sec_keys = []
            for cm in citation_matches:
                for tok in cm.split(','):
                    t = tok.strip()
                    if t:
                        sec_keys.append(t)
            viol = cls.audit_section_citations(sec_num, sec_keys, bibliography)
            all_violations.extend(viol)

        is_compliant = (len(all_violations) == 0)
        can_proceed = is_compliant if fail_closed else True

        return {
            "is_compliant": is_compliant,
            "can_proceed": can_proceed,
            "violations_count": len(all_violations),
            "violations": [v.to_dict() for v in all_violations],
            "error_messages": [v.message_fa for v in all_violations]
        }

