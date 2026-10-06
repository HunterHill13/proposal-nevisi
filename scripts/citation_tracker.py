#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
citation_tracker.py - Universal Citation Integrity & Vancouver Sequence Tracker
Proposal-Nevisi Engine v9.0 (Layer 3: Citation Integrity)

Eliminates citation orphans (claims without references, references without claims),
enforces Vancouver style appearance-order citation indexing, and validates that
every scientific assertion in the proposal narrative is strictly bound to empirical proof.

100% General-Purpose: Zero hardcoded topics.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

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
    """Tracks scientific claims, binds citations, and computes Vancouver order."""

    def __init__(self):
        # Maps citation_id -> reference_dict
        self._registered_references: Dict[str, Dict[str, Any]] = {}
        # List of (claim_text, citation_id)
        self._claims: List[Dict[str, str]] = []
        # Ordered unique citation_ids by appearance
        self._appearance_order: List[str] = []

    def register_reference(self, citation_id: str, reference_data: Dict[str, Any]) -> None:
        """Registers a bibliographic reference under a unique identifier."""
        if not citation_id:
            raise ValueError("citation_id cannot be empty or None")
        ref_copy = dict(reference_data) if reference_data else {}
        ref_copy["citation_id"] = str(citation_id)
        self._registered_references[str(citation_id)] = ref_copy

    def register_claim(self, claim_text: str, citation_id: Optional[str]) -> None:
        """Registers a scientific claim and binds it to a citation identifier."""
        cid_str = str(citation_id).strip() if citation_id else ""
        self._claims.append({
            "claim_text": claim_text,
            "citation_id": cid_str
        })
        if cid_str and cid_str not in self._appearance_order:
            self._appearance_order.append(cid_str)

    def get_orphaned_claims(self) -> List[str]:
        """Returns all scientific claims that lack a citation or cite an unregistered reference."""
        orphans = []
        for c in self._claims:
            cid = c["citation_id"]
            if not cid or cid not in self._registered_references:
                orphans.append(c["claim_text"])
        return orphans

    def get_unused_references(self) -> List[str]:
        """Returns citation identifiers of registered references that were never cited."""
        cited_cids = {c["citation_id"] for c in self._claims if c["citation_id"]}
        unused = [cid for cid in self._registered_references if cid not in cited_cids]
        return unused

    def get_ordered_references(self) -> List[Dict[str, Any]]:
        """
        Returns registered references ordered strictly by appearance in the text (Vancouver style).
        Assigns sequential citation_number (1, 2, 3...) to each.
        Uncited references are appended at the end with a flagged status.
        """
        ordered = []
        assigned_num = 1
        seen_cids = set()

        # 1. References that were cited, in order of appearance
        for cid in self._appearance_order:
            if cid in self._registered_references and cid not in seen_cids:
                ref = dict(self._registered_references[cid])
                ref["citation_number"] = assigned_num
                ref["is_cited"] = True
                ordered.append(ref)
                seen_cids.add(cid)
                assigned_num += 1

        # 2. Registered references that were never cited
        for cid, ref_data in self._registered_references.items():
            if cid not in seen_cids:
                ref = dict(ref_data)
                ref["citation_number"] = assigned_num
                ref["is_cited"] = False
                ordered.append(ref)
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
        """Validates that there are zero orphaned claims and zero unused references."""
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
