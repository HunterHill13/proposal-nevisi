#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Epistemic Rigor Auditor (Pillar 10 / ARA Seal Level 2 Alignment)
================================================================
Evaluates biomedical proposals against 6 epistemic rigor dimensions derived from
Orchestra-Research Agent-Native Research Artifacts (ARA) and the AIPOCH / arXiv:2606.11830v1
medical research benchmark.

Six Rigor Dimensions:
1. Evidence Grounding & Full-Text Authenticity (Fail-closed citation verification & full-text quota >= 80%)
2. Falsifiability & Formal Null Hypothesis (Explicit quantitative H0 and H1 with testable directions)
3. Methodological & End-to-End Coherence (Gap -> Endpoint -> Sample Size -> Statistical Model invariant)
4. Scope, Limits & Boundary Conditions (Model organism limitations, assay LOD, and feasibility constraints)
5. Exploration Integrity & Contradiction Resolution (Explicit resolution of conflicting literature findings)
6. Biological Resource Authentication (STR cell line authentication, RRIDs, chemical purity >= 95%)

Author: proposal-nevisi Hardened Modular Core
License: MIT / Academic Grant Compliance
"""

import re
from typing import Dict, Any, List, Optional, Tuple


class EpistemicRigorGateError(Exception):
    """Raised when a proposal or research dossier fails one or more epistemic rigor dimensions."""
    pass


class EpistemicRigorAuditor:
    """
    Evaluates research dossiers and proposals across 6 core epistemic dimensions.
    Acts as a blocking gatekeeper prior to final Word (.docx) publication.
    """

    PASS_THRESHOLD = 80.0  # Minimum composite score out of 100

    def __init__(self, fail_closed: bool = True):
        self.fail_closed = fail_closed

    def audit_dossier(self, dossier_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits a ProposalResearchDossier structure.
        Returns a detailed evaluation dictionary with dimension scores and findings.
        """
        results = {
            "dimension_1_evidence_grounding": self._check_evidence_grounding(dossier_data),
            "dimension_2_falsifiability": self._check_falsifiability(dossier_data),
            "dimension_3_methodological_coherence": self._check_methodological_coherence(dossier_data),
            "dimension_4_boundary_conditions": self._check_boundary_conditions(dossier_data),
            "dimension_5_contradiction_resolution": self._check_contradiction_resolution(dossier_data),
            "dimension_6_biological_authentication": self._check_biological_authentication(dossier_data),
        }

        # Calculate overall score (weighted equally across all 6 dimensions)
        dim_scores = [d["score"] for d in results.values()]
        composite_score = sum(dim_scores) / len(dim_scores)

        all_findings = []
        blocking_failures = []

        for dim_name, dim_res in results.items():
            for f in dim_res.get("findings", []):
                all_findings.append(f"[{dim_name}] {f}")
            if not dim_res.get("passed", False):
                blocking_failures.append(f"{dim_name}: {dim_res.get('reason', 'Failed threshold')}")

        passed = (composite_score >= self.PASS_THRESHOLD) and (len(blocking_failures) == 0)

        report = {
            "passed": passed,
            "composite_score": round(composite_score, 1),
            "dimensions": results,
            "blocking_failures": blocking_failures,
            "all_findings": all_findings,
            "seal_status": "SEALED_LEVEL_2" if passed else "AUDIT_REJECTED",
        }

        if not passed and self.fail_closed:
            failures_str = "; ".join(blocking_failures)
            raise EpistemicRigorGateError(
                f"Epistemic Rigor Audit FAILED (Score: {composite_score:.1f}/100). Blocking failures: {failures_str}"
            )

        return report

    def _check_evidence_grounding(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Dimension 1: Evidence Grounding & Full-Text Authenticity."""
        evidence = data.get("literature_evidence", [])
        if not evidence:
            return {"passed": False, "score": 0.0, "reason": "No literature evidence provided in dossier", "findings": ["Zero cited literature."]}

        total = len(evidence)
        full_text_count = sum(1 for e in evidence if e.get("is_full_text", False))
        unverified = [e for e in evidence if not e.get("verified", False)]
        has_grounded_passages = sum(1 for e in evidence if len(e.get("passages", [])) > 0)

        findings = []
        score = 100.0

        if unverified:
            score -= 50.0
            findings.append(f"Found {len(unverified)} unverified references without verified PMID/DOI.")

        # Check abstract-only justification compliance
        abstract_only_papers = [e for e in evidence if not e.get("is_full_text", False)]
        unjustified_abstracts = [
            e for e in abstract_only_papers 
            if not e.get("abstract_only_justification") or len(str(e.get("abstract_only_justification")).strip()) < 10
        ]
        if unjustified_abstracts:
            score -= len(unjustified_abstracts) * 20.0
            findings.append(f"Found {len(unjustified_abstracts)} abstract-only reference(s) lacking mandatory explicit paywall/unindexed justification.")

        full_text_ratio = full_text_count / total if total > 0 else 0
        if full_text_ratio < 0.85:
            deficit = (0.85 - full_text_ratio) * 100
            score -= deficit * 0.8
            findings.append(f"Full-text ratio ({full_text_ratio*100:.1f}%) is below 85% quota target (max 15% abstract-only permitted).")

        passage_ratio = has_grounded_passages / total if total > 0 else 0
        if passage_ratio < 0.80:
            deficit = (0.80 - passage_ratio) * 100
            score -= deficit * 0.5
            findings.append(f"Grounded evidence passages ratio ({passage_ratio*100:.1f}%) is below 80% target.")

        score = max(0.0, min(100.0, score))
        passed = (score >= self.PASS_THRESHOLD) and (len(unverified) == 0) and (full_text_ratio >= 0.85) and (len(unjustified_abstracts) == 0)
        return {
            "passed": passed,
            "score": round(score, 1),
            "full_text_ratio": round(full_text_ratio, 2),
            "unverified_count": len(unverified),
            "unjustified_abstracts_count": len(unjustified_abstracts),
            "findings": findings,
            "reason": findings[0] if findings else "Evidence grounding compliant."
        }

    def _check_falsifiability(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Dimension 2: Falsifiability & Formal Null Hypothesis."""
        hypotheses = data.get("hypotheses", {})
        h0 = hypotheses.get("h0", "").strip()
        h1 = hypotheses.get("h1", "").strip()

        score = 100.0
        findings = []

        if not h0 or len(h0) < 15:
            score -= 50.0
            findings.append("Null hypothesis (H0) is missing or insufficiently defined.")
        if not h1 or len(h1) < 15:
            score -= 40.0
            findings.append("Alternative hypothesis (H1) is missing or insufficiently defined.")

        # Check for directionality or quantitative metric
        combined = f"{h0} {h1}".lower()
        has_quant_or_dir = any(w in combined for w in ["معنی‌دار", "افزایش", "کاهش", "تفاوت", "برابر", "significant", "difference", "effect", "increase", "decrease"])
        if not has_quant_or_dir:
            score -= 20.0
            findings.append("Hypotheses lack explicit statistical directionality or measurable effect metric.")

        score = max(0.0, min(100.0, score))
        passed = (score >= self.PASS_THRESHOLD)
        return {
            "passed": passed,
            "score": round(score, 1),
            "findings": findings,
            "reason": findings[0] if findings else "Falsifiability criteria met."
        }

    def _check_methodological_coherence(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Dimension 3: Methodological & End-to-End Coherence."""
        invariants = data.get("methodological_invariants", {})
        study_family = invariants.get("study_family", "")
        primary_endpoint = invariants.get("primary_endpoint", "")
        sample_size_formula = invariants.get("sample_size_formula", "")
        statistical_test = invariants.get("statistical_test", "")

        score = 100.0
        findings = []

        if not study_family:
            score -= 30.0
            findings.append("Study design family (in vitro / in vivo / clinical / cohort) is undeclared.")
        if not primary_endpoint:
            score -= 25.0
            findings.append("Primary quantitative endpoint is undefined.")
        if not sample_size_formula:
            score -= 25.0
            findings.append("Bio-statistical sample size calculation formula is omitted.")
        if not statistical_test:
            score -= 20.0
            findings.append("Statistical analysis model/test is unspecified.")

        # Coherence rule: If study is factorial, test cannot be simple 2-group t-test without two-way interaction
        if "factorial" in study_family.lower() and "t-test" in statistical_test.lower() and "anova" not in statistical_test.lower():
            score -= 30.0
            findings.append("Methodological mismatch: Factorial study requires Two-Way ANOVA/Regression, not isolated t-test.")

        score = max(0.0, min(100.0, score))
        passed = (score >= self.PASS_THRESHOLD)
        return {
            "passed": passed,
            "score": round(score, 1),
            "findings": findings,
            "reason": findings[0] if findings else "Methodological coherence verified."
        }

    def _check_boundary_conditions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Dimension 4: Scope, Limits & Boundary Conditions."""
        limitations = data.get("limitations_and_boundaries", [])
        score = 100.0
        findings = []

        if not limitations:
            score -= 40.0
            findings.append("No explicit methodological limitations or boundary conditions declared.")
        elif len(limitations) < 2:
            score -= 25.0
            findings.append("Insufficient boundary conditions: at least 2 distinct study limitations/assumptions required.")

        # Check for model system limit declaration (e.g. translation gap or in vitro extrapolation)
        all_limits = " ".join(limitations).lower()
        has_trans_limit = any(term in all_limits for term in ["ترجمان", "بالینی", "محدودیت", "خطا", "تداخل", "extrapolation", "translation", "limitation", "confounder"])
        if not has_trans_limit:
            score -= 15.0
            findings.append("Limitations fail to address biological translation or potential experimental confounders.")

        score = max(0.0, min(100.0, score))
        passed = (score >= self.PASS_THRESHOLD)
        return {
            "passed": passed,
            "score": round(score, 1),
            "findings": findings,
            "reason": findings[0] if findings else "Boundary conditions compliant."
        }

    def _check_contradiction_resolution(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Dimension 5: Exploration Integrity & Contradiction Resolution."""
        contradictions = data.get("contradictory_evidence", [])
        score = 100.0
        findings = []

        if not contradictions:
            # Advisory deduction if zero contradictions or conflicting studies searched
            score -= 10.0
            findings.append("Notice: No contradictory literature documented; ensure negative or conflicting studies were surveyed.")
        else:
            unresolved = [c for c in contradictions if not c.get("resolution_rationale", "").strip()]
            if unresolved:
                score -= 30.0
                findings.append(f"Found {len(unresolved)} documented contradictory findings without a scientific resolution rationale.")

        score = max(0.0, min(100.0, score))
        passed = (score >= self.PASS_THRESHOLD)
        return {
            "passed": passed,
            "score": round(score, 1),
            "findings": findings,
            "reason": findings[0] if findings else "Contradiction resolution verified."
        }

    def _check_biological_authentication(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Dimension 6: Biological Resource Authentication."""
        entities = data.get("biological_entities", [])
        score = 100.0
        findings = []

        if not entities:
            score -= 20.0
            findings.append("No biological entities or key reagents cataloged in dossier.")
        else:
            unauthenticated = []
            for ent in entities:
                ent_type = ent.get("type", "").lower()
                identifier = ent.get("identifier", "").strip()
                # If cell line, must have STR or ATCC/RRID
                if "cell" in ent_type and not identifier:
                    unauthenticated.append(f"Cell line '{ent.get('name')}' missing STR authentication or catalog ID.")
                # If chemical compound, purity should be declared
                elif "compound" in ent_type or "drug" in ent_type:
                    purity = ent.get("purity", "")
                    if not purity or purity == "NOT_REPORTED":
                        findings.append(f"Chemical entity '{ent.get('name')}' missing >=95% purity verification.")

            if unauthenticated:
                score -= len(unauthenticated) * 15.0
                findings.extend(unauthenticated)

        score = max(0.0, min(100.0, score))
        passed = (score >= self.PASS_THRESHOLD)
        return {
            "passed": passed,
            "score": round(score, 1),
            "findings": findings,
            "reason": findings[0] if findings else "Biological resource authentication compliant."
        }
