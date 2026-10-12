# Deep Research Benchmark & Multi-Agent Architecture Audit for `proposal-nevisi`

> [!IMPORTANT]
> **Document Scope & Purpose:** This report presents a primary-source investigation of frontier AI Deep Research systems (Anthropic Claude Multi-Agent Research, OpenAI ChatGPT o3 Deep Research, Perplexity Deep Research, Google Gemini Deep Research), open-source scientific research & writing frameworks (`PaperQA2`, `AI-Scientist-v2`, `STORM`, `claude-scientific-writer`, `medical-research-skills`, `gpt-researcher`, `AgentLaboratory`), and a line-by-line architectural and code audit of `proposal-nevisi` (v11.4.2 / v11.5). It concludes with a concrete remediation blueprint for both the symbolic Python remediation engine and the LLM cognitive subagent loop.

---

## 1. Frontier AI Deep Research Architectures: Primary-Source Analysis

Modern "Deep Research" systems have converged on a fundamental paradigm shift: replacing single-pass RAG and monolithic prompt generation with **governed, multi-hop, verify-then-synthesize agentic workflows**. However, the four frontier providers implement markedly different orchestration topologies.

### 1.1 Anthropic Claude Multi-Agent Research System
* **Primary Source:** Hadfield, J., Zhang, B., Lien, K., Scholz, F., Fox, J., & Ford, D. (June 13, 2025). *"How we built our multi-agent research system."* Anthropic Engineering Blog (`https://www.anthropic.com/engineering/built-multi-agent-research-system`).
* **Architectural Topology (Orchestrator–Worker with Externalized State):**
  1. **`LeadResearcher` (Orchestrator Agent):** Receives the user prompt, conducts initial scoping, formulates a decomposed research strategy, and **persists the research plan to an external memory store**. External state persistence prevents catastrophic plan amnesia when context windows exceed 200,000 tokens and undergo compaction/truncation.
  2. **Parallel Specialized `Subagents`:** The `LeadResearcher` dynamically spawns 3–5+ parallel subagents (e.g., Claude Sonnet 4 workers coordinated by a Claude Opus 4 lead). Each subagent operates in an isolated context window, executing iterative tool calls (web search, workspace retrieval) using **interleaved thinking** to evaluate source quality and refine sub-queries before returning a structured distillation to the lead agent.
  3. **Structured Handoffs & Scaling Rules:** Subagents are prompted with explicit output schemas, task boundaries, and stopping heuristics (e.g., token/tool-call budgets per subagent) to prevent "infinite rabbit-hole browsing" or duplicated work across sibling subagents.
  4. **Dedicated `CitationAgent`:** Once the `LeadResearcher` exits the iterative retrieval loop and drafts the synthesis, the complete text and retrieved source corpus are handed off to a specialized `CitationAgent`. This agent performs deterministic and semantic span-level alignment, verifying that every factual and quantitative claim is anchored to a specific passage in the retrieved corpus.
* **Empirical Performance & Token Economics:**
  * On Anthropic's internal research evaluations, the multi-agent architecture (Opus 4 Lead + Sonnet 4 Subagents) outperformed a single-agent Opus 4 baseline by **90.2%**.
  * **Token Budget Law:** Multi-agent research consumes approximately **15× more tokens** than standard single-turn chat interactions, and token usage alone explained **~80% of the variance** in research quality alongside tool-call count and model selection.

### 1.2 OpenAI ChatGPT Deep Research (o3 Agentic Browsing & Python Loop)
* **Primary Source:** OpenAI (February 2025). *"Introducing Deep Research"* & *"OpenAI o3 and o4-mini System Card / Technical Report"* (`https://openai.com/index/introducing-deep-research/`).
* **Architectural Topology (End-to-End RL-Trained Single-Trajectory Reasoner with Sandboxed Tool Use):**
  1. **Reinforcement Learning over Long-Horizon Trajectories:** Rather than relying solely on heuristic prompt chaining, OpenAI trained a specialized version of the **o3 reasoning model** using end-to-end reinforcement learning (RL) on complex browsing, multi-hop retrieval, and data-analysis tasks.
  2. **Iterative Search–Read–Reason–Verify Loop:** Within its extended chain-of-thought (CoT), the agent formulates queries, opens full documents (HTML/PDF), scans for specific quantitative values, and **actively back-tracks** when a source is paywalled, contradictory, or low-authority.
  3. **Interleaved Sandboxed Python Execution:** Unlike pure text-retrieval agents, o3 Deep Research invokes a stateful Python interpreter mid-research to verify statistical calculations, transform tables, or cross-check numerical consistency across papers before writing its synthesis.
  4. **Test-Time Compute Scaling:** Sessions run asynchronously for 5 to 30 minutes, executing dozens of sequential and pivoted searches until epistemic uncertainty is resolved, emitting inline claim-level provenance.

### 1.3 Perplexity Deep Research
* **Primary Source:** Perplexity AI Technical Documentation & Release Notes (February 2025). *"Introducing Perplexity Deep Research."*
* **Architectural Topology (Iterative Query Decomposition & Multi-Hop Claim Verification):**
  1. **Tree-Structured Query Decomposition:** Decomposes a complex user prompt into atomic sub-questions, executes initial retrieval across academic/web indices, reads the resulting snippets/full-texts, and dynamically generates follow-up queries to fill missing variables.
  2. **Cross-Source Contradiction Triangulation:** When two retrieved sources report conflicting figures (e.g., different epidemiological incidence rates or drug IC50 values), the reasoning loop triggers a targeted disambiguation query to resolve date, methodology, or population differences.
  3. **Inline Claim-Level Verification:** Enforces strict post-retrieval grounding where every synthesized sentence is mapped to numbered bibliography entries without hallucinated URLs or DOIs.

### 1.4 Google Gemini Deep Research
* **Primary Source:** Google DeepMind / Gemini Team (December 2024 / 2025). *"Gemini Deep Research: Asynchronous Agentic Planning and Synthesis."*
* **Architectural Topology (Upfront User-Auditable Action Plan + High-Volume Asynchronous Gap Analysis):**
  1. **Explicit Multi-Step Research Planner:** Generates an explicit, structured research plan (broken into numbered investigative phases) before executing searches.
  2. **Asynchronous Gap-Analysis Loop:** Executes high-volume parallel search batches (often 40–100+ queries per session), continuously comparing accumulated notes against the initial research plan to identify unanswered sub-questions ("epistemic gaps") and launching refinement queries until coverage thresholds are met.
  3. **Long-Context Synthesis:** Leverages Gemini's 1M–2M token context window to hold full retrieved documents simultaneously during final synthesis, minimizing lossy intermediate summarization drift.

### 1.5 Comparative Matrix of Frontier Deep Research Systems

| Architectural Dimension | Anthropic Claude Research | OpenAI Deep Research (o3) | Perplexity Deep Research | Google Gemini Deep Research | `proposal-nevisi` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Core Topology** | Orchestrator (`LeadResearcher`) + Parallel `Subagents` + `CitationAgent` | End-to-End RL Reasoner (o3) with Browsing + Python Sandbox | Iterative Decomposition + Multi-Hop Retrieval Loop | Explicit Upfront Planner + High-Volume Async Gap Loop + 1M Context | Hybrid Two-Loop Python Engine + 2-Stage Native Subagents |
| **State & Memory Persistence** | Externalized Plan & Note Store (survives 200k truncation) | Stateful CoT + Python Notebook Environment | Iterative Scratchpad Buffer | Long-Context Window + Plan State Tracker | `PROPOSAL_RESEARCH_DOSSIER.json` + `PROPOSAL_SPEC.json` |
| **Quantitative / Statistical Verification** | Subagent tool calls | Native Python Sandbox execution mid-research | LLM reasoning over retrieved text | LLM reasoning over long context | Symbolic Python Auditors (`Mead`, `G*Power`, `SciFact`) |
| **Back-Tracking & Conflict Resolution** | Orchestrator spawns follow-up subagents on gaps | Native RL back-tracking on dead ends / conflicts | Targeted disambiguation queries | Iterative gap analysis against upfront plan | Tier-1 MeSH -> Tier-2 Free-text -> Facet expansion |
| **Citation Verification** | Dedicated post-draft `CitationAgent` | Inline span grounding during CoT synthesis | Inline claim-level citation mapper | Context-grounded source linking | `LiveReferenceVerificationGate` + `CitationTracker` |

---

## 2. Benchmark Against Open-Source Scientific Writing & Research Frameworks

### 2.1 `Future-House/paper-qa` (PaperQA2)
* **Primary Source:** Skarlinski, M. D., et al. (2024). *"Language agents achieve superhuman synthesis of scientific knowledge."* `arXiv:2409.13740` (`https://github.com/Future-House/paper-qa`).
* **Key Mechanism:** Decouples retrieval from generation into three explicit agent tools: `paper_search`, `gather_evidence` (**Ranking & Contextual Summarization — RCS**, scoring chunks 1–10 and distilling contextual summaries before drafting), and `generate_answer`.

### 2.2 `SakanaAI/AI-Scientist` & `AI-Scientist-v2`
* **Primary Sources:** Lu, C., et al. (2024). `arXiv:2408.06292`; Yamada, Y., et al. (2025). (`https://github.com/SakanaAI/AI-Scientist-v2`).
* **Key Mechanism:** Multi-reviewer simulation followed by an iterative **Author Reflexion Loop** where the drafting agent specifically addresses each reviewer weakness and re-submits for re-scoring.

### 2.3 `stanford-oval/storm` (STORM & Co-STORM)
* **Primary Sources:** Shao, Y., et al. (2024). `NAACL 2024` (`arXiv:2402.14207`); Jiang, Y., et al. (2024). `EMNLP 2024` (`https://github.com/stanford-oval/storm`).
* **Key Mechanism:** Multi-perspective expert persona questioning before outline generation, paired with a shared concept tree mapping claims to evidence nodes.

### 2.4 `K-Dense-AI/claude-scientific-writer` & `aipoch/medical-research-skills`
* **Primary Sources:** `https://github.com/K-Dense-AI/claude-scientific-writer` and `https://github.com/aipoch/medical-research-skills`.
* **Key Mechanism:** Domain-specialized scientific agent skills (`SKILL.md` + verification scripts) enforcing PICO/EQUATOR guidelines, iterative section drafting, and persistent file-system state (`PROPOSAL_SPEC.json`, `citations.bib`).

### 2.5 `assafelovic/gpt-researcher` & `SamuelSchmidgall/AgentLaboratory`
* **Primary Sources:** `https://github.com/assafelovic/gpt-researcher`; Schmidgall, S., et al. (2025). `arXiv:2501.04227`.
* **Key Mechanism:** Cyclic state-graph orchestration (`Researcher -> Writer -> Reviewer <-> Reviser -> Publisher`) with multi-round critic-refine loops.

---

## 3. Code Audit Findings in `proposal-nevisi` (`IterativeRemediationEngine` & `PROPOSAL_SPEC.json` Flow)

### 3.1 `PROPOSAL_SPEC.json` (`--spec-file`) Data Flow Gaps
1. **Dropped Subagent `studies` & `farsi_synthesis_summary`:** `execute_inner_loop()` (`run_research_pipeline.py:189-355`) ignored `self.spec_data.get("studies")`, and `execute_outer_loop()` (`line 660`) blocked `"studies"` from merging into `proposal_data`. Furthermore, `generate_compliant_proposal.py:595` checked `review_paragraph` without checking `farsi_synthesis_summary`.
2. **Disconnected `MethodologyResearchSubagent`:** `scripts/methodology_research_subagent.py` was not imported or invoked in `run_research_pipeline.py` or `generate_compliant_proposal.py`.
3. **Partial `research_problem_model` Override Risk:** Returning `self.spec_data["research_problem_model"]` raw without deep-merging defaults risked `KeyError` if a subagent omitted sub-keys.

### 3.2 `IterativeRemediationEngine` & `SurgicalSectionPatcher` Audit
1. **Flaw ID & List Mismatches:**
   * `MockGrantReviewPanel` emits `UNBOUNDED_EPISTEMIC_NOVELTY`, `CHOU_TALALAY_PROTOCOL_INCOMPLETE` (in `weaknesses`), `APOPTOSIS_POSITIVE_CONTROL_MISSING` (in `weaknesses`), `CASPASE3_MRNA_INSUFFICIENCY`, and `ASSAY_INTERFERENCE_DEFECT`.
   * `IterativeRemediationEngine` previously checked for mismatched string IDs (`UNBOUNDED_COSMIC_NOVELTY_CLAIM`, `CHOU_TALALAY_MONOTHERAPY_CURVE_MISSING`, `CASPASE3_TRANSCRIPTIONAL_PRIMING_CONFLATION`, `CELL_FREE_BLANK_INTERFERENCE_MISSING`) or checked `flaws` instead of `all_issues`.
2. **Organ-Blind Lung Cancer Stats in `patch_sec_2`:** `patch_sec_2` previously injected lung cancer statistics (`2,480,301` cases / `1,817,172` deaths) regardless of target organ and did not strip outdated `"2.2 میلیون"` / `"GLOBOCAN 2020"` strings.
3. **`patch_sec_26` Substring Mismatch:** `patch_sec_26` injected `"مرزهای ترجمان برون‌تنی به بالین"` instead of the exact tokens checked by `MockGrantReviewPanel` (`"فرضیه پیش‌بالینی"`, `"محدودیت مدل برون‌تن"`, `"نیازمند کارآزمایی بالینی"`, `"مرزهای تعمیم‌پذیری"`).
4. **Missing Surgical Patchers:** Added comprehensive surgical patchers for `SEMANTIC_DRIFT_CROSS_MODEL_OVERGENERALIZATION`, `UNSUBSTANTIATED_NOVELTY_CLAIM`, `INTER_SECTION_DRIFT`, `EMPTY_VARIABLE_TABLE`, `ROB2_IN_VITRO_MISAPPLICATION`, `MIQE_COMPLIANCE_DEFECT`, `BIOSTATISTICAL_SAMPLE_SIZE_CONTRADICTION`, and short sections, plus increased `DEFAULT_MAX_ITERATIONS` to `8` (and configurable via `--max-iterations`).
