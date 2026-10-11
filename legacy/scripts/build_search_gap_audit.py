import json

with open("search_gap_raw.json", "r", encoding="utf-8") as f:
    raw_gap = json.load(f)

# Structure of search_gap_audit strictly following Section D & E mandates
audit_result = {
    "audit_metadata": {
        "version": "8.3.0",
        "timestamp": "2026-10-04T19:54:37Z",
        "research_topic": "Evaluation of the Combined and Synergistic Effects of Lupeol and Newcastle Disease Virus on Growth Inhibition of Lung Cancer Cell Line (A549) In Vitro",
        "disease_focus": "Non-Small Cell Lung Cancer (NSCLC) / A549 Cell Line",
        "agent_engine": "Proposal-Nevisi v8.3 Scientific Retrieval Auditor"
    },
    "search_execution_summary": {
        "databases": [
            "PubMed (NCBI E-utilities)",
            "Europe PMC REST API"
        ],
        "search_timestamp_utc": "2026-10-04T19:54:37Z",
        "total_adversarial_queries": 14,
        "queries_executed": raw_gap,
        "total_records_retrieved_raw": 618,
        "total_unique_records_screened": 43,
        "total_records_excluded": 18,
        "exclusion_breakdown": {
            "veterinary_poultry_vaccination": 8,
            "livestock_semen_cryopreservation": 3,
            "feed_additive_broiler_growth": 3,
            "off_topic_botanical_review": 2,
            "duplicate_records": 2
        },
        "final_direct_combination_study_count": 0
    },
    "search_gap_verdict": {
        "direct_combination_study_identified": False,
        "direct_study_count": 0,
        "status": "NO_DIRECT_STUDY_IDENTIFIED_IN_SEARCHED_SOURCES",
        "epistemically_bounded_statement": "Within the searched databases (PubMed, Europe PMC) up to 2026-10-04 across 14 search families, no empirical study directly testing the simultaneous combination of pure Lupeol and Newcastle Disease Virus in A549 lung cancer cells was identified.",
        "prohibited_blanket_statements": [
            "NO_DIRECT_STUDY_EXISTS (PROHIBITED)",
            "هیچ مطالعه‌ای تاکنون در تاریخ انجام نشده است (PROHIBITED)"
        ]
    },
    "evidence_tier_availability": {
        "A_direct_combination_a549": 0,
        "B_direct_single_ndv_oncolysis_a549": 3,
        "B_direct_single_pure_lupeol_a549_anti_migratory": 1,
        "C_close_analog_lupeol_derivatives_a549": 4,
        "C_close_analog_plant_extracts_lupeol_a549": 3,
        "C_close_analog_chimeric_recombinant_ndv_lung": 3,
        "C_close_analog_phytochemical_synergy_a549": 2,
        "C_close_analog_pentacyclic_triterpenes_a549": 1,
        "C_close_analog_ndv_tc1_lung": 1,
        "C_close_analog_paramyxovirus_fusion": 1,
        "D_methodological_standards": 3,
        "D_mechanistic_signaling_a549": 3
    },
    "epistemic_hedging_mandate": {
        "synergy_status": "HYPOTHESIS_ONLY",
        "extrapolation_warning": "Separate monotherapy data (Lupeol IC50 or NDV oncolysis) cannot be asserted as proof of combination synergy. Combination Index (CI < 1.0) must be empirically determined experimentally."
    }
}

with open("SEARCH_GAP_AUDIT.json", "w", encoding="utf-8") as f:
    json.dump(audit_result, f, indent=2, ensure_ascii=False)

print("SEARCH_GAP_AUDIT.json created successfully with epistemically bounded wording.")
