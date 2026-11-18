---
name: proposal-nevisi
description: Autonomous Medical Research Proposal Writing Engine (v14.2.0) featuring 7-Subagent Cognitive Study Section Panel, 7-Archetype Polymorphism (+ Usability), Native OMML Math Engine, and Two-Gate Review Protocol.
version: 14.2.0
---

# Proposal-Nevisi: Autonomous Medical Research Proposal Writing Engine (v14.2.0)

`proposal-nevisi` is an autonomous scientific engineering skill designed to generate publication-grade, evidence-grounded medical research proposals adhering to the 28 canonical sections of the Iranian Ministry of Health (*Pajooheshyar*) portal.

The engine integrates real-time biomedical literature retrieval (PubMed, Europe PMC, OpenAlex), mathematical formula compilation via native Office Math Markup Language (OMML), a 7-archetype study design polymorphism matrix (including PRISMA-ScR/JBI Scoping Reviews plus Usability evaluation), and a 7-subagent adversarial cognitive study section panel.

---

## 1. Core Directorial Workflow

```
┌────────────────────────────────────────────────────────┐
│  Creative Gate 1: Socratic Strategy & Archetype Conf.   │
│  - ask_question: Clarify study archetype & methodology │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│  Stage 1: Pre-Draft Literature & Evidence Harvesting   │
│  - generic_search_planner.py & mesh_query_expander.py  │
│  - Parallel Research Subagents (PaperQA2 RCS 0-10)     │
│  - Generate PROPOSAL_SPEC.json                         │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│  Stage 2: Core Proposal & Native Word OMML Synthesis   │
│  - Render 28 Canonical Pajooheshyar Sections           │
│  - docx_builder.py (Dynamic Cover & OOXML Chrome)      │
│  - native_omml_math_engine.py (<m:f>, <m:rad>)        │
│  - Literature & Concept Graphs (Cytoscape.js)          │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│  Stage 3: 7-Subagent Cognitive Study Section Panel     │
│  - 6 Specialized Domain Reviewers (NIH Heuristic 1-9) │
│  - Biostatistics Verification (verify_biostatistics.py)│
│  - SRO Panel Synthesis (grant-study-section-sro)      │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│  Stage 4: Post-Draft Citation & Quality Audit Loop     │
│  - citation-claim-verifier: Abstract entailment check  │
│  - professor-namoosi-auditor: Objective rubric check   │
│  - Self-repair loop (Max 2 iterations if needed)       │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│  Creative Gate 2: Package Release & Delivery           │
│  - Final verified proposal.docx & proposal.md          │
│  - Visual Literature Graph & Audit Dossier             │
└────────────────────────────────────────────────────────┘
```

---

## 2. Execution Protocol & Stages

### Creative Gate 1: Socratic Strategy Confirmation
Before executing any generation pipeline, the agent must interact with the user via `ask_question` to determine:
1. **Study Archetype:** Choose from the 7 canonical archetypes (`clinical_rct`, `in_vivo`, `in_vitro`, `health_systems`, `epidemiological`, `diagnostic`, `scoping_review`) plus `usability` (`USABILITY_AND_DIGITAL_HEALTH`). For `scoping_review` / `evidence_synthesis`, the protocol strictly enforces PRISMA-ScR / JBI search comprehensiveness and saturation, omitting Cochran formulas and alpha/power tests.
2. **Target Intervention & Biological System:** Confirm specific drugs, cell lines, animal models, or clinical cohorts.
3. **Primary Outcome Measure:** Confirm the primary statistical endpoint (e.g., cell viability, hazard ratio, Catastrophic Health Expenditures, sensitivity/specificity, SUS score).

### Stage 1: Evidence Harvesting & Specification (`PROPOSAL_SPEC.json`)
The agent initiates literature harvesting:
1. Formulate two-tier MeSH query strings using `scripts/mesh_query_expander.py`.
2. Execute balanced dual-path search (efficacy trials vs. safety/toxicity/negative trials) across PubMed and Europe PMC.
3. Spawn two parallel research subagents (`Role: Evidence & Quantitative RCS Appraisal Subagent`) to evaluate studies, compute Relevance and Citation Scores (RCS 0-10), and extract quantitative data points (IC50, sample size, odds ratios, p-values).
4. Save the gathered metadata to `PROPOSAL_SPEC.json`.

### Stage 2: Proposal Drafting & Native OMML Compilation
The proposal is generated strictly across the **28 Canonical Pajooheshyar Sections** (see `docs/STANDARDS_REFERENCE.md` for section definitions).
- **Mathematical Equations:** Sample size formulas and statistical equations must be compiled into native Word OMML via `scripts/native_omml_math_engine.py`. Raw LaTeX strings (e.g., `\frac{...}{...}`) are strictly prohibited in the final `.docx` (enforced by `HARD-05`).
- **Visual Design:** Governed by `scripts/docx_builder.py`, enforcing Dubai 10.5pt font, `#1A365D` headers, metadata-driven cover tables, zero soft line breaks, and table pagination tags (`<w:tblHeader/>`, `<w:cantSplit/>`).

### Stage 3: 7-Subagent Cognitive Study Section Panel
The unverified draft is evaluated by 7 specialized zero-context subagent reviewers:
1. **Significance & Innovation (`grant-significance-innovation.md`):** Evaluates Sections 2, 3, 4 against epidemiologic indices (GLOBOCAN for oncology; WHO/IHME GBD for non-oncology).
2. **Methodology & Biostatistics (`grant-methodology-biostatistics.md`):** Audits Sections 9, 11, 14–16, 18–23, 27; executes `scripts/verify_biostatistics.py` to mathematically verify sample size formulas.
3. **Evidence Entailment (`grant-evidence-entailment.md`):** Audits Sections 2, 3, 28 for zero citation drift and accurate PubMed metadata matching.
4. **Feasibility & Logistics (`grant-feasibility-logistics.md`):** Audits Sections 12, 16, 18, 19, 27 for realistic timeline Gantt charts, data tools, and equipment availability.
5. **Ethics & Lay Advocacy (`grant-ethics-lay-advocate.md`):** Audits Sections 5, 24, 25, 26 for Pajooheshyar ethics compliance, ARRIVE 2.0, and BSL safety.
6. **Academic Style & Voice (`grant-academic-style-voice.md`):** Audits Sections 2, 3, 4, 6, 13, 26, 27 for lexical hygiene, sentence burstiness ($\ge 8.0$), naturalized transitions, and zero AI disclosure boilerplate.
7. **Scientific Review Officer (`grant-study-section-sro.md`):** Synthesizes reviewer scores into an aggregate Heuristic Readiness Score (1.0–9.0) and issues the panel verdict.

### Stage 4: Post-Draft Verification & Self-Repair
- `citation-claim-verifier` inspects cited sentences against actual PubMed/PMC abstracts.
- `professor-namoosi-auditor` evaluates the draft against `resources/rubrics/professor-namoosi-rubric.md` (`HARD-01` to `HARD-07`).
- If Heuristic Readiness Score $\le 2.0$ (Exceptional $\le 1.5$) with `0` Blocker/Hard failures: Status is `APPROVED_FUNDABLE`.
- If deficiencies exist: The agent performs up to 2 targeted surgical self-repair cycles (`5` outer audit return cycles max).

### Creative Gate 2: Release & Delivery
Deliver the verified artifacts in `output/[topic_slug]/`:
- `proposal.docx`: Official Word document with native OMML formulas.
- `proposal.md`: Markdown proposal manuscript.
- `LITERATURE_CITATION_GRAPH.html`: Interactive Cytoscape.js citation network.
- `BIOMEDICAL_CONCEPT_GRAPH.json`: Structured biomedical knowledge graph.
- `AUDIT_REPORT.json`: Complete audit findings and scoring breakdown.

---

## 3. Core Script Architecture (`scripts/`)

| Script | Purpose & Capabilities |
|---|---|
| `docx_builder.py` | Official Word (.docx) compiler with dynamic cover metadata, Pajooheshyar stylesheet, Dubai font, and table formatting. |
| `native_omml_math_engine.py` | Converts LaTeX math expressions into native Office Math Markup Language (`<m:oMath>`, `<m:f>`, `<m:rad>`). |
| `verify_biostatistics.py` | Parametrically verifies sample size equations across all 7 canonical archetypes + usability (including PRISMA-ScR/JBI evidence saturation); fails closed as `UNVERIFIED` on unknown designs. |
| `mesh_query_expander.py` | Maps clinical keywords across 119 standardized MeSH descriptors in 19 biomedical & health-systems branches (`<= 3` top-level `AND` blocks). |
| `generic_search_planner.py` | Formulates balanced, multi-database search queries with dynamic time windows. |
| `generic_claim_entailment_engine.py` | Evaluates factual entailment between cited claims and retrieved abstracts. |
| `citation_graph_engine.py` | Constructs directed citation networks and exports interactive Cytoscape HTML visualizers. |
| `biomedical_concept_graph.py` | Builds semantic concept graphs connecting interventions, outcomes, and disease targets. |

*(Parent workspace sync utilities reside outside the skill at root: `sync_skills.py`, `sync_agent_memory.py`.)*

---

## 4. Test Suite & Validation Commands

All core functionality is covered by regression tests in `tests/`:

```bash
# Run the complete test suite
uv run python tests/run_all_tests.py

# Run targeted adversarial and math conversion tests
uv run python -m unittest tests/test_v90_adversarial.py

# Run cognitive study section verification tests
uv run python -m unittest tests/test_v140_cognitive_study_section.py

# Run JSON schema integrity tests
uv run python -m unittest tests/test_property_and_schemas.py
```

---

## 5. Reference Standards & Supplementary Documentation

For exhaustive specifications, consult the following documentation in `docs/`:
- **`docs/STANDARDS_REFERENCE.md`**: Detailed breakdown of the 28 Pajooheshyar canonical sections, the 7-archetype polymorphism matrix (+ usability), full MeSH thesaurus mapping, and Word typography rules.
- **`docs/HISTORICAL_CHANGELOG.md`**: Complete architectural evolution from v1.0 through v14.2.0.
- **`resources/rubrics/professor-namoosi-rubric.md`**: Heuristic Readiness Score (`<= 2.0 APPROVED_FUNDABLE`) rubric and `HARD-01` to `HARD-07` failure definitions.
