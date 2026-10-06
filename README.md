# Proposal-Nevisi 🔬📄
### Universal Evidence-Driven Medical Research, Modular Architecture & Adversarial Verification Engine (v9.0)
### موتور ماژولار و جامع سنتز شواهد، راستی‌آزمایی خصمانه و نگارش پروپوزال‌های پژوهشی علوم پزشکی (نسخه ۹.۰)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Unified Tests: 350/350 Passed](https://img.shields.io/badge/Unified%20Tests-350%2F350%20Passed-success.svg)](#unified-multi-tier-test-harness)
[![Mutation Testing: 100%](https://img.shields.io/badge/Mutation%20Score-100%25%20Killed-success.svg)](#unified-multi-tier-test-harness)
[![Master Release Gate: 43/43 Passed](https://img.shields.io/badge/Master%20Gate-43%2F43%20Passed-success.svg)](#master-release-gate-43-criteria)
[![Pajooheshyar 28 Sections Compliant](https://img.shields.io/badge/Pajooheshyar-28%20Sections%20Complete-teal.svg)](#layer-2-structural-compliance)
[![Native OMML Equations](https://img.shields.io/badge/DOCX%20Math-Native%20OMML%20XML-purple.svg)](#layer-4-formatting--typesetting)
[![Architecture: Topic-Agnostic](https://img.shields.io/badge/Architecture-Topic--Agnostic%20Core-blueviolet.svg)](#universal-architecture)

---

> **Language / زبان:** [English](#english) | [فارسی](#فارسی)

---

<a name="english"></a>
## English Documentation

**Proposal-Nevisi (v9.0)** is an autonomous, publication-grade academic research proposal drafting framework and **Topic-Agnostic Research-Grade Medical Literature & Proposal Engine**. Built upon foundational architectures from AIPOCH (`aipoch/medical-research-skills`), K-Dense (`K-Dense-AI/claude-scientific-writer`), and the SciFact claim-evidence framework (AllenAI / Wadden et al.), **v9.0 introduces a 4-Layer Modular Architecture** that replaces rigid, topic-specific heuristics with fully generalized, fail-closed adversarial verification components.

It operates seamlessly across diverse biomedical disciplines—including **Oncology**, **Cardiology**, **Infectious Diseases**, **Molecular Diagnostics**, **Epidemiology**, **Endocrinology**, **Nephrology**, **Regenerative Medicine / Biomaterials**, **Occupational Toxicology**, **Pediatric Pulmonology**, and **Basic Molecular / Cellular Science**.

> **Pre-Generation Readiness Guarantee:** Proposal generation is strictly governed by `ProposalReadinessGate`. If any module fails verification, generation is aborted immediately with a diagnostic error report.

---

### v9.0 Four-Layer Modular Architecture

```
+-----------------------------------------------------------------------------------+
|                        ProposalReadinessGate (Master Gatekeeper)                  |
+-----------------------------------------------------------------------------------+
        |                                                                   |
        v                                                                   v
+---------------------------------------+   +---------------------------------------+
|    LAYER 1: SCIENTIFIC ACCURACY       |   |    LAYER 2: STRUCTURAL COMPLIANCE     |
| • BiologicalMechanismVerifier         |   | • MethodologyCompletenessGate (28)    |
| • CombinationHypothesisEngine         |   | • CombinationModelSelector (ANOVA/GLM)|
| • CompoundEntityNormalizer            |   | • Mandatory Sample Size Formula Box   |
+---------------------------------------+   +---------------------------------------+
        |                                                                   |
        v                                                                   v
+---------------------------------------+   +---------------------------------------+
|    LAYER 3: CITATION INTEGRITY        |   |   LAYER 4: FORMATTING & TYPESETTING   |
| • CitationTracker                     |   | • NativeOmmlMathEngine (LaTeX->OMML)  |
| • Strict Vancouver Order of Appearance|   | • PersianMedicalTypographyLinter      |
| • Orphaned Claim & Unused Ref Auditor |   | • YAML Rules & First-Mention Expansion|
+---------------------------------------+   +---------------------------------------+
```

#### Layer 1: Scientific Accuracy
1. **Adversarial Biological Mechanism Verifier (`scripts/biological_mechanism_adversarial_verifier.py`):**
   - Implements a structured biomedical ontology of apoptosis and cell cycle regulators (Bcl-2, Bcl-xL, Bax, Bak, Caspases 3/7/8/9, p53, AKT, PTEN, etc.).
   - Catches biological role inversions (e.g. claiming Bcl-xL is pro-apoptotic or Bax is anti-apoptotic) returning `CONTRADICTED` and blocking flawed mechanistic statements.
2. **Combination Hypothesis Engine (`scripts/combination_hypothesis_engine.py`):**
   - Automatically generates dual, parallel hypotheses for co-treatment studies: $H_1$ (Synergism) and $H_2$ (Antagonism / Additive effect).
   - Computes an `evidence_balance_score` and triggers `POSITIVE_EVIDENCE_DOMINANCE_WARNING` when only positive synergy claims are present without negative/neutral evidence.
3. **Compound Entity Normalizer (`scripts/compound_entity_normalizer.py`):**
   - Classifies substances into standardized ontological tiers: `PURE_COMPOUND`, `STANDARDIZED_EXTRACT`, `CRUDE_EXTRACT`, `SYNTHETIC_ANALOG`.
   - Prevents the crude extract attribution fallacy (e.g., claiming whole-plant extract effects as isolated constituent properties without purity specifications).

#### Layer 2: Structural Compliance
4. **Pajooheshyar 28-Section Methodology Completeness Gate (`scripts/methodology_completeness_gate.py`):**
   - Strictly enforces all 28 mandatory sections required by the official Iranian Biomedical Research Information System (Pajooheshyar / Ministry of Health).
   - Enforces a mandatory mathematical sample size formula (Cohen's $d$, Mead's Resource Equation $E = N - B - T$, or Cochran's formula) in Section 10; missing formulas completely block compilation.
5. **Combination Model Selector (`scripts/combination_model_selector.py`):**
   - Selects scientifically valid statistical models based on study design and factor structures (e.g., Two-Way Factorial ANOVA with explicit interaction term $A \times B$, Repeated Measures ANOVA, or Cox Proportional Hazards).
   - Generates statistical assumption checks (Shapiro-Wilk, Levene's test) and appropriate post-hoc tests (Tukey HSD / Bonferroni).

#### Layer 3: Citation Integrity
6. **Unified Citation Tracker (`scripts/citation_tracker.py`):**
   - Enforces strict Vancouver numeric style strictly by order of appearance.
   - Detects orphaned claims (text making substantive factual claims without reference markers) and unused references (sources registered in the bibliography but never cited).
   - Re-indexes citations dynamically if the narrative structure is altered.

#### Layer 4: Formatting & Typesetting
7. **Native OMML Word Math Engine (`scripts/native_omml_math_engine.py`):**
   - Converts LaTeX formulas into standard Office Math Markup Language (`<m:oMath>`, `<m:oMathPara>`) via MathML, with clean Unicode text fallback.
   - Completely eliminates raw LaTeX code, delimiters (`$...$`, `\[...\]`), and markup leakage in generated Microsoft Word `.docx` documents.
8. **Persian Medical Typography Linter (`scripts/persian_medical_typography_linter.py` & `scripts/typography_rules.yaml`):**
   - Configuration-driven typography engine enforcing Zero-Width Non-Joiner (ZWNJ, `\u200c`) for Persian affixes (`می‌`, `ها`, `تر`).
   - Normalizes digits in Persian prose to Persian numerals while protecting scientific formulas, units, and citation keys.
   - Automatically expands first mentions of medical abbreviations (e.g. `NDV` -> `ویروس بیماری نیوکاسل (Newcastle Disease Virus; NDV)`).

---

<a name="master-release-gate-43-criteria"></a>
### Master Release Gate (43 Production Criteria)

The engine enforces 43 non-negotiable release criteria verified on every build:
1. `MAX_FINAL_REFERENCES == 25` (Hard Ceiling)
2. `NO_QUOTA_FILLING == True` (Zero Artificial Padding)
3. `GENERIC_EXCLUSION_ONTOLOGY` (16 Topic-Agnostic Categories)
4. Two-Stage Screening & Citation Integrity Engine
5. `SEARCH_DATABASE_STATUSES` (8 Standardized Statuses)
6. `RESEARCH_PIPELINE_STAGES` (7 Standard Phases)
7. `GENERIC_CONTRADICTION_ROOT_CAUSES` (14 Generic Root Causes)
8. `HIGH_VALUE_SCORING_WEIGHTS` (10 Dimensions Normalized)
9. `SELECTION_ORDER_PRIORITIES` (9 Strict Tiers)
10. Universal Entity Hierarchy (13 Types) & Evidence Roles (10 Roles)
11. Bounded Search Gap Policy ("Absence of Evidence != Evidence of Absence")
12. Anti-Hardcoding Static Leakage Audit (31/31 Scripts Zero Leakage)
13. Portfolio Audit with Decoupled Search Pool and Ceiling Enforcement
14. 7-Point Structured Literature Synthesis Narrative Engine
15. `SEARCH_FAMILIES_ONTOLOGY` (16 Query Families) & MeSH Mapper
16. Citation Chasing Engine (Backward, Forward, Lateral) with Provenance
17. Seed Paper Discovery Engine (8 Categories & Non-Automatic Inclusion)
18. Evidence-Based Saturation Tracker (7 Dimensions & False Saturation Guard)
19. Structured Paper Reader (4 Tracks & 18 Deterministic Fields)
20. Paper-to-Claim Verifier (6 Citation Drift Types & Entailment Verdicts)
21. Enhanced Triple-Check Deduplication & Identifier Canonicalization
22. Reproducible Research Run Manifest & SHA-256 Checksum
23. Research Recall Benchmark & Diagnostic Taxonomy (13 Failure Modes)
24. Deep Reading 5-Section Architecture & Figure-First Visual Review
25. 8-Tier Evidence Hierarchy & Confidence Evaluation
26. Paper-to-Claim Verification 2.0 (8-Stage Pipeline & 13 Issues)
27. Post-Research Citation Auditor (Placeholders & Unused References)
28. Adaptive Database Selector & Negative Evidence Scanner
29. Canonical Paper Evidence Record (16 Fields & Location Provenance)
30. Numeric Provenance Gate (Anti-Numeric Hallucination & Exact Extraction)
31. Contextual Boundary Gate (11 Boundary Mismatches & Leap Prevention)
32. Exact Claim-to-Evidence Mapper (SciFact-Aligned 5-Tier Claim Verdicts)
33. Evidence-Driven Paragraph Builder (Anti-Boilerplate & Null/Negative Surfacing)
34. Strict Claim-to-Citation Binding & Literature Review Gate
35. `CompoundEntityNormalizer` (Pure/Extract/Analogue Classification & Mismatch Guard)
36. `BiologicalMechanismAdversarialVerifier` (Apoptosis & Cell Cycle Role Inversion Guard)
37. `CombinationHypothesisEngine` (Dual Hypotheses & Evidence Balance Verification)
38. `CombinationModelSelector` (Factorial ANOVA, Interaction Terms & Model Taxonomy)
39. `MethodologyCompletenessGate` (28 Pajooheshyar Sections Schema & Sample Size Gate)
40. `CitationTracker` (Vancouver Order, Orphaned Claims & Unused Reference Auditor)
41. `NativeOmmlMathEngine` (Native Word OMML Equations & LaTeX DOCX Elimination)
42. `PersianMedicalTypographyLinter` (YAML Rules, ZWNJ, Persian Numerals & Medical Expansions)
43. `ProposalReadinessGate` (Fail-Closed Master Verification Across All 8 v9.0 Modules)

---

<a name="unified-multi-tier-test-harness"></a>
### Unified Multi-Tier Test Harness (`scripts/master_release_gate.py`)

The engine includes a master test harness verifying 350 total software assertions across 13 independent test suites:
- **Suite 1: Static Analysis Hard-Code Leakage Audit (`test_hard_code_leakage.py`):** Asserts 0 hard-coded biological entities across all 31 core generic scripts (31 tests - **PASS**).
- **Suite 2: Multi-Domain Generalization Suite (`test_generalization.py`):** Validates execution across 12 distinct biomedical fixtures (12 tests - **PASS**).
- **Suite 3: Adversarial Stress Scenarios & Negative Rejection Tests (`test_adversarial_scenarios.py`):** 114 stress tests evaluating swappable search backends, deduplication, saturation curves, relevance gates, 25-reference ceiling, 14-factor scoring, screening funnels, DOI conflicts, retracted papers, calendar cutoffs, leap years, causal overclaims, synergy fallacies (114 tests - **PASS**).
- **Suite 4: Tri-Tier Benchmark Audit (`self_audit_suite.py`):** 60 behavioral and scientific assertions on the benchmark proposal (60 tests - **PASS**).
- **Suite 5: Mutation Testing Layer (`test_mutations.py`):** 10 deliberate scientific defect mutations with 100% kill score (10 tests - **PASS**).
- **Suite 6: Property-Based Invariants & JSON Schemas (`test_property_and_schemas.py`):** 14 tests validating Invariants 1–8 and Draft-07 JSON Schemas (14 tests - **PASS**).
- **Suite 7: End-to-End Pipeline & Integration Scenarios (`test_e2e_integration.py`):** 24 tests validating full pipeline execution and adversarial failure/demotion scenarios (24 tests - **PASS**).
- **Suite 8: Cross-Topic Adversarial Test Suite (`test_cross_topic_adversarial.py`):** 11 tests verifying topic-agnosticism across Scenarios A through J (11 tests - **PASS**).
- **Suite 9: Advanced Research Engine Integration (`test_advanced_research_engine.py`):** 22 tests verifying multi-source federated search, citation chasing, and claim verification (22 tests - **PASS**).
- **Suite 10: Deep Reading & Recall Benchmark Suite (`test_v86_deep_reading_and_recall_benchmark.py`):** 14 tests verifying recall benchmarking, 13-category search miss taxonomy, 5-section deep reading, figure-first evidence recovery, methods reverse-engineering, 8-tier evidence hierarchy, paper-to-claim verifier 2.0, post-research citation auditing, and thematic comparative synthesis (14 tests - **PASS**).
- **Suite 11: Evidence Grounding & Semantic Attribution Integrity Suite (`test_v87_evidence_grounding_and_attribution.py`):** 14 tests validating Canonical Paper Evidence Records, numeric provenance, contextual boundary gates, SciFact claim-evidence mapping, anti-boilerplate paragraph generation, and claim-to-citation binding (14 tests - **PASS**).
- **Suite 12: Real-World Evidence Remediation Regressions (`test_v87_remediation_regressions.py`):** 10 tests validating complete architectural prevention of off-target intervention leakage, derivative/extract conflation, non-human model mismatches, template placeholder leaks, and quota filling (10 tests - **PASS**).
- **Suite 13: v9.0 Adversarial Stress & Modular Architecture Suite (`test_v90_adversarial.py`):** 14 adversarial stress tests deliberately testing mechanism inversion detection, positive evidence bias warnings, crude extract normalization, missing sample size formula blocks, complex OMML equation rendering, Vancouver re-ordering, orphaned claim detection, and fail-closed readiness gatekeeping (14 tests - **PASS**).

```bash
# Run the master production release gate
python scripts/master_release_gate.py
```

---

<a name="فارسی"></a>
## مستندات فارسی

مهارت **Proposal-Nevisi (نسخه v9.0)** یک پلتفرم جامع، تعاملی، کاملاً ماژولار، مستقل از موضوع (Topic-Agnostic) و مبتنی بر شواهد برای تدوین پروپوزال‌های پژوهشی علوم پزشکی و زیست‌پزشکی در بالاترین تراز دانشگاهی است. نسخه ۹.۰ منطق‌های شرطی و وابسته به موضوع را به طور کامل حذف کرده و معماری ماژولار ۴ لایه‌ای زیر را ارائه می‌دهد:

### لایه‌های معماری v9.0:

1. **لایه ۱: صحت علمی (Scientific Accuracy):**
   - **راستی‌آزمای خصمانه مکانیسم‌های بیولوژیک (`BiologicalMechanismAdversarialVerifier`):** کشف و مسدودسازی وارونگی نقش پروتئین‌ها (نظیر انتساب نقش پیش‌آپوپتوزی به Bcl-xL یا ضدآپوپتوزی به Bax).
   - **موتور فرضیات ترکیب درمانی (`CombinationHypothesisEngine`):** تولید خودکار دو فرضیه موازی هم‌افزایی ($H_1$) و عدم هم‌افزایی/تضاد ($H_2$)، ارزیابی تعادل شواهد و هشدار سوگیری شواهد مثبت (`POSITIVE_EVIDENCE_DOMINANCE_WARNING`).
   - **نرمال‌ساز هویت مواد (`CompoundEntityNormalizer`):** دسته‌بندی مواد در سطوح استاندارد ماده خالص، عصاره استاندارد، عصاره خام و آنالوگ سنتزی با جلوگیری از تعمیم نادرست اثرات عصاره گیاهی به ترکیب خالص.

2. **لایه ۲: تطابق ساختاری (Structural Compliance):**
   - **گیت جامعیت ۲۸ بخشی پژوهشیار (`MethodologyCompletenessGate`):** اعتبارسنجی کامل ۲۸ بخش رسمی سامانه اطلاعات تحقیقاتی پزشکی کشور (پژوهشیار / وزارت بهداشت) با الزامی بودن فرمول ریاضی محاسبه حجم نمونه (کوهن، مید، کوکران).
   - **انتخاب‌گر مدل آماری ترکیبی (`CombinationModelSelector`):** تعیین خودکار آنالیز واریانس عاملی دوطرفه با ترم اثر متقابل ($A \times B$)، آزمون‌های پیش‌فرض و آزمون‌های تعقیبی متناسب با ساختار آزمایش.

3. **لایه ۳: تمامیت استنادها (Citation Integrity):**
   - **ره‌گیر یکپارچه استنادات (`CitationTracker`):** بازشماری و مرتب‌سازی ارجاعات بر اساس ترتیب ظهور در متن (ونکور استاندارد)، کشف گزاره‌های بی‌رفرنس (Orphaned Claims) و رفرنس‌های استفاده‌نشده (Unused References).

4. **لایه ۴: فرمت‌بندی و تایپوگرافی (Formatting & Typesetting):**
   - **موتور فرمول‌نویسی بومی ورد (`NativeOmmlMathEngine`):** تبدیل کدهای LaTeX به فرمول‌های استاندارد OMML ورد (`<m:oMath>`) و حذف ۱۰۰٪ نشت کدهای لاتک (`$...$`) از سند DOCX.
   - **لینتر تایپوگرافی پزشکی فارسی (`PersianMedicalTypographyLinter`):** اصلاح خودکار نیم‌فاصله‌ها (ZWNJ)، تبدیل ارقام در متن فارسی به اعداد فارسی و باز کردن خودکار اختصارات انگلیسی در نخستین اشاره.

5. **گیت یکپارچه‌ساز آمادگی (`ProposalReadinessGate`):**
   - سد بازدارنده (Fail-Closed) که تا پیش از تأیید سلامت و انطباق تمامی ۸ ماژول فوق، اجازه کامپایل نهایی هیچ پروپوزالی را صادر نمی‌کند.

---

## مجوز (License)
این پروژه تحت مجوز [MIT License](LICENSE) منتشر شده است.
