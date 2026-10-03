# SEARCH POLICY & PROTOCOL
## Universal Dual-Path Literature Search, Saturation, and Boundary Accounting

**Policy Version:** 8.0  
**Scope:** Universal Biomedical, Clinical, and Translational Proposals  
**Governing Principle:** Evidence-Seeking vs. Confirmation-Seeking Retrieval  

---

## 1. Dual-Path Evidence Retrieval Architecture

Traditional literature searches in automated agents suffer from confirmation bias: querying only the positive formulation of a hypothesis (e.g., `"drug X inhibits cancer Y"`), which systematically retrieves supporting publications while overlooking negative findings, off-target toxicity, and replication failures.

Under this policy, every search plan **must formulate and execute two independent, concurrent search paths**:

```text
                                HYPOTHESIS
                                    │
           ┌────────────────────────┴────────────────────────┐
           ▼                                                 ▼
   SUPPORTING PATH                                   CONTRADICTING PATH
[ SUPPORTING_SEARCH ]                             [ CONTRADICTING_SEARCH ]
Probes: efficacy, activation,                     Probes: null results, failure to replicate,
synergy, therapeutic index,                       antagonism, resistance, dose-limiting toxicity,
and biomarker elevation.                          subadditivity, and off-target adverse effects.
```

---

## 2. The 8-Facet Query Matrix Architecture

Every research project generates a structured `QUERY_MATRIX.json` spanning eight systematic query categories:

### Facet A: Direct Evidence Queries
- Focus: Studies addressing the exact research question, intervention combination, or clinical diagnostic protocol.
- Example: `("Target Intervention" AND "Target Condition" AND "Target Model")`.

### Facet B: Component Evidence Queries
- Focus: Independent evaluations of each isolated intervention, comparator, disease model, or diagnostic tool.
- Ensures robust baseline knowledge for all elements in multi-arm or combination studies.

### Facet C: Combination & Interaction Queries
- Focus: Investigates interactions, drug-drug compatibility, synergy metrics (e.g., Combination Index, Bliss independence), or antagonistic interactions.

### Facet D: Mechanistic Queries
- Focus: Interrogates upstream molecular targets, downstream signaling cascades, phosphorylation events, receptor binding, and pathway crosstalk.

### Facet E: Translational & Cross-Model Queries
- Focus: Evaluates biological consistency across the translational continuum: in vitro cell lines $\rightarrow$ organoids $\rightarrow$ animal models $\rightarrow$ human clinical trials.

### Facet F: Negative & Null Evidence Queries
- Focus: Dedicated searches for publications reporting null outcomes, lack of efficacy, failed endpoints, and non-significant statistical findings.
- Search syntax mandates terms such as: `("no significant effect" OR "failed to inhibit" OR "ineffective" OR "lack of efficacy" OR "null response")`.

### Facet G: Safety, Toxicity & Limitation Queries
- Focus: Adverse event profiles, cytotoxic thresholds, off-target tissue damage, immunogenicity, and pharmacokinetic clearance limits.

### Facet H: Methodological & Confounder Queries
- Focus: Standardized assays, vehicle/solvent artifacts, assay interference (e.g., optical absorbance interference in viability dyes), and replicate reproducibility.

---

## 3. Multi-Database Integration & Hierarchy

Searches must be federated across distinct bibliographic and registry sources to ensure cross-database coverage:

1. **PubMed / MEDLINE:** Primary repository for peer-reviewed biomedical literature and controlled MeSH indexing.
2. **Europe PMC:** Extended repository providing open-access full-text XML, supplementary datasets, and preprint indexing.
3. **OpenAlex:** Comprehensive scholarly graph used for citation tracking, institutional attribution, and citation chaining.
4. **Crossref:** Official DOI registry for definitive metadata verification, publication date confirmation, and errata/retraction checks.

---

## 4. Citation Chaining Protocol

For all foundational and seminal primary papers identified:
1. **Backward Chaining:** Inspect the bibliography of the paper to retrieve historical methodology and foundational baseline evidence.
2. **Forward Chaining:** Query OpenAlex and Crossref to identify recent citing articles that have replicated, extended, or challenged the original findings.
3. **Related Articles Discovery:** Retrieve semantically related studies to identify alternative mechanistic explanations.

---

## 5. Search Saturation & PRISMA Accounting

A search is deemed **saturated** only when:
- All 8 query facets have executed across target databases.
- Both forward and backward citation chaining have concluded.
- Additional search iterations across standard synonyms yield $> 90\%$ duplicate records.
- Negative evidence queries have been exhausted.

### PRISMA 2020 Accounting Rules:
All search operations must record exact counts in `SEARCH_QUERY_LOG.json` and compile a verifiable `PRISMA_FLOW_DATA.json`:
- $N_{\text{retrieved}}$: Raw records returned by query strings across each database.
- $N_{\text{duplicates}}$: Exact deduplicated count based on matching DOI or PMID.
- $N_{\text{screened}}$: Total unique titles and abstracts evaluated against eligibility criteria.
- $N_{\text{excluded}}$: Records excluded during screening, classified by explicit exclusion reasons.
- $N_{\text{fulltext}}$: Number of eligible records sought for full-text extraction.
- $N_{\text{included}}$: Final synthesis cohort.

*Prohibition:* Fabricating or guessing PRISMA numbers is strictly prohibited. If API or network interruptions occur, the ledger must record `PRISMA_DATA_INCOMPLETE` with specific missing source logs.

---

## 6. The "Absence of Evidence" Epistemic Rule

When exhaustive negative evidence searches yield no contradictory publications, the system **must never state**:
> *"No contradictory evidence exists in the scientific literature."*

Because absence of evidence is not evidence of absence, the system must strictly document:
> `NO_RELEVANT_CONTRADICTING_EVIDENCE_IDENTIFIED_WITHIN_SEARCH_BOUNDARY`

The statement must be bounded by the databases queried, the date range, and the explicit keywords executed.

---

## 7. Search Failure & Interruption Protocol

If third-party APIs (PubMed E-utilities, Europe PMC, Crossref) encounter rate limits, network timeouts, or downtime:
1. The engine records a persistent incident entry: `SOURCE_UNAVAILABLE` or `SEARCH_INCOMPLETE`.
2. The engine must not fabricate synthetic search results or extrapolate bibliographic data.
3. Synthesis pipelines downstream are formally notified to downgrade claim certainty to `INSUFFICIENT_SEARCH_COVERAGE`.
