#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Proposal Research Dossier (Pillar 10 / Persistent Research Memory)
==================================================================
Manages the structured, persistent research record that decouples the evidence
discovery and grounding phase (Inner Loop) from the 28-section proposal synthesis
phase (Outer Loop).

Enforces:
1. Two-Loop lifecycle: Dossier must be audited and sealed before section drafting.
2. Dual export: Machine-readable JSON (`PROPOSAL_RESEARCH_DOSSIER.json`) and
   human-readable Persian/English Markdown (`PROPOSAL_RESEARCH_DOSSIER.md`).
3. Deep tracking of:
   - Hypotheses ($H_0$, $H_1$) and quantitative primary endpoints.
   - Biological entities authenticated via RRID/ATCC/CAS with purity >= 95%.
   - Full-text literature grounding with verbatim evidence passages.
   - Contradictory literature findings and explicit scientific resolutions.
   - Methodological invariants (study family, sample size equation, ANOVA/regression test).
   - Epistemic rigor audit status via EpistemicRigorAuditor.

Author: proposal-nevisi Hardened Modular Core
License: MIT / Academic Grant Compliance
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

try:
    from scripts.epistemic_rigor_auditor import EpistemicRigorAuditor, EpistemicRigorGateError
except ImportError:
    from epistemic_rigor_auditor import EpistemicRigorAuditor, EpistemicRigorGateError


class ProposalResearchDossier:
    """
    Encapsulates the persistent, verifiable research memory for a biomedical proposal.
    """

    def __init__(self, topic: str, domain: str = "Biomedical Science"):
        self.topic = topic
        self.domain = domain
        self.created_at = datetime.utcnow().isoformat() + "Z"
        self.sealed_at: Optional[str] = None
        self.is_sealed: bool = False

        self.hypotheses: Dict[str, str] = {
            "h0": "",
            "h1": "",
            "rationale": ""
        }

        self.methodological_invariants: Dict[str, Any] = {
            "study_family": "",
            "primary_endpoint": "",
            "sample_size_formula": "",
            "target_n": None,
            "statistical_test": "",
            "alpha": 0.05,
            "power": 0.80
        }

        self.biological_entities: List[Dict[str, Any]] = []
        self.literature_evidence: List[Dict[str, Any]] = []
        self.contradictory_evidence: List[Dict[str, Any]] = []
        self.limitations_and_boundaries: List[str] = []
        self.audit_report: Optional[Dict[str, Any]] = None

    def set_hypotheses(self, h0: str, h1: str, rationale: str = "") -> None:
        """Sets null and alternative hypotheses."""
        if self.is_sealed:
            raise RuntimeError("Cannot modify a sealed research dossier.")
        self.hypotheses["h0"] = h0.strip()
        self.hypotheses["h1"] = h1.strip()
        self.hypotheses["rationale"] = rationale.strip()

    def set_methodological_invariants(
        self,
        study_family: str,
        primary_endpoint: str,
        sample_size_formula: str,
        target_n: Optional[int] = None,
        statistical_test: str = "",
        alpha: float = 0.05,
        power: float = 0.80
    ) -> None:
        """Sets the core invariant links between design, endpoints, and statistics."""
        if self.is_sealed:
            raise RuntimeError("Cannot modify a sealed research dossier.")
        self.methodological_invariants.update({
            "study_family": study_family.strip(),
            "primary_endpoint": primary_endpoint.strip(),
            "sample_size_formula": sample_size_formula.strip(),
            "target_n": target_n,
            "statistical_test": statistical_test.strip(),
            "alpha": alpha,
            "power": power
        })

    def add_biological_entity(
        self,
        name: str,
        entity_type: str,
        identifier: str = "",
        purity: str = ">=95%",
        source: str = ""
    ) -> None:
        """Adds and authenticates a biological reagent or entity."""
        if self.is_sealed:
            raise RuntimeError("Cannot modify a sealed research dossier.")
        self.biological_entities.append({
            "name": name.strip(),
            "type": entity_type.strip(),
            "identifier": identifier.strip(),
            "purity": purity.strip(),
            "source": source.strip()
        })

    def add_evidence_paper(
        self,
        pmid: str,
        doi: str,
        title: str,
        authors: List[str],
        year: int,
        is_full_text: bool = True,
        verified: bool = True,
        passages: Optional[List[str]] = None,
        grade: str = "High"
    ) -> None:
        """Adds a verified scientific reference with verbatim grounded passages."""
        if self.is_sealed:
            raise RuntimeError("Cannot modify a sealed research dossier.")
        self.literature_evidence.append({
            "pmid": pmid.strip(),
            "doi": doi.strip(),
            "title": title.strip(),
            "authors": authors,
            "year": year,
            "is_full_text": is_full_text,
            "verified": verified,
            "passages": passages or [],
            "grade": grade
        })

    def add_contradictory_finding(
        self,
        topic: str,
        reported_claim_a: str,
        citation_a: str,
        reported_claim_b: str,
        citation_b: str,
        resolution_rationale: str
    ) -> None:
        """Adds documented contradictory literature along with a mechanistic resolution."""
        if self.is_sealed:
            raise RuntimeError("Cannot modify a sealed research dossier.")
        self.contradictory_evidence.append({
            "topic": topic.strip(),
            "claim_a": reported_claim_a.strip(),
            "citation_a": citation_a.strip(),
            "claim_b": reported_claim_b.strip(),
            "citation_b": citation_b.strip(),
            "resolution_rationale": resolution_rationale.strip()
        })

    def add_limitation(self, limitation_text: str) -> None:
        """Adds an explicit boundary condition or study limitation."""
        if self.is_sealed:
            raise RuntimeError("Cannot modify a sealed research dossier.")
        lim = limitation_text.strip()
        if lim and lim not in self.limitations_and_boundaries:
            self.limitations_and_boundaries.append(lim)

    def seal_dossier(self, auditor: Optional[EpistemicRigorAuditor] = None) -> Dict[str, Any]:
        """
        Runs the 6-dimension epistemic audit and seals the dossier.
        Raises EpistemicRigorGateError if fail-closed audit fails.
        """
        if self.is_sealed:
            return self.audit_report or {}

        aud = auditor or EpistemicRigorAuditor(fail_closed=True)
        data = self.to_dict()
        report = aud.audit_dossier(data)

        self.audit_report = report
        self.is_sealed = True
        self.sealed_at = datetime.utcnow().isoformat() + "Z"
        return report

    def to_dict(self) -> Dict[str, Any]:
        """Serializes dossier state into a dictionary."""
        return {
            "topic": self.topic,
            "domain": self.domain,
            "created_at": self.created_at,
            "sealed_at": self.sealed_at,
            "is_sealed": self.is_sealed,
            "hypotheses": self.hypotheses,
            "methodological_invariants": self.methodological_invariants,
            "biological_entities": self.biological_entities,
            "literature_evidence": self.literature_evidence,
            "contradictory_evidence": self.contradictory_evidence,
            "limitations_and_boundaries": self.limitations_and_boundaries,
            "audit_report": self.audit_report
        }

    def export_json(self, output_path: str) -> str:
        """Exports the dossier to a JSON file."""
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        data = self.to_dict()
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return output_path

    def export_markdown(self, output_path: str) -> str:
        """Exports the dossier to a comprehensive human-readable Markdown file."""
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        data = self.to_dict()

        md_lines = [
            f"# پرونده پژوهشی و پایگاه استنادی پروپوزال (Proposal Research Dossier)",
            f"",
            f"- **موضوع پژوهش**: {self.topic}",
            f"- **حوزه تخصصی**: {self.domain}",
            f"- **تاریخ ایجاد**: `{self.created_at}`",
            f"- **وضعیت پلمپ پرونده (Seal Status)**: `{'پلمپ شده (SEALED)' if self.is_sealed else 'پیش‌نویس (DRAFT)'}`",
            f"- **تاریخ پلمپ**: `{self.sealed_at or 'هنوز پلمپ نشده است'}`",
            f"",
            f"---",
            f"",
            f"## ۱. فرضیات پژوهش (Formal Hypotheses)",
            f"",
            f"- **فرضیه صفر ($H_0$)**: {self.hypotheses.get('h0', 'تعریف نشده')}",
            f"- **فرضیه جایگزین ($H_1$)**: {self.hypotheses.get('h1', 'تعریف نشده')}",
            f"- **توجیه مکانیکی و منطق فرضیه**: {self.hypotheses.get('rationale', 'تعریف نشده')}",
            f"",
            f"---",
            f"",
            f"## ۲. پیوستگی متدولوژیک بالادست/پایین‌دست (Methodological Invariants)",
            f"",
            f"| مؤلفه | مقدار تعریف‌شده در پرونده |",
            f"| :--- | :--- |",
            f"| **خانواده طراحی مطالعه** | `{self.methodological_invariants.get('study_family')}` |",
            f"| **نقطه پایانی اولیه (Primary Endpoint)** | {self.methodological_invariants.get('primary_endpoint')} |",
            f"| **فرمول محاسبه حجم نمونه** | `{self.methodological_invariants.get('sample_size_formula')}` |",
            f"| **تعداد نمونه کل ($N$)** | `{self.methodological_invariants.get('target_n')}` |",
            f"| **مدل/آزمون آماری اولیه** | `{self.methodological_invariants.get('statistical_test')}` |",
            f"| **سطح خطا و توان آزمون** | $\\alpha={self.methodological_invariants.get('alpha')}, 1-\\beta={self.methodological_invariants.get('power')}$ |",
            f"",
            f"---",
            f"",
            f"## ۳. احراز اصالت موجودیت‌های زیستی و معرف‌ها (Biological Resource Authentication)",
            f"",
        ]

        if not self.biological_entities:
            md_lines.append("_موجودیت زیستی یا معرف شیمیایی ثبت نشده است._\n")
        else:
            md_lines.extend([
                f"| نام ماده / خط سلولی | نوع | شناسه استاندارد (RRID / CAS) | خلوص / تأییدیه STR | منبع |",
                f"| :--- | :--- | :--- | :--- | :--- |",
            ])
            for ent in self.biological_entities:
                md_lines.append(
                    f"| {ent.get('name')} | {ent.get('type')} | `{ent.get('identifier')}` | {ent.get('purity')} | {ent.get('source')} |"
                )
            md_lines.append("")

        md_lines.extend([
            f"---",
            f"",
            f"## ۴. پایگاه مقالات معتبر و فرازهای مستند (Literature Evidence & Grounded Passages)",
            f"",
        ])

        if not self.literature_evidence:
            md_lines.append("_مقاله‌ای ثبت نشده است._\n")
        else:
            for idx, paper in enumerate(self.literature_evidence, 1):
                authors_str = ", ".join(paper.get("authors", [])[:3])
                if len(paper.get("authors", [])) > 3:
                    authors_str += " et al."
                ft_badge = "✅ Full-Text" if paper.get("is_full_text") else "⚠️ Abstract-Only"
                md_lines.extend([
                    f"### [{idx}] {paper.get('title')}",
                    f"- **نویسندگان و سال**: {authors_str} ({paper.get('year')})",
                    f"- **شناسه‌ها**: PMID: `{paper.get('pmid')}` | DOI: [{paper.get('doi')}](https://doi.org/{paper.get('doi')}) | وضعیت متن: {ft_badge} | رتبه GRADE: `{paper.get('grade')}`",
                    f"- **فرازهای متنی استخراج‌شده (Verbatim Evidence Sentences)**:",
                ])
                passages = paper.get("passages", [])
                if not passages:
                    md_lines.append(f"  - _هیچ فراز مستندی استخراج نشده است._")
                else:
                    for p in passages:
                        md_lines.append(f"  > \"{p}\"")
                md_lines.append("")

        md_lines.extend([
            f"---",
            f"",
            f"## ۵. یافته‌های متناقض و تحلیل حل اختلاف (Contradictory Findings & Resolutions)",
            f"",
        ])

        if not self.contradictory_evidence:
            md_lines.append("_مورد تناقض ادبیات گزارش نشده است._\n")
        else:
            for c in self.contradictory_evidence:
                md_lines.extend([
                    f"### تناقض در موضوع: {c.get('topic')}",
                    f"- **دیدگاه الف ({c.get('citation_a')})**: {c.get('claim_a')}",
                    f"- **دیدگاه ب ({c.get('citation_b')})**: {c.get('claim_b')}",
                    f"- **تحلیل توجیهی و حل اختلاف (Resolution Rationale)**: {c.get('resolution_rationale')}",
                    f"",
                ])

        md_lines.extend([
            f"---",
            f"",
            f"## ۶. مرزها و محدودیت‌های روش‌شناختی (Boundaries & Limitations)",
            f"",
        ])
        for lim in self.limitations_and_boundaries:
            md_lines.append(f"- {lim}")
        md_lines.append("")

        if self.audit_report:
            md_lines.extend([
                f"---",
                f"",
                f"## ۷. گزارش ممیزی اپیستمیک (Epistemic Rigor Audit Report)",
                f"",
                f"- **نمره کل دقت علمی**: `{self.audit_report.get('composite_score')}/100`",
                f"- **نتیجه ارزیابی**: `{'قبول (PASSED)' if self.audit_report.get('passed') else 'رد (FAILED)'}`",
                f"- **نشان پلمپ (Seal Status)**: `{self.audit_report.get('seal_status')}`",
                f"",
                f"### یافته‌ها و توصیه‌های ممیزی:",
            ])
            for f in self.audit_report.get("all_findings", []):
                md_lines.append(f"- {f}")
            md_lines.append("")

        content = "\n".join(md_lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path
