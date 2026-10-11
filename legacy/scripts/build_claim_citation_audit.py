import json
import sys
import os

# Add scripts to sys.path
sys.path.insert(0, os.path.abspath("scripts"))
from generic_claim_entailment_engine import GenericClaimEntailmentEngine

with open("FINAL_SELECTED_PORTFOLIO_AUDITED.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

selected_refs = raw.get("selection", {}).get("selected_references", [])

# Construct 14 rigorously grounded scientific claims matching the authentic 25 papers
claims = [
    {
        "claim_id": "CLM_01",
        "claim_text": "Semi-synthetic lupeol quaternary phosphonium salt and carbamate derivatives induce mitochondrial apoptosis, caspase-3/9 cleavage, and S-phase arrest in human lung cancer A549 cells.",
        "supporting_references": ["39369566", "39274838"] # Ref 1, Ref 8
    },
    {
        "claim_id": "CLM_02",
        "claim_text": "MicroRNA-204 functions as a tumor suppressor and augments oncolytic Newcastle Disease Virus cytotoxicity and apoptosis in lung adenocarcinoma models.",
        "supporting_references": ["33968198"] # Ref 2
    },
    {
        "claim_id": "CLM_03",
        "claim_text": "Newcastle Disease Virus induces p53-mediated regulation of mitochondrial electron transport chain and triggers nuclear shrinkage and oncolytic death in lung cancer cells.",
        "supporting_references": ["41170972"] # Ref 4
    },
    {
        "claim_id": "CLM_04",
        "claim_text": "Integrated transcriptomics and proteomics demonstrate that Newcastle Disease Virus infection reprogrammes cellular apoptotic, metabolic, and autophagic pathways in host cells.",
        "supporting_references": ["41942850"] # Ref 9
    },
    {
        "claim_id": "CLM_05",
        "claim_text": "Novel tubulin-targeting and thiazolidinedione-conjugated lupeol derivatives display antiproliferative activity against A549 non-small cell lung cancer cells.",
        "supporting_references": ["41297068", "39459325"] # Ref 6, Ref 11
    },
    {
        "claim_id": "CLM_06",
        "claim_text": "Plant extracts containing pentacyclic triterpenes including lupeol exhibit antioxidant capacity and cytotoxic activity against human cancer cell lines.",
        "supporting_references": ["39336114", "37845669", "40951590"] # Ref 7, Ref 10, Ref 16
    },
    {
        "claim_id": "CLM_07",
        "claim_text": "Recombinant oncolytic viral platforms such as rVSV-NDV and NDV-anti-VEGFR2 induce syncytial cell death and modulate the lung tumor microenvironment.",
        "supporting_references": ["40896365", "40382521"] # Ref 12, Ref 15
    },
    {
        "claim_id": "CLM_08",
        "claim_text": "Pentacyclic triterpenes modulate cell cycle distribution, viability, and apoptosis cascades in lung and other neoplastic models.",
        "supporting_references": ["38931361"] # Ref 13
    },
    {
        "claim_id": "CLM_09",
        "claim_text": "Newcastle Disease Virus infection stimulates type I interferon production, influencing PD-L1 immune checkpoint dynamics and immunogenic tumor cell death.",
        "supporting_references": ["42699700"] # Ref 17
    },
    {
        "claim_id": "CLM_10",
        "claim_text": "Lupeol inhibits cancer cell invasion and metastasis through downregulation of MAPK and Akt signaling cascades.",
        "supporting_references": ["32329697"] # Ref 22
    },
    {
        "claim_id": "CLM_11",
        "claim_text": "Phytochemical combinations with therapeutic agents show analogous enhancement of apoptotic pathways and antiproliferative effects in lung cancer cells.",
        "supporting_references": ["42621169", "42404852"] # Ref 5, Ref 18 (Both have synergy_evidence: ANALOGOUS)
    },
    {
        "claim_id": "CLM_12",
        "claim_text": "The quantitative evaluation of drug combinations and putative synergism is conducted via the Median-Effect Equation and Combination Index (CI) method.",
        "supporting_references": ["16968952", "6382953"] # Ref 19, Ref 21 (Method landmarks)
    },
    {
        "claim_id": "CLM_13",
        "claim_text": "Cellular viability and cytotoxic metabolic activity are quantitatively assessed using the tetrazolium dye MTT reduction assay.",
        "supporting_references": ["6606682"] # Ref 20 (Mosmann 1983)
    },
    {
        "claim_id": "CLM_14",
        "claim_text": "Dual modulation of apoptosis and survival pathways by natural compounds provides mechanistic rationale for combined anticancer strategies in A549 cells.",
        "supporting_references": ["42772808", "42633541"] # Ref 23, Ref 25
    }
]

audit_results = GenericClaimEntailmentEngine.audit_citation_to_claims(claims, selected_refs)

with open("CLAIM_CITATION_AUDIT.json", "w", encoding="utf-8") as f:
    json.dump(audit_results, f, indent=2, ensure_ascii=False)

print(f"CLAIM_CITATION_AUDIT.json generated:")
print(f"  Total claims: {audit_results['total_claims_audited']}")
print(f"  Accepted: {audit_results['accepted_count']}")
print(f"  Revised: {audit_results['revised_count']}")
print(f"  Rejected: {audit_results['rejected_count']}")
print(f"  All passed: {audit_results['all_passed']}")
for c in audit_results['audited_claims']:
    print(f"  [{c['status']}] {c['claim_id']} ({c['support_strength']} / {c['evidence_relationship']}): {c['audit_note']}")
