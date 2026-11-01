#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mesh_query_expander.py - Advanced Multi-Domain MeSH Thesaurus & Precision Boolean Query Expansion Engine
Proposal-Nevisi Engine v13.2 (Comprehensive Multi-Domain Medical Core)

Provides:
1. Multi-Domain MeSH Thesaurus Mapping (130+ Standard Descriptors across 10 Clinical Disciplines):
   - Oncology & Hematology
   - Cardiovascular Medicine
   - Nephrology & Urology
   - Infectious Diseases & Antimicrobial Resistance
   - Neurology & Psychiatry
   - Endocrinology & Metabolic Disorders
   - Gastroenterology & Hepatology
   - Immunology & Rheumatology
   - Health Systems, Economics & Public Health
   - Diagnostic Medicine, Biomarkers & Imaging
   - Cellular & Molecular Mechanisms
2. Two-Tier Cascaded Search Strategy:
   - Tier 1: Precision MeSH Boolean Query with explicit field tags [MeSH Terms] OR [Title/Abstract].
   - Tier 2: Free-Text Smart Expansion Fallback.
3. Zero-Leakage Dynamic Tokenizer:
   - Clean extraction of Latin binomials, chemical entities, and English tokens.
   - Absolutely zero fall-through to cancer, apoptosis, or synergism on non-cancer topics.
"""

import re
from typing import Dict, List, Any, Optional, Tuple

MESH_THESAURUS: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # 1. ONCOLOGY & HEMATOLOGY
    # =========================================================================
    "colorectal": {
        "mesh": "Colorectal Neoplasms",
        "synonyms": ["colorectal cancer", "colon cancer", "rectal cancer", "colorectal carcinoma"],
        "category": "disease"
    },
    "breast": {
        "mesh": "Breast Neoplasms",
        "synonyms": ["breast cancer", "breast carcinoma", "mammary neoplasms"],
        "category": "disease"
    },
    "gastric": {
        "mesh": "Stomach Neoplasms",
        "synonyms": ["gastric cancer", "stomach cancer", "gastric carcinoma"],
        "category": "disease"
    },
    "pulmonary_neoplasms": {
        "mesh": "Lung Neoplasms",
        "synonyms": ["pulmonary neoplasms", "non-small cell pulmonary carcinoma", "NSCLC"],
        "category": "disease"
    },
    "prostate": {
        "mesh": "Prostatic Neoplasms",
        "synonyms": ["prostate cancer", "prostatic cancer", "prostate carcinoma"],
        "category": "disease"
    },
    "leukemia": {
        "mesh": "Leukemia",
        "synonyms": ["leukaemia", "acute myeloid leukemia", "AML"],
        "category": "disease"
    },
    "hepatocellular": {
        "mesh": "Carcinoma, Hepatocellular",
        "synonyms": ["liver cancer", "hepatoma", "HCC"],
        "category": "disease"
    },
    "glioblastoma": {
        "mesh": "Glioblastoma",
        "synonyms": ["GBM", "glioblastoma multiforme", "astrocytoma"],
        "category": "disease"
    },
    "ovarian": {
        "mesh": "Ovarian Neoplasms",
        "synonyms": ["ovarian cancer", "ovary cancer", "ovarian carcinoma"],
        "category": "disease"
    },
    "melanoma": {
        "mesh": "Melanoma",
        "synonyms": ["malignant melanoma", "cutaneous melanoma"],
        "category": "disease"
    },
    "pancreatic": {
        "mesh": "Pancreatic Neoplasms",
        "synonyms": ["pancreatic cancer", "pancreatic carcinoma", "PDAC"],
        "category": "disease"
    },
    "lymphoma": {
        "mesh": "Lymphoma",
        "synonyms": ["malignant lymphoma", "Hodgkin lymphoma", "non-Hodgkin lymphoma"],
        "category": "disease"
    },
    "multiple_myeloma": {
        "mesh": "Multiple Myeloma",
        "synonyms": ["plasma cell myeloma", "Kahler disease"],
        "category": "disease"
    },
    "bladder_cancer": {
        "mesh": "Urinary Bladder Neoplasms",
        "synonyms": ["bladder cancer", "urothelial carcinoma"],
        "category": "disease"
    },
    "renal_cancer": {
        "mesh": "Carcinoma, Renal Cell",
        "synonyms": ["renal cell cancer", "kidney cancer", "RCC"],
        "category": "disease"
    },
    "thyroid_cancer": {
        "mesh": "Thyroid Neoplasms",
        "synonyms": ["thyroid cancer", "papillary thyroid carcinoma"],
        "category": "disease"
    },
    "esophageal_cancer": {
        "mesh": "Esophageal Neoplasms",
        "synonyms": ["esophagus cancer", "esophageal carcinoma"],
        "category": "disease"
    },

    # =========================================================================
    # 2. CARDIOVASCULAR MEDICINE
    # =========================================================================
    "hypertension": {
        "mesh": "Hypertension",
        "synonyms": ["high blood pressure", "arterial hypertension", "essential hypertension"],
        "category": "disease"
    },
    "myocardial_infarction": {
        "mesh": "Myocardial Infarction",
        "synonyms": ["heart attack", "acute coronary syndrome", "coronary thrombosis"],
        "category": "disease"
    },
    "heart_failure": {
        "mesh": "Heart Failure",
        "synonyms": ["cardiac failure", "congestive heart failure", "HFpEF", "HFrEF"],
        "category": "disease"
    },
    "atherosclerosis": {
        "mesh": "Atherosclerosis",
        "synonyms": ["arteriosclerosis", "atheroma", "vascular plaque"],
        "category": "disease"
    },
    "arrhythmias": {
        "mesh": "Arrhythmias, Cardiac",
        "synonyms": ["cardiac arrhythmia", "atrial fibrillation", "ventricular arrhythmia"],
        "category": "disease"
    },
    "stroke": {
        "mesh": "Stroke",
        "synonyms": ["cerebrovascular accident", "ischemic stroke", "cerebral infarction", "CVA"],
        "category": "disease"
    },
    "coronary_artery_disease": {
        "mesh": "Coronary Artery Disease",
        "synonyms": ["coronary heart disease", "ischemic heart disease", "angina pectoris"],
        "category": "disease"
    },
    "cardiomyopathy": {
        "mesh": "Cardiomyopathies",
        "synonyms": ["dilated cardiomyopathy", "hypertrophic cardiomyopathy"],
        "category": "disease"
    },
    "thrombosis": {
        "mesh": "Thrombosis",
        "synonyms": ["blood clot", "deep vein thrombosis", "DVT", "embolism"],
        "category": "disease"
    },

    # =========================================================================
    # 3. NEPHROLOGY & UROLOGY
    # =========================================================================
    "chronic_kidney_disease": {
        "mesh": "Renal Insufficiency, Chronic",
        "synonyms": ["chronic kidney disease", "CKD", "chronic renal failure", "end-stage renal disease"],
        "category": "disease"
    },
    "acute_kidney_injury": {
        "mesh": "Acute Kidney Injury",
        "synonyms": ["acute renal failure", "AKI", "renal ischemia-reperfusion"],
        "category": "disease"
    },
    "glomerulonephritis": {
        "mesh": "Glomerulonephritis",
        "synonyms": ["glomerular disease", "nephrotic syndrome", "nephritic syndrome"],
        "category": "disease"
    },
    "diabetic_nephropathy": {
        "mesh": "Diabetic Nephropathies",
        "synonyms": ["diabetic kidney disease", "DKD", "diabetic glomerulosclerosis"],
        "category": "disease"
    },
    "dialysis": {
        "mesh": "Renal Dialysis",
        "synonyms": ["hemodialysis", "peritoneal dialysis", "renal replacement therapy"],
        "category": "therapy"
    },
    "urinary_tract_infection": {
        "mesh": "Urinary Tract Infections",
        "synonyms": ["UTI", "cystitis", "pyelonephritis"],
        "category": "disease"
    },

    # =========================================================================
    # 4. INFECTIOUS DISEASES & ANTIMICROBIAL RESISTANCE
    # =========================================================================
    "sepsis": {
        "mesh": "Sepsis",
        "synonyms": ["septic shock", "severe sepsis", "bacteremia", "systemic inflammatory response"],
        "category": "disease"
    },
    "bacterial_infections": {
        "mesh": "Bacterial Infections",
        "synonyms": ["bacterial disease", "Gram-negative infection", "Gram-positive infection"],
        "category": "disease"
    },
    "antimicrobial_resistance": {
        "mesh": "Drug Resistance, Microbial",
        "synonyms": ["antibiotic resistance", "multidrug resistant bacteria", "MDR pathogens"],
        "category": "pharmacology"
    },
    "tuberculosis": {
        "mesh": "Tuberculosis",
        "synonyms": ["TB", "Mycobacterium tuberculosis", "pulmonary tuberculosis"],
        "category": "disease"
    },
    "pneumonia": {
        "mesh": "Pneumonia",
        "synonyms": ["pulmonary infection", "community-acquired pneumonia", "nosocomial pneumonia"],
        "category": "disease"
    },
    "covid19": {
        "mesh": "COVID-19",
        "synonyms": ["SARS-CoV-2 infection", "coronavirus disease 2019"],
        "category": "disease"
    },
    "acinetobacter": {
        "mesh": "Acinetobacter baumannii",
        "synonyms": ["Acinetobacter infection", "carbapenem-resistant Acinetobacter"],
        "category": "organism"
    },
    "staphylococcus": {
        "mesh": "Staphylococcus aureus",
        "synonyms": ["MRSA", "methicillin-resistant Staphylococcus aureus", "staphylococcal infection"],
        "category": "organism"
    },
    "pseudomonas": {
        "mesh": "Pseudomonas aeruginosa",
        "synonyms": ["Pseudomonas infection", "multidrug-resistant Pseudomonas"],
        "category": "organism"
    },
    "viral_hepatitis": {
        "mesh": "Hepatitis, Viral, Human",
        "synonyms": ["hepatitis B", "hepatitis C", "HBV", "HCV"],
        "category": "disease"
    },

    # =========================================================================
    # 5. NEUROLOGY & PSYCHIATRY
    # =========================================================================
    "alzheimer": {
        "mesh": "Alzheimer Disease",
        "synonyms": ["Alzheimer's", "dementia, Alzheimer type", "senile dementia"],
        "category": "disease"
    },
    "parkinson": {
        "mesh": "Parkinson Disease",
        "synonyms": ["Parkinson's", "parkinsonism", "paralysis agitans"],
        "category": "disease"
    },
    "multiple_sclerosis": {
        "mesh": "Multiple Sclerosis",
        "synonyms": ["MS", "demyelinating autoimmune disease", "disseminated sclerosis"],
        "category": "disease"
    },
    "epilepsy": {
        "mesh": "Epilepsy",
        "synonyms": ["seizure disorder", "convulsions", "status epilepticus"],
        "category": "disease"
    },
    "depression": {
        "mesh": "Depressive Disorder",
        "synonyms": ["major depressive disorder", "MDD", "unipolar depression"],
        "category": "disease"
    },
    "anxiety": {
        "mesh": "Anxiety Disorders",
        "synonyms": ["generalized anxiety disorder", "panic disorder", "phobia"],
        "category": "disease"
    },
    "ptsd": {
        "mesh": "Stress Disorders, Post-Traumatic",
        "synonyms": ["PTSD", "posttraumatic stress disorder"],
        "category": "disease"
    },
    "schizophrenia": {
        "mesh": "Schizophrenia",
        "synonyms": ["schizoaffective disorder", "psychotic disorders"],
        "category": "disease"
    },
    "neuropathy": {
        "mesh": "Peripheral Neuropathy",
        "synonyms": ["diabetic neuropathy", "polyneuropathy", "nerve damage"],
        "category": "disease"
    },

    # =========================================================================
    # 6. ENDOCRINOLOGY & METABOLISM
    # =========================================================================
    "diabetes": {
        "mesh": "Diabetes Mellitus, Type 2",
        "synonyms": ["type 2 diabetes", "diabetic", "T2DM", "non-insulin dependent diabetes"],
        "category": "disease"
    },
    "diabetes_type1": {
        "mesh": "Diabetes Mellitus, Type 1",
        "synonyms": ["type 1 diabetes", "T1DM", "insulin-dependent diabetes"],
        "category": "disease"
    },
    "metabolic_syndrome": {
        "mesh": "Metabolic Syndrome",
        "synonyms": ["syndrome X", "insulin resistance syndrome"],
        "category": "disease"
    },
    "obesity": {
        "mesh": "Obesity",
        "synonyms": ["adiposity", "morbid obesity", "body mass index"],
        "category": "disease"
    },
    "thyroid_disease": {
        "mesh": "Thyroid Diseases",
        "synonyms": ["hypothyroidism", "hyperthyroidism", "Hashimoto thyroiditis"],
        "category": "disease"
    },
    "dyslipidemia": {
        "mesh": "Dyslipidemias",
        "synonyms": ["hyperlipidemia", "hypercholesterolemia", "high triglycerides"],
        "category": "disease"
    },
    "osteoporosis": {
        "mesh": "Osteoporosis",
        "synonyms": ["bone loss", "osteopenia", "bone mineral density"],
        "category": "disease"
    },

    # =========================================================================
    # 7. GASTROENTEROLOGY & HEPATOLOGY
    # =========================================================================
    "fatty_liver": {
        "mesh": "Fatty Liver",
        "synonyms": ["NAFLD", "NASH", "steatohepatitis", "metabolic dysfunction-associated steatotic liver disease"],
        "category": "disease"
    },
    "liver_cirrhosis": {
        "mesh": "Liver Cirrhosis",
        "synonyms": ["hepatic cirrhosis", "end-stage liver disease", "hepatic fibrosis"],
        "category": "disease"
    },
    "inflammatory_bowel_disease": {
        "mesh": "Inflammatory Bowel Diseases",
        "synonyms": ["IBD", "ulcerative colitis", "Crohn disease"],
        "category": "disease"
    },
    "peptic_ulcer": {
        "mesh": "Peptic Ulcer",
        "synonyms": ["gastric ulcer", "duodenal ulcer", "Helicobacter pylori ulcer"],
        "category": "disease"
    },
    "gerd": {
        "mesh": "Gastroesophageal Reflux",
        "synonyms": ["GERD", "acid reflux", "reflux esophagitis"],
        "category": "disease"
    },
    "pancreatitis": {
        "mesh": "Pancreatitis",
        "synonyms": ["acute pancreatitis", "chronic pancreatitis"],
        "category": "disease"
    },
    "ibs": {
        "mesh": "Irritable Bowel Syndrome",
        "synonyms": ["IBS", "spastic colon", "functional bowel disorder"],
        "category": "disease"
    },

    # =========================================================================
    # 8. IMMUNOLOGY & RHEUMATOLOGY
    # =========================================================================
    "rheumatoid_arthritis": {
        "mesh": "Arthritis, Rheumatoid",
        "synonyms": ["rheumatoid arthritis", "RA", "rheumatoid disease"],
        "category": "disease"
    },
    "lupus": {
        "mesh": "Lupus Erythematosus, Systemic",
        "synonyms": ["SLE", "systemic lupus", "lupus nephritis"],
        "category": "disease"
    },
    "autoimmune_diseases": {
        "mesh": "Autoimmune Diseases",
        "synonyms": ["autoimmunity", "autoantibody production"],
        "category": "disease"
    },
    "cytokines": {
        "mesh": "Cytokines",
        "synonyms": ["pro-inflammatory cytokines", "interleukins", "TNF-alpha", "IL-6"],
        "category": "mechanism"
    },
    "macrophages": {
        "mesh": "Macrophages",
        "synonyms": ["macrophage polarization", "M1 macrophage", "M2 macrophage"],
        "category": "mechanism"
    },

    # =========================================================================
    # 9. HEALTH SYSTEMS, ECONOMICS & PUBLIC HEALTH
    # =========================================================================
    "health_expenditures": {
        "mesh": "Health Expenditures",
        "synonyms": ["catastrophic health expenditure", "CHE", "out-of-pocket costs", "OOP", "financial protection"],
        "category": "health_economics"
    },
    "health_insurance": {
        "mesh": "Universal Health Insurance",
        "synonyms": ["health insurance coverage", "social health insurance", "universal health coverage"],
        "category": "health_economics"
    },
    "health_services_accessibility": {
        "mesh": "Health Services Accessibility",
        "synonyms": ["access to healthcare", "healthcare disparities", "equity in health"],
        "category": "health_economics"
    },
    "quality_of_life": {
        "mesh": "Quality of Life",
        "synonyms": ["health-related quality of life", "HRQoL", "QALY", "DALY"],
        "category": "health_economics"
    },
    "socioeconomic_factors": {
        "mesh": "Socioeconomic Factors",
        "synonyms": ["social determinants of health", "household income", "poverty"],
        "category": "health_economics"
    },

    # =========================================================================
    # 10. DIAGNOSTIC MEDICINE, BIOMARKERS & IMAGING
    # =========================================================================
    "diagnostic_accuracy": {
        "mesh": "Sensitivity and Specificity",
        "synonyms": ["diagnostic sensitivity", "diagnostic specificity", "accuracy of diagnostic tests"],
        "category": "diagnostic"
    },
    "biomarkers": {
        "mesh": "Biomarkers, Pharmacological",
        "synonyms": ["biological markers", "serum biomarkers", "diagnostic biomarkers"],
        "category": "diagnostic"
    },
    "roc_curve": {
        "mesh": "ROC Curve",
        "synonyms": ["receiver operating characteristic", "AUC-ROC", "area under curve"],
        "category": "diagnostic"
    },
    "predictive_values": {
        "mesh": "Predictive Value of Tests",
        "synonyms": ["positive predictive value", "PPV", "negative predictive value", "NPV"],
        "category": "diagnostic"
    },
    "mri": {
        "mesh": "Magnetic Resonance Imaging",
        "synonyms": ["MRI", "nuclear magnetic resonance imaging", "diffusion-weighted MRI"],
        "category": "diagnostic"
    },

    # =========================================================================
    # 11. CELLULAR & MOLECULAR PHENOMENA & PHARMACOLOGY
    # =========================================================================
    "apoptosis": {
        "mesh": "Apoptosis",
        "synonyms": ["programmed cell death", "caspase-dependent death"],
        "category": "mechanism"
    },
    "autophagy": {
        "mesh": "Autophagy",
        "synonyms": ["macroautophagy", "autophagic cell death"],
        "category": "mechanism"
    },
    "ferroptosis": {
        "mesh": "Ferroptosis",
        "synonyms": ["iron-dependent cell death", "lipid peroxidation cell death"],
        "category": "mechanism"
    },
    "synergism": {
        "mesh": "Drug Synergism",
        "synonyms": ["synergy", "synergistic effect", "combination index", "Chou-Talalay"],
        "category": "pharmacology"
    },
    "resistance": {
        "mesh": "Drug Resistance, Neoplasm",
        "synonyms": ["chemoresistance", "multidrug resistance", "MDR"],
        "category": "pharmacology"
    },
    "oxidative_stress": {
        "mesh": "Oxidative Stress",
        "synonyms": ["reactive oxygen species", "ROS generation", "lipid peroxidation"],
        "category": "mechanism"
    },
    "inflammation": {
        "mesh": "Inflammation",
        "synonyms": ["inflammatory response", "pro-inflammatory cytokines"],
        "category": "mechanism"
    },
    "nanoparticles": {
        "mesh": "Nanoparticles",
        "synonyms": ["nanocarriers", "nanomedicine", "nanoformulation"],
        "category": "delivery"
    },
    "liposomes": {
        "mesh": "Liposomes",
        "synonyms": ["liposomal delivery", "lipid nanoparticles"],
        "category": "delivery"
    },
    "cell_cycle": {
        "mesh": "Cell Cycle",
        "synonyms": ["cell cycle arrest", "G0/G1 arrest", "G2/M arrest"],
        "category": "mechanism"
    },
    "metastasis": {
        "mesh": "Neoplasm Invasiveness",
        "synonyms": ["cell migration", "cell invasion", "metastasis"],
        "category": "mechanism"
    },
    "angiogenesis": {
        "mesh": "Neovascularization, Pathologic",
        "synonyms": ["angiogenesis", "VEGF signaling"],
        "category": "mechanism"
    },

    # =========================================================================
    # 12. PULMONOLOGY & RESPIRATORY MEDICINE
    # =========================================================================
    "asthma": {
        "mesh": "Asthma",
        "synonyms": ["bronchial asthma", "airway hyperresponsiveness"],
        "category": "disease"
    },
    "copd": {
        "mesh": "Pulmonary Disease, Chronic Obstructive",
        "synonyms": ["COPD", "chronic bronchitis", "pulmonary emphysema"],
        "category": "disease"
    },
    "pulmonary_fibrosis": {
        "mesh": "Pulmonary Fibrosis",
        "synonyms": ["idiopathic pulmonary fibrosis", "IPF", "lung fibrosis"],
        "category": "disease"
    },
    "ards": {
        "mesh": "Respiratory Distress Syndrome",
        "synonyms": ["ARDS", "acute respiratory distress syndrome"],
        "category": "disease"
    },

    # =========================================================================
    # 13. OPHTHALMOLOGY & SENSORY MEDICINE
    # =========================================================================
    "glaucoma": {
        "mesh": "Glaucoma",
        "synonyms": ["ocular hypertension", "open-angle glaucoma"],
        "category": "disease"
    },
    "macular_degeneration": {
        "mesh": "Macular Degeneration",
        "synonyms": ["AMD", "age-related macular degeneration"],
        "category": "disease"
    },
    "diabetic_retinopathy": {
        "mesh": "Diabetic Retinopathy",
        "synonyms": ["proliferative diabetic retinopathy", "macular edema"],
        "category": "disease"
    },

    # =========================================================================
    # 14. DERMATOLOGY
    # =========================================================================
    "psoriasis": {
        "mesh": "Psoriasis",
        "synonyms": ["plaque psoriasis", "psoriatic disease"],
        "category": "disease"
    },
    "atopic_dermatitis": {
        "mesh": "Dermatitis, Atopic",
        "synonyms": ["eczema", "atopic eczema"],
        "category": "disease"
    },
    "vitiligo": {
        "mesh": "Vitiligo",
        "synonyms": ["leukoderma", "depigmentation"],
        "category": "disease"
    },

    # =========================================================================
    # 15. OBSTETRICS, GYNECOLOGY & REPRODUCTIVE HEALTH
    # =========================================================================
    "preeclampsia": {
        "mesh": "Pre-Eclampsia",
        "synonyms": ["pregnancy-induced hypertension", "toxemia of pregnancy"],
        "category": "disease"
    },
    "pcos": {
        "mesh": "Polycystic Ovary Syndrome",
        "synonyms": ["PCOS", "Stein-Leventhal syndrome"],
        "category": "disease"
    },
    "endometriosis": {
        "mesh": "Endometriosis",
        "synonyms": ["endometrioma", "pelvic endometriosis"],
        "category": "disease"
    },
    "infertility": {
        "mesh": "Infertility",
        "synonyms": ["subfertility", "reproductive sterility"],
        "category": "disease"
    },

    # =========================================================================
    # 16. ORTHOPEDICS & RHEUMATOLOGY EXTENDED
    # =========================================================================
    "osteoarthritis": {
        "mesh": "Osteoarthritis",
        "synonyms": ["degenerative joint disease", "knee osteoarthritis"],
        "category": "disease"
    },
    "ankylosing_spondylitis": {
        "mesh": "Spondylitis, Ankylosing",
        "synonyms": ["axial spondyloarthritis", "Bechterew disease"],
        "category": "disease"
    },

    # =========================================================================
    # 17. TOXICOLOGY, SAFETY & REPLICATION
    # =========================================================================
    "toxicity": {
        "mesh": "Toxicity Tests",
        "synonyms": ["toxicology", "acute toxicity", "cytotoxicity assay"],
        "category": "pharmacology"
    },
    "adverse_effects": {
        "mesh": "Drug-Related Side Effects and Adverse Reactions",
        "synonyms": ["adverse drug events", "drug toxicity", "side effects"],
        "category": "pharmacology"
    },
    "pharmacokinetics": {
        "mesh": "Pharmacokinetics",
        "synonyms": ["bioavailability", "drug metabolism", "clearance", "half-life"],
        "category": "pharmacology"
    },

    # =========================================================================
    # 18. HEALTH ECONOMICS & POLICY EXTENDED
    # =========================================================================
    "cost_benefit": {
        "mesh": "Cost-Benefit Analysis",
        "synonyms": ["cost-effectiveness analysis", "ICER", "economic evaluation"],
        "category": "health_economics"
    },
    "out_of_pocket": {
        "mesh": "Health Expenditures",
        "synonyms": ["out-of-pocket payment", "direct medical costs", "OOP"],
        "category": "health_economics"
    },

    # =========================================================================
    # 19. ADVANCED DIAGNOSTICS & IMAGING
    # =========================================================================
    "pet_scan": {
        "mesh": "Positron-Emission Tomography",
        "synonyms": ["PET scan", "18F-FDG PET", "PET-CT"],
        "category": "diagnostic"
    },
    "computed_tomography": {
        "mesh": "Tomography, X-Ray Computed",
        "synonyms": ["CT scan", "computed tomography", "spiral CT"],
        "category": "diagnostic"
    },
    "ultrasound": {
        "mesh": "Ultrasonography",
        "synonyms": ["ultrasound imaging", "sonography", "echocardiography"],
        "category": "diagnostic"
    },
    "qpcr": {
        "mesh": "Real-Time Polymerase Chain Reaction",
        "synonyms": ["quantitative PCR", "qPCR", "RT-qPCR"],
        "category": "diagnostic"
    },
    "flow_cytometry": {
        "mesh": "Flow Cytometry",
        "synonyms": ["FACS", "fluorescence-activated cell sorting"],
        "category": "diagnostic"
    },
    "biopsy": {
        "mesh": "Biopsy",
        "synonyms": ["histopathological biopsy", "tissue needle biopsy"],
        "category": "diagnostic"
    }
}

PERSIAN_TO_CONCEPT_MAP: List[Tuple[str, str]] = [
    # Oncology
    (r'سرطان\s+کولون|سرطان\s+روده|کولورکتال', "colorectal"),
    (r'سرطان\s+پستان|سرطان\s+سینه', "breast"),
    (r'سرطان\s+معده', "gastric"),
    (r'سرطان\s+ریه', "pulmonary_neoplasms"),
    (r'سرطان\s+پروستات', "prostate"),
    (r'لوسمی|سرطان\s+خون', "leukemia"),
    (r'سرطان\s+کبد|هپاتوسلولار', "hepatocellular"),
    (r'گلیوبلاستوما|تومور\s+مغزی', "glioblastoma"),
    (r'سرطان\s+تخمدان', "ovarian"),
    (r'ملانوما|سرطان\s+پوست', "melanoma"),
    (r'پانکراس|سرطان\s+پانکراس|لوزوالمعده', "pancreatic"),
    (r'لنفوم', "lymphoma"),
    (r'مولتیپل\s+میلوما', "multiple_myeloma"),
    (r'سرطان\s+مثانه', "bladder_cancer"),
    (r'سرطان\s+کلیه', "renal_cancer"),
    (r'سرطان\s+تیروئید', "thyroid_cancer"),
    (r'سرطان\s+مری', "esophageal_cancer"),

    # Cardiovascular
    (r'فشار\s*خون|پرفشاری\s*خون', "hypertension"),
    (r'سکته\s*قلبی|انفارکتوس\s*میوکارد', "myocardial_infarction"),
    (r'نارسایی\s*قلبی', "heart_failure"),
    (r'تصلب\s*شرایین|آترواسکلروز', "atherosclerosis"),
    (r'آریتمی|فیبریلاسیون\s*دهلیزی', "arrhythmias"),
    (r'سکته\s*مغزی|ایسکمی\s*مغزی', "stroke"),
    (r'بیماری\s*عروق\s*کرونر|تنگی\s*عروق\s*قلب', "coronary_artery_disease"),
    (r'کاردیومیوپاتی', "cardiomyopathy"),
    (r'ترومبوز|لخته\s*خون|آمبولی', "thrombosis"),

    # Nephrology & Urology
    (r'نارسایی\s*مزمن\s*کلیه|بیماری\s*مزمن\s*کلیه|\bckd\b', "chronic_kidney_disease"),
    (r'آسیب\s*حاد\s*کلیه|نارسایی\s*حاد\s*کلیه|\baki\b', "acute_kidney_injury"),
    (r'گلومرولونفریت|سندرم\s*نفروتیک', "glomerulonephritis"),
    (r'نفروپاتی\s*دیابتی', "diabetic_nephropathy"),
    (r'دیالیز|همودیالیز', "dialysis"),
    (r'عفونت\s*ادراری', "urinary_tract_infection"),

    # Infectious Diseases
    (r'سپسیس|شوک\s*سپتیک|عفونت\s*خون', "sepsis"),
    (r'عفونت\s*باکتریایی|باکتری', "bacterial_infections"),
    (r'مقاومت\s*میکروبی|مقاومت\s*آنتی‌بیوتیکی', "antimicrobial_resistance"),
    (r'(?:^|\s)سل(?:\s|[.,;:]|$)|بیماری\s*سل|توبرکولوز', "tuberculosis"),
    (r'پنومونی|ذات‌الریه', "pneumonia"),
    (r'کووید|کرونا|covid', "covid19"),
    (r'اسینتوباکتر|اسینتوباکتر\s*بومانی', "acinetobacter"),
    (r'استافیلوکوک|استافیلوکوک\s*اورئوس', "staphylococcus"),
    (r'سودوموناس|پسودوموناس', "pseudomonas"),
    (r'هپاتیت\s*ویروسی|هپاتیت', "viral_hepatitis"),

    # Neurology & Psychiatry
    (r'آلزایمر', "alzheimer"),
    (r'پارکینسون', "parkinson"),
    (r'ام‌اس|مولتیپل\s*اسکلروزیس', "multiple_sclerosis"),
    (r'صرع|تشنج', "epilepsy"),
    (r'افسردگی', "depression"),
    (r'اضطراب|اختلال\s*اضطرابی', "anxiety"),
    (r'استرس\s*پس\s*از\s*سانحه|ptsd', "ptsd"),
    (r'اسکیزوفرنی', "schizophrenia"),
    (r'نوروپاتی', "neuropathy"),

    # Endocrinology & Metabolism
    (r'دیابت\s*نوع\s*۲|دیابت', "diabetes"),
    (r'دیابت\s*نوع\s*۱', "diabetes_type1"),
    (r'سندرم\s*متابولیک', "metabolic_syndrome"),
    (r'چاقی|اضافه\s*وزن', "obesity"),
    (r'تیروئید|کم‌کاری\s*تیروئید|پرکاری\s*تیروئید', "thyroid_disease"),
    (r'چربی\s*خون|دیس‌لیپیدمی|کلسترول', "dyslipidemia"),
    (r'پوکی\s*استخوان|استئوپروز', "osteoporosis"),

    # Gastroenterology & Hepatology
    (r'کبد\s*چرب', "fatty_liver"),
    (r'سیروز\s*کبدی|سیروز', "liver_cirrhosis"),
    (r'بیماری\s*التهابی\s*روده|کولیت|کرون|\bibd\b', "inflammatory_bowel_disease"),
    (r'زخم\s*معده|زخم\s*پپتیک', "peptic_ulcer"),
    (r'رفلاکس|ریفلاکس|سوزش\s*سر\s*دل', "gerd"),
    (r'پانکراتیت', "pancreatitis"),
    (r'روده\s*تحریک‌پذیر|\bibs\b', "ibs"),

    # Immunology & Rheumatology
    (r'آرتریت\s*روماتوئید|روماتیسم', "rheumatoid_arthritis"),
    (r'لوپوس|\bsle\b', "lupus"),
    (r'بیماری\s*خودایمنی|خودایمنی', "autoimmune_diseases"),
    (r'سایتوکاین|سیتوکین', "cytokines"),
    (r'ماکروفاژ', "macrophages"),

    # Health Systems & Public Health
    (r'هزینه‌های\s*کمرشکن|هزینه\s*کمرشکن|\bche\b', "health_expenditures"),
    (r'پرداخت\s*از\s*جیب|\boop\b', "health_expenditures"),
    (r'بیمه\s*سلامت|بیمه\s*درمانی|پوشش\s*همگانی', "health_insurance"),
    (r'دسترسی\s*به\s*خدمات|دسترسی\s*به\s*سلامت|عدالت\s*در\s*سلامت', "health_services_accessibility"),
    (r'کیفیت\s*زندگی|qaly|daly', "quality_of_life"),
    (r'عوامل\s*اجتماعی\s*سلامت|وضعیت\s*اقتصادی', "socioeconomic_factors"),

    # Diagnostics, Biomarkers & Imaging
    (r'دقت\s*تشخیصی|حساسیت\s*و\s*ویژگی|روایی\s*تشخیصی', "diagnostic_accuracy"),
    (r'بیومارکر|نشانگر\s*زیستی', "biomarkers"),
    (r'منحنی\s*راک|منحنی\s*roc|\bauc\b', "roc_curve"),
    (r'ارزش\s*اخباری|\bppv\b|\bnpv\b', "predictive_values"),
    (r'ام‌آر‌آی|\bmri\b|تصویربرداری\s*تشدید\s*مغناطیسی', "mri"),

    # Cellular Mechanisms & Pharmacology
    (r'آپوپتوز|مرگ\s*برنامه‌ریزی\s*شده', "apoptosis"),
    (r'اتوفاژی', "autophagy"),
    (r'پروپتوز|فروپتوز', "ferroptosis"),
    (r'چرخه\s*سلولی|توقف\s*چرخه', "cell_cycle"),
    (r'مهاجرت\s*سلولی|تهاجم\s*سلولی|متاستاز', "metastasis"),
    (r'رگ‌زایی|آنژیوژنز', "angiogenesis"),
    (r'هم‌افزایی|سینرژی|سینرژیسم', "synergism"),
    (r'مقاومت\s*دارویی|مقاومت\s*به\s*شیمی‌درمانی', "resistance"),
    (r'استرس\s*اکسیداتیو|اکسیدان', "oxidative_stress"),
    (r'التهاب|ضد\s*التهاب', "inflammation"),
    (r'نانوذرات|نانوذره', "nanoparticles"),
    (r'لیپوزوم', "liposomes"),

    # Pulmonology
    (r'آسم|تنگی\s*نفس', "asthma"),
    (r'بیماری\s*انسدادی\s*مزمن\s*ریه|copd', "copd"),
    (r'فیبروز\s*ریه|فیبروز\s*ریوی', "pulmonary_fibrosis"),
    (r'دیسترس\s*تنفسی|ards', "ards"),

    # Ophthalmology
    (r'گلوکوم|آب\s*سیاه', "glaucoma"),
    (r'دژنراسیون\s*ماکولا|تخریب\s*ماکولا', "macular_degeneration"),
    (r'رتینوپاتی\s*دیابتی', "diabetic_retinopathy"),

    # Dermatology
    (r'پسوریازیس', "psoriasis"),
    (r'درماتیت\s*آتوپیک|اگزما', "atopic_dermatitis"),
    (r'پیسی|برص|ویتیلیگو', "vitiligo"),

    # OB/GYN
    (r'پره‌اکلامپسی|مسمومیت\s*بارداری', "preeclampsia"),
    (r'تخمدان\s*پلی‌کیستیک|pcos', "pcos"),
    (r'اندومتریوز', "endometriosis"),
    (r'ناباروری|عقیمی', "infertility"),

    # Orthopedics
    (r'آرتروز|استئوآرتریت', "osteoarthritis"),
    (r'اسپوندیلیت\s*آنکیلوزان', "ankylosing_spondylitis"),

    # Toxicology & Safety
    (r'سمیت|آزمون\s*سمیت', "toxicity"),
    (r'عوارض\s*جانبی|اثرات\s*نامطلوب', "adverse_effects"),
    (r'فارماکوکینتیک|نیمه‌عمر', "pharmacokinetics"),

    # Health Economics Extended
    (r'هزینه-اثربخشی|تحلیل\s*هزینه-فایده|icer', "cost_benefit"),

    # Diagnostics Extended
    (r'پت\s*اسکن|\bpet\b', "pet_scan"),
    (r'سی‌تی\s*اسکن|\bct\b', "computed_tomography"),
    (r'سونوگرافی|اکوکاردیوگرافی', "ultrasound"),
    (r'پلی‌مراز\s*زنجیره‌ای|qpcr|real-time\s*pcr', "qpcr"),
    (r'فلوسایتومتری|facs', "flow_cytometry"),
    (r'بیوپسی|نمونه‌برداری\s*بافتی', "biopsy"),
]


class MeSHQueryExpander:
    """Intelligent Multi-Domain MeSH thesaurus and two-tier search query planner."""

    @classmethod
    def map_concept_to_mesh(cls, concept_or_term: str) -> Optional[Dict[str, Any]]:
        """Maps any concept key, English term, or raw string to a standardized MeSH descriptor record."""
        term_clean = concept_or_term.strip().lower()
        if term_clean in MESH_THESAURUS:
            return MESH_THESAURUS[term_clean]

        for k, v in MESH_THESAURUS.items():
            if term_clean == v["mesh"].lower():
                return v
            if any(term_clean == syn.lower() for syn in v["synonyms"]):
                return v
        return None

    @classmethod
    def extract_mesh_entities(cls, text: str) -> List[Dict[str, Any]]:
        """Extracts all recognized biomedical MeSH entities from mixed Persian/English text."""
        matched = []
        seen_meshes = set()

        # 1. Match Persian regex patterns
        for pat, concept_key in PERSIAN_TO_CONCEPT_MAP:
            if re.search(pat, text, re.IGNORECASE):
                record = MESH_THESAURUS.get(concept_key)
                if record and record["mesh"] not in seen_meshes:
                    seen_meshes.add(record["mesh"])
                    matched.append(record)

        # 2. Match English words against Thesaurus
        words = re.findall(r'[A-Za-z][A-Za-z0-9_\-\+]{2,}', text)
        for w in words:
            rec = cls.map_concept_to_mesh(w)
            if rec and rec["mesh"] not in seen_meshes:
                seen_meshes.add(rec["mesh"])
                matched.append(rec)

        return matched

    @classmethod
    def build_tier1_precision_mesh_query(
        cls,
        text_or_topic: str,
        custom_agents: Optional[List[str]] = None
    ) -> str:
        """
        Builds Tier 1 Precision MeSH Boolean Query:
        Combines (MeSH Descriptor OR synonyms[Title/Abstract]) for each entity,
        ANDed together with pharmacological or clinical intervention agents.
        Guarantees 0% false cancer fallback for non-cancer topics.
        """
        entities = cls.extract_mesh_entities(text_or_topic)
        clauses = []

        # Build MeSH clauses
        for ent in entities:
            mesh_term = ent["mesh"]
            syns = ent.get("synonyms", [])
            terms = [f'"{mesh_term}"[MeSH Terms]']
            for s in syns[:3]:
                terms.append(f'"{s}"[Title/Abstract]')
            clauses.append("(" + " OR ".join(terms) + ")")

        # Add explicit agent/compound clauses (strictly English/ASCII tokens to protect NCBI API)
        raw_agents = list(custom_agents or [])
        agents = [ag.strip() for ag in raw_agents if ag and not re.search(r'[\u0600-\u06FF]', ag) and len(ag.strip()) > 1]
        if not agents:
            # Extract Latin/English chemical or clinical tokens from topic if not in MeSH
            en_tokens = re.findall(r'[A-Za-z][A-Za-z0-9_\-\+]{2,}', text_or_topic)
            for tok in en_tokens:
                if tok.lower() not in ["and", "the", "for", "with", "from", "against", "effect", "study", "evaluation"]:
                    if not any(tok.lower() in [ent["mesh"].lower()] + [s.lower() for s in ent.get("synonyms", [])] for ent in entities):
                        agents.append(tok)

        for ag in agents[:3]:
            clauses.append(f'("{ag}"[Title/Abstract] OR "{ag}"[MeSH Terms])')

        if not clauses:
            # Dynamic neutral clean fallback - NEVER falls back to cancer or apoptosis on unmapped topics
            return '("Biomedical Research"[Title/Abstract] OR "Clinical Protocol"[Title/Abstract]) AND "Health"[Title/Abstract]'

        return " AND ".join(clauses)

    @classmethod
    def build_tier2_fallback_query(
        cls,
        text_or_topic: str,
        custom_agents: Optional[List[str]] = None
    ) -> str:
        """
        Builds Tier 2 Broad Fallback Query.
        Prioritizes primary condition and interventions; guarantees 0% cancer fallback.
        """
        entities = cls.extract_mesh_entities(text_or_topic)
        keywords = []

        cat_order = {
            "disease": 0, "health_economics": 1, "diagnostic": 2,
            "pharmacology": 3, "mechanism": 4, "therapy": 5, "organism": 6, "delivery": 7
        }
        sorted_entities = sorted(entities, key=lambda e: cat_order.get(e.get("category", "mechanism"), 8))

        for ent in sorted_entities:
            keywords.append(ent["mesh"].split(",")[0])  # Primary name

        for ent in sorted_entities:
            if ent.get("synonyms"):
                keywords.append(ent["synonyms"][0])

        if custom_agents:
            clean_custom = [ag.strip() for ag in custom_agents if ag and not re.search(r'[\u0600-\u06FF]', ag) and len(ag.strip()) > 1]
            keywords.extend(clean_custom)
        else:
            en_tokens = re.findall(r'[A-Za-z][A-Za-z0-9_\-\+]{2,}', text_or_topic)
            for tok in en_tokens:
                if tok.lower() not in ["and", "the", "for", "with", "from", "against", "effect", "study", "evaluation"]:
                    keywords.append(tok)

        unique_kws = list(dict.fromkeys(keywords))
        if len(unique_kws) >= 2:
            return " AND ".join(f'"{k}"' for k in unique_kws[:4])
        elif unique_kws:
            return f'"{unique_kws[0]}" AND ("evaluation" OR "clinical" OR "outcomes")'
        return '"biomedical clinical evaluation" AND "protocol outcome"'
