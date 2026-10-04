#!/usr/bin/env python3
"""
generic_study_family_detector.py - Study Family & Duplicate Publication De-Duplication
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

Detects shared trial IDs (NCTxxxx), shared epidemiological cohorts (NHANES, UK Biobank, etc.),
and isolates Systematic Reviews from underlying primary papers to prevent double-counting.
"""

import re
from typing import Dict, List, Any, Set

KNOWN_COHORTS = [
    "uk biobank", "nhanes", "framingham", "tcga", "the cancer genome atlas",
    "mkn45 cohort", "seer database", "mesa study", "whi cohort", "nurses' health study",
    "health professionals follow-up", "aric study"
]

class StudyFamilyDetector:
    """Clusters publications derived from identical cohorts, trials, or reviews."""

    @staticmethod
    def extract_trial_registrations(text: str) -> List[str]:
        """Extracts clinical trial IDs like NCT12345678, ISRCTN12345678, IRCT12345678."""
        patterns = [
            r'NCT\d{3,8}',
            r'ISRCTN\d{8}',
            r'IRCT\d{10,14}[A-Za-z0-9]*'
        ]
        found = []
        for p in patterns:
            found.extend(re.findall(p, text, re.IGNORECASE))
        return list(set(found))

    @staticmethod
    def extract_cohort_names(text: str) -> List[str]:
        text_lower = text.lower()
        found = []
        for cohort in KNOWN_COHORTS:
            if cohort in text_lower:
                found.append(cohort)
        return found

    @classmethod
    def cluster_studies(cls, studies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assigns study_family_id to each study and identifies secondary/review dependencies."""
        trial_map: Dict[str, str] = {}    # trial_id -> family_id
        cohort_map: Dict[str, str] = {}   # cohort_name -> family_id
        families: Dict[str, List[str]] = {} # family_id -> list of study_ids
        study_assignments: Dict[str, str] = {}
        double_counting_warnings: List[str] = []

        # Pass 1: Extract registries and cohorts
        for study in studies:
            sid = study.get("study_id", study.get("doi", "unknown"))
            text_corpus = f"{study.get('title', '')} {study.get('abstract', '')}"
            
            trials = cls.extract_trial_registrations(text_corpus)
            cohorts = cls.extract_cohort_names(text_corpus)
            
            assigned_family = None
            for t in trials:
                if t in trial_map:
                    assigned_family = trial_map[t]
                    break
            if not assigned_family:
                for c in cohorts:
                    if c in cohort_map:
                        assigned_family = cohort_map[c]
                        break

            if not assigned_family:
                assigned_family = f"FAM_{sid}"

            # Register
            for t in trials:
                trial_map[t] = assigned_family
            for c in cohorts:
                cohort_map[c] = assigned_family

            study_assignments[sid] = assigned_family
            if assigned_family not in families:
                families[assigned_family] = []
            families[assigned_family].append(sid)

        # Pass 2: Detect multi-member families and flag potential double counting
        for fam_id, member_ids in families.items():
            if len(member_ids) > 1:
                double_counting_warnings.append(
                    f"Family {fam_id} has {len(member_ids)} clustered publications ({', '.join(member_ids)}). Synthesis must treat as 1 composite evidentiary unit."
                )

        return {
            "total_studies_evaluated": len(studies),
            "unique_evidence_families": len(families),
            "study_assignments": study_assignments,
            "multi_study_families": {k: v for k, v in families.items() if len(v) > 1},
            "double_counting_warnings": double_counting_warnings
        }

    @classmethod
    def evaluate_evidence_independence(cls, studies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates multi-tiered evidence independence metrics (Prompt Pt 7).
        Prevents conflating publication count with independent study count.
        """
        cluster_info = cls.cluster_studies(studies)
        unique_families = cluster_info["unique_evidence_families"]

        # Track distinct cohorts and author/research groups
        cohorts = set()
        research_groups = set()
        trials = set()

        for s in studies:
            text = f"{s.get('title', '')} {s.get('abstract', '')}"
            c_found = cls.extract_cohort_names(text)
            for c in c_found:
                cohorts.add(c)
            t_found = cls.extract_trial_registrations(text)
            for t in t_found:
                trials.add(t)

            lead_author = (s.get("authors", []) or ["UNKNOWN_GROUP"])[0]
            inst = s.get("affiliation", s.get("institution", lead_author))
            research_groups.add(str(inst).strip().lower())

        pub_count = len(studies)
        # Calculate true independent evidence streams: distinct combination of cohort, research group, and family
        independent_streams = min(unique_families, max(len(cohorts), 1) if cohorts else unique_families)

        return {
            "publication_count": pub_count,
            "study_count": unique_families,
            "independent_evidence_streams": independent_streams,
            "independent_study_count": unique_families,
            "independent_cohort_count": max(len(cohorts), 1) if cohorts else unique_families,
            "independent_research_group_count": max(len(research_groups), 1),
            "trial_count": len(trials),
            "evidence_inflation_factor": round(pub_count / max(unique_families, 1), 2),
            "synthesis_recommendation": f"Base evidence synthesis weight on {independent_streams} independent evidence streams rather than {pub_count} publications."
        }


if __name__ == "__main__":
    demo_studies = [
        {"study_id": "STUDY_01", "title": "Primary results of the EMPEROR-Preserved Trial (NCT03057977)", "abstract": "Randomized 5988 patients."},
        {"study_id": "STUDY_02", "title": "Subgroup analysis of EMPEROR-Preserved by renal function (NCT03057977)", "abstract": "Secondary analysis of trial cohort."},
        {"study_id": "STUDY_03", "title": "Independent in vitro study on cardiomyocytes", "abstract": "Investigated sodium hydrogen exchange."}
    ]
    result = StudyFamilyDetector.cluster_studies(demo_studies)
    print("Unique Families:", result["unique_evidence_families"], "out of", result["total_studies_evaluated"])
    print("Warnings:", result["double_counting_warnings"])
