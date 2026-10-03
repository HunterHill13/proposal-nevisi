# CONTRADICTION & NEGATIVE EVIDENCE POLICY
## Extensible Disagreement Taxonomy, Contextual Reconciliation, and Adversarial Literature Standards

**Policy Version:** 8.0  
**Scope:** Universal Medical & Biomedical Research Proposals  
**Governing Principle:** Systematic Detection and Epistemic Separation of True Contradiction from Contextual Disagreement  

---

## 1. Extensible Negative Evidence Taxonomy

Scientific progress depends on mapping boundary conditions, null findings, and replication failures. The engine enforces an extensible 15-category taxonomy across all biomedical fields:

| Category Code | Classification | Definition & Operational Criteria |
| :--- | :--- | :--- |
| **`NULL_RESULT`** | Null / Statistically Non-Significant | Study observed no statistically significant difference between intervention and control ($p \ge 0.05$). |
| **`NO_EFFECT`** | Biological Inertness | High-dose or sustained exposure failed to elicit the hypothesized phenotypic or molecular shift. |
| **`ANTAGONISM`** | Antagonistic Interaction | Co-administration produced an effect strictly inferior to the single-agent response or $CI > 1.2$. |
| **`SUBADDITIVITY`** | Sub-additive Interaction | Combined outcome was less than the sum of individual effects without overt antagonism. |
| **`TOXICITY`** | Dose-Limiting Toxicity | Intervention caused severe host tissue necrosis, lethal organ dysfunction, or excessive cytotoxicity. |
| **`OFF_TARGET_EFFECT`** | Non-Specific Binding / Disruption | Compound or vector engaged unintended molecular targets or altered off-target gene pathways. |
| **`RESISTANCE`** | Acquired or Intrinsic Resistance | Target cells or pathogens exhibited progressive loss of sensitivity or genetic escape mutations. |
| **`NON_RESPONSE`** | Primary Non-Responsiveness | Specific genetic, clinical, or phenotypic subgroups failed to respond entirely. |
| **`SAFETY_LIMITATION`** | Narrow Therapeutic Window | Maximum tolerated dose (MTD) overlaps with or falls below the minimum biologically effective dose. |
| **`DOSE_LIMITATION`** | Concentration Boundary | Efficacy observed only at supra-physiological concentrations (> 100 µM in vitro or toxic in vivo). |
| **`TIME_LIMITATION`** | Transient Response | Initial response dissipated rapidly due to receptor desensitization or compensatory survival loops. |
| **`MODEL_LIMITATION`** | Model-Specific Restriction | Effect successfully demonstrated in 2D cell cultures but completely failed in 3D spheroid/organoid models. |
| **`TRANSLATIONAL_FAILURE`**| Animal-to-Human Inconsistency | Robust efficacy in murine or rodent models failed to demonstrate clinical benefit in human trials. |
| **`METHODOLOGICAL_CONFLICT`**| Assay / Protocol Artifact | Apparent effect shown to stem from optical dye reduction, vehicle toxicity, or bacterial endotoxin. |
| **`CONTRADICTORY_RESULT`** | Opposite Phenotypic Outcome | High-quality study reported the exact opposite biological effect under ostensibly similar conditions. |

---

## 2. Resolving True Contradiction vs. Contextual Disagreement

When two or more studies present divergent conclusions regarding an intervention or biomarker, automated systems often lazily report an "irreconcilable contradiction".

Under this policy, the engine must perform a **Contextual Parameter Decomposition** before classifying an outcome:

```text
                               DIVERGENT FINDINGS
                                       │
                    Are experimental parameters identical?
                    (Dose, Time, Assay, Model, Cell Line,
                     Species, Disease Stage, Vehicle)
                                       │
                      ┌────────────────┴────────────────┐
                     YES                                NO
                      ▼                                 ▼
             [ TRUE_CONTRADICTION ]        [ CONTEXTUAL_DISAGREEMENT ]
           Studies used identical              Discrepancy explained by:
           reagents, models, and doses         - Different drug formulation
           yet observed opposite outcomes.     - Higher vs. lower concentrations
           Indicates reproducibility crisis    - 24h vs. 72h exposure duration
           or uncharacterized biological       - Different cell line genetic drivers
           mediators.                          - Rodent vs. human species divergence
```

### Mandatory Deconstruction Variables:
1. **Dose / Exposure Gradient:** Was one study conducted at physiological levels (e.g., $5\ \mu\text{M}$) while the other used cytotoxic supra-physiological levels (e.g., $100\ \mu\text{M}$)?
2. **Exposure Duration:** Was the endpoint measured at early phase (12–24h) or late phase (72–96h)?
3. **Biological Model / Genotype:** Were experiments performed in wild-type p53 vs. mutant p53 backgrounds?
4. **Formulation & Vehicle:** Was the compound solubilized in DMSO (with vehicle toxicity) or an aqueous nanoparticle formulation?
5. **Assay Methodology:** Was viability assessed by MTT (metabolic enzymatic reduction) or Annexin V/PI (membrane integrity)?

---

## 3. Mandatory Dual-Path Opposing Search Execution

It is a violation of this protocol to finalize a proposal without having launched dedicated queries explicitly designed to seek out null, antagonistic, and failure literature.

For each primary claim, the `generic_contradiction_engine.py` must formulate and execute queries matching:
$$\text{Query}_{\text{opposing}} = \text{Target Concept} \land (\text{"null"} \lor \text{"antagonism"} \lor \text{"failure"} \lor \text{"toxicity"} \lor \text{"resistance"})$$

---

## 4. Epistemic Reporting Standard

If the opposing search yields zero contradictory publications, the output record must state:
```json
{
  "contradiction_status": "NO_RELEVANT_CONTRADICTING_EVIDENCE_IDENTIFIED",
  "search_boundary": {
    "databases_queried": ["PubMed", "Europe PMC", "Crossref"],
    "date_window": "2010-2026",
    "exact_queries_executed": [
      "Target AND null effect",
      "Target AND antagonism",
      "Target AND resistance"
    ]
  },
  "epistemic_caveat": "Absence of identified contradictory evidence reflects current published literature within the defined search boundary and cannot rule out unpublished negative findings or publication bias."
}
```
Writing *"No contradictory evidence exists in the scientific domain"* is strictly forbidden.
