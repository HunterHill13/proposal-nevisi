# Proposal-Nevisi Standards & Specifications Reference Manual
**Version:** 14.1.0  
**Scope:** Iranian Ministry of Health (Pajooheshyar) Proposal Architecture, 6-Archetype Study Polymorphism, Typography & OMML Specifications.

---

## 1. The 28 Canonical Pajooheshyar Sections

Every academic medical research proposal must strictly contain exactly 28 canonical sections (Level 2 Markdown headings `##`) numbered 1 to 28 with approved Persian titles:

| # | Canonical Persian Title | English Section Mapping | Objective & Core Methodological Requirements |
|---|-------------------------|-------------------------|----------------------------------------------|
| 1 | **موضوع** | Title & Study Identifiers | Full Persian title, English title, running title, project category, target university, and Pajooheshyar domain registration. |
| 2 | **بیان مسئله** | Statement of the Problem | Mechanistic biological rationale, epidemiological disease burden (GLOBOCAN, WHO/IHME GBD), unmet clinical need, and specific knowledge gap. |
| 3 | **مرور بر منابع (مقالات و فعالیت های مشابه به موضوع ما)** | Literature Review | Critical evidence synthesis structured with dedicated paragraphs per cited landmark study. Must separate direct target evidence from parallel models. |
| 4 | **اهمیت وضرورت تحقیق** | Significance & Innovation | Clinical, translational, and socio-economic necessity. Details why the study must be funded now and how it advances current standard of care. |
| 5 | **تعریف واژه ها (واژه های بولد و علمی که نیازمند توضیح هستند)** | Operational Definitions | Rigorous operational definitions for all primary interventions, biomarkers, pharmacological agents, clinical indices, and outcome measures. |
| 6 | **اهداف جزیی (تعیین تاثیر متغیر مستقل روی متغیر وابسته)** | Specific Aims | Quantifiable, hypothesis-driven aims testing specific independent-dependent variable relationships. |
| 7 | **اهداف کلی (همین موضوع با کلمه تعیین..)** | Primary Objective | Formal overarching objective matching the study title, prefixed with "تعیین...". |
| 8 | **اهداف کاربردی** | Practical Applications | Tangible applications in clinical practice, public health policy, diagnostic pipelines, or domestic pharmaceutical development. |
| 9 | **فرضیات و سوالات** | Hypotheses & Research Questions | Null ($H_0$) and alternative ($H_1$) hypotheses aligned with each specific aim, balancing expected synergy, non-inferiority, or equivalence. |
| 10 | **دستاورد ها (چه دستاوردی ازین تحقیق خواهیم داشت)** | Expected Deliverables | High-impact peer-reviewed publications, patentable IP, domestic diagnostic algorithms, and clinical protocols. |
| 11 | **جدول متغیر ها (نقش متغیر (وابسته، مستقل،مخدوش گر) و نوع متغیر(کیفی، کمی پیوسته یا کمی گسسته))** | Variables Matrix | Standardized Markdown table classifying role (Independent, Dependent, Confounder, Effect Modifier), type, scale of measurement, and measurement tool. |
| 12 | **جدول زمان بندی و مراحل اجرا** | Timeline & Implementation Gantt | Comprehensive multi-phase Gantt chart breaking down procurement, bench experiments, data collection, statistical audit, and reporting across quarters. |
| 13 | **روش اجرا** | General Methodology Overview | High-level architectural flowchart and experimental design overview connecting all procedural phases. |
| 14 | **نوع مطالعه** | Study Design | Specific epidemiological/experimental taxonomy (e.g., Double-blind Parallel RCT, In Vitro Factorial, Multistage Cross-Sectional, Prospective Cohort). |
| 15 | **جامعه مورد مطالعه** | Target Population & Model System | Biological host, animal model species/strain, certified human cell lines (ATCC), or patient cohort definition. |
| 16 | **محل انجام مطالعه** | Study Setting & Facilities | Accredited laboratories, university clinical research centers, hospitals, and collaborating reference institutions. |
| 17 | **معیار های ورود به مطالعه** | Inclusion Criteria | Objective clinical, phenotypic, diagnostic, or cellular prerequisites for eligibility. |
| 18 | **معیار های خروج از مطالعه** | Exclusion Criteria | Specific confounding comorbidities, pre-treatments, sample contamination, protocol non-compliance, or dropouts. |
| 19 | **ابزار های گردآوری اطلاعات** | Data Collection Instruments & Equipment | Specialized laboratory instrumentation (e.g., flow cytometer, qPCR, spectrophotometer), standardized case report forms (eCRF), or validated questionnaires. |
| 20 | **تعیین اعتبار ابزار گردآوری** | Tool Validity & Calibration | Instrument calibration protocols, international reference standards, assay sensitivity/specificity, or psychometric content/construct validity (CVI/CVR). |
| 21 | **تعیین ابزار گردآوری** | Tool Reliability & Reproducibility | Inter-rater and intra-rater reliability, test-retest intraclass correlation (ICC), Cronbach's alpha, or inter-assay coefficient of variation ($CV < 10\%$). |
| 22 | **حجم نمونه و روش محاسبه آن** | Sample Size Calculation | Formal statistical calculation utilizing validated formulas (Chow & Wang, Festing & Mead, Cochran, Buderer) with explicit $\alpha$, power ($1-\beta$), effect sizes, and attrition buffers. |
| 23 | **روش تجزیه و تحلیل داده** | Statistical Analysis Plan | Normality testing (Shapiro-Wilk), parametric/non-parametric tests (ANOVA, ANCOVA, Kruskal-Wallis), multivariable regression, effect sizes, and analysis software. |
| 24 | **ملاحظلات اخلاقی در صورت نیاز** | Ethical Considerations | National Research Ethics Committee compliance, institutional IRB approval code, informed consent procedures, biological sample handling, and data confidentiality. |
| 25 | **نحوه رعایت نکات امنیتی و حفاظت پروژه در صورت نیاز** | Biosafety & Risk Management | Biosafety Level (BSL-1/BSL-2) protocols, chemical hazard handling, hazardous waste disposal, personal protective equipment (PPE), and emergency spill procedures. |
| 26 | **مشکلات و محدودیت ها** | Potential Pitfalls & Limitations | Potential technical bottlenecks, biological model limitations, loss to follow-up, batch effects, and explicit mitigation strategies. |
| 27 | **روش انجام طرح، شیوه اجرایی مراحل طرح و چگونگی جمع آوری اطلاعات** | Step-by-Step Experimental Protocol | Exhaustive, reproducible procedural protocol detailing reagents, concentrations, incubation times, positive/negative controls, and assay steps. |
| 28 | **منابعی که استفاده شد (انگلیسی یا فارسی)** | Vancouver References | Complete bibliography strictly formatted according to ICMJE Vancouver style in monotonic cited order `[1]`, `[2]`, `[3]`, matching text markers. |

---

## 2. Six-Archetype Study Polymorphism Matrix

The proposal generation engine dynamically adapts all 28 sections based on the study archetype:

```
                            ┌────────────────────────────────────────┐
                            │    Study Archetype Classifier          │
                            └───────────────────┬────────────────────┘
                                                │
         ┌───────────────┬──────────────────────┼──────────────────────┬────────────────┐
         ▼               ▼                      ▼                      ▼                ▼
   clinical_rct       in_vivo                in_vitro            health_systems  epidemiological
   - CONSORT 2010     - ARRIVE 2.0           - MIQE / ATCC       - WHO WHS/NHA   - STROBE
   - Chow & Wang      - Mead Resource Eq.    - CompuSyn CI       - Cochran+DEFF  - Prevalence
   - ANCOVA / ITT     - Repeated ANOVA       - 2-Way ANOVA       - AOR / Kakwani - Multivariable
```

### Archetype Invariants:

1. **`clinical_rct` (Randomized Controlled Trial):**
   - **Framework:** CONSORT 2010 statement and GCP guidelines.
   - **Sample Size:** Chow & Wang / Cohen $d=0.50$ two-arm formula: $n_{\text{arm}} = 2(z_\alpha + z_\beta)^2 / d^2 = 64$ per arm ($N=128$, with $10-15\%$ attrition buffer).
   - **Analysis:** Intention-to-Treat (ITT) and Per-Protocol (PP), Baseline-adjusted ANCOVA.
   - **Ethics:** Clinical trial registry registration (IRCT), informed written consent, Data Safety Monitoring Board (DSMB).

2. **`in_vivo` (Animal Model Experimentation):**
   - **Framework:** ARRIVE 2.0 guidelines and 3Rs principle (Replacement, Reduction, Refinement).
   - **Sample Size:** Festing & Mead Resource Equation: $E = N - B - T$, where $10 \le E \le 20$. For 4 treatment groups ($T=4$) and 1 block ($B=1$), $N=24$ animals ($n=6$ per group gives $E = 24 - 1 - 4 = 19$).
   - **Analysis:** One-way or Repeated-Measures ANOVA followed by Tukey/Bonferroni post-hoc tests; survival curves with Kaplan-Meier and Log-Rank test.
   - **Ethics:** National animal welfare guidelines, humane endpoints, certified animal care facility protocols.

3. **`in_vitro` (Cellular & Molecular Assay):**
   - **Framework:** MIQE guidelines for qPCR, ATCC cell authentication via Short Tandem Repeat (STR), Mycoplasma-free verification.
   - **Sample Size:** Minimum 3 independent biological replicates ($N \ge 3$) conducted in triplicate technical wells.
   - **Analysis:** Factorial two-way ANOVA, dose-response curves (4-parameter logistic), Combination Index (CI) calculation via CompuSyn (Chou-Talalay method).
   - **Biosafety:** Biosafety Level 2 (BSL-2), laminar flow cabinet protocols, cytotoxic waste autoclaving.

4. **`health_systems` (Health Economics & Policy):**
   - **Framework:** WHO World Health Survey (WHS) and National Health Accounts (NHA).
   - **Sample Size:** Cochran formula adjusted for design effect ($DEFF = 1.5$) and non-response: $N = \frac{z^2 p (1-p)}{d^2} \times DEFF \times \frac{1}{1 - r} \approx 642$ households/patients.
   - **Analysis:** Catastrophic Health Expenditures (CHE at $40\%$ capacity to pay), Out-of-Pocket (OOP) expenditure ratios, Kakwani Concentration Index, multivariable logistic regression.
   - **Ethics:** Verbal/written institutional consent, strict anonymization of health insurance identifiers.

5. **`epidemiological` (Observational Cohort / Cross-Sectional / Case-Control):**
   - **Framework:** STROBE guidelines (Strengthening the Reporting of Observational Studies in Epidemiology).
   - **Sample Size:** Cochran prevalence formula: $n = \frac{z_{1-\alpha/2}^2 \cdot P(1-P)}{d^2}$.
   - **Analysis:** Directed Acyclic Graphs (DAGs) for confounding assessment, multivariable adjusted odds ratios (AOR), Cox proportional hazards models.
   - **Ethics:** Institutional review board approval, secure encrypted server storage for epidemiological registries.

6. **`diagnostic` (Diagnostic Accuracy & Biomarker Validation):**
   - **Framework:** STARD 2015 and QUADAS-2 risk of bias tool.
   - **Sample Size:** Buderer formula based on expected sensitivity, specificity, disease prevalence, and allowable absolute error margin.
   - **Analysis:** Receiver Operating Characteristic (ROC) curve analysis, Area Under the Curve (AUC), positive/negative predictive values (PPV/NPV), Youden Index cutoff determination.
   - **Ethics:** Blinded evaluation of index test and gold standard reference; human tissue biorepository consent.

---

## 3. MeSH Query Expansion & Dual-Path Balanced Search

The search engine (`scripts/mesh_query_expander.py` and `scripts/generic_search_planner.py`) incorporates 130+ standardized MeSH descriptors across 11 clinical fields:
1. **Oncology & Hematology:** Neoplasms, Carcinoma, Leukemia, Apoptosis, Antineoplastic Agents.
2. **Cardiovascular Medicine:** Myocardial Infarction, Heart Failure, Hypertension, Atherosclerosis.
3. **Nephrology & Urology:** Acute Kidney Injury, Renal Insufficiency Chronic, Glomerulonephritis.
4. **Infectious Diseases & AMR:** Drug Resistance Bacterial, Sepsis, Viral Load, Anti-Bacterial Agents.
5. **Neurology & Psychiatry:** Alzheimer Disease, Parkinson Disease, Stroke, Neuroprotective Agents.
6. **Endocrinology & Metabolism:** Diabetes Mellitus Type 2, Insulin Resistance, Obesity, Metabolic Syndrome.
7. **Gastroenterology & Hepatology:** Hepatitis, Liver Cirrhosis, Inflammatory Bowel Diseases.
8. **Immunology & Rheumatology:** Autoimmune Diseases, Arthritis Rheumatoid, Cytokines.
9. **Health Systems & Public Health:** Universal Health Insurance, Health Expenditures, Quality of Life.
10. **Diagnostic Medicine & Biomarkers:** ROC Curve, Sensitivity and Specificity, Early Detection of Cancer.
11. **Cellular & Molecular Mechanisms:** Autophagy, Reactive Oxygen Species, Gene Expression Profiling.

### Epistemic Transparency (Dual-Path Search Rule):
For any interventional or therapeutic topic, the engine queries both positive efficacy endpoints AND negative/toxic/adverse effect trials in parallel. It automatically inserts an official Epistemic Transparency callout:
> `◄ شفافیت معرفتی پیرامون سوگیری انتشار (Publication Bias):`  
> Explicitly documents potential publication bias, negative trial suppression, and heterogeneity across published reports.

---

## 4. Microsoft Word (.docx) Typesetting & Visual Standards

Documents compiled by `build_canonical_proposal_docx.py` conform to the official Pajooheshyar visual stylesheet:

### Typography & Palette:
- **Primary Corporate Font:** Dubai (دبی) with 10.5pt regular body text, color Charcoal (`#2D3748`), line spacing 1.15.
- **English Supporting Font:** Times New Roman for Latin terms, gene symbols, and Vancouver citations.
- **Palette Hierarchy:**
  - Navy (`#1A365D`): University titles, Level 1 headings, table headers.
  - Crimson (`#742A2A`): Level 2 subheadings, warnings, critical cutoffs.
  - Steel Blue (`#2B6CB0`): Level 3 subheadings, 55-character horizontal dividers (`───────────────────────────────────────────────────────`).
  - Teal (`#0D5C75`): Callout border highlights, special project tags.
  - Light Slate (`#F8FAFC`): Table zebra alternating rows, callout background.

### Invariant Rules:
1. **Soft Line Break Elimination:** Absolute zero `\r\n` or `<w:br/>` characters within paragraph body text. Soft returns cause Word justified alignment to stretch final lines across the entire page margin.
2. **Unicode Bidirectional Isolation:** Arabic/Persian text containing English citations or chemical names is isolated using Right-to-Left Marks (`\u200F`) and Left-to-Right Marks (`\u200E`) to prevent bracket inversion (e.g., ensuring `[1, 2, 8]` does not render as `[8 ,2 ,1]`).
3. **Table Pagination & Formatting:** Every table row must contain `<w:cantSplit/>` to prevent ugly page splits across rows. Header rows must contain `<w:tblHeader/>` to repeat automatically across page boundaries.
4. **Native OMML Formulas:** Mathematical equations (sample size, biostatistical models) are encoded in Office Math Markup Language (OMML) using `<m:oMath>`, `<m:f>` (fractions), and `<m:rad>` (radicals), ensuring crisp vector rendering at any zoom level.

---

## 5. Quality Rubric & Hard Gates (HARD-01 to HARD-06)

Evaluations performed by `resources/rubrics/professor-namoosi-rubric.md` and the 7-subagent study section enforce the following red lines:

- **`HARD-01: UNGROUNDED_PARAMETRIC_EXTRAPOLATION`**: Injecting diseases, cell lines, drugs, or numerical values completely unsupported by the cited literature.
- **`HARD-02: PHANTOM_REFERENCE_EXTERNAL_DRIFT`**: Fabricating PMIDs, DOIs, or referencing phantom textbooks (e.g., Harrison's) not indexed in verified databases.
- **`HARD-03: CRITICAL_CUTOFF_OMISSION`**: Omitting required clinical laboratory cutoffs, effect size parameters, $\alpha$ levels, or power thresholds.
- **`HARD-04: INSTRUCTOR_EXAM_ALERT_OMISSION`**: Omitting direct university guidelines, required Pajooheshyar section numbers, or mandatory methodological constraints.
- **`HARD-05: LATEX_MATH_SYNTAX_LEAKAGE`**: Allowing raw LaTeX tokens (`\frac`, `\sqrt`, `$$`) to leak into the Word document instead of native OMML formulas.
- **`HARD-06: BANNED_CLICHE_AND_META_LEAKAGE`**: Including colloquial AI conversational disclaimers ("As an AI assistant...", "In this proposal I have generated...") or shallow boilerplate cliches.
