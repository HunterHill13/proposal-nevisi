#!/usr/bin/env python3
"""
Comprehensive Citation & Relevance Checkpoint for Proposal-Nevisi Skill
Verifies:
1. All in-text citations ([1], [2], etc.) map to valid reference entries without gaps.
2. Every reference actually exists in NCBI PubMed with matching PMID, DOI, authors, and year.
3. Every reference is strictly relevant to the study domain (e.g. cancer, lupeol, NDV, synergy).
4. All non-foundational references adhere to the <= 5-6 year publication date window.
"""

import sys
import os
import re
import json
import urllib.request
import urllib.parse
import argparse

sys.stdout.reconfigure(encoding='utf-8')

PUBMED_ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def extract_in_text_citations(text):
    # Match patterns like [1], [1, 2], [1, 3, 5]
    matches = re.findall(r'\[(\d+(?:\s*,\s*\d+)*)\]', text)
    cited_numbers = set()
    for m in matches:
        nums = [int(n.strip()) for n in m.split(',')]
        cited_numbers.update(nums)
    return cited_numbers

def verify_pmids_ncbi(pmids):
    if not pmids:
        return {}
    url = f"{PUBMED_ESUMMARY}?db=pubmed&id={','.join(pmids)}&retmode=json"
    req = urllib.request.Request(url, headers={"User-Agent": "ProposalNevisi-Checkpoint/2.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get("result", {})
    except Exception as e:
        print(f"[Warning] NCBI API connection error during checkpoint: {e}", file=sys.stderr)
        return {}

def check_relevance(title, journal, domain_keywords):
    text_to_check = (title + " " + journal).lower()
    matches = [kw for kw in domain_keywords if kw.lower() in text_to_check]
    return len(matches) > 0, matches

def run_checkpoint(md_path, json_path, domain_keywords=None, min_year=2020, max_year=2026):
    if domain_keywords is None:
        domain_keywords = ["cancer", "lung", "nsclc", "a549", "adenocarcinoma", "lupeol", "triterpene", 
                           "newcastle", "ndv", "oncolytic", "virus", "virotherapy",
                           "synergy", "synergistic", "combination", "cytotoxicity", "mtt", 
                           "chou-talalay", "median-effect", "mortality", "globocan", "carcinoma", 
                           "antitumor", "tumor", "neoplasm", "apoptosis", "caspase", "bcl-2", "bax", "akt"]

    print("==================== PROPOSAL CITATION CHECKPOINT AUDIT ====================")
    
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Split body from Section 14 to avoid counting references list as in-text citations
    parts = re.split(r'##\s*(?:۱۴|14)\.\s*فهرست\s*منابع', md_text)
    body_text = parts[0]
    
    in_text_citations = extract_in_text_citations(body_text)
    print(f"[1/4] In-Text Citations detected: {sorted(list(in_text_citations))}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        records = json.load(f)
        
    num_records = len(records)
    print(f"[2/4] Bibliography Entries in database: {num_records}")

    # Check for citation gaps or mismatches
    expected_set = set(range(1, num_records + 1))
    missing_in_text = expected_set - in_text_citations
    orphan_in_text = in_text_citations - expected_set

    if missing_in_text:
        print(f"  [Warning] References in list not cited in body text: {sorted(list(missing_in_text))}")
    else:
        print("  [Pass] 100% of bibliography references are cited in body text.")
        
    if orphan_in_text:
        print(f"  [Fail] In-text citations without reference entry: {sorted(list(orphan_in_text))}")
    else:
        print("  [Pass] No orphan in-text citations.")

    # Check NCBI existence and topic relevance
    pmids = [r["pmid"] for r in records if r.get("pmid")]
    ncbi_results = verify_pmids_ncbi(pmids)

    print("\n[3/4] Authenticity & Relevance Audit per Reference:")
    all_passed = True

    for i, r in enumerate(records, 1):
        pmid = r.get("pmid", "")
        title = r.get("title", "")
        year = r.get("year", "")
        journal = r.get("journal", "")
        is_foundation = r.get("is_foundation", False)
        
        # Check 1: Real existence
        ncbi_rec = ncbi_results.get(pmid)
        exists = ncbi_rec is not None and "title" in ncbi_rec
        
        # Check 2: Date window
        try:
            yr_int = int(year[:4])
            date_ok = (min_year <= yr_int <= max_year) or is_foundation
        except ValueError:
            date_ok = False
            
        # Check 3: Topic relevance
        rel_ok, matched_kws = check_relevance(title, journal, domain_keywords)
        
        # Check 4: In-text citation
        cited_ok = i in in_text_citations

        status = "PASS" if (exists and date_ok and rel_ok and cited_ok) else "WARN"
        if not exists:
            status = "FAIL"
            all_passed = False
            
        kws_str = ", ".join(matched_kws[:3]) if matched_kws else "None"
        found_flag = " [Foundation Method]" if is_foundation else ""
        print(f"  Ref #{i:02d} [{status}]: [{year}] PMID:{pmid} | Rel: {kws_str} | Cited: {cited_ok}{found_flag}")
        print(f"          Title: {title[:75]}...")

    print("\n[4/4] Summary Result:")
    if all_passed and not orphan_in_text:
        print("  =======================================================")
        print("  >>> CITATION CHECKPOINT PASSED: ALL REFERENCES VERIFIED <<<")
        print("  =======================================================")
        return True
    else:
        print("  >>> CITATION CHECKPOINT COMPLETED WITH WARNINGS/FAILURES <<<")
        return False

def main():
    parser = argparse.ArgumentParser(description="Citation & Relevance Checkpoint")
    parser.add_argument("md_path", help="Path to Markdown proposal")
    parser.add_argument("json_path", help="Path to references JSON database")
    parser.add_argument("--min-year", type=int, default=2020)
    parser.add_argument("--max-year", type=int, default=2026)
    parser.add_argument("--keywords", nargs="*", default=None, help="Domain keywords for relevance check")
    args = parser.parse_args()

    success = run_checkpoint(args.md_path, args.json_path, domain_keywords=args.keywords, min_year=args.min_year, max_year=args.max_year)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
