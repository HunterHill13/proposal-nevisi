# Third-Party Research Patterns & Provenance Documentation
## Proposal-Nevisi v8.5 Research Engine Upgrade

This document records the provenance, architectural analysis, adaptation rationale, and licensing compliance for external research-grade workflows integrated from open-source biomedical research repositories into Proposal-Nevisi v8.5.

---

### 1. Source Repositories & License Compliance

Both source repositories are licensed under the **MIT License**. In compliance with MIT license conditions, the original copyright notices and permission notices are acknowledged, and all substantial logic reused has been adapted, sanitized, generalized to topic-agnostic biomedical architecture, and integrated with full attribution.

#### Source A: AIPOCH Medical Research Skills
- **Repository:** `https://github.com/aipoch/medical-research-skills`
- **License:** MIT License
- **Copyright:** (c) 2024-2026 AIPOCH
- **Architecture Role:** Conceptual workflows for biomedical search strategy construction, multi-stage paper reading, claim verification, topic saturation/whitespace analysis, and structured contradiction diagnosis.

#### Source B: K-Dense AI Claude Scientific Writer
- **Repository:** `https://github.com/K-Dense-AI/claude-scientific-writer`
- **License:** MIT License
- **Copyright:** (c) 2024-2026 K-Dense AI
- **Architecture Role:** Deterministic citation validation, multi-identifier deduplication, scholarly regex patterns, research packet assembly, manuscript audit trails, and reproducible search manifests.

---

### 2. Capability Extraction, Adaptation & Attribution Matrix

| Capability | Source Repository & Component | Original Problem Solved | Adaptation for Proposal-Nevisi v8.5 | Why Adapted / Dependencies Removed |
| :--- | :--- | :--- | :--- | :--- |
| **Query Families & Search Strategy** | **AIPOCH**: `biomedical-search-strategy-builder` (`scripts/main.py`) | Constructing Boolean queries with field tags `[MeSH Terms]`, `[Title/Abstract]`, and subheadings | Extracted `FieldTag`, `FilterType`, and `SearchConcept` architecture; unified with 16 dynamic query families in `generic_search_planner.py`. | Eliminated fixed cancer/diabetes domain bias. Generalized into topic-agnostic dynamic generation with provenance tracking. |
| **Controlled-Vocabulary & Free-Text Hybrid Search** | **AIPOCH**: `biomedical-search-strategy-builder` (`MeSHMapper`) | Mapping medical terms to official MeSH descriptors | Adapted MeSH descriptor mapping with dynamic fallback to free-text literals and comparator tracking. | Local dictionary modernized to operate dynamically and fall back gracefully offline without external API failure. |
| **Scholarly Identifier & Pattern Extraction** | **K-Dense**: `research-lookup` (`manuscript_packet.py`) | Regex parsing of DOIs, PMIDs, publication years, sample sizes, and effect estimates | Adapted `DOI_PATTERN`, `PMID_PATTERN`, `YEAR_PATTERN`, `SAMPLE_SIZE_PATTERN`, and `EFFECT_PATTERN` into `StructuredPaperReader`. | Replaced ad-hoc regexes with battle-tested scholarly parsing patterns; eliminated external dependency on `manuscript_packet`. |
| **Citation Deduplication & Normalization** | **K-Dense**: `research-lookup` (`manuscript_packet.py`) & `citation-management` (`validate_citations.py`) | Deduplicating URLs by stripping tracking parameters, normalizing titles, detecting duplicate DOIs and citation keys | Adapted `canonicalize_url`, `normalize_title`, and duplicate detection algorithms into `ScientificSearchAdapter`. | Integrated into unified multi-database deduplication pipeline (connected components + normalized titles). |
| **Multi-Dimensional Search Saturation** | **AIPOCH**: `medical-topic-saturation-and-whitespace-checker` (`SKILL.md`) | Differentiating true field saturation from superficial crowding | Formulated `EvidenceBasedSaturationTracker` evaluating 7 independent novelty dimensions (Record, Entity, Evidence, Contradiction, Citation, Database, Vocabulary). | Replaced single duplicate-percentage threshold with genuine multi-channel marginal yield computation. |
| **Citation Chasing & Lineage Recovery** | **AIPOCH**: `Citation Network Builder` & **K-Dense**: `research-lookup` | Recovering papers invisible to keyword queries via backward and forward references | Implemented first-class `CitationChasingEngine` supporting backward, forward, and lateral reference chaining. | Modeled citation links as directed edges with provenance tracking (`seed_paper`, `direction`, `discovered_paper`, `why_discovered`). |
| **Structured Paper Reading (Beyond Titles)** | **AIPOCH**: `medical-research-literature-reader-pro` (`SKILL.md`) | Routing papers to 4 research tracks (Clinical, Computational, Basic Experimental, Hybrid) | Created `StructuredPaperReader` extracting 18 structured fields (design, sample size, primary/secondary endpoints, effect sizes, bias, limits). | Replaced shallow keyword scanning with deep clinical/experimental evidence characterization. |
| **Paper-to-Claim Verification** | **AIPOCH**: `paper-to-claim-verifier` (`SKILL.md`) | Preventing citation drift and false attribution of causal claims | Implemented `PaperToClaimVerifier` testing claim-paper scope alignment, detecting 5 citation drift types, and bounding support strength. | Strictly distinguishes "paper is related to topic" from "paper proves the claim". Enforces causal language boundaries. |
| **Structured Contradiction Resolution** | **AIPOCH**: `contradictory-findings-resolver` (`SKILL.md`) | Explaining scientific discrepancies across divergent studies | Enhanced `GenericContradictionEngine` to classify explanations into `DEMONSTRATED`, `PLAUSIBLE`, and `UNRESOLVED_UNCERTAINTY`. | Avoids false compromises or averaging; isolates exact experimental parameters causing divergence. |
| **Reproducible Research Manifest** | **K-Dense**: `research-lookup` (`save_packet`, `manuscript_packet.py`) | Storing machine-readable research evidence packets for reproducibility | Implemented `ResearchRunManifest` generating reproducible JSON audit trails (`research_run_manifest.json`). | Pure Python standard library implementation, self-contained, lightweight, zero vendor lock-in. |

---

### 3. Components Intentionally NOT Reused & Rationale

1. **Vendor-Specific LLM Tool Chains:**
   - Both AIPOCH and K-Dense reference specific third-party APIs (Perplexity, Tavily, Anthropic API, or OpenClaw wrappers).
   - **Decision:** Omitted. Proposal-Nevisi relies exclusively on pure Python standard library adapters, authenticated or public REST endpoints (NCBI E-utilities, Europe PMC REST, Crossref REST, OpenAlex REST), and deterministic offline fixture fallbacks.

2. **BibTeX File Compilation Scripts (`doi_to_bibtex.py`, `format_bibtex.py`):**
   - K-Dense contains extensive BibTeX file manipulation scripts for LaTeX pipelines.
   - **Decision:** Omitted. Proposal-Nevisi already has native EndNote/RIS export, JSON schemas, and OpenXML Word DOCX compilation with Arabic/Dubai RTL typography.

3. **Superficial "Layer 10/11/12" Multipliers:**
   - Neither artificial pipeline steps nor decorative prompt wraps were adopted.
   - **Decision:** Focused strictly on substantive retrieval recall, citation chasing, and verifiable evidence auditing.
