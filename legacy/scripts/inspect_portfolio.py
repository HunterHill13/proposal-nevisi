import json

with open("FINAL_SELECTED_PORTFOLIO_AUDITED.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

data = raw.get("selection", {}).get("selected_references", [])
print(f"Total count: {len(data)}")
for i, r in enumerate(data):
    pmid = r.get("pmid", "N/A")
    doi = r.get("doi", "N/A")
    rel = r.get("evidence_relationship", "UNKNOWN")
    comp = r.get("compound_identity", "N/A")
    viral = r.get("viral_platform", "N/A")
    title = r.get("title", "")[:60]
    print(f"{i+1:2d}. PMID: {pmid:<9} | Rel: {rel:<18} | Comp: {comp:<15} | Viral: {viral:<10} | {title}")

