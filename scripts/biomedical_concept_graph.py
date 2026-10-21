#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
biomedical_concept_graph.py - Bipartite Biomedical Concept Graph & Claim Extractor
Proposal-Nevisi Engine v12.0 (Cognitive Multi-Agent Architecture)

Bridges the Macro-Level Bibliographic Citation Graph with a Micro-Level Mechanistic Knowledge Graph:
1. Extracts structured biological entities:
   - Interventions / Drugs / Small Molecules
   - Targets / Genes / Receptors / Enzymes
   - Cellular Signaling Pathways
   - Diseases / Neoplasms / Clinical Conditions
   - Experimental Assay Endpoints (e.g. IC50, Apoptosis, Clonogenic Survival, CI)
2. Connects papers to biological claims via bipartite edges (Paper -> asserts -> Edge).
3. Detects multi-hop mechanistic synergies (e.g. Drug A -> Target X -> Pathway -> Disease).
4. Enforces span-level claim grounding against abstract sentences.
5. Exports to `BIOMEDICAL_CONCEPT_GRAPH.json`.

100% Dependency-Free (Pure Python Standard Library).
"""

import os
import re
import json
import time
from typing import Dict, List, Any, Optional, Set, Tuple


class BiomedicalConceptGraph:
    """Micro-level biological entity-relationship and claim knowledge graph."""

    # Canonical biological relationship types
    RELATION_TYPES = {
        "INHIBITS": "Chemical or genetic downregulation/antagonism of target",
        "ACTIVATES": "Agonism or positive induction of target/pathway",
        "PARTICIPATES_IN": "Target membership in biological cascade or signaling pathway",
        "DYSREGULATED_IN": "Pathological alteration of pathway or gene in disease",
        "SYNERGIZES_WITH": "Combination produces greater-than-additive effect (CI < 1.0)",
        "MEASURED_BY": "Quantitative readout assessed via specific analytical protocol",
        "RESISTANT_TO": "Cellular phenotype showing reduced sensitivity to intervention"
    }

    def __init__(self, topic_context: Optional[str] = None):
        self.topic_context = topic_context or "Biomedical Experimental Study"
        self.entities: Dict[str, Dict[str, Any]] = {}
        self.relationships: List[Dict[str, Any]] = []
        self.paper_claims: Dict[str, List[Dict[str, Any]]] = {}

    # =========================================================================
    # 1. ENTITY REGISTRATION & NORMALIZATION
    # =========================================================================

    def _normalize_entity_id(self, entity_type: str, raw_name: str) -> str:
        """Converts raw entity string to canonical namespaced ID."""
        clean = re.sub(r'[^a-zA-Z0-9_]', '_', raw_name.strip()).upper()
        clean = re.sub(r'_+', '_', clean).strip('_')
        return f"{entity_type.upper()}:{clean}"

    def register_entity(
        self,
        entity_type: str,
        name: str,
        synonyms: Optional[List[str]] = None,
        mesh_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Registers a named biological entity."""
        eid = self._normalize_entity_id(entity_type, name)
        if eid not in self.entities:
            self.entities[eid] = {
                "id": eid,
                "type": entity_type.upper(),
                "canonical_name": name.strip(),
                "synonyms": synonyms or [],
                "mesh_id": mesh_id,
                "metadata": metadata or {},
                "degree": 0
            }
        else:
            if synonyms:
                existing = set(self.entities[eid]["synonyms"])
                existing.update(synonyms)
                self.entities[eid]["synonyms"] = list(existing)
            if mesh_id and not self.entities[eid]["mesh_id"]:
                self.entities[eid]["mesh_id"] = mesh_id
        return eid

    # =========================================================================
    # 2. RELATIONSHIP REGISTRATION & GROUNDING
    # =========================================================================

    def add_relationship(
        self,
        source_id: str,
        relation_type: str,
        target_id: str,
        supporting_paper_id: Optional[str] = None,
        quantitative_metrics: Optional[Dict[str, Any]] = None,
        abstract_evidence_span: Optional[str] = None,
        confidence: float = 1.0
    ) -> Dict[str, Any]:
        """
        Creates a directed biological assertion grounded in a primary paper.
        Enforces that source and target entities exist in the concept graph.
        """
        rel_type = relation_type.upper()
        if rel_type not in self.RELATION_TYPES:
            rel_type = "PARTICIPATES_IN"

        if source_id not in self.entities:
            # Auto-infer entity type from ID
            etype = source_id.split(":")[0] if ":" in source_id else "CONCEPT"
            self.register_entity(etype, source_id.split(":")[-1])

        if target_id not in self.entities:
            etype = target_id.split(":")[0] if ":" in target_id else "CONCEPT"
            self.register_entity(etype, target_id.split(":")[-1])

        rel_record = {
            "source": source_id,
            "relation": rel_type,
            "target": target_id,
            "supporting_paper": supporting_paper_id,
            "metrics": quantitative_metrics or {},
            "evidence_span": abstract_evidence_span,
            "confidence": round(confidence, 4)
        }

        # Check existing
        for r in self.relationships:
            if r["source"] == source_id and r["relation"] == rel_type and r["target"] == target_id:
                if supporting_paper_id and r.get("supporting_paper") != supporting_paper_id:
                    # Multi-paper consensus
                    r["supporting_papers"] = list(set(r.get("supporting_papers", [r.get("supporting_paper")]) + [supporting_paper_id]))
                if quantitative_metrics:
                    r["metrics"].update(quantitative_metrics)
                return r

        self.relationships.append(rel_record)
        self.entities[source_id]["degree"] += 1
        self.entities[target_id]["degree"] += 1

        if supporting_paper_id:
            if supporting_paper_id not in self.paper_claims:
                self.paper_claims[supporting_paper_id] = []
            self.paper_claims[supporting_paper_id].append(rel_record)

        return rel_record

    # =========================================================================
    # 3. TEXT & ABSTRACT PARSING
    # =========================================================================

    def ingest_paper_abstract(
        self,
        paper_id: str,
        title: str,
        abstract: str,
        known_entities: Optional[Dict[str, List[str]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Extracts structured biological assertions from paper abstract text.
        Identifies quantitative tokens (IC50, concentrations, percentages, CI values)
        and binds them to extracted biological entities.
        """
        extracted_claims = []
        if not abstract:
            return extracted_claims

        full_text = f"{title}. {abstract}"
        sentences = re.split(r'(?<=[.!?])\s+', full_text)

        # 1. Match known or supplied entities
        detected_entities = []
        if known_entities:
            for etype, terms in known_entities.items():
                for term in terms:
                    if len(term) >= 3 and re.search(r'\b' + re.escape(term) + r'\b', full_text, re.IGNORECASE):
                        eid = self.register_entity(etype, term)
                        detected_entities.append((eid, term))

        # 2. Extract quantitative patterns
        ic50_pattern = re.compile(r'IC50\s*(?:of|[:=])?\s*([\d\.]+\s*(?:nM|µM|uM|mM|mg/ml))', re.IGNORECASE)
        ci_pattern = re.compile(r'(?:combination\s*index|CI)\s*(?:of|[:=])?\s*([\d\.]+)', re.IGNORECASE)
        synergy_pattern = re.compile(r'\b(synerg\w+|sensitiz\w+|potentiat\w+|overcom\w+ resistance)\b', re.IGNORECASE)
        inhibit_pattern = re.compile(r'\b(inhibit\w+|suppress\w+|downregulat\w+|block\w+)\b', re.IGNORECASE)

        for sent in sentences:
            metrics = {}
            ic50_match = ic50_pattern.search(sent)
            if ic50_match:
                metrics["ic50"] = ic50_match.group(1).strip()

            ci_match = ci_pattern.search(sent)
            if ci_match:
                try:
                    metrics["ci_value"] = float(ci_match.group(1))
                except ValueError:
                    pass

            # Detect entities co-occurring in the sentence
            sent_entities = [eid for eid, term in detected_entities if re.search(r'\b' + re.escape(term) + r'\b', sent, re.IGNORECASE)]

            if len(sent_entities) >= 2:
                # Pairwise relationship
                src = sent_entities[0]
                tgt = sent_entities[1]

                rel = "PARTICIPATES_IN"
                if synergy_pattern.search(sent):
                    rel = "SYNERGIZES_WITH"
                elif inhibit_pattern.search(sent):
                    rel = "INHIBITS"

                claim = self.add_relationship(
                    source_id=src,
                    relation_type=rel,
                    target_id=tgt,
                    supporting_paper_id=paper_id,
                    quantitative_metrics=metrics,
                    abstract_evidence_span=sent.strip()[:300],
                    confidence=0.90 if metrics else 0.75
                )
                extracted_claims.append(claim)

        return extracted_claims

    # =========================================================================
    # 4. MULTI-HOP PATHFINDING & MECHANISTIC SYNERGY
    # =========================================================================

    def find_mechanistic_paths(
        self,
        start_entity_id: str,
        end_entity_id: str,
        max_hops: int = 3
    ) -> List[List[Dict[str, Any]]]:
        """
        Traverses concept graph to find causal paths connecting an intervention to a disease.
        e.g., [Drug A] -> INHIBITS -> [Target B] -> PARTICIPATES_IN -> [Pathway C] -> DYSREGULATED_IN -> [Disease D]
        """
        paths: List[List[Dict[str, Any]]] = []

        def dfs(current_id: str, target_id: str, current_path: List[Dict[str, Any]], visited: Set[str]):
            if len(current_path) > max_hops:
                return
            if current_id == target_id and current_path:
                paths.append(list(current_path))
                return

            visited.add(current_id)
            for r in self.relationships:
                if r["source"] == current_id and r["target"] not in visited:
                    current_path.append(r)
                    dfs(r["target"], target_id, current_path, visited.copy())
                    current_path.pop()

        dfs(start_entity_id, end_entity_id, [], set())
        return paths

    def query_claim_entailment(
        self,
        source_name: str,
        relation_type: str,
        target_name: str
    ) -> Dict[str, Any]:
        """
        Verifies whether an asserted biological relationship exists as a verified path in the graph.
        Returns the supporting papers and quantitative metrics if entailed.
        """
        clean_rel = relation_type.upper().strip()
        matching_edges = []

        for r in self.relationships:
            src_match = (source_name.upper() in r["source"]) or (source_name.lower() in self.entities.get(r["source"], {}).get("canonical_name", "").lower())
            tgt_match = (target_name.upper() in r["target"]) or (target_name.lower() in self.entities.get(r["target"], {}).get("canonical_name", "").lower())
            rel_match = (clean_rel == r["relation"]) or (clean_rel in ("INHIBITS", "SUPPRESSES") and r["relation"] == "INHIBITS")

            if src_match and tgt_match and rel_match:
                matching_edges.append(r)

        if matching_edges:
            best_edge = max(matching_edges, key=lambda x: x.get("confidence", 0.0))
            return {
                "is_entailed": True,
                "confidence": best_edge.get("confidence", 1.0),
                "supporting_papers": [best_edge.get("supporting_paper")] if best_edge.get("supporting_paper") else best_edge.get("supporting_papers", []),
                "metrics": best_edge.get("metrics", {}),
                "evidence_span": best_edge.get("evidence_span")
            }

        return {
            "is_entailed": False,
            "confidence": 0.0,
            "supporting_papers": [],
            "metrics": {},
            "evidence_span": None
        }

    # =========================================================================
    # 5. SERIALIZATION & EXPORT
    # =========================================================================

    def to_dict(self) -> Dict[str, Any]:
        """Serializes concept graph into structured JSON dictionary."""
        return {
            "topic_context": self.topic_context,
            "generation_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "total_entities": len(self.entities),
            "total_relationships": len(self.relationships),
            "entities": list(self.entities.values()),
            "relationships": self.relationships,
            "paper_claims_index": self.paper_claims
        }

    def save_json(self, output_path: str) -> str:
        """Saves concept graph JSON to disk."""
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        return output_path
