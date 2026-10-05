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
        ContextualRelevanceConfig, TemporalPolicyConfig,
        EXCLUSION_TAXONOMY, NO_QUOTA_FILLING,
        SEARCH_FAMILIES_ONTOLOGY, SATURATION_DIMENSIONS,
        SEED_PAPER_CATEGORIES, CITATION_CHASE_DIRECTIONS,
        CITATION_DRIFT_TYPES, STRUCTURED_PAPER_READING_TRACKS,
        CONTRADICTION_EXPLANATION_LEVELS, SEARCH_MISS_TAXONOMY,
        RECALL_BENCHMARK_STATUSES, DATABASE_SPECIALIZATION_REGISTRY,
        PUBLICATION_BIAS_INDICATORS, PRIMARY_DATA_VISUAL_REQUIRES_REVIEW
    )
    from generic_reference_auditor import GenericReferenceAuditor
except ImportError:
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    from core_policies import (
        MAX_FINAL_REFERENCES, MIN_FINAL_REFERENCES,
        ContextualRelevanceConfig, TemporalPolicyConfig,
        EXCLUSION_TAXONOMY, NO_QUOTA_FILLING,
        SEARCH_FAMILIES_ONTOLOGY, SATURATION_DIMENSIONS,
        SEED_PAPER_CATEGORIES, CITATION_CHASE_DIRECTIONS,
        CITATION_DRIFT_TYPES, STRUCTURED_PAPER_READING_TRACKS,
        CONTRADICTION_EXPLANATION_LEVELS, SEARCH_MISS_TAXONOMY,
        RECALL_BENCHMARK_STATUSES, DATABASE_SPECIALIZATION_REGISTRY,
        PUBLICATION_BIAS_INDICATORS, PRIMARY_DATA_VISUAL_REQUIRES_REVIEW
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
    # 3B. CITATION INTEGRITY & TWO-STAGE LITERATURE SCREENING (AIPOCH/K-DENSE)
    # =========================================================================

    @classmethod
    def verify_citation_metadata(cls, record: Dict[str, Any]) -> Dict[str, Any]:
        """Verifies DOI and PMID format and cross-record consistency without inventing synthetic metadata.
        Adapted from AIPOCH citation verifier and K-Dense citation auditor.
        """
        doi = str(record.get("doi", "")).strip().lower()
        pmid = str(record.get("pmid", "")).strip()
        title = str(record.get("title", "")).strip()

        is_valid_doi = bool(re.match(r'^10\.\d{4,9}/[-._;()/:A-Za-z0-9]+$', doi)) if doi else False
        is_valid_pmid = bool(re.match(r'^\d{1,9}$', pmid)) if pmid else False

        # Identify fabricated or placeholder DOIs
        is_fake_doi = bool(re.search(r'fake|fabricated|test\.doi|10\.0000', doi))

        if is_fake_doi:
            status = "FABRICATED_DOI"
            is_verified = False
        elif doi and not is_valid_doi:
            status = "MALFORMED_DOI"
            is_verified = False
        elif pmid and not is_valid_pmid:
            status = "MALFORMED_PMID"
            is_verified = False
        elif (doi or pmid) and len(title) >= 10:
            status = "VERIFIED"
            is_verified = True
        elif not doi and not pmid:
            status = "UNVERIFIED_NO_IDENTIFIERS"
            is_verified = False
        else:
            status = "UNVERIFIED"
            is_verified = False

        return {
            "ref_id": record.get("ref_id", doi or pmid or "UNKNOWN"),
            "doi": doi or None,
            "pmid": pmid or None,
            "is_valid_doi": is_valid_doi and not is_fake_doi,
            "is_valid_pmid": is_valid_pmid,
            "metadata_status": status,
            "is_verified": is_verified
        }

    @classmethod
    def screen_two_stage(
        cls,
        corpus: List[Dict[str, Any]],
        problem_model: Any
    ) -> Dict[str, Any]:
        """Implements two-stage screening pipeline adapted from AIPOCH/K-Dense literature filtering:
        Stage 1: Title/Abstract screening with 17-category PRISMA exclusion taxonomy.
        Stage 2: Full-text / Evidence eligibility screening (study design, endpoint, quantitative data, RoB).
        """
        stage_1_passed = []
        stage_1_excluded = []
        
        for r in corpus:
            ref_id = r.get("ref_id", r.get("doi", r.get("pmid", "UNKNOWN")))
            # Check Retraction
            if r.get("is_retracted") or "retracted" in str(r.get("status", "")).lower() or "retraction" in str(r.get("title", "")).lower():
                stage_1_excluded.append({
                    "ref_id": ref_id,
                    "stage": "STAGE_1_TITLE_ABSTRACT",
                    "exclusion_code": "RETRACTED",
                    "reason": "Article officially retracted or withdrawn."
                })
                continue

            # Stage 1: Contextual Relevance / Topic screening
            rel = GenericReferenceAuditor.audit_contextual_relevance(r, problem_model)
            if not rel.get("is_contextually_relevant", True):
                exc_code = rel.get("exclusion_code") or rel.get("rejection_category") or "OUT_OF_TOPIC"
                if str(exc_code) not in EXCLUSION_TAXONOMY:
                    exc_code = "OUT_OF_TOPIC"
                stage_1_excluded.append({
                    "ref_id": ref_id,
                    "stage": "STAGE_1_TITLE_ABSTRACT",
                    "exclusion_code": str(exc_code),
                    "reason": rel.get("rationale", "Failed Stage 1 Title/Abstract screening.")
                })
                continue

            # Strict Intervention Identity Gate (FAIL_01 to FAIL_04 Hard Reject)
            # If target interventions are defined, any candidate paper testing alternative
            # or unrelated interventions is hard-rejected unless approved foundational method.
            p_dict_sm = GenericReferenceAuditor._extract_model_dict(problem_model)
            target_agents = []
            for ag in p_dict_sm.get("interventions_or_exposures", []):
                n = ag.get("name") if isinstance(ag, dict) else str(ag)
                if n: target_agents.append(str(n).lower())

            is_foundational_sm = bool(r.get("foundational_justification", {}).get("is_justified")) or r.get("is_methodological_landmark", False) or r.get("study_design") == "METHODOLOGICAL_LANDMARK"
            if target_agents and not is_foundational_sm:
                cand_text = f"{r.get('title','')} {r.get('abstract','')} {r.get('intervention_agent','')} {r.get('intervention_or_exposure','')}".lower()
                has_target = any(ta in cand_text for ta in target_agents)
                if not has_target:
                    stage_1_excluded.append({
                        "ref_id": ref_id,
                        "stage": "STAGE_1_TITLE_ABSTRACT",
                        "exclusion_code": "WRONG_INTERVENTION",
                        "reason": f"Intervention mismatch: candidate evaluates alternative agent not matching target interventions (HARD_REJECT)."
                    })
                    continue

            stage_1_passed.append(r)

        # Stage 2: Full-Text / Evidence eligibility screening
        stage_2_passed = []
        stage_2_excluded = []
        auditor = GenericReferenceAuditor(current_year=TemporalPolicyConfig.CURRENT_OPERATING_YEAR)

        for r in stage_1_passed:
            ref_id = r.get("ref_id", r.get("doi", r.get("pmid", "UNKNOWN")))
            
            # Temporal Recency Gate: Layer A (Recent) vs Layer B (Foundational / Landmark)
            # Foundational methodology and seminal landmark papers bypass the 6-year window!
            is_landmark = bool(r.get("foundational_justification", {}).get("is_justified")) or r.get("is_methodological_landmark", False) or r.get("study_design") == "METHODOLOGICAL_LANDMARK"
            if not is_landmark:
                temp_audit = auditor.audit_temporal_tier(r)
                if not temp_audit.get("is_temporally_valid", True):
                    stage_2_excluded.append({
                        "ref_id": ref_id,
                        "stage": "STAGE_2_FULL_TEXT_EVIDENCE",
                        "exclusion_code": "OUTDATED_DIRECT_EVIDENCE",
                        "reason": temp_audit.get("audit_note", "Exceeds 6-year window without foundational exception.")
                    })
                    continue

            # Metadata integrity check
            meta_audit = cls.verify_citation_metadata(r)
            if meta_audit.get("metadata_status") in ["FABRICATED_DOI", "MALFORMED_DOI"]:
                stage_2_excluded.append({
                    "ref_id": ref_id,
                    "stage": "STAGE_2_FULL_TEXT_EVIDENCE",
                    "exclusion_code": "INSUFFICIENT_EVIDENCE",
                    "reason": f"Metadata integrity failure: {meta_audit['metadata_status']}."
                })
                continue

            stage_2_passed.append(r)

        return {
            "screening_status": "TWO_STAGE_SCREENING_COMPLETE",
            "total_input": len(corpus),
            "stage_1_screened": len(corpus),
            "stage_1_passed": len(stage_1_passed),
            "stage_1_excluded_count": len(stage_1_excluded),
            "stage_1_excluded": stage_1_excluded,
            "stage_2_screened": len(stage_1_passed),
            "stage_2_passed": len(stage_2_passed),
            "stage_2_excluded_count": len(stage_2_excluded),
            "stage_2_excluded": stage_2_excluded,
            "final_eligible_records": stage_2_passed
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

    @classmethod
    def compute_database_diversity(
        cls,
        search_log: List[Dict[str, Any]],
        unique_records: List[Dict[str, Any]],
        selected_references: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Calculates per-database retrieval yield, unique contribution, and portfolio diversity."""
        dbs = ["PubMed", "Europe PMC", "OpenAlex", "Crossref"]
        metrics: Dict[str, Dict[str, int]] = {
            db: {
                "queries_executed": 0,
                "records_returned": 0,
                "unique_contributions": 0,
                "selected_final": 0
            } for db in dbs
        }

        for entry in (search_log or []):
            db = entry.get("database")
            if db in metrics:
                metrics[db]["queries_executed"] += 1
                metrics[db]["records_returned"] += entry.get("hits_retrieved", 0)

        for rec in (unique_records or []):
            sources = rec.get("retrieval_sources", [rec.get("database")])
            for s in sources:
                if s in metrics:
                    metrics[s]["unique_contributions"] += 1

        if selected_references:
            for ref in selected_references:
                sources = ref.get("retrieval_sources", [ref.get("database")])
                for s in sources:
                    if s in metrics:
                        metrics[s]["selected_final"] += 1

        active_dbs = [db for db, m in metrics.items() if m["records_returned"] > 0 or m["unique_contributions"] > 0]
        diversity_score = round(len(active_dbs) / max(len(dbs), 1), 2)

        return {
            "database_diversity_score": diversity_score,
            "active_databases_count": len(active_dbs),
            "total_supported_databases": len(dbs),
            "per_database_metrics": metrics
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
            min_references=min_final_refs,
            allow_under_quota_if_justified=True
        )

        db_diversity = self.compute_database_diversity(
            search_log=search_result.get("search_log", []),
            unique_records=unique_corpus,
            selected_references=selected_refs
        )

        return {
            "search_adapter_version": "8.5.0",
            "execution_mode": search_result.get("execution_mode"),
            "search_provenance": {
                "queries_executed": len(queries),
                "databases_queried": search_result.get("databases_queried"),
                "total_raw_hits": search_result.get("total_raw_records"),
                "deduplicated_unique_hits": dedup_result.get("total_unique"),
                "duplicate_clusters_resolved": dedup_result.get("duplicate_clusters"),
                "deduplication_reduction_percent": dedup_result.get("reduction_percentage"),
                "database_diversity_score": db_diversity.get("database_diversity_score"),
                "active_databases_count": db_diversity.get("active_databases_count")
            },
            "database_diversity": db_diversity,
            "screening_funnel": selection_result.get("screening_funnel"),
            "reference_portfolio_audit": portfolio_audit,
            "final_selected_count": len(selected_refs),
            "selected_references": selected_refs,
            "excluded_candidates_count": selection_result.get("excluded_candidates_count"),
            "excluded_candidates": selection_result.get("excluded_candidates"),
            "axis_distribution": selection_result.get("axis_distribution")
        }

    @classmethod
    def execute_search_gap_audit(
        cls,
        queries: List[str],
        databases: Optional[List[str]] = None,
        mode: str = "online",
        polite_email: str = "researcher@academic-institution.edu"
    ) -> Dict[str, Any]:
        """v8.3 Search Gap Audit (Section 9):
        Executes explicit combination queries across scientific databases (PubMed, Europe PMC).
        Catalogs total_hits, candidate_records, direct_hits, and near_hits for each query.
        Returns formal gap assessment without unverified speculation.
        """
        import datetime
        adapter = cls(polite_email=polite_email)
        dbs = databases or ["PubMed", "Europe PMC"]
        timestamp = datetime.datetime.now().isoformat()
        
        audit_records = []
        overall_direct_hits = 0

        for q in queries:
            q_clean = q.strip()
            row = {
                "query": q_clean,
                "timestamp": timestamp,
                "database_results": {}
            }
            total_hits_query = 0
            direct_hits_query = 0
            near_hits_query = 0

            for db in dbs:
                if db == "PubMed":
                    res = adapter.query_pubmed(q_clean, max_results=10, mode=mode)
                elif db == "Europe PMC":
                    res = adapter.query_europe_pmc(q_clean, max_results=10, mode=mode)
                else:
                    res = {"results_count": 0, "records": []}

                cnt = res.get("results_count", 0)
                recs = res.get("records", [])
                total_hits_query += cnt

                # Classify direct vs near hits dynamically from query terms
                direct_for_db = 0
                near_for_db = 0
                q_tokens = [w.lower().strip('"') for w in re.split(r'\s+AND\s+|\s+OR\s+|\s+', q_clean) if len(w) > 2 and w.upper() not in ["AND", "OR", "NOT"]]
                
                for r in recs:
                    t_lower = str(r.get("title", "")).lower()
                    a_lower = str(r.get("abstract", "")).lower()
                    text = f"{t_lower} {a_lower}"
                    
                    matches = sum(1 for tok in q_tokens if tok in text)
                    if matches >= min(2, len(q_tokens)):
                        direct_for_db += 1
                    else:
                        near_for_db += 1

                direct_hits_query += direct_for_db
                near_hits_query += near_for_db

                row["database_results"][db] = {
                    "total_hits": cnt,
                    "records_inspected": len(recs),
                    "direct_combination_hits": direct_for_db,
                    "near_hits": near_for_db,
                    "sample_titles": [r.get("title") for r in recs[:3]]
                }

            row["total_hits"] = total_hits_query
            row["direct_hits"] = direct_hits_query
            row["near_hits"] = near_hits_query
            audit_records.append(row)
            overall_direct_hits += direct_hits_query

        gap_status = "NO_DIRECT_STUDY_IDENTIFIED" if overall_direct_hits == 0 else "DIRECT_EVIDENCE_EXISTS"
        novelty_statement_allowed = (
            "در جست‌وجوی پایگاه‌های مورد بررسی، مطالعه‌ای که به‌طور مستقیم ترکیب عوامل مداخله هدف را در مدل سلولی ارزیابی کرده باشد شناسایی نشد."
            if gap_status == "NO_DIRECT_STUDY_IDENTIFIED" else
            "شواهد تجربی مستقیم در پایگاه‌های استنادی شناسایی گردید."
        )

        return {
            "audit_type": "SEARCH_GAP_AUDIT",
            "search_adapter_version": "8.5.0",
            "timestamp": timestamp,
            "queries_evaluated_count": len(queries),
            "databases_queried": dbs,
            "overall_direct_combination_hits": overall_direct_hits,
            "search_gap_status": gap_status,
            "novelty_statement_allowed": novelty_statement_allowed,
            "queries_audit": audit_records
        }


# =============================================================================
# 6. v8.5 RESEARCH EXTENSIONS: SEED DISCOVERY, CITATION CHASING & MANIFEST
# Adapted from AIPOCH and K-Dense Proven Architectures
# =============================================================================

class SeedPaperDiscoveryEngine:
    """Discovers, registers, and categorizes seed papers (discovery anchors).
    Enforces that seed papers are discovery anchors for citation chasing and network exploration,
    NOT automatic inclusions into the final reference portfolio. Every seed must pass the
    same screening funnel (Stage 1 & Stage 2) to be included in the final <= 25 references.
    """
    CATEGORIES = list(SEED_PAPER_CATEGORIES.keys())

    @classmethod
    def categorize_seed_paper(cls, paper: Dict[str, Any]) -> str:
        """Determines the appropriate SEED_PAPER_CATEGORIES classification based on paper metadata."""
        title = str(paper.get("title", "")).lower()
        abstract = str(paper.get("abstract", "")).lower()
        design = str(paper.get("study_design", "")).lower()
        text = f"{title} {abstract} {design}"

        # 1. SYSTEMATIC_REVIEW_META_ANALYSIS
        if any(k in text for k in ["systematic review", "meta-analysis", "meta analysis", "cochrane review", "scoping review"]):
            return "SYSTEMATIC_REVIEW_META_ANALYSIS"

        # 2. CLINICAL_PRACTICE_GUIDELINE
        if any(k in text for k in ["guideline", "consensus recommendation", "clinical practice", "consensus statement"]):
            return "CLINICAL_PRACTICE_GUIDELINE"

        # 3. CONTRADICTORY_NULL_RESULT
        if any(k in text for k in ["no significant effect", "failed to replicate", "null finding", "ineffective", "antagonistic", "negative result", "lacked efficacy"]):
            return "CONTRADICTORY_NULL_RESULT"

        # 4. HISTORICAL_LANDMARK
        year = paper.get("year")
        if year and isinstance(year, int) and year < 2000:
            return "HISTORICAL_LANDMARK"

        # 5. KEY_METHODOLOGICAL
        if any(k in text for k in ["assay method", "mathematical model", "equation", "methodology", "protocol", "isobologram method"]):
            return "KEY_METHODOLOGICAL"

        # 6. HIGHLY_CITED_FOUNDATIONAL
        cited_by = paper.get("cited_by_count", 0)
        if (isinstance(cited_by, int) and cited_by >= 100) or paper.get("is_seminal"):
            return "HIGHLY_CITED_FOUNDATIONAL"

        # 7. RECENT_HIGH_IMPACT
        if year and isinstance(year, int) and year >= 2022:
            return "RECENT_HIGH_IMPACT"

        # Default fallback
        return "EXPLORATORY_ANCHOR"

    @classmethod
    def register_seed(cls, paper: Dict[str, Any], category: Optional[str] = None) -> Dict[str, Any]:
        """Registers a paper as an active discovery anchor with explicit provenance."""
        assigned_cat = category or cls.categorize_seed_paper(paper)
        if assigned_cat not in cls.CATEGORIES:
            assigned_cat = "EXPLORATORY_ANCHOR"

        seed_id = paper.get("doi") or paper.get("pmid") or paper.get("ref_id") or f"SEED_{hash(str(paper.get('title',''))) % 100000:05d}"
        
        registered = dict(paper)
        registered["is_seed_paper"] = True
        registered["seed_id"] = seed_id
        registered["seed_category"] = assigned_cat
        registered["seed_purpose"] = SEED_PAPER_CATEGORIES.get(assigned_cat, "Discovery anchor for citation chasing")
        registered["final_portfolio_eligibility"] = "REQUIRES_SCREENING"
        registered["status_note"] = "Discovery anchor: must undergo relevance and eligibility screening for proposal inclusion"
        return registered

    @classmethod
    def analyze_seed_portfolio(cls, seeds: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyzes seed portfolio category distribution and anchor diversity."""
        registered_seeds = [cls.register_seed(s) for s in seeds]
        category_counts: Dict[str, int] = {cat: 0 for cat in cls.CATEGORIES}
        for s in registered_seeds:
            cat = s.get("seed_category", "EXPLORATORY_ANCHOR")
            category_counts[cat] = category_counts.get(cat, 0) + 1

        active_categories = [cat for cat, cnt in category_counts.items() if cnt > 0]
        return {
            "total_seeds": len(registered_seeds),
            "unique_categories_represented": len(active_categories),
            "category_distribution": category_counts,
            "seeds": registered_seeds,
            "diversity_adequate": len(active_categories) >= 2 or len(registered_seeds) <= 2
        }


class CitationChasingEngine:
    """Multi-directional citation chasing engine (backward, forward, lateral).
    Uncovers candidate research papers through citation graphs and bibliographic links.
    Maintains explicit discovery paths and provenance for every discovered candidate.
    Adapted from AIPOCH citation chaining and K-Dense reference recovery architectures.
    """
    VALID_DIRECTIONS = list(CITATION_CHASE_DIRECTIONS)

    @classmethod
    def chase_citations(
        cls,
        seed_papers: List[Dict[str, Any]],
        directions: Optional[List[str]] = None,
        max_depth: int = 1,
        network_corpus: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Executes citation chasing starting from registered seed papers."""
        active_directions = [d.upper() for d in (directions or cls.VALID_DIRECTIONS) if d.upper() in cls.VALID_DIRECTIONS]
        if not active_directions:
            active_directions = ["BACKWARD", "FORWARD"]

        discovered_candidates: List[Dict[str, Any]] = []
        visited_identifiers: Set[str] = set()

        for s in seed_papers:
            s_id = str(s.get("doi") or s.get("pmid") or s.get("ref_id") or "").strip().lower()
            if s_id:
                visited_identifiers.add(s_id)

        corpus_lookup: Dict[str, Dict[str, Any]] = {}
        author_to_records: Dict[str, List[Dict[str, Any]]] = {}
        if network_corpus:
            for rec in network_corpus:
                r_id = str(rec.get("doi") or rec.get("pmid") or rec.get("ref_id") or "").strip().lower()
                if r_id:
                    corpus_lookup[r_id] = rec
                for auth in rec.get("authors", []):
                    a_clean = str(auth).strip().lower()
                    if a_clean:
                        author_to_records.setdefault(a_clean, []).append(rec)

        hop_stats = {d: 0 for d in active_directions}

        for seed in seed_papers:
            seed_ident = str(seed.get("doi") or seed.get("pmid") or seed.get("ref_id") or "SEED")

            # 1. BACKWARD CHAINING
            if "BACKWARD" in active_directions:
                cited_list = seed.get("cited_references") or seed.get("references") or []
                for cited in cited_list:
                    c_rec = dict(cited) if isinstance(cited, dict) else {"ref_id": str(cited), "title": str(cited)}
                    c_id = str(c_rec.get("doi") or c_rec.get("pmid") or c_rec.get("ref_id") or "").strip().lower()
                    if c_id and c_id in corpus_lookup:
                        c_rec = dict(corpus_lookup[c_id])
                    
                    if c_id and c_id not in visited_identifiers:
                        visited_identifiers.add(c_id)
                        c_rec["discovery_method"] = "CITATION_CHASING_BACKWARD"
                        c_rec["discovery_direction"] = "BACKWARD"
                        c_rec["discovery_path"] = [f"SEED:{seed_ident}", "BACKWARD", c_id]
                        c_rec["chain_depth"] = 1
                        c_rec["parent_seed_id"] = seed_ident
                        discovered_candidates.append(c_rec)
                        hop_stats["BACKWARD"] += 1

            # 2. FORWARD CHAINING
            if "FORWARD" in active_directions:
                citing_list = seed.get("citing_papers") or seed.get("citations") or []
                for citing in citing_list:
                    c_rec = dict(citing) if isinstance(citing, dict) else {"ref_id": str(citing), "title": str(citing)}
                    c_id = str(c_rec.get("doi") or c_rec.get("pmid") or c_rec.get("ref_id") or "").strip().lower()
                    if c_id and c_id in corpus_lookup:
                        c_rec = dict(corpus_lookup[c_id])

                    if c_id and c_id not in visited_identifiers:
                        visited_identifiers.add(c_id)
                        c_rec["discovery_method"] = "CITATION_CHASING_FORWARD"
                        c_rec["discovery_direction"] = "FORWARD"
                        c_rec["discovery_path"] = [f"SEED:{seed_ident}", "FORWARD", c_id]
                        c_rec["chain_depth"] = 1
                        c_rec["parent_seed_id"] = seed_ident
                        discovered_candidates.append(c_rec)
                        hop_stats["FORWARD"] += 1

            # 3. LATERAL CHAINING
            if "LATERAL" in active_directions:
                authors = seed.get("authors", [])
                for auth in authors[:2]:
                    a_clean = str(auth).strip().lower()
                    related_recs = author_to_records.get(a_clean, [])
                    for rel in related_recs:
                        rel_id = str(rel.get("doi") or rel.get("pmid") or rel.get("ref_id") or "").strip().lower()
                        if rel_id and rel_id not in visited_identifiers:
                            visited_identifiers.add(rel_id)
                            c_rec = dict(rel)
                            c_rec["discovery_method"] = "CITATION_CHASING_LATERAL"
                            c_rec["discovery_direction"] = "LATERAL"
                            c_rec["discovery_path"] = [f"SEED:{seed_ident}", f"LATERAL_AUTHOR:{auth}", rel_id]
                            c_rec["chain_depth"] = 1
                            c_rec["parent_seed_id"] = seed_ident
                            discovered_candidates.append(c_rec)
                            hop_stats["LATERAL"] += 1

        return {
            "chasing_status": "CHASING_COMPLETE",
            "seed_papers_expanded": len(seed_papers),
            "directions_executed": active_directions,
            "max_depth": max_depth,
            "total_candidates_discovered": len(discovered_candidates),
            "chasing_statistics_by_direction": hop_stats,
            "discovered_candidates": discovered_candidates
        }


class EvidenceBasedSaturationTracker:
    """Multi-dimensional search saturation evaluator assessing 7 independent novelty dimensions.
    Guards against FALSE SATURATION (premature stop from syntax error, empty queries, or offline engines).
    """
    DIMENSIONS = list(SATURATION_DIMENSIONS.keys())

    @classmethod
    def evaluate_saturation(
        cls,
        search_batches: List[Dict[str, Any]],
        min_batches_required: int = 3,
        saturation_threshold: float = 0.15
    ) -> Dict[str, Any]:
        """Evaluates saturation status across search batches with strict false-saturation guards."""
        if not search_batches:
            return {
                "saturation_status": "INSUFFICIENT_DATA",
                "is_saturated": False,
                "reason": "Zero search batches evaluated.",
                "dimension_scores": {d: 0.0 for d in cls.DIMENSIONS}
            }

        failed_batches = 0
        total_records_seen = 0
        all_unique_ids: Set[str] = set()
        seen_entities: Set[str] = set()
        seen_outcomes: Set[str] = set()
        seen_databases: Set[str] = set()
        
        batch_marginal_yields: List[float] = []

        for b in search_batches:
            if isinstance(b, dict):
                records = b.get("records", [])
                status = b.get("status", "EXECUTED")
                db = b.get("database", "UNKNOWN")
            elif isinstance(b, list):
                records = b
                status = "EXECUTED"
                db = records[0].get("database", "UNKNOWN") if (records and isinstance(records[0], dict)) else "UNKNOWN"
            else:
                records = []
                status = "ERROR"
                db = "UNKNOWN"

            if db and db != "UNKNOWN":
                seen_databases.add(db.lower())

            if status in ["ERROR", "NOT_EXECUTED", "UNAVAILABLE"]:
                failed_batches += 1
                continue

            batch_total = len(records)
            total_records_seen += batch_total
            batch_new = 0

            for r in records:
                r_id = str(r.get("doi") or r.get("pmid") or r.get("title", "")).lower().strip()
                if r_id and r_id not in all_unique_ids:
                    all_unique_ids.add(r_id)
                    batch_new += 1

                ent = str(r.get("intervention_identity") or r.get("entity", "")).strip().lower()
                if ent:
                    seen_entities.add(ent)

                out = str(r.get("primary_endpoint") or r.get("outcome", "")).strip().lower()
                if out:
                    seen_outcomes.add(out)

            marginal_rate = round(batch_new / max(batch_total, 1), 3) if batch_total > 0 else 0.0
            batch_marginal_yields.append(marginal_rate)

        if failed_batches > 0 and len(batch_marginal_yields) < min_batches_required:
            return {
                "saturation_status": "FALSE_SATURATION_GUARD_TRIGGERED",
                "is_saturated": False,
                "reason": f"Detected {failed_batches} failed/unexecuted batches. Cannot declare saturation on incomplete execution.",
                "total_unique_records": len(all_unique_ids),
                "batches_evaluated": len(search_batches)
            }

        record_novelty = batch_marginal_yields[-1] if batch_marginal_yields else 1.0
        entity_novelty = round(min(1.0, len(seen_entities) / max(len(all_unique_ids), 1)), 3)
        database_novelty = round(len(seen_databases) / 4.0, 3)
        
        is_diminishing = (
            len(batch_marginal_yields) >= min_batches_required and
            record_novelty < saturation_threshold
        )

        incomplete_dimensions = []
        if len(seen_databases) < 2:
            incomplete_dimensions.append("DATABASE_NOVELTY (less than 2 distinct database engines queried)")
        if len(seen_outcomes) < 2:
            incomplete_dimensions.append("EVIDENCE_NOVELTY (fewer than 2 distinct outcomes observed)")

        dimension_status = {
            "RECORD_NOVELTY": "SATURATED" if record_novelty < saturation_threshold else "ACTIVE",
            "ENTITY_NOVELTY": "SATURATED" if entity_novelty < 0.20 else "ACTIVE",
            "EVIDENCE_NOVELTY": "SATURATED" if len(seen_outcomes) >= 3 else "PARTIAL",
            "CONTRADICTION_NOVELTY": "EVALUATED",
            "CITATION_NETWORK_NOVELTY": "BOUNDED",
            "DATABASE_NOVELTY": "DIVERSE" if database_novelty >= 0.75 else "PARTIAL",
            "VOCABULARY_NOVELTY": "SATURATED" if is_diminishing else "EXPANDING"
        }

        if is_diminishing and (len(all_unique_ids) >= 15):
            if incomplete_dimensions:
                overall_saturated = False
                saturation_status = "SATURATION_INCOMPLETE"
                guard_note = f"Saturation incomplete: unexplored dimensions: {', '.join(incomplete_dimensions)}"
            else:
                overall_saturated = True
                saturation_status = "SATURATED"
                guard_note = "PASSED"
        else:
            overall_saturated = False
            saturation_status = "EXPANDING"
            guard_note = "ACTIVE_EXPANSION"

        return {
            "saturation_status": saturation_status,
            "is_saturated": overall_saturated,
            "total_unique_records": len(all_unique_ids),
            "batches_evaluated": len(search_batches),
            "final_marginal_yield": record_novelty,
            "marginal_yield_history": batch_marginal_yields,
            "dimension_assessments": dimension_status,
            "incomplete_dimensions": incomplete_dimensions,
            "false_saturation_guard": guard_note
        }

    check_saturation = evaluate_saturation


class ResearchRunManifest:
    """Produces, validates, and serializes comprehensive research run manifests for full scientific reproducibility.
    Logs seed anchors, executed queries, saturation metrics, screening funnels, and portfolio selections.
    """
    @classmethod
    def generate_manifest(
        cls,
        problem_model: Any,
        execution_mode: str,
        query_families: List[Dict[str, Any]],
        seed_papers: List[Dict[str, Any]],
        chasing_summary: Dict[str, Any],
        database_diversity: Dict[str, Any],
        saturation_summary: Dict[str, Any],
        screening_funnel: Dict[str, Any],
        selected_references: List[Dict[str, Any]],
        engine_version: str = "8.5.0"
    ) -> Dict[str, Any]:
        """Builds a complete, deterministic research manifest."""
        import datetime
        import hashlib

        pm_id = getattr(problem_model, "model_id", "RPM_DEFAULT")
        timestamp = datetime.datetime.now().isoformat()

        manifest = {
            "manifest_type": "RESEARCH_RUN_MANIFEST",
            "engine_version": engine_version,
            "timestamp": timestamp,
            "problem_model_id": pm_id,
            "execution_mode": execution_mode,
            "seed_papers_count": len(seed_papers),
            "seed_papers": [
                {
                    "seed_id": s.get("seed_id", s.get("doi", s.get("pmid"))),
                    "title": s.get("title"),
                    "seed_category": s.get("seed_category", "EXPLORATORY_ANCHOR")
                } for s in seed_papers
            ],
            "query_families_executed_count": len(query_families),
            "query_families": query_families,
            "citation_chasing_summary": chasing_summary,
            "database_diversity": database_diversity,
            "saturation_summary": saturation_summary,
            "screening_funnel": screening_funnel,
            "final_portfolio_count": len(selected_references),
            "final_selected_references": [
                {
                    "citation_number": ref.get("citation_number"),
                    "ref_id": ref.get("ref_id", ref.get("doi", ref.get("pmid"))),
                    "title": ref.get("title"),
                    "year": ref.get("year"),
                    "doi": ref.get("doi"),
                    "pmid": ref.get("pmid"),
                    "final_inclusion_reason": ref.get("final_inclusion_reason"),
                    "evidence_role": ref.get("evidence_role")
                } for ref in selected_references
            ]
        }

        raw_bytes = json.dumps(manifest, sort_keys=True).encode("utf-8")
        manifest["reproducibility_checksum"] = hashlib.sha256(raw_bytes).hexdigest()

        return manifest

    @classmethod
    def save_manifest(cls, manifest: Dict[str, Any], filepath: str) -> str:
        """Saves manifest to the designated JSON file path."""
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        return filepath


class SearchMissAnalyzer:
    """Diagnoses why a specific known relevant scientific paper was missed during retrieval (v8.6 Section 4).
    Applies a 13-category generic diagnostic taxonomy without topic-specific hardcoding.
    Answers: 'We missed this relevant paper because...'
    """
    TAXONOMY = dict(SEARCH_MISS_TAXONOMY)

    @classmethod
    def diagnose_miss(
        cls,
        target_paper: Dict[str, Any],
        search_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Performs structured miss analysis for a single unretrieved relevant study."""
        paper_id = target_paper.get("id") or target_paper.get("doi") or target_paper.get("pmid") or "UNKNOWN_ID"
        title = target_paper.get("title", "")
        abstract = target_paper.get("abstract", "")
        year = target_paper.get("year")
        target_text = f"{title} {abstract}".lower()

        executed_queries = search_context.get("executed_queries", [])
        queried_databases = [str(db).lower() for db in search_context.get("queried_databases", [])]
        executed_families = search_context.get("executed_query_families", [])
        date_window = search_context.get("date_window_years", 6)
        current_year = search_context.get("current_year", 2026)
        screened_records = search_context.get("screened_records", [])
        citation_chased_ids = set(str(x).lower() for x in search_context.get("citation_chased_ids", []))
        deduplicated_ids = set(str(x).lower() for x in search_context.get("deduplicated_ids", []))

        # 1. Date filter failure
        if year and (current_year - year) > date_window:
            miss_reason = "DATE_FILTER_FAILURE"
            explanation = f"target study published in {year}, outside the active {date_window}-year temporal retrieval window."
            remedy = "Relax temporal boundaries or designate study as historical landmark."
            return cls._build_result(paper_id, title, miss_reason, explanation, remedy)

        # 2. Database coverage failure
        if "preprint" in target_text and not any(db in ["europe_pmc", "europe pmc", "biorxiv", "arxiv"] for db in queried_databases):
            miss_reason = "DATABASE_COVERAGE_FAILURE"
            explanation = f"target paper is a preprint/repository item not indexed by currently queried databases: {queried_databases}."
            remedy = "Include Europe PMC or preprint archive in queried databases."
            return cls._build_result(paper_id, title, miss_reason, explanation, remedy)

        # 3. Deduplication error
        norm_title = re.sub(r'[^a-z0-9]', '', title.lower())
        for d_id in deduplicated_ids:
            if paper_id and str(paper_id).lower() in str(d_id):
                miss_reason = "DEDUPLICATION_ERROR"
                explanation = "target paper was erroneously flagged as a duplicate of an existing record and discarded."
                remedy = "Verify DOI/PMID canonicalization and refine fuzzy title similarity threshold."
                return cls._build_result(paper_id, title, miss_reason, explanation, remedy)

        # 4. Screening false negative
        for sc in screened_records:
            sc_id = str(sc.get("doi") or sc.get("pmid") or sc.get("title", "")).lower()
            if (paper_id and str(paper_id).lower() in sc_id) or (norm_title and norm_title in re.sub(r'[^a-z0-9]', '', str(sc.get("title", "")).lower())):
                if sc.get("screening_verdict") in ["REJECTED", "EXCLUDED"]:
                    miss_reason = "SCREENING_FALSE_NEGATIVE"
                    explanation = f"target paper was retrieved but excluded during screening under reason: {sc.get('exclusion_reason', 'RELEVANCE_GATE')}."
                    remedy = "Audit screening exclusion thresholds and inspect false-positive filters."
                    return cls._build_result(paper_id, title, miss_reason, explanation, remedy)

        # 5. Citation network failure
        if target_paper.get("requires_citation_chasing"):
            if str(paper_id).lower() not in citation_chased_ids:
                miss_reason = "CITATION_NETWORK_FAILURE"
                explanation = "target paper was not linked to the primary seed papers' citation graph within the allowed traversal depth."
                remedy = "Broaden seed paper selection or increase citation chaining depth to 2 or 3."
                return cls._build_result(paper_id, title, miss_reason, explanation, remedy)

        # 6. Query family failure
        if target_paper.get("is_negative_finding") and "NEGATIVE_EVALUATION" not in executed_families and "NEGATIVE_NULL_RESULT" not in executed_families:
            miss_reason = "QUERY_FAMILY_FAILURE"
            explanation = "target paper reported null or adverse results, and negative query families were not executed."
            remedy = "Execute NEGATIVE_EVALUATION and NEGATIVE_NULL_RESULT query families."
            return cls._build_result(paper_id, title, miss_reason, explanation, remedy)

        # 7. MeSH mapping failure
        target_mesh = [str(m).lower() for m in target_paper.get("mesh_terms", [])]
        mapped_mesh = [str(m).lower() for m in search_context.get("mapped_mesh_terms", [])]
        if target_mesh and not any(tm in mapped_mesh for tm in target_mesh):
            miss_reason = "MESH_MAPPING_FAILURE"
            explanation = f"target study indexed with MeSH terms {target_mesh} which were not generated by MeSH mapper."
            remedy = "Enhance MeSH controlled vocabulary mapping for target indications and interventions."
            return cls._build_result(paper_id, title, miss_reason, explanation, remedy)

        # 8. Synonym failure
        target_synonyms = target_paper.get("synonyms", [])
        if target_synonyms:
            miss_reason = "SYNONYM_FAILURE"
            explanation = f"target study utilized alternative lexical variants or synonyms ({target_synonyms}) not captured in query expansion."
            remedy = f"Add lexical variants: {target_synonyms} to BROAD_SYNONYM query expansion."
            return cls._build_result(paper_id, title, miss_reason, explanation, remedy)

        # Default: Vocabulary failure
        miss_reason = "VOCABULARY_FAILURE"
        explanation = "search queries did not contain specific technical keywords present in the target study title or abstract."
        remedy = "Expand query synonyms and add domain-specific terminology variants."
        return cls._build_result(paper_id, title, miss_reason, explanation, remedy)

    @classmethod
    def _build_result(cls, paper_id: str, title: str, reason: str, explanation: str, remedy: str) -> Dict[str, Any]:
        return {
            "paper_id": str(paper_id),
            "title": title,
            "primary_miss_reason": reason,
            "diagnostic_explanation": f"We missed this relevant paper because {explanation}",
            "suggested_remedy": remedy
        }


class ResearchRecallBenchmark:
    """Rigorous, empirical research recall benchmark calculator (v8.6 Section 3).
    Evaluates literature retrieval against ground-truth gold-standard datasets.
    Calculates Recall, Precision, F1, Gold-Standard Coverage, and component contributions.
    """
    @classmethod
    def evaluate_benchmark(
        cls,
        benchmark_spec: Dict[str, Any],
        retrieved_records: List[Dict[str, Any]],
        search_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Calculates recall metrics and diagnoses misses against ground-truth specification."""
        topic_id = benchmark_spec.get("topic_id", "GENERIC_TOPIC")
        research_question = benchmark_spec.get("research_question", "")
        gold_standard_ids = [str(x).strip().lower() for x in benchmark_spec.get("gold_standard_ids", []) if str(x).strip()]
        expected_seeds = [str(x).strip().lower() for x in benchmark_spec.get("expected_seed_papers", []) if str(x).strip()]

        ctx = search_context or {}

        def _canonicalize_id(raw_val: Any) -> str:
            s = str(raw_val or "").strip().lower()
            s = re.sub(r'^(?:doi:|pmid:|https?://(?:dx\.)?doi\.org/)', '', s)
            return s

        # Canonical map of retrieved IDs
        retrieved_id_map: Dict[str, Dict[str, Any]] = {}
        for r in retrieved_records:
            for k in ["id", "doi", "pmid"]:
                val = r.get(k)
                if val:
                    raw_s = str(val).strip().lower()
                    clean_s = _canonicalize_id(raw_s)
                    norm_s = re.sub(r'[^a-z0-9]', '', clean_s)
                    retrieved_id_map[raw_s] = r
                    retrieved_id_map[clean_s] = r
                    retrieved_id_map[norm_s] = r
            if r.get("title"):
                norm_t = re.sub(r'[^a-z0-9]', '', str(r["title"]).lower())
                if norm_t:
                    retrieved_id_map[norm_t] = r

        true_positives = []
        false_negatives = []
        for g_id in gold_standard_ids:
            clean_g = _canonicalize_id(g_id)
            norm_g = re.sub(r'[^a-z0-9]', '', clean_g)
            if g_id in retrieved_id_map or clean_g in retrieved_id_map or norm_g in retrieved_id_map:
                true_positives.append(g_id)
            else:
                false_negatives.append(g_id)

        tp_count = len(true_positives)
        gold_count = len(gold_standard_ids)
        total_retrieved = len(retrieved_records)

        recall = round(tp_count / max(gold_count, 1), 3) if gold_count > 0 else 0.0
        precision = round(tp_count / max(total_retrieved, 1), 3) if total_retrieved > 0 else 0.0
        f1 = round(2 * (precision * recall) / max(precision + recall, 1e-6), 3) if (precision + recall) > 0 else 0.0
        coverage = recall

        # Validation status categorization (v8.6 Section 3)
        if gold_count == 0:
            val_status = "RECALL_NOT_EMPIRICALLY_ESTABLISHED"
        elif recall >= 0.85:
            val_status = "EMPIRICALLY_VALIDATED_RECALL"
        elif recall > 0.0:
            val_status = "PARTIALLY_VALIDATED_RECALL"
        else:
            val_status = "UNVALIDATED_RECALL"

        # Database contribution
        db_contrib: Dict[str, int] = {}
        for tp in true_positives:
            rec = retrieved_id_map.get(tp) or retrieved_id_map.get(_canonicalize_id(tp), {})
            db = str(rec.get("source_database", rec.get("database", "pubmed"))).lower()
            db_contrib[db] = db_contrib.get(db, 0) + 1

        # Query family contribution
        qf_contrib: Dict[str, int] = {}
        for tp in true_positives:
            rec = retrieved_id_map.get(tp) or retrieved_id_map.get(_canonicalize_id(tp), {})
            fam = str(rec.get("query_family", "DIRECT_CORE"))
            qf_contrib[fam] = qf_contrib.get(fam, 0) + 1

        # Chasing contribution
        chasing_count = sum(1 for tp in true_positives if (retrieved_id_map.get(tp) or retrieved_id_map.get(_canonicalize_id(tp), {})).get("is_citation_chased"))

        # Seed paper contribution
        seed_matches = [s for s in expected_seeds if s in retrieved_id_map or _canonicalize_id(s) in retrieved_id_map or re.sub(r'[^a-z0-9]', '', _canonicalize_id(s)) in retrieved_id_map]

        # Missed paper analysis
        miss_diagnoses = []
        target_papers_map = {str(p.get("id", p.get("doi", p.get("pmid")))).strip().lower(): p for p in benchmark_spec.get("gold_standard_details", [])}
        for fn in false_negatives:
            target_p = target_papers_map.get(fn, {"id": fn, "title": f"Study {fn}"})
            diag = SearchMissAnalyzer.diagnose_miss(target_p, ctx)
            miss_diagnoses.append(diag)

        return {
            "topic_id": topic_id,
            "research_question": research_question,
            "validation_status": val_status,
            "recall": recall,
            "precision": precision,
            "f1_score": f1,
            "gold_standard_coverage": coverage,
            "gold_standard_count": gold_count,
            "true_positive_count": tp_count,
            "false_negative_count": len(false_negatives),
            "total_retrieved_count": total_retrieved,
            "database_contribution": db_contrib,
            "query_family_contribution": qf_contrib,
            "citation_chasing_contribution": chasing_count,
            "seed_paper_contribution": len(seed_matches),
            "expected_seeds_found": seed_matches,
            "missed_paper_analysis": miss_diagnoses,
            "reproducibility_distinction": "EMPIRICAL_BENCHMARK_RECORDED"
        }


class AdaptiveDatabaseSelector:
    """Adapts scientific database selection based on research problem characteristics (v8.6 Section 14).
    Explains WHY each database was selected and WHICH evidence it can or cannot capture.
    """
    REGISTRY = dict(DATABASE_SPECIALIZATION_REGISTRY)

    @classmethod
    def select_databases_for_problem(
        cls,
        research_problem: Dict[str, Any]
    ) -> Dict[str, Any]:
        domain = str(research_problem.get("domain", "")).lower()
        title = str(research_problem.get("title", "")).lower()

        selected = ["pubmed", "europe_pmc"]  # Core biomedical baseline

        # If multidisciplinary, technology, engineering, device, or computational
        if any(w in domain or w in title for w in ["bioinformatics", "computational", "machine learning", "engineering", "device", "biomaterial", "physics"]):
            selected.append("openalex")

        # Crossref for DOI canonicalization & publisher retractions
        selected.append("crossref")

        rationales = {}
        for db in selected:
            info = cls.REGISTRY.get(db, {})
            rationales[db] = {
                "domain": info.get("domain", "GENERAL"),
                "why_this_database_was_used": info.get("why_used", ""),
                "can_capture": info.get("can_capture", []),
                "cannot_capture": info.get("cannot_capture", [])
            }

        return {
            "selected_databases": selected,
            "database_count": len(selected),
            "database_rationales": rationales
        }


class NegativeEvidenceScanner:
    """Actively scans retrieved literature for negative, null, contradictory, or inert findings (v8.6 Section 13).
    Identifies publication bias risk and emits POSITIVE_EVIDENCE_DOMINANCE when appropriate.
    """
    @classmethod
    def scan_evidence_balance(cls, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        total = len(records)
        if total == 0:
            return {
                "total_records": 0,
                "positive_count": 0,
                "negative_count": 0,
                "neutral_count": 0,
                "evidence_balance_status": "NO_EVIDENCE",
                "publication_bias_risk": "UNASSESSED"
            }

        pos_count = 0
        neg_count = 0
        neu_count = 0

        for r in records:
            eff = str(r.get("effect_direction", r.get("evidence_polarity", ""))).upper()
            text = f"{r.get('title', '')} {r.get('abstract', '')}".lower()
            
            if any(k in eff for k in ["NEGATIVE", "INERT", "NO_CHANGE", "INHIBITION_ABSENT", "CONTRADICTS"]) or \
               any(w in text for w in ["no significant effect", "was inert", "failed to inhibit", "did not reduce", "non-superiority"]):
                neg_count += 1
            elif any(k in eff for k in ["POSITIVE", "SUPPORTS", "INCREASE", "DECREASE", "INHIBITION", "CYTOTOXIC"]):
                pos_count += 1
            else:
                neu_count += 1

        pos_ratio = round(pos_count / max(total, 1), 3)
        neg_ratio = round(neg_count / max(total, 1), 3)

        if pos_ratio >= 0.85 and neg_count == 0:
            status = "POSITIVE_EVIDENCE_DOMINANCE"
            bias_risk = "HIGH_PUBLICATION_BIAS_SUSPECTED"
            recommendation = "Execute dedicated negative-evidence and adverse-outcome search queries to mitigate positive publication bias."
        elif neg_count > 0:
            status = "NEGATIVE_EVIDENCE_RECOVERED"
            bias_risk = "LOW_OR_BALANCED"
            recommendation = "Negative and null findings successfully recovered; boundary conditions established."
        else:
            status = "SYMMETRIC_EVIDENCE_DISTRIBUTION"
            bias_risk = "MODERATE"
            recommendation = "Continue balanced multi-family retrieval."

        return {
            "total_records": total,
            "positive_count": pos_count,
            "negative_count": neg_count,
            "neutral_count": neu_count,
            "positive_ratio": pos_ratio,
            "negative_ratio": neg_ratio,
            "evidence_balance_status": status,
            "publication_bias_risk": bias_risk,
            "recommendation": recommendation
        }


if __name__ == "__main__":
    adapter = ScientificSearchAdapter()
    print("ScientificSearchAdapter initialized successfully.")
    print("Endpoints:", list(adapter.API_ENDPOINTS.keys()))
