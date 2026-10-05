import json
import sys
import os

sys.path.insert(0, os.path.abspath("scripts"))
from generate_compliant_proposal import ProposalGenerator

# Load audited portfolio
with open("FINAL_SELECTED_PORTFOLIO_AUDITED.json", "r", encoding="utf-8") as f:
    raw_portfolio = json.load(f)

selected_refs = raw_portfolio.get("selection", {}).get("selected_references", [])

for s in selected_refs:
    pmid_val = str(s.get("pmid", ""))
    cnum = s.get("citation_number", "")
    if pmid_val == "32329697":
        s["review_paragraph"] = (
            f"**Bhatt M و همکاران (2021)** در مطالعه‌ای تجربی بر روی سلول‌های آدنوکارسینومای ریه رده A549 [{cnum}]، به ارزیابی اثرات لوپئول طبیعی خالص پرداختند. "
            f"نکته کلیدی و تمایزبخش این مطالعه آن است که لوپئول در دوزهای غیرسمی تحت‌آزمون فاقد سمیت سلولی مستقیم (No Cytotoxic Effects) بر رده A549 بود، اما توانست به شکل معناداری مهاجرت و تهاجم سلولی را از طریق مهار فسفوریلاسیون مسیر MAPK/ERK و سرکوب مارکرهای گذار اپیتلیال-مزانشیمی (N-cadherin و Vimentin) مهار نماید. "
            f"این شواهد اثبات می‌کند که لوپئول خالص در غلظت‌های فیزیولوژیک عامل کشنده مستقیم نیست و نقش آن ضد مهاجرت است؛ لذا ترکیب آن با یک عامل فعال انکولیتیک نظیر ویروس نیوکاسل برای دستیابی همزمان به مهار رشد، انکولیز و آپوپتوز، از توجیه بیولوژیک بالایی برخوردار است [{cnum}]."
        )
    elif pmid_val == "41170972":
        s["review_paragraph"] = (
            f"**Zhao C و همکاران (2025)** در مطالعه‌ای پیرامون برهم‌کنش ویروس نیوکاسل و متابولیسم سلول‌های A549 [{cnum}]، نشان دادند که عفونت NDV موجب تغییرات ساختاری میتوکندری و استرس اکسیداتیو می‌گردد. با این حال، در سلول‌های A549 حضور ژن p53 نوع وحشی به عنوان ضربه‌گیر متابولیک عمل نموده و مانع از تخلیه سریع انرژی و سمیت سلولی ناشی از ROS می‌شود. "
            f"این یافته‌ها نشان‌دهنده تاب‌آوری متابولیک سلول‌های A549 در برابر انکولیز تک‌عاملی NDV بوده و نیاز به مداخله همزمان با ترکیباتی که مسیرهای بقای میتوکندریایی را مهار می‌کنند، توجیه می‌نماید [{cnum}]."
        )
    elif pmid_val == "41942850":
        s["review_paragraph"] = (
            f"**Sun Y و همکاران (2026)** با بهره‌گیری از آنالیز چندامیکسی یکپارچه (ترانسکریپتومیکس، پروتئومیکس و متابولومیکس) در سلول‌های A549 [{cnum}]، اثبات کردند که عفونت NDV متابولیسم گلیسروفسفولیپیدهای میزبان را بازآرایی کرده و مسیرهای بیوسنتز چربی را در جهت تسهیل همانندسازی ویروس هدایت می‌کند. "
            f"این داده‌های متابولومیک آسیب‌پذیری‌های زیستی سلول‌های آدنوکارسینوما را در مواجهه با عفونت ویروسی تبیین می‌سازند [{cnum}]."
        )

# Construct comprehensive proposal payload
proposal_data = {
    "research_title_fa": "بررسی اثرات همزمان و هم‌افزایی لوپئول و ویروس بیماری نیوکاسل بر میزان مهار رشد رده سلول سرطانی ریه (A549) در شرایط آزمایشگاهی",
    "research_title_en": "Evaluation of the Combined and Synergistic Effects of Lupeol and Newcastle Disease Virus on Growth Inhibition of Lung Cancer Cell Line (A549) In Vitro",
    "domain": "oncology",
    "framework": "EXPERIMENTAL_IN_VITRO",
    "research_problem_model": {
        "domain": "oncology",
        "framework": "EXPERIMENTAL_IN_VITRO",
        "problem_type": "MECHANISTIC_THERAPEUTIC",
        "target_condition": {
            "name_en": "Non-Small Cell Lung Cancer",
            "name_fa": "سرطان ریه سلول غیرکوچک (NSCLC)",
            "synonyms": ["NSCLC", "lung cancer", "lung adenocarcinoma", "A549", "carcinoma", "cancer", "tumor", "neoplasm", "adenocarcinoma"]
        },
        "population_or_model": {
            "primary_system": "A549 human lung adenocarcinoma cell line with normal BEAS-2B controls",
            "synonyms": ["A549", "lung cancer cell line", "NSCLC", "BEAS-2B", "in vitro", "cell culture", "adenocarcinoma"],
            "cell_lines": ["A549", "BEAS-2B"]
        },
        "interventions_or_exposures": [
            {
                "name": "Lupeol",
                "synonyms": ["lupeol", "triterpene", "pentacyclic triterpene", "triterpenoid", "lupene", "lupeol derivative"],
                "chemical_names": ["lupeol"]
            },
            {
                "name": "Newcastle Disease Virus",
                "synonyms": ["newcastle disease virus", "ndv", "oncolytic virus", "paramyxovirus", "oNDV", "rVSV-NDV"],
                "chemical_names": ["ndv"]
            }
        ],
        "comparison_group": {
            "name_fa": "مونوتراپی لوپئول، مونوتراپی ویروس نیوکاسل، کنترل حلال (DMSO <= 0.1%) و کنترل منفی درمان‌نشده",
            "name_en": "Lupeol monotherapy, NDV monotherapy, vehicle control (DMSO <= 0.1%), and untreated control"
        },
        "primary_outcomes": [
            {
                "name": "درصد مهار رشد و سمیت سلولی",
                "measurement_unit": "درصد مهار MTT نسبت به کنترل",
                "measurement_method": "اسپکتروفتومتری رنگ‌سنجی MTT در ۵۷۰ نانومتر",
                "synonyms": ["viability", "cytotoxicity", "growth inhibition", "mtt", "ic50", "cell survival", "proliferation"]
            },
            {
                "name": "شاخص ترکیب و هم‌افزایی فارماکولوژیک",
                "measurement_unit": "شاخص عددی CI بر مبنای اثر میانه چو-تالاتای",
                "measurement_method": "محاسبه کمی با الگوریتم چو-تالاتای در CompuSyn",
                "synonyms": ["chou-talalay", "synergy", "synergism", "combination index", "ci"]
            }
        ],
        "secondary_outcomes": [
            "شاخص تمایز و سمیت اختصاصی (Selectivity Index; SI > 2.0)",
            "نرخ القای آپوپتوز و فعال‌سازی کاسپاز-۳",
            "تغییر پتانسیل غشای میتوکندری"
        ],
        "hypothesized_mechanisms": [
            {
                "pathway_name": "apoptosis",
                "target_molecules": ["caspase", "caspase-3", "caspase-9", "bax", "bcl-2", "ros", "mitochondrial membrane potential", "akt", "mapk", "interferon"]
            }
        ]
    },

    "problem_statement_text": """سرطان ریه و به‌ویژه کارسینوم ریه سلول غیرکوچک (Non-Small Cell Lung Cancer; NSCLC) با منشأ آدنوکارسینوما، یکی از علل اصلی مرگ‌ومیر ناشی از بدخیمی‌ها در سراسر جهان است. سلول‌های آدنوکارسینومای ریه رده A549 به دلیل اختلالات ژنتیکی گسترده و فعال‌سازی مداوم مسیرهای بقای سلولی نظیر Akt/MAPK و فرار از آپوپتوز با واسطه اختلالات مسیر میتوکندریایی (Bax/Bcl-2)، پاسخ‌دهی درمانی محدودی به رژیم‌های رایج شیمی‌درمانی نشان می‌دهند و توسعه درمان‌های ترکیبی با مکانیسم‌های هم‌افزا اجتناب‌ناپذیر است.

لوپئول (Lupeol) به عنوان یک تری‌ترپنوئید پنج‌حلقه‌ای طبیعی با فرمول ساختاری لوپان، اثرات ضدتکثیری و پیش‌آپوپتوتیک متعددی را از طریق القای مسیر میتوکندریایی و مهار مسیرهای پیش‌تکثیری نشان داده است. با این حال، به دلیل آب‌گریزی بالا و محدودیت حلالیت زیستی، در شرایط برون‌تن (in vitro) نیازمند کنترل دقیق غلظت تا سقف ۸۰ میکرومولار و کنترل غلظت حلال DMSO در حد حداکثر ۰.۱ درصد حجمی می‌باشد. از سوی دیگر، ویروس بیماری نیوکاسل (Newcastle Disease Virus; NDV) یک پارامیکسو ویروس پرندگان با خاصیت انکولیتیک ذاتی در سلول‌های پستانداران است که با تکیه بر نقص مسیر پیام‌رسانی اینترفرون نوع یک (IFN-I) در سلول‌های توموری، تکثیر انتخابی یافته و از طریق تشکیل سین‌سیشیوم و تجزیه توموری آپوپتوز وابسته به کاسپاز را القا می‌کند.

ممیزی جامع پایگاه‌های داده علمی نشان می‌دهد که اثرات تک‌دارویی لوپئول و انکولیز NDV به صورت جداگانه در مدل‌های تجربی گزارش شده است. با این حال، در پایگاه‌ها، بازه زمانی، و راهبردهای جستجوی ثبت‌شده در این ممیزی، مطالعه تجربی مستقیمی که ترکیب همزمان Pure Lupeol و NDV را در A549 بررسی کرده باشد شناسایی نشد. لذا ارزیابی احتمال برهم‌کنش هم‌افزا (Synergism) صرفاً به عنوان یک فرضیه پژوهشی تجربی (Hypothesis) بر پایه آزمون‌های بیومتینیک کمی و معادله شاخص ترکیبی چو-تالاتای، در این طرح مورد آزمون قرار می‌گیرد.""",
    "studies": selected_refs
}


md_path = "MEDICAL_PROPOSAL_LUPEOL_NDV.md"
docx_path = "MEDICAL_PROPOSAL_LUPEOL_NDV.docx"

res = ProposalGenerator.generate_and_save(proposal_data, md_path, docx_path)
print("Proposal generation result:")
print("  Status:", res["status"])
print("  MD Path:", res["md_path"])
print("  DOCX Path:", res["docx_path"])
print("  Validation details:", json.dumps(res["validation"], indent=2, ensure_ascii=False))
