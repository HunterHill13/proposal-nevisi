# Exhaustive Research Report: Academic Citation Graph Networks, Semantic Literature Discovery Engines, and Biomedical Concept Graph Architectures

**Target File for Persistence:** `g:\دانشگاه\پژوهش\طرح1\.agents\skills\proposal-nevisi\docs\LITERATURE_CITATION_GRAPH_AND_DISCOVERY_RESEARCH.md`
**Author:** Subagent Research Specialist (`proposal-nevisi` Cognitive Subagent Engine)
**Date:** October 2026
**Status:** Publication-Grade Comprehensive Report (Ready for Direct Commit / File Write)

---

# Academic Citation Graphs, Semantic Literature Discovery Engines, and Biomedical Knowledge Architectures: Theory, Algorithms, and Implementation Blueprint for `proposal-nevisi`

> [!IMPORTANT]
> **Executive Summary & Scope:** This document provides a primary-source, exhaustive investigation into the mathematical, algorithmic, and architectural foundations of academic citation graphs, semantic discovery engines (Litmaps, Connected Papers, ResearchRabbit, Inciteful), scientific Graph-RAG frameworks (Microsoft GraphRAG, FutureHouse PaperQA2), and programmatic REST APIs (OpenAlex, Semantic Scholar S2AG, Europe PMC, PubMed E-Utilities). It formulates a unified **Dual-Layer Heterogeneous Information Network (HIN)** bridging macro-level bibliographic citation topology with micro-level biomedical mechanistic graphs (Drug $\to$ Target $\to$ Pathway $\to$ Disease). Finally, it delivers an actionable, dependency-free engineering blueprint, data schema (`LITERATURE_CITATION_GRAPH.json`), Cytoscape.js interactive visualizer, and complete Python reference implementation for `proposal-nevisi` v12.0.

---

## 1. Academic Citation Graph & Literature Discovery Platforms: Technical Reverse-Engineering

Modern academic discovery platforms have fundamentally transitioned beyond traditional keyword Boolean indexing (e.g., standard PubMed or Google Scholar queries). Instead, they exploit the topological and graph-theoretic properties of scientific literature modeled as **Directed Acyclic Graphs (DAGs)**, bipartite graphs, and projected co-occurrence spaces.

### 1.1 Litmaps: Traversal Dynamics, Coordinate Geometry & Discover Mode
* **Underlying Philosophy:** Litmaps maps literature across a continuous Cartesian space where time and citation momentum form the geometric axes, solving the problem of temporal disorientation common in unstructured force-directed graphs.
* **Network Traversal Mechanics:**
  1. **Seed Maps & Multi-Seed Ingestion:** Users define a set of initial seed nodes $S = \{s_1, s_2, \dots, s_k\}$.
  2. **First-Degree Expansion ($k=1$):** Traverses direct citations:
     $$\mathcal{N}_1(S) = \bigcup_{s \in S} \left( \text{Refs}(s) \cup \text{Cites}(s) \right)$$
     where $\text{Refs}(s) = \{u \in V \mid (s \to u) \in E\}$ (backward citation links) and $\text{Cites}(s) = \{v \in V \mid (v \to s) \in E\}$ (forward citation links).
  3. **Second-Degree Traversal ($k=2$):** Traverses references of references and citations of citations:
     $$\mathcal{N}_2(S) = \bigcup_{u \in \mathcal{N}_1(S)} \left( \text{Refs}(u) \cup \text{Cites}(u) \right)$$
* **Coordinate Mapping & Visual Layout:**
  * **X-Axis ($X_i = \text{PubDate}(P_i)$):** Deterministic temporal coordinate preventing backward chronological links from pointing rightward.
  * **Y-Axis ($Y_i = \log(\text{CitationCount}(P_i) + 1)$ or Citation Velocity):** Vertical elevation signifies cumulative academic impact or citation momentum ($\Delta \text{Citations} / \Delta t$).
  * **Node Size & Directed Edges:** Node radius scales with citation volume; directed bezier curves trace knowledge dissemination forward in time ($P_{earlier} \to P_{later}$).
* **Discover Mode Algorithm:**
  Litmaps analyzes the topological neighborhood of the active collection $S$ against the candidate frontier $\mathcal{C} = \mathcal{N}_2(S) \setminus S$. Candidates are ranked by an edge-overlap heuristic:
  $$\text{DiscoverScore}(c \in \mathcal{C}, S) = w_{in} \cdot |\text{Cites}(c) \cap S| + w_{out} \cdot |\text{Refs}(c) \cap S| + w_{sim} \cdot \text{TextSim}(c, S)$$
  This highlights "hub" papers that cite multiple seeds or "authoritative" papers cited by multiple seeds that the user missed during initial scoping.

---

### 1.2 Connected Papers: Co-Citation, Bibliographic Coupling & Metric Proximity
* **Underlying Philosophy:** Connected Papers specifically rejects displaying raw citation trees because direct citation links are sparse, biased by academic rivalries, or missing between contemporaneous competing laboratories. Instead, it measures **latent metric similarity** using co-citation and bibliographic coupling.
* **Foundational Bibliometric Metrics:**
  1. **Bibliographic Coupling (Kessler, 1963):** Two papers $A$ and $B$ are bibliographically coupled if they cite one or more common reference sources:
     $$BC(A, B) = |\text{Refs}(A) \cap \text{Refs}(B)|$$
     Normalized via Salton's Cosine:
     $$S_{BC}(A, B) = \frac{|\text{Refs}(A) \cap \text{Refs}(B)|}{\sqrt{|\text{Refs}(A)| \cdot |\text{Refs}(B)|}}$$
     *Property:* Fixed at time of publication; captures shared theoretical foundations and methodological protocols.
  2. **Co-Citation (Small, 1973):** Two papers $A$ and $B$ are co-cited if subsequent papers cite both simultaneously:
     $$CC(A, B) = |\{C \in V \mid (C \to A) \in E \land (C \to B) \in E\}|$$
     Normalized Jaccard Index:
     $$S_{CC}(A, B) = \frac{|\text{Citing}(A) \cap \text{Citing}(B)|}{|\text{Citing}(A) \cup \text{Citing}(B)|}$$
     *Property:* Dynamic over time; reflects how the scientific community perceives semantic kinship.
* **The Connected Papers Algorithmic Pipeline:**
  1. **Candidate Pool Extraction:** Given a seed paper $P_{seed}$, the engine queries Semantic Scholar Academic Graph (S2AG) to pull ~50,000 papers within 2-3 degrees of citation separation.
  2. **Top-$K$ Similarity Pruning:** A combined similarity score is computed:
     $$Sim(A, B) = \alpha \cdot S_{BC}(A, B) + (1 - \alpha) \cdot S_{CC}(A, B)$$
     The top 20–40 candidates with the highest $Sim(P_{seed}, P_i)$ are retained.
  3. **Force-Directed Graph Embedding:**
     The sub-graph of top-$K$ papers is embedded in 2D Euclidean space using a spring-electrical force model (e.g., Fruchterman-Reingold / D3-force):
     * Attractive spring force along edges: $F_a(d) = \frac{d^2}{k} \cdot Sim(A, B)$
     * Repulsive electrostatic force between all node pairs: $F_r(d) = -\frac{k^2}{d}$
     Clustered nodes reveal specialized sub-disciplines (e.g., in vitro assays vs in vivo pharmacokinetics).
* **Prior Works & Derivative Works Derivations:**
  * **Prior Works:** Papers outside the immediate graph that are cited by the highest percentage of nodes within the graph:
    $$\text{PriorScore}(u) = \sum_{v \in G_{graph}} \mathbb{I}((v \to u) \in E)$$
    Surfaces the seminal bedrock papers upon which the whole field rests.
  * **Derivative Works:** Recent papers published after the graph nodes that cite the highest percentage of nodes in the graph:
    $$\text{DerivativeScore}(w) = \sum_{v \in G_{graph}} \mathbb{I}((w \to v) \in E)$$
    Surfaces major systematic reviews, meta-analyses, and transformative next-generation breakthroughs.

---

### 1.3 ResearchRabbit: The "Spotify for Papers" Paradigm & Multi-Hop Social Topology
* **Underlying Philosophy:** Treats literature discovery as an active, recursive collaborative filtering process where user-curated collections act as "playlists" and papers act as "tracks".
* **Algorithmic Mechanics:**
  1. **Recursive Seed Centroid:** Adding or removing papers from a collection dynamically updates the centroid vector in academic embedding space:
     $$\mathbf{v}_{collection} = \frac{1}{|C|} \sum_{p \in C} \mathbf{v}_p$$
  2. **Hop-Based Exploration:**
     * **Hop 0:** The curated collection $C$.
     * **Hop 1:** Immediate direct citations ($\text{Cites}(C)$) and direct references ($\text{Refs}(C)$).
     * **Hop 2:** Neighborhoods of Hop 1 nodes.
  3. **Partitioned Views:**
     * *Earlier Work:* Filtered to $\text{Refs}(C)$ ranked by in-collection citation frequency.
     * *Later Work:* Filtered to $\text{Cites}(C)$ ranked by publication recency and citation count.
     * *Similar Work:* Filtered to bibliographically coupled and co-cited papers lacking direct citation edges with $C$.
  4. **Author Networks & Institutional Graphs:**
     Constructs a projected bipartite author collaboration graph $G_{auth} = (V_{auth}, E_{collab})$:
     * Node weight = total publications in collection topic.
     * Edge weight = count of co-authored papers between Author $X$ and Author $Y$.
     * Institutional clustering groups authors by academic affiliation, identifying dominant research consortia (e.g., Broad Institute, Charité, Tehran University of Medical Sciences).

---

### 1.4 Inciteful: Open-Source Network Science & Transparent Bibliometrics
* **Creator & Stack:** Created by Maximillian Weishuhn (`IncitefulMed` / `inciteful.xyz`). Built on pure open science principles using data from OpenCitations, Crossref, and Semantic Scholar.
* **Core Algorithmic Innovations:**
  1. **PageRank on Academic Citation DAGs:**
     While PageRank was designed for the cyclic web graph, citation graphs are strictly directed acyclic graphs (excluding corrigenda). Inciteful computes PageRank to measure structural prestige:
     $$\mathbf{PR}(u) = \frac{1 - d}{|V|} + d \sum_{v \in \text{Citing}(u)} \frac{\mathbf{PR}(v)}{|\text{Refs}(v)|}$$
     where $d \approx 0.85$. A paper cited by 3 high-impact Nature/Lancet trials receives a significantly higher PageRank than a paper cited by 50 predatory or unindexed journals.
  2. **Adamic/Adar Index for Recent State-of-the-Art Discovery:**
     *The Problem:* Newly published groundbreaking papers have had zero time to accumulate citations or PageRank, making them invisible to traditional metric ranking.
     *The Inciteful Solution:* Inciteful applies the **Adamic/Adar link prediction metric** (originally designed for social networks) to the bibliographic coupling space:
     $$AA(A, B) = \sum_{z \in \text{Refs}(A) \cap \text{Refs}(B)} \frac{1}{\log |\text{Citing}(z)|}$$
     *Why this works brilliantly:* If Paper $A$ (your seed) and Paper $B$ (published last week) both cite a hyper-generic manual (e.g., standard Cochrane Handbook, cited 100,000 times), the contribution $\frac{1}{\log(100,000)} = 0.086$ is tiny. But if both cite a highly specialized, niche 2024 crystal-structure paper cited only 3 times, the contribution $\frac{1}{\log(3)} = 0.910$ is massive! This penalizes generic noise and elevates deeply specific, contemporaneous peer papers.

---

### 1.5 Open-Source Ecosystem & Python Toolkits

| Library / Tool | Primary Data Source | Core Data Model | Key Strengths | Limitations |
| :--- | :--- | :--- | :--- | :--- |
| **`pyalex` (`openalex-python`)** | OpenAlex REST API | Works, Authors, Sources, Institutions, Concepts, Topics | Full graph navigation; `filter(cites=...)`; inverted-index abstract reconstruction; 100% free polite pool | Abstracts require reconstruction; heavy concept hierarchy |
| **`semanticscholar`** | Semantic Scholar S2AG | Paper, Author, Citation, Reference | `isInfluential` citation filtering; embedding vectors (SPECTER); citation intent | Strict rate limits without API key (1 req/sec); occasional schema shifts |
| **`habanero`** | Crossref REST API | Works, Funders, Members, Licenses | Definitive source for DOIs, funding metadata, publisher-deposited references | Citation traversal is limited compared to OpenAlex/S2AG |
| **`pybliometrics`** | Elsevier Scopus | Abstract, Author, Affiliation | Exhaustive peer-reviewed citation index; detailed citation overviews | Proprietary; strictly requires institutional Scopus API key |
| **`scholarly`** | Google Scholar | Author profiles, Search queries | Deepest gray-literature and book citation coverage | Web scraping based; frequent CAPTCHA blocking and IP bans |
| **`NetworkX` / `igraph`** | In-memory graph structures | DiGraph, MultiDiGraph, Bipartite | Native implementation of PageRank, HITS, Adamic/Adar, Betweenness, Leiden/Louvain | Memory scales with $O(V+E)$; Python execution overhead for $>10^6$ edges |

---

## 2. Graph-RAG & Knowledge Graph Frameworks for Scientific Literature

Standard Retrieval-Augmented Generation (RAG) splits text into isolated chunks (typically 256–512 tokens), embeds them into dense vector space, and retrieves the top-$K$ cosine matches. This fails disastrously for complex scientific proposals because:
1. It suffers from **semantic myopia** (cannot synthesize thematic patterns across 50 papers).
2. It lacks **topological provenance** (cannot verify whether Paper A actually cites Paper B or merely shares vocabulary).
3. It cannot resolve **entity-relationship cascades** (e.g., Drug X inhibits Protein Y, which downregulates Pathway Z, which suppresses Phenotype W).

### 2.1 Microsoft GraphRAG: Hierarchical Leiden Community Summaries
* **Primary Source:** Edge, D., et al. (2024). *"From Local to Global: A Graph RAG Approach to Query-Focused Summarization."* `arXiv:2404.16130`.
* **Architectural Mechanics:**
  1. **Source Text Chunking:** Input literature corpus is partitioned into large chunks (~600–1200 tokens).
  2. **Domain-Specific Entity & Relationship Extraction:** An LLM extracts named entities (Nodes: Genes, Proteins, Diseases, Drugs, Assays) and claims/relationships (Directed Edges with textual description and weight).
  3. **Covariate Claim Extraction:** Extracts explicit factual assertions anchored to source text spans.
  4. **Hierarchical Leiden Community Detection:** Applies the Leiden graph clustering algorithm to partition the knowledge graph into hierarchical communities across multiple resolution levels:
     * Level 0: Granular, highly specialized protein-protein interaction clusters.
     * Level 1: Cellular pathway modules (e.g., DNA Damage Repair, PI3K/AKT signaling).
     * Level 2: Broad disease and therapeutic domain modules (e.g., Oncology, Targeted Chemoresistance).
  5. **Pre-Computed Community Summaries:** The LLM generates a comprehensive, executive synthesis for each community at each level of the hierarchy.
  6. **Dual Query Modes:**
     * **Local Search:** For entity-specific questions ("What is the affinity of Olaparib for PARP1?"). Traverses 1-hop and 2-hop entity neighborhoods and local community summaries.
     * **Global Search:** For broad thematic synthesis ("What are the main mechanisms of acquired resistance to PARP inhibitors in homologous recombination-proficient tumors?"). Executes a **Map-Reduce** sweep over high-level Leiden community summaries, synthesizing a complete multi-paper landscape without scanning raw text chunks.

---

### 2.2 FutureHouse PaperQA2 & LitQA2: Gather-Score-Cite & Claim Entailment
* **Primary Source:** Skarlinski, M. D., et al. (2024). *"Language agents achieve superhuman synthesis of scientific knowledge."* `arXiv:2409.13740`.
* **Architectural Mechanics:**
  1. **Gather Stage:** Hybrid retrieval executing lexical BM25 queries and dense vector searches across full-text scientific paper PDFs and XMLs.
  2. **Score Stage:** Instead of feeding raw retrieved chunks into an answer generator, a scoring agent prompts an LLM to evaluate each individual passage on a 0–10 relevance scale:
     * Does this passage contain direct empirical evidence relevant to the research query?
     * Extracts an exact evidence quote from the chunk.
  3. **Cite Stage:** High-scoring passages are provided to the synthesis LLM with explicit citation tags `[Author, Year, ID]`. The model is instructed under strict zero-shot constraints:
     * Never assert a scientific fact without an inline citation tag.
     * Every citation tag must directly support the preceding sentence.
  4. **Post-Hoc Verification & LitQA2 Benchmark:**
     * *LitQA2:* An 800+ question scientific benchmark demanding exact, verifiable answers derived exclusively from primary literature.
     * PaperQA2 incorporates a secondary **adversarial claim-checking subagent** that verifies semantic entailment:
       $$\text{Entails}(\text{Passage}_{cited}, \text{SynthesizedSentence}) \in \{\text{True}, \text{False}\}$$
       Any unentailed or hallucinated sentence is rejected and rewritten.

---

### 2.3 Programmatic Citation Network Traversal via Free REST APIs

#### A. OpenAlex Works API (Polite Pool, Free, 100M+ Works)
* **Endpoint Base:** `https://api.openalex.org/works`
* **Polite Pool Header:** Append `?mailto=researcher@university.edu` for 10 requests/second with zero cost.
* **Backward Citation Traversal (References):**
  A fetched Work object contains:
  ```json
  {
    "id": "https://openalex.org/W2741809807",
    "doi": "https://doi.org/10.1038/s41586-020-2649-2",
    "title": "Structural basis of transcription-translation coupling",
    "publication_year": 2020,
    "referenced_works": [
      "https://openalex.org/W1983749823",
      "https://openalex.org/W2094857201"
    ],
    "referenced_works_count": 54
  }
  ```
  Fetching all backward references in a single batch request:
  `GET https://api.openalex.org/works?filter=openalex_id:W1983749823|W2094857201`
* **Forward Citation Traversal (Citing Papers):**
  To find all papers citing `W2741809807` sorted by citation impact:
  `GET https://api.openalex.org/works?filter=cites:W2741809807&sort=cited_by_count:desc&per-page=50`

#### B. Semantic Scholar Academic Graph (S2AG) API
* **Endpoint Base:** `https://api.semanticscholar.org/graph/v1/paper/{paper_id}`
* **Query Parameters:** `fields=paperId,title,year,citationCount,influentialCitationCount,references.paperId,references.title,references.isInfluential,citations.paperId,citations.title,citations.isInfluential`
* **Influential Citation Filtering:** S2AG uses a machine-learned classifier to label citations where the citing paper actually builds upon the method or findings of the cited paper (`isInfluential: true`), filtering out superficial passing mentions.

#### C. Europe PMC REST API
* **Backward References:** `https://www.ebi.ac.uk/europepmc/webservices/rest/{source}/{extId}/references?format=json`
* **Forward Citations:** `https://www.ebi.ac.uk/europepmc/webservices/rest/{source}/{extId}/citations?format=json`

#### D. NCBI PubMed E-Utilities
* **Backward & Forward Linkage via `elink.fcgi`:**
  * Backward references: `dbfrom=pubmed&db=pubmed&id={pmid}&linkname=pubmed_pubmed_refs`
  * Forward citations: `dbfrom=pubmed&db=pubmed&id={pmid}&linkname=pubmed_pubmed_citedin`
  * Related articles (PubMed co-occurrence algorithm): `dbfrom=pubmed&db=pubmed&id={pmid}&linkname=pubmed_pubmed`

---

### 2.4 Markdown Bi-Directional Link Graphs (Obsidian & Logseq)
* **Local Graph Modeling:**
  Academic literature notes are stored as plain Markdown files (`.md`).
  * YAML Frontmatter defines node metadata:
    ```yaml
    ---
    id: PMID_32832599
    doi: 10.1038/s41586-020-2649-2
    title: "Structural basis of transcription-translation coupling"
    year: 2020
    journal: Nature
    type: Primary_Article
    targets: ["[[RNAP]]", "[[Ribosome]]", "[[NusG]]"]
    pathways: ["[[Transcription]]", "[[Translation_Coupling]]"]
    ---
    ```
  * In-text Wikilinks define directed semantic edges:
    `According to [[PMID_32832599]], transcription factor [[NusG]] physically links [[RNAP]] to [[Ribosome]].`
* **Parsing Mechanics to NetworkX:**
  ```python
  import re, frontmatter, networkx as nx
  from pathlib import Path

  def parse_markdown_vault(vault_dir: Path) -> nx.DiGraph:
      G = nx.DiGraph()
      wikilink_re = re.compile(r'\[\[([^\]\|#]+)(?:#[^\]\|]+)?(?:\|[^\]]+)?\]\]')
      
      for md_file in vault_dir.rglob("*.md"):
          post = frontmatter.load(md_file)
          node_id = md_file.stem
          G.add_node(node_id, **post.metadata)
          
          # Extract body wikilinks
          body_links = wikilink_re.findall(post.content)
          for target in body_links:
              G.add_edge(node_id, target.strip(), type="WIKILINK")
      return G
  ```

---

## 3. Bridging Bibliographic Citation Graphs with Biomedical Semantic Concept Graphs

A critical epistemic flaw in existing discovery tools is the complete separation between:
1. **Bibliographic Citation Graph ($G_{bib}$):** Paper-to-Paper links based purely on citations.
2. **Biomedical Knowledge Graph ($G_{bio}$):** Entity-to-Entity links based on biological ontology (Drug $\to$ Target $\to$ Pathway $\to$ Disease).

A proposal planner cannot evaluate scientific feasibility solely by knowing that Paper A cites Paper B; it must understand **why** they are linked (e.g., Paper A tested Compound X on Cell Line Y, whereas Paper B showed Target Z causes Resistance to Compound X).

```
========================================================================================
             DUAL-LAYER HETEROGENEOUS INFORMATION NETWORK (HIN)
========================================================================================

  [MACRO-LEVEL: BIBLIOGRAPHIC CITATION GRAPH (Paper-to-Paper)]
  
       Paper P1 (Seed: 2021) ─────────── cites ───────────► Paper P2 (2018)
          │            ▲                                        │
          │            │                                        │
      co-cites    bib-coupled                                 cites
          │            │                                        │
          ▼            │                                        ▼
       Paper P3 (2023) ◄─────────────────────────────────── Paper P4 (Foundational)
          │                                                     │
          │ (asserts)                                           │ (asserts)
          ▼                                                     ▼
  ──────────────────────────────────────────────────────────────────────────────────────
  [BIPARTITE PROJECTION LAYER: CLAIMS & EVIDENCE EXTRACTION]
  ──────────────────────────────────────────────────────────────────────────────────────
          │                                                     │
          ▼                                                     ▼
  [MICRO-LEVEL: BIOMEDICAL MECHANISTIC KNOWLEDGE GRAPH (Entity-to-Entity)]
  
   [Drug: Olaparib] ──── inhibits ────► [Target: PARP1]
          │                                    │
          │ synergizes_with                    │ participates_in
          ▼                                    ▼
   [Drug: AZD6738]  ─── inhibits ────►  [Target: ATR] ────► [Pathway: DNA Repair]
                                                                   │
                                                              dysregulated_in
                                                                   │
                                                                   ▼
                                                            [Disease: TNBC]
========================================================================================
```

### 3.1 Formal Definition of the Heterogeneous Information Network (HIN)
We define the Literature-Biomedical Graph as $\mathcal{H} = (V, E, \mathcal{T}_v, \mathcal{T}_e)$ where:
* **Node Types $\mathcal{T}_v$:** $\{\text{Paper}, \text{Drug}, \text{Protein/Gene}, \text{Pathway}, \text{Disease}, \text{AssayEndpoint}\}$
* **Edge Types $\mathcal{T}_e$:**
  * Bibliographic: $\{\text{CITES}, \text{CO_CITED_WITH}, \text{BIBLIOGRAPHIC_COUPLING}\}$
  * Bipartite: $\{\text{ASSERTS_FINDING}, \text{BENCHMARKS_PROTOCOL}\}$
  * Mechanistic: $\{\text{INHIBITS}, \text{ACTIVATES}, \text{PARTICIPATES_IN}, \text{DYSREGULATED_IN}, \text{MEASURED_BY}\}$

### 3.2 Meta-Path Analysis for Proposal Feasibility
Using Meta-Paths across $\mathcal{H}$, the agent can compute semantic proximity between an intervention and a clinical disease:
$$\text{Meta-Path } \mathcal{M} = \text{Paper}_1 \xrightarrow{\text{ASSERTS}} \text{Drug} \xrightarrow{\text{INHIBITS}} \text{Target} \xrightarrow{\text{PARTICIPATES_IN}} \text{Pathway} \xleftarrow{\text{ASSERTS}} \text{Paper}_2$$
This allows `proposal-nevisi` to uncover hidden mechanistic synergies between two compounds even if no prior published paper has ever directly co-cited or combined them!

---

### 3.3 Graph Algorithms for Scientific Paper Ranking & Node Importance

#### A. Personalized PageRank (PPR) with Seed Teleportation
Standard PageRank distributes random surfer restarts uniformly across the entire graph. In **Personalized PageRank**, the restart vector $\mathbf{v}_0$ is concentrated strictly on the user's seed papers $S$:
$$\mathbf{p}_{t+1} = (1 - \alpha) \mathbf{M} \mathbf{p}_t + \alpha \mathbf{v}_0$$
where:
* $\mathbf{M}_{ij} = \frac{1}{|\text{Refs}(j)|}$ if paper $j$ cites paper $i$, else $0$.
* $\alpha \in [0.15, 0.20]$ is the teleportation probability.
* $\mathbf{v}_0(i) = \frac{1}{|S|}$ if $i \in S$, else $0$.
*Convergence:* Iterated until $\|\mathbf{p}_{t+1} - \mathbf{p}_t\|_1 < 10^{-6}$. Papers with the highest stationary probability $\mathbf{p}^*(u)$ are mathematically guaranteed to be the most structurally central works relevant to the seed topic.

#### B. Kleinberg's HITS Algorithm (Hubs & Authorities)
In scientific literature:
* **Authority ($a_i$):** Landmark clinical trials, seminal biological discoveries, and canonical assay benchmarks. Cited by many high-quality hubs.
* **Hub ($h_i$):** Comprehensive systematic reviews, meta-analyses, and scoping studies. Cites many authoritative works.
The iterative update rules:
$$a_i^{(k)} = \sum_{j : (j \to i) \in E} h_j^{(k-1)}, \quad h_j^{(k)} = \sum_{i : (j \to i) \in E} a_i^{(k)}$$
followed by $L_2$ normalization at each iteration:
$$\mathbf{a}^{(k)} \leftarrow \frac{\mathbf{a}^{(k)}}{\|\mathbf{a}^{(k)}\|_2}, \quad \mathbf{h}^{(k)} \leftarrow \frac{\mathbf{h}^{(k)}}{\|\mathbf{h}^{(k)}\|_2}$$

#### C. Temporal Decay & NIH Relative Citation Ratio (RCR)
Raw citation count is heavily biased toward older papers. To rectify this, `proposal-nevisi` applies an exponential half-life discount:
$$\text{Score}_{temporal}(P) = \text{CitationCount}(P) \cdot e^{-\lambda \cdot (T_{current} - T_{pub}(P))}$$
where $\lambda = \frac{\ln(2)}{t_{1/2}}$ (with medical literature half-life $t_{1/2} \approx 4.0$ years).
Furthermore, we integrate the **NIH Relative Citation Ratio (RCR)** concept:
$$\text{RCR}(P) = \frac{\text{Actual Citation Rate of Paper } P}{\text{Expected Citation Rate of Co-Citation Benchmark Network}}$$
An $\text{RCR} > 1.0$ indicates above-average field-normalized influence; landmark papers typically display $\text{RCR} > 5.0$.

#### D. Hummon & Doreian's Main Path Analysis (Search Path Count - SPC)
* **Primary Source:** Hummon, N. P., & Doreian, P. (1989). *"Connectivity in a Citation Network: The Development of DNA Theory."* Social Networks, 11(1), 39-63.
* **Mechanism:** In the DAG of scientific citations, every path from an origin node (a root paper with in-degree 0) to a terminal node (a recent paper with out-degree 0) represents a trajectory of scientific thought.
* The **Search Path Count (SPC)** algorithm computes how many total source-to-sink paths pass through each directed citation edge $e = (u, v)$:
  $$\text{SPC}(u \to v) = N_{sources}(u) \times N_{sinks}(v)$$
  where $N_{sources}(u)$ is the count of paths from all network roots to $u$, and $N_{sinks}(v)$ is the count of paths from $v$ to all network sinks.
* Tracing the sequence of edges with the maximal SPC from roots to sinks isolates the **Main Scientific Backbone Trajectory**, stripping away peripheral or dead-end studies.

#### E. Betweenness Centrality & Pivotal Bridge Detection
Betweenness centrality identifies multidisciplinary bridge papers that link separate citation clusters:
$$C_B(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$$
where $\sigma_{st}$ is the total number of shortest paths from node $s$ to node $t$, and $\sigma_{st}(v)$ is the number of those paths that pass through $v$.
*Application:* In biomedical proposal design, high-betweenness papers frequently represent cross-disciplinary innovations (e.g., applying single-cell RNA-seq algorithms to cardiac fibrosis).

---

## 4. Actionable Architecture Blueprint for `proposal-nevisi`

### 4.1 System Topology: The Seed-to-Graph Literature Expansion Engine
The new engine (`citation_graph_engine.py`) operates as a specialized submodule coordinated by `generic_search_planner.py` and federated via `scientific_search_adapter.py`.

```
========================================================================================
           `proposal-nevisi` SEED-TO-GRAPH EXPANSION PIPELINE
========================================================================================

  [PROPOSAL_SPEC.json / Research Dossier]
                   │
                   ▼ (1-3 Seed PMIDs / DOIs)
  ┌────────────────────────────────────────────────────────┐
  │ Step 1: Federated Seed Metadata Resolution             │
  │ (OpenAlex + Europe PMC + PubMed E-Utilities)           │
  └────────────────────────┬───────────────────────────────┘
                           │
                           ▼
  ┌────────────────────────────────────────────────────────┐
  │ Step 2: 2-Hop Bidirectional Citation Harvesting        │
  │ - Backward: OpenAlex `referenced_works` (Lineage)       │
  │ - Forward: OpenAlex `filter=cites:...` (Replications)   │
  │ - Lateral: Europe PMC / PubMed Related Articles        │
  └────────────────────────┬───────────────────────────────┘
                           │
                           ▼
  ┌────────────────────────────────────────────────────────┐
  │ Step 3: Metric Graph Construction & Adamic/Adar Matrix │
  │ - Co-citation & Bibliographic Coupling calculation     │
  │ - Adamic/Adar link prediction for recent papers         │
  └────────────────────────┬───────────────────────────────┘
                           │
                           ▼
  ┌────────────────────────────────────────────────────────┐
  │ Step 4: Graph Centrality & Ranking Execution           │
  │ - Personalized PageRank (teleporting to seeds)         │
  │ - Kleinberg HITS (Hubs vs Authorities)                 │
  │ - Main Path Analysis (SPC Backbone Trajectory)         │
  └────────────────────────┬───────────────────────────────┘
                           │
                           ▼
  ┌────────────────────────────────────────────────────────┐
  │ Step 5: Biomedical Entity Annotation & Bipartite Map   │
  │ - MeSH / Concept alignment (Drugs, Targets, Diseases)  │
  │ - Claim Entailment Verification against Abstract Spans │
  └────────────────────────┬───────────────────────────────┘
                           │
                           ▼
  ┌────────────────────────────────────────────────────────┐
  │ Step 6: Output Artifact Generation                     │
  │ 1. `LITERATURE_CITATION_GRAPH.json` (Structured Store) │
  │ 2. `LITERATURE_CITATION_GRAPH.html` (Cytoscape.js UI)  │
  │ 3. Pruned Top-25 Reference Ingestion for Proposal      │
  └────────────────────────────────────────────────────────┘
========================================================================================
```

---

### 4.2 Comprehensive JSON Schema: `LITERATURE_CITATION_GRAPH.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "LiteratureCitationGraph",
  "type": "object",
  "required": ["metadata", "nodes", "edges", "clusters", "main_path"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["topic_query", "generation_timestamp", "seed_ids", "metrics"],
      "properties": {
        "topic_query": {"type": "string"},
        "generation_timestamp": {"type": "string", "format": "date-time"},
        "seed_ids": {"type": "array", "items": {"type": "string"}},
        "metrics": {
          "type": "object",
          "properties": {
            "total_nodes": {"type": "integer"},
            "total_edges": {"type": "integer"},
            "density": {"type": "number"},
            "diameter": {"type": "integer"}
          }
        }
      }
    },
    "nodes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "title", "year", "citation_count", "scores", "is_seed"],
        "properties": {
          "id": {"type": "string", "description": "Persistent ID: PMID:xxxxx or DOI:xxxx or OpenAlex:Wxxxx"},
          "doi": {"type": ["string", "null"]},
          "pmid": {"type": ["string", "null"]},
          "openalex_id": {"type": ["string", "null"]},
          "title": {"type": "string"},
          "journal": {"type": "string"},
          "year": {"type": "integer"},
          "authors": {"type": "array", "items": {"type": "string"}},
          "abstract": {"type": "string"},
          "citation_count": {"type": "integer"},
          "influential_citation_count": {"type": "integer"},
          "is_seed": {"type": "boolean"},
          "category": {
            "type": "string",
            "enum": [
              "SYSTEMATIC_REVIEW_META_ANALYSIS",
              "CLINICAL_PRACTICE_GUIDELINE",
              "HISTORICAL_LANDMARK",
              "HIGHLY_CITED_FOUNDATIONAL",
              "RECENT_HIGH_IMPACT",
              "KEY_METHODOLOGICAL",
              "CONTRADICTORY_NULL_RESULT",
              "EXPLORATORY_ANCHOR"
            ]
          },
          "scores": {
            "type": "object",
            "properties": {
              "personalized_pagerank": {"type": "number"},
              "authority_score": {"type": "number"},
              "hub_score": {"type": "number"},
              "adamic_adar_proximity": {"type": "number"},
              "recency_weighted_impact": {"type": "number"},
              "composite_rank": {"type": "integer"}
            }
          },
          "biomedical_entities": {
            "type": "object",
            "properties": {
              "interventions_drugs": {"type": "array", "items": {"type": "string"}},
              "targets_genes": {"type": "array", "items": {"type": "string"}},
              "cellular_pathways": {"type": "array", "items": {"type": "string"}},
              "diseases_conditions": {"type": "array", "items": {"type": "string"}},
              "assay_endpoints": {"type": "array", "items": {"type": "string"}}
            }
          }
        }
      }
    },
    "edges": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["source", "target", "edge_type", "weight"],
        "properties": {
          "source": {"type": "string"},
          "target": {"type": "string"},
          "edge_type": {
            "type": "string",
            "enum": ["CITES", "CO_CITED_WITH", "BIBLIOGRAPHIC_COUPLING", "MECHANISTIC_SYNERGY"]
          },
          "weight": {"type": "number"},
          "evidence_context": {"type": ["string", "null"]}
        }
      }
    },
    "clusters": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "cluster_id": {"type": "integer"},
          "cluster_label": {"type": "string"},
          "dominant_concepts": {"type": "array", "items": {"type": "string"}},
          "node_ids": {"type": "array", "items": {"type": "string"}}
        }
      }
    },
    "main_path": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Ordered sequence of node IDs defining the Hummon-Doreian Search Path Count backbone"
    }
  }
}
```

---

### 4.3 Interactive Visualizer: Standalone HTML with Cytoscape.js (`LITERATURE_CITATION_GRAPH.html`)
The engine generates a 100% self-contained HTML file requiring zero external servers, using CDN Cytoscape.js or inlined JS:
* **Visualization Features:**
  * **Layout Engine:** Cytoscape `cose` (Compound Spring Embedder) with customizable physics parameters (ideal edge length: 100, repulsion: 4500).
  * **Node Styling:**
    * Color gradient based on publication year (e.g., `#2b5c8f` deep blue for foundational $\le 2018$ to `#e65100` vivid amber for recent 2024–2026).
    * Node diameter dynamically scaled by Personalized PageRank score ($15\text{px}$ to $55\text{px}$).
    * Seed papers marked with a thick crimson outer halo (`border-width: 4px; border-color: #d32f2f`).
  * **Edge Styling:**
    * Directed solid arrows for direct citations (`edge_type: "CITES"`).
    * Translucent dashed lines for strong bibliographic coupling (`edge_type: "BIBLIOGRAPHIC_COUPLING"`).
  * **Dual-View Switcher:**
    * Toggle between **"Macro Citation View"** (paper-to-paper network) and **"Micro Mechanistic View"** (bipartite network showing Drug $\to$ Target $\to$ Pathway nodes).
  * **Side Inspector Panel:**
    Clicking any node displays:
    1. Bibliographic details (Title, Authors, Journal, Year, DOI, PMID).
    2. Computed Metrics (Personalized PageRank, HITS Authority, Adamic/Adar similarity).
    3. Extracted Biological Mechanisms & Claims.
    4. Verified Abstract text with highlighting of key quantitative endpoints.

---

### 4.4 Verification Gates Against Hallucination & Citation Drift

To preserve the uncompromising rigor of `proposal-nevisi`, the citation graph is governed by four fail-closed automated verification gates:

```
┌────────────────────────────────────────────────────────────────────────┐
│               ANTI-HALLUCINATION & RIGOR GATE PIPELINE                 │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Persistent ID & Endpoint Verification Gate                          │
│    - Rule: Every node must possess a valid, resolvable DOI or PMID.    │
│    - Check: Hits PubMed E-utilities or OpenAlex REST API. Zero         │
│      invented DOIs (e.g., 10.1016/j.fake.2024.001) permitted.         │
├────────────────────────────────────────────────────────────────────────┤
│ 2. Ground-Truth Citation Edge Validation Gate                          │
│    - Rule: Every directed citation edge (A -> B) must be physically    │
│      present in OpenAlex `referenced_works` or Europe PMC reference.   │
│    - Check: No edges synthesized from LLM parametric memory.           │
├────────────────────────────────────────────────────────────────────────┤
│ 3. Span-Level Claim Entailment Gate                                    │
│    - Rule: Any factual finding attributed to a graph node must be      │
│      semantically entailed by its retrieved abstract text.             │
│    - Check: Evaluated via `generic_claim_entailment_engine.py`.        │
├────────────────────────────────────────────────────────────────────────┤
│ 4. Six-Category Citation Drift Audit (core_policies.py)                │
│    - Blocks: OVERSTATEMENT, CITATION_DRIFT, CONTEXT_MISMATCH,         │
│      SELECTIVE_CITATION, CORRELATION_TO_CAUSATION.                     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Complete Production-Grade Python Implementation (`citation_graph_engine.py`)

Below is the complete, dependency-free reference implementation designed to drop directly into `g:\دانشگاه\پژوهش\طرح1\.agents\skills\proposal-nevisi\scripts\citation_graph_engine.py`. It uses only the Python standard library, with graceful optional fallback to `networkx` if available.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
citation_graph_engine.py - Academic Citation Graph & Semantic Literature Discovery Engine
Proposal-Nevisi Engine v12.0 (Cognitive Multi-Agent Architecture)

Implements:
1. Bidirectional Citation Network Traversal (Backward references & Forward citations).
2. Bibliographic Coupling & Co-Citation Strength Matrices.
3. Adamic/Adar Index for Contemporaneous State-of-the-Art Paper Discovery.
4. Personalized PageRank (PPR) with Seed Paper Teleportation.
5. Kleinberg's HITS Algorithm (Hubs & Authorities).
6. Hummon & Doreian's Main Path Analysis (Search Path Count - SPC).
7. Standalone Cytoscape.js Interactive HTML Visualizer Generator.
8. Zero-Hallucination Persistent Identifier (PID) and Edge Ground-Truth Verification.

100% Dependency-Free (Pure Standard Library with optional NetworkX acceleration).
"""

import os
import sys
import json
import math
import time
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, List, Any, Optional, Set, Tuple

class CitationGraphEngine:
    """Production-grade bibliometric citation network analysis and discovery engine."""

    OPENALEX_WORKS_URL = "https://api.openalex.org/works"
    EUROPE_PMC_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest"

    def __init__(self, polite_email: str = "proposal-nevisi@research-institute.ac.ir"):
        self.polite_email = polite_email
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.adjacency_out: Dict[str, Set[str]] = {}  # u -> set(v) where u cites v (Refs)
        self.adjacency_in: Dict[str, Set[str]] = {}   # v -> set(u) where u cites v (Citations)
        self.seed_ids: Set[str] = set()

    # =========================================================================
    # 1. API HARVESTING & TRAVERSAL
    # =========================================================================

    def _fetch_url_json(self, url: str) -> Optional[Dict[str, Any]]:
        """Performs HTTP GET with polite user agent, timeout, and backoff."""
        headers = {
            "User-Agent": f"proposal-nevisi-citation-engine/12.0 (mailto:{self.polite_email})"
        }
        req = urllib.request.Request(url, headers=headers)
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=12) as resp:
                    if resp.status == 200:
                        return json.loads(resp.read().decode("utf-8"))
            except Exception as e:
                time.sleep(1.0 * (attempt + 1))
        return None

    def add_seed_paper(self, identifier: str) -> Optional[str]:
        """Resolves seed paper by PMID, DOI, or OpenAlex ID and registers it."""
        clean_id = identifier.strip()
        work = None
        if clean_id.startswith("10."):
            url = f"{self.OPENALEX_WORKS_URL}/https://doi.org/{clean_id}?mailto={self.polite_email}"
            work = self._fetch_url_json(url)
        elif clean_id.isdigit():
            url = f"{self.OPENALEX_WORKS_URL}/pmid:{clean_id}?mailto={self.polite_email}"
            work = self._fetch_url_json(url)
        elif clean_id.startswith("W"):
            url = f"{self.OPENALEX_WORKS_URL}/{clean_id}?mailto={self.polite_email}"
            work = self._fetch_url_json(url)

        if not work or "id" not in work:
            return None

        node_id = self._ingest_openalex_work(work, is_seed=True)
        if node_id:
            self.seed_ids.add(node_id)
        return node_id

    def _ingest_openalex_work(self, item: Dict[str, Any], is_seed: bool = False) -> str:
        """Parses OpenAlex raw work object into normalized node."""
        raw_id = item.get("id", "")
        node_id = raw_id.replace("https://openalex.org/", "").strip()
        if not node_id:
            node_id = str(item.get("doi", "")).lower()

        if node_id in self.nodes:
            if is_seed:
                self.nodes[node_id]["is_seed"] = True
            return node_id

        # Reconstruct abstract from inverted index
        abstract_text = ""
        inv_idx = item.get("abstract_inverted_index")
        if inv_idx and isinstance(inv_idx, dict):
            words = []
            for word, positions in inv_idx.items():
                for pos in positions:
                    words.append((pos, word))
            words.sort(key=lambda x: x[0])
            abstract_text = " ".join([w[1] for w in words])

        authors = []
        for authorship in item.get("authorships", []):
            author_obj = authorship.get("author", {})
            name = author_obj.get("display_name")
            if name:
                authors.append(name)

        doi = item.get("doi")
        if doi and "doi.org/" in doi:
            doi = doi.split("doi.org/")[-1].strip().lower()

        pmid = None
        for loc in item.get("locations", []):
            source = loc.get("source") or {}
            ext_ids = item.get("ids", {})
            if "pmid" in ext_ids:
                pmid = str(ext_ids["pmid"]).replace("https://pubmed.ncbi.nlm.nih.gov/", "").strip()

        referenced_works = [
            rw.replace("https://openalex.org/", "").strip()
            for rw in item.get("referenced_works", [])
        ]

        self.nodes[node_id] = {
            "id": node_id,
            "doi": doi,
            "pmid": pmid,
            "openalex_id": node_id,
            "title": item.get("title") or "Untitled",
            "journal": (item.get("primary_location", {}) or {}).get("source", {}).get("display_name") or "Unknown",
            "year": item.get("publication_year") or 0,
            "authors": authors[:6],
            "abstract": abstract_text[:1200],
            "citation_count": item.get("cited_by_count", 0),
            "referenced_works": referenced_works,
            "is_seed": is_seed,
            "scores": {}
        }

        if node_id not in self.adjacency_out:
            self.adjacency_out[node_id] = set()
        if node_id not in self.adjacency_in:
            self.adjacency_in[node_id] = set()

        return node_id

    def expand_graph_bidirectional(self, max_refs_per_seed: int = 25, max_cites_per_seed: int = 25):
        """Executes 1-hop backward and forward expansion for all active seeds."""
        for seed_id in list(self.seed_ids):
            seed_data = self.nodes.get(seed_id)
            if not seed_data:
                continue

            # 1. Backward Chaining (References)
            ref_ids = seed_data.get("referenced_works", [])[:max_refs_per_seed]
            if ref_ids:
                filter_str = "|".join(ref_ids[:25])
                url = f"{self.OPENALEX_WORK
<truncated 18591 bytes>

NOTE: The output was truncated because it was too long. Use a more targeted query or a smaller range to get the information you need.