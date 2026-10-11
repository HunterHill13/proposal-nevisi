#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
live_pubmed_audit.py - Live PubMed Retrieval and Verification for Real-World Evidence Audit
Configurable runtime query runner for biomedical topics.
"""

import sys
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Tuple

def search_pubmed(term: str, retmax: int = 50) -> Tuple[List[str], int]:
    """Queries PubMed E-utilities esearch."""
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={urllib.parse.quote(term)}&retmode=json&retmax={retmax}&sort=pub_date"
    req = urllib.request.Request(url, headers={"User-Agent": "ProposalNevisi-Audit/8.7 (mailto:research@audit.org)"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        count = int(data["esearchresult"].get("count", 0))
        idlist = data["esearchresult"].get("idlist", [])
        return idlist, count

def fetch_summaries(idlist: List[str]) -> List[Dict[str, Any]]:
    """Fetches document summaries for given PMIDs."""
    if not idlist:
        return []
    ids = ",".join(idlist)
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={ids}&retmode=json"
    req = urllib.request.Request(url, headers={"User-Agent": "ProposalNevisi-Audit/8.7 (mailto:research@audit.org)"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        result = data.get("result", {})
        return [result[uid] for uid in idlist if uid in result]

def fetch_abstracts_xml(idlist: List[str]) -> Dict[str, Dict[str, Any]]:
    """Fetches full XML details including abstract text and mesh headings."""
    if not idlist:
        return {}
    ids = ",".join(idlist)
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={ids}&retmode=xml"
    req = urllib.request.Request(url, headers={"User-Agent": "ProposalNevisi-Audit/8.7 (mailto:research@audit.org)"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        xml_content = resp.read()
    
    root = ET.fromstring(xml_content)
    papers = {}
    for article in root.findall(".//PubmedArticle"):
        pmid_el = article.find(".//MedlineCitation/PMID")
        if pmid_el is None or not pmid_el.text:
            continue
        pmid = pmid_el.text.strip()
        
        # Title
        title_el = article.find(".//ArticleTitle")
        title = "".join(title_el.itertext()).strip() if title_el is not None else ""
        
        # Abstract
        abstract_parts = []
        for ab in article.findall(".//Abstract/AbstractText"):
            label = ab.get("Label", "")
            text = "".join(ab.itertext()).strip()
            if label:
                abstract_parts.append(f"{label}: {text}")
            else:
                abstract_parts.append(text)
        abstract = "\n".join(abstract_parts)
        
        # Journal & Year
        journal_el = article.find(".//Journal/Title")
        journal = journal_el.text.strip() if journal_el is not None and journal_el.text else ""
        
        year = ""
        pubdate_el = article.find(".//JournalIssue/PubDate/Year")
        if pubdate_el is not None and pubdate_el.text:
            year = pubdate_el.text.strip()
        else:
            medline_date = article.find(".//JournalIssue/PubDate/MedlineDate")
            if medline_date is not None and medline_date.text:
                year = medline_date.text[:4]
                
        # DOI
        doi = ""
        for el in article.findall(".//ArticleIdList/ArticleId"):
            if el.get("IdType") == "doi":
                doi = el.text.strip()
                break
                
        # Authors
        authors = []
        for auth in article.findall(".//AuthorList/Author"):
            last = auth.find("LastName")
            initials = auth.find("Initials")
            if last is not None and last.text:
                lname = last.text.strip()
                init = initials.text.strip() if initials is not None and initials.text else ""
                authors.append(f"{lname} {init}".strip())
                
        papers[pmid] = {
            "pmid": pmid,
            "doi": doi,
            "title": title,
            "journal": journal,
            "year": year,
            "authors": authors,
            "abstract": abstract
        }
    return papers

def run_broad_analysis():
    print("=================================================================")
    print("LIVE REAL-WORLD PUBMED SEARCH: LUPEOL & NDV IN LUNG CANCER")
    print("=================================================================\n")
    
    # 1. Lupeol in A549
    ids1, count1 = search_pubmed('Lupeol AND A549', retmax=60)
    print(f"Total Lupeol + A549: {count1} records found. Top 25:")
    papers1 = fetch_abstracts_xml(ids1[:25])
    for pmid, p in sorted(papers1.items(), key=lambda x: x[1]['year']):
        title = p["title"].encode("ascii", "replace").decode("ascii")
        print(f"  [PMID: {pmid}] ({p['year']}) {title[:80]} | {p['journal'][:25]}")
        
def fetch_portfolio_25():
    pmids = [
        '39369566', '41297068', '39336114', '39274838', '41170972',
        '33968198', '39624055', '42621169', '41942850', '37845669',
        '41674174', '39459325', '32329697', '40896365', '38931361',
        '40951590', '42699700', '42404852', '6606682',  '16968952',
        '6382953',  '40382521', '42772808', '42633541', '39792924'
    ]
    print(f"Fetching {len(pmids)} papers from live NCBI PubMed...")
    papers = fetch_abstracts_xml(pmids)
    print(f"Successfully retrieved {len(papers)} of {len(pmids)} papers.")
    with open("real_world_raw_papers.json", "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)
    print("Saved to real_world_raw_papers.json")
    for idx, pmid in enumerate(pmids):
        p = papers.get(pmid, {})
        title = p.get("title", "").encode("ascii", "replace").decode("ascii")
        print(f"  [{idx+1}] PMID {pmid} ({p.get('year')}) {title[:70]} | DOI: {p.get('doi')}")

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    fetch_portfolio_25()



