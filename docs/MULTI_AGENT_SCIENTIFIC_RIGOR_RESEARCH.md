# Multi-Agent Scientific Rigor & Verification Architecture Research Report

**Repository:** `g:\دانشگاه\پژوهش\طرح1\.agents\skills\proposal-nevisi`  
**Target Engine Version:** v11.4.1 → v12.0 True Neuro-Symbolic Multi-Agent Architecture  

---

## Executive Summary

An audit of `proposal-nevisi` reveals a fundamental architectural split-brain: while `SKILL.md` mandates a **3-Subagent Cognitive Multi-Agent Architecture** (`Evidence Appraisal Subagent`, `Methodology & Anti-Chimera Subagent`, and `Adversarial Mock Grant Reviewer`), **their outputs are completely disconnected from the deterministic Python execution pipeline (`run_research_pipeline.py` and `generate_compliant_proposal.py`)**. 

When `run_research_pipeline.py` runs, it ignores any cognitive subagent outputs and instead falls back to deterministic Python templates that inject **hardcoded, biologically mismatched boilerplate**—originally overfitted to fix flaws in a single historical topic (*Fucoidan + Pemetrexed in Lung Cancer A549/H1299*). Furthermore, `MockGrantReviewPanel` and `IterativeRemediationEngine` are **not LLM reasoning agents**, but deterministic regex scanners that **check for and actively inject** those exact lung-cancer/A549-specific strings into every proposal, creating a closed-loop Goodhart's Law effect where the internal panel scores the proposal `1.4 / 9.0 (APPROVED_FUNDABLE)` while any blind external LLM reviewer immediately flags severe scientific, biological, biostatistical, and citation fabrication flaws.

---

## 1. Subagent Disconnection Audit (Split-Brain Architecture)

### 1.1 Unconnected Subagent Orchestration (`SKILL.md` vs. `run_research_pipeline.py`)
- **Where defined:** `SKILL.md:78-115` instructs the main agent to call `invoke_subagent` with three `"TypeName": "research"` subagents (`Evidence Appraisal Subagent`, `Methodology & Anti-Chimera Subagent`, `Adversarial Mock Grant Reviewer`), and then run:
  ```powershell
  uv run python scripts/run_research_pipeline.py --topic "<...>" --keywords "<...>" --output-dir "<...>"
  ```
- **Why it fails:**
  1. `run_research_pipeline.py:544-565` (`main()`) only accepts CLI arguments `--topic`, `--keywords`, `--study-family`, `--output-dir`, `--mode`, `--min-refs`, and `--max-refs`. There is **no CLI flag, JSON input parameter, or file ingestion hook** to pass subagent reports, curated evidence syntheses, custom section prose, or structured `research_problem_model` JSON into `MasterResearchPipeline`.
  2. In `run_research_pipeline.py:480-492`, `execute_outer_loop()` constructs `proposal_data` with only 11 top-level keys (`research_title_fa`, `research_title_en`, `study_type`, `primary_endpoint`, `sample_size_justification`, `target_population`, `statistical_analysis_plan`, `negative_search_strategy`, `studies`, `proposal_research_dossier`, `format`).
  3. It **never passes** `research_problem_model`, `interventions_or_exposures`, `primary_outcomes`, `problem_statement_text`, `literature_review_text`, `study_population_text`, `sample_size_text`, or `step_by_step_procedure_text` into `ProposalGenerator.generate_and_save()`.
  4. Even the internal Python class `MethodologyResearchSubagent` (`scripts/methodology_research_subagent.py:54-272`) is **dead code** in the pipeline—it is never imported or called by `run_research_pipeline.py` or `generate_compliant_proposal.py`.

---

## 2. Hardcoded & Template Fallback Injections Causing Biological/Methodological Flaws

Because `run_research_pipeline.py:480-492` omits `research_problem_model` and all section-specific text overrides, `generate_compliant_proposal.py` (`assemble_pajooheshyar_28`, lines `477-1021`) falls back to hardcoded strings in almost every section:

### 2.1 Lung Cancer GLOBOCAN 2022 Statistics Injected into ALL Cancers
- **Location:** `scripts/generate_compliant_proposal.py:544-550` and `scripts/iterative_remediation_engine.py:200-218`
- **Scientific Flaw Caught by External Reviewers:** `2,480,301 new cases (12.4%)` and `1,817,172 deaths (18.7%)` in Bray et al. (2024) are the **exact statistics for Lung Cancer**, NOT "malignant cancers" in general (total global cancer incidence in GLOBOCAN 2022 is ~20 million cases and ~9.7 million deaths), nor colorectal cancer, breast cancer, gastric cancer, or glioblastoma. Furthermore, `cite_burden` (`generate_compliant_proposal.py:539`) attaches `[{model_cnums[0]}]` or `[1]` (whatever paper happened to be retrieved first from PubMed) to this Bray et al. 2024 claim, creating a **false citation attribution**.

### 2.2 Fabricated Biphasic ROS Contradiction Assigned to `studies[0]` and `studies[1]`
- **Location:** `scripts/run_research_pipeline.py:436-446`
- **Scientific Flaw Caught by External Reviewers:** Regardless of what `studies[0]` and `studies[1]` actually studied (e.g., an epidemiological study, a kinase inhibitor trial, or an immunotoxin paper), the pipeline fabricates a claim that `PMID: p1` reported high-dose ROS apoptosis and `PMID: p2` reported low-dose free-radical scavenging! This was hardcoded solely to satisfy `EpistemicRigorAuditor._check_contradiction_resolution()` (`scripts/epistemic_rigor_auditor.py:239-262`).

### 2.3 Fake / Unverified Negative Search Log (`0 hits` Claim Without Execution)
- **Location:** `scripts/run_research_pipeline.py:375-381` and `scripts/generate_compliant_proposal.py:554-566`
- **Scientific Flaw Caught by External Reviewers:** The pipeline never actually verifies that this query returns 0 hits—in fact, during Phase 1 (`run_research_pipeline.py:200-206`), `tier1_mesh_q` often returned multiple papers (`len(studies) > 0`), yet the pipeline still writes `-> 0 hits` into the Dossier and Section 2! If the combination is already published, claiming `0 hits` and `First-in-Class` in Section 2 while citing papers on that exact combination in Section 3 is a blatant self-contradiction.

### 2.4 Missing `research_problem_model` Degrades Sections 2, 4, 5, 6, 9, 11, 13, 15 to Generic Placeholders
- **Location:** `scripts/run_research_pipeline.py:480-492` → `scripts/generate_compliant_proposal.py:486-498`
- **Mechanism:** Because `run_research_pipeline.py` does not populate `research_problem_model`, `target_condition`, `population_or_model`, `interventions_or_exposures`, or `primary_outcomes` in `proposal_data`:
  - `cond_name` defaults to `"بیماری یا وضعیت هدف"` (`line 494`)
  - `sys_name` defaults to `"سیستم بیولوژیک هدف"` (`line 496`)
  - `interventions` defaults to `[]` (`line 497`), so `agt1` becomes `"مداخله اول"` (`line 515`) and `len(interventions) >= 2` is `False`!
  - **Section 6 (Specific Aims, `lines 659-668`):** `outcomes` is empty (`[]`), so it outputs only a single generic line.
  - **Section 9 (Hypotheses, `lines 695-713`):** Because `len(interventions) < 2`, it skips `CombinationHypothesisEngine` and outputs a single generic sentence.
  - **Section 11 (Variable Table, `lines 732-736` & `dynamic_protocol_designer.py:74-150`):** Because `interventions` and `primary_outcomes` are empty, `DynamicProtocolDesigner.generate_variable_table()` generates a table with **ZERO independent variables and ZERO dependent variables**, containing only 3 control/confounder rows (`بلانک بدون سلول`, `کنترل حلال ناقل`, and `تعداد پاساژ`)!

### 2.5 Hardcoded `p53-WT vs. p53-null` and `F-12K / EMEM / RPMI-1640` Media in Section 15
- **Location:** `scripts/generate_compliant_proposal.py:801-808` and `scripts/iterative_remediation_engine.py:251-263`
- **Scientific Flaw Caught by External Reviewers:** Written specifically for A549 (`p53-WT`, `F-12K`) vs. H1299 (`p53-null`, `RPMI-1640`) vs. MRC-5 (`EMEM`). When the user's topic involves a single cell line (e.g., HCT116, MCF-7, HepG2), or DMEM-cultured cells, Section 15 falsely claims the study compares `p53-WT` vs `p53-null` cell lines in `F-12K / EMEM / RPMI-1640`.

### 2.6 Biostatistical & Group-Count Contradictions Across Dossier, Section 22, and Section 27
- **Location:** `run_research_pipeline.py:369`, `generate_compliant_proposal.py:916-925`, `generate_compliant_proposal.py:991-992`
- **Scientific Flaws Caught by External Reviewers:**
  1. **Cross-Document Contradiction:** The Dossier says `target_n=24`, Section 22 says $N=30$ ($10$ groups $\times 3$ replicates), and Section 27 describes $5-7$ monotherapy doses + $5$ combination doses + controls across $24, 48, 72$ hours.
  2. **Mathematical Error in G*Power Claim:** In G*Power (`F tests - ANOVA: Fixed effects, special, main effects and interactions`), with numerator $df = 9$, total sample size $N = 30$ ($10$ groups, error $df = 20$), $\alpha = 0.05$, and effect size $f = 0.40$ ($\lambda = N \cdot f^2 = 30 \times 0.16 = 4.8$), the actual statistical power is **~21.5%**, NOT **85.2%**!

### 2.7 Generic Template Boilerplate in Section 3 (`EvidenceDrivenParagraphBuilder`)
- **Location:** `scripts/generic_reference_auditor.py:3535-3721`
- **Scientific Flaw Caught by External Reviewers:** `synthesize_findings_persian()` checks 7 broad keyword buckets and emits identical stock phrases for every paper, and discards English verbatim passages (`if has_persian_passage: ... else:`), making every paragraph in Section 3 read like a repetitive template without paper-specific results, gene names, or IC50 values.

---

## 3. Best-Practice Multi-Agent Architectures from Primary Literature

1. **FutureHouse `PaperQA2` (Skarlinski et al., 2024 — *arXiv:2409.13740*):**
   - Uses Contextual Summarization (RCS) tied to atomic citations and permits abstention rather than fabricating contradictions when none exist.
2. **Stanford `STORM` & `Co-STORM` (Shao et al., 2024 — *NAACL 2024, arXiv:2402.14207*; Jiang et al., 2024 — *EMNLP 2024, arXiv:2408.15232*):**
   - Multi-perspective persona agents build a verified, citation-bound **Proposal Specification / Outline** before drafting any section.
3. **Sakana AI `The AI Scientist` v1 & v2 (Lu et al., 2024 — *arXiv:2408.06292*; Yamada et al., 2025 — *arXiv:2504.08066*, *Nature* 2026):**
   - Employs a **Blind LLM Peer Reviewer** after manuscript compilation, feeding structured critiques into an iterative LLM refinement loop.
4. **Atomic Claim-to-Evidence Verification (`FActScore`, Min et al., *EMNLP 2023*; `SAFE`, Wei et al., *arXiv:2403.18802*; `VeriScore`, Song et al., *EMNLP 2024*; `SciFact`, Wadden et al., *EMNLP 2020*):**
   - Decomposes generated prose into atomic claims and verifies each claim against the cited reference's abstract/full-text.
5. **Stanford `Biomni` & Multi-Agent Scientific Peer Review (`AgentReview`, Jin et al., *EMNLP 2024*):**
   - Equips specialist agents with executable computational tools (`scipy.stats` for exact power calculations, live PubMed Boolean hit verification) so biostatistics and experimental designs are mathematically identical across all sections.
