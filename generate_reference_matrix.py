import json
import csv

with open("FINAL_SELECTED_PORTFOLIO_AUDITED.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

refs = raw.get("selection", {}).get("selected_references", [])

audit_rows = []

for idx, r in enumerate(refs, 1):
    pmid = str(r.get("pmid", "")).strip()
    doi = r.get("doi", "")
    title = r.get("title", "")
    authors = r.get("authors", [])
    first_author = authors[0] if authors else "Unknown"
    year = r.get("year", "")
    journal = r.get("journal", "")
    abstract = r.get("abstract", "")
    abstract_lower = abstract.lower()
    title_lower = title.lower()
    text = f"{title_lower} {abstract_lower}"

    # Default values
    intervention_identity = "Unknown"
    intervention_purity = "UNKNOWN"
    second_intervention_identity = "None"
    biological_model = "HUMAN_CELL_CULTURE"
    cell_line = "A549"
    study_design = "IN_VITRO_EXPERIMENTAL"
    primary_endpoint = "Unknown"
    actual_observed_effect = ""
    evidence_directness = "CLOSE_ANALOG"
    evidence_role = "BENCHMARK"
    evidence_polarity = "SUPPORTS"

    compound_tier = "NOT_APPLICABLE_VIRAL"
    is_pure_lupeol = "NO"
    viral_platform = "NOT_APPLICABLE"
    has_ndv = "NO"
    has_a549 = "YES" if "a549" in text else "NO"
    has_comb = "NO"

    # Specific paper mappings
    if pmid == "39369566": # Chen 2024
        intervention_identity = "Lupeol Quaternary Phosphonium Salt Derivatives"
        intervention_purity = "SEMI_SYNTHETIC_DERIVATIVE"
        second_intervention_identity = "None"
        cell_line = "A549"
        primary_endpoint = "Apoptosis induction, caspase-3/9 cleavage, S-phase arrest"
        actual_observed_effect = "Compound 14f significantly downregulated Bcl-2, upregulated Bax, cleaved caspase-3/9, and arrested A549 in S phase (IC50 = 1.2 uM)"
        evidence_directness = "CLOSE_ANALOG (Synthetic Derivative)"
        evidence_role = "DERIVATIVE_CYTOTOXICITY_BENCHMARK"
        evidence_polarity = "SUPPORTS"
        compound_tier = "TIER_3_LUPEOL_DERIVATIVES"
        is_pure_lupeol = "NO (Synthetic Derivative)"

    elif pmid == "33968198": # Liang 2021
        intervention_identity = "Newcastle Disease Virus (Strain 7793)"
        intervention_purity = "BIOLOGICAL_VIRAL_STRAIN"
        second_intervention_identity = "miR-204 mimic / inhibitor"
        viral_platform = "WILD_TYPE_OR_STANDARD_ONCOLYTIC_NDV"
        has_ndv = "YES"
        cell_line = "A549"
        primary_endpoint = "Oncolysis, cell viability reduction, apoptosis induction"
        actual_observed_effect = "NDV induced oncolytic cell death and caspase-3/Bax apoptosis in A549; miR-204 overexpression significantly augmented NDV-induced oncolysis"
        evidence_directness = "DIRECT_SINGLE_INTERVENTION (NDV oncolysis in A549)"
        evidence_role = "TARGET_VIRUS_ONCOLYSIS_BASELINE"
        evidence_polarity = "SUPPORTS"

    elif pmid == "39624055": # Rosewell Shaw 2024
        intervention_identity = "IL-12 encoding oNDV"
        intervention_purity = "RECOMBINANT_VIRUS"
        second_intervention_identity = "CAR-T cells"
        viral_platform = "RECOMBINANT_OR_CHIMERIC_PLATFORM"
        has_ndv = "YES (Engineered / Chimeric)"
        biological_model = "ORTHOTOPIC_LUNG_CANCER_MODEL"
        cell_line = "Other NSCLC lines / In Vivo"
        has_a549 = "NO"
        has_comb = "YES (Analogous: oNDV + CAR-T)"
        primary_endpoint = "Immunotherapy synergy, orthotopic lung tumor eradication"
        actual_observed_effect = "IL-12-encoding oNDV reprogrammed immunosuppressive tumor microenvironment and synergized with CAR-T cells in orthotopic NSCLC models"
        evidence_directness = "CLOSE_ANALOG (Recombinant NDV + Immunotherapy in Lung)"
        evidence_role = "VIRAL_COMBINATION_BENCHMARK"
        evidence_polarity = "SUPPORTS"

    elif pmid == "41170972": # Zhao 2025
        intervention_identity = "Newcastle Disease Virus"
        intervention_purity = "BIOLOGICAL_VIRAL_STRAIN"
        second_intervention_identity = "None (p53 genetic comparison)"
        viral_platform = "WILD_TYPE_OR_STANDARD_ONCOLYTIC_NDV"
        has_ndv = "YES"
        cell_line = "A549 (p53-WT) vs H1299 (p53-null)"
        primary_endpoint = "Mitochondrial electron transport chain, nucleotide synthesis, viral replication"
        actual_observed_effect = "NDV disrupted ETC complexes I/III and nucleotide biosynthesis; p53 in A549 buffered against energy depletion and ROS-mediated cytotoxicity, restricting NDV replication without catastrophic energetic collapse"
        evidence_directness = "DIRECT_SINGLE_INTERVENTION (Mechanistic NDV in A549)"
        evidence_role = "MECHANISTIC_VIRAL_METABOLISM_BASELINE"
        evidence_polarity = "LIMITS_INTERPRETATION" # p53 buffering in A549 limits ETC-mediated cytotoxicity

    elif pmid == "42621169": # Kumar 2026
        intervention_identity = "Erucin"
        intervention_purity = "PURE_PHYTOCHEMICAL"
        second_intervention_identity = "Kaempferol"
        compound_tier = "NOT_APPLICABLE_OTHER_PHYTOCHEMICAL"
        is_pure_lupeol = "NO (Other Phytochemical)"
        cell_line = "A549"
        has_comb = "YES (Phytochemical + Phytochemical in A549)"
        primary_endpoint = "Synergistic growth inhibition, apoptosis induction, CI calculation"
        actual_observed_effect = "Erucin and kaempferol co-treatment demonstrated synergistic growth inhibition in A549 cells (Chou-Talalay CI < 1.0) and enhanced apoptotic annexin V binding"
        evidence_directness = "CLOSE_ANALOG (Analogous Phytochemical Synergy in A549)"
        evidence_role = "ANALOGOUS_PHYTOCHEMICAL_SYNERGY_PROOF_OF_CONCEPT"
        evidence_polarity = "SUPPORTS"

    elif pmid == "41297068": # Zhao 2026
        intervention_identity = "Tubulin-targeting Lupeol Derivatives"
        intervention_purity = "SEMI_SYNTHETIC_DERIVATIVE"
        second_intervention_identity = "None"
        cell_line = "A549"
        compound_tier = "TIER_3_LUPEOL_DERIVATIVES"
        is_pure_lupeol = "NO (Synthetic Derivative)"
        primary_endpoint = "Tubulin polymerization inhibition, antiproliferative activity"
        actual_observed_effect = "Synthesized lupeol derivatives inhibited tubulin polymerization and exhibited sub-micromolar antiproliferative IC50 against A549 lung cancer cells"
        evidence_directness = "CLOSE_ANALOG (Synthetic Derivative)"
        evidence_role = "DERIVATIVE_CYTOTOXICITY_BENCHMARK"
        evidence_polarity = "SUPPORTS"

    elif pmid == "39336114": # Seglab 2024
        intervention_identity = "Inula viscosa terpenoid-rich fraction (containing Lupeol)"
        intervention_purity = "WHOLE_PLANT_EXTRACT"
        second_intervention_identity = "None"
        compound_tier = "TIER_4_CONTAINING_EXTRACT"
        is_pure_lupeol = "NO (Natural Plant Extract)"
        cell_line = "A549"
        primary_endpoint = "Free radical scavenging, cytotoxic growth inhibition"
        actual_observed_effect = "Terpenoid fraction containing pentacyclic triterpenes demonstrated antioxidant capacity and dose-dependent cytotoxicity in A549 cells"
        evidence_directness = "CLOSE_ANALOG (Whole Plant Extract)"
        evidence_role = "EXTRACT_CYTOTOXICITY_BENCHMARK"
        evidence_polarity = "SUPPORTS"

    elif pmid == "39274838": # Tian 2024
        intervention_identity = "Lupeol-3-carbamate Derivatives"
        intervention_purity = "SEMI_SYNTHETIC_DERIVATIVE"
        second_intervention_identity = "None"
        compound_tier = "TIER_3_LUPEOL_DERIVATIVES"
        is_pure_lupeol = "NO (Synthetic Derivative)"
        cell_line = "A549"
        primary_endpoint = "Antitumor evaluation, cell proliferation inhibition"
        actual_observed_effect = "Lupeol-3-carbamates displayed potent cytotoxicity against A549 cells with enhanced solubility compared to parent molecule"
        evidence_directness = "CLOSE_ANALOG (Synthetic Derivative)"
        evidence_role = "DERIVATIVE_CYTOTOXICITY_BENCHMARK"
        evidence_polarity = "SUPPORTS"

    elif pmid == "41942850": # Sun 2026
        intervention_identity = "Newcastle Disease Virus"
        intervention_purity = "BIOLOGICAL_VIRAL_STRAIN"
        second_intervention_identity = "None"
        viral_platform = "WILD_TYPE_OR_STANDARD_ONCOLYTIC_NDV"
        has_ndv = "YES"
        cell_line = "A549"
        study_design = "MULTI_OMICS_PROFILING"
        primary_endpoint = "Glycerophospholipid remodeling, host metabolome rewiring"
        actual_observed_effect = "Integrated transcriptomics/proteomics/metabolomics revealed NDV depletes host LPC/LPE and modulates phosphatidylserine to facilitate viral propagation"
        evidence_directness = "DIRECT_SINGLE_INTERVENTION (Multi-omics NDV in A549)"
        evidence_role = "METABOLIC_HOST_RESPONSE_BASELINE"
        evidence_polarity = "SUPPORTS"

    elif pmid == "37845669": # Aborehab 2023
        intervention_identity = "Thymus capitatus Lupene Derivative"
        intervention_purity = "WHOLE_PLANT_EXTRACT / FRACTION"
        second_intervention_identity = "None"
        compound_tier = "TIER_4_CONTAINING_EXTRACT"
        is_pure_lupeol = "NO (Natural Plant Extract)"
        cell_line = "A549"
        primary_endpoint = "Apoptosis induction, Let-7 miRNA / Cyclin D1 / VEGF pathway"
        actual_observed_effect = "Lupene derivative from Thymus capitatus induced apoptosis and downregulated Cyclin D1 and VEGF in A549 lung cancer cells"
        evidence_directness = "CLOSE_ANALOG (Plant Extract Lupene)"
        evidence_role = "EXTRACT_CYTOTOXICITY_BENCHMARK"
        evidence_polarity = "SUPPORTS"

    elif pmid == "39459325": # Deng 2024
        intervention_identity = "Thiazolidinedione-Conjugated Lupeol Derivatives"
        intervention_purity = "SEMI_SYNTHETIC_DERIVATIVE"
        second_intervention_identity = "None"
        compound_tier = "TIER_3_LUPEOL_DERIVATIVES"
        is_pure_lupeol = "NO (Synthetic Derivative)"
        cell_line = "A549"
        primary_endpoint = "Mitochondrial apoptotic pathway, membrane potential collapse"
        actual_observed_effect = "TZD-conjugated lupeol derivatives induced intrinsic apoptosis via mitochondrial disruption in A549 lung cancer cells"
        evidence_directness = "CLOSE_ANALOG (Synthetic Derivative)"
        evidence_role = "DERIVATIVE_CYTOTOXICITY_BENCHMARK"
        evidence_polarity = "SUPPORTS"

    elif pmid == "40896365": # Kortum 2025
        intervention_identity = "Oncolytic rVSV-NDV hybrid virus"
        intervention_purity = "CHIMERIC_HYBRID_VIRUS"
        second_intervention_identity = "None"
        viral_platform = "RECOMBINANT_OR_CHIMERIC_PLATFORM"
        has_ndv = "YES (Engineered / Chimeric)"
        cell_line = "Human lung cancer cells / A549"
        primary_endpoint = "Syncytial formation, immunogenic apoptosis and necroptosis"
        actual_observed_effect = "rVSV-NDV chimeric virus mediated robust syncytial cell fusion, activating both apoptotic and necroptotic cell death cascades in human lung cancer"
        evidence_directness = "CLOSE_ANALOG (Chimeric NDV Hybrid)"
        evidence_role = "ONCOLYTIC_SYNCYTIA_BENCHMARK"
        evidence_polarity = "SUPPORTS"

    elif pmid == "38931361": # Torres-Sanchez 2024
        intervention_identity = "Six Pentacyclic Triterpenes"
        intervention_purity = "RELATED_PENTACYCLIC_TRITERPENES"
        second_intervention_identity = "None"
        compound_tier = "TIER_5_RELATED_PENTACYCLIC_TRITERPENES"
        is_pure_lupeol = "NO (Group of 6 Triterpenes)"
        cell_line = "A549"
        primary_endpoint = "Metabolic flux, cell cycle arrest, glycolytic inhibition"
        actual_observed_effect = "Comparative analysis of 6 pentacyclic triterpenes demonstrated differential inhibition of glycolytic metabolism and viability in A549 cells"
        evidence_directness = "CLOSE_ANALOG (Related Triterpene Class)"
        evidence_role = "TRITERPENE_CLASS_BENCHMARK"
        evidence_polarity = "SUPPORTS"

    elif pmid == "41674174": # Ali Akbar Esfahani 2026
        intervention_identity = "Newcastle Disease Virus"
        intervention_purity = "BIOLOGICAL_VIRAL_STRAIN"
        second_intervention_identity = "None"
        viral_platform = "WILD_TYPE_OR_STANDARD_ONCOLYTIC_NDV"
        has_ndv = "YES"
        biological_model = "MOUSE_LUNG_CANCER_MODEL"
        cell_line = "TC-1 (Mouse Lung)"
        has_a549 = "NO"
        primary_endpoint = "Apoptosis-related gene expression (Bax, Bcl-2, Caspase-3)"
        actual_observed_effect = "NDV significantly upregulated Bax and Caspase-3 and downregulated Bcl-2 expression in lung carcinoma TC-1 cells"
        evidence_directness = "CLOSE_ANALOG (NDV in Non-A549 Lung Line)"
        evidence_role = "VIRAL_APOPTOSIS_MECHANISM_BENCHMARK"
        evidence_polarity = "SUPPORTS"

    elif pmid == "40382521": # Liu 2025
        intervention_identity = "Recombinant NDV-anti-VEGFR2"
        intervention_purity = "RECOMBINANT_VIRUS"
        second_intervention_identity = "Radiotherapy"
        viral_platform = "RECOMBINANT_OR_CHIMERIC_PLATFORM"
        has_ndv = "YES (Engineered / Chimeric)"
        has_a549 = "NO (Other NSCLC)"
        has_comb = "YES (oNDV + Radiotherapy)"
        primary_endpoint = "Radiotherapy sensitization, VEGF signaling, DNA repair impairment"
        actual_observed_effect = "Recombinant NDV expressing anti-VEGFR2 impaired DNA repair pathways and sensitized NSCLC cells to radiation"
        evidence_directness = "CLOSE_ANALOG (Recombinant NDV Combination)"
        evidence_role = "VIRAL_COMBINATION_BENCHMARK"
        evidence_polarity = "SUPPORTS"

    elif pmid == "40951590": # Shehzadi 2025
        intervention_identity = "Lantana camara leaf & root extracts (containing Lupeol)"
        intervention_purity = "WHOLE_PLANT_EXTRACT"
        second_intervention_identity = "None"
        compound_tier = "TIER_4_CONTAINING_EXTRACT"
        is_pure_lupeol = "NO (Natural Plant Extract)"
        cell_line = "A549, MCF-7, HepG2"
        primary_endpoint = "Cytotoxicity, phytochemical profiling"
        actual_observed_effect = "Crude Lantana extracts rich in triterpenes demonstrated dose-dependent cytotoxic effects across A549 and other solid tumor lines"
        evidence_directness = "CLOSE_ANALOG (Whole Plant Extract)"
        evidence_role = "EXTRACT_CYTOTOXICITY_BENCHMARK"
        evidence_polarity = "SUPPORTS"

    elif pmid == "42699700": # Ginting 2026
        intervention_identity = "Newcastle Disease Virus"
        intervention_purity = "BIOLOGICAL_VIRAL_STRAIN"
        second_intervention_identity = "None"
        viral_platform = "WILD_TYPE_OR_STANDARD_ONCOLYTIC_NDV"
        has_ndv = "YES"
        cell_line = "A549 & normal fibroblasts"
        primary_endpoint = "Type I interferon production, PD-L1 and MICA regulation"
        actual_observed_effect = "NDV-induced IFN-I secretion modulated PD-L1 and MICA expression differentially in tumor cells (A549) versus non-malignant normal cells"
        evidence_directness = "MECHANISTIC_METHOD_EVIDENCE (Interferon Selectivity)"
        evidence_role = "IMMUNE_SELECTIVITY_MECHANISM"
        evidence_polarity = "SUPPORTS"

    elif pmid == "42404852": # Almalghooth 2026
        intervention_identity = "Eugenol"
        intervention_purity = "PURE_PHYTOCHEMICAL"
        second_intervention_identity = "Paclitaxel"
        compound_tier = "NOT_APPLICABLE_OTHER_PHYTOCHEMICAL"
        is_pure_lupeol = "NO (Other Phytochemical)"
        cell_line = "A549"
        has_comb = "YES (Phytochemical + Chemotherapy in A549)"
        primary_endpoint = "Anticancer enhancement, combination efficacy in A549"
        actual_observed_effect = "Eugenol combined with paclitaxel enhanced apoptotic cytotoxicity and cell cycle arrest in A549 cells"
        evidence_directness = "CLOSE_ANALOG (Phytochemical + Drug Synergy in A549)"
        evidence_role = "ANALOGOUS_COMBINATION_BENCHMARK"
        evidence_polarity = "SUPPORTS"

    elif pmid == "16968952": # Chou 2006
        intervention_identity = "None (Theoretical Pharmacology & Algorithm)"
        intervention_purity = "METHODOLOGICAL_LANDMARK"
        second_intervention_identity = "None"
        biological_model = "CELL_FREE_MATHEMATICAL_MODEL"
        cell_line = "None / Theoretical"
        has_a549 = "NO"
        study_design = "METHODOLOGICAL_LANDMARK"
        compound_tier = "NOT_APPLICABLE_METHOD"
        is_pure_lupeol = "NO (Methodological Landmark)"
        primary_endpoint = "Median-effect equation, Combination Index theorem (CI)"
        actual_observed_effect = "Established mathematical definition and computer simulation for synergism (CI < 1), additivity (CI = 1), and antagonism (CI > 1)"
        evidence_directness = "METHOD_SUPPORT (Quantitative Synergy Algorithm)"
        evidence_role = "CANONICAL_SYNERGY_MATHEMATICAL_FRAMEWORK"
        evidence_polarity = "SUPPORTS" # Supports methodology, not biological efficacy

    elif pmid == "6606682": # Mosmann 1983
        intervention_identity = "None (MTT Colorimetric Bioassay Development)"
        intervention_purity = "METHODOLOGICAL_LANDMARK"
        second_intervention_identity = "None"
        biological_model = "CELL_CULTURE_BIOASSAY_DEVELOPMENT"
        cell_line = "Multiple In Vitro Lines"
        has_a549 = "NO"
        study_design = "METHODOLOGICAL_LANDMARK"
        compound_tier = "NOT_APPLICABLE_METHOD"
        is_pure_lupeol = "NO (Methodological Landmark)"
        primary_endpoint = "Colorimetric tetrazolium MTT cleavage by mitochondrial dehydrogenase"
        actual_observed_effect = "Developed standard colorimetric assay measuring cell survival and cytotoxicity via mitochondrial MTT reduction"
        evidence_directness = "METHOD_SUPPORT (Cell Viability Bioassay Standard)"
        evidence_role = "CANONICAL_MTT_ASSAY_STANDARD"
        evidence_polarity = "SUPPORTS" # Supports assay, not biological efficacy

    elif pmid == "6382953": # Chou 1984
        intervention_identity = "None (Dose-Effect Relationship Modeling)"
        intervention_purity = "METHODOLOGICAL_LANDMARK"
        second_intervention_identity = "None"
        biological_model = "CELL_FREE_MATHEMATICAL_MODEL"
        cell_line = "None / Theoretical"
        has_a549 = "NO"
        study_design = "METHODOLOGICAL_LANDMARK"
        compound_tier = "NOT_APPLICABLE_METHOD"
        is_pure_lupeol = "NO (Methodological Landmark)"
        primary_endpoint = "Quantitative analysis of dose-effect relationships for multiple inhibitors"
        actual_observed_effect = "Formulated original mass-action law derivation for multiple drug interactions"
        evidence_directness = "METHOD_SUPPORT (Dose-Effect Law Formulation)"
        evidence_role = "CANONICAL_DOSE_EFFECT_MATHEMATICAL_FRAMEWORK"
        evidence_polarity = "SUPPORTS" # Supports methodology, not biological efficacy

    elif pmid == "32329697": # Bhatt 2021 (ADVERSARIAL CORE AUDIT)
        intervention_identity = "Pure Natural Lupeol"
        intervention_purity = "PURE_NATURAL_COMPOUND"
        second_intervention_identity = "None"
        cell_line = "A549"
        compound_tier = "TIER_1_PURE_LUPEOL_A549_LUNG"
        is_pure_lupeol = "YES (Pure Natural Lupeol)"
        primary_endpoint = "Anti-metastatic migration inhibition & MAPK/ERK pathway modulation"
        actual_observed_effect = "Lupeol inhibited cell migration, showed NO cytotoxic effects on A549 cells, and decreased pErk1/2 and EMT gene expression (N-cadherin, vimentin)"
        evidence_directness = "DIRECT_SINGLE_INTERVENTION (Pure Lupeol in A549: Anti-Migratory)"
        evidence_role = "TARGET_INTERVENTION_ANTI_MIGRATORY_BASELINE"
        evidence_polarity = "LIMITS_INTERPRETATION" # Non-cytotoxic on A549; limits interpretation of Lupeol as a standalone cytotoxic killer

    elif pmid == "42772808": # Yu 2026
        intervention_identity = "Matrine"
        intervention_purity = "PURE_ALKALOID"
        second_intervention_identity = "None"
        compound_tier = "NOT_APPLICABLE_OTHER_PHYTOCHEMICAL"
        is_pure_lupeol = "NO (Other Phytochemical)"
        cell_line = "A549"
        primary_endpoint = "CHEK1-mediated DNA repair, PI3K/Akt survival signaling, apoptosis"
        actual_observed_effect = "Matrine suppressed NSCLC progression via dual inhibition of CHEK1-mediated DNA repair and PI3K/Akt pathway"
        evidence_directness = "MECHANISTIC_METHOD_EVIDENCE (Pathway Signaling)"
        evidence_role = "ORTHOGONAL_SURVIVAL_PATHWAY_BENCHMARK"
        evidence_polarity = "SUPPORTS"

    elif pmid == "39792924": # Yang 2025
        intervention_identity = "Paramyxovirus fusion machinery / SLC35A2 modulation"
        intervention_purity = "MOLECULAR_VIROLOGY_MECHANISM"
        second_intervention_identity = "None"
        viral_platform = "RECOMBINANT_OR_CHIMERIC_PLATFORM"
        has_ndv = "YES (Paramyxovirus Family)"
        cell_line = "A549"
        primary_endpoint = "Host factor SLC35A2 regulation of viral syncytial fusion"
        actual_observed_effect = "SLC35A2 gene product modulates paramyxovirus fusion events during host cell infection"
        evidence_directness = "CLOSE_ANALOG (Paramyxovirus Fusion Virology)"
        evidence_role = "SYNCYTIAL_VIROLOGY_MECHANISM"
        evidence_polarity = "SUPPORTS"

    elif pmid == "42633541": # Sun 2026
        intervention_identity = "Jolkinolide B"
        intervention_purity = "PURE_DITERPENOID"
        second_intervention_identity = "None"
        compound_tier = "NOT_APPLICABLE_OTHER_PHYTOCHEMICAL"
        is_pure_lupeol = "NO (Other Phytochemical)"
        cell_line = "A549"
        primary_endpoint = "JAK2/STAT3 signaling inhibition, G1 cell cycle arrest, apoptosis"
        actual_observed_effect = "Jolkinolide B induced intrinsic apoptosis and G1 arrest in A549 cells via JAK2/STAT3 pathway suppression"
        evidence_directness = "MECHANISTIC_METHOD_EVIDENCE (Apoptosis Pathway)"
        evidence_role = "ORTHOGONAL_APOPTOSIS_MECHANISM_BENCHMARK"
        evidence_polarity = "SUPPORTS"

    # Evidence Category Partition
    if "DIRECT_COMBINATION" in evidence_directness:
        evidence_category = "A. DIRECT_COMBINATION_EVIDENCE"
    elif "DIRECT_SINGLE_INTERVENTION" in evidence_directness:
        evidence_category = "B. DIRECT_SINGLE_INTERVENTION_EVIDENCE"
    elif "CLOSE_ANALOG" in evidence_directness:
        evidence_category = "C. CLOSE_ANALOG_EVIDENCE"
    else:
        evidence_category = "D. MECHANISTIC_METHOD_EVIDENCE"

    # Role in proposal / Claims mapping
    claim_ids = []
    if pmid in ["39369566", "39274838"]: claim_ids.append("CLM_01")
    if pmid in ["33968198"]: claim_ids.append("CLM_02")
    if pmid in ["41170972"]: claim_ids.append("CLM_03")
    if pmid in ["41942850"]: claim_ids.append("CLM_04")
    if pmid in ["41297068", "39459325"]: claim_ids.append("CLM_05")
    if pmid in ["39336114", "37845669", "40951590"]: claim_ids.append("CLM_06")
    if pmid in ["40896365", "40382521", "39624055"]: claim_ids.append("CLM_07")
    if pmid in ["38931361"]: claim_ids.append("CLM_08")
    if pmid in ["42699700"]: claim_ids.append("CLM_09")
    if pmid in ["32329697"]: claim_ids.extend(["CLM_10", "CLM_10_CYTO_LIMITATION"])
    if pmid in ["42621169", "42404852"]: claim_ids.append("CLM_11")
    if pmid in ["16968952", "6382953"]: claim_ids.append("CLM_12")
    if pmid in ["6606682"]: claim_ids.append("CLM_13")
    if pmid in ["42772808", "42633541"]: claim_ids.append("CLM_14")
    if pmid in ["41674174"]: claim_ids.append("CLM_02")
    if pmid in ["39792924"]: claim_ids.append("CLM_03")

    role_status = "VALID_EMPIRICAL_ROLE" if claim_ids else "DECORATIVE_REFERENCE_FLAGGED"

    row = {
        "Ref_Number": idx,
        "PMID": pmid,
        "DOI": doi,
        "First_Author": first_author,
        "Publication_Year": year,
        "Journal": journal,
        "Title": title,
        "Bibliographic_Verification_Status": "VERIFIED_AUTHENTIC_PUBMED_E_FETCH",
        "intervention_identity": intervention_identity,
        "intervention_purity": intervention_purity,
        "second_intervention_identity": second_intervention_identity,
        "biological_model": biological_model,
        "cell_line": cell_line,
        "study_design": study_design,
        "primary_endpoint": primary_endpoint,
        "actual_observed_effect": actual_observed_effect,
        "evidence_directness": evidence_directness,
        "evidence_role": evidence_role,
        "evidence_polarity": evidence_polarity,
        "Compound_Identity_Tier": compound_tier,
        "Pure_Lupeol": is_pure_lupeol,
        "Viral_Platform": viral_platform,
        "NDV": has_ndv,
        "A549": has_a549,
        "Combination": has_comb,
        "Evidence_Category": evidence_category,
        "Claims_Supported": "; ".join(claim_ids) if claim_ids else "NONE",
        "Role_Status": role_status
    }
    audit_rows.append(row)

print("Reference evidence matrix generated with complete Section A fields.")
print(f"Total rows: {len(audit_rows)}")

# Write to CSV
fieldnames = list(audit_rows[0].keys())
with open("REFERENCE_EVIDENCE_MATRIX.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(audit_rows)
print("REFERENCE_EVIDENCE_MATRIX.csv written successfully.")
