import urllib.request
import urllib.parse
import json
import time
import ssl
from datetime import datetime

# Setup SSL context
ctx = ssl.create_default_context()

SEARCH_FAMILIES = [
    "Lupeol AND NDV",
    "Lupeol AND Newcastle disease virus",
    "Lupeol AND A549",
    "Lupeol AND lung cancer",
    "NDV AND A549",
    "NDV AND lung cancer",
    "Lupeol AND NDV AND A549",
    "Lupeol AND Newcastle disease virus AND lung",
    "lupeol AND combination AND cancer",
    "NDV AND combination AND cancer",
    "lupeol AND synerg*",
    "NDV AND synerg*",
    "Lupeol AND apoptosis AND A549",
    "NDV AND apoptosis AND A549"
]

def query_pubmed(q):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urllib.parse.urlencode({
        "db": "pubmed",
        "term": q,
        "retmode": "json",
        "retmax": 20
    })
    req = urllib.request.Request(url, headers={"User-Agent": "ProposalNevisi-Auditor/8.3 (academic-research)"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            count = int(data.get("esearchresult", {}).get("count", 0))
            ids = data.get("esearchresult", {}).get("idlist", [])
            return {"status": "SUCCESS", "count": count, "ids": ids}
    except Exception as e:
        return {"status": "ERROR", "error": str(e), "count": 0, "ids": []}

def query_europe_pmc(q):
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode({
        "query": q,
        "format": "json",
        "pageSize": 10,
        "resultType": "lite"
    })
    req = urllib.request.Request(url, headers={"User-Agent": "ProposalNevisi-Auditor/8.3 (academic-research)"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            count = int(data.get("hitCount", 0))
            result_list = data.get("resultList", {}).get("result", [])
            titles = [r.get("title") for r in result_list[:5]]
            return {"status": "SUCCESS", "count": count, "sample_titles": titles}
    except Exception as e:
        return {"status": "ERROR", "error": str(e), "count": 0, "sample_titles": []}

def main():
    ledger = {
        "ledger_metadata": {
            "audit_type": "ADVERSARIAL_SEARCH_STRATEGY_AUDIT",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "target_question": "Combined and synergistic effects of Lupeol + Newcastle Disease Virus on growth inhibition of A549 lung cancer cells in vitro",
            "databases_queried": ["PubMed / NCBI E-utilities", "Europe PMC REST API"],
            "total_search_families": len(SEARCH_FAMILIES)
        },
        "search_families_evaluated": []
    }

    for idx, q in enumerate(SEARCH_FAMILIES, 1):
        print(f"[{idx}/{len(SEARCH_FAMILIES)}] Querying: {q}")
        pm_res = query_pubmed(q)
        time.sleep(0.4)
        epmc_res = query_europe_pmc(q)
        time.sleep(0.4)

        entry = {
            "query_id": f"QRY_{idx:02d}",
            "exact_query": q,
            "pubmed": pm_res,
            "europe_pmc": epmc_res,
            "direct_combination_detected": False,
            "notes": ""
        }

        # Analyze direct combination
        if "NDV" in q.upper() or "NEWCASTLE" in q.upper():
            if "LUPEOL" in q.upper():
                # Direct combination family
                if pm_res.get("count", 0) == 0:
                    entry["notes"] = "Zero PubMed results for direct Lupeol + NDV combination."
                else:
                    entry["notes"] = f"PubMed returned {pm_res.get('count')} results - inspection required."

        ledger["search_families_evaluated"].append(entry)

    with open("SEARCH_LEDGER.json", "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)

    print("SEARCH_LEDGER.json generated successfully.")

if __name__ == "__main__":
    main()
