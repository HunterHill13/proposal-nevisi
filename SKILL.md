---
name: proposal-nevisi
description: >
  Comprehensive end-to-end Iranian medical and biomedical research proposal drafting, deep literature research,
  evidence synthesis, humanization, and Word (.docx) publication workflow (v6.0). Interactively clarifies scope
  and methodological ambiguities, executes a 15-stage Evidence-Driven Deep Research Engine across 4 databases
  (PubMed/MeSH, Europe PMC, OpenAlex, Crossref), generates granular 34-field Study Evidence Records (STUDY_EVIDENCE_RECORD.json),
  produces 20-column Evidence Matrices (EVIDENCE_MATRIX.csv & json), conducts 12-dimension pairwise Study Comparability Analysis
  (STUDY_COMPARABILITY_MATRIX.json), executes negative evidence searches across 6 categories with strict A-F contradiction taxonomy
  (CONTRADICTION_ANALYSIS.json, NEGATIVE_EVIDENCE_REPORT.md), constructs DAG Claim Dependency Graphs (CLAIM_DEPENDENCY_GRAPH.json)
  with 12 approved typed cross-study edges and mechanism chaining, conducts multi-dimensional claim certainty assessment across 7 dimensions,
  compiles 19-section Final Evidence Synthesis reports (FINAL_EVIDENCE_SYNTHESIS.md) with mathematically reconciled PRISMA 2020 accounting,
  performs true field-level bibliographic and honest author verification without fake fallbacks (FINAL_REFERENCE_VALIDITY_AUDIT.json),
  produces beautifully formatted Word documents featuring Dubai Persian typography, native RTL bidi XML (<w:bidi/>, <w:rtlGutter/>),
  Complex Script bolding (<w:bCs/>), zero divider dashes, and executes an automated 54-test behavioral self-audit suite (100% pass).
---

# Proposal-Nevisi (مهارت جامع نگارش پروپوزال‌های پژوهشی علوم پزشکی و موتور Deep Research v6.0)

این مهارت یک راهکار خودکار، تعاملی، پیشرفته و با استاندارد سخت‌گیرانه برای تدوین پروپوزال‌های پژوهشی علوم پزشکی و زیست‌پزشکی در بالاترین تراز دانشگاهی است که مجهز به موتور اختصاصی **Evidence-Driven Deep Research & Synthesis Engine v6.0** مبتنی بر شواهد پدیدارشده تجربی، بازیابی ۴ پایگاهی، اعتبارسنجی فیلد-محور کتابشناختی، ماتریس همسنجی ۱۲ بعدی مطالعات، تحلیل تناقضات بر مبنای تاکسونومی ۶ گانه A تا F، گراف جهت‌دار بدون دور (DAG) وابستگی ادعاها، حسابداری جریان PRISMA 2020، و سوئیت جامع ۵۴ آزمون خود-ممیزی رفتاری می‌باشد.

---

## اصول کلیدی و استانداردهای الزامی (Core Standards v6.0)

1. **معماری ۱۵ مرحله‌ای بازیابی و استخراج شواهد (The 15-Stage Evidence Funnel):**
   ```text
   Research Question
           ↓
   Evidence Questions (12 Categories: EQ01 - EQ12)
           ↓
   Concept / Synonym Expansion (MeSH & Controlled Vocabularies)
           ↓
   Search Facets (Direct Combination, Phytochemical, Oncolytic, Mechanistic, Methodological, Safety)
           ↓
   Multi-Database Retrieval (PubMed, Europe PMC, OpenAlex, Crossref)
           ↓
   Contradictory / Negative Evidence Search (6 Categories: Antagonism, Toxicity, Resistance, IFN, Solubility, Null)
           ↓
   Canonical Deduplication (DOI, PMID, Normalized Title)
           ↓
   Title & Abstract Screening (Explicit Audit Trail & Tier Segregation)
           ↓
   Full-Text Retrieval & Universal Audit (Tier A Full-Text vs Tier B Landscape)
           ↓
   Saturation-Based Citation Chaining (Marginal Yield Stopping Condition)
           ↓
   Study-Level Evidence Record Modeling (34 Structured Fields per Study)
           ↓
   Pairwise Study Comparability Analysis (12 Methodological Dimensions)
           ↓
   Contradiction Taxonomy Classification (Categories A to F, Zero Fake Direct Contradictions)
           ↓
   Claim Dependency Graph & Mechanism Chaining (DAG, Directed Edges, 12 Approved Typed Edges)
           ↓
   Final Evidence Synthesis & Master Word Document Compilation (19 Sections, Dubai RTL XML)
   ```

2. **قاعده کفایت شواهد و ممیزی کاربرد مراجع (Reference Usage & Zero Padding Policy):**
   - **تفکیک چهار شاخص کلیدی مراجع:**
     1. `Natural Selected References`: تعداد منابعی که بر پایه ضرورت شواهد و پوشش ادعاها به طور طبیعی انتخاب شده‌اند (بدون سقف و بدون اعمال هدف عددی).
     2. `Actually Cited Unique References`: تعداد منابع یکتا که واقعاً در بدنه متن پروپوزال با نشانگر استنادی معتبر (مانند `[1]` تا `[N]`) استناد شده‌اند (الزام: حداقل ۱۵ منبع، سقف نامحدود).
     3. `Unused Selected References`: تعداد منابعی که در فهرست مراجع وجود دارند ولی در متن پروپوزال استفاده نشده‌اند (خط قرمز: باید دقیقاً صفر باشد: `Unused Selected References == 0`).
     4. `Padding Added`: تعداد مقالاتی که صرفاً برای رسیدن به کف عددی افزوده شده‌اند (خط قرمز: باید دقیقاً صفر باشد: `Padding Added == 0`).
   - **کف مراجع یک دروازه سنجش کفایت است، نه هدف گزینش (Sufficiency Gate, Not a Selection Target):** الگوریتم گزینش ابتدا تمام منابعی را که واقعاً برای پوشش ادعاهای ضروری و حوزه‌های شواهد پروپوزال نیاز است به صورت طبیعی (Natural Evidence Selection) استخراج می‌کند؛ سپس در مرحله پایانی کفایت آن را با حداقل ۱۵ ارزیابی می‌نماید.
   - **ممنوعیت مطلق افزودن منبع برای رساندن به عدد:** افزودن هرگونه مقاله ضعیف یا اضافی صرفاً برای رساندن عدد به ۱۵ اکیداً غیرمجاز است.
   - **تعیین پدیدارشده منابع بدون سقف حداکثری:** هیچ سقفی (مانند ۱۵، ۲۰، ۳۰، ۵۰ یا ۸۰) برای تعداد مراجع نهایی وجود ندارد و در این طرح ۴۰ منبع با اعتبارسنجی کامل گزینش و استناد شده‌اند.

3. **مدل‌سازی شواهد در سطح مطالعه (Study Evidence Records with 34 Fields):**
   - تولید سند `STUDY_EVIDENCE_RECORD.json` که برای تک‌تک مطالعات واجد ۳۴ فیلد استاندارد است (شامل: `study_id`, `citation_number`, `doi`, `pmid`, `title`, `authors`, `journal`, `year`, `study_design`, `evidence_tier`, `evidence_type`, `in_vitro_in_vivo_boundary`, `model_system`, `organism_cell_line`, `sample_size_replicates`, `intervention_agent`, `control_agent`, `dose_concentration_range`, `exposure_duration`, `outcome_measures`, `primary_findings`, `quantitative_parameters`, `statistical_significance`, `chou_talalay_ci_extracted`, `synergy_interpretation`, `risk_of_bias`, `limitations_disclosed`, `funding_source`, `conflict_of_interest`, `claim_links`, `contradictory_search_category`, `synthesis_inclusion_status`, `data_extraction_date`, `extracted_by`).
   - تولید ماتریس شواهد در دو فرمت همگام `EVIDENCE_MATRIX.csv` و `EVIDENCE_MATRIX.json` با ۲۰ ستون یکپارچه.

4. **ارزیابی همسنجی مطالعات در ۱۲ بعد (Study Comparability Matrix):**
   - تولید سند `STUDY_COMPARABILITY_MATRIX.json` شامل تحلیل دوبه‌دوی مطالعات در ۱۲ بعد متدولوژیک:
     `model_system`, `cell_line_passage`, `agent_source_purity`, `vehicle_control`, `dose_range`, `exposure_duration`, `assay_readout`, `endpoint_timing`, `normalization_method`, `statistical_test`, `replicate_structure`, `serum_culture_conditions`.
   - دسته‌بندی زوج‌ها به `HIGH_COMPARABILITY`, `MODERATE_COMPARABILITY`, `LOW_COMPARABILITY`, `NOT_COMPARABLE`.

5. **موتور شواهد منفی و تاکسونومی تناقضات (Categories A to F):**
   - کاوش فعال در ۶ دسته شواهد متناقض و منفی:
     1. `ANTAGONISM_OR_SUBADDITIVITY`
     2. `HIGH_DOSE_TOXICITY_OFF_TARGET`
     3. `RESISTANCE_OR_NON_RESPONSIVENESS`
     4. `INTERFERON_INDUCED_VIRAL_CLEARANCE`
     5. `SOLUBILITY_BIOAVAILABILITY_LIMITS`
     6. `NEGATIVE_OR_NULL_FINDINGS`
   - تفکیک اکید بر مبنای تاکسونومی ۶ گانه در `CONTRADICTION_ANALYSIS.json` و `NEGATIVE_EVIDENCE_REPORT.md`:
     - **Category A (`A_DIRECT_CONTRADICTION`):** مداخله، مدل، دوز و زمان کاملاً یکسان با نتیجه متضاد (تنها این مورد تناقض مستقیم است).
     - **Category B (`B_CONTEXTUAL_DISAGREEMENT`):** تفاوت ناشی از رده سلولی، فرمولاسیون یا حلال.
     - **Category C (`C_NULL_RESULT`):** عدم حصول اثر یا توقف در غلظت‌های تحت‌کشنده.
     - **Category D (`D_DOSE_DEPENDENT_DIVERGENCE`):** تفاوت رفتار بیولوژیک در دوزهای پایین و بالا.
     - **Category E (`E_METHODOLOGICAL_DISAGREEMENT`):** تفاوت ناشی از روش یا آزمون سنجش.
     - **Category F (`F_TEMPORAL_PHASE_DISPARITY`):** تفاوت در سینتیک زمانی و نقاط خوانش.

6. **گراف وابستگی ادعاها و زنجیره مکانیسمی (Claim Dependency DAG & Mechanism Chaining):**
   - تدوین `CLAIM_DEPENDENCY_GRAPH.json` به عنوان یک گراف جهت‌دار بدون دور (DAG) فاقد هرگونه دور باطل.
   - زنجیره‌های مکانیسمی با تفکیک اکید گام‌های تأییدشده (`DIRECTLY_SUPPORTED`) از گام‌های فرضیه ترکیبی (`BIOLOGICALLY_PLAUSIBLE_HYPOTHESIS`).
   - یال‌های ارتباطی بین مطالعات بر مبنای ۱۲ نوع مجاز استاندارد (مانند `DIRECT_REPLICATION`, `CONCEPTUAL_REPLICATION`, `EXTENSION_TO_NEW_MODEL`, `PARAMETRIC_VARIATION`, `METHODOLOGICAL_DISAGREEMENT`, `SUBSTANTIVE_CONTRADICTION`, `MECHANISTIC_COMPLEMENT`, `UPSTREAM_DOWNSTREAM_PATHWAY`, `DOSE_REGIME_COMPARISON`, `HOST_VIRUS_INTERACTION_PARALLEL`, `SYNERGY_COMPONENT_VALIDATION`, `NEGATIVE_CONTROL_PARALLEL`).

7. **گزارش نهایی تلفیق شواهد در ۱۹ بخش و حسابداری PRISMA 2020:**
   - تدوین `FINAL_EVIDENCE_SYNTHESIS.md` در ۱۹ بخش ساختارمند استاندارد از خلاصه اجرایی تا بیانیه بازتولیدپذیری.
   - ثبت دقیق جریان شواهد در `PRISMA_SEARCH_ACCOUNTING.json` و `PRISMA_FLOW_DATA.json` با انطباق کامل ریاضی در تمام مراحل غربالگری و بازیابی.

8. **ممیزی کتابشناختی فیلد-محور و صحت‌سنجی نویسندگان (Field-Level Bibliographic & Honest Author Audit):**
   - ارزیابی مستقل فیلدهای DOI, PMID, Title, First Author, Journal, Year, Volume, Issue, Pages در `FINAL_REFERENCE_VALIDITY_AUDIT.json`.
   - موتور اعتبارسنجی صادقانه نویسندگان بدون ضریب ساختگی 0.8: ثبت وضعیت‌های `EXACT_AUTHOR_MATCH`, `FUZZY_AUTHOR_MATCH`, `AUTHOR_MISMATCH`, `AUTHOR_UNAVAILABLE`.

9. **سوئیت آزمونگر رفتاری ۵۴ گانه خود-ممیزی (54-Test Behavioral Self-Audit Suite v6.0):**
   - ممیزی سخت‌گیرانه شامل ۳۴ آزمون پیشین بعلاوه ۲۰ آزمون نوین رفتاری (Tests 35 to 54) که با اجرای `self_audit_suite.py` به وضعیت ۱۰۰٪ قبولی (54/54 PASS) دست می‌یابد.

---

## ساختار ابزارها و اسکریپت‌های اجرایی در مهارت

- **`scripts/study_evidence_engine.py`:** ساخت رکوردهای ۳۴ فیلدی و ماتریس شواهد ۲۰ ستونی.
- **`scripts/study_comparability.py`:** تحلیل همسنجی دوبه‌دوی مطالعات در ۱۲ بعد.
- **`scripts/contradiction_engine.py`:** کاوش شواهد منفی در ۶ دسته و طبقه‌بندی تاکسونومی A-F.
- **`scripts/evidence_graph_engine.py`:** مدل‌سازی گراف DAG، زنجیره مکانیسمی و یال‌های ۱۲ گانه.
- **`scripts/evidence_synthesis_engine.py`:** تدوین سند تلفیق شواهد در ۱۹ بخش و حسابداری PRISMA.
- **`scripts/reference_validity_auditor.py`:** ممیزی اعتبار کتابشناختی فیلد-محور و صحت نویسندگان.
- **`scripts/self_audit_suite.py`:** آزمونگر رفتاری ۵۴ گانه مستقل بر پایه داده‌های واقعی.
- **`scripts/sync_proposal_and_audit.py`:** خط لوله یکپارچه هماهنگ‌سازی، نگارش و اجرای ممیزی.
- **`scripts/docx_builder.py`:** کامپایل سند نهایی ورد با تایپوگرافی Dubai و تگ‌های native RTL bidi XML.
