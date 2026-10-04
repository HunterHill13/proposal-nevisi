#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scientific_search_adapter.py - Multi-Source Federated Scientific Literature Search Engine
Proposal-Nevisi Engine v8.2 (Universal Biomedical Architecture)

Provides a standard-library, dependency-free adapter for federated literature retrieval
across PubMed, Europe PMC, OpenAlex, and Crossref.
Implements:
1. Multi-source API querying with polite rate limiting and exponential backoff.
2. Connected-component graph deduplication across multiple persistent identifiers (DOI, PMID, OpenAlex ID).
3. Search saturation curve tracking and yield analytics.
4. Deterministic offline and recorded-fixture modes for reproducible testing.
5. End-to-end integration with the 10-dimension Contextual Relevance Gate and 25-reference hard ceiling.

100% Domain-Agnostic: Zero hardcoded biomedical entities, diseases, or drugs.
"""

import os
import re
import ssl
import sys
import json
import time
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
import difflib
from typing import Dict, List, Any, Optional, Set, Tuple

# Import core policies and reference auditor
try:
    from core_policies import (
        MAX_FINAL_REFERENCES, MIN_FINAL_REFERENCES,
        ContextualRelevanceConfig, TemporalPolicyConfig
    )
    from generic_reference_auditor import GenericReferenceAuditor
except ImportError:
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    from core_policies import (
        MAX_FINAL_REFERENCES, MIN_FINAL_REFERENCES,
        ContextualRelevanceConfig, TemporalPolicyConfig
    )
    from generic_reference_auditor import GenericReferenceAuditor


class BaseScientificSearchBackend:
    """Abstract Base Class for pluggable scientific search backends."""
    backend_name: str = "BASE"

    def search(self, query: str, max_results: int = 50, mode: str = "offline") -> Dict[str, Any]:
        """Executes a search query and returns standardized search results."""
        raise NotImplementedError("Subclasses must implement search()")


class PubMedBackend(BaseScientificSearchBackend):
    """Concrete backend adapter for NCBI PubMed / E-utilities."""
    backend_name: str = "PubMed"

    def __init__(self, adapter: Optional["ScientificSearchAdapter"] = None):
        self.adapter = adapter or ScientificSearchAdapter()

    def search(self, query: str, max_results: int = 50, mode: str = "offline") -> Dict[str, Any]:
        return self.adapter.query_pubmed(query, max_results=max_results, mode=mode)


class EuropePMCBackend(BaseScientificSearchBackend):
    """Concrete backend adapter for Europe PMC REST API."""
    backend_name: str = "Europe PMC"

    def __init__(self, adapter: Optional["ScientificSearchAdapter"] = None):
        self.adapter = adapter or ScientificSearchAdapter()

    def search(self, query: str, max_results: int = 50, mode: str = "offline") -> Dict[str, Any]:
        return self.adapter.query_europe_pmc(query, max_results=max_results, mode=mode)


class OpenAlexBackend(BaseScientificSearchBackend):
    """Concrete backend adapter for OpenAlex Works REST API."""
    backend_name: str = "OpenAlex"

    def __init__(self, adapter: Optional["ScientificSearchAdapter"] = None):
        self.adapter = adapter or ScientificSearchAdapter()

    def search(self, query: str, max_results: int = 50, mode: str = "offline") -> Dict[str, Any]:
        return self.adapter.query_openalex(query, max_results=max_results, mode=mode)


class CrossrefBackend(BaseScientificSearchBackend):
    """Concrete backend adapter for Crossref Metadata REST API."""
    backend_name: str = "Crossref"

    def __init__(self, adapter: Optional["ScientificSearchAdapter"] = None):
        self.adapter = adapter or ScientificSearchAdapter()

    def search(self, query: str, max_results: int = 50, mode: str = "offline") -> Dict[str, Any]:
        return self.adapter.query_crossref(query, max_results=max_results, mode=mode)


class FixtureSearchBackend(BaseScientificSearchBackend):
    """Deterministic offline fixture backend for reproducible testing."""
    backend_name: str = "FixtureCorpus"

    def __init__(self, records: Optional[List[Dict[str, Any]]] = None):
        self.records = records or []

    def set_records(self, records: List[Dict[str, Any]]) -> None:
        self.records = list(records)

    def search(self, query: str, max_results: int = 50, mode: str = "fixture") -> Dict[str, Any]:
        q_terms = [w.lower() for w in query.split() if len(w) > 3]
        if not q_terms:
            res_list = self.records[:max_results]
        else:
            matched = [
                r for r in self.records
                if any(t in f"{r.get('title','')} {r.get('abstract','')} {r.get('doi','')} {r.get('pmid','')}".lower() for t in q_terms)
            ]
            res_list = matched[:max_results] if matched else self.records[:max_results]
        return {
            "database": self.backend_name,
            "query": query,
            "status": "EXECUTED",
            "results_count": len(res_list),
            "records": res_list
        }


class KDenseCompatibilityBackend(BaseScientificSearchBackend):
    """Compatibility bridge for K-Dense scientific agent skills and local science tools.
    
    Acts as a pluggable Retrieval-Only Adapter that translates K-Dense paper-lookup,
    literature-review, and citation-management output structures into standardized
    Proposal-Nevisi Study Evidence records with full field provenance.
    Leaves all relevance, entailment, and portfolio decisions to Proposal-Nevisi.
    """
    backend_name: str = "KDenseCompatible"

    def __init__(self, primary_backend: Optional[BaseScientificSearchBackend] = None):
        self.primary_backend = primary_backend or PubMedBackend()

    @staticmethod
    def normalize_kdense_record(raw_record: Dict[str, Any]) -> Dict[str, Any]:
        """Normalizes a K-Dense / Science skill output item into Proposal-Nevisi format."""
        doi = raw_record.get("doi")
        if doi:
            doi = str(doi).strip().lower().replace("https://doi.org/", "").replace("http://doi.org/", "")

        pmid = raw_record.get("pmid") or raw_record.get("ext_id")
        if pmid:
            pmid = str(pmid).strip()

        openalex_id = raw_record.get("openalex_id") or raw_record.get("id")
        if openalex_id and "openalex.org" in str(openalex_id):
            openalex_id = str(openalex_id).split("/")[-1].strip().lower()

        title = str(raw_record.get("title", "")).strip().rstrip(".")
        abstract = str(raw_record.get("abstract", raw_record.get("abstractText", ""))).strip()
        authors = raw_record.get("authors", [])
        if isinstance(authors, str):
            authors = [a.strip() for a in authors.split(",") if a.strip()]

        year = raw_record.get("year") or raw_record.get("publication_year") or raw_record.get("pubYear")
        if year and str(year).isdigit():
            year = int(year)
        else:
            year = None

        journal = str(raw_record.get("journal", raw_record.get("journalTitle", raw_record.get("source", "")))).strip()

        normalized = {
            "database": raw_record.get("database", "KDense/PaperLookup"),
            "doi": doi,
            "pmid": pmid,
            "openalex_id": openalex_id,
            "title": title,
            "abstract": abstract if abstract else None,
            "authors": authors,
            "journal": journal,
            "year": year,
            "kdense_interoperable": True,
            "kdense_schema": "kdense/paper-lookup/v2.4",
            "field_provenance": {
                "title": raw_record.get("database", "KDense"),
                "doi": raw_record.get("database", "KDense") if doi else None,
                "pmid": raw_record.get("database", "KDense") if pmid else None,
                "abstract": raw_record.get("database", "KDense") if abstract else None
            },
            "raw_metadata": raw_record
        }
        return normalized

    def search(self, query: str, max_results: int = 50, mode: str = "offline") -> Dict[str, Any]:
        """Delegates search to primary backend while wrapping in K-Dense schema semantics."""
        res = self.primary_backend.search(query, max_results=max_results, mode=mode)
        recs = res.get("records", [])
        kdense_records = [self.normalize_kdense_record(r) for r in recs]
        res["records"] = kdense_records
        res["compatibility_layer"] = "K_DENSE_SCIENTIFIC_SKILLS"
        return res


class ScientificSearchAdapter:
    """Universal federated scientific search engine and deduplication adapter."""

    USER_AGENT = "Proposal-Nevisi/8.2 (Universal Biomedical Engine; mailto:audit@proposal-nevisi.org)"
    DEFAULT_TIMEOUT_SECONDS = 10
    MAX_RETRIES = 3
    BACKOFF_BASE_SECONDS = 1.0

    API_ENDPOINTS = {
        "PubMed_search": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
        "PubMed_summary": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
        "PubMed_fetch": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
        "Europe_PMC": "https://www.ebi.ac.uk/europepmc/webservices/rest/search",
        "OpenAlex": "https://api.openalex.org/works",
        "Crossref": "https://api.crossref.org/works"
    }

    def __init__(
        self,
        ncbi_api_key: Optional[str] = None,
        polite_email: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
        custom_backend: Optional[BaseScientificSearchBackend] = None
    ):
        self.ncbi_api_key = ncbi_api_key or os.environ.get("NCBI_API_KEY")
        self.polite_email = polite_email or os.environ.get("POLITE_EMAIL", "audit@proposal-nevisi.org")
        self.timeout = timeout
        self.request_delay = 0.12 if self.ncbi_api_key else 0.35
        self.last_request_time: Dict[str, float] = {}
        self.custom_backend = custom_backend
        self._registered_backends: Dict[str, BaseScientificSearchBackend] = {}
        self._init_default_backends()

    def _init_default_backends(self):
        """Initializes default swappable database backends."""
        self._registered_backends["PubMed"] = PubMedBackend(self)
        self._registered_backends["Europe PMC"] = EuropePMCBackend(self)
        self._registered_backends["OpenAlex"] = OpenAlexBackend(self)
        self._registered_backends["Crossref"] = CrossrefBackend(self)
        self._registered_backends["KDense"] = KDenseCompatibilityBackend(self._registered_backends["PubMed"])

    def register_backend(self, name: str, backend: BaseScientificSearchBackend) -> None:
        """Registers or overrides a scientific search backend."""
        self._registered_backends[name] = backend

    def get_backend(self, name: str) -> Optional[BaseScientificSearchBackend]:
        """Retrieves a registered search backend by name."""
        return self._registered_backends.get(name)

    def _rate_limit(self, db_key: str):
        """Enforces cooperative rate-limiting per source API."""
        now = time.time()
        last = self.last_request_time.get(db_key, 0.0)
        elapsed = now - last
        if elapsed < self.request_delay:
            time.sleep(self.request_delay - elapsed)
        self.last_request_time[db_key] = time.time()

    def _http_get_json(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Executes HTTP GET request with retries, exponential backoff, and JSON parsing."""
        req_headers = {
            "User-Agent": self.USER_AGENT,
            "Accept": "application/json"
        }
        if headers:
            req_headers.update(headers)

        req = urllib.request.Request(url, headers=req_headers)
        # Permissive SSL context for compatibility across diverse platforms
        ctx = ssl.create_default_context()

        last_error = None
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout, context=ctx) as resp:
                    raw_bytes = resp.read()
                    charset = resp.headers.get_content_charset() or "utf-8"
                    text = raw_bytes.decode(charset, errors="replace")
                    return json.loads(text)
            except urllib.error.HTTPError as http_err:
                last_error = http_err
                if http_err.code in [429, 500, 502, 503, 504]:
                    sleep_time = self.BACKOFF_BASE_SECONDS * (2 ** (attempt - 1))
                    time.sleep(sleep_time)
                else:
                    break
            except (urllib.error.URLError, TimeoutError, OSError) as net_err:
                last_error = net_err
                sleep_time = self.BACKOFF_BASE_SECONDS * (2 ** (attempt - 1))
                time.sleep(sleep_time)
            except json.JSONDecodeError as json_err:
                return {"_error": "JSON_DECODE_ERROR", "details": str(json_err)}

        return {"_error": "HTTP_REQUEST_FAILED", "details": str(last_error)}

    def _http_get_text(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Executes HTTP GET request with retries and returns text body."""
        req_headers = {
            "User-Agent": self.USER_AGENT,
            "Accept": "application/xml, text/xml, */*"
        }
        if headers:
            req_headers.update(headers)

        req = urllib.request.Request(url, headers=req_headers)
        ctx = ssl.create_default_context()

        last_error = None
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout, context=ctx) as resp:
                    raw_bytes = resp.read()
                    charset = resp.headers.get_content_charset() or "utf-8"
                    text = raw_bytes.decode(charset, errors="replace")
                    return {"text": text}
            except urllib.error.HTTPError as http_err:
                last_error = http_err
                if http_err.code in [429, 500, 502, 503, 504]:
                    sleep_time = self.BACKOFF_BASE_SECONDS * (2 ** (attempt - 1))
                    time.sleep(sleep_time)
                else:
                    break
            except (urllib.error.URLError, TimeoutError, OSError) as net_err:
                last_error = net_err
                sleep_time = self.BACKOFF_BASE_SECONDS * (2 ** (attempt - 1))
                time.sleep(sleep_time)

        return {"_error": "HTTP_REQUEST_FAILED", "details": str(last_error)}

    def fetch_pubmed_abstracts_efetch(self, pmid_list: List[str]) -> Dict[str, str]:
        """Fetches authentic abstracts for PMIDs via NCBI E-Fetch XML.
        
        Extracts structured or plain abstract text cleanly without fabrication.
        Returns dict mapping pmid -> abstract_text.
        """
        if not pmid_list:
            return {}
        self._rate_limit("pubmed")
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(pmid_list),
            "rettype": "abstract",
            "retmode": "xml"
        }
        if self.ncbi_api_key:
            fetch_params["api_key"] = self.ncbi_api_key

        fetch_url = f"{self.API_ENDPOINTS['PubMed_fetch']}?{urllib.parse.urlencode(fetch_params)}"
        res = self._http_get_text(fetch_url)
        if "_error" in res:
            return {}

        xml_text = res.get("text", "")
        if not xml_text:
            return {}

        abstracts_map: Dict[str, str] = {}
        try:
            root = ET.fromstring(xml_text)
            for article in root.iter("PubmedArticle"):
                pmid_elem = article.find(".//MedlineCitation/PMID")
                if pmid_elem is None or not pmid_elem.text:
                    continue
                pmid = pmid_elem.text.strip()
                abstract_elem = article.find(".//Article/Abstract")
                if abstract_elem is None:
                    continue
                parts = []
                for at in abstract_elem.findall("AbstractText"):
                    label = at.get("Label")
                    t = "".join(at.itertext()).strip()
                    if label and t:
                        parts.append(f"{label}: {t}")
                    elif t:
                        parts.append(t)
                if parts:
                    abstracts_map[pmid] = "\n".join(parts)
        except Exception:
            return {}

        return abstracts_map

    # =========================================================================
    # 1. DATABASE-SPECIFIC ADAPTERS
    # =========================================================================

    def query_pubmed(self, query: str, max_results: int = 50, mode: str = "offline") -> Dict[str, Any]:
        """Queries NCBI PubMed using E-utilities (esearch + esummary + efetch for real abstracts)."""
        if mode != "online":
            return {
                "database": "PubMed",
                "query": query,
                "status": "NOT_EXECUTED" if mode == "offline" else "RECORDED_FIXTURE",
                "results_count": 0,
                "records": []
            }

        self._rate_limit("pubmed")
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": str(max_results),
            "sort": "pub_date"
        }
        if self.ncbi_api_key:
            search_params["api_key"] = self.ncbi_api_key

        search_url = f"{self.API_ENDPOINTS['PubMed_search']}?{urllib.parse.urlencode(search_params)}"
        search_data = self._http_get_json(search_url)

        if "_error" in search_data:
            return {
                "database": "PubMed",
                "query": query,
                "status": "ERROR",
                "error": search_data["details"],
                "results_count": 0,
                "records": []
            }

        id_list = search_data.get("esearchresult", {}).get("idlist", [])
        if not id_list:
            return {
                "database": "PubMed",
                "query": query,
                "status": "EXECUTED",
                "results_count": 0,
                "records": []
            }

        self._rate_limit("pubmed")
        summary_params = {
            "db": "pubmed",
            "id": ",".join(id_list),
            "retmode": "json"
        }
        if self.ncbi_api_key:
            summary_params["api_key"] = self.ncbi_api_key

        summary_url = f"{self.API_ENDPOINTS['PubMed_summary']}?{urllib.parse.urlencode(summary_params)}"
        summary_data = self._http_get_json(summary_url)

        # Retrieve authentic abstracts via E-Fetch XML
        abstracts_map = self.fetch_pubmed_abstracts_efetch(id_list)

        records = []
        result_dict = summary_data.get("result", {})
        for pmid in id_list:
            if pmid in result_dict:
                item = result_dict[pmid]
                doi = None
                for aid in item.get("articleids", []):
                    if aid.get("idtype") == "doi":
                        doi = str(aid.get("value", "")).strip().lower()
                        break
                
                authors = [a.get("name", "") for a in item.get("authors", []) if a.get("name")]
                year = None
                pubdate = str(item.get("pubdate", ""))
                year_m = re.search(r'\b(19\d\d|20\d\d)\b', pubdate)
                if year_m:
                    year = int(year_m.group(1))

                rec = {
                    "database": "PubMed",
                    "pmid": pmid,
                    "doi": doi,
                    "title": str(item.get("title", "")).strip().rstrip("."),
                    "authors": authors,
                    "journal": str(item.get("source", "")).strip(),
                    "year": year,
                    "publication_date": pubdate,
                    "raw_metadata": item
                }
                # Assign authentic abstract if fetched from NCBI E-Fetch
                if pmid in abstracts_map:
                    rec["abstract"] = abstracts_map[pmid]
                    rec["abstract_provenance"] = "NCBI_EFETCH_XML"

                records.append(rec)

        return {
            "database": "PubMed",
            "query": query,
            "status": "EXECUTED",
            "results_count": len(records),
            "records": records
        }

    def query_europe_pmc(self, query: str, max_results: int = 50, mode: str = "offline") -> Dict[str, Any]:
        """Queries Europe PMC REST API."""
        if mode != "online":
            return {
                "database": "Europe PMC",
                "query": query,
                "status": "NOT_EXECUTED" if mode == "offline" else "RECORDED_FIXTURE",
                "results_count": 0,
                "records": []
            }

        self._rate_limit("europe_pmc")
        params = {
            "query": query,
            "format": "json",
            "pageSize": str(max_results),
            "resultType": "core"
        }
        url = f"{self.API_ENDPOINTS['Europe_PMC']}?{urllib.parse.urlencode(params)}"
        data = self._http_get_json(url)

        if "_error" in data:
            return {
                "database": "Europe PMC",
                "query": query,
                "status": "ERROR",
                "error": data["details"],
                "results_count": 0,
                "records": []
            }

        raw_list = data.get("resultList", {}).get("result", [])
        records = []
        for item in raw_list:
            pmid = str(item.get("pmid", "")).strip() or None
            doi = str(item.get("doi", "")).strip().lower() or None
            title = str(item.get("title", "")).strip().rstrip(".")
            year = int(item["pubYear"]) if item.get("pubYear") and str(item["pubYear"]).isdigit() else None
            author_str = str(item.get("authorString", ""))
            authors = [a.strip() for a in author_str.split(",") if a.strip()]

            records.append({
                "database": "Europe PMC",
                "pmid": pmid,
                "doi": doi,
                "title": title,
                "authors": authors,
                "journal": str(item.get("journalTitle", "")).strip(),
                "year": year,
                "abstract": str(item.get("abstractText", "")).strip(),
                "cited_by_count": item.get("citedByCount", 0),
                "raw_metadata": item
            })

        return {
            "database": "Europe PMC",
            "query": query,
            "status": "EXECUTED",
            "results_count": len(records),
            "records": records
        }

    def query_openalex(self, query: str, max_results: int = 50, mode: str = "offline") -> Dict[str, Any]:
        """Queries OpenAlex Works REST API using polite headers."""
        if mode != "online":
            return {
                "database": "OpenAlex",
                "query": query,
                "status": "NOT_EXECUTED" if mode == "offline" else "RECORDED_FIXTURE",
                "results_count": 0,
                "records": []
            }

        self._rate_limit("openalex")
        params = {
            "search": query,
            "per-page": str(max_results)
        }
        if self.polite_email:
            params["mailto"] = self.polite_email

        url = f"{self.API_ENDPOINTS['OpenAlex']}?{urllib.parse.urlencode(params)}"
        data = self._http_get_json(url)

        if "_error" in data:
            return {
                "database": "OpenAlex",
                "query": query,
                "status": "ERROR",
                "error": data["details"],
                "results_count": 0,
                "records": []
            }

        records = []
        for item in data.get("results", []):
            openalex_id = str(item.get("id", "")).replace("https://openalex.org/", "").strip()
            raw_doi = str(item.get("doi", "")).strip().lower()
            doi = raw_doi.replace("https://doi.org/", "").strip() if raw_doi else None
            title = str(item.get("title", "")).strip().rstrip(".")
            year = item.get("publication_year")
            
            # Authors
            authors = []
            for auth in item.get("authorships", []):
                a_name = auth.get("author", {}).get("display_name")
                if a_name:
                    authors.append(a_name)

            # Journal / Source
            journal = item.get("primary_location", {}).get("source", {}).get("display_name", "")

            # Reconstruct abstract from inverted index if present
            abstract = ""
            inv_idx = item.get("abstract_inverted_index")
            if isinstance(inv_idx, dict):
                word_positions = []
                for word, pos_list in inv_idx.items():
                    for pos in pos_list:
                        word_positions.append((pos, word))
                word_positions.sort(key=lambda x: x[0])
                abstract = " ".join(w for _, w in word_positions)

            pmid = None
            ids_dict = item.get("ids", {})
            if "pmid" in ids_dict:
                pmid = str(ids_dict["pmid"]).replace("https://pubmed.ncbi.nlm.nih.gov/", "").strip()

            records.append({
                "database": "OpenAlex",
                "openalex_id": openalex_id,
                "doi": doi,
                "pmid": pmid,
                "title": title,
                "authors": authors,
                "journal": str(journal).strip(),
                "year": year,
                "abstract": abstract,
                "cited_by_count": item.get("cited_by_count", 0),
                "raw_metadata": item
            })

        return {
            "database": "OpenAlex",
            "query": query,
            "status": "EXECUTED",
            "results_count": len(records),
            "records": records
        }

    def query_crossref(self, query: str, max_results: int = 50, mode: str = "offline") -> Dict[str, Any]:
        """Queries Crossref Metadata REST API."""
        if mode != "online":
            return {
                "database": "Crossref",
                "query": query,
                "status": "NOT_EXECUTED" if mode == "offline" else "RECORDED_FIXTURE",
                "results_count": 0,
                "records": []
            }

        self._rate_limit("crossref")
        params = {
            "query": query,
            "rows": str(max_results)
        }
        if self.polite_email:
            params["mailto"] = self.polite_email

        url = f"{self.API_ENDPOINTS['Crossref']}?{urllib.parse.urlencode(params)}"
        data = self._http_get_json(url)

        if "_error" in data:
            return {
                "database": "Crossref",
                "query": query,
                "status": "ERROR",
                "error": data["details"],
                "results_count": 0,
                "records": []
            }

        items = data.get("message", {}).get("items", [])
        records = []
        for item in items:
            doi = str(item.get("DOI", "")).strip().lower() or None
            titles = item.get("title", [])
            title = titles[0] if isinstance(titles, list) and titles else str(item.get("title", ""))
            title = title.strip().rstrip(".")

            authors = []
            for a in item.get("author", []):
                given = a.get("given", "")
                family = a.get("family", "")
                if family:
                    authors.append(f"{family} {given}".strip())

            year = None
            date_parts = item.get("published-print", {}).get("date-parts") or item.get("published-online", {}).get("date-parts")
            if date_parts and isinstance(date_parts, list) and len(date_parts) > 0:
                if len(date_parts[0]) > 0 and isinstance(date_parts[0][0], int):
                    year = date_parts[0][0]

            journals = item.get("container-title", [])
            journal = journals[0] if isinstance(journals, list) and journals else ""

            records.append({
                "database": "Crossref",
                "doi": doi,
                "title": title,
                "authors": authors,
                "journal": str(journal).strip(),
                "year": year,
                "cited_by_count": item.get("is-referenced-by-count", 0),
                "raw_metadata": item
            })

        return {
            "database": "Crossref",
            "query": query,
            "status": "EXECUTED",
            "results_count": len(records),
            "records": records
        }

    # =========================================================================
    # 2. FEDERATED RETRIEVAL ACROSS MULTIPLE QUERIES & SOURCES
    # =========================================================================

    def search_federated(
        self,
        queries: List[str],
        databases: Optional[List[str]] = None,
        max_results_per_source: int = 50,
        mode: str = "offline",
        fixture_corpus: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Orchestrates federated search across multiple queries and literature databases."""
        target_dbs = databases or ["PubMed", "Europe PMC", "OpenAlex", "Crossref"]
        raw_corpus = []
        search_log = []

        if mode == "fixture" and fixture_corpus is not None:
            raw_corpus = list(fixture_corpus)
            return {
                "execution_mode": "RECORDED_INTEGRATION_FIXTURE",
                "total_queries_executed": len(queries),
                "databases_queried": target_dbs,
                "total_raw_records": len(raw_corpus),
                "raw_corpus": raw_corpus,
                "search_log": [{"mode": "fixture", "loaded_records": len(raw_corpus)}]
            }

        if mode == "offline":
            for q in queries:
                for db in target_dbs:
                    search_log.append({
                        "query": q,
                        "database": db,
                        "status": "NOT_EXECUTED",
                        "message": "Offline dry-run mode active; network requests withheld."
                    })
            return {
                "execution_mode": "OFFLINE_DRY_RUN",
                "total_queries_executed": len(queries),
                "databases_queried": target_dbs,
                "total_raw_records": 0,
                "raw_corpus": [],
                "search_log": search_log
            }

        # Online mode: query sources using registered or custom backends
        for q in queries:
            for db in target_dbs:
                res = None
                backend = self.custom_backend or self.get_backend(db)
                if backend:
                    res = backend.search(q, max_results=max_results_per_source, mode="online")
                elif db == "PubMed":
                    res = self.query_pubmed(q, max_results=max_results_per_source, mode="online")
                elif db == "Europe PMC":
                    res = self.query_europe_pmc(q, max_results=max_results_per_source, mode="online")
                elif db == "OpenAlex":
                    res = self.query_openalex(q, max_results=max_results_per_source, mode="online")
                elif db == "Crossref":
                    res = self.query_crossref(q, max_results=max_results_per_source, mode="online")

                if res and res.get("status") == "EXECUTED":
                    recs = res.get("records", [])
                    raw_corpus.extend(recs)
                    search_log.append({
                        "query": q,
                        "database": db,
                        "status": "EXECUTED",
                        "hits_retrieved": len(recs)
                    })
                elif res:
                    search_log.append({
                        "query": q,
                        "database": db,
                        "status": res.get("status", "ERROR"),
                        "error": res.get("error", "Unknown error")
                    })

        return {
            "execution_mode": "ONLINE_FEDERATED_SEARCH",
            "total_queries_executed": len(queries),
            "databases_queried": target_dbs,
            "total_raw_records": len(raw_corpus),
            "raw_corpus": raw_corpus,
            "search_log": search_log
        }

    # =========================================================================
    # 3. CONNECTED-COMPONENT MULTI-IDENTIFIER DEDUPLICATION
    # =========================================================================

    @staticmethod
    def _normalize_title_for_comparison(title: str) -> str:
        """Strips punctuation, lowercases, and removes whitespace variations for robust matching."""
        if not title:
            return ""
        t = title.lower()
        t = re.sub(r'[^a-z0-9\s]', ' ', t)
        return " ".join(t.split())

    @classmethod
    def deduplicate_corpus(cls, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Connected-component graph deduplication across DOI, PMID, OpenAlex ID, and title similarity.
        
        Merges metadata across duplicates according to authoritative hierarchy:
        PubMed > Crossref > Europe PMC > OpenAlex.
        """
        if not records:
            return {
                "total_raw": 0,
                "total_unique": 0,
                "duplicate_clusters": 0,
                "reduction_percentage": 0.0,
                "unique_records": []
            }

        n = len(records)
        # Build adjacency graph
        adj: Dict[int, Set[int]] = {i: set() for i in range(n)}

        # Map persistent identifiers to record indices
        doi_map: Dict[str, List[int]] = {}
        pmid_map: Dict[str, List[int]] = {}
        alex_map: Dict[str, List[int]] = {}

        normalized_titles = []
        years = []

        for idx, rec in enumerate(records):
            doi = str(rec.get("doi", "")).strip().lower()
            if doi and len(doi) > 5:
                doi_map.setdefault(doi, []).append(idx)

            pmid = str(rec.get("pmid", "")).strip()
            if pmid and pmid.isdigit():
                pmid_map.setdefault(pmid, []).append(idx)

            alex_id = str(rec.get("openalex_id", "")).strip().lower()
            if alex_id:
                alex_map.setdefault(alex_id, []).append(idx)

            norm_t = cls._normalize_title_for_comparison(rec.get("title", ""))
            normalized_titles.append(norm_t)
            y = rec.get("year")
            years.append(int(y) if y and str(y).isdigit() else None)

        # 1. Connect identical DOIs
        for indices in doi_map.values():
            for i in indices:
                for j in indices:
                    if i != j:
                        adj[i].add(j)

        # 2. Connect identical PMIDs
        for indices in pmid_map.values():
            for i in indices:
                for j in indices:
                    if i != j:
                        adj[i].add(j)

        # 3. Connect identical OpenAlex IDs
        for indices in alex_map.values():
            for i in indices:
                for j in indices:
                    if i != j:
                        adj[i].add(j)

        # 4. Connect highly similar titles with matching publication year (SequenceMatcher >= 0.92)
        # ONLY if neither record possesses conflicting distinct persistent identifiers (DOI or PMID)
        for i in range(n):
            t_i = normalized_titles[i]
            y_i = years[i]
            doi_i = str(records[i].get("doi", "")).strip().lower()
            pmid_i = str(records[i].get("pmid", "")).strip()
            if not t_i or len(t_i) < 15:
                continue
            for j in range(i + 1, n):
                if j in adj[i]:
                    continue
                doi_j = str(records[j].get("doi", "")).strip().lower()
                pmid_j = str(records[j].get("pmid", "")).strip()

                # Distinct non-empty DOIs imply separate publications
                if doi_i and doi_j and doi_i != doi_j:
                    continue
                # Distinct non-empty PMIDs imply separate publications
                if pmid_i and pmid_j and pmid_i != pmid_j:
                    continue

                y_j = years[j]
                if y_i and y_j and abs(y_i - y_j) > 1:
                    continue  # Mismatched years by > 1 cannot be duplicates
                t_j = normalized_titles[j]
                if not t_j or len(t_j) < 15:
                    continue
                # Quick length check before SequenceMatcher
                len_ratio = len(t_i) / max(len(t_j), 1)
                if len_ratio < 0.75 or len_ratio > 1.33:
                    continue
                sim = difflib.SequenceMatcher(None, t_i, t_j).ratio()
                if sim >= 0.92:
                    adj[i].add(j)
                    adj[j].add(i)

        # 5. Connected Components using BFS
        visited = set()
        clusters: List[List[int]] = []

        for i in range(n):
            if i not in visited:
                cluster = []
                queue = [i]
                visited.add(i)
                while queue:
                    curr = queue.pop(0)
                    cluster.append(curr)
                    for neighbor in adj[curr]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                clusters.append(cluster)

        # 6. Merge each cluster into a canonical unified record
        AUTHORITY_PRIORITY = {"PubMed": 1, "Crossref": 2, "Europe PMC": 3, "OpenAlex": 4, "UNKNOWN": 5}
        unique_records = []
        duplicate_clusters_count = 0

        for c_idx, cluster in enumerate(clusters, 1):
            if len(cluster) > 1:
                duplicate_clusters_count += 1

            # Sort cluster items by authority hierarchy
            cluster_recs = [records[idx] for idx in cluster]
            cluster_recs.sort(key=lambda r: AUTHORITY_PRIORITY.get(r.get("database", "UNKNOWN"), 5))

            canonical = dict(cluster_recs[0])
            all_sources = set()
            all_dois = set()
            all_pmids = set()
            all_alex_ids = set()

            # Field-level provenance tracking
            field_provenance: Dict[str, str] = {}
            primary_db = canonical.get("database", "UNKNOWN")
            if canonical.get("title"): field_provenance["title"] = primary_db
            if canonical.get("doi"): field_provenance["doi"] = primary_db
            if canonical.get("pmid"): field_provenance["pmid"] = primary_db
            if canonical.get("openalex_id"): field_provenance["openalex_id"] = primary_db
            if canonical.get("year"): field_provenance["year"] = primary_db
            if canonical.get("authors"): field_provenance["authors"] = primary_db
            if canonical.get("journal"): field_provenance["journal"] = primary_db
            if canonical.get("abstract"): field_provenance["abstract"] = primary_db

            for r in cluster_recs:
                db_name = r.get("database", "UNKNOWN")
                if db_name:
                    all_sources.add(db_name)
                d = r.get("doi")
                if d:
                    all_dois.add(str(d).lower().strip())
                p = r.get("pmid")
                if p:
                    all_pmids.add(str(p).strip())
                a = r.get("openalex_id")
                if a:
                    all_alex_ids.add(str(a).strip().lower())

                # Fill missing canonical fields from secondary records with exact provenance
                if not canonical.get("abstract") and r.get("abstract"):
                    canonical["abstract"] = r["abstract"]
                    field_provenance["abstract"] = db_name
                if not canonical.get("year") and r.get("year"):
                    canonical["year"] = r["year"]
                    field_provenance["year"] = db_name
                if not canonical.get("authors") and r.get("authors"):
                    canonical["authors"] = r["authors"]
                    field_provenance["authors"] = db_name
                if not canonical.get("journal") and r.get("journal"):
                    canonical["journal"] = r["journal"]
                    field_provenance["journal"] = db_name

            canonical["retrieval_sources"] = sorted(list(all_sources))
            canonical["field_provenance"] = field_provenance
            canonical["doi"] = sorted(list(all_dois))[0] if all_dois else canonical.get("doi")
            canonical["pmid"] = sorted(list(all_pmids))[0] if all_pmids else canonical.get("pmid")
            canonical["openalex_id"] = sorted(list(all_alex_ids))[0] if all_alex_ids else canonical.get("openalex_id")
            canonical["cluster_size"] = len(cluster)
            canonical["study_id"] = canonical.get("study_id") or canonical.get("ref_id") or f"STUDY_UNIQ_{c_idx:03d}"

            unique_records.append(canonical)

        reduction = round(((n - len(unique_records)) / max(n, 1)) * 100.0, 1)

        return {
            "total_raw": n,
            "total_unique": len(unique_records),
            "duplicate_clusters": duplicate_clusters_count,
            "reduction_percentage": reduction,
            "unique_records": unique_records
        }

    # =========================================================================
    # 4. SATURATION CURVE & YIELD ANALYTICS
    # =========================================================================

    @classmethod
    def calculate_search_saturation(
        cls,
        faceted_batches: List[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """Calculates marginal unique paper yield per facet batch to detect search saturation."""
        seen_identifiers = set()
        saturation_curve = []

        for b_idx, batch in enumerate(faceted_batches, 1):
            batch_unique = 0
            has_high_value_discovery = False
            for r in batch:
                ident = str(r.get("doi") or r.get("pmid") or r.get("title", "")).lower().strip()
                if ident and ident not in seen_identifiers:
                    seen_identifiers.add(ident)
                    batch_unique += 1
                    # Detect high-value discovery in new unique items
                    t_str = f"{r.get('title','')} {r.get('abstract','')} {r.get('study_design','')}".lower()
                    if any(k in t_str for k in ["contradict", "discrepan", "inconsistent", "isobologram", "synergy index", "rct", "phase iii"]):
                        has_high_value_discovery = True

            marginal_yield = round(batch_unique / max(len(batch), 1), 3)
            saturation_curve.append({
                "facet_batch": b_idx,
                "batch_total": len(batch),
                "marginal_new_unique": batch_unique,
                "cumulative_unique": len(seen_identifiers),
                "marginal_yield_ratio": marginal_yield,
                "has_high_value_discovery": has_high_value_discovery
            })

        # Bounded deterministic saturation logic:
        # Saturated if >= 3 batches and marginal yield < 0.15, EXCEPT if the latest batch surfaced a high-value discovery
        # Hard ceiling on total batches evaluated (max 8) prevents infinite search loops.
        latest = saturation_curve[-1] if saturation_curve else {}
        is_yield_low = len(saturation_curve) >= 3 and latest.get("marginal_yield_ratio", 1.0) < 0.15
        is_hard_ceiling = len(saturation_curve) >= 8

        if is_hard_ceiling:
            is_saturated = True
            sat_status = "SATURATED_HARD_CEILING"
        elif is_yield_low and not latest.get("has_high_value_discovery", False):
            is_saturated = True
            sat_status = "SATURATED"
        elif is_yield_low and latest.get("has_high_value_discovery", False):
            is_saturated = False
            sat_status = "EXPANDING_HIGH_VALUE_DISCOVERY"
        else:
            is_saturated = False
            sat_status = "EXPANDING"

        return {
            "saturation_status": sat_status,
            "is_saturated": is_saturated,
            "total_cumulative_unique": len(seen_identifiers),
            "total_batches_evaluated": len(faceted_batches),
            "final_marginal_yield_ratio": latest.get("marginal_yield_ratio", 0.0),
            "saturation_curve": saturation_curve
        }

    # =========================================================================
    # 5. END-TO-END EXECUTION, SCREENING & PORTFOLIO SELECTION (<= 25 REFS)
    # =========================================================================

    def execute_and_screen(
        self,
        problem_model: Any,
        facet_queries: Optional[List[str]] = None,
        databases: Optional[List[str]] = None,
        mode: str = "offline",
        fixture_corpus: Optional[List[Dict[str, Any]]] = None,
        max_final_refs: int = MAX_FINAL_REFERENCES,
        min_final_refs: int = MIN_FINAL_REFERENCES
    ) -> Dict[str, Any]:
        """Executes federated search, deduplicates records, applies the 10-dimension Relevance Gate,
        classifies into 6 tiers, strictly drops IRRELEVANT papers, and selects top references under
        the strict ceiling of <= 25 references.
        """
        queries = facet_queries or ["Biomedical intervention efficacy in experimental disease model"]
        
        # Step 1: Federated Search
        search_result = self.search_federated(
            queries=queries,
            databases=databases,
            mode=mode,
            fixture_corpus=fixture_corpus
        )
        raw_corpus = search_result.get("raw_corpus", [])

        # Step 2: Connected-Component Deduplication
        dedup_result = self.deduplicate_corpus(raw_corpus)
        unique_corpus = dedup_result.get("unique_records", [])

        # Step 3 & 4 & 5: Relevance Screening, 14-Factor Scoring, and Optimal Selection (<= 25)
        selection_result = GenericReferenceAuditor.select_optimal_proposal_references(
            candidate_records=unique_corpus,
            problem_model=problem_model,
            max_references=max_final_refs,
            min_references=min_final_refs,
            total_retrieved_in_corpus=search_result.get("total_raw_records", len(raw_corpus))
        )

        # Audit the selected portfolio against strict institutional criteria
        selected_refs = selection_result.get("selected_references", [])
        portfolio_audit = GenericReferenceAuditor.audit_final_reference_portfolio(
            references=selected_refs,
            max_references=max_final_refs,
            min_references=min_final_refs
        )

        return {
            "search_adapter_version": "8.2.0",
            "execution_mode": search_result.get("execution_mode"),
            "search_provenance": {
                "queries_executed": len(queries),
                "databases_queried": search_result.get("databases_queried"),
                "total_raw_hits": search_result.get("total_raw_records"),
                "deduplicated_unique_hits": dedup_result.get("total_unique"),
                "duplicate_clusters_resolved": dedup_result.get("duplicate_clusters"),
                "deduplication_reduction_percent": dedup_result.get("reduction_percentage")
            },
            "screening_funnel": selection_result.get("screening_funnel"),
            "reference_portfolio_audit": portfolio_audit,
            "final_selected_count": len(selected_refs),
            "selected_references": selected_refs,
            "excluded_candidates_count": selection_result.get("excluded_candidates_count"),
            "excluded_candidates": selection_result.get("excluded_candidates"),
            "axis_distribution": selection_result.get("axis_distribution")
        }


if __name__ == "__main__":
    adapter = ScientificSearchAdapter()
    print("ScientificSearchAdapter initialized successfully.")
    print("Endpoints:", list(adapter.API_ENDPOINTS.keys()))
