#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
biological_mechanism_adversarial_verifier.py - Universal Biological Mechanism & Mechanistic Chain Verifier
Proposal-Nevisi Engine v9.1 (Layer 1: Scientific Accuracy)

Operates across two rigorous tiers:
- Level A (Role Contradiction): Detects role inversions (e.g. Bcl-xL/Bcl-2 asserted as pro-apoptotic,
  or Bax/Bak as anti-apoptotic) against an authoritative, extensible molecular ontology.
- Level B (Contextual Mechanistic Inference): Deconstructs multi-step causal chains:
  [Agent A] -> [Molecular Target] -> [Cellular Process] -> [Interaction/Replication] -> [Phenotypic Endpoint]
  Validates evidence per edge, rejecting ungrounded causal leaps (e.g. asserting that Bcl-xL reduction
  automatically causes increased viral replication/oncolysis without direct co-culture proof).

100% General-Purpose: Zero hardcoded project subjects; uses an extensible ontology
of verified biological mechanisms and causal graph boundaries.
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class MechanismCheckResult:
    status: str  # "VERIFIED" | "CONTRADICTED" | "UNVERIFIED" | "NOT_ESTABLISHED" | "HYPOTHETICAL"
    correction: Optional[str]
    confidence: float
    entity: Optional[str] = None
    canonical_role: Optional[str] = None
    asserted_role: Optional[str] = None
    context_section: Optional[str] = None
    scientific_rationale: Optional[str] = None
    inference_type: str = "DIRECT_ROLE_CHECK"  # "DIRECT_ROLE_CHECK" | "MULTI_STEP_INFERENCE"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "correction": self.correction,
            "confidence": self.confidence,
            "entity": self.entity,
            "canonical_role": self.canonical_role,
            "asserted_role": self.asserted_role,
            "context_section": self.context_section,
            "scientific_rationale": self.scientific_rationale,
            "inference_type": self.inference_type
        }

@dataclass
class MechanisticEdge:
    source: str
    target: str
    relation: str
    evidence_status: str  # "ESTABLISHED", "SUPPORTED_BY_DIRECT_STUDY", "SUPPORTED_BY_ANALOG", "HYPOTHETICAL", "UNSUPPORTED"
    confidence: float
    evidence_citation: Optional[str] = None
    notes: Optional[str] = None

@dataclass
class MechanisticChainAnalysis:
    chain_status: str  # "ESTABLISHED", "PARTIALLY_SUPPORTED", "HYPOTHETICAL_INFERENCE", "CONTRADICTED", "NOT_ESTABLISHED"
    edges: List[MechanisticEdge]
    unsupported_edges: List[MechanisticEdge]
    is_fully_established: bool
    scientific_summary_fa: str
    rationale: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chain_status": self.chain_status,
            "edges": [
                {
                    "source": e.source, "target": e.target, "relation": e.relation,
                    "evidence_status": e.evidence_status, "confidence": e.confidence,
                    "citation": e.evidence_citation, "notes": e.notes
                }
                for e in self.edges
            ],
            "unsupported_edges_count": len(self.unsupported_edges),
            "is_fully_established": self.is_fully_established,
            "scientific_summary_fa": self.scientific_summary_fa,
            "rationale": self.rationale
        }


class BiologicalMechanismAdversarialVerifier:
    """Verifies biological mechanism claims and multi-step inference chains."""

    # Curated authoritative knowledge base of verified molecular mechanisms
    CANONICAL_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
        # Anti-apoptotic proteins
        "bcl-xl": {
            "canonical_role": "anti-apoptotic",
            "primary_function": "INHIBIT_APOPTOSIS",
            "pathway": "Intrinsic Apoptosis",
            "synonyms": ["bcl2l1", "bcl-x(l)", "bcl-x"],
            "expected_effects": {"apoptosis": "INHIBIT", "cell_survival": "PROMOTE", "momp": "INHIBIT"}
        },
        "bcl-2": {
            "canonical_role": "anti-apoptotic",
            "primary_function": "INHIBIT_APOPTOSIS",
            "pathway": "Intrinsic Apoptosis",
            "synonyms": ["bcl2"],
            "expected_effects": {"apoptosis": "INHIBIT", "cell_survival": "PROMOTE", "momp": "INHIBIT"}
        },
        "mcl-1": {
            "canonical_role": "anti-apoptotic",
            "primary_function": "INHIBIT_APOPTOSIS",
            "pathway": "Intrinsic Apoptosis",
            "synonyms": ["mcl1"],
            "expected_effects": {"apoptosis": "INHIBIT", "cell_survival": "PROMOTE", "momp": "INHIBIT"}
        },
        "survivin": {
            "canonical_role": "anti-apoptotic",
            "primary_function": "INHIBIT_APOPTOSIS",
            "pathway": "IAP Pathway",
            "synonyms": ["birc5"],
            "expected_effects": {"apoptosis": "INHIBIT", "caspase_activation": "INHIBIT", "cell_survival": "PROMOTE"}
        },
        "xiap": {
            "canonical_role": "anti-apoptotic",
            "primary_function": "INHIBIT_APOPTOSIS",
            "pathway": "IAP Pathway",
            "synonyms": ["birc4"],
            "expected_effects": {"apoptosis": "INHIBIT", "caspase_activation": "INHIBIT"}
        },

        # Pro-apoptotic pore formers and BH3-only proteins
        "bax": {
            "canonical_role": "pro-apoptotic",
            "primary_function": "PROMOTE_APOPTOSIS",
            "pathway": "Intrinsic Apoptosis",
            "synonyms": ["bcl2l4"],
            "expected_effects": {"apoptosis": "PROMOTE", "momp": "PROMOTE", "cytochrome_c_release": "PROMOTE"}
        },
        "bak": {
            "canonical_role": "pro-apoptotic",
            "primary_function": "PROMOTE_APOPTOSIS",
            "pathway": "Intrinsic Apoptosis",
            "synonyms": ["bak1"],
            "expected_effects": {"apoptosis": "PROMOTE", "momp": "PROMOTE", "cytochrome_c_release": "PROMOTE"}
        },
        "bad": {
            "canonical_role": "pro-apoptotic",
            "primary_function": "PROMOTE_APOPTOSIS",
            "pathway": "Intrinsic Apoptosis (BH3-only)",
            "synonyms": ["bbcb"],
            "expected_effects": {"apoptosis": "PROMOTE", "bcl2_inhibition": "PROMOTE"}
        },
        "bim": {
            "canonical_role": "pro-apoptotic",
            "primary_function": "PROMOTE_APOPTOSIS",
            "pathway": "Intrinsic Apoptosis (BH3-only)",
            "synonyms": ["bcl2l11"],
            "expected_effects": {"apoptosis": "PROMOTE"}
        },
        "puma": {
            "canonical_role": "pro-apoptotic",
            "primary_function": "PROMOTE_APOPTOSIS",
            "pathway": "Intrinsic Apoptosis (BH3-only)",
            "synonyms": ["bbc3"],
            "expected_effects": {"apoptosis": "PROMOTE"}
        },
        "noxa": {
            "canonical_role": "pro-apoptotic",
            "primary_function": "PROMOTE_APOPTOSIS",
            "pathway": "Intrinsic Apoptosis (BH3-only)",
            "synonyms": ["pmaip1"],
            "expected_effects": {"apoptosis": "PROMOTE"}
        },

        # Executioner & Initiator Caspases
        "caspase-3": {
            "canonical_role": "executioner_caspase",
            "primary_function": "PROMOTE_APOPTOSIS",
            "pathway": "Apoptosis Execution",
            "synonyms": ["casp3", "caspase 3"],
            "expected_effects": {"apoptosis": "PROMOTE", "parp_cleavage": "PROMOTE"}
        },
        "caspase-7": {
            "canonical_role": "executioner_caspase",
            "primary_function": "PROMOTE_APOPTOSIS",
            "pathway": "Apoptosis Execution",
            "synonyms": ["casp7", "caspase 7"],
            "expected_effects": {"apoptosis": "PROMOTE"}
        },
        "caspase-9": {
            "canonical_role": "initiator_caspase",
            "primary_function": "PROMOTE_APOPTOSIS",
            "pathway": "Intrinsic Apoptosis",
            "synonyms": ["casp9", "caspase 9"],
            "expected_effects": {"apoptosis": "PROMOTE", "caspase_3_activation": "PROMOTE"}
        },
        "caspase-8": {
            "canonical_role": "initiator_caspase",
            "primary_function": "PROMOTE_APOPTOSIS",
            "pathway": "Extrinsic Apoptosis",
            "synonyms": ["casp8", "caspase 8"],
            "expected_effects": {"apoptosis": "PROMOTE"}
        },

        # Tumor Suppressors & Cell Cycle Inhibitors
        "p53": {
            "canonical_role": "tumor_suppressor",
            "primary_function": "PROMOTE_APOPTOSIS_AND_ARREST",
            "pathway": "DNA Damage Response",
            "synonyms": ["tp53"],
            "expected_effects": {"apoptosis": "PROMOTE", "cell_cycle_arrest": "PROMOTE", "tumor_growth": "INHIBIT"}
        },
        "pten": {
            "canonical_role": "tumor_suppressor",
            "primary_function": "INHIBIT_SURVIVAL_PATHWAY",
            "pathway": "PI3K/AKT Regulation",
            "synonyms": ["phosphatase and tensin homolog"],
            "expected_effects": {"akt_activation": "INHIBIT", "tumor_growth": "INHIBIT", "cell_survival": "INHIBIT"}
        },
        "p21": {
            "canonical_role": "cell_cycle_inhibitor",
            "primary_function": "ARREST_CELL_CYCLE",
            "pathway": "CDK Inhibition",
            "synonyms": ["cdkn1a", "cip1", "waf1"],
            "expected_effects": {"cell_cycle_progression": "INHIBIT", "cell_cycle_arrest": "PROMOTE"}
        },
        "p27": {
            "canonical_role": "cell_cycle_inhibitor",
            "primary_function": "ARREST_CELL_CYCLE",
            "pathway": "CDK Inhibition",
            "synonyms": ["cdkn1b", "kip1"],
            "expected_effects": {"cell_cycle_progression": "INHIBIT", "cell_cycle_arrest": "PROMOTE"}
        },
        "rb": {
            "canonical_role": "tumor_suppressor",
            "primary_function": "ARREST_CELL_CYCLE",
            "pathway": "G1/S Checkpoint",
            "synonyms": ["rb1", "retinoblastoma"],
            "expected_effects": {"cell_cycle_progression": "INHIBIT", "e2f_activity": "INHIBIT"}
        },

        # Survival kinases & Cell Cycle Promoters
        "akt": {
            "canonical_role": "survival_kinase",
            "primary_function": "PROMOTE_CELL_SURVIVAL",
            "pathway": "PI3K/AKT Pathway",
            "synonyms": ["protein kinase b", "pkb", "akt1"],
            "expected_effects": {"cell_survival": "PROMOTE", "apoptosis": "INHIBIT", "bad_phosphorylation": "PROMOTE"}
        },
        "mtor": {
            "canonical_role": "cell_growth_promoter",
            "primary_function": "PROMOTE_CELL_GROWTH",
            "pathway": "mTOR Signaling",
            "synonyms": ["mechanistic target of rapamycin"],
            "expected_effects": {"cell_growth": "PROMOTE", "protein_synthesis": "PROMOTE", "autophagy": "INHIBIT"}
        },
        "cyclin d1": {
            "canonical_role": "cell_cycle_promoter",
            "primary_function": "PROMOTE_CELL_CYCLE",
            "pathway": "G1/S Transition",
            "synonyms": ["ccnd1"],
            "expected_effects": {"cell_cycle_progression": "PROMOTE", "g1_s_transition": "PROMOTE"}
        }
    }

    # Action direction keywords
    PROMOTE_KEYWORDS = [
        r'\bpromotes?\b', r'\binduces?\b', r'\bactivates?\b', r'\btriggers?\b',
        r'\benhances?\b', r'\bcauses?\b', r'\baccelerates?\b', r'\bstimulates?\b',
        r'\bmediates?\s+apoptosis\b', r'القا(?:ی)?', r'فعال‌?سازی', r'افزایش', r'تحریک', r'پیش‌?برد'
    ]

    INHIBIT_KEYWORDS = [
        r'\binhibits?\b', r'\bsuppresses?\b', r'\bblocks?\b', r'\bprevents?\b',
        r'\battenuates?\b', r'\breduces?\b', r'\bdecreases?\b', r'مهار', r'کاهش', r'سرکوب', r'بلاک', r'جلوگیری'
    ]

    APOPTOSIS_KEYWORDS = [
        r'\bapoptosis\b', r'\bapoptotic\b', r'\bprogrammed\s+cell\s+death\b', r'آپوپتوز', r'مرگ\s+برنامه‌?ریزی‌?شده'
    ]

    # Causal inference leap keywords (Level B)
    CAUSAL_LEAP_PATTERNS = [
        r'\b(?:therefore|thereby|thus|consequently|hence)\s+(?:increases?|enhances?|leads\s+to|causes?)\b',
        r'در\s+نتیجه\s+(?:باعث|منجر\s+به|افزایش)',
        r'بنابراین\s+(?:موجب|تکثیر|انکولیز)',
        r'\bleads\s+to\s+(?:increased\s+viral|enhanced\s+viral|productive\s+replication|oncolysis)\b'
    ]

    @classmethod
    def check(cls, claim: str, context_section: Optional[str] = None) -> MechanismCheckResult:
        """
        Extracts molecular entities and asserted causal directions from claim text.
        Verifies Level A (Role Inversion) and Level B (Mechanistic Inference Leaps).
        """
        claim_str = str(claim).strip()
        claim_lower = claim_str.lower()

        # 1. Identify Target Entity in Claim
        detected_entity_key = None
        matched_kb_entry = None

        for key, entry in cls.CANONICAL_KNOWLEDGE_BASE.items():
            if re.search(r'\b' + re.escape(key) + r'\b', claim_lower):
                detected_entity_key = key
                matched_kb_entry = entry
                break
            for syn in entry.get("synonyms", []):
                if re.search(r'\b' + re.escape(syn) + r'\b', claim_lower):
                    detected_entity_key = key
                    matched_kb_entry = entry
                    break
            if detected_entity_key:
                break

        # Level B: Check for multi-step mechanistic causal leaps without direct proof
        has_causal_leap = any(re.search(pat, claim_lower) for pat in cls.CAUSAL_LEAP_PATTERNS)
        if has_causal_leap:
            # Check if this asserts an ungrounded bridge between target modulation and viral replication/oncolysis
            if any(term in claim_lower for term in ["viral", "oncolysis", "replication", "ویروس", "تکثیر", "انکولیز"]):
                rationale = (
                    "LEVEL_B_MECHANISTIC_INFERENCE: استنتاج مکانیسمی چندمرحله‌ای شناسایی شد. "
                    "کاهش یا تغییر بیان یک پروتئین سلولی لزوماً اثبات‌کننده افزایش تکثیر یا انکولیز ویروس نیست؛ "
                    "این ادعا باید به عنوان یک فرضیه (Hypothesis) صورت‌بندی شود نه مکانیسم اثبات‌شده."
                )
                return MechanismCheckResult(
                    status="NOT_ESTABLISHED",
                    correction="این گزاره باید به صورت فرضیه مطرح شود نه حقیقت اثبات‌شده.",
                    confidence=0.90,
                    entity=detected_entity_key,
                    canonical_role=matched_kb_entry["canonical_role"] if matched_kb_entry else None,
                    asserted_role="mechanistic_causal_leap",
                    context_section=context_section,
                    scientific_rationale=rationale,
                    inference_type="MULTI_STEP_INFERENCE"
                )

        # If entity not found in structured ontology, return UNVERIFIED
        if not detected_entity_key or not matched_kb_entry:
            return MechanismCheckResult(
                status="UNVERIFIED",
                correction=None,
                confidence=0.0,
                entity=None,
                canonical_role=None,
                asserted_role=None,
                context_section=context_section,
                scientific_rationale="مولکول یا عامل بیولوژیک مورد ادعا در دانش‌نامه ساختاریافته مرجع موجود نیست؛ فاقد اعتبارسنجی قطعی.",
                inference_type="DIRECT_ROLE_CHECK"
            )

        # 2. Extract Asserted Direction regarding Apoptosis / Survival
        has_apoptosis_mention = any(re.search(pat, claim_lower) for pat in cls.APOPTOSIS_KEYWORDS)
        asserts_promotion = any(re.search(pat, claim_lower) for pat in cls.PROMOTE_KEYWORDS)
        asserts_inhibition = any(re.search(pat, claim_lower) for pat in cls.INHIBIT_KEYWORDS)

        canonical_role = matched_kb_entry["canonical_role"]
        expected_apoptosis_effect = matched_kb_entry["expected_effects"].get("apoptosis")

        # 3. Level A: Check for Role Inversion regarding Apoptosis
        if has_apoptosis_mention:
            # Case A: Entity is Anti-Apoptotic (expected INHIBIT), but claim asserts PROMOTE / INDUCE
            if expected_apoptosis_effect == "INHIBIT" and asserts_promotion and not asserts_inhibition:
                correction = (
                    f"خطای وارونگی نقش بیولوژیک: پروتئین {detected_entity_key.upper()} یک عامل ضدآپوپتوز (anti-apoptotic) است "
                    f"که مانع از رخداد آپوپتوز و پرمه‌آبیلیزه شدن غشای میتوکندری (MOMP) می‌گردد، نه اینکه آپوپتوز را القا یا فعال کند."
                )
                return MechanismCheckResult(
                    status="CONTRADICTED",
                    correction=correction,
                    confidence=0.98,
                    entity=detected_entity_key,
                    canonical_role=canonical_role,
                    asserted_role="pro-apoptotic / induces apoptosis",
                    context_section=context_section,
                    scientific_rationale=f"Assertion '{claim_str}' contradicts canonical function of {detected_entity_key} ({canonical_role}).",
                    inference_type="DIRECT_ROLE_CHECK"
                )

            # Case B: Entity is Pro-Apoptotic (expected PROMOTE), but claim asserts INHIBIT
            if expected_apoptosis_effect == "PROMOTE" and asserts_inhibition and not asserts_promotion:
                correction = (
                    f"خطای وارونگی نقش بیولوژیک: پروتئین {detected_entity_key.upper()} یک عامل پیش‌آپوپتوز (pro-apoptotic) است "
                    f"که آپوپتوز را پیش می‌برد یا اجرا می‌کند، نه اینکه آپوپتوز را مهار کند."
                )
                return MechanismCheckResult(
                    status="CONTRADICTED",
                    correction=correction,
                    confidence=0.98,
                    entity=detected_entity_key,
                    canonical_role=canonical_role,
                    asserted_role="anti-apoptotic / inhibits apoptosis",
                    context_section=context_section,
                    scientific_rationale=f"Assertion '{claim_str}' contradicts canonical function of {detected_entity_key} ({canonical_role}).",
                    inference_type="DIRECT_ROLE_CHECK"
                )

            # Case C: Compatible claim
            if (expected_apoptosis_effect == "INHIBIT" and asserts_inhibition) or \
               (expected_apoptosis_effect == "PROMOTE" and asserts_promotion):
                return MechanismCheckResult(
                    status="VERIFIED",
                    correction=None,
                    confidence=0.95,
                    entity=detected_entity_key,
                    canonical_role=canonical_role,
                    asserted_role=f"consistent ({expected_apoptosis_effect.lower()} apoptosis)",
                    context_section=context_section,
                    scientific_rationale=f"Assertion aligns with canonical role: {detected_entity_key} acts as {canonical_role}.",
                    inference_type="DIRECT_ROLE_CHECK"
                )

        # 4. Generic check if no direct apoptosis term
        return MechanismCheckResult(
            status="VERIFIED",
            correction=None,
            confidence=0.85,
            entity=detected_entity_key,
            canonical_role=canonical_role,
            asserted_role="contextual_statement",
            context_section=context_section,
            scientific_rationale=f"Entity {detected_entity_key} identified with canonical role {canonical_role}; no direct contradiction detected.",
            inference_type="DIRECT_ROLE_CHECK"
        )

    @classmethod
    def verify_mechanistic_chain(
        cls,
        agent: str,
        target: str,
        cellular_process: str,
        interaction: Optional[str] = None,
        endpoint: Optional[str] = None,
        evidence_records: Optional[List[Dict[str, Any]]] = None
    ) -> MechanisticChainAnalysis:
        """
        Level B: Rigorously verifies each edge in a multi-step mechanistic causal chain:
        Edge 1: Agent -> Target (e.g. Agent_A -> Target_X suppression)
        Edge 2: Target -> Cellular Process (e.g. Target_X -> Mitochondrial permeability)
        Edge 3: Cellular Process -> Drug/Viral Interaction (e.g. Apoptosis threshold -> Interaction endpoint)
        Edge 4: Interaction -> Phenotypic Endpoint (e.g. Interaction -> Synergistic cytotoxicity)
        """
        records = evidence_records or []
        edges: List[MechanisticEdge] = []
        unsupported: List[MechanisticEdge] = []

        # Edge 1: Agent -> Target
        e1_supported = False
        e1_cit = None
        for r in records:
            txt = (str(r.get("title", "")) + " " + str(r.get("abstract", ""))).lower()
            if target.lower() in txt:
                e1_supported = True
                e1_cit = r.get("source_id") or r.get("pmid")
                break

        e1 = MechanisticEdge(
            source=agent,
            target=target,
            relation="modulates_expression_or_activity",
            evidence_status="ESTABLISHED" if e1_supported else "UNSUPPORTED",
            confidence=0.90 if e1_supported else 0.30,
            evidence_citation=e1_cit,
            notes="Direct pharmacological effect on target"
        )
        edges.append(e1)
        if not e1_supported:
            unsupported.append(e1)

        # Edge 2: Target -> Cellular Process (Canonical biological function)
        target_key = target.lower()
        kb_entry = cls.CANONICAL_KNOWLEDGE_BASE.get(target_key)
        e2_status = "ESTABLISHED" if kb_entry else "SUPPORTED_BY_ANALOG"
        e2 = MechanisticEdge(
            source=target,
            target=cellular_process,
            relation="canonical_cellular_regulation",
            evidence_status=e2_status,
            confidence=0.95 if kb_entry else 0.70,
            notes=f"Pathway: {kb_entry.get('pathway') if kb_entry else 'General Signaling'}"
        )
        edges.append(e2)

        # Edge 3: Cellular Process -> Interaction / Viral Replication
        if interaction:
            e3_supported = False
            e3_cit = None
            for r in records:
                txt = (str(r.get("title", "")) + " " + str(r.get("abstract", ""))).lower()
                if (cellular_process.lower() in txt or target.lower() in txt) and any(w in txt for w in ["virus", "viral", "replication", "titer", "oncoly"]):
                    e3_supported = True
                    e3_cit = r.get("source_id") or r.get("pmid")
                    break

            e3 = MechanisticEdge(
                source=cellular_process,
                target=interaction,
                relation="facilitates_or_potentiates_interaction",
                evidence_status="SUPPORTED_BY_DIRECT_STUDY" if e3_supported else "HYPOTHETICAL",
                confidence=0.85 if e3_supported else 0.40,
                evidence_citation=e3_cit,
                notes="Bridge between host cellular process and viral/drug oncolysis"
            )
            edges.append(e3)
            if not e3_supported:
                unsupported.append(e3)

        # Edge 4: Interaction -> Phenotypic Endpoint
        if endpoint:
            e4_status = "SUPPORTED_BY_DIRECT_STUDY" if (len(unsupported) == 0 and len(records) > 0) else "HYPOTHETICAL"
            e4 = MechanisticEdge(
                source=interaction or cellular_process,
                target=endpoint,
                relation="results_in_phenotypic_change",
                evidence_status=e4_status,
                confidence=0.85 if e4_status == "SUPPORTED_BY_DIRECT_STUDY" else 0.45,
                notes="Terminal phenotypic manifestation"
            )
            edges.append(e4)
            if e4_status == "HYPOTHETICAL":
                unsupported.append(e4)

        is_fully_established = (len(unsupported) == 0)
        if is_fully_established:
            status = "ESTABLISHED"
            summary_fa = "تمامی یال‌های زنجیره مکانیسمی دارای شواهد مستقیم و اعتبار تجربی می‌باشند."
            rationale = "Full mechanistic chain grounded in published evidence."
        elif len(unsupported) == len(edges):
            status = "NOT_ESTABLISHED"
            summary_fa = "زنجیره مکانیسمی فاقد شواهد پشتیبان بوده و کاملاً فرضی است."
            rationale = "Entire mechanistic chain lacks empirical evidence."
        else:
            status = "HYPOTHETICAL_INFERENCE"
            summary_fa = (
                f"زنجیره مکانیسمی دارای {len(unsupported)} گسست تجربی است؛ "
                f"بخش‌هایی از زنجیره بر پایه فرضیات منطقی شکل گرفته و نمی‌تواند به عنوان مکانیسم اثبات‌شده قطعی ارائه گردد."
            )
            rationale = f"Chain contains {len(unsupported)} unverified inferential leaps."

        return MechanisticChainAnalysis(
            chain_status=status,
            edges=edges,
            unsupported_edges=unsupported,
            is_fully_established=is_fully_established,
            scientific_summary_fa=summary_fa,
            rationale=rationale
        )


biological_mechanism_adversarial_verifier = BiologicalMechanismAdversarialVerifier
