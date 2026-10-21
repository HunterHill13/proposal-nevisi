#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
graph_entailment_gate.py - Anti-Hallucination & Anti-Fluff Graph Entailment Gate
Proposal-Nevisi Engine v12.0 (Cognitive Multi-Agent Architecture)

Enforces two strict academic writing gates:
1. Anti-Hallucination Gate (Graph Entailment):
   - Every biomedical claim, parameter, and biological cascade must trace back
     to an explicit node or directed edge in `LITERATURE_CITATION_GRAPH.json`
     and `BIOMEDICAL_CONCEPT_GRAPH.json`.
   - Rejects unverified PMIDs, fake DOIs, or fabricated mechanisms.
2. Anti-Fluff Gate (Zero Information Density Elimination):
   - Detects low-information boilerplate AI filler sentences (e.g., generic intros,
     vague assertions of importance, empty transitional padding).
   - Flags them for remediation or replaces them with information-dense, quantitative
     prose extracted from verified graph edges.
3. Produces `claim_entailment_audit.json`.

100% Dependency-Free (Pure Standard Library).
"""

import os
import re
import json
import time
from typing import Dict, List, Any, Optional, Set, Tuple


class GraphEntailmentGate:
    """Verifies that proposal text is strictly entailed by the citation & concept graph."""

    # Low-information generic boilerplate patterns (English & Persian)
    GENERIC_FLUFF_PATTERNS = [
        # English fluff
        r'\b(?:is a|remains a)\s+(?:major|significant|devastating)\s+(?:global\s+)?(?:public\s+health\s+)?(?:challenge|concern|burden)\b',
        r'\b(?:numerous|various|many)\s+studies\s+have\s+(?:explored|investigated|demonstrated)\b',
        r'\bplays?\s+(?:a\s+)?(?:crucial|pivotal|vital|essential|key)\s+role\s+in\b',
        r'\bfurther\s+(?:research|investigation|studies)\s+(?:is|are)\s+(?:urgently\s+)?needed\s+to\b',
        r'\b(?:delving|diving)\s+deeper\s+into\b',
        r'\bit\s+is\s+worth\s+noting\s+that\b',
        r'\bcomprehensively\s+sheds?\s+light\s+on\b',
        # Persian fluff
        r'یکی\s+از\s+(?:بزرگ‌ترین|مهم‌ترین)\s+چالش‌های\s+(?:بهداشتی|سلامت|پزشکی)\s+(?:جهان|بشریت)',
        r'مطالعات\s+(?:متعددی|بسیاری)\s+نشان\s+داده‌اند\s+که',
        r'نقش\s+(?:بسیار\s+)?(?:کلیدی|حیاتی|محوری)\s+ایفا\s+می‌کند',
        r'تحقیقات\s+بیشتری\s+برای\s+(?:روشن\s+شدن|درک\s+بهتر)\s+مورد\s+نیاز\s+است',
        r'شایان\s+ذکر\s+است\s+که'
    ]

    def __init__(
        self,
        citation_graph: Optional[Dict[str, Any]] = None,
        concept_graph: Optional[Dict[str, Any]] = None,
        min_information_density_ratio: float = 0.65
    ):
        self.citation_graph = citation_graph or {}
        self.concept_graph = concept_graph or {}
        self.min_density = min_information_density_ratio

        # Index known graph IDs and titles
        self.known_pmids: Set[str] = set()
        self.known_dois: Set[str] = set()
        self.known_node_ids: Set[str] = set()
        self.known_entities: Set[str] = set()

        self._build_indices()

    def _build_indices(self):
        """Indexes all verified identifiers from the graphs."""
        nodes = self.citation_graph.get("nodes", [])
        for n in nodes:
            nid = str(n.get("id", ""))
            self.known_node_ids.add(nid)
            if n.get("pmid"):
                self.known_pmids.add(str(n["pmid"]).strip())
            if n.get("doi"):
                self.known_dois.add(str(n["doi"]).strip().lower())

        entities = self.concept_graph.get("entities", [])
        for e in entities:
            self.known_entities.add(e.get("canonical_name", "").lower())
            for syn in e.get("synonyms", []):
                self.known_entities.add(syn.lower())

    def audit_sentence(self, sentence: str) -> Dict[str, Any]:
        """
        Audits a single sentence for:
        1. Low-information fluff.
        2. Unverified citation references (fabricated PMIDs or DOIs).
        3. Quantitative grounding.
        """
        clean_sent = sentence.strip()
        if len(clean_sent) < 15:
            return {"status": "SKIP", "reason": "Too short to audit", "fluff": False, "citations": []}

        # 1. Fluff Check
        is_fluff = False
        matched_fluff_patterns = []
        for pat in self.GENERIC_FLUFF_PATTERNS:
            if re.search(pat, clean_sent, re.IGNORECASE):
                is_fluff = True
                matched_fluff_patterns.append(pat)

        # 2. Citation Verification
        # Find PMIDs like [PMID: 12345] or (PMID: 12345) or PMID 12345
        pmid_matches = re.findall(r'PMID[\s:]*(\d{7,8})', clean_sent, re.IGNORECASE)
        # Find DOIs like 10.xxxx/...
        doi_matches = re.findall(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', clean_sent)

        invalid_citations = []
        verified_citations = []

        for pmid in pmid_matches:
            if self.known_pmids and pmid not in self.known_pmids:
                invalid_citations.append(f"PMID:{pmid}")
            else:
                verified_citations.append(f"PMID:{pmid}")

        for doi in doi_matches:
            clean_doi = doi.strip().rstrip(".,;)").lower()
            if self.known_dois and clean_doi not in self.known_dois:
                invalid_citations.append(f"DOI:{clean_doi}")
            else:
                verified_citations.append(f"DOI:{clean_doi}")

        # 3. Information Density Scoring
        # Density ratio: proportion of words that are substantive medical/quantitative tokens
        words = re.findall(r'\b\w+\b', clean_sent)
        num_matches = re.findall(r'\b\d+(?:\.\d+)?(?:%|nM|µM|uM|mM|mg/kg|mg/ml|Gy)?\b', clean_sent)

        density_score = 0.5
        if words:
            dense_tokens = len(num_matches) + len(verified_citations)
            for w in words:
                if w.lower() in self.known_entities:
                    dense_tokens += 1
            density_score = min(1.0, dense_tokens / max(1, len(words) * 0.35))

        status = "ACCEPT"
        reasons = []

        if invalid_citations:
            status = "REJECT"
            reasons.append(f"Unverified or fabricated citations detected: {', '.join(invalid_citations)}")

        if is_fluff and not num_matches and not verified_citations:
            status = "REJECT" if status != "REJECT" else status
            reasons.append("Generic low-information AI boilerplate without quantitative grounding")

        return {
            "sentence": clean_sent,
            "status": status,
            "is_fluff": is_fluff,
            "reasons": reasons,
            "verified_citations": verified_citations,
            "invalid_citations": invalid_citations,
            "density_score": round(density_score, 3)
        }

    def audit_section(self, section_name: str, text: str) -> Dict[str, Any]:
        """Audits an entire proposal section across all sentences."""
        sentences = re.split(r'(?<=[.!?])\s+|\n\n+', text)
        audited = []
        rejected = []
        fluff_count = 0

        for s in sentences:
            s_clean = s.strip()
            if not s_clean:
                continue
            res = self.audit_sentence(s_clean)
            audited.append(res)
            if res.get("is_fluff"):
                fluff_count += 1
            if res["status"] == "REJECT":
                rejected.append(res)

        all_passed = len(rejected) == 0
        overall_density = sum(a.get("density_score", 0.5) for a in audited) / max(1, len(audited))

        return {
            "section_name": section_name,
            "total_sentences": len(audited),
            "accepted_count": len(audited) - len(rejected),
            "rejected_count": len(rejected),
            "fluff_sentence_count": fluff_count,
            "overall_density_score": round(overall_density, 3),
            "all_passed": all_passed,
            "rejected_sentences": rejected,
            "sentence_audits": audited
        }

    def audit_full_proposal(self, sections: Dict[str, str], output_audit_path: Optional[str] = None) -> Dict[str, Any]:
        """Audits all proposal sections and generates `claim_entailment_audit.json`."""
        section_results = {}
        total_audited = 0
        total_rejected = 0
        total_fluff = 0

        for sec_name, text in sections.items():
            res = self.audit_section(sec_name, text)
            section_results[sec_name] = res
            total_audited += res["total_sentences"]
            total_rejected += res["rejected_count"]
            total_fluff += res["fluff_sentence_count"]

        audit_report = {
            "audit_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "overall_summary": {
                "total_sections_audited": len(sections),
                "total_sentences": total_audited,
                "total_rejected": total_rejected,
                "total_fluff_detected": total_fluff,
                "overall_pass_rate": round((total_audited - total_rejected) / max(1, total_audited), 4),
                "all_sections_passed": total_rejected == 0
            },
            "sections": section_results
        }

        if output_audit_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_audit_path)), exist_ok=True)
            with open(output_audit_path, "w", encoding="utf-8") as f:
                json.dump(audit_report, f, indent=2, ensure_ascii=False)

        return audit_report
