# Proposal-Nevisi 🔬📄
### Universal Evidence-Driven Medical Research, Cognitive Multi-Agent Architecture & Autonomous Proposal Pipeline (v11.4.1)
### موتور خودکار و جامع پژوهش زیست‌پزشکی، معماری چندایجنت شناختی و تدوین پروپوزال‌های علوم پزشکی (نسخه ۱۱.۴.۱)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Unified Tests: 479/479 Passed](https://img.shields.io/badge/Unified%20Tests-479%2F479%20Passed-success.svg)](#unified-multi-tier-test-harness)
[![Master Release Gate: 43/43 Passed](https://img.shields.io/badge/Master%20Gate-43%2F43%20Passed-success.svg)](#master-release-gate-43-criteria)
[![Pajooheshyar 28 Sections Compliant](https://img.shields.io/badge/Pajooheshyar-28%20Sections%20Complete-teal.svg)](#layer-2-structural-compliance)
[![Native OMML Equations](https://img.shields.io/badge/DOCX%20Math-Native%20OMML%20XML-purple.svg)](#layer-4-formatting--typesetting)
[![Architecture: Cognitive Multi-Agent](https://img.shields.io/badge/Architecture-Cognitive%20Multi--Agent-blueviolet.svg)](#cognitive-multi-agent-architecture)
[![Closed-Loop Critic-Refine](https://img.shields.io/badge/Closed--Loop-Iterative%20Remediation-orange.svg)](#iterative-remediation-engine)
[![ARA Seal Level 2: Epistemic Rigor](https://img.shields.io/badge/Epistemic%20Rigor-6D%20Audited-green.svg)](#epistemic-rigor-auditor)

---

> **Language / زبان:** [English Documentation](#english) | [مستندات فارسی](#فارسی)

---

<a name="english"></a>
## English Documentation (v11.4.1)

**Proposal-Nevisi (v11.4.1)** is an autonomous, publication-grade academic research proposal drafting framework and **Topic-Agnostic Research-Grade Medical Literature & Proposal Engine**. Built upon foundational architectures from AIPOCH (`aipoch/medical-research-skills`), K-Dense (`K-Dense-AI/claude-scientific-writer`), and the SciFact claim-evidence framework (AllenAI / Wadden et al.), **v11.4.1 introduces the Two-Stage Cognitive Multi-Agent Architecture (`Pre-Draft Specialist Subagents -> PROPOSAL_SPEC.json` + `Post-Draft Blind Adversarial Reviewer Loop`), Organ-Specific GLOBOCAN 2022 Checksums, and 13-Pillar Adversarial Review Immunization**.

It completely eliminates AI literature hallucination, Frankenstein/chimera methodology stitching, cross-cancer epidemiology overfitting, DOI digit drift, biostatistical sample-size drift, and abstract-only truncation through an immutable research dossier, cohesive methodology subagents, live Crossref/PubMed verification, iterative surgical patching, and post-draft blind grant peer review.

---

### End-to-End System Architecture & 4-Subagent Closed-Loop Flow

```mermaid
flowchart TD
    subgraph Stage1 ["۱. مرحله اول: ۲ ساب‌ایجنت تخصصی پیش از نگارش (Stage 1: Parallel Pre-Draft Subagents)"]
        A["کاربر: عنوان پژوهش به فارسی + کلیدواژه‌های انگلیسی"] --> B["MeSHQueryExpander<br>• نگاشت به سرعنوان‌های MeSH<br>• فیلتر ۱۰۰٪ کاراکترهای غیرلاتین"]
        B --> S1["ساب‌ایجنت ۱: ارزیابی کمی شواهد (Evidence & Quantitative RCS Subagent)<br>• جستجوی چندمرحله‌ای PubMed / Europe PMC / OpenAlex<br>• امتیازدهی PaperQA2 RCS (0-10) و استخراج مقادیر کمی (IC50, p-value)<br>• آمار اختصاصی ارگان هدف در GLOBOCAN 2022 + تدوین farsi_synthesis_summary"]
        B --> S2["ساب‌ایجنت ۲: متدولوژی ضد کیمرا (Methodology & Anti-Chimera Subagent)<br>• انتخاب مطالعه مرجع اصلی (Primary Anchor Protocol)<br>• پروفایل ژنتیکی و محیط کشت ATCC اختصاصی مدل + جدول متغیرهای بخش ۱۱<br>• قفل ریاضی حجم نمونه (N=30, B=2, T=9, E=19) با تحلیل توان G*Power"]
        S1 & S2 --> SPEC["ادغام عمیق بدون اتلاف در فایل مشخصات طرح<br>PROPOSAL_SPEC.json (--spec-file Deep-Merge)"]
    end

    subgraph InnerLoop ["۲. حلقه بهینه‌سازی درونی: استخراج، ادغام و پلمپ شواهد (Inner Loop)"]
        SPEC --> D["ScientificSearchAdapter + حفظ کامل مقالات ساب‌ایجنت"]
        D --> D1["NCBI PubMed (E-Search, E-Summary, E-Fetch XML)"]
        D --> D2["Europe PMC & OpenAlex REST API"]
        D1 & D2 --> E["FullTextRetrievalEngine (واکشی متن کامل JATS XML)"]
        E --> F["LiveDoiCrossrefVerifier (ممیزی برخط DOI در Crossref)"]
        F --> G["Quantitative Grounding + MethodologyResearchSubagent Wiring"]
        G --> H["پلمپ تغییرناپذیر پرونده پژوهش<br>PROPOSAL_RESEARCH_DOSSIER.json / .md<br>(ARA Seal Level 2 - ممیزی ۶ بعدی)"]
    end

    subgraph OuterLoop ["۳. حلقه نگارش بیرونی: تدوین ۲۸ بخش پژوهشیار (Outer Loop)"]
        H --> I["ProposalGenerator (موتور تدوین ۲۸ بخشی)"]
        I --> J1["بخش ۲: بیان مسئله + آمار GLOBOCAN 2022 اختصاصی ارگان هدف"]
        I --> J2["بخش ۳: مرور منابع + شاخص‌های کمی اختصاصی هر مقاله + جدول ToxRTool فارسی"]
        I --> J3["بخش ۱۱ و ۱۵: جدول کامل متغیرها (همگام با بخش ۶) + شناسنامه ژنتیکی ATCC"]
        I --> J4["بخش ۲۲: حجم نمونه همگام (N=30, B=2, E=19) + پارامتر غیرمرکزی λ=10.1 در G*Power"]
        I --> J5["بخش ۲۷ و ۲۸: پروتکل دو فازی چو-تالالای + منابع انگلیسی با ارقام استاندارد"]
    end

    subgraph RemediationLoop ["۴. چرخه بسته داوری نمادین و اصلاح جراحی تا ۱۰ راند (Symbolic Critic-Refine Loop — Max 10 Rounds)"]
        J1 & J2 & J3 & J4 & J5 --> R1["MockGrantReviewPanel (داوری ۳ داور تخصصی NIH 1-9)"]
        R1 --> R2{"آیا نیاز به اصلاح دارد؟<br>(Flaws > 0 یا نمره > 2.0)"}
        R2 -- "بله (نقص بحرانی یا ضعف ساختاری)" --> R3["IterativeRemediationEngine<br>• پچ جراحی تمام ۱۵+ نقص داوران ۱، ۲ و ۳<br>• اصلاح پیوسته تا سقف ۱۰ راند (DEFAULT_MAX_ITERATIONS=10)"]
        R3 --> R1
        R2 -- "خیر (اجماع کامل نمادین)" --> DRAFT["تولید پیش‌نویس کامل ۲۸ بخشی<br>proposal.md"]
    end

    subgraph Stage2 ["۵. مرحله دوم: ۲ ساب‌ایجنت ممیز پس از نگارش در حلقه بسته تا ۱۰ راند (Stage 2: Post-Draft Subagents)"]
        DRAFT --> CIT["ساب‌ایجنت ۳: ممیز استنادات و اعداد (Citation & Claim-Span Verifier)<br>• تطبیق تک‌تک استنادات [n] در بخش ۲ و ۳ با چکیده واقعی منبع در بخش ۲۸<br>• کشف هرگونه خطای انتساب (Citation Drift) یا عدد فاقد پشتوانه"]
        DRAFT --> BLIND["ساب‌ایجنت ۴: داور کور گرنت (Post-Draft Blind Adversarial Reviewer)<br>• مطالعه خط‌به‌خط فایل واقعی proposal.md در تمام ۲۸ بخش<br>• ممیزی تطابق بیولوژیک، اپیدمیولوژیک و آماری بین بخش‌های ۶، ۱۱، ۱۳، ۱۹، ۲۲ و ۲۷"]
        CIT & BLIND --> BCHECK{"تایید هر دو ساب‌ایجنت ممیز؟<br>(0 خطای علمی / 0 خطای استنادی)"}
        BCHECK -- "خیر (کشف خطای معنایی/استنادی - تا ۱۰ راند)" --> BPATCH["اصلاح جراحی PROPOSAL_SPEC.json و بازتولید"]
        BPATCH --> I
        BCHECK -- "بله (APPROVED_FUNDABLE)" --> L["Master Release Gate (۴۳ معیار کنترل کیفیت)"]
    end

    subgraph Artifacts ["۶. اسناد نهایی تولیدشده (Final Output Artifacts)"]
        L --> M1["proposal.docx (سند ورد با فرمول‌های بومی OMML)"]
        L --> M2["proposal.md (متن کامل ۲۸ بخشی)"]
        L --> M3["PROPOSAL_RESEARCH_DOSSIER (پلمپ پرونده شواهد)"]
        L --> M4["MOCK_GRANT_REVIEW & REVISION_AUDIT_TRAIL"]
    end
```

---

### Benchmark Comparison: Frontier AI Deep Research & GitHub Scientific Skills

Full primary-source benchmark details are documented in [`docs/DEEP_RESEARCH_BENCHMARK_AND_SUBAGENT_ARCHITECTURE.md`](docs/DEEP_RESEARCH_BENCHMARK_AND_SUBAGENT_ARCHITECTURE.md).

| Architecture / Framework | Core Paradigm | Key Strength Adopted in `proposal-nevisi` |
| :--- | :--- | :--- |
| **Anthropic Claude Multi-Agent Research** | Lead Orchestrator + Parallel Subagents + Dedicated `CitationAgent` | Two-Stage 4-Subagent split with a dedicated **Post-Draft Citation & Claim-Span Verifier Subagent** |
| **OpenAI ChatGPT (o3) Deep Research** | ReAct Browsing + Python Code Execution + Backtracking | Live multi-database retrieval + deterministic Python biostatistical & Crossref verification |
| **Perplexity Deep Research** | Iterative Query Decomposition + Multi-Hop Retrieval | 16-layer MeSH Boolean query expansion + negative search log (`0 hits` proof) |
| **FutureHouse `PaperQA2`** | Gather $\rightarrow$ RCS Score (0–10) $\rightarrow$ Quote-Grounded Cite | Quantitative passage & pathway extraction (`IC50`, doses, $p$-values) + `farsi_synthesis_summary` preservation |
| **Sakana AI `AI-Scientist-v2`** | Multi-Round Automated Peer Review + Reflexion | Closed-loop **10-iteration** symbolic + subagent remediation (`DEFAULT_MAX_ITERATIONS = 10`) |
| **Stanford `STORM` / `Co-STORM`** | Multi-Perspective Persona Questioning | 3-Reviewer NIH Study Section (Scientific Premise, Methodology/Biostatistics, Bioethics/Biosafety) |
| **K-Dense `claude-scientific-writer` & AIPOCH** | Structured IMRaD/Grant Templates + PICO/EQUATOR | 28-section Pajooheshyar completeness + ARRIVE 2.0 / MIQE / ToxRTool / Native Word OMML |

---

### 10-Pillar Adversarial Review Immunization Matrix (v11.4.1)

```mermaid
flowchart LR
    subgraph Flaws ["نقایص رصدشده در داوری‌های خارجی"]
        F1["لغزش ارقام انتهای DOI"]
        F2["خطای چک‌سام آمار جهانی GLOBOCAN"]
        F3["اعمال اشتباه RoB-2 بالینی روی سلول"]
        F4["خلط معادله مید با توان آماری (B=1)"]
        F5["جهش مستقیم به ترکیب چو-تالالای"]
        F6["محیط‌های کشت سلولی جنریک"]
        F7["ادعای گزاف کیهانی نوآوری"]
        F8["اکتفا به mRNA کاسپاز ۳ برای مرگ"]
        F9["برون‌یابی سلولی به سمیت بالینی"]
        F10["تعمیم یک رده سلولی به کل بیماری"]
    end

    subgraph Pillars ["۱۰ ستون ایمن‌سازی ساختاری در نسخه v11.4.1"]
        P1["استعلام زنده Crossref و تطابق عنوانی > 40%"]
        P2["ثبت دقیق ۲,۴۸۰,۳۰۱ ابتلا و ۱,۸۱۷,۱۷۲ مرگ (Bray 2024)"]
        P3["سنجش اختصاصی برون‌تن با ابزار ToxRTool / NTP OHAT"]
        P4["درجات آزادی بلوک B=2, E=19 + تحلیل توان فاکتوریل G*Power"]
        P5["پروتکل دو فازی: منحنی تک‌دارویی قبل از محاسبه CI"]
        P6["تطابق با شناسنامه رسمی ATCC (مانند F-12K / EMEM)"]
        P7["مقیدسازی ادعای نوآوری به استراتژی رسمی سرچ منفی (0 Hits)"]
        P8["سنجش کاسپاز ۳ فعال (Cleaved) و فلوسایتومتری Annexin V/PI"]
        P9["مهار برون‌یابی داده‌های برون‌تن به بالین بیمار"]
        P10["تبیین ناهمگونی ژنتیکی رده سلولی (وضعیت KRAS و p53)"]
    end

    F1 --> P1
    F2 --> P2
    F3 --> P3
    F4 --> P4
    F5 --> P5
    F6 --> P6
    F7 --> P7
    F8 --> P8
    F9 --> P9
    F10 --> P10
```

---

### Key Architectural Pillars in v11.4.1:

1. **Two-Loop Autonomous Cognitive Architecture:**
   - **Inner Optimization Loop (Research & Grounding):** Executes live literature discovery across PubMed and Europe PMC, retrieves full-text JATS XML, extracts verbatim grounded passages, detects cross-study contradictions, and immutably seals findings into `PROPOSAL_RESEARCH_DOSSIER.json` and `.md`.
   - **Outer Synthesis Loop (Proposal Drafting):** Synthesizes all 28 canonical sections required by Iranian biomedical universities (Pajooheshyar format), strictly bound to the sealed dossier without parametric memory hallucination.
2. **Methodology Research Subagent (`scripts/methodology_research_subagent.py`):**
   - **Anti-Chimera Protocol Engine:** Prevents the critical failure mode where AI stitches incompatible protocol details from disparate studies. Enforces cohesive protocols aligned with OECD GCCP (Good Cell Culture Practice), MIQE guidelines for RT-qPCR (mandating dual reference genes, e.g., GAPDH + ACTB), and photometric interference mitigation (Cell-Free Blank & 570/630 nm spectrophotometry for tetrazolium/MTT assays).
   - **Biostatistical Coherence ($B=2, E=19$):** Resolves degrees of freedom contradictions by enforcing Mead's Resource Equation ($E = N - B - T = 30 - 2 - 9 = 19 \in [10, 20]$ for 3 independent replicate days) coupled with independent G*Power Factorial ANOVA power analysis ($1 - \beta = 85.2\%$).
3. **Live Crossref DOI Title Verification (`scripts/generic_reference_auditor.py`):**
   - Connects in real-time to `api.crossref.org/works/{doi}`.
   - Calculates title sequence similarity; if similarity < 40%, emits `CRITICAL_DOI_MISMATCH` and rejects drifted DOIs.
4. **100% Academic Persian Synthesis (`synthesize_findings_persian`):**
   - Eradicates raw English sentence leakage in Section 3 (Literature Review) by transforming biomedical actions (inhibition, apoptosis, ROS modulation, migration, viability) into high-register Persian scholarly prose.
5. **Adversarial Mock Grant Study Section (`scripts/mock_grant_review_panel.py`):**
   - **Reviewer 1 (Scientific Significance & Semantic Drift):** Audits model drift (ensuring unrelated tissue data is not attributed to target models), verifies updated GLOBOCAN 2022/2024 epidemiology (2,480,301 cases, 1,817,172 deaths), and mandates a formal negative Boolean search strategy log (`0 hits`) to substantiate novelty claims.
   - **Reviewer 2 (Methodology & Biostatistics):** Verifies replicate design (biological vs technical), sample size mathematical justification, cell-free blank interference controls, and 2-phase Chou-Talalay curves.
   - **Reviewer 3 (Bioethics & Biosafety):** Audits Iranian 31-Principle Biomedical Ethics Code and BSL-2 compliance.
6. **Native Word OMML Equations (`scripts/native_omml_math_engine.py`):**
   - Converts LaTeX formulas directly into Microsoft Word native Office Math Markup Language (`<m:oMath>`), eliminating raw LaTeX leakage in `.docx` files.
7. **Persian Medical Typography Linter (`scripts/persian_medical_typography_linter.py`):**
   - Strictly enforces Persian Zero-Width Non-Joiner (ZWNJ), Persian numerals in prose, and bilingual expansion for medical acronyms on first mention.

---

### Quick Start / CLI Usage

Run the master autonomous research pipeline:

```powershell
uv run python scripts/run_research_pipeline.py --topic "Your Biomedical Research Topic in Persian" --keywords "Agent1, Agent2, Target Condition" --output-dir "./output"
```

#### Example Invocation:
```powershell
uv run python scripts/run_research_pipeline.py `
  --topic "مقایسه اثر همزمان فوکوئیدان با پمترکسد بر مهار رشد سلول‌های سرطان ریه" `
  --keywords "Fucoidan, Pemetrexed, Non-Small Cell Lung Carcinoma" `
  --study-family "in_vitro" `
  --output-dir "./output"
```

#### Generated Artifacts:
- `proposal.docx`: Publication-grade Microsoft Word proposal with native OMML formulas, styled tables, and zero duplicate headings.
- `proposal.md`: Complete 28-section Markdown proposal.
- `PROPOSAL_RESEARCH_DOSSIER.json` & `.md`: Sealed immutable evidence records with full-text passages and audit logs.
- `MOCK_GRANT_REVIEW_REPORT.md` & `.json`: Grant panel score and detailed critique.
- `REVISION_AUDIT_TRAIL.md` & `.json`: Closed-loop iterative surgical remediation audit trail across all reviewer rounds.
- `EQUATOR_COMPLIANCE_AUDIT.md` & `.json`: ARRIVE 2.0 / MIQE compliance scorecards.
- `RISK_OF_BIAS_MITIGATION_REPORT.md` & `.json`: ToxRTool / NTP OHAT / RoB-2 domain assessments.

---

<a name="master-release-gate-43-criteria"></a>
### Master Release Gate (43 Production Criteria)

The engine enforces 43 fail-closed release criteria before approving proposals:
1. Static analysis leakage audit: 0 hardcoded biological entities in core scripts (`test_hard_code_leakage.py`).
2. Single source of truth version synchronization (`VERSION`, `project_metadata.json`, `core_policies.py`).
3. Two-Loop Research Dossier immutability and pass/fail sealing.
4. 28 canonical Pajooheshyar section completeness.
5. Mandatory mathematical sample size formulas (Mead's Equation, Cohen's $d$, Cochran).
6. 100% Native OMML XML generation without raw LaTeX delimiter leakage.
7. 100% Vancouver citation re-indexing by appearance order.
8. Zero tolerance for orphaned claims or unreferenced citations.

---

<a name="unified-multi-tier-test-harness"></a>
### Unified Multi-Tier Test Harness

The engine includes 24 comprehensive test suites with **477 / 477 tests passing (100% Pass Rate)**:

```powershell
uv run python tests/run_all_tests.py
```

- **Suite 1: Static Analysis Hard-Code Leakage Audit (`test_hard_code_leakage.py`)** - 42 tests verifying zero hardcoded entities.
- **Suite 2: Two-Loop Dossier & Master Pipeline Suite (`test_two_loop_dossier.py`)** - E2E verification of research dossier, epistemic auditor, and orchestrator.
- **Suite 3: Multi-Domain Generalization Suite (`test_generalization.py`)** - Validates across 12 distinct biomedical domains.
- **Suite 4: Adversarial Stress Scenarios & Negative Rejection Tests (`test_adversarial_scenarios.py`)** - 114 stress tests.
- **Suite 5: Mutation Testing Layer (`test_mutations.py`)** - 10 deliberate scientific defects with 100% kill score.
- **Suite 6: v11.4.1 Adversarial Immunization Suite (`test_v114_adversarial_immunization.py`)** - 11 tests verifying DOI Crossref verification, ToxRTool quality assessment, GLOBOCAN checksums, Mead degrees of freedom, and Chou-Talalay two-phase protocol.
- **Suite 7: Closed-Loop Iterative Remediation Suite (`test_iterative_remediation_engine.py`)** - 3 tests auditing surgical section patching, multi-round convergence, and fail-closed consensus gating.
- **Suites 8–24:** Property invariants, schema audits, EQUATOR compliance, RoB-2 mitigation, OMML math engines, typography linters, and Pillar 1-5 hardening.

---

<a name="فارسی"></a>
## مستندات فارسی (نسخه ۱۱.۴.۱)

پلتفرم **پروپوزال‌نویسی (Proposal-Nevisi نسخه ۱۱.۴.۱)** یک سیستم خودکار، پیشرفته، شناختی و مبتنی بر شواهد واقعی (Evidence-Driven) برای تدوین پروپوزال‌های پژوهشی علوم پزشکی، داروسازی، دندان‌پزشکی و زیست‌پزشکی مطابق با استاندارد رسمی معاونت پژوهشی و سامانه **پژوهشیار** است.

نسخه ۱۱.۴.۱ با ادغام **معماری ساب‌ایجنت‌های شناختی (Cognitive Multi-Agent Architecture)**، **موتور چرخه بسته داوری و اصلاح پیوسته (Closed-Loop Critic-Refine Remediation)**، **ایمن‌سازی ده‌گانه در برابر ممیزی داوران خارجی (10-Pillar Adversarial Immunization)**، **استعلام زنده Crossref API** و **حذف کامل نشت متن انگلیسی در پیشینه پژوهش**، کلیه خطاهای متدولوژیک و بیواستاتیک را به صورت قطعی ریشه‌کن کرده است.

---

### قابلیت‌های کلیدی و نوین نسخه ۱۱.۴.۱:

1. **موتور چرخه بسته داوری و اصلاح پیوسته (`IterativeRemediationEngine`):**
   - جایگزینی داوری تک‌مرحله‌ای باز (Open-Loop) با لوپ بسته بازخورد و اصلاح پیوسته (تا ۵ راند).
   - پچ‌کردن جراحی بخش‌های آسیب‌دیده با `SurgicalSectionPatcher` بدون دستکاری سایر بخش‌های تاییدشده.
   - اعمال فیوز توقف قطعی (Fail-Closed Circuit Breaker) در صورت عدم احراز نمره ممتاز (< 2.0) و عدم تایید اجماعی هیئت داوران.
   - ثبت شفاف کارنامه حسابرسی اصلاحات در `REVISION_AUDIT_TRAIL.md` و `.json`.
2. **استعلام برخط شناسه‌های DOI و ممیزی عنوان مقاله (`LiveDoiCrossrefVerifier`):**
   - اتصال مستقیم به سرورهای رسمی Crossref جهت راستی‌آزمایی عنوان مقاله در برابر شناسه ثبت‌شده.
   - ممانعت قطعی از خطای لغزش ارقام انتهای DOI (تطابق رشته عنوان با آستانه تشابه حداقل ۴۰٪ و صدور خطای بحرانی در صورت مغایرت).
3. **سنتز ۱۰۰٪ فارسی و آکادمیک بخش ۳ (مرور منابع):**
   - استقرار متد `synthesize_findings_persian` جهت ترجمه و سنتز مفهومی افعال و مکانیزم‌های زیستی (مهار رشد، آپوپتوز، استرس اکسیداتیو، مهاجرت سلولی، مقاومت دارویی).
   - حذف کامل نشت عناوین یا جملات خام انگلیسی در گیومه‌ها.
4. **همسویی دقیق بیواستاتیک در معادله مید ($B=2, E=19$):**
   - محاسبه دقیق درجات آزادی اثر بلوک‌بندی آزمایشگاهی برای ۳ روز کاری مستقل ($B = k_{\text{blocks}} - 1 = 3 - 1 = 2$).
   - انطباق درجات آزادی خطای آزمون با بازه استاندارد جهانی ($E = 30 - 2 - 9 = 19 \in [10, 20]$).
   - تفکیک قطعی معادله مید از تحلیل مستقل توان آزمون ANOVA دوطرفه در G*Power با توان ۸۵.۲٪ ($1 - \beta = 0.852$).
5. **جایگزینی RoB-2 بالینی با ابزار استاندارد سلولی ToxRTool / NTP OHAT:**
   - حذف خطای اعمال ابزار کارآزمایی بالینی انسانی (Cochrane RoB-2) روی مطالعات کشت سلولی آزمایشگاهی.
   - ارزیابی ۵ دامنه اختصاصی سمیت و زیستایی برون‌تن (مستندسازی ماده، خلوص، شرایط آزمون، اعتبار بیولوژیک و پایایی).
6. **چک‌سام دقیق آمار رسمی سرطان GLOBOCAN 2022/2024:**
   - الزام به ثبت دقیق ارقام مرجع بین‌المللی جدول Bray et al. 2024 در CA Cancer J Clin (۲,۴۸۰,۳۰۱ مورد ابتلا و ۱,۸۱۷,۱۷۲ مورد مرگ).
7. **پروتکل دو فازی برهم‌کنش دارویی چو-تالالای (Chou-Talalay 2-Phase Protocol):**
   - الزام به رسم منحنی ۵ تا ۷ نقطه‌ای تک‌دارویی جهت استخراج $IC_{50}$، شیب منحنی $m$ و دوز میانه $D_m$ پیش از اجرای ماتریس ترکیبی و محاسبه شاخص ترکیب (CI).
8. **احراز اصالت بیوشیمیایی و بیولوژیک:**
   - تفکیک بیان رونویسی mRNA کاسپاز ۳ از فعالیت پروتئولیتیک آنزیم فعال (Cleaved Caspase-3) به همراه فلوسایتومتری دوگانه Annexin V/PI.
   - الزام به کنترل مثبت القای آپوپتوز (استاروسپورین ۱ میکرومولار) و کنترل بلانک بدون سلول (Cell-Free Blank) در تست‌های تترازولیوم.
   - ثبت محیط‌های کشت اختصاصی بر پایه شناسنامه ATCC (مانند Ham's F-12K برای A549 و EMEM برای MRC-5).
   - تبیین ناهمگونی ژنتیکی رده‌های سلولی بر مبنای جهش‌های KRAS و وضعیت p53 وحشی در برابر p53-null.
9. **تواضع معرفتی و مقیدسازی نوآوری به سرچ منفی:**
   - مهار ادعاهای مطلق کیهانی («برای اولین بار در جهان») و مقیدسازی نوآوری به گزارش رسمی استراتژی جستجوی منفی بولین (0 Hits در PubMed).
10. **فرمول‌نویسی بومی ورد (Native OMML):**
   - تبدیل تمامی فرمول‌های ریاضی مستقیماً به ساختار XML بومی ورد (`<m:oMath>`) بدون نشت کدهای لاتک خام (`$...$`).

---

### راهنمای اجرای سریع (خط فرمان)

اجرای کامل پایپ‌لاین تحقیق و نگارش پروپوزال با یک دستور واحد:

```powershell
uv run python scripts/run_research_pipeline.py --topic "عنوان کامل پژوهش شما به فارسی" --keywords "English Agent1, English Agent2, Target Condition" --output-dir "./output"
```

#### نمونه دستور اجرا:
```powershell
uv run python scripts/run_research_pipeline.py `
  --topic "مقایسه اثر همزمان فوکوئیدان با پمترکسد بر مهار رشد سلول‌های سرطان ریه" `
  --keywords "Fucoidan, Pemetrexed, Non-Small Cell Lung Carcinoma" `
  --study-family "in_vitro" `
  --output-dir "./output"
```

#### اسناد خروجی تولیدشده در پوشه خروجی:
1. `proposal.docx`: فایل نهایی Word پروپوزال شامل ۲۸ بخش کامل پژوهشیار، فرمول‌های OMML، جداول متغیرها، گانت چارت و بدون تیترهای تکراری.
2. `proposal.md`: متن کامل پروپوزال به فرمت مارک‌داون یکپارچه.
3. `PROPOSAL_RESEARCH_DOSSIER.json` و `.md`: پرونده شواهد پلمپ‌شده شامل قطعات استخراج‌شده از متن کامل مقالات.
4. `MOCK_GRANT_REVIEW_REPORT.md` و `.json`: کارنامه داوری گرنت به سبک NIH.
5. `EQUATOR_COMPLIANCE_AUDIT.md` و `.json`: کارنامه انطباق با گایدلاین‌های بین‌المللی پژوهش (ARRIVE, MIQE, GCCP).
6. `RISK_OF_BIAS_MITIGATION_REPORT.md` و `.json`: جدول جامع مهار سوگیری‌های مطالعاتی (ToxRTool / RoB-2 / SYRCLE).

---

### ۲۸ بخش مصوب سامانه پژوهشیار (وزارت بهداشت)

۱. **موضوع** (عنوان فارسی و انگلیسی)  
۲. **بیان مسئله** (Problem Statement تحلیلی با بار بیماری GLOBOCAN 2022/2024 و سرچ منفی)  
۳. **مرور بر منابع** (پیشینه پژوهش با سنتز نقادانه ۱۰۰٪ فارسی بر پایه مقالات متن کامل)  
۴. **اهمیت و ضرورت تحقیق**  
۵. **تعریف واژه‌ها**  
۶. **اهداف جزئی**  
۷. **اهداف کلی**  
۸. **اهداف کاربردی**  
۹. **فرضیات و سوالات پژوهش**  
۱۰. **دستاوردها**  
۱۱. **جدول متغیرها** (مستقل، وابسته، مداخله‌گر، مقیاس و نقش)  
۱۲. **جدول زمان‌بندی و مراحل اجرا** (گانت چارت)  
۱۳. **روش اجرا** (چارچوب کلی متدولوژی)  
۱۴. **نوع مطالعه**  
۱۵. **جامعه مورد مطالعه** (مدل زیستی، رده سلولی، تبارشناسی ژنتیکی ATCC)  
۱۶. **محل انجام مطالعه**  
۱۷. **معیارهای ورود به مطالعه**  
۱۸. **معیارهای خروج از مطالعه**  
۱۹. **ابزارهای گردآوری اطلاعات** (دستگاه‌ها، کیت‌ها، کاسپاز فعال و انکسین)  
۲۰. **تعیین اعتبار ابزار گردآوری** (روایی و کالیبراسیون)  
۲۱. **تعیین ابزار گردآوری** (پایایی، ضرایب تغییرات CV و ۳ تکرار مستقل)  
۲۲. **حجم نمونه و روش محاسبه آن** (معادله تخصیص منابع مید $E = 30 - 2 - 9 = 19$ و توان فاکتوریل G*Power)  
۲۳. **روش تجزیه و تحلیل داده‌ها** (Two-Way Factorial ANOVA، مدل اثرات متقابل و حدود CI)  
۲۴. **ملاحظات اخلاقی و کدهای اخلاق زیستی**  
۲۵. **نحوه رعایت نکات امنیتی و حفاظت پروژه** (سطح ایمنی BSL-2)  
۲۶. **مشکلات و محدودیت‌ها** (چالش‌های تکنیکال، مرزهای برون‌یابی بالینی و راهکارها)  
۲۷. **روش انجام طرح، شیوه اجرایی مراحل طرح و چگونگی جمع‌آوری اطلاعات** (پروتکل دو فازی چو-تالالای و بلانک بدون سلول)  
۲۸. **منابعی که استفاده شد** (فهرست کامل منابع بر اساس سبک ونکوور و ترتیب ظهور)

---

### وضعیت آزمون‌های کنترل کیفیت نرم‌افزاری

سیستم دارای ۲۴ سوئیت آزمون مستقل با **۴۷۷ تست فعال** است که همگی با **۱۰۰٪ قبولی** پاس می‌شوند:

```powershell
uv run python tests/run_all_tests.py
```

- **تست ضد نشت و تعمیم‌پذیری کامل (`test_hard_code_leakage.py`):** صفر بودن کلمات سخت‌کدشده زیستی در ۴۲ آزمون استاتیک.
- **تست چرخه بسته داوری و اصلاح پیوسته (`test_iterative_remediation_engine.py`):** ۳ تست ممیزی پچ‌های جراحی، همگرایی نمره داوری و فیوز Fail-Closed.
- **تست ایمن‌سازی ده‌گانه داوری (`test_v114_adversarial_immunization.py`):** ۱۱ تست اعتبارسنجی ارقام DOI، ارزیابی ToxRTool، چک‌سام گلوبوکان و درجات آزادی مید.
- **تست پلمپ پرونده شواهد (`test_two_loop_dossier.py`):** بررسی تغییرناپذیری شواهد پس از پلمپ.
- **تست‌های خصمانه و جهش نرم‌افزاری (`test_adversarial_scenarios.py` و `test_mutations.py`):** کشتن ۱۰۰٪ جهش‌های عمدی در منطق بیولوژیک.
- **تست‌های هاردنینگ ستون‌های ۱ تا ۵ (`test_v91_hardening.py` و `test_v92_hardening.py`):** اعتبارسنجی گیت‌های ضد کیمرا، تداخل تترازولیوم، کنترل بلانک و عدم نشت لاتک.

---

## مجوز (License)
این پروژه تحت مجوز [MIT License](LICENSE) منتشر شده است.
