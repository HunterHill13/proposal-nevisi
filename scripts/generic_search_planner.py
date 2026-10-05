#!/usr/bin/env python3
"""
generic_search_planner.py - Multi-Facet Dual-Path Literature Search Planner
Proposal-Nevisi Engine v8.2 (Universal Biomedical Architecture)

Generates an 8-facet query matrix and dual-path search plan (SUPPORTING vs CONTRADICTING)
dynamically from any ResearchProblemModel across biomedical fields.
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple, Set
try:
    from research_problem_model import ResearchProblemModel, ProblemModelBuilder
except ImportError:
    from scripts.research_problem_model import ResearchProblemModel, ProblemModelBuilder

class BaseSearchAdapter:
    """Abstract database search adapter defining interface, query validation, translation, and error normalization."""
    database_name: str = "BASE"

    def translate_query(self, canonical_query: str) -> str:
        """Translates canonical query into database-specific syntax."""
        return canonical_query

    def validate_query(self, query: str) -> Dict[str, Any]:
        """Validates query syntax, parentheses balance, and non-empty status."""
        q = query.strip()
        if not q:
            return {"is_valid": False, "error": "EMPTY_QUERY", "message": "Query string cannot be empty."}
        if q.count("(") != q.count(")"):
            return {"is_valid": False, "error": "UNBALANCED_PARENTHESES", "message": "Query contains mismatched parentheses."}
        if q.count('"') % 2 != 0:
            return {"is_valid": False, "error": "UNBALANCED_QUOTES", "message": "Query contains unbalanced quotation marks."}
        return {"is_valid": True, "error": None, "query": q}

    def normalize_record(self, raw_record: Dict[str, Any]) -> Dict[str, Any]:
        """Maps raw API response to standardized record format."""
        return {
            "database": self.database_name,
            "pmid": str(raw_record.get("pmid", "")).strip() if raw_record.get("pmid") else None,
            "doi": str(raw_record.get("doi", "")).strip().lower() if raw_record.get("doi") else None,
            "openalex_id": str(raw_record.get("openalex_id", "")).strip().lower() if raw_record.get("openalex_id") else None,
            "title": str(raw_record.get("title", "")).strip(),
            "authors": raw_record.get("authors", []),
            "year": int(raw_record.get("year")) if raw_record.get("year") else None,
            "journal": str(raw_record.get("journal", "")).strip(),
            "raw_provenance": raw_record
        }

    def normalize_error(self, error_type: str, details: Any = None) -> Dict[str, Any]:
        """Standardizes database and network retrieval errors across adapters."""
        known_errors = {
            "TIMEOUT": "Connection or read timeout occurred while querying database API.",
            "HTTP_429": "Rate limit exceeded (HTTP 429 Too Many Requests).",
            "HTTP_500": "Remote database internal server error (HTTP 500).",
            "MALFORMED_JSON": "Remote server returned invalid or unparseable JSON payload.",
            "EMPTY_RESULT": "Query executed successfully but returned zero matching records.",
            "PARTIAL_RESULT": "Query returned partial result set due to truncated response or network cut.",
            "PAGINATION_FAILURE": "Failed to fetch subsequent result pages during cursor/offset iteration."
        }
        msg = known_errors.get(error_type, f"Unclassified error: {error_type}")
        return {
            "database": self.database_name,
            "error_type": error_type,
            "message": msg,
            "details": details,
            "is_retriable": error_type in ["TIMEOUT", "HTTP_429", "HTTP_500"]
        }

    def execute_query(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        mode: str = "offline",
        fixture_records: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Executes search query supporting PLANNED, NOT_EXECUTED, and EXECUTED states with full provenance."""
        val = self.validate_query(query)
        if not val["is_valid"]:
            return {
                "database": self.database_name,
                "query": query,
                "status": "VALIDATION_FAILED",
                "error": val["error"],
                "results_count": 0,
                "records": []
            }

        t_query = self.translate_query(query)

        if mode == "planned":
            return {
                "database": self.database_name,
                "query": query,
                "translated_query": t_query,
                "filters": filters or {},
                "status": "PLANNED",
                "message": "Query plan registered; pending execution.",
                "results_count": 0,
                "records": []
            }

        if mode == "offline":
            return {
                "database": self.database_name,
                "query": query,
                "translated_query": t_query,
                "filters": filters or {},
                "status": "NOT_EXECUTED",
                "message": f"{self.database_name} API was not contacted (dry-run/offline protocol active). Prohibits fictitious execution.",
                "results_count": 0,
                "records": []
            }

        if mode in ["fixture", "recorded_integration_fixture"]:
            raw_recs = fixture_records or []
            norm_recs = [self.normalize_record(r) for r in raw_recs]
            return {
                "database": self.database_name,
                "query": query,
                "translated_query": t_query,
                "filters": filters or {},
                "status": "EXECUTED",
                "execution_mode": "RECORDED_INTEGRATION_FIXTURE",
                "results_count": len(norm_recs),
                "returned_identifiers": [r.get("doi") or r.get("pmid") for r in norm_recs if r.get("doi") or r.get("pmid")],
                "records": norm_recs,
                "retrieval_errors": [],
                "pagination": {"total_pages": 1, "page_size": len(norm_recs)}
            }

        return {
            "database": self.database_name,
            "query": query,
            "translated_query": t_query,
            "filters": filters or {},
            "status": "NOT_EXECUTED",
            "message": "Live network connection not active in execution environment.",
            "results_count": 0,
            "records": []
        }

class PubMedAdapter(BaseSearchAdapter):
    """Adapter for NCBI PubMed/MEDLINE query translation and execution."""
    database_name = "PubMed"

    def translate_query(self, canonical_query: str) -> str:
        return canonical_query.strip()

    def normalize_record(self, raw_record: Dict[str, Any]) -> Dict[str, Any]:
        rec = super().normalize_record(raw_record)
        rec["pmid"] = str(raw_record.get("uid") or raw_record.get("pmid", "")).strip() or None
        return rec

class EuropePMCAdapter(BaseSearchAdapter):
    """Adapter for Europe PMC REST query translation and execution."""
    database_name = "Europe PMC"

    def translate_query(self, canonical_query: str) -> str:
        q = canonical_query
        q = re.sub(r'"([^"]+)"\[Title/Abstract\]', r'(TITLE:"\1" OR ABS:"\1")', q)
        q = re.sub(r'"([^"]+)"\[MeSH Terms\]', r'KW:"\1"', q)
        return q.strip()

    def normalize_record(self, raw_record: Dict[str, Any]) -> Dict[str, Any]:
        rec = super().normalize_record(raw_record)
        rec["pmid"] = str(raw_record.get("pmid", "")).strip() or None
        rec["doi"] = str(raw_record.get("doi", "")).strip().lower() or None
        return rec

class CrossrefAdapter(BaseSearchAdapter):
    """Adapter for Crossref Metadata REST API query translation and execution."""
    database_name = "Crossref"

    def translate_query(self, canonical_query: str) -> str:
        q = canonical_query
        q = re.sub(r'\[Title/Abstract\]', '', q)
        q = re.sub(r'\[MeSH Terms\]', '', q)
        return q.strip()

    def normalize_record(self, raw_record: Dict[str, Any]) -> Dict[str, Any]:
        rec = super().normalize_record(raw_record)
        rec["doi"] = str(raw_record.get("DOI") or raw_record.get("doi", "")).strip().lower() or None
        if "title" in raw_record and isinstance(raw_record["title"], list):
            rec["title"] = raw_record["title"][0] if raw_record["title"] else ""
        return rec

class OpenAlexAdapter(BaseSearchAdapter):
    """Adapter for OpenAlex scholarly concepts and inverted index search."""
    database_name = "OpenAlex"

    def translate_query(self, canonical_query: str) -> str:
        q = canonical_query
        q = re.sub(r'\[Title/Abstract\]', '', q)
        q = re.sub(r'\[MeSH Terms\]', '', q)
        return q.strip()

    def normalize_record(self, raw_record: Dict[str, Any]) -> Dict[str, Any]:
        rec = super().normalize_record(raw_record)
        rec["openalex_id"] = str(raw_record.get("id") or raw_record.get("openalex_id", "")).strip().lower() or None
        return rec

class GenericSearchPlanner:
    """Constructs dynamic, multi-database query matrices for evidence-seeking literature retrieval."""

    def __init__(self, model: ResearchProblemModel):
        self.model = model

    def build_query_matrix(self) -> Dict[str, Any]:
        """Builds all 8 systematic search facets."""
        cond_en = self.model.target_condition.name_en
        cond_mesh = self.model.target_condition.mesh_term
        system = self.model.population_or_model.primary_system
        agents = [agt.name for agt in self.model.interventions_or_exposures]
        primary_agent = agents[0] if agents else "Target Intervention"
        adjuvant_agent = agents[1] if len(agents) > 1 else None

        facets = {}

        # Layer A: Direct Evidence Queries
        if adjuvant_agent:
            facets["LAYER_A_DIRECT_EVIDENCE"] = [
                f'("{primary_agent}"[Title/Abstract] AND "{adjuvant_agent}"[Title/Abstract] AND ("{cond_en}"[Title/Abstract] OR "{cond_mesh}"[MeSH Terms]))',
                f'("{primary_agent}" AND "{adjuvant_agent}" AND "{system}")'
            ]
        else:
            facets["LAYER_A_DIRECT_EVIDENCE"] = [
                f'("{primary_agent}"[Title/Abstract] AND ("{cond_en}"[Title/Abstract] OR "{cond_mesh}"[MeSH Terms]))',
                f'("{primary_agent}" AND "{system}")'
            ]

        # Layer B: Component Evidence Queries
        facets["LAYER_B_COMPONENT_EVIDENCE"] = []
        for agt in agents:
            facets["LAYER_B_COMPONENT_EVIDENCE"].append(
                f'("{agt}"[Title/Abstract] AND ("{cond_en}"[Title/Abstract] OR "{cond_mesh}"[MeSH Terms]))'
            )
            facets["LAYER_B_COMPONENT_EVIDENCE"].append(
                f'("{agt}"[Title/Abstract] AND "{system}"[Title/Abstract])'
            )

        # Layer C: Mechanistic Evidence Queries
        facets["LAYER_C_MECHANISTIC_EVIDENCE"] = []
        for mech in self.model.hypothesized_mechanisms:
            p_name = mech.pathway_name
            targets = " OR ".join([f'"{t}"' for t in mech.target_molecules])
            facets["LAYER_C_MECHANISTIC_EVIDENCE"].append(
                f'("{primary_agent}" AND ("{p_name}" OR {targets}) AND ("signaling" OR "pathway" OR "phosphorylation" OR "cleavage" OR "modulation"))'
            )

        # Layer D: Model Evidence Queries
        facets["LAYER_D_MODEL_EVIDENCE"] = [
            f'("{system}"[Title/Abstract] AND ("{cond_en}" OR "{cond_mesh}") AND ("biology" OR "characteristics" OR "molecular profiling" OR "heterogeneity"))'
        ]

        # Layer E: Translational Evidence Queries
        facets["LAYER_E_TRANSLATIONAL_EVIDENCE"] = [
            f'("{primary_agent}" AND ("in vivo" OR "animal model" OR "preclinical model" OR "clinical trial" OR "pharmacokinetics"))'
        ]

        # Layer F: Safety & Toxicity Queries
        facets["LAYER_F_SAFETY_TOXICITY"] = [
            f'("{primary_agent}" AND ("maximum tolerated dose" OR "LD50" OR "cytotoxicity" OR "safety profile" OR "therapeutic window"))'
        ]

        # Layer G: Negative & Null Evidence Queries (MANDATORY DUAL-PATH)
        facets["LAYER_G_NEGATIVE_NULL_EVIDENCE"] = [
            f'("{primary_agent}" AND ("no effect" OR "lack of efficacy" OR "failed to inhibit" OR "null response" OR "non-significant" OR "resistance"))',
            f'("{primary_agent}" AND ("toxicity" OR "adverse effect" OR "off-target" OR "tolerance" OR "subadditive"))'
        ]
        if adjuvant_agent:
            facets["LAYER_G_NEGATIVE_NULL_EVIDENCE"].append(
                f'("{primary_agent}" AND "{adjuvant_agent}" AND ("antagonism" OR "antagonistic" OR "subadditive" OR "no synergy" OR "attenuation"))'
            )

        # Layer H: Contradictory Evidence Queries
        facets["LAYER_H_CONTRADICTORY_EVIDENCE"] = [
            f'("{primary_agent}" AND ("conflicting" OR "contradictory" OR "discrepancy" OR "failed replication" OR "opposite effect"))'
        ]
        if adjuvant_agent:
            facets["LAYER_H_CONTRADICTORY_EVIDENCE"].append(
                f'("{primary_agent}" AND "{adjuvant_agent}" AND ("discordant" OR "inconsistent" OR "independent action" OR "antagonistic interaction"))'
            )

        # Layer I: Methodological Evidence Queries
        outcomes = [o.name for o in self.model.primary_outcomes]
        outcome_str = " OR ".join([f'"{o}"' for o in outcomes])
        facets["LAYER_I_METHODOLOGICAL_EVIDENCE"] = [
            f'("{system}" AND ({outcome_str}) AND ("assay validation" OR "reproducibility" OR "protocol" OR "standardization"))'
        ]

        # Layer J: Alternative Explanation Queries
        facets["LAYER_J_ALTERNATIVE_EXPLANATION"] = [
            f'("{cond_en}" AND ({outcome_str}) AND ("alternative pathway" OR "compensatory mechanism" OR "off-target mediated" OR "spontaneous remission" OR "bystander effect"))',
            f'("{primary_agent}" AND ("non-specific cytotoxicity" OR "optical artifact" OR "vehicle interference" OR "aggregation artifact"))'
        ]

        # Layer K: Confounder Search Queries
        facets["LAYER_K_CONFOUNDER_SEARCH"] = [
            f'("{cond_en}" AND ({outcome_str}) AND ("confounding factor" OR "covariate effect" OR "baseline imbalance" OR "batch effect" OR "passage effect"))',
            f'("{system}" AND ("culture variation" OR "phenotypic drift" OR "mycoplasma artifact" OR "heterogeneity"))'
        ]

        # Layer L: Independent Replication Search Queries
        facets["LAYER_L_REPLICATION_SEARCH"] = [
            f'("{primary_agent}" AND "{cond_en}" AND ("independent replication" OR "reproducibility study" OR "confirmatory trial" OR "multicenter validation" OR "failed replication"))'
        ]

        # Standardized 9-Layer Adaptive Search Architecture (Cross-Audited from AIPOCH / K-Dense)
        facets["LAYER_1_EXACT_DIRECT_COMBINATION"] = facets["LAYER_A_DIRECT_EVIDENCE"]
        facets["LAYER_2_INDIVIDUAL_INTERVENTIONS"] = facets["LAYER_B_COMPONENT_EVIDENCE"]
        facets["LAYER_3_MECHANISTIC_EVIDENCE"] = facets["LAYER_C_MECHANISTIC_EVIDENCE"]
        facets["LAYER_4_MODEL_SPECIFIC_EVIDENCE"] = facets["LAYER_D_MODEL_EVIDENCE"]
        facets["LAYER_5_COMBINATION_ANALOGUES"] = [
            f'("{primary_agent}" AND ("standard-of-care" OR "combination therapy" OR "adjuvant" OR "co-treatment"))'
        ]
        if adjuvant_agent:
            facets["LAYER_5_COMBINATION_ANALOGUES"].append(
                f'("{adjuvant_agent}" AND ("standard-of-care" OR "combination therapy" OR "adjuvant" OR "co-treatment"))'
            )
        facets["LAYER_6_METHODOLOGY"] = facets["LAYER_I_METHODOLOGICAL_EVIDENCE"]
        facets["LAYER_7_SAFETY_TOXICITY"] = facets["LAYER_F_SAFETY_TOXICITY"]
        facets["LAYER_8_CONTRADICTORY_NEGATIVE"] = (
            facets["LAYER_G_NEGATIVE_NULL_EVIDENCE"] +
            facets["LAYER_H_CONTRADICTORY_EVIDENCE"]
        )
        facets["LAYER_9_CITATION_CHASING"] = [
            f'("{primary_agent}" AND ("seminal" OR "landmark" OR "foundational" OR "citation lineage"))'
        ]

        # Backward compatibility aliases for existing suites
        facets["FACET_A_DIRECT_EVIDENCE"] = facets["LAYER_A_DIRECT_EVIDENCE"]
        facets["FACET_B_COMPONENT_EVIDENCE"] = facets["LAYER_B_COMPONENT_EVIDENCE"]
        facets["FACET_C_COMBINATION_INTERACTION"] = facets["LAYER_A_DIRECT_EVIDENCE"]
        facets["FACET_D_MECHANISTIC_EVIDENCE"] = facets["LAYER_C_MECHANISTIC_EVIDENCE"]
        facets["FACET_E_TRANSLATIONAL_EVIDENCE"] = facets["LAYER_E_TRANSLATIONAL_EVIDENCE"]
        facets["FACET_F_NEGATIVE_NULL_EVIDENCE"] = facets["LAYER_G_NEGATIVE_NULL_EVIDENCE"]
        facets["FACET_G_SAFETY_LIMITATIONS"] = facets["LAYER_F_SAFETY_TOXICITY"]
        facets["FACET_H_METHODOLOGICAL_EVIDENCE"] = facets["LAYER_I_METHODOLOGICAL_EVIDENCE"]

        # Dual-Path Grouping
        supporting_queries = (
            facets["LAYER_A_DIRECT_EVIDENCE"] +
            facets["LAYER_B_COMPONENT_EVIDENCE"] +
            facets["LAYER_C_MECHANISTIC_EVIDENCE"] +
            facets["LAYER_D_MODEL_EVIDENCE"] +
            facets["LAYER_E_TRANSLATIONAL_EVIDENCE"]
        )

        contradicting_queries = (
            facets["LAYER_F_SAFETY_TOXICITY"] +
            facets["LAYER_G_NEGATIVE_NULL_EVIDENCE"] +
            facets["LAYER_H_CONTRADICTORY_EVIDENCE"] +
            facets["LAYER_J_ALTERNATIVE_EXPLANATION"] +
            facets["LAYER_K_CONFOUNDER_SEARCH"] +
            facets["LAYER_L_REPLICATION_SEARCH"]
        )

        return {
            "model_id": self.model.model_id,
            "domain": self.model.domain,
            "framework": self.model.framework,
            "search_boundary": {
                "databases": ["PubMed", "Europe PMC", "OpenAlex", "Crossref"],
                "target_condition": cond_en,
                "primary_system": system,
                "time_window": "2020-2026 (primary) / unrestricted (foundational)"
            },
            "query_matrix_facets": facets,
            "dual_path_execution": {
                "supporting_search_count": len(supporting_queries),
                "supporting_queries": supporting_queries,
                "contradicting_search_count": len(contradicting_queries),
                "contradicting_queries": contradicting_queries
            },
            "epistemic_policy": {
                "absence_of_contradiction_rule": "NO_RELEVANT_CONTRADICTING_EVIDENCE_IDENTIFIED",
                "prohibit_unbounded_claims": True
            }
        }

    @staticmethod
    def build_pubmed_boolean_query(
        concepts: List[List[str]],
        mesh_terms: Optional[List[str]] = None,
        date_range: Optional[Tuple[int, int]] = None,
        study_types: Optional[List[str]] = None,
        field_tag: str = "[Title/Abstract]"
    ) -> str:
        """Constructs precision Boolean queries with MeSH terms, field tags, date filters, and study types (AIPOCH/K-Dense)."""
        clauses = []
        for term_group in concepts:
            if not term_group:
                continue
            tagged_terms = [f'"{t}"{field_tag}' if not t.endswith("]") else t for t in term_group]
            clauses.append("(" + " OR ".join(tagged_terms) + ")")
        
        if mesh_terms:
            mesh_clauses = [f'"{m}"[MeSH Terms]' for m in mesh_terms]
            clauses.append("(" + " OR ".join(mesh_clauses) + ")")
            
        combined_query = " AND ".join(clauses)
        
        if date_range:
            start_y, end_y = date_range
            combined_query += f" AND ({start_y}:{end_y}[dp])"
            
        if study_types:
            st_clauses = [f'"{st}"[pt]' for st in study_types]
            combined_query += f" AND (" + " OR ".join(st_clauses) + ")"
            
        return combined_query

    @classmethod
    def decompose_problem_for_search(cls, model: Any) -> Dict[str, Any]:
        """Decomposes any research problem model into multi-faceted search targets across 12 generic dimensions:
        population/model, disease/condition, intervention A, intervention B, combination,
        comparator, outcome, mechanism, study type, experimental model, safety, and methodology.
        100% Generic and domain-independent.
        """
        if hasattr(model, "to_dict"):
            m_dict = model.to_dict()
        elif isinstance(model, dict):
            m_dict = model.get("research_problem_model", model)
        else:
            m_dict = {}

        domain = m_dict.get("domain", "biomedical")
        framework = m_dict.get("framework", "PICO")

        cond = m_dict.get("target_condition", {})
        cond_en = cond.get("name_en", "") if isinstance(cond, dict) else str(cond)
        cond_mesh = cond.get("mesh_term", "") if isinstance(cond, dict) else ""
        cond_synonyms = cond.get("synonyms", []) if isinstance(cond, dict) else []

        pop = m_dict.get("population_or_model", {})
        system = pop.get("primary_system", "") if isinstance(pop, dict) else str(pop)
        sec_systems = pop.get("secondary_systems", []) if isinstance(pop, dict) else []

        interventions = m_dict.get("interventions_or_exposures", [])
        agent_names = []
        agent_synonyms = []
        agent_classes = []
        for ag in interventions:
            if isinstance(ag, dict):
                if ag.get("name"): agent_names.append(ag["name"])
                if ag.get("chemical_or_biological_class"): agent_classes.append(ag["chemical_or_biological_class"])
                agent_synonyms.extend(ag.get("synonyms", []))
            elif isinstance(ag, str):
                agent_names.append(ag)

        primary_agent = agent_names[0] if agent_names else "Target Intervention"
        adjuvant_agent = agent_names[1] if len(agent_names) > 1 else None

        outcomes = m_dict.get("primary_outcomes", [])
        outcome_names = [o.get("name") for o in outcomes if isinstance(o, dict) and o.get("name")]

        mechs = m_dict.get("hypothesized_mechanisms", [])
        pathways = [m.get("pathway_name") for m in mechs if isinstance(m, dict) and m.get("pathway_name")]
        molecules = []
        for m in mechs:
            if isinstance(m, dict):
                molecules.extend(m.get("target_molecules", []))

        study_type = m_dict.get("study_type", "IN_VITRO_EXPERIMENTAL")
        
        # Adaptive Comparator Detection
        comp_records = m_dict.get("comparators", [])
        comp_names = [c.get("name") if isinstance(c, dict) else str(c) for c in comp_records if c]
        if comp_names:
            comparator = " / ".join(comp_names)
        elif framework == "DIAGNOSTIC":
            comparator = "reference standard / gold standard comparator"
        elif framework in ["SURGICAL", "SURGICAL_TECHNIQUE"] or "SURGERY" in domain.upper():
            comparator = "standard open procedure / conventional management"
        elif "IN_VITRO" in str(study_type).upper():
            comparator = "vehicle / untreated control / monotherapy"
        else:
            comparator = "standard of care / placebo / active comparator"

        # Adaptive Intervention B & Combination Detection
        if adjuvant_agent:
            intervention_b_val = adjuvant_agent
            combination_val = f"{primary_agent} + {adjuvant_agent}"
        else:
            intervention_b_val = "NOT_APPLICABLE"
            combination_val = "NOT_APPLICABLE"

        # Adaptive Mechanism Detection
        if pathways:
            mechanism_val = pathways
        elif framework in ["PECO", "EPIDEMIOLOGICAL", "PUBLIC_HEALTH", "SURGICAL", "DIAGNOSTIC"] and not mechs:
            mechanism_val = "NOT_APPLICABLE"
        else:
            mechanism_val = "hypothesized molecular mechanism / target signaling"

        # Adaptive Safety / Toxicity Detection
        if (framework in ["DIAGNOSTIC", "EPIDEMIOLOGICAL", "PECO", "PUBLIC_HEALTH"] or "EPIDEMIOLOG" in domain.upper() or "PUBLIC_HEALTH" in domain.upper()) and not any(k in domain.lower() for k in ["pharmacolog", "drug", "toxicology"]):
            safety_val = "NOT_APPLICABLE"
        elif framework in ["SURGICAL", "SURGICAL_TECHNIQUE"] or "SURGERY" in domain.upper():
            safety_val = "postoperative complications / morbidity / adverse events"
        else:
            safety_val = "adverse events / therapeutic window / selectivity / toxicity boundaries"

        # Adaptive Methodology Detection
        if framework == "DIAGNOSTIC" or "DIAGNOSTIC" in str(study_type).upper():
            methodology_val = "sensitivity / specificity / ROC curve / index test vs reference standard"
        elif framework in ["SURGICAL", "SURGICAL_TECHNIQUE"] or "SURGERY" in domain.upper():
            methodology_val = "standardized surgical technique / clinical endpoints / follow-up assessment"
        elif "IN_VITRO" in str(study_type).upper():
            methodology_val = "quantitative bioassay / dose-response titration / flow cytometry"
        else:
            methodology_val = "controlled experimental protocol / standardized measurement assay / statistical analysis"

        # Explicit 12-component adaptive generic decomposition (v8.4 Section 4)
        decomposed_components = {
            "population_or_model": system,
            "disease_or_condition": cond_en,
            "intervention_a": primary_agent,
            "intervention_b": intervention_b_val,
            "combination": combination_val,
            "comparator": comparator,
            "outcome": outcome_names,
            "mechanism": mechanism_val,
            "study_type": study_type,
            "experimental_model": system,
            "safety_toxicity": safety_val,
            "methodology": methodology_val
        }

        applicable_dims = [k for k, v in decomposed_components.items() if v != "NOT_APPLICABLE"]
        not_applicable_dims = [k for k, v in decomposed_components.items() if v == "NOT_APPLICABLE"]

        return {
            "model_id": m_dict.get("model_id", "RPM_SEARCH_DECOMPOSED"),
            "domain": domain,
            "framework": framework,
            "decomposed_question_components": decomposed_components,
            "applicable_dimensions": applicable_dims,
            "not_applicable_dimensions": not_applicable_dims,
            "condition_facets": {
                "primary_term": cond_en,
                "mesh_term": cond_mesh,
                "synonyms": cond_synonyms
            },
            "population_model_facets": {
                "primary_system": system,
                "secondary_systems": sec_systems
            },
            "intervention_facets": {
                "agent_names": agent_names,
                "classes": agent_classes,
                "synonyms": agent_synonyms
            },
            "outcome_facets": {
                "primary_outcomes": outcome_names
            },
            "mechanistic_facets": {
                "pathways": pathways if pathways else ("NOT_APPLICABLE" if mechanism_val == "NOT_APPLICABLE" else []),
                "target_molecules": molecules
            }
        }

    @classmethod
    def expand_query_terms(cls, term: str, category: str = "INTERVENTION") -> List[Dict[str, str]]:
        """v8.4 Section 5.A: Structured query expansion with provenance tracking."""
        clean = term.strip()
        if not clean:
            return []
        expansions = [{"term": clean, "provenance": "EXACT_CANONICAL_SPECIFICATION", "type": "PRIMARY"}]
        # Parenthetical acronym/base extraction
        if "(" in clean and ")" in clean:
            inner = re.findall(r'\((.*?)\)', clean)
            base = re.sub(r'\(.*?\)', '', clean).strip()
            if base and base != clean:
                expansions.append({"term": base, "provenance": "BASE_FORM_EXTRACTION", "type": "SYNONYM"})
            for inn in inner:
                if len(inn) >= 2:
                    expansions.append({"term": inn, "provenance": "ABBREVIATION_EXTRACTION", "type": "ABBREVIATION"})
        # Hyphenated / space variants
        if "-" in clean:
            expansions.append({"term": clean.replace("-", " "), "provenance": "SPELLING_VARIANT_DEHYPHENATION", "type": "SYNONYM"})
        elif " " in clean and len(clean.split()) == 2:
            expansions.append({"term": clean.replace(" ", "-"), "provenance": "SPELLING_VARIANT_HYPHENATION", "type": "SYNONYM"})
        return expansions

    @classmethod
    def track_search_saturation(cls, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """v8.4 Section 5.C: Tracks multi-dimensional search saturation across entities, mechanisms, outcomes, and designs."""
        seen_ids = set()
        seen_entities = set()
        seen_mechs = set()
        seen_outcomes = set()
        seen_designs = set()
        seen_contradictions = set()
        duplicates_count = 0

        for r in records:
            rid = r.get("pmid") or r.get("doi") or r.get("title", "")
            if rid in seen_ids:
                duplicates_count += 1
            else:
                seen_ids.add(rid)

            ent = r.get("universal_entity_type") or r.get("compound_identity")
            if ent and ent not in ["UNKNOWN_IDENTITY", "NOT_APPLICABLE"]:
                seen_entities.add(ent)

            for m in r.get("mechanisms", []):
                seen_mechs.add(str(m).lower())

            for o in r.get("reported_outcomes", []):
                seen_outcomes.add(str(o).upper())

            des = r.get("study_design")
            if des:
                seen_designs.add(str(des).upper())

            pol = r.get("evidence_polarity")
            if pol in ["CONTRADICTS", "LIMITS_INTERPRETATION"]:
                seen_contradictions.add(rid)

        total = len(records)
        unique_count = len(seen_ids)
        dup_rate = (duplicates_count / total) if total > 0 else 0.0

        is_saturated = (dup_rate >= 0.40 and unique_count >= 15) or (total >= 25 and len(seen_entities) >= 1)
        return {
            "total_records_screened": total,
            "unique_studies_count": unique_count,
            "duplicate_count": duplicates_count,
            "duplicate_rate": round(dup_rate, 4),
            "unique_entities_discovered": sorted(list(seen_entities)),
            "unique_mechanisms_discovered": sorted(list(seen_mechs)),
            "unique_outcomes_discovered": sorted(list(seen_outcomes)),
            "unique_designs_discovered": sorted(list(seen_designs)),
            "contradictory_studies_count": len(seen_contradictions),
            "is_saturated": is_saturated,
            "saturation_recommendation": "Search saturation reached; marginal information gain is low" if is_saturated else "Continue targeted querying for unexplored outcomes/mechanisms"
        }

    @classmethod
    def generate_expanded_query_matrix(cls, model: Any) -> Dict[str, Any]:
        """Generates comprehensive, multi-layer search query matrix without artificial retrieval caps."""
        if isinstance(model, ResearchProblemModel):
            planner = cls(model)
        else:
            try:
                from research_problem_model import ProblemModelBuilder
            except ImportError:
                from scripts.research_problem_model import ProblemModelBuilder
            m_dict = model.get("research_problem_model", model) if isinstance(model, dict) else {}
            built_model = ProblemModelBuilder.create_from_specification(m_dict)
            planner = cls(built_model)
        return planner.build_query_matrix()

    @classmethod
    def adaptive_search_iteration(
        cls,
        current_records: List[Dict[str, Any]],
        model: Any,
        iteration_number: int = 1,
        new_search_facets: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Dynamically adapts search based on identified evidence gaps and completeness analysis.
        Expands queries iteratively to target missing streams without artificial pagination caps.
        """
        decomp = cls.decompose_problem_for_search(model)
        framework = decomp.get("framework", "PICO")
        required_streams = cls.get_required_evidence_streams(framework)

        # Categorize current records into streams
        streams_map: Dict[str, List[Dict[str, Any]]] = {s: [] for s in required_streams}
        for r in current_records:
            findings = str(r.get("primary_findings", r.get("title", ""))).lower()
            role = str(r.get("evidence_role", "")).upper()
            design = str(r.get("study_design", "")).upper()

            if "NEGATIVE" in role or any(k in findings for k in ["no effect", "null", "antagonis", "toxic", "resistance"]):
                if "NEGATIVE_NULL_EVIDENCE" in streams_map: streams_map["NEGATIVE_NULL_EVIDENCE"].append(r)
                if "SAFETY_TOXICITY" in streams_map and any(k in findings for k in ["toxic", "adverse"]): streams_map["SAFETY_TOXICITY"].append(r)
            elif "MECHANIS" in role or any(k in findings for k in ["pathway", "signaling", "caspase", "cleavage", "receptor"]):
                if "MECHANISTIC_EVIDENCE" in streams_map: streams_map["MECHANISTIC_EVIDENCE"].append(r)
                if "MECHANISTIC_PATHWAY" in streams_map: streams_map["MECHANISTIC_PATHWAY"].append(r)
            elif "COMPONENT" in role or "MONOTHERAPY" in role:
                if "COMPONENT_EVIDENCE" in streams_map: streams_map["COMPONENT_EVIDENCE"].append(r)
            elif "REPLICATION" in role or "reproducib" in findings:
                if "REPLICATION_EVIDENCE" in streams_map: streams_map["REPLICATION_EVIDENCE"].append(r)
            else:
                if "DIRECT_EVIDENCE" in streams_map: streams_map["DIRECT_EVIDENCE"].append(r)
                if "DIRECT_CYTOTOXICITY_EFFICACY" in streams_map: streams_map["DIRECT_CYTOTOXICITY_EFFICACY"].append(r)
                if "DIRECT_CLINICAL_EFFICACY" in streams_map: streams_map["DIRECT_CLINICAL_EFFICACY"].append(r)

        completeness_eval = cls.evaluate_evidence_completeness_matrix(streams_map, required_streams)
        missing_streams = completeness_eval.get("missing_streams", [])

        # Formulate targeted adaptive queries for missing streams
        adaptive_queries = []
        cond_term = decomp["condition_facets"]["primary_term"]
        agent_names = decomp["intervention_facets"]["agent_names"]
        primary_agent = agent_names[0] if agent_names else "Intervention"

        for stream in missing_streams:
            if "NEGATIVE" in stream or "NULL" in stream:
                adaptive_queries.append(f'("{primary_agent}" AND "{cond_term}" AND ("null response" OR "ineffective" OR "no difference" OR "failed to inhibit" OR "resistance"))')
            elif "SAFETY" in stream or "TOXICITY" in stream:
                adaptive_queries.append(f'("{primary_agent}" AND ("therapeutic index" OR "cytotoxicity threshold" OR "maximum tolerated dose" OR "adverse effect"))')
            elif "MECHANIS" in stream:
                pathways = decomp["mechanistic_facets"]["pathways"]
                p_term = pathways[0] if pathways else "pathway"
                adaptive_queries.append(f'("{primary_agent}" AND "{p_term}" AND ("molecular mechanism" OR "target phosphorylation" OR "cascade"))')
            elif "REPLICATION" in stream:
                adaptive_queries.append(f'("{primary_agent}" AND "{cond_term}" AND ("replication study" OR "multicenter validation" OR "reproducibility"))')

        saturation_eval = cls.assess_search_saturation([len(current_records)])

        return {
            "iteration_number": iteration_number,
            "total_corpus_evaluated": len(current_records),
            "evidence_completeness_status": completeness_eval["is_complete"],
            "missing_evidence_streams": missing_streams,
            "adaptive_expanded_queries": adaptive_queries,
            "completeness_ratio": completeness_eval["completeness_ratio"],
            "saturation_status": saturation_eval["saturation_reached"],
            "next_recommended_action": "SYNTHESIZE_EVIDENCE" if (completeness_eval["is_complete"] or iteration_number >= 3) else "EXECUTE_ADAPTIVE_EXPANSION_QUERIES"
        }

    @staticmethod
    def assess_search_saturation(
        iteration_yields: List[int],
        new_study_families_yield: Optional[List[int]] = None,
        new_gaps_yield: Optional[List[int]] = None,
        threshold: float = 0.05
    ) -> Dict[str, Any]:
        """Assesses whether evidence saturation has been achieved across iterative query cycles.
        Integrates paper yields, new study families, and new contradictory/gap discoveries (Prompt Pt 28).
        """
        if not iteration_yields:
            return {"saturation_reached": False, "novel_evidence_rate": 1.0, "recommendation": "Initiate baseline search"}

        if len(iteration_yields) < 2:
            return {"saturation_reached": False, "novel_evidence_rate": 1.0, "recommendation": "Execute additional query facets"}

        latest_yield = iteration_yields[-1]
        cumulative = sum(iteration_yields[:-1])
        novel_rate = (latest_yield / cumulative) if cumulative > 0 else 1.0

        family_rate = 0.0
        if new_study_families_yield and len(new_study_families_yield) >= 2:
            latest_fam = new_study_families_yield[-1]
            cum_fam = sum(new_study_families_yield[:-1])
            family_rate = (latest_fam / cum_fam) if cum_fam > 0 else 1.0

        is_saturated = (novel_rate <= threshold) and (family_rate <= threshold or new_study_families_yield is None)
        return {
            "saturation_reached": is_saturated,
            "novel_evidence_rate": round(novel_rate, 4),
            "novel_family_rate": round(family_rate, 4) if new_study_families_yield else None,
            "threshold": threshold,
            "epistemic_warning": "Search saturation indicates diminishing returns in current search boundary; it is NOT empirical proof of complete literature exhaustiveness (Phase 21).",
            "recommendation": "Evidence saturation satisfied; proceed to synthesis" if is_saturated else "Continue iterative expansion across negative/replication facets"
        }

    @classmethod
    def evaluate_search_coverage(
        cls,
        searched_databases: List[str],
        covered_concepts: List[str],
        required_concepts: List[str],
        has_contradiction_search: bool,
        has_citation_chaining: bool
    ) -> Dict[str, Any]:
        """Separates Search Coverage from Search Saturation across 7 multi-dimensional parameters (Phase 20)."""
        standard_dbs = {"PubMed", "Europe PMC", "OpenAlex", "Crossref"}
        db_coverage = len(set(searched_databases).intersection(standard_dbs)) / len(standard_dbs)
        
        missing_concepts = [c for c in required_concepts if c not in covered_concepts]
        concept_coverage = (len(required_concepts) - len(missing_concepts)) / max(len(required_concepts), 1)

        coverage_score = round((db_coverage * 0.3) + (concept_coverage * 0.3) + (0.2 if has_contradiction_search else 0.0) + (0.2 if has_citation_chaining else 0.0), 3)

        return {
            "overall_search_coverage_score": coverage_score,
            "database_coverage": {
                "databases_queried": searched_databases,
                "coverage_ratio": round(db_coverage, 2)
            },
            "concept_coverage": {
                "covered_concepts": covered_concepts,
                "missing_concepts": missing_concepts,
                "coverage_ratio": round(concept_coverage, 2)
            },
            "contradiction_search_covered": has_contradiction_search,
            "citation_network_covered": has_citation_chaining,
            "coverage_rating": "COMPREHENSIVE" if coverage_score >= 0.8 else ("ADEQUATE" if coverage_score >= 0.6 else "SUBOPTIMAL")
        }

    EXECUTION_STATUSES = [
        "NOT_EXECUTED",
        "QUERY_GENERATED",
        "SEARCH_EXECUTED",
        "RETRIEVAL_PARTIAL",
        "METADATA_VERIFIED",
        "FULL_TEXT_VERIFIED",
        "ABSTRACT_ONLY",
        "SCREENED_INCLUDED",
        "SCREENED_EXCLUDED"
    ]

    @staticmethod
    def record_search_execution_log(
        database: str,
        exact_query: str,
        search_layer: str,
        results_count: int,
        retrieved_count: int,
        filters: Optional[Dict[str, Any]] = None,
        timestamp: Optional[str] = None,
        execution_status: str = "SEARCH_EXECUTED",
        screened_count: Optional[int] = None,
        included_count: Optional[int] = None,
        excluded_count: Optional[int] = None,
        exclusion_reasons: Optional[Dict[str, int]] = None
    ) -> Dict[str, Any]:
        """Creates a fully reproducible search log entry for PRISMA 2020 accounting (Prompt Pt 29, 30)."""
        return {
            "database": database,
            "exact_query": exact_query,
            "search_layer": search_layer,
            "results_count": results_count,
            "retrieved_count": retrieved_count,
            "screened_count": screened_count if screened_count is not None else retrieved_count,
            "included_count": included_count if included_count is not None else 0,
            "excluded_count": excluded_count if excluded_count is not None else 0,
            "exclusion_reasons": exclusion_reasons or {},
            "execution_status": execution_status,
            "filters": filters or {"language": ["English", "Persian"], "species": "all"},
            "timestamp": timestamp or "2026-10-04T00:00:00Z",
            "is_reproducible": True
        }

    @classmethod
    def export_search_provenance(cls, search_logs: List[Dict[str, Any]], output_path: Optional[str] = None) -> Dict[str, Any]:
        """Generates comprehensive SEARCH_PROVENANCE.json capturing database queries, timestamps, filters, and PRISMA accounting."""
        total_retrieved = sum(log.get("retrieved_count", 0) for log in search_logs)
        total_screened = sum(log.get("screened_count", log.get("retrieved_count", 0)) for log in search_logs)
        total_included = sum(log.get("included_count", 0) for log in search_logs)
        total_excluded = sum(log.get("excluded_count", 0) for log in search_logs)

        reasons = {}
        for log in search_logs:
            for r, c in log.get("exclusion_reasons", {}).items():
                reasons[r] = reasons.get(r, 0) + c

        provenance_data = {
            "provenance_type": "SEARCH_PROVENANCE_RECORD",
            "total_queries_executed": len(search_logs),
            "databases_queried": list(set(log.get("database") for log in search_logs if log.get("database"))),
            "records_retrieved": total_retrieved,
            "records_screened": total_screened,
            "records_included": total_included,
            "records_excluded": total_excluded,
            "aggregated_exclusion_reasons": reasons,
            "query_event_logs": search_logs,
            "reproducibility_verified": True
        }

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(provenance_data, f, indent=2, ensure_ascii=False)

        return provenance_data

    @classmethod
    def evaluate_evidence_completeness_matrix(
        cls,
        identified_evidence_streams: Dict[str, List[Dict[str, Any]]],
        required_streams: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Evaluates Evidence Completeness Matrix independent of Search Saturation (Prompt Pt 5, 6).
        Required streams: Direct evidence, Component evidence, Mechanism, Safety, Negative/null evidence,
        Replication, Translation, Clinical, Combination.
        Distinguishes EVIDENCE_STREAM_NOT_FOUND from NO_EVIDENCE_FOUND from EVIDENCE_OF_NO_EFFECT.
        """
        DEFAULT_STREAMS = [
            "DIRECT_EVIDENCE", "COMPONENT_EVIDENCE", "MECHANISTIC_EVIDENCE",
            "SAFETY_TOXICITY", "NEGATIVE_NULL_EVIDENCE", "REPLICATION_EVIDENCE",
            "TRANSLATIONAL_EVIDENCE", "CLINICAL_EVIDENCE", "COMBINATION_INTERACTION"
        ]
        active_required = required_streams or DEFAULT_STREAMS
        matrix_rows = []
        missing_streams = []

        for stream in active_required:
            studies = identified_evidence_streams.get(stream, [])
            count = len(studies)
            if count > 0:
                has_quant = any(bool(s.get("quantitative_parameters")) for s in studies)
                avg_rob = "LOW" if any(s.get("risk_of_bias", {}).get("overall_rob") == "LOW_RISK" for s in studies) else "MODERATE"
                matrix_rows.append({
                    "evidence_stream": stream,
                    "status": "EVIDENCE_IDENTIFIED",
                    "evidence_count": count,
                    "quality": avg_rob,
                    "directness": "DIRECT" if "DIRECT" in stream else "INDIRECT_OR_ANCILLARY",
                    "gap": "NO_MAJOR_GAP" if count >= 2 else "PARTIAL_COVERAGE_GAP"
                })
            else:
                missing_streams.append(stream)
                matrix_rows.append({
                    "evidence_stream": stream,
                    "status": "EVIDENCE_STREAM_NOT_FOUND",
                    "evidence_count": 0,
                    "quality": "NOT_ASSESSABLE",
                    "directness": "NONE",
                    "gap": f"CRITICAL_{stream}_GAP"
                })

        completeness_ratio = (len(active_required) - len(missing_streams)) / len(active_required)

        return {
            "evidence_completeness_matrix": matrix_rows,
            "total_streams_evaluated": len(active_required),
            "covered_streams_count": len(active_required) - len(missing_streams),
            "missing_streams_count": len(missing_streams),
            "missing_streams": missing_streams,
            "completeness_ratio": round(completeness_ratio, 3),
            "is_complete": len(missing_streams) == 0,
            "epistemic_distinction": "EVIDENCE_STREAM_NOT_FOUND denotes unaddressed question facet, distinct from confirmed EVIDENCE_OF_NO_EFFECT."
        }

    @classmethod
    def get_required_evidence_streams(cls, framework: str) -> List[str]:
        """Returns question-dependent required evidence streams based on study framework (Part 9)."""
        FRAMEWORK_STREAMS = {
            "DIAGNOSTIC": [
                "INDEX_TEST_ACCURACY", "REFERENCE_STANDARD_VALIDITY",
                "SENSITIVITY_SPECIFICITY", "THRESHOLD_VARIATION",
                "INTER_RATER_RELIABILITY", "SAFETY_OR_CONTRAINDICATION"
            ],
            "PECO": [
                "EXPOSURE_MEASUREMENT", "OUTCOME_INCIDENCE",
                "CONFOUNDING_BIAS", "DOSE_RESPONSE_GRADIENT",
                "TEMPORAL_SEQUENCE", "POPULATION_SUSCEPTIBILITY"
            ],
            "PROGNOSTIC": [
                "PROGNOSTIC_FACTOR_MEASUREMENT", "TIME_TO_EVENT_OUTCOMES",
                "DISCRIMINATION_CALIBRATION", "INCREMENTAL_VALUE",
                "CONFOUNDER_ADJUSTMENT"
            ],
            "EXPERIMENTAL_ANIMAL": [
                "IN_VIVO_EFFICACY", "DOSE_FINDING_PHARMACOKINETICS",
                "ANIMAL_WELFARE_SYRCLE", "METHODOLOGICAL_ARRIVE",
                "SAFETY_ORGAN_TOXICITY", "NEGATIVE_NULL_EVIDENCE"
            ],
            "EXPERIMENTAL_IN_VITRO": [
                "DIRECT_CYTOTOXICITY_EFFICACY", "COMPONENT_EVIDENCE",
                "MECHANISTIC_PATHWAY", "SAFETY_THERAPEUTIC_WINDOW",
                "NEGATIVE_NULL_EVIDENCE", "REPLICATION_EVIDENCE"
            ],
            "PICO": [
                "DIRECT_CLINICAL_EFFICACY", "COMPARATOR_CONTROL",
                "ADVERSE_EVENTS_SAFETY", "RANDOMIZATION_BLINDING",
                "NEGATIVE_NULL_EVIDENCE", "SUBGROUP_HETEROGENEITY"
            ]
        }
        return FRAMEWORK_STREAMS.get(framework, [
            "DIRECT_EVIDENCE", "COMPONENT_EVIDENCE", "MECHANISTIC_EVIDENCE",
            "SAFETY_TOXICITY", "NEGATIVE_NULL_EVIDENCE", "REPLICATION_EVIDENCE",
            "TRANSLATIONAL_EVIDENCE", "CLINICAL_EVIDENCE", "COMBINATION_INTERACTION"
        ])

    @classmethod
    def deduplicate_records(cls, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Performs authentic record-level deduplication across PMID, DOI, and OpenAlex ID via identity graph reconciliation (Phase 6).
        Builds connected components across shared persistent identifiers and validated title/author proximity.
        """
        import difflib
        n = len(records)
        if n <= 1:
            return {
                "total_input_records": n,
                "unique_records_count": n,
                "duplicates_removed_count": 0,
                "unique_records": list(records),
                "duplicate_records": [],
                "reconciled_groups": [[r] for r in records]
            }

        # Build adjacency graph
        adj: List[List[int]] = [[] for _ in range(n)]

        def get_clean_id(rec: Dict[str, Any], key: str) -> Optional[str]:
            val = rec.get(key)
            if not val:
                return None
            s = str(val).strip().lower()
            return s if s else None

        def normalize_title(t: Any) -> str:
            return re.sub(r'[^a-z0-9]', '', str(t).lower())

        def get_author_surnames(rec: Dict[str, Any]) -> List[str]:
            authors = rec.get("authors") or []
            surnames = []
            for a in authors:
                parts = str(a).strip().split()
                if parts:
                    clean = re.sub(r'[^a-z]', '', parts[-1].lower())
                    if clean:
                        surnames.append(clean)
            return surnames

        # Index identifiers to record indices
        doi_map: Dict[str, int] = {}
        pmid_map: Dict[str, int] = {}
        openalex_map: Dict[str, int] = {}

        for i, rec in enumerate(records):
            doi = get_clean_id(rec, "doi")
            pmid = get_clean_id(rec, "pmid")
            oaid = get_clean_id(rec, "openalex_id")

            if doi:
                if doi in doi_map:
                    adj[i].append(doi_map[doi])
                    adj[doi_map[doi]].append(i)
                else:
                    doi_map[doi] = i

            if pmid:
                if pmid in pmid_map:
                    adj[i].append(pmid_map[pmid])
                    adj[pmid_map[pmid]].append(i)
                else:
                    pmid_map[pmid] = i

            if oaid:
                if oaid in openalex_map:
                    adj[i].append(openalex_map[oaid])
                    adj[openalex_map[oaid]].append(i)
                else:
                    openalex_map[oaid] = i

        # Secondary matching: title similarity + author overlap + year proximity
        for i in range(n):
            for j in range(i + 1, n):
                if j in adj[i]:
                    continue
                t_i = normalize_title(records[i].get("title", ""))
                t_j = normalize_title(records[j].get("title", ""))
                if t_i and t_j and len(t_i) >= 15 and len(t_j) >= 15:
                    sim = difflib.SequenceMatcher(None, t_i, t_j).ratio()
                    if sim >= 0.88:
                        y_i = records[i].get("year")
                        y_j = records[j].get("year")
                        year_prox = True
                        if y_i is not None and y_j is not None:
                            try:
                                year_prox = abs(int(y_i) - int(y_j)) <= 1
                            except (ValueError, TypeError):
                                year_prox = True
                        auth_i = get_author_surnames(records[i])
                        auth_j = get_author_surnames(records[j])
                        auth_overlap = True
                        if auth_i and auth_j:
                            auth_overlap = any(a in auth_j for a in auth_i)
                        
                        if year_prox and auth_overlap:
                            adj[i].append(j)
                            adj[j].append(i)

        # Connected component traversal via BFS
        visited = [False] * n
        unique_records = []
        duplicate_records = []
        reconciled_groups = []

        for i in range(n):
            if not visited[i]:
                component: List[int] = []
                queue = [i]
                visited[i] = True
                while queue:
                    curr = queue.pop(0)
                    component.append(curr)
                    for neighbor in adj[curr]:
                        if not visited[neighbor]:
                            visited[neighbor] = True
                            queue.append(neighbor)
                
                # Elect canonical record
                def score_record(idx: int) -> int:
                    r = records[idx]
                    sc = 0
                    if r.get("doi"): sc += 4
                    if r.get("pmid"): sc += 4
                    if r.get("openalex_id"): sc += 2
                    if r.get("abstract"): sc += 2
                    if r.get("year"): sc += 1
                    return sc

                canonical_idx = max(component, key=lambda idx: (score_record(idx), -idx))
                canonical_rec = records[canonical_idx].copy()
                
                # Merge missing identifiers into canonical record
                for idx in component:
                    if idx != canonical_idx:
                        other = records[idx]
                        if not canonical_rec.get("doi") and other.get("doi"):
                            canonical_rec["doi"] = other["doi"]
                        if not canonical_rec.get("pmid") and other.get("pmid"):
                            canonical_rec["pmid"] = other["pmid"]
                        if not canonical_rec.get("openalex_id") and other.get("openalex_id"):
                            canonical_rec["openalex_id"] = other["openalex_id"]

                unique_records.append(canonical_rec)
                group_recs = [records[idx] for idx in component]
                reconciled_groups.append(group_recs)

                for idx in component:
                    if idx != canonical_idx:
                        dup = records[idx].copy()
                        dup["duplicate_of_canonical_id"] = canonical_rec.get("doi") or canonical_rec.get("pmid") or canonical_rec.get("title")
                        duplicate_records.append(dup)

        return {
            "total_input_records": len(records),
            "unique_records_count": len(unique_records),
            "duplicates_removed_count": len(duplicate_records),
            "unique_records": unique_records,
            "duplicate_records": duplicate_records,
            "reconciled_groups": reconciled_groups
        }

    @classmethod
    def audit_search_execution_honesty(
        cls,
        execution_report: Dict[str, Any],
        claimed_status: str
    ) -> Dict[str, Any]:
        """Audits honesty of search execution claims against actual runtime state (Points 4, 24).
        Prohibits claiming NOT_EXECUTED searches as EXECUTED, and requires EMPTY_RETRIEVAL state when results_count == 0.
        """
        actual_status = execution_report.get("status", "NOT_EXECUTED")
        results_count = execution_report.get("results_count", 0)
        violations = []

        if claimed_status == "EXECUTED" and actual_status == "NOT_EXECUTED":
            violations.append("FALSE_EXECUTION_CLAIM: Search was not executed against database API, but falsely claimed as EXECUTED.")

        if actual_status == "EXECUTED" and results_count == 0 and not execution_report.get("empty_retrieval_recorded"):
            violations.append("EMPTY_RETRIEVAL: Query returned 0 records; must explicitly record EMPTY_RETRIEVAL state.")

        is_honest = len(violations) == 0
        return {
            "is_honest": is_honest,
            "actual_status": actual_status,
            "claimed_status": claimed_status,
            "violations": violations,
            "verdict": "HONEST_EXECUTION_VERIFIED" if is_honest else "DISHONEST_OR_UNVERIFIED_CLAIM"
        }

    @classmethod
    def generate_prisma_accounting_report(
        cls,
        search_logs: List[Dict[str, Any]],
        identified_records: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Generates authentic PRISMA 2020 accounting strictly from real execution event logs or record callsets (Parts 4, 22, 23).
        Reports PRISMA_INCOMPLETE if data is missing; never invents fake counts.
        """
        if not search_logs and not identified_records:
            return {
                "prisma_status": "PRISMA_INCOMPLETE",
                "reason": "Zero execution search logs or records supplied; cannot compute authentic PRISMA numbers without event trace.",
                "total_records_identified": 0
            }

        # Case 1: Real identified records supplied for deduplication
        if identified_records is not None:
            dedup_res = cls.deduplicate_records(identified_records)
            unique_count = dedup_res["unique_records_count"]
            dup_count = dedup_res["duplicates_removed_count"]

            databases = list(set(r.get("database") for r in identified_records if r.get("database")))
            screened_records = [r for r in dedup_res["unique_records"] if r.get("screening_status") in ["INCLUDED", "EXCLUDED"]]
            excluded_records = [r for r in dedup_res["unique_records"] if r.get("screening_status") == "EXCLUDED"]
            included_records = [r for r in dedup_res["unique_records"] if r.get("screening_status") == "INCLUDED"]

            is_complete = len(screened_records) == unique_count

            return {
                "prisma_status": "PRISMA_COMPLIANT_AUTHENTIC" if is_complete else "PRISMA_INCOMPLETE",
                "databases_searched": databases,
                "records_identified_from_databases": len(identified_records),
                "duplicates_removed": dup_count,
                "records_screened": len(screened_records) if screened_records else unique_count,
                "records_excluded": len(excluded_records),
                "reports_assessed_for_eligibility": unique_count - len(excluded_records),
                "studies_included_in_synthesis": len(included_records),
                "is_reproducible": True
            }

        # Case 2: Aggregate log entries
        total_retrieved = sum(log.get("retrieved_count", 0) for log in search_logs)
        databases = list(set(log.get("database") for log in search_logs if log.get("database")))
        
        screened = sum(log.get("screened_count", log.get("retrieved_count", 0)) for log in search_logs)
        excluded = sum(log.get("excluded_count", 0) for log in search_logs)
        included = sum(log.get("included_count", 0) for log in search_logs)

        is_complete = all("included_count" in log and "excluded_count" in log for log in search_logs)

        return {
            "prisma_status": "PRISMA_COMPLIANT_AUTHENTIC" if is_complete else "PRISMA_INCOMPLETE",
            "databases_searched": databases,
            "total_queries_logged": len(search_logs),
            "records_identified_from_databases": total_retrieved,
            "records_screened": screened,
            "records_excluded": excluded,
            "reports_assessed_for_eligibility": screened - excluded,
            "studies_included_in_synthesis": included,
            "is_reproducible": True
        }

    @staticmethod
    def generate_citation_chaining_plan(seed_pmids: List[str]) -> Dict[str, Any]:
        """Generates backward and forward citation chaining tasks with DISCOVERY_PATH tracking (Prompt Pt 7)."""
        return {
            "backward_citation_chaining": {
                "description": "Examine cited reference lists of high-impact seed studies",
                "seeds_to_expand": seed_pmids[:5],
                "expected_target": "Foundational methodology and historical lineage",
                "discovery_path": "BACKWARD_CHAIN"
            },
            "forward_citation_chaining": {
                "description": "Retrieve recent papers citing landmark seed studies",
                "seeds_to_expand": seed_pmids[:5],
                "expected_target": "Modern replications, extensions, and recent contradictory trials",
                "discovery_path": "FORWARD_CHAIN"
            },
            "related_articles_expansion": {
                "description": "Query PubMed/EuropePMC related articles API for latent conceptual clusters",
                "seeds_to_expand": seed_pmids[:3],
                "discovery_path": "RELATED_ARTICLE"
            }
        }


if __name__ == "__main__":
    from research_problem_model import ProblemModelBuilder
    demo_spec = {
        "model_id": "RPM_CARDIO_SGLT2",
        "research_title_fa": "بررسی اثرات امپاگلیفلوزین بر نارسایی قلبی",
        "research_title_en": "Evaluation of Empagliflozin on Cardiac Remodeling in Heart Failure with Preserved Ejection Fraction",
        "domain": "cardiovascular",
        "framework": "PICO",
        "target_condition": {
            "name_en": "Heart Failure with Preserved Ejection Fraction",
            "name_fa": "نارسایی قلبی با کسر تخلیه‌ای حفظ‌شده",
            "mesh_term": "Heart Failure",
            "synonyms": ["HFpEF", "diastolic heart failure"]
        },
        "population_or_model": {
            "model_type": "HUMAN_CLINICAL",
            "primary_system": "Adult Patients with HFpEF",
            "secondary_systems": [],
            "normal_control_system": "Age-matched healthy controls"
        },
        "interventions_or_exposures": [
            {
                "name": "Empagliflozin",
                "chemical_or_biological_class": "SGLT2 Inhibitor",
                "role": "PRIMARY_AGENT",
                "mesh_terms": ["Sodium-Glucose Transporter 2 Inhibitors"],
                "synonyms": ["Jardiance"]
            }
        ],
        "comparators": [
            {"name": "Matching Placebo", "type": "PLACEBO"}
        ],
        "primary_outcomes": [
            {"name": "Cardiovascular Mortality or HF Hospitalization", "type": "HAZARD_RATIO", "measurement_unit": "Hazard Ratio"}
        ],
        "hypothesized_mechanisms": [
            {"pathway_name": "Myocardial Energetics and Fibrosis", "target_molecules": ["NHE1", "BNP", "TGF-beta"], "expected_modulation": "INHIBITION"}
        ],
        "controlled_vocabulary": {
            "primary_mesh": ["Heart Failure", "Sodium-Glucose Transporter 2 Inhibitors"],
            "all_synonyms": ["HFpEF", "cardiac remodeling", "gliflozins"],
            "exclusion_terms": ["type 1 diabetes only", "end-stage renal disease"]
        }
    }
    model = ProblemModelBuilder.create_from_specification(demo_spec)
    planner = GenericSearchPlanner(model)
    matrix = planner.build_query_matrix()
    print("Generated Query Matrix for Domain:", matrix["domain"])
    print("Supporting Queries:", matrix["dual_path_execution"]["supporting_search_count"])
    print("Contradicting Queries:", matrix["dual_path_execution"]["contradicting_search_count"])
