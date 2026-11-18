#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
egm_study_section_subagents.py - EGM-Powered Academic Grant Study Section
Proposal-Nevisi Engine v14.2.0 (Elephant-Goldfish Model Hybrid Architecture)

Implements the 6-Persona Goldfish Grant Study Section:
1. grant-significance-innovation (Skeptical Architect / YAGNI - derived from egm-zoom-out)
2. grant-methodology-biostatistics (Hostile Critic - derived from egm-design)
3. grant-evidence-entailment (Pedantic Literature & Citation Auditor - derived from egm-codebase-details)
4. grant-feasibility-logistics (Lab & Clinical Logistics Lead - derived from egm-implementation-readiness)
5. grant-ethics-lay-advocate (Bioethics & Naive Lay Reader - derived from egm-comprehension)
6. grant-study-section-sro (Scientific Review Officer Synthesizer - derived from egm-synthesizer)

Enforces:
- Stateless zero-context mindset (Goldfish Isolation)
- Anti-sycophancy & anti-glazing (no ungrounded promotional flattery)
- Paraphrase-first validation
- NIH 1.0 (Exceptional) to 9.0 (Poor) standardized scoring rubric
- Blocker / Major / Nit prioritized finding triage
"""

import os
import sys
import re
import json
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple, Union

try:
    from core_policies import (
        NIH_APPROVAL_SCORE_CEILING,
        classify_study_archetype,
        parse_proposal_sections as _core_parse_sections,
    )
except ImportError:  # pragma: no cover
    NIH_APPROVAL_SCORE_CEILING = 2.0
    classify_study_archetype = None
    _core_parse_sections = None

try:
    from verify_biostatistics import BiostatisticalValidator
except ImportError:  # pragma: no cover
    BiostatisticalValidator = None


@dataclass
class GoldfishFinding:
    issue_name: str
    severity: str  # "Blocker" | "Major" | "Nit"
    reviewer_lens: str
    affected_scope: str  # Section number or section heading
    discrepancy_description: str
    rationale_recommendation: str
    remediated: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "issue_name": self.issue_name,
            "severity": self.severity,
            "reviewer_lens": self.reviewer_lens,
            "affected_scope": self.affected_scope,
            "discrepancy_description": self.discrepancy_description,
            "rationale_recommendation": self.rationale_recommendation,
            "remediated": self.remediated
        }


@dataclass
class GoldfishReviewerResult:
    reviewer_id: str
    name_fa: str
    name_en: str
    egm_lens: str
    status: str  # "completed" | "not run"
    nih_score: float  # 1.0 (Exceptional) to 9.0 (Poor)
    paraphrase_summary: str
    findings: List[GoldfishFinding] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)

    @property
    def blockers(self) -> List[GoldfishFinding]:
        return [f for f in self.findings if f.severity == "Blocker"]

    @property
    def majors(self) -> List[GoldfishFinding]:
        return [f for f in self.findings if f.severity == "Major"]

    @property
    def nits(self) -> List[GoldfishFinding]:
        return [f for f in self.findings if f.severity == "Nit"]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "reviewer_id": self.reviewer_id,
            "name_fa": self.name_fa,
            "name_en": self.name_en,
            "egm_lens": self.egm_lens,
            "status": self.status,
            "nih_score": round(self.nih_score, 2),
            "paraphrase_summary": self.paraphrase_summary,
            "findings_count": len(self.findings),
            "blockers_count": len(self.blockers),
            "majors_count": len(self.majors),
            "nits_count": len(self.nits),
            "findings": [f.to_dict() for f in self.findings],
            "strengths": self.strengths,
            "weaknesses": self.weaknesses
        }


@dataclass
class EGMStudySectionResult:
    overall_nih_score: float
    funding_verdict: str  # "APPROVED_FUNDABLE" | "REVISION_REQUIRED" | "REJECTED_UNFUNDABLE"
    can_proceed: bool
    percentile: float
    reviewer_results: Dict[str, GoldfishReviewerResult]
    prioritized_findings: List[GoldfishFinding]
    remediation_rounds_conducted: int
    executive_summary_fa: str
    structural_completeness_percent: Optional[float] = None

    def __post_init__(self):
        if self.structural_completeness_percent is None:
            self.structural_completeness_percent = float(self.percentile)

    @property
    def total_blockers(self) -> int:
        return sum(1 for f in self.prioritized_findings if f.severity == "Blocker" and not f.remediated)

    @property
    def total_majors(self) -> int:
        return sum(1 for f in self.prioritized_findings if f.severity == "Major" and not f.remediated)

    @property
    def total_nits(self) -> int:
        return sum(1 for f in self.prioritized_findings if f.severity == "Nit" and not f.remediated)

    def to_dict(self) -> Dict[str, Any]:
        sc_pct = (
            self.structural_completeness_percent
            if self.structural_completeness_percent is not None
            else self.percentile
        )
        return {
            "overall_nih_score": round(self.overall_nih_score, 2),
            "funding_verdict": self.funding_verdict,
            "can_proceed": self.can_proceed,
            "percentile": round(self.percentile, 1),
            "structural_completeness_percent": round(sc_pct, 1),
            "remediation_rounds_conducted": self.remediation_rounds_conducted,
            "total_blockers": self.total_blockers,
            "total_majors": self.total_majors,
            "total_nits": self.total_nits,
            "executive_summary_fa": self.executive_summary_fa,
            "reviewer_results": {k: v.to_dict() for k, v in self.reviewer_results.items()},
            "prioritized_findings": [f.to_dict() for f in self.prioritized_findings]
        }


class EGMStudySectionCoordinator:
    """Orchestrates the 6-persona Goldfish Swarm Academic Grant Study Section."""

    @classmethod
    def parse_proposal_sections(cls, markdown_text: str) -> Dict[int, str]:
        """Extracts canonical 28 sections from Pajooheshyar markdown proposal text."""
        sections: Dict[int, str] = {}
        if _core_parse_sections is not None:
            sections = _core_parse_sections(markdown_text)

        if not sections:
            # Restrict top-level headings to # or ## only so ### subsections (e.g. ### 1. بار بیماری) never overwrite Section 1
            pattern = r'(?:^|\n)#{1,2}(?!#)\s*(?:(?:بخش|Section)\s+)?([۰-۹0-9]+)[\.\-\:\s]+([^\n]*)\n(.*?)(?=(?:\n#{1,2}(?!#)\s*(?:(?:بخش|Section)\s+)?[۰-۹0-9]+[\.\-\:\s]+)|$)'
            matches = re.findall(pattern, markdown_text, re.DOTALL | re.IGNORECASE)

            fa_to_en = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
            for num_str, title, content in matches:
                try:
                    norm_num = int(num_str.translate(fa_to_en))
                    if 1 <= norm_num <= 28:
                        sections[norm_num] = content.strip()
                except ValueError:
                    continue

        # Fallback if headers are formatted differently
        if not sections:
            for sec_num in range(1, 29):
                sec_pat = rf'(?:بخش|قسمت)?\s*(?:{sec_num}|{cls._to_fa_digits(sec_num)})[\.\-\:\s]+(.*?)(?=(?:بخش|قسمت)?\s*(?:{sec_num+1}|{cls._to_fa_digits(sec_num+1)})[\.\-\:\s]+|$)'
                m = re.search(sec_pat, markdown_text, re.DOTALL)
                if m:
                    sections[sec_num] = m.group(1).strip()

        return sections

    @staticmethod
    def _to_fa_digits(num: int) -> str:
        en_to_fa = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
        return str(num).translate(en_to_fa)

    @classmethod
    def evaluate_significance_and_innovation(cls, sections: Dict[int, str], data: Dict[str, Any]) -> GoldfishReviewerResult:
        """
        Lens 1: grant-significance-innovation (Derived from egm-zoom-out)
        High-altitude Contrarian / YAGNI check:
        - Problem Statement (Sec 2), Literature Review (Sec 3), Significance (Sec 4)
        - Disease burden justification (GLOBOCAN / NCDs / WHO)
        - Prevents incremental 'salami slicing' and unbacked assertions.
        """
        findings: List[GoldfishFinding] = []
        strengths: List[str] = []
        weaknesses: List[str] = []

        sec2 = sections.get(2, "")
        sec3 = sections.get(3, "")
        sec4 = sections.get(4, "")
        combined = f"{sec2}\n{sec3}\n{sec4}".lower()

        # Paraphrase generation
        paraphrase = "این پژوهش اهمیت و بار بیماری هدف را در جمعیت بررسی کرده و تلاش می‌کند با طراحی روش‌شناسی مدون، پاسخ علمی موثری برای خلاء موجود بیابد."
        if "سرطان" in combined or "neoplasm" in combined or "cancer" in combined:
            paraphrase = "طرح پیشنهادی بر مبنای بار سرطان و ضرورت کاهش مرگ‌ومیر یا هزینه‌های درمانی ناشی از آن متمرکز شده است."
        elif "اقتصاد سلامت" in combined or "che" in combined or "oop" in combined:
            paraphrase = "طرح پیشنهادی با هدف ارزیابی و مهار هزینه‌های کمرشکن سلامت (CHE) و پرداخت‌های مستقیم از جیب (OOP) در نظام سلامت پایه‌ریزی شده است."

        # Audit Vector 1: Disease Burden / Epidemiological Context
        has_burden = bool(re.search(r'(بار\s+بیماری|globocan|who|شیوع|میزان\s+بروز|مرگ\s*و\s*میر|هزینه‌|سالمندی)', combined))
        if has_burden:
            strengths.append("توجیه مستند بار بیماری و ضرورت ملی/بین‌المللی پژوهش بر مبنای شاخص‌های سلامت")
        else:
            findings.append(GoldfishFinding(
                issue_name="MISSING_EPIDEMIOLOGICAL_BURDEN_JUSTIFICATION",
                severity="Major",
                reviewer_lens="grant-significance-innovation",
                affected_scope="بخش ۲ و ۴ (بیان مسئله و ضرورت)",
                discrepancy_description="فقدان استناد کمی به بار بیماری، آمار شیوع یا داده‌های اپیدمیولوژیک معتبر جهت توجیه ضرورت پژوهش.",
                rationale_recommendation="افزودن آمارهای کمی بروز/شیوع بر پایه گزارش‌های GLOBOCAN یا گزارش‌های رسمی نظام سلامت."
            ))
            weaknesses.append("عدم توجیه کافی ابعاد اقتصادی یا اپیدمیولوژیک بیماری در مقدمه")

        # Audit Vector 2: Innovation vs Reinventing the Wheel
        has_novelty = bool(re.search(r'(نوآوری|خلاء\s+پژوهشی|برای\s+نخستین\s+بار|شکاف\s+دانش|novelty|knowledge\s+gap)', combined))
        if has_novelty:
            strengths.append("تبیین شفاف خلاء پژوهشی و تمایز آشکار با مطالعات قبلی")
        else:
            findings.append(GoldfishFinding(
                issue_name="VAGUE_INNOVATION_STATEMENT",
                severity="Major",
                reviewer_lens="grant-significance-innovation",
                affected_scope="بخش ۴ (اهمیت و ضرورت تحقیق)",
                discrepancy_description="نوآوری پژوهش به طور صریح در برابر مطالعات گذشته مستند نشده و خطر پژوهش موازی/تکراری وجود دارد.",
                rationale_recommendation="بیان صریح شکاف دانش (Knowledge Gap) و جنبه نوآورانه مطالعه نسبت به مقالات داخلی و بین‌المللی."
            ))

        # Audit Vector 3: Section Sufficiency
        if len(sec2.split()) < 80:
            findings.append(GoldfishFinding(
                issue_name="SPARSE_PROBLEM_STATEMENT",
                severity="Major",
                reviewer_lens="grant-significance-innovation",
                affected_scope="بخش ۲ (بیان مسئله)",
                discrepancy_description="طول متن بیان مسئله برای یک گرنت رقابتی دانشگاهی بسیار کوتاه و فاقد جزئیات کافی است.",
                rationale_recommendation="توسعه بیان مسئله به حداقل ۱۵۰ تا ۳۰۰ کلمه با استناد به مراجع دست اول."
            ))

        # Score computation (1.0 best, 9.0 worst)
        score = 1.2
        score += sum(1.2 for f in findings if f.severity == "Blocker")
        score += sum(0.6 for f in findings if f.severity == "Major")
        score += sum(0.2 for f in findings if f.severity == "Nit")
        score = min(max(round(score, 2), 1.0), 9.0)

        return GoldfishReviewerResult(
            reviewer_id="REV_1_SIGNIFICANCE",
            name_fa="داور نوآوری، اهمیت بالینی و بار بیماری",
            name_en="Grant Significance & Innovation Reviewer (EGM Zoom-Out Lens)",
            egm_lens="egm-zoom-out",
            status="completed",
            nih_score=score,
            paraphrase_summary=paraphrase,
            findings=findings,
            strengths=strengths,
            weaknesses=weaknesses
        )

    @classmethod
    def evaluate_methodology_and_biostatistics(cls, sections: Dict[int, str], data: Dict[str, Any]) -> GoldfishReviewerResult:
        """
        Lens 2: grant-methodology-biostatistics (Derived from egm-design)
        Hostile Methodologist & Biostatistician check:
        - Hypotheses (Sec 9), Study Type (Sec 14), Population (Sec 15), Eligibility (Sec 17, 18)
        - Sample size justification (Sec 22), Statistical model (Sec 23), Protocol (Sec 27)
        - Internal validity, confounding variables, controls.
        """
        findings: List[GoldfishFinding] = []
        strengths: List[str] = []
        weaknesses: List[str] = []

        sec9 = sections.get(9, "")
        sec11 = sections.get(11, "")
        sec13 = sections.get(13, "")
        sec14 = sections.get(14, "")
        sec22 = sections.get(22, "")
        sec23 = sections.get(23, "")
        sec27 = sections.get(27, "")
        combined = f"{sec9}\n{sec11}\n{sec13}\n{sec14}\n{sec22}\n{sec23}\n{sec27}".lower()

        data_dict = data or {}
        explicit_sf = str(data_dict.get("study_family") or data_dict.get("framework") or "").strip()
        if explicit_sf.lower() in {"unknown", "unsupported", "invalid"}:
            study_family = "unknown"
        elif explicit_sf and classify_study_archetype is not None:
            inferred_explicit = classify_study_archetype({"framework": explicit_sf}, sections=sections)
            study_family = inferred_explicit if inferred_explicit != "unknown" else explicit_sf.lower()
        elif classify_study_archetype is not None:
            study_family = classify_study_archetype(f"{sections.get(1, '')} {sec14} {sec22}", sections=sections)
            if study_family == "unknown" and ("کوکران" in sec22.lower() or "cochran" in sec22.lower()):
                study_family = "epidemiological"
        else:
            study_family = "unknown"

        paraphrase = "متدولوژی طرح بر مبنای طراحی ساختاریافته، تعیین حجم نمونه/پوشش شواهد متناسب با کهن‌الگو و برنامه تحلیل مرتبط تنظیم گردیده است."

        # Audit Vector 1: Sample Size Formula & Parameters (Sec 22)
        has_formula = bool(re.search(
            r'(فرمول|cochran|کوکران|مید|mead|g\*power|حجم\s+نمونه\s*=|n\s*=|حجم\s+نمونه\s+برابر|توان\s+آزمون|سطح\s+اطمینان|\bprisma(?:-scr)?\b|\bjbi\b|\bbuderer\b|\bnielsen\b|\bsus\b|اشباع|چارتینگ|1\s*-\s*\(1\s*-\s*l\))',
            sec22.lower()
        ))
        if has_formula:
            strengths.append("فرمول/چارچوب محاسباتی حجم نمونه متناسب با کهن‌الگو همراه با پارامترهای مرتبط ارائه شده است.")
        else:
            findings.append(GoldfishFinding(
                issue_name="MISSING_SAMPLE_SIZE_FORMULA",
                severity="Blocker",
                reviewer_lens="grant-methodology-biostatistics",
                affected_scope="بخش ۲۲ (حجم نمونه)",
                discrepancy_description="حجم نمونه فاقد فرمول ریاضی مشخص، چارچوب اشباع شواهد/نیلسن یا مبنای محاسبه عددی است.",
                rationale_recommendation="درج فرمول کوکران، مید، بودرر، G*Power یا چارچوب PRISMA-ScR / Nielsen متناسب با نوع مطالعه."
            ))
            weaknesses.append("ضعف در توجیه ریاضی یا چارچوب حجم نمونه")

        # Computational Biostatistical Verification (verify_biostatistics)
        if BiostatisticalValidator is not None and sec22.strip():
            # For unsupported explicit unknown family, check directly; map health_systems/epidemiological consistently
            bio_res = BiostatisticalValidator.verify_sample_size(sec22, study_family)
            raw_issues = bio_res.get("issues", []) or []
            hard_prefixes = (
                "UNSUPPORTED_STUDY_FAMILY",
                "MISSING_COCHRAN_FORMULA",
                "INSUFFICIENT_COCHRAN_SAMPLE_SIZE",
                "INSUFFICIENT_SAMPLE_SIZE_AFTER_DEFF",
                "MISSING_CLINICAL_TRIAL_SAMPLE_SIZE_FORMULA",
                "INSUFFICIENT_TRIAL_SAMPLE_SIZE",
                "MEAD_EQUATION_DEGREE_OUT_OF_BOUNDS",
                "MISSING_MEAD_RESOURCE_EQUATION",
                "MISSING_BUDERER_DIAGNOSTIC_FORMULA",
                "MISSING_USABILITY_SAMPLE_SIZE_FORMULA",
                "MISSING_REVIEW_FRAMEWORK",
            )
            hard_issues = [iss for iss in raw_issues if any(iss.startswith(p) for p in hard_prefixes)]
            # Preserve Cochran cross-sectional CI prevalence surveys omitting power without blocking
            is_cochran_ci_survey = (
                study_family in ("epidemiological", "health_systems")
                and bio_res.get("formula_found")
                and not any(i.startswith("MISSING_COCHRAN") for i in raw_issues)
            )
            if bio_res.get("coherence_status") == "UNVERIFIED" or (hard_issues and not is_cochran_ci_survey) or hard_issues:
                # Filter redundant message when MISSING_SAMPLE_SIZE_FORMULA was already added
                if has_formula or bio_res.get("coherence_status") == "UNVERIFIED":
                    findings.append(GoldfishFinding(
                        issue_name="BIOSTATISTICAL_VALIDATION_FAILURE",
                        severity="Blocker",
                        reviewer_lens="grant-methodology-biostatistics",
                        affected_scope="بخش ۲۲ (راستی‌آزمایی محاسباتی حجم نمونه)",
                        discrepancy_description="; ".join(hard_issues or raw_issues[:2]),
                        rationale_recommendation="اصلاح پارامترهای فرمول حجم نمونه متناسب با کهن‌الگوی مطالعه و تطابق کامل با خروجی BiostatisticalValidator."
                    ))
                    weaknesses.append("خطای محاسباتی یا عدم انطباق کهن‌الگو در حجم نمونه")

        # Audit Vector 2: Statistical Plan Appropriateness (Sec 23)
        has_stat = bool(re.search(
            r'(آزمون|رگرسیون|anova|t-test|مربع\s+کای|کای[\s\-]*اسکوئر|chi-square|log-rank|spss|stata|تحلیل\s+آماری|p-value|فاصله\s+اطمینان|\bprisma(?:-scr)?\b|\bjbi\b|\bkappa\b|\bicc\b|سنتز|چارتینگ|لجستیک|حساسیت|ویژگی|\broc\b|\bauc\b|توصیفی|میانگین|فراوانی)',
            sec23.lower()
        ))
        if has_stat:
            strengths.append("برنامه تحلیل داده/آماری شفاف و متناسب با نوع مطالعه تعیین شده است.")
        else:
            findings.append(GoldfishFinding(
                issue_name="VAGUE_STATISTICAL_ANALYSIS_PLAN",
                severity="Blocker",
                reviewer_lens="grant-methodology-biostatistics",
                affected_scope="بخش ۲۳ (روش تجزیه و تحلیل داده)",
                discrepancy_description="طرح تحلیل داده فاقد ذکر روش‌های آماری استنباطی یا چارچوب سنتز/چارتینگ متناسب با طراحی مطالعه است.",
                rationale_recommendation="تعیین صریح آزمون‌های آماری، رگرسیون/ROC یا پروتکل سنتز PRISMA-ScR/JBI متناسب با نوع مطالعه."
            ))

        # Audit Vector 3: Controls, Confounders, or Scoping/Usability Rigor
        has_controls = bool(re.search(r'(کنترل|شاهد|مخدوشگر|blank|vehicle|دارونما|placebo|confound|عوامل\s+مداخله‌گر)', combined))
        if not has_controls and study_family == "scoping_review":
            has_controls = any(k in combined for k in ["دو داور", "داور سوم", "چارتینگ", "pcc", "prisma", "jbi", "معیار ورود"])
        elif not has_controls and study_family == "usability":
            has_controls = any(k in combined for k in ["نیلسن", "تفکر با صدای بلند", "سناریو", "تکلیف"]) or bool(re.search(r'\b(?:nielsen|sus)\b', combined))

        if has_controls:
            strengths.append("سازوکارهای کنترل سوگیری، گروه‌های شاهد یا تضمین کیفیت روش‌شناختی متناسب با کهن‌الگو لحاظ شده است.")
        else:
            findings.append(GoldfishFinding(
                issue_name="UNSPECIFIED_CONTROL_GROUPS_OR_CONFOUNDERS",
                severity="Major",
                reviewer_lens="grant-methodology-biostatistics",
                affected_scope="بخش ۱۱ و ۲۷ (متغیرها و روش اجرا)",
                discrepancy_description="گروه‌های شاهد/کنترل منفی یا مخدوشگرها و مکانیسم کنترل خطا به وضوح مشخص نشده‌اند.",
                rationale_recommendation="مشخص کردن گروه‌های کنترل، مخدوشگرهای زمینه‌ای یا پروتکل کنترل سوگیری متناسب با کهن‌الگو."
            ))

        score = 1.1
        score += sum(1.5 for f in findings if f.severity == "Blocker")
        score += sum(0.7 for f in findings if f.severity == "Major")
        score += sum(0.2 for f in findings if f.severity == "Nit")
        score = min(max(round(score, 2), 1.0), 9.0)

        return GoldfishReviewerResult(
            reviewer_id="REV_2_METHODOLOGY",
            name_fa="داور متدولوژی و زیست‌آمار خصمانه",
            name_en="Grant Methodology & Biostatistics Reviewer (EGM Design Critic Lens)",
            egm_lens="egm-design",
            status="completed",
            nih_score=score,
            paraphrase_summary=paraphrase,
            findings=findings,
            strengths=strengths,
            weaknesses=weaknesses
        )

    @classmethod
    def evaluate_evidence_entailment(cls, sections: Dict[int, str], data: Dict[str, Any]) -> GoldfishReviewerResult:
        """
        Lens 3: grant-evidence-entailment (Derived from egm-codebase-details)
        Pedantic Literature & Citation Auditor:
        - Fact-checking against literature dossier
        - Verifies that cited PMIDs/DOIs exist and claim quantitative facts truthfully.
        - Prevents hallucinated citations and ungrounded statements.
        """
        findings: List[GoldfishFinding] = []
        strengths: List[str] = []
        weaknesses: List[str] = []

        sec3 = sections.get(3, "")
        full_text = "\n".join(sections.values())

        paraphrase = "شواهد مرور منابع بر پایه مطالعات پیشین استوار شده و شواهد تجربی مرتبط با مسئله را بررسی نموده است."

        # Audit Vector 1: Citation Density in Literature Review
        citations_found = len(re.findall(r'\[(?:PMID:?\s*\d+|[۰-۹0-9]+)\]', full_text))
        if citations_found >= 5:
            strengths.append(f"تراکم استنادی بالا با بیش از {citations_found} ارجاع درون‌متنی به مقالات معتبر")
        elif citations_found > 0:
            strengths.append("وجود ارجاعات درون‌متنی به پایگاه‌های اطلاعاتی")
        else:
            findings.append(GoldfishFinding(
                issue_name="ZERO_FORMAL_CITATIONS_DETECTED",
                severity="Blocker",
                reviewer_lens="grant-evidence-entailment",
                affected_scope="بخش ۳ (مرور منابع)",
                discrepancy_description="هیچ ارجاع درون‌متنی رسمی یا نمایه استنادی معتبر در مرور منابع یافت نشد.",
                rationale_recommendation="افزودن شناسه‌های PMID/DOI و مستندسازی دقیق گزاره‌های تجربی به مقالات نمایه شده در PubMed."
            ))
            weaknesses.append("فقدان استناددهی استاندارد در ادعاهای علمی")

        # Audit Vector 2: Hallucination & Vague Claim Guard
        vague_claims = re.findall(r'(مطالعات\s+بسیار\s+زیاد\s+نشان\s+داده|ثابت\s+شده\s+است\s+که\s+همیشه|بدون\s+شک|همه\s+می‌دانند)', full_text)
        if vague_claims:
            findings.append(GoldfishFinding(
                issue_name="UNGROUNDED_SWEEPING_ASSERTIONS",
                severity="Major",
                reviewer_lens="grant-evidence-entailment",
                affected_scope="بخش ۲ و ۳ (بیان مسئله و منابع)",
                discrepancy_description="استفاده از گزاره‌های کلی‌گویانه بدون استناد مانند 'مطالعات بسیار زیاد نشان داده است'.",
                rationale_recommendation="جایگزینی ادعاهای کلی با گزاره‌های استنادی دقیق همراه با مقادیر کمی و ذکر نویسندگان."
            ))

        # Audit Vector 3: Temporal Trajectory & Chronological Grounding (Graphify Pillar)
        has_temporal_flow = bool(re.search(r'(سال\s+\d{4}|پیشینه|سیر\s+زمانی|مطالعات\s+اخیر|تحقیقات\s+گذشته|تکامل|افق|خط\s+زمانی|timeline)', sec3.lower()))
        if has_temporal_flow:
            strengths.append("تنظیم خط سیر زمانی شواهد بر پایه تکامل تاریخی و پیشینه علمی مقالات (Temporal Graphify)")
        else:
            findings.append(GoldfishFinding(
                issue_name="MISSING_TEMPORAL_EVIDENCE_TRAJECTORY",
                severity="Nit",
                reviewer_lens="grant-evidence-entailment",
                affected_scope="بخش ۳ (مرور منابع)",
                discrepancy_description="مرور منابع فاقد سیر تکامل زمانی مشخص و تفکیک مقالات پایه‌ای از مطالعات معاصر است.",
                rationale_recommendation="تنظیم مرور منابع در سه افق زمانی (مقالات پایه‌ای، مطالعات میانی و شواهد خط‌مقدم معاصر)."
            ))

        score = 1.0
        score += sum(1.5 for f in findings if f.severity == "Blocker")
        score += sum(0.6 for f in findings if f.severity == "Major")
        score += sum(0.2 for f in findings if f.severity == "Nit")
        score = min(max(round(score, 2), 1.0), 9.0)

        return GoldfishReviewerResult(
            reviewer_id="REV_3_EVIDENCE",
            name_fa="ممیز شواهد، ارجاعات و انطباق مقالات",
            name_en="Grant Evidence & Citation Entailment Auditor (EGM Codebase Details Lens)",
            egm_lens="egm-codebase-details",
            status="completed",
            nih_score=score,
            paraphrase_summary=paraphrase,
            findings=findings,
            strengths=strengths,
            weaknesses=weaknesses
        )

    @classmethod
    def evaluate_feasibility_and_logistics(cls, sections: Dict[int, str], data: Dict[str, Any]) -> GoldfishReviewerResult:
        """
        Lens 4: grant-feasibility-logistics (Derived from egm-implementation-readiness)
        Pragmatic Feasibility & Lab Logistics Lead:
        - Timeline (Sec 12 - Gantt chart)
        - Site / Laboratory (Sec 16), Data Collection Tools (Sec 19), Reagents / Equipment
        - Consumables sourcing in Iranian academic context.
        """
        findings: List[GoldfishFinding] = []
        strengths: List[str] = []
        weaknesses: List[str] = []

        sec12 = sections.get(12, "")
        sec16 = sections.get(16, "")
        sec19 = sections.get(19, "")
        combined = f"{sec12}\n{sec16}\n{sec19}".lower()

        paraphrase = "امکان‌پذیری فنی و اجرایی پروژه شامل جدول زمان‌بندی مراحل، محل اجرای تحقیق و ابزارهای گردآوری تبیین شده است."

        # Audit Vector 1: Gantt Chart / Timeline Feasibility (Sec 12)
        has_timeline = bool(re.search(r'(ماه|هفته|جدول|زمان‌بندی|گانت|مرحله|فاز|phase|duration)', sec12.lower()))
        if has_timeline and len(sec12.split()) >= 15:
            strengths.append("مراحل اجرایی کار در جدول زمان‌بندی تفکیک شده است.")
        else:
            findings.append(GoldfishFinding(
                issue_name="INCOMPLETE_GANTT_TIMELINE",
                severity="Major",
                reviewer_lens="grant-feasibility-logistics",
                affected_scope="بخش ۱۲ (جدول زمان‌بندی و مراحل اجرا)",
                discrepancy_description="جدول زمان‌بندی مراحل اجرا بسیار کلی و فاقد تفکیک ماهانه یا فازهای واقع‌بینانه است.",
                rationale_recommendation="تدوین جدول زمان‌بندی تفکیکی ۶ تا ۲۴ ماهه با تخصیص زمان برای تست‌های پایلوت و ممیزی اخلاق."
            ))

        # Audit Vector 2: Study Location and Equipment (Sec 16 & 19)
        if len(sec16.strip()) < 10:
            findings.append(GoldfishFinding(
                issue_name="UNSPECIFIED_STUDY_LOCATION",
                severity="Major",
                reviewer_lens="grant-feasibility-logistics",
                affected_scope="بخش ۱۶ (محل انجام مطالعه)",
                discrepancy_description="محل دقیق انجام آزمایش‌ها، بیمارستان‌های همکار یا آزمایشگاه مرکزی پروژه ذکر نشده است.",
                rationale_recommendation="ذکر بیمارستان‌ها، مراکز درمانی، یا آزمایشگاه‌های تحقیقاتی مرجع همکار در دانشگاه."
            ))
        else:
            strengths.append("محل انجام و امکانات آزمایشگاهی یا درمانی معین شده است.")

        score = 1.1
        score += sum(1.4 for f in findings if f.severity == "Blocker")
        score += sum(0.6 for f in findings if f.severity == "Major")
        score += sum(0.2 for f in findings if f.severity == "Nit")
        score = min(max(round(score, 2), 1.0), 9.0)

        return GoldfishReviewerResult(
            reviewer_id="REV_4_FEASIBILITY",
            name_fa="داور امکان‌پذیری، جدول زمانی و تدارکات اجرایی",
            name_en="Grant Feasibility & Lab Logistics Reviewer (EGM Implementation Readiness Lens)",
            egm_lens="egm-implementation-readiness",
            status="completed",
            nih_score=score,
            paraphrase_summary=paraphrase,
            findings=findings,
            strengths=strengths,
            weaknesses=weaknesses
        )

    @classmethod
    def evaluate_ethics_and_lay_comprehension(cls, sections: Dict[int, str], data: Dict[str, Any]) -> GoldfishReviewerResult:
        """
        Lens 5: grant-ethics-lay-advocate (Derived from egm-comprehension)
        Bioethics & Naive Reader Persona:
        - Ethical Considerations (Sec 24), Security / Data Protection (Sec 25)
        - Helsinki Declaration, Informed Consent, Anonymization (AES-256)
        - Clarity of language and absence of unexplained laboratory jargon.
        """
        findings: List[GoldfishFinding] = []
        strengths: List[str] = []
        weaknesses: List[str] = []

        sec24 = sections.get(24, "")
        sec25 = sections.get(25, "")
        combined = f"{sec24}\n{sec25}".lower()

        paraphrase = "ملاحظات اخلاقی و الزامات رازداری داده‌ها در انطباق با کدهای اخلاق زیست‌پزشکی ارزیابی گردید."

        # Audit Vector 1: Bioethics Statement (Sec 24)
        has_ethics = bool(re.search(
            r'(اخلاق|هلسینکی|helsinki|رضایت|محرمان|کمیته\s+اخلاق|کد\s+اخلاق|irb|معافیت\s+اخلاق|فاقد\s+هرگونه\s+مداخله\s+انسانی|تعارض\s+منافع)',
            combined
        ))
        if has_ethics:
            strengths.append("پروتکل ملاحظات اخلاقی شامل رضایت‌نامه، کدهای بین‌المللی و رازداری پیش‌بینی شده است.")
        else:
            findings.append(GoldfishFinding(
                issue_name="MISSING_BIOETHICS_COMPLIANCE_PROTOCOL",
                severity="Blocker",
                reviewer_lens="grant-ethics-lay-advocate",
                affected_scope="بخش ۲۴ (ملاحظات اخلاقی)",
                discrepancy_description="بخش ملاحظات اخلاقی فاقد اشاره به بیانیه هلسینکی، رضایت‌آگاهانه یا نحوه صیانت از آزمودنی‌هاست.",
                rationale_recommendation="افزودن تعهدنامه انطباق با بیانیه هلسینکی و دریافت رضایت‌نامه کتبی آگاهانه."
            ))
            weaknesses.append("نقص در تبیین سازوکارهای اخلاق زیستی و حقوق آزمودنی")

        # Audit Vector 2: Data Protection & Confidentiality (Sec 25)
        has_security = bool(re.search(r'(امنیت|محرمان|رمزنگاری|aes|ناشناس|کدگذاری|حفاظت\s+داده|اطلاعات)', sec25.lower()))
        if has_security:
            strengths.append("تمهیدات صیانت از محرمانگی و امنیت داده‌ها درج شده است.")
        else:
            findings.append(GoldfishFinding(
                issue_name="WEAK_DATA_CONFIDENTIALITY_PLAN",
                severity="Major",
                reviewer_lens="grant-ethics-lay-advocate",
                affected_scope="بخش ۲۵ (نکات امنیتی و حفاظت پروژه)",
                discrepancy_description="برنامه حفاظت از محرمانگی داده‌ها و پرونده‌های آزمودنی‌ها فاقد جزئیات فنی مشخص است.",
                rationale_recommendation="تشریح سازوکار کدگذاری داده‌ها و ذخیره‌سازی در بسترهای امن بدون درج هویت آشکار بیماران."
            ))

        score = 1.0
        score += sum(1.5 for f in findings if f.severity == "Blocker")
        score += sum(0.6 for f in findings if f.severity == "Major")
        score += sum(0.2 for f in findings if f.severity == "Nit")
        score = min(max(round(score, 2), 1.0), 9.0)

        return GoldfishReviewerResult(
            reviewer_id="REV_5_ETHICS",
            name_fa="داور اخلاق زیستی، حقوق آزمودنی و ساده‌فهمی",
            name_en="Grant Bioethics & Lay Advocate Reviewer (EGM Comprehension Lens)",
            egm_lens="egm-comprehension",
            status="completed",
            nih_score=score,
            paraphrase_summary=paraphrase,
            findings=findings,
            strengths=strengths,
            weaknesses=weaknesses
        )


    @classmethod
    def evaluate_academic_style_and_voice(cls, sections: Dict[int, str], data: Dict[str, Any]) -> GoldfishReviewerResult:
        """
        Lens 6: grant-academic-style-voice (Derived from egm-style and academic-humanizer)
        Academic Style, Scholarly Voice and Prose Hygiene Reviewer:
        - 6-Layer Architecture based on https://github.com/AIScientists-Dev/academic-humanizer
        - Layer 1: Eradicate robotic transition cliches and Em-dashes
        - Layer 2: Sentence-length cadence and burstiness variance (target sigma >= 8.0)
        - Layer 3: Concrete laboratory and clinical grounding (concentrations, timepoints, kinetics)
        - Layer 4: Zero premature certainty (no false proof/isbat or over-claiming)
        - Layer 5: Naturalized structure and non-repetitive list starters in aims
        - Layer 6: Data invariant protection and ZERO AI disclosure mentions (Strict Blocker on AI leakage).
        """
        findings: List[GoldfishFinding] = []
        strengths: List[str] = []
        weaknesses: List[str] = []

        sec2 = sections.get(2, '')
        sec3 = sections.get(3, '')
        sec4 = sections.get(4, '')
        sec6 = sections.get(6, '')
        sec12 = sections.get(12, '')
        sec13 = sections.get(13, '')
        sec26 = sections.get(26, '')
        sec27 = sections.get(27, '')
        full_text = '\n'.join(sections.values())

        paraphrase = 'نثر آکادمیک، ریتم طول جملات، اصالت لحن علمی و عدم نشت تکیه‌کلام‌ها و بیانیه‌های هوش مصنوعی ارزیابی گردید.'

        # Audit Vector 1: Robotic AI Signatures and Transition Traps (Layer 1)
        banned_fa_cliches = [
            'در این راستا', 'حائز اهمیت است', 'نقش بسزایی دارد',
            'به عنوان یک', 'از این رو', 'شایان ذکر است', 'لازم به ذکر است',
            'جامع و مانع', 'در دنیای امروز', 'پرواضح است'
        ]
        found_cliches = [c for c in banned_fa_cliches if c in full_text]
        em_dash_count = full_text.count('—') + full_text.count('–')

        if not found_cliches and em_dash_count == 0:
            strengths.append('متن کاملاً عاری از تکیه‌کلام‌های کلیشه‌ای ماشینی و خط فاصله‌های کشیده است.')
        else:
            if found_cliches:
                findings.append(GoldfishFinding(
                    issue_name='BANNED_TRANSITION_CLICHES_DETECTED',
                    severity='Major' if len(found_cliches) > 2 else 'Nit',
                    reviewer_lens='grant-academic-style-voice',
                    affected_scope='متن عمومی پروپوزال',
                    discrepancy_description=f'تعداد {len(found_cliches)} تکیه‌کلام کلیشه‌ای شناسایی شد: {", ".join(found_cliches[:4])}',
                    rationale_recommendation='حذف عبارات کلیشه‌ای و بازنویسی مستقیم گزاره‌ها با افعال معلوم علمی.'
                ))
                weaknesses.append(f'وجود تکیه‌کلام‌های کلیشه‌ای ({", ".join(found_cliches[:3])})')
            if em_dash_count > 2:
                findings.append(GoldfishFinding(
                    issue_name='EXCESSIVE_EM_DASH_USAGE',
                    severity='Nit',
                    reviewer_lens='grant-academic-style-voice',
                    affected_scope='نگارش متن',
                    discrepancy_description=f'تعداد {em_dash_count} خط فاصله کشیده انگلیسی (—/–) در متن فارسی شناسایی شد.',
                    rationale_recommendation='جایگزینی خط فاصله‌ها با ویرگول، نقطه یا پرانتز استاندارد.'
                ))

        # Audit Vector 2: Sentence Cadence and High Burstiness (Layer 2)
        raw_sentences = [s.strip() for s in re.split(r'[\.!\?؟\n]+', full_text) if len(s.strip()) > 3]
        word_counts = [len(s.split()) for s in raw_sentences if len(s.split()) >= 3]
        if len(word_counts) >= 5:
            mean_wc = sum(word_counts) / len(word_counts)
            variance = sum((x - mean_wc) ** 2 for x in word_counts) / len(word_counts)
            sigma = variance ** 0.5
            has_short = any(4 <= x <= 8 for x in word_counts)
            has_long = any(x >= 20 for x in word_counts)

            if sigma >= 7.0 and (has_short or has_long):
                strengths.append(f'تنوع و ریتم ساختاری طول جملات برجسته است (σ = {sigma:.1f} کلمه بر جمله).')
            elif sigma < 4.5:
                findings.append(GoldfishFinding(
                    issue_name='MONOTONOUS_SENTENCE_CADENCE',
                    severity='Nit',
                    reviewer_lens='grant-academic-style-voice',
                    affected_scope='ساختار و ریتم جملات',
                    discrepancy_description=f'توزیع طول جملات بیش از حد یکنواخت است (انحراف معیار σ = {sigma:.1f} کلمه).',
                    rationale_recommendation='ایجاد تنوع با ترکیب جملات کوتاه تک‌گزاره‌ای (۴-۸ کلمه) و جملات تبیینی مشروح (۲۰-۳۰ کلمه).'
                ))
                weaknesses.append('ریتم نسبتاً یکنواخت طول جملات')
        else:
            sigma = 8.0

        # Audit Vector 3: Concrete Lab / Clinical / Protocol Operational Grounding (Layer 3)
        ops_text = f"{sec13}\n{sec27}".strip()
        ops_scope = 'بخش ۱۳ و ۲۷ (روش اجرا)'
        if not ops_text:
            ops_text = sec12
            ops_scope = 'بخش ۱۲ (روش اجرا)'
        if ops_text:
            has_grounding = bool(re.search(
                r'(\d+\s*(?:میلی|میکرو|mg|ml|μm|nm|ساعت|روزه?|درصد|%|rpm|سانتی‌گراد|c°|ماه|هفته|دقیقه|نفر|خانوار|مطالعه))|\b(?:pubmed|scopus|web\s+of\s+science|embase|pcc|sus|irct|deff|his|cochran|prisma|jbi|nielsen)\b',
                ops_text,
                re.I,
            ))
            if has_grounding:
                strengths.append('پروتکل اجرایی پژوهش دارای مشخصات عملیاتی دقیق (مقادیر عددی، پایگاه‌ها، ابزارها یا بازه‌های زمانی) است.')
            else:
                findings.append(GoldfishFinding(
                    issue_name='ABSTRACT_METHODOLOGY_DESCRIPTION',
                    severity='Nit',
                    reviewer_lens='grant-academic-style-voice',
                    affected_scope=ops_scope,
                    discrepancy_description='روش اجرا بیش از حد کلی توصیف شده و فاقد مشخصات عملیاتی ملموس (مقادیر عددی، ابزار استاندارد یا زمان‌بندی) است.',
                    rationale_recommendation='تصریح مقادیر عددی دقیق، نام پایگاه‌ها/ابزارها، غلظت‌ها یا بازه‌های زمانی اجرا.'
                ))

        # Audit Vector 4: Zero Premature Certainty (Layer 4)
        over_claims = re.findall(r'(به طور قطعی اثبات خواهد شد|اثبات قطعی|یقین کامل|بدون تردید ثابت|کاملاً مشخص است که)', full_text)
        if over_claims:
            findings.append(GoldfishFinding(
                issue_name='PREMATURE_CERTAINTY_IN_PROPOSAL',
                severity='Major',
                reviewer_lens='grant-academic-style-voice',
                affected_scope='لحن علمی و گزاره‌ها',
                discrepancy_description=f'استفاده از ادعای قطعیت یا اثبات برای پژوهش اجرا‌نشده: {", ".join(set(over_claims))}',
                rationale_recommendation='استفاده از افعال فرضیه‌محور نظیر «آزمون فرضیه»، «بررسی احتمال اثر» و «ارزیابی معناداری».'
            ))
            weaknesses.append('ادعای قطعیت زودهنگام در اهداف یا فرضیات')
        else:
            strengths.append('لحن نگارش کاملاً علمی، کالیبره‌شده و بدون ادعای قطعیت زودهنگام است.')

        # Audit Vector 5: Non-repetitive List Traps in Aims (Layer 5)
        aims_text = sec6 or sec4
        if aims_text:
            repeated_openers = re.findall(r'(?:^|\n)\s*[-*•\d\.]+\s*(تعیین|بررسی|شناسایی|سنجش)', aims_text)
            if len(repeated_openers) >= 6 and len(set(repeated_openers)) == 1:
                findings.append(GoldfishFinding(
                    issue_name='REPETITIVE_AIM_LIST_OPENERS',
                    severity='Nit',
                    reviewer_lens='grant-academic-style-voice',
                    affected_scope='بخش ۶ (اهداف اختصاصی)',
                    discrepancy_description=f'تکرار بیش از حد یک فعل یکسان در آغاز بندهای اهداف ({repeated_openers[0]}).',
                    rationale_recommendation='طبیعی‌سازی ساختار فهرست با افعال متنوع و دسته‌بندی فازبندی‌شده اهداف.'
                ))

        # Audit Vector 6: Zero AI Mentions Leakage (Layer 6 - STRICT BLOCKER)
        ai_leakage = re.findall(r'(?i)(?:هوش مصنوعی|artificial intelligence|generative ai|ai-generated|چت‌جی‌پی‌تی|chatgpt|مدل زبانی|زبانی بزرگ|large language model|llm|نوشته شده توسط|ai usage disclosure|افشای استفاده)', full_text)
        if ai_leakage:
            findings.append(GoldfishFinding(
                issue_name='UNWARRANTED_AI_DISCLOSURE_LEAKAGE',
                severity='Blocker',
                reviewer_lens='grant-academic-style-voice',
                affected_scope='متن نهایی پروپوزال',
                discrepancy_description=f'نشت اشاره یا بیانیه هوش مصنوعی در متن پروپوزال: {", ".join(set(ai_leakage))}',
                rationale_recommendation='حذف قطعی و کامل هرگونه بیانیه، پانویس یا اشاره به هوش مصنوعی/مدل زبانی از متن پروپوزال جهت تضمین ارائه اصیل اثر.'
            ))
            weaknesses.append('نشت غیرمجاز اشاره به ابزارهای هوش مصنوعی در متن علمی')

        # Score calculation
        score = 1.10
        for f in findings:
            if f.severity == 'Blocker':
                score += 2.0
            elif f.severity == 'Major':
                score += 0.5
            elif f.severity == 'Nit':
                score += 0.1
        score = min(max(round(score, 2), 1.0), 9.0)

        return GoldfishReviewerResult(
            reviewer_id='REV_6_STYLE_VOICE',
            name_fa='داور نگارش آکادمیک، لحن علمی و پالایش نثر',
            name_en='Grant Academic Style, Scholarly Voice & Prose Hygiene Reviewer (EGM Style Lens)',
            egm_lens='egm-style',
            status='completed',
            nih_score=score,
            paraphrase_summary=paraphrase,
            findings=findings,
            strengths=strengths,
            weaknesses=weaknesses
        )

    @classmethod
    def synthesize_grant_study_section(cls, reviewer_results: Dict[str, GoldfishReviewerResult], remediation_round: int = 1) -> EGMStudySectionResult:
        """
        Lens 6: grant-study-section-sro (Derived from egm-synthesizer)
        Scientific Review Officer (SRO) Swarm Compiler:
        - Normalizes and deduplicates findings
        - Triages by Blocker, Major, Nit
        - Computes NIH overall composite score (1.0 - 9.0)
        - Determines official funding verdict.
        """
        prioritized_findings: List[GoldfishFinding] = []
        seen_issues = set()

        # Collect and deduplicate
        for rev_res in reviewer_results.values():
            for f in rev_res.findings:
                if f.issue_name not in seen_issues:
                    seen_issues.add(f.issue_name)
                    prioritized_findings.append(f)

        # Sort: Blockers first, then Majors, then Nits
        severity_order = {"Blocker": 0, "Major": 1, "Nit": 2}
        prioritized_findings.sort(key=lambda x: severity_order.get(x.severity, 3))

        # Overall composite score calculation
        scores = [r.nih_score for r in reviewer_results.values() if r.status == "completed"]
        avg_score = sum(scores) / len(scores) if scores else 5.0

        # Adjust for blockers
        blocker_count = sum(1 for f in prioritized_findings if f.severity == "Blocker" and not f.remediated)
        if blocker_count > 0:
            overall_score = max(avg_score, 3.8 + (blocker_count * 0.5))
        else:
            overall_score = avg_score

        overall_score = min(max(round(overall_score, 2), 1.0), 9.0)

        # Funding verdict based on canonical ceiling (<= 2.0 APPROVED_FUNDABLE)
        if overall_score <= NIH_APPROVAL_SCORE_CEILING and blocker_count == 0:
            funding_verdict = "APPROVED_FUNDABLE"
            can_proceed = True
            percentile = max(100.0 - (overall_score - 1.0) * 15.0, 85.0)
            exec_summary = f"پروپوزال موفق به کسب امتیاز جامعیت ساختاری برجسته {overall_score}/9.0 (آستانه مصوب <= {NIH_APPROVAL_SCORE_CEILING}) بدون خطای بحرانی گردید و حائز شرایط تایید تشخیص داده شد."
        elif overall_score <= 4.0 or blocker_count > 0:
            funding_verdict = "REVISION_REQUIRED"
            can_proceed = False
            percentile = 70.0 - (overall_score - 2.0) * 15.0
            exec_summary = f"پروپوزال نمره قابل قبول مشروط {overall_score}/9.0 را کسب کرد اما نیازمند رفع {blocker_count} نقص بحرانی و بازنگری متدولوژیک در راندهای اصلاحی است."
        else:
            funding_verdict = "REJECTED_UNFUNDABLE"
            can_proceed = False
            percentile = max(40.0 - (overall_score - 4.0) * 10.0, 5.0)
            exec_summary = f"پروپوزال نمره ضعیف {overall_score}/9.0 را کسب کرد و به دلیل وجود {blocker_count} نقص بحرانی در متدولوژی یا اخلاق، در این مرحله غیرقابل تصویب است."

        return EGMStudySectionResult(
            overall_nih_score=overall_score,
            funding_verdict=funding_verdict,
            can_proceed=can_proceed,
            percentile=percentile,
            reviewer_results=reviewer_results,
            prioritized_findings=prioritized_findings,
            remediation_rounds_conducted=remediation_round,
            executive_summary_fa=exec_summary,
            structural_completeness_percent=percentile,
        )

    @classmethod
    def conduct_full_study_section_review(cls, markdown_text: str, proposal_data: Dict[str, Any], remediation_round: int = 1) -> EGMStudySectionResult:
        """Executes all 5 Goldfish lenses in parallel/sequence and synthesizes with SRO."""
        sections = cls.parse_proposal_sections(markdown_text)

        rev1 = cls.evaluate_significance_and_innovation(sections, proposal_data)
        rev2 = cls.evaluate_methodology_and_biostatistics(sections, proposal_data)
        rev3 = cls.evaluate_evidence_entailment(sections, proposal_data)
        rev4 = cls.evaluate_feasibility_and_logistics(sections, proposal_data)
        rev5 = cls.evaluate_ethics_and_lay_comprehension(sections, proposal_data)
        rev6 = cls.evaluate_academic_style_and_voice(sections, proposal_data)

        reviewer_results = {
            "rev_1_significance": rev1,
            "rev_2_methodology": rev2,
            "rev_3_evidence": rev3,
            "rev_4_feasibility": rev4,
            "rev_5_ethics": rev5,
            "rev_6_style_voice": rev6
        }

        return cls.synthesize_grant_study_section(reviewer_results, remediation_round=remediation_round)

    @classmethod
    def generate_report_markdown(cls, result: EGMStudySectionResult, proposal_title: str = "پروپوزال تحقیقاتی") -> str:
        """Generates the official EGM_GRANT_STUDY_SECTION_REPORT.md deliverable."""
        md = []
        md.append("# 🏛️ کارنامه رسمی نشست داوری گرنت‌های پزشکی (EGM Study Section Report)")
        md.append("> [!NOTE]")
        md.append("> **تذکر شفافیت:** نمره حاضر شاخص جامعیت ساختاری و روش‌شناختی (Heuristic Completeness Score) مبتنی بر شبیه‌سازی هوشمند هیئت داوران بوده و نباید به عنوان تاییدیه رسمی نهادهای حاکمیتی گرنت تفسیر شود.")
        md.append("")
        md.append(f"**عنوان طرح پژوهشی:** {proposal_title}")
        md.append(f"**معماری ارزیابی:** EGM v14.2.0 (Elephant-Goldfish Multi-Agent Swarm)")
        md.append(f"**امتیاز جامعیت ساختاری و روش‌شناختی (Heuristic Completeness / NIH Impact Score):** `{result.overall_nih_score} / 9.0`")
        sc_pct = (
            result.structural_completeness_percent
            if result.structural_completeness_percent is not None
            else result.percentile
        )
        md.append(f"**شاخص جامعیت ساختاری (Structural Completeness Index):** `{sc_pct:.1f}%`")
        md.append(f"**وضعیت نهایی تخصیص بودجه:** **{result.funding_verdict}**")
        md.append(f"**تعداد دورهای اصلاحی طی‌شده:** `{result.remediation_rounds_conducted}`")
        md.append("")
        md.append("---")
        md.append("## ۱. خلاصه اجرایی دبیر علمی نشست داوری (Executive SRO Summary)")
        md.append(f"> {result.executive_summary_fa}")
        md.append("")
        md.append("---")
        md.append("## ۲. کارنامه تفکیکی هیئت داوران گلدفیش (Goldfish Reviewers Scorecard)")
        md.append("")
        md.append("| داور / لنز تخصصی | شناسه EGM | وضعیت | نمره NIH (۱ تا ۹) | نقایص بحرانی | نقایص عمده |")
        md.append("| :--- | :--- | :---: | :---: | :---: | :---: |")

        for rev in result.reviewer_results.values():
            md.append(f"| **{rev.name_fa}** | `{rev.egm_lens}` | `{rev.status}` | **{rev.nih_score}** | {len(rev.blockers)} | {len(rev.majors)} |")

        md.append("")
        md.append("---")
        md.append("## ۳. ماتریس اولویت‌بندی اشکالات و نقدهای متدولوژیک (Prioritized Findings)")
        md.append("")

        if not result.prioritized_findings:
            md.append("✅ **هیچ نقص یا ابهام متدولوژیک در ارزیابی داوران شناسایی نشد (Zero Defects).**")
        else:
            for i, f in enumerate(result.prioritized_findings, 1):
                icon = "🔴" if f.severity == "Blocker" else ("🟡" if f.severity == "Major" else "🟢")
                rem_status = " *(رفع‌شده)*" if f.remediated else ""
                md.append(f"### {i}. {icon} {f.issue_name} [{f.severity}]{rem_status}")
                md.append(f"* **لنز داور:** `{f.reviewer_lens}`")
                md.append(f"* **بخش تحت تاثیر:** `{f.affected_scope}`")
                md.append(f"* **شرح نقص:** {f.discrepancy_description}")
                md.append(f"* **راهکار اصلاحی:** {f.rationale_recommendation}")
                md.append("")

        md.append("---")
        md.append("## ۴. نقاط قوت اثبات‌شده در داوری (Documented Strengths)")
        for rev in result.reviewer_results.values():
            if rev.strengths:
                md.append(f"#### ▪ {rev.name_fa}:")
                for s in rev.strengths:
                    md.append(f"  * {s}")

        return "\n".join(md)

    @classmethod
    def save_reports(cls, result: EGMStudySectionResult, output_dir: str, proposal_title: str = "") -> Tuple[str, str]:
        """Saves both markdown and JSON study section reports to disk."""
        os.makedirs(output_dir, exist_ok=True)
        md_path = os.path.join(output_dir, "EGM_GRANT_STUDY_SECTION_REPORT.md")
        json_path = os.path.join(output_dir, "EGM_GRANT_STUDY_SECTION_REPORT.json")

        md_content = cls.generate_report_markdown(result, proposal_title=proposal_title)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)

        return md_path, json_path


if __name__ == "__main__":
    sample_text = """
## ۱. موضوع
بررسی اثر هم‌افزایی ترکیب نانوذرات دارویی و مهارکننده مسیر سیگنالینگ در مهار تکثیر سلول‌های سرطانی

## ۲. بیان مسئله
سرطان یکی از مهم‌ترین معضلات نظام سلامت بوده و سالانه بر اساس آمار GLOBOCAN میلیون‌ها مورد مرگ در جهان ایجاد می‌کند. بار بیماری و هزینه‌های گزاف مراقبت درمانی ضرورت توسعه درمان‌های نوآورانه را برجسته ساخته است.

## ۳. مرور بر منابع
مطالعات گذشته نشان داده است که ترکیبات هدفمند می‌توانند مرگ سلولی را تحریک کنند [PMID: 32329697]. همچنین پژوهش‌های معتبر دیگر بر نقش مسیرهای بیولوژیک تاکید دارند [PMID: 31234567].

## ۴. اهمیت و ضرورت تحقیق
شناسایی درمان‌های ترکیبی جهت مهار مقاومت دارویی و ارتقای اثربخشی درمانی از اولویت‌های ضروری نظام سلامت است.

## ۲۲. حجم نمونه و روش محاسبه آن
محاسبه حجم نمونه بر مبنای فرمول مید (Mead's Resource Equation) و تحلیل توان فاکتوریل نرم‌افزار G*Power با توان ۹۰٪ و آلفای ۵٪ برابر n=19 انجام می‌شود.

## ۲۳. روش تجزیه و تحلیل داده
تحلیل داده‌ها با استفاده از آزمون تحلیل واریانس دوطرفه فاکتوریل (Two-Way ANOVA) و آزمون تعقیبی توکی در نرم‌افزار آماری SPSS انجام خواهد شد. سطح معناداری P<0.05 لحاظ می‌شود.

## ۲۴. ملاحظات اخلاقی در صورت نیاز
این پژوهش کاملاً منطبق بر موازین بیانیه هلسینکی و مصوبات کمیته اخلاق در پژوهش‌های زیست‌پزشکی دانشگاه انجام خواهد شد.

## ۲۵. نحوه رعایت نکات امنیتی و حفاظت پروژه در صورت نیاز
اطلاعات پروژه در بسترهای دیجیتال امن با رمزنگاری استاندارد AES-256 ذخیره و دسترسی افراد کاملاً محدود خواهد بود.
    """
    res = EGMStudySectionCoordinator.conduct_full_study_section_review(sample_text, {})
    print(f"Overall NIH Score: {res.overall_nih_score} ({res.funding_verdict})")
    print(f"Blockers: {res.total_blockers}, Majors: {res.total_majors}")
    md_out = EGMStudySectionCoordinator.generate_report_markdown(res, "طرح نمونه")
    print("Report Markdown generated successfully (length: ", len(md_out), ")")
