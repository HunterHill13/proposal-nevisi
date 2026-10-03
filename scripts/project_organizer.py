#!/usr/bin/env python3
"""
project_organizer.py - Standard Biomedical Proposal Workspace Structurer
Proposal-Nevisi Engine v8.0 (Universal Biomedical Architecture)

Automatically provisions and maintains a clean, multi-tier directory structure
for any research proposal project session:
  - proposal/          : Word (.docx), Markdown (.md), and document guides
  - references/        : Citations, RIS, EndNote, and bibliographic validity audits
  - evidence/          : Study evidence records, matrices, ledgers, and DAG graphs
  - literature_search/ : Multi-database queries, logs, PRISMA accounting, and corpora
  - contradictions/    : Negative evidence, comparability matrices, and contradiction reports
  - policies/          : System architecture, search policies, and verification reports
  - archive/           : Superseded drafts, old versions, and historical logs
"""

import os
import sys
import shutil
from typing import Dict, List, Any

sys.stdout.reconfigure(encoding='utf-8')

STANDARD_DIRECTORIES = [
    "proposal",
    "references",
    "evidence",
    "literature_search",
    "contradictions",
    "policies",
    "archive"
]

FILE_ROUTING_MAP: Dict[str, List[str]] = {
    "proposal": [
        "MEDICAL_PROPOSAL_LUPEOL_NDV.docx",
        "MEDICAL_PROPOSAL_LUPEOL_NDV.md",
        "DOCUMENT_STYLE_GUIDE.md"
    ],
    "references": [
        "PROPOSAL_REFERENCE_SET.json",
        "BIBLIOGRAPHIC_VERIFICATION_CACHE.json",
        "FINAL_REFERENCE_VALIDITY_AUDIT.json",
        "FINAL_REFERENCE_VALIDITY_AUDIT.md",
        "FINAL_REFERENCE_USAGE_AUDIT.json",
        "references_library.ris",
        "EndNote_Citations.enw"
    ],
    "evidence": [
        "STUDY_EVIDENCE_RECORD.json",
        "EVIDENCE_LEDGER.json",
        "EVIDENCE_MATRIX.csv",
        "EVIDENCE_MATRIX.json",
        "ATOMIC_CLAIM_INVENTORY.json",
        "CLAIM_INVENTORY.json",
        "CLAIM_EVIDENCE_GRAPH.json",
        "CLAIM_EVIDENCE_MAP.json",
        "CLAIM_EVIDENCE_MATRIX.json",
        "CLAIM_DEPENDENCY_GRAPH.json",
        "CROSS_STUDY_RELATIONSHIP_LEDGER.json",
        "EVIDENCE_PROVENANCE_GRAPH.json",
        "TEMPORAL_EVIDENCE_MAP.json",
        "RESEARCH_GAP_MAP.json",
        "OVERREACH_AUDIT.json",
        "FINAL_EVIDENCE_SYNTHESIS.md"
    ],
    "literature_search": [
        "RESEARCH_CORPUS.json",
        "SOURCE_REGISTRY.json",
        "QUERY_MATRIX.json",
        "SEARCH_QUERY_LOG.json",
        "SEARCH_BOUNDARY.json",
        "PRISMA_FLOW_DATA.json",
        "PRISMA_SEARCH_ACCOUNTING.json",
        "EXCLUDED_STUDIES.json",
        "FULLTEXT_RETRIEVAL_AUDIT.json",
        "LITERATURE_DEEP_RESEARCH.md"
    ],
    "contradictions": [
        "CONTRADICTION_ANALYSIS.json",
        "NEGATIVE_EVIDENCE_REPORT.md",
        "NEGATIVE_EVIDENCE_LEDGER.json",
        "OPPOSING_EVIDENCE_MATRIX.json",
        "ADVERSARIAL_SEARCH_LOG.json",
        "STUDY_COMPARABILITY_MATRIX.json"
    ],
    "policies": [
        "FINAL_ARCHITECTURE.md",
        "GENERALIZATION_AUDIT.md",
        "SEARCH_POLICY.md",
        "EVIDENCE_SYNTHESIS_POLICY.md",
        "CONTRADICTION_POLICY.md",
        "CITATION_ENTAILMENT_POLICY.md",
        "TIME_BOUNDARY_POLICY.md",
        "SELF_AUDIT_REPORT.md",
        "V7_SELF_AUDIT_REPORT.md",
        "GENERALIZATION_TEST_REPORT.md"
    ]
}

def organize_workspace(base_dir: str = ".") -> Dict[str, Any]:
    """Creates the standard workspace directories and organizes files into their assigned folders."""
    print("=" * 75)
    print(">>> STRUCTURING BIOMEDICAL RESEARCH PROJECT WORKSPACE <<<")
    print(f"Base Directory: {os.path.abspath(base_dir)}")
    print("=" * 75)

    created_dirs = []
    moved_files = []

    # 1. Provision standard directories
    for d in STANDARD_DIRECTORIES:
        d_path = os.path.join(base_dir, d)
        if not os.path.exists(d_path):
            os.makedirs(d_path, exist_ok=True)
            created_dirs.append(d)

    # 2. Route files from base_dir into structured subdirectories
    for folder, file_list in FILE_ROUTING_MAP.items():
        dest_folder = os.path.join(base_dir, folder)
        for fname in file_list:
            src_path = os.path.join(base_dir, fname)
            dest_path = os.path.join(dest_folder, fname)

            # Only move if the file is in root and not already in dest
            if os.path.isfile(src_path) and os.path.abspath(src_path) != os.path.abspath(dest_path):
                shutil.move(src_path, dest_path)
                moved_files.append((fname, folder))
                print(f"  [MOVED] {fname} -> {folder}/")

    print("-" * 75)
    print(f"Directories created : {len(created_dirs)} ({', '.join(created_dirs) if created_dirs else 'All existed'})")
    print(f"Files organized     : {len(moved_files)}")
    print("=" * 75)

    return {
        "status": "SUCCESS",
        "created_directories": created_dirs,
        "moved_files_count": len(moved_files),
        "standard_directories": STANDARD_DIRECTORIES
    }

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    organize_workspace(target)
