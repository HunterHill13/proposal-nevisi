import csv
import json

claim_records = [
    {
        "claim_id": "CLM_01",
        "Claim": "Semi-synthetic lupeol quaternary phosphonium and carbamate derivatives induce apoptosis, caspase-3/9 cleavage, and S-phase arrest in A549 cells.",
        "Reference": "Chen Z et al. (2024); Tian S et al. (2024)",
        "PMID": "39369566; 39274838",
        "Exact_supporting_result": "Compound 14f significantly downregulated Bcl-2, upregulated Bax, cleaved caspase-9/3, and arrested A549 cells in S phase (IC50 = 1.2 uM).",
        "Endpoint": "Apoptosis induction & Cell cycle S-phase arrest",
        "Model": "A549 in vitro",
        "Evidence_polarity": "SUPPORTS",
        "Directness": "CLOSE_ANALOG (Semi-synthetic derivatives)",
        "Allowed_wording": "Findings strictly pertain to semi-synthetic C-3 modified derivatives and demonstrate that chemical functionalization can overcome natural lupeol resistance in lung cancer."
    },
    {
        "claim_id": "CLM_02",
        "Claim": "Oncolytic Newcastle Disease Virus strain induces oncolytic cytotoxicity and caspase-3/Bax apoptosis in lung cancer A549 cells.",
        "Reference": "Liang Y et al. (2021); Ali Akbar Esfahani M et al. (2026)",
        "PMID": "33968198; 41674174",
        "Exact_supporting_result": "NDV strain 7793 induced oncolysis in lung cancer A549 cells; caspase-3 and Bax upregulation mediated apoptosis, augmented by miR-204.",
        "Endpoint": "Oncolysis & Apoptosis (Caspase-3/Bax)",
        "Model": "A549 in vitro (and TC-1 in vitro)",
        "Evidence_polarity": "SUPPORTS",
        "Directness": "DIRECT_SINGLE_INTERVENTION (NDV oncolysis in A549)",
        "Allowed_wording": "NDV exhibits intrinsic oncolytic cytotoxicity and triggers caspase-3-mediated apoptosis in A549 lung adenocarcinoma cells."
    },
    {
        "claim_id": "CLM_03",
        "Claim": "Newcastle Disease Virus disrupts mitochondrial electron transport chain and metabolic precursor synthesis, modulated by p53 in A549 cells.",
        "Reference": "Zhao C et al. (2025)",
        "PMID": "41170972",
        "Exact_supporting_result": "NDV infection induces mitochondrial fragmentation and ETC impairment; wild-type p53 in A549 cells acts as a metabolic buffer preventing catastrophic energetic depletion.",
        "Endpoint": "Mitochondrial ETC, ROS & Host metabolic buffering",
        "Model": "A549 (p53-WT) vs H1299 (p53-null)",
        "Evidence_polarity": "SUPPORTS (for metabolic perturbation) / LIMITS_INTERPRETATION (for direct cytotoxic killing)",
        "Directness": "DIRECT_SINGLE_INTERVENTION (Mechanistic virology in A549)",
        "Allowed_wording": "NDV alters mitochondrial ETC and nucleotide synthesis, but p53 in A549 buffers against rapid energetic exhaustion, highlighting the necessity of co-targeting survival pathways."
    },
    {
        "claim_id": "CLM_04",
        "Claim": "Newcastle Disease Virus rewires host glycerophospholipid metabolism during viral infection in A549 cells.",
        "Reference": "Sun Y et al. (2026)",
        "PMID": "41942850",
        "Exact_supporting_result": "Multi-omics profiling revealed NDV infection significantly remodels glycerophospholipid metabolism, depleting LPC and LPE to facilitate viral replication.",
        "Endpoint": "Multi-omics host lipid metabolic rewiring",
        "Model": "A549 in vitro",
        "Evidence_polarity": "SUPPORTS",
        "Directness": "DIRECT_SINGLE_INTERVENTION (Multi-omics in A549)",
        "Allowed_wording": "NDV actively reprograms host lipid metabolism in A549 cells, establishing an altered metabolic state during oncolytic viral propagation."
    },
    {
        "claim_id": "CLM_05",
        "Claim": "Tubulin-targeting and thiazolidinedione-conjugated lupeol derivatives exert antiproliferative activity against A549 cells.",
        "Reference": "Zhao Y et al. (2026); Deng S et al. (2024)",
        "PMID": "41297068; 39459325",
        "Exact_supporting_result": "Synthesized lupeol derivatives targeted tubulin polymerization and mitochondrial membrane potential with sub-micromolar IC50 in A549 cells.",
        "Endpoint": "Antiproliferative IC50 & Tubulin / Mitochondrial targeting",
        "Model": "A549 in vitro",
        "Evidence_polarity": "SUPPORTS",
        "Directness": "CLOSE_ANALOG (Semi-synthetic derivatives)",
        "Allowed_wording": "Semi-synthetic functionalization of lupeol at C-3 yields potent antiproliferative derivatives against lung cancer cells."
    },
    {
        "claim_id": "CLM_06",
        "Claim": "Crude plant extracts and fractions rich in pentacyclic triterpenes exhibit antioxidant and cytotoxic growth inhibition in lung cancer cells.",
        "Reference": "Seglab F et al. (2024); Aborehab NM et al. (2023); Shehzadi S et al. (2025)",
        "PMID": "39336114; 37845669; 40951590",
        "Exact_supporting_result": "Terpenoid-rich fractions and crude extracts containing lupeol exhibited antioxidant capacity and cytotoxic inhibition across A549 cell lines.",
        "Endpoint": "Cytotoxic growth inhibition (Extract matrix)",
        "Model": "A549 in vitro",
        "Evidence_polarity": "SUPPORTS",
        "Directness": "CLOSE_ANALOG (Whole Plant Extracts)",
        "Allowed_wording": "Natural extracts containing lupeol and related triterpenoids exhibit in vitro growth inhibition in A549, reflecting combined phytochemical matrix effects."
    },
    {
        "claim_id": "CLM_07",
        "Claim": "Recombinant and chimeric NDV platforms (rVSV-NDV, IL-12 oNDV, NDV-anti-VEGFR2) mediate syncytial cell death and overcome therapeutic resistance in lung cancer.",
        "Reference": "Kortum F et al. (2025); Rosewell Shaw A et al. (2024); Liu L et al. (2025)",
        "PMID": "40896365; 39624055; 40382521",
        "Exact_supporting_result": "rVSV-NDV mediated syncytial cell fusion and necroptosis; IL-12 oNDV synergized with CAR-T cells in orthotopic NSCLC models.",
        "Endpoint": "Syncytial oncolytic cell death & Combination synergy",
        "Model": "Human lung cancer in vitro & Orthotopic in vivo",
        "Evidence_polarity": "SUPPORTS",
        "Directness": "CLOSE_ANALOG (Engineered & Hybrid Viral Platforms)",
        "Allowed_wording": "Engineered NDV constructs demonstrate the feasibility of combining oncolytic viral platforms with secondary agents to achieve enhanced tumor destruction in lung cancer."
    },
    {
        "claim_id": "CLM_08",
        "Claim": "Pentacyclic triterpenes differentially regulate cellular metabolism and viability in lung carcinoma cells.",
        "Reference": "Torres-Sanchez A et al. (2024)",
        "PMID": "38931361",
        "Exact_supporting_result": "Comparative profiling of six pentacyclic triterpenes revealed differential downregulation of glycolytic flux and cell viability in A549 cells.",
        "Endpoint": "Metabolic regulation & Viability across triterpene class",
        "Model": "A549 in vitro",
        "Evidence_polarity": "SUPPORTS",
        "Directness": "CLOSE_ANALOG (Related Triterpene Class)",
        "Allowed_wording": "Pentacyclic triterpenes as a structural class modulate cellular metabolic flux in A549 cells, with potency strongly dependent on specific molecular substitutions."
    },
    {
        "claim_id": "CLM_09",
        "Claim": "NDV stimulates differential Type I interferon production, providing tumor-selective oncolytic replication while sparing non-malignant cells.",
        "Reference": "Ginting TE et al. (2026)",
        "PMID": "42699700",
        "Exact_supporting_result": "NDV-induced IFN-I secretion modulated PD-L1 and MICA expression differentially in A549 tumor cells compared to normal cells.",
        "Endpoint": "Type I Interferon signaling & Tumor selectivity",
        "Model": "A549 vs normal non-malignant cells",
        "Evidence_polarity": "SUPPORTS",
        "Directness": "MECHANISTIC_METHOD_EVIDENCE (Selectivity mechanism)",
        "Allowed_wording": "Oncolytic selectivity of NDV is biologically grounded in deficient antiviral interferon pathways in malignant cells compared to normal counterparts."
    },
    {
        "claim_id": "CLM_10",
        "Claim": "Pure natural Lupeol inhibits cancer cell migration and invasion via downregulation of the MAPK/ERK pathway in lung adenocarcinoma.",
        "Reference": "Bhatt M et al. (2021)",
        "PMID": "32329697",
        "Exact_supporting_result": "Lupeol significantly inhibited cell migration in A549 cells with decreased expression of pErk1/2 protein along with N-cadherin and vimentin genes.",
        "Endpoint": "Cell migration, invasion & MAPK/ERK pathway inhibition",
        "Model": "A549 in vitro",
        "Evidence_polarity": "SUPPORTS",
        "Directness": "DIRECT_SINGLE_INTERVENTION (Pure Lupeol in A549: Anti-Migratory)",
        "Allowed_wording": "Pure natural Lupeol exerts selective anti-metastatic effects in A549 lung cancer cells through suppression of the MAPK/ERK signaling cascade."
    },
    {
        "claim_id": "CLM_10_CYTO_LIMITATION",
        "Claim": "Pure natural Lupeol alone at sub-toxic anti-migratory doses exerts direct cytotoxic cell killing or marked growth inhibition in A549 cells.",
        "Reference": "Bhatt M et al. (2021)",
        "PMID": "32329697",
        "Exact_supporting_result": "Despite having NO cytotoxic effects, lupeol also significantly inhibited cell migration in A549 cells... Lupeol showed no cytotoxic effects on A549 cells.",
        "Endpoint": "Cytotoxicity & Cell viability reduction",
        "Model": "A549 in vitro",
        "Evidence_polarity": "LIMITS_INTERPRETATION",
        "Directness": "LIMITING_EVIDENCE (Non-cytotoxic at physiological anti-migratory doses)",
        "Allowed_wording": "Pure natural Lupeol alone was documented to show NO cytotoxic effects on A549 cells at tested anti-migratory doses, directly establishing that Lupeol monotherapy is non-cytotoxic and necessitating investigation of combination strategies with an oncolytic virus."
    },
    {
        "claim_id": "CLM_11",
        "Claim": "Phytochemical combinations with therapeutic agents display synergistic cytotoxicity and enhanced apoptosis in A549 lung cancer cells.",
        "Reference": "Kumar A et al. (2026); Almalghooth HDM et al. (2026)",
        "PMID": "42621169; 42404852",
        "Exact_supporting_result": "Erucin + kaempferol and paclitaxel + eugenol co-treatments yielded synergistic growth inhibition (CI < 1.0) and enhanced apoptotic caspase activation in A549.",
        "Endpoint": "Drug combination synergism (CI < 1.0)",
        "Model": "A549 in vitro",
        "Evidence_polarity": "SUPPORTS",
        "Directness": "CLOSE_ANALOG (Proof-of-concept for phytochemical combination in A549)",
        "Allowed_wording": "Serves as empirical proof-of-concept that phytochemical co-treatments can achieve synergistic growth inhibition (CI < 1.0) in A549, but does NOT establish synergy for the untested Lupeol + NDV pair."
    },
    {
        "claim_id": "CLM_12",
        "Claim": "Pharmacological combination interactions and synergy are quantitatively evaluated using the Median-Effect Equation and Combination Index (CI).",
        "Reference": "Chou TC (2006); Chou TC (1984)",
        "PMID": "16968952; 6382953",
        "Exact_supporting_result": "Median-effect equation and combination index theorem define the mass-action mathematical basis for synergism (CI < 1), additive effect (CI = 1), and antagonism (CI > 1).",
        "Endpoint": "Mathematical algorithm for combination interaction analysis",
        "Model": "Theoretical pharmacology / Computerized algorithm",
        "Evidence_polarity": "SUPPORTS (for methodology)",
        "Directness": "METHOD_SUPPORT (Quantitative Algorithm Standard)",
        "Allowed_wording": "Provides the formal quantitative mathematical framework (Chou-Talalay method) for testing whether simultaneous drug interactions are synergistic, additive, or antagonistic."
    },
    {
        "claim_id": "CLM_13",
        "Claim": "Cellular viability and antiproliferative effects in vitro are quantitatively assessed using the colorimetric tetrazolium MTT reduction assay.",
        "Reference": "Mosmann T (1983)",
        "PMID": "6606682",
        "Exact_supporting_result": "Rapid colorimetric assay measuring cell survival and proliferation via mitochondrial cleavage of tetrazolium salt (MTT).",
        "Endpoint": "Mitochondrial metabolic viability bioassay",
        "Model": "In vitro cell culture bioassay",
        "Evidence_polarity": "SUPPORTS (for bioassay standard)",
        "Directness": "METHOD_SUPPORT (Standard Cell Viability Bioassay)",
        "Allowed_wording": "Established reference protocol for colorimetric measurement of in vitro cellular viability and cytotoxicity at 570 nm."
    },
    {
        "claim_id": "CLM_14",
        "Claim": "Co-targeting cell survival pathways (Akt, STAT3) and activating apoptotic cascades provides mechanistic rationale for combined anticancer approaches.",
        "Reference": "Yu J et al. (2026); Sun J et al. (2026)",
        "PMID": "42772808; 42633541",
        "Exact_supporting_result": "Dual inhibition of survival signaling (PI3K/Akt, STAT3) triggers mitochondrial apoptosis and cell cycle arrest in A549 cells.",
        "Endpoint": "Apoptotic pathway crosstalk & Survival signaling inhibition",
        "Model": "A549 in vitro",
        "Evidence_polarity": "SUPPORTS",
        "Directness": "MECHANISTIC_METHOD_EVIDENCE (Orthogonal signaling benchmarks)",
        "Allowed_wording": "Supports the biological hypothesis that inhibiting parallel survival cascades can sensitize NSCLC cells to apoptotic stimuli."
    },
    {
        "claim_id": "HYP_01",
        "Claim": "The simultaneous co-administration of Pure Lupeol and oncolytic Newcastle Disease Virus exerts a synergistic inhibitory effect (Chou-Talalay CI < 1.0) on A549 cells.",
        "Reference": "UNTESTED_HYPOTHESIS_PENDING_EXPERIMENT",
        "PMID": "NO_DIRECT_STUDY_IDENTIFIED_IN_SEARCHED_SOURCES",
        "Exact_supporting_result": "Zero published studies evaluating the combination of Pure Lupeol and NDV in cancer were identified in PubMed or Europe PMC.",
        "Endpoint": "Combination Index (CI < 1.0) / Synergistic growth inhibition",
        "Model": "A549 in vitro",
        "Evidence_polarity": "NEUTRAL (Untested Empirical Hypothesis)",
        "Directness": "HYPOTHESIS_ONLY (Primary research question of the proposed study)",
        "Allowed_wording": "Formulated strictly as a research hypothesis (HYPOTHESIS_ONLY) to be experimentally determined by median-effect dose titration and CompuSyn CI calculation."
    }
]

# Write to CSV
fieldnames = [
    "claim_id", "Claim", "Reference", "PMID", "Exact_supporting_result",
    "Endpoint", "Model", "Evidence_polarity", "Directness", "Allowed_wording"
]

with open("CLAIM_EVIDENCE_MATRIX.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(claim_records)

print(f"CLAIM_EVIDENCE_MATRIX.csv generated successfully with {len(claim_records)} claim-specific records.")
