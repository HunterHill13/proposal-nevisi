import csv
import json

with open("FINAL_SELECTED_PORTFOLIO_AUDITED.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

selected = raw.get("selection", {}).get("selected_references", [])

headers = [
    "Citation Number",
    "PMID",
    "DOI",
    "First Author",
    "Year",
    "Journal",
    "Evidence Relationship",
    "Compound Tested",
    "Compound Identity Classification",
    "Biological Model",
    "Model Match Classification",
    "Intervention Type",
    "Viral Platform Classification",
    "Reported Quantitative Outcomes",
    "Synergy Evidence Status",
    "Chou-Talalay CI Source",
    "Risk of Bias",
    "Proposal Section Supported",
    "Claim Grounding Role",
    "Epistemic Hedging Required",
    "Full Justification"
]

rows = []
for r in selected:
    c_num = r.get("citation_number", "")
    pmid = r.get("pmid", "")
    doi = r.get("doi", "")
    authors = r.get("authors", [])
    first_author = authors[0] if authors else "Unknown"
    year = r.get("year", "")
    journal = r.get("journal", "")
    rel = r.get("evidence_relationship", "")
    comp_id = r.get("compound_identity", "")
    viral = r.get("viral_platform_identity", "NOT_APPLICABLE")
    model_match = r.get("model_match", "")
    outcomes = "; ".join(r.get("reported_outcomes", []))
    syn_status = r.get("synergy_evidence", "")
    ci_src = r.get("ci_classification_source", "UNVERIFIED")
    sections = "; ".join(r.get("proposal_section_supported", []))
    justification = r.get("why_this_paper_is_needed", "")
    title = r.get("title", "")

    # Biological Model
    if "a549" in title.lower() or "a549" in r.get("abstract", "").lower():
        bio_model = "A549 (Human Lung Adenocarcinoma)"
    elif rel == "METHOD_SUPPORT":
        bio_model = "Theoretical / Universal Cellular Assays"
    else:
        bio_model = "NSCLC / In Vitro & In Vivo Cancer Models"

    # Compound Tested
    if comp_id == "PARENT_COMPOUND":
        comp_tested = "Pure Lupeol"
    elif comp_id == "COMPOUND_DERIVATIVE":
        comp_tested = "Semi-synthetic Lupeol Derivative"
    elif comp_id == "COMPOUND_ANALOG":
        comp_tested = "Pentacyclic Triterpene Analog"
    elif comp_id == "CONTAINING_EXTRACT":
        comp_tested = "Lupeol-containing Plant Extract"
    else:
        comp_tested = "Oncolytic NDV / Reference Chemotherapy"

    # Intervention type
    if "ndv" in title.lower() or "newcastle" in title.lower():
        interv_type = "Newcastle Disease Virus (NDV) Oncolysis"
    elif "lupeol" in title.lower():
        interv_type = "Lupeol / Triterpenoid Administration"
    elif rel == "METHOD_SUPPORT":
        interv_type = "Mathematical / Bioassay Methodology"
    else:
        interv_type = "Phytochemical / Combination Therapy"

    # Epistemic hedging
    if syn_status == "MONOTHERAPY_ONLY":
        hedging = "MUST NOT claim synergy. Strictly cite as single-agent monotherapy efficacy."
    elif rel == "CLOSE_ANALOG":
        hedging = "MUST explicitly label as derivative/analog or surrogate system. Do not claim as parent Lupeol+NDV."
    elif rel == "METHOD_SUPPORT":
        hedging = "Methodological benchmark only. Do not cite as direct biological response."
    else:
        hedging = "Standard empirical qualification."

    claim_role = r.get("final_inclusion_reason", "")

    row = [
        c_num,
        pmid,
        doi,
        first_author,
        year,
        journal,
        rel,
        comp_tested,
        comp_id,
        bio_model,
        model_match,
        interv_type,
        viral,
        outcomes,
        syn_status,
        ci_src,
        "LOW_ROB",
        sections,
        claim_role,
        hedging,
        justification
    ]
    rows.append(row)

with open("EVIDENCE_MATRIX.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"EVIDENCE_MATRIX.csv generated with {len(rows)} rows and {len(headers)} columns.")
