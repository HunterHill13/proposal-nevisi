#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mesh_query_expander.py - Advanced MeSH Thesaurus & Precision Boolean Query Expansion Engine
Proposal-Nevisi Engine v11.3 (Two-Loop Literature Harvester Core)

Provides:
1. MeSH Thesaurus Mapping: Translates Persian/English disease and pharmacological concepts
   into standardized MeSH Descriptors and Qualifier subheadings.
2. Two-Tier Cascaded Search Strategy:
   - Tier 1: Precision MeSH Boolean Query with explicit field tags [MeSH Terms] OR [Title/Abstract].
   - Tier 2: Free-Text Smart Expansion Fallback if Tier 1 yields < min_results authentic papers.
3. Universal & Config-Driven: Zero domain hardcoding.
"""

import re
from typing import Dict, List, Any, Optional, Tuple

MESH_THESAURUS: Dict[str, Dict[str, Any]] = {
    # Oncology
    "colorectal": {
        "mesh": "Colorectal Neoplasms",
        "synonyms": ["colorectal cancer", "colon cancer", "rectal cancer", "colorectal carcinoma"],
        "category": "disease"
    },
    "breast": {
        "mesh": "Breast Neoplasms",
        "synonyms": ["breast cancer", "breast carcinoma", "mammary neoplasms"],
        "category": "disease"
    },
    "gastric": {
        "mesh": "Stomach Neoplasms",
        "synonyms": ["gastric cancer", "stomach cancer", "gastric carcinoma"],
        "category": "disease"
    },
    "pulmonary_neoplasms": {
        "mesh": "Lung Neoplasms",
        "synonyms": ["pulmonary neoplasms", "non-small cell pulmonary carcinoma", "NSCLC"],
        "category": "disease"
    },
    "prostate": {
        "mesh": "Prostatic Neoplasms",
        "synonyms": ["prostate cancer", "prostatic cancer", "prostate carcinoma"],
        "category": "disease"
    },
    "leukemia": {
        "mesh": "Leukemia",
        "synonyms": ["leukaemia", "acute myeloid leukemia", "AML"],
        "category": "disease"
    },
    "hepatocellular": {
        "mesh": "Carcinoma, Hepatocellular",
        "synonyms": ["liver cancer", "hepatoma", "HCC"],
        "category": "disease"
    },
    "glioblastoma": {
        "mesh": "Glioblastoma",
        "synonyms": ["GBM", "glioblastoma multiforme", "astrocytoma"],
        "category": "disease"
    },
    
    # Mechanisms & Cellular Phenomena
    "apoptosis": {
        "mesh": "Apoptosis",
        "synonyms": ["programmed cell death", "caspase-dependent death"],
        "category": "mechanism"
    },
    "autophagy": {
        "mesh": "Autophagy",
        "synonyms": ["macroautophagy", "autophagic cell death"],
        "category": "mechanism"
    },
    "ferroptosis": {
        "mesh": "Ferroptosis",
        "synonyms": ["iron-dependent cell death", "lipid peroxidation cell death"],
        "category": "mechanism"
    },
    "synergism": {
        "mesh": "Drug Synergism",
        "synonyms": ["synergy", "synergistic effect", "combination index", "Chou-Talalay"],
        "category": "pharmacology"
    },
    "resistance": {
        "mesh": "Drug Resistance, Neoplasm",
        "synonyms": ["chemoresistance", "multidrug resistance", "MDR"],
        "category": "pharmacology"
    },
    "oxidative_stress": {
        "mesh": "Oxidative Stress",
        "synonyms": ["reactive oxygen species", "ROS generation", "lipid peroxidation"],
        "category": "mechanism"
    },
    "inflammation": {
        "mesh": "Inflammation",
        "synonyms": ["inflammatory response", "pro-inflammatory cytokines"],
        "category": "mechanism"
    },
    
    # Metabolic & Chronic Conditions
    "diabetes": {
        "mesh": "Diabetes Mellitus",
        "synonyms": ["type 2 diabetes", "diabetic", "T2DM"],
        "category": "disease"
    },
    "fatty_liver": {
        "mesh": "Fatty Liver",
        "synonyms": ["NAFLD", "NASH", "steatohepatitis", "metabolic dysfunction-associated steatotic liver disease"],
        "category": "disease"
    },
    "alzheimer": {
        "mesh": "Alzheimer Disease",
        "synonyms": ["Alzheimer's", "dementia, Alzheimer type"],
        "category": "disease"
    },
    "parkinson": {
        "mesh": "Parkinson Disease",
        "synonyms": ["Parkinson's", "parkinsonism"],
        "category": "disease"
    },
    
    # Drug Delivery & Nanotechnology
    "nanoparticles": {
        "mesh": "Nanoparticles",
        "synonyms": ["nanocarriers", "nanomedicine", "nanoformulation"],
        "category": "delivery"
    },
    "liposomes": {
        "mesh": "Liposomes",
        "synonyms": ["liposomal delivery", "lipid nanoparticles"],
        "category": "delivery"
    }
}

PERSIAN_TO_CONCEPT_MAP: List[Tuple[str, str]] = [
    (r'سرطان\s+کولون|سرطان\s+روده|کولورکتال', "colorectal"),
    (r'سرطان\s+پستان|سرطان\s+سینه', "breast"),
    (r'سرطان\s+معده', "gastric"),
    (r'سرطان\s+ریه', "lung"),
    (r'سرطان\s+پروستات', "prostate"),
    (r'لوسمی|سرطان\s+خون', "leukemia"),
    (r'سرطان\s+کبد|هپاتوسلولار', "hepatocellular"),
    (r'گلیوبلاستوما|تومور\s+مغزی', "glioblastoma"),
    (r'آپوپتوز|مرگ\s+برنامه‌ریزی\s*شده', "apoptosis"),
    (r'اتوفاژی', "autophagy"),
    (r'پروپتوز|فروپتوز', "ferroptosis"),
    (r'هم‌افزایی|سینرژی|سینرژیسم', "synergism"),
    (r'مقاومت\s+دارویی|مقاومت\s+به\s+شیمی‌درمانی', "resistance"),
    (r'استرس\s+اکسیداتیو|اکسیدان', "oxidative_stress"),
    (r'التهاب|ضد\s+التهاب', "inflammation"),
    (r'دیابت', "diabetes"),
    (r'کبد\s+چرب', "fatty_liver"),
    (r'آلزایمر', "alzheimer"),
    (r'پارکینسون', "parkinson"),
    (r'نانوذرات|نانوذره', "nanoparticles"),
    (r'لیپوزوم', "liposomes")
]


class MeSHQueryExpander:
    """Intelligent MeSH thesaurus and two-tier search query planner."""

    @classmethod
    def map_concept_to_mesh(cls, concept_or_term: str) -> Optional[Dict[str, Any]]:
        """Maps any concept key, English term, or raw string to a standardized MeSH descriptor record."""
        term_clean = concept_or_term.strip().lower()
        if term_clean in MESH_THESAURUS:
            return MESH_THESAURUS[term_clean]
        
        for k, v in MESH_THESAURUS.items():
            if term_clean == v["mesh"].lower():
                return v
            if any(term_clean == syn.lower() for syn in v["synonyms"]):
                return v
        return None

    @classmethod
    def extract_mesh_entities(cls, text: str) -> List[Dict[str, Any]]:
        """Extracts all recognized biomedical MeSH entities from mixed Persian/English text."""
        matched = []
        seen_meshes = set()

        # 1. Match Persian regex patterns
        for pat, concept_key in PERSIAN_TO_CONCEPT_MAP:
            if re.search(pat, text, re.IGNORECASE):
                record = MESH_THESAURUS.get(concept_key)
                if record and record["mesh"] not in seen_meshes:
                    seen_meshes.add(record["mesh"])
                    matched.append(record)

        # 2. Match English words against Thesaurus
        words = re.findall(r'[A-Za-z][A-Za-z0-9_\-\+]{2,}', text)
        for w in words:
            rec = cls.map_concept_to_mesh(w)
            if rec and rec["mesh"] not in seen_meshes:
                seen_meshes.add(rec["mesh"])
                matched.append(rec)

        return matched

    @classmethod
    def build_tier1_precision_mesh_query(
        cls,
        text_or_topic: str,
        custom_agents: Optional[List[str]] = None
    ) -> str:
        """
        Builds Tier 1 Precision MeSH Boolean Query:
        Combines (MeSH Descriptor OR synonyms[Title/Abstract]) for each entity,
        ANDed together with pharmacological agents.
        """
        entities = cls.extract_mesh_entities(text_or_topic)
        clauses = []

        # Build MeSH clauses
        for ent in entities:
            mesh_term = ent["mesh"]
            syns = ent.get("synonyms", [])
            terms = [f'"{mesh_term}"[MeSH Terms]']
            for s in syns[:3]:
                terms.append(f'"{s}"[Title/Abstract]')
            clauses.append("(" + " OR ".join(terms) + ")")

        # Add explicit agent/compound clauses
        agents = list(custom_agents or [])
        if not agents:
            # Extract Latin/English chemical tokens from topic if not in MeSH
            en_tokens = re.findall(r'[A-Za-z][A-Za-z0-9_\-\+]{2,}', text_or_topic)
            for tok in en_tokens:
                if tok.lower() not in ["and", "the", "for", "with", "from", "against"]:
                    if not any(tok.lower() in [ent["mesh"].lower()] + [s.lower() for s in ent.get("synonyms", [])] for ent in entities):
                        agents.append(tok)

        for ag in agents[:3]:
            clauses.append(f'("{ag}"[Title/Abstract] OR "{ag}"[MeSH Terms])')

        if not clauses:
            # Fallback to general terms
            return '("Drug Synergism"[MeSH Terms] OR "Apoptosis"[MeSH Terms]) AND "Biomedical Research"[Title/Abstract]'

        return " AND ".join(clauses)

    @classmethod
    def build_tier2_fallback_query(
        cls,
        text_or_topic: str,
        custom_agents: Optional[List[str]] = None
    ) -> str:
        """Builds Tier 2 Broad Fallback Query."""
        entities = cls.extract_mesh_entities(text_or_topic)
        keywords = []

        # Prioritize disease/condition first, then mechanisms, then pharmacology
        cat_order = {"disease": 0, "pharmacology": 1, "mechanism": 2, "delivery": 3}
        sorted_entities = sorted(entities, key=lambda e: cat_order.get(e.get("category", "mechanism"), 4))

        for ent in sorted_entities:
            keywords.append(ent["mesh"].split(",")[0])  # Primary name

        for ent in sorted_entities:
            if ent.get("synonyms"):
                keywords.append(ent["synonyms"][0])

        if custom_agents:
            keywords.extend(custom_agents)
        else:
            en_tokens = re.findall(r'[A-Za-z][A-Za-z0-9_\-\+]{2,}', text_or_topic)
            for tok in en_tokens:
                if tok.lower() not in ["and", "the", "for", "with", "from", "against"]:
                    keywords.append(tok)

        unique_kws = list(dict.fromkeys(keywords))
        if len(unique_kws) >= 2:
            return " AND ".join(f'"{k}"' for k in unique_kws[:4])
        elif unique_kws:
            return f'"{unique_kws[0]}" AND (viability OR apoptosis OR cytotoxicity)'
        return "synergism AND apoptosis AND cancer"
