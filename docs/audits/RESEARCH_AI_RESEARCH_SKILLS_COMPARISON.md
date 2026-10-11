# Comprehensive Comparative Analysis: State-of-the-Art AI Research Agent Architectures and Next-Gen Enhancements for `proposal-nevisi`

**Date**: October 2026  
**Status**: Research Synthesis & Architectural Blueprint  
**Target Systems**: `proposal-nevisi` (v10.2 -> v11.0), Claude Code Research Agent, OpenAI Deep Research / ChatGPT, Orchestra-Research, AIPOCH Medical Research Skills, Nanoskill Research Catalog.

---

## 1. Executive Summary

Modern AI research systems have evolved from simple conversational retrieval (RAG) to autonomous, multi-loop agentic architectures. To elevate `proposal-nevisi` into an internationally competitive, publication- and grant-grade biomedical proposal engine, we conducted an in-depth analysis of five primary benchmark systems and repositories:

1. **AIPOCH Medical Research Skills** (`github.com/aipoch/medical-research-skills`): 550+ domain-specific skills across Evidence Insights, Protocol Design, Data Analysis, and Academic Writing, governed by the `MedSkillAudit` benchmark.
2. **arXiv:2606.11830v1** (*Skill-Augmented AI Agents for Medical Research Analysis*): Empirical multi-model benchmark (GPT-5.4, Claude Sonnet 4.6, DeepSeek-V4 Pro) demonstrating the critical necessity of upstream-downstream workflow continuity, biological validity checks, and expert-aligned evaluation metrics.
3. **SkillsLLM Medical Research Directory** (`skillsllm.com/skill/medical-research-skills`): Standardized agent skill packaging, automated security auditing, and prompt-injection defense heuristics.
4. **Orchestra-Research AI-Research-SKILLs** (`github.com/orchestra-research/AI-research-SKILLs`): 98 research engineering skills featuring the **Autoresearch Two-Loop Architecture** (Inner Optimization + Outer Synthesis) and **Agent-Native Research Artifacts (ARA)** with epistemic rigor scoring.
5. **Nanoskill 2026 Research Agent Catalog** (`nanoskill.ai/blog/best-agent-skills-for-research`): Critical analysis of Hermes iterative loops, Local Deep Research source-grounding, and running research dossier workflows.

---

## 2. Architecture Comparison: How Frontier Research Agents Work

| Feature / Dimension | Claude Code Research Engine | OpenAI ChatGPT Deep Research | Orchestra AI-Research-SKILLs | AIPOCH Med-Research-Skills | `proposal-nevisi` (Current v10.2) | Proposed `proposal-nevisi` (v11.0 Target) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Execution Architecture** | Context-efficient Subagent delegation (`research`, `self`) | Recursive search tree crawl (BFS/DFS multi-hop) | Two-Loop: Inner Optimization + Outer Synthesis | Procedural & execution modular skill routing | 4-Layer Modular Pipeline (Accuracy, Structure, Citation, Word) | **Two-Loop Hybrid**: Autonomous Evidence Loop + 28-Section Proposal Synthesizer |
| **Literature Verification** | Local file grounding & grep | Web snippet grounding with strict attribution | Primary source citation verification & BibTeX | Hard rules for paper authenticity & PRISMA | Live PubMed E-utilities + Crossref fail-closed gate | **Multi-tier Verified Graph**: Live PubMed/Crossref + Europe PMC Full-Text + SciFact |
| **Research Memory** | Ephemeral context + Markdown notes | Internal latent scratchpad + citation cache | ARA Dossier (`ara/` directory with user/AI tags) | Domain-specific prompt templates | In-memory config dictionary + temp disk cache | **Persistent Research Dossier** (`PROPOSAL_RESEARCH_DOSSIER.json`) |
| **Epistemic Rigor Audit** | Tool linting & unit tests | Parametric fact-checking | ARA Seal Level 2 Rigor Reviewer (6 dimensions) | MedSkillAudit Domain-Specific Framework | MockGrantReviewPanel (NIH 1-9) + EquatorAuditor | **Unified Epistemic Audit Gate** (6-dimension rigor + Equator + RoB-2 + NIH Grant Score) |
| **Contradictory Evidence** | Manual human-in-the-loop review | Heuristic balanced-perspective synthesis | Self-refuting hypothesis loop (Norm Heterogeneity) | Contradictory Findings Resolver skill | BiologicalMechanism AdversarialVerifier | **Active Contradictory Evidence Resolver**: identifies conflicts & formulates resolution |
| **Methodological Chain** | Ad-hoc agent prompt chain | Multi-stage prompt plan | ARA Compiler with structured code stubs | Study Design Identifier -> Cohort -> Endpoint | Canonical 28 sections + EQUATOR compliance | **Strict Upstream-Downstream Invariant Engine**: Gap -> Endpoint -> Sample Size -> Statistical Test |

---

## 3. Deep Dive: Key Architectural Patterns from the 5 Sources

### 3.1 Orchestra-Research: The Two-Loop Architecture & ARA Rigor Reviewer
- **Autoresearch Two-Loop Framework**:
  - *Outer Loop (Synthesis)*: Operates at the strategic proposal level: formulates the research question, scopes the specific aims, structures the 28 sections, and synthesizes the literature review.
  - *Inner Loop (Optimization & Discovery)*: Operates at the evidence and methodological level: executes targeted multi-database queries, downloads full texts, extracts verbatim evidence sentences, runs power calculations, and checks assay interference.
- **Agent-Native Research Artifacts (ARA)**:
  - Preserves a clean separation between human user decisions and AI-derived evidence.
  - The `ARA Rigor Reviewer` evaluates six epistemic dimensions:
    1. *Evidence Relevance & Strength*: Directness of biological links.
    2. *Falsifiability & Null Hypothesis*: Explicit statement of statistical null and alternative hypotheses.
    3. *Methodological Coherence*: Alignment between assay limits of detection (LOD) and expected effect sizes.
    4. *Scope & Boundary Conditions*: Explicit declaration of study limitations and model organism translational barriers.
    5. *Exploration Integrity*: Transparent reporting of negative results and rejected mechanisms.
    6. *Biological Grounding*: Zero parametric hallucination of cell lines, antibodies, or gene symbols.

### 3.2 AIPOCH & arXiv:2606.11830v1: Addressing the "Biological Validity Gap"
The empirical benchmark revealed that AI agents often produce structurally attractive protocols that fail expert scrutiny due to:
- **Upstream-Downstream Disconnect**: An identified clinical research gap (e.g., immunotherapy resistance) was not properly translated into the biomarker feature-selection pipeline.
- **Biological Validity Gap**: Models cited non-existent or inappropriate gene sets (e.g., conflating ferroptosis with cuproptosis markers).
- **AIPOCH Countermeasures**:
  - *Hard Literature Authenticity Constraints*: Prohibiting any uncited or provisionally assumed biological claims.
  - *Study Design Classifier*: Explicitly classifying the study (In Vitro mechanistic, In Vivo efficacy, Case-Control, Cohort, Diagnostic Accuracy) before generating methodology.
  - *Contradictory Findings Resolver*: Actively retrieving papers with opposing outcomes to build a robust, defensible rationale.

### 3.3 Nanoskill 2026 Insights: Source-Grounded Running Research Dossier
- The most reliable research agents (such as Hermes and Local Deep Research) maintain a **running research notes dossier** on disk.
- Instead of generating the final manuscript in a single pass from context memory, the agent progressively compiles:
  1. Primary literature queries & retrieved PMIDs.
  2. Full-text passage extracts with page/paragraph coordinates.
  3. Methodological parameters (concentrations, incubation times, sample sizes).
  4. Contradictions & resolutions.
  5. Only once the dossier passes verification does document generation proceed.

---

## 4. Architectural Blueprint for `proposal-nevisi` v11.0

To incorporate these best practices into `proposal-nevisi` while preserving its 100% test integrity (429 passing tests) and Persian medical typography rules, we design four evolutionary pillars:

### Pillar 10: Persistent Proposal Research Dossier (`ProposalResearchDossier`)
- Generates a structured JSON/Markdown research record (`proposal_research_dossier.json`) storing:
  - Formulated hypotheses ($H_0$, $H_1$).
  - Full-text grounded passages with verified DOIs and PubMed PMIDs.
  - Target biological entities (cell lines, antibodies, genes, drugs) authenticated via RRID/CAS/UniProt.
  - Evidence matrix mapping each of the 28 sections to specific empirical claims.

### Pillar 11: Active Contradictory Evidence & Conflict Resolver (`ContradictoryFindingsResolver`)
- When drafting Section 2 (بیان مسئله) and Section 3 (مرور بر منابع), actively queries PubMed for conflicting evidence or negative findings.
- Generates a dedicated "تحلیل یافته‌های متناقض و توجیه علمی" (Contradictory Evidence Synthesis) sub-clause resolving discrepancies by experimental model, dosage, or exposure kinetics.

### Pillar 12: Upstream-Downstream Methodological Invariant Gate (`MethodologicalInvariantGate`)
- Enforces strict mathematical and logical continuity across the 28 sections:
  $$\text{Clinical Gap (Sec 2)} \longrightarrow \text{Primary Endpoint (Sec 6/7)} \longrightarrow \text{Sample Size Formula (Sec 22)} \longrightarrow \text{Statistical Model (Sec 23)}$$
- Blocks generation if the statistical test in Section 23 (e.g., ANOVA) does not match the sample size design in Section 22 (e.g., 2-arm t-test) or the primary outcome metric.

### Pillar 13: ARA-Aligned Epistemic Rigor Auditor (`EpistemicRigorAuditor`)
- Evaluates the proposal against the 6 ARA rigor dimensions before docx rendering.
- Integrates seamlessly with `MockGrantReviewPanel` (NIH 1-9 scoring) and `EquatorComplianceAuditor` to guarantee fundable quality ($\le 3.5$).

---

## 5. Verification & Testing Strategy
- Add unit and integration tests in `tests/test_research_dossier.py`, `tests/test_contradictory_findings.py`, and `tests/test_methodological_invariants.py`.
- Maintain 100% test pass rate across all test suites (`tests/run_all_tests.py`).
- Synchronize all scripts and SKILL.md documentation between the local workspace and the global plugin path.
