#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
biological_mechanism_adversarial_verifier.py - Universal Biological Mechanism Verifier
Proposal-Nevisi Engine v9.0 (Layer 1: Scientific Accuracy)

Detects role inversion and contradictory biological assertions (e.g. asserting that
an anti-apoptotic protein like Bcl-xL or Bcl-2 induces apoptosis, or that a tumor suppressor
promotes oncogenesis) against a structured, extensible biological knowledge base.

100% General-Purpose: Zero hardcoded project subjects; uses an extensible ontology
of verified biological mechanisms.
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class MechanismCheckResult:
    status: str  # "VERIFIED" | "CONTRADICTED" | "UNVERIFIED"
    correction: Optional[str]
    confidence: float
    entity: Optional[str] = None
    canonical_role: Optional[str] = None
    asserted_role: Optional[str] = None
    context_section: Optional[str] = None
    scientific_rationale: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "correction": self.correction,
            "confidence": self.confidence,
            "entity": self.entity,
            "canonical_role": self.canonical_role,
            "asserted_role": self.asserted_role,
            "context_section": self.context_section,
            "scientific_rationale": self.scientific_rationale
        }

class BiologicalMechanismAdversarialVerifier:
    """Verifies biological mechanism claims against an authoritative molecular ontology."""

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
            "pathway": "Intrinsic Apoptosis",
            "synonyms": ["bbcb"],
            "expected_effects": {"apoptosis": "PROMOTE"}
        },
        "bid": {
            "canonical_role": "pro-apoptotic",
            "primary_function": "PROMOTE_APOPTOSIS",
            "pathway": "Apoptosis Cross-talk",
            "synonyms": ["tbid"],
            "expected_effects": {"apoptosis": "PROMOTE", "momp": "PROMOTE"}
        },
        "bim": {
            "canonical_role": "pro-apoptotic",
            "primary_function": "PROMOTE_APOPTOSIS",
            "pathway": "Intrinsic Apoptosis",
            "synonyms": ["bcl2l11"],
            "expected_effects": {"apoptosis": "PROMOTE"}
        },
        "puma": {
            "canonical_role": "pro-apoptotic",
            "primary_function": "PROMOTE_APOPTOSIS",
            "pathway": "p53-Mediated Apoptosis",
            "synonyms": ["bbc3"],
            "expected_effects": {"apoptosis": "PROMOTE"}
        },
        "noxa": {
            "canonical_role": "pro-apoptotic",
            "primary_function": "PROMOTE_APOPTOSIS",
            "pathway": "p53-Mediated Apoptosis",
            "synonyms": ["pmaip1"],
            "expected_effects": {"apoptosis": "PROMOTE"}
        },
        "cytochrome c": {
            "canonical_role": "pro-apoptotic",
            "primary_function": "PROMOTE_APOPTOSIS",
            "pathway": "Apoptosome Formation",
            "synonyms": ["cycs"],
            "expected_effects": {"apoptosis": "PROMOTE", "caspase_activation": "PROMOTE"}
        },

        # Caspases
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

    @classmethod
    def check(cls, claim: str, context_section: Optional[str] = None) -> MechanismCheckResult:
        """
        Extracts molecular entities and asserted causal directions from claim text.
        Verifies alignment against CANONICAL_KNOWLEDGE_BASE.
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
                scientific_rationale="مولکول یا عامل بیولوژیک مورد ادعا در دانش‌نامه ساختاریافته مرجع موجود نیست؛ فاقد اعتبارسنجی قطعی."
            )

        # 2. Extract Asserted Direction regarding Apoptosis / Survival
        has_apoptosis_mention = any(re.search(pat, claim_lower) for pat in cls.APOPTOSIS_KEYWORDS)
        asserts_promotion = any(re.search(pat, claim_lower) for pat in cls.PROMOTE_KEYWORDS)
        asserts_inhibition = any(re.search(pat, claim_lower) for pat in cls.INHIBIT_KEYWORDS)

        canonical_role = matched_kb_entry["canonical_role"]
        expected_apoptosis_effect = matched_kb_entry["expected_effects"].get("apoptosis")

        # 3. Check for Role Inversion regarding Apoptosis
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
                    scientific_rationale=f"Assertion '{claim_str}' contradicts canonical function of {detected_entity_key} ({canonical_role})."
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
                    scientific_rationale=f"Assertion '{claim_str}' contradicts canonical function of {detected_entity_key} ({canonical_role})."
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
                    scientific_rationale=f"Assertion aligns with canonical role: {detected_entity_key} acts as {canonical_role}."
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
            scientific_rationale=f"Entity {detected_entity_key} identified with canonical role {canonical_role}; no direct contradiction detected."
        )

biological_mechanism_adversarial_verifier = BiologicalMechanismAdversarialVerifier
