import json

with open("FINAL_SELECTED_PORTFOLIO_AUDITED.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

refs = raw.get("selection", {}).get("selected_references", [])
print(f"Total references in portfolio: {len(refs)}")

for i, r in enumerate(refs):
    pmid = r.get("pmid")
    doi = r.get("doi")
    title = r.get("title")
    authors = r.get("authors", [])
    first_auth = authors[0] if authors else "Unknown"
    year = r.get("year")
    journal = r.get("journal")
    abstract = r.get("abstract", "")
    rel = r.get("evidence_relationship")
    comp = r.get("compound_identity")
    viral = r.get("viral_platform_identity")
    syn = r.get("synergy_evidence")
    print(f"\n--- REF [{i+1}] PMID: {pmid} | DOI: {doi} ---")
    print(f"Title: {title}")
    print(f"Authors: {first_auth} et al. ({year}) - {journal}")
    print(f"Rel: {rel} | Comp: {comp} | Viral: {viral} | Syn: {syn}")
    # Print first 200 chars of abstract
    print(f"Abstract snippet: {abstract[:250]}...")
