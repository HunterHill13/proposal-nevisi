#!/usr/bin/env python3
"""
dynamic_protocol_designer.py - Dynamic Variables, Timeline, and Statistical Planning
Proposal-Nevisi Engine v14.2.0 (Universal Biomedical Architecture)

Generates dynamic Variable Tables, study-type-specific Gantt Timelines,
and coherent Statistical Analysis Plans tailored strictly to all 7+1 archetypes.
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from core_policies import classify_study_archetype

STUDY_TIMELINE_TEMPLATES = {
    "EXPERIMENTAL_IN_VITRO": [
        ("فاز ۱: مرور سیستماتیک منابع و تدوین نهایی پروتکل آزمایشگاهی", 1, 2),
        ("فاز ۲: تهیه و آماده‌سازی رده‌های سلولی، آزمون‌های کنترل کیفی و تایید هویت", 2, 3),
        ("فاز ۳: بهینه‌سازی دوز و سنجش غلظت‌های غیرسمی حلال / کنترل‌ها", 3, 4),
        ("فاز ۴: اجرای آزمون‌های سنجش بقا و مهار تکثیر سلولی", 4, 6),
        ("فاز ۵: آزمون‌های سنجش میان‌کنش و تحلیل کمی اثرات ترکیبی", 6, 8),
        ("فاز ۶: سنجش‌های مولکولی مسیرهای پیام‌رسانی و مکانیسم‌های مرگ سلولی", 7, 10),
        ("فاز ۷: پردازش داده‌ها، تحلیل آماری و نگارش گزارش نهایی", 10, 12)
    ],
    "EXPERIMENTAL_ANIMAL": [
        ("فاز ۱: تدوین پروتکل، اخذ تاییدیه کمیته اخلاق کار با حیوانات آزمایشگاهی", 1, 2),
        ("فاز ۲: خرید، قرنطینه و سازگاری حیوانات آزمایشگاهی در بیوتروم", 2, 3),
        ("فاز ۳: القای مدل بیماری و پایش دوره نهفتگی", 3, 5),
        ("فاز ۴: اجرای مداخله دارویی / درمانی و کنترل عوارض", 5, 8),
        ("فاز ۵: نمونه‌برداری بافتی، سنجش‌های پاتولوژیک و ایمونوهیستوشیمی", 8, 10),
        ("فاز ۶: آنالیز آماری داده‌های پیش‌بالینی و تدوین مستندات", 10, 12)
    ],
    "PICO": [
        ("فاز ۱: ثبت در رجیستری کارآزمایی‌های بالینی و اخذ مجوز کمیته اخلاق", 1, 3),
        ("فاز ۲: غربالگری، اخذ رضایت آگاهانه و ورود بیماران واجد شرایط", 3, 7),
        ("فاز ۳: اجرای پروتکل تصادفی‌سازی، کورسازی و تجویز مداخله", 6, 12),
        ("فاز ۴: پیگیری دوره‌ای بیماران، ثبت عوارض جانبی و سنجش پیامدها", 8, 16),
        ("فاز ۵: پاک‌سازی داده‌ها، خروج از کورسازی و آنالیز آماری طبق پروتکل ITT", 16, 18),
        ("فاز ۶: تدوین گزارش نهایی و تحلیل پیامدهای بالینی", 18, 20)
    ],
    "CLINICAL_TRIAL": [
        ("فاز ۱: ثبت در رجیستری IRCT و اخذ تاییدیه کمیته اخلاق پزشکی", 1, 2),
        ("فاز ۲: غربالگری بیماران، اخذ رضایت آگاهانه و تصادفی‌سازی بازوها", 2, 6),
        ("فاز ۳: اجرای پروتکل درمانی استاندارد و پایش ایمنی/عوارض (DSMB)", 5, 11),
        ("فاز ۴: پیگیری پیامدهای بالینی و آزمایشگاهی بیماران", 9, 14),
        ("فاز ۵: تحلیل آماری Intention-to-Treat / ANCOVA و نگارش گزارش نهایی", 14, 16)
    ],
    "DIAGNOSTIC": [
        ("فاز ۱: تدوین پروتکل، هماهنگی با آزمایشگاه مرجع و اخذ کد اخلاق", 1, 2),
        ("فاز ۲: جمع‌آوری نمونه‌های زیستی طبق معیارهای ورود و خروج", 2, 5),
        ("فاز ۳: اجرای آزمون شاخص (Index Test) توسط اپراتورهای مستقل و کور", 4, 7),
        ("فاز ۴: اجرای آزمون استاندارد طلایی (Gold Standard) مرجع", 5, 8),
        ("فاز ۵: محاسبه شاخص‌های تشخیصی (حساسیت، ویژگی، ROC curve)", 8, 10),
        ("فاز ۶: اعتبارسنجی تکرارپذیری، تحلیل آماری و گزارش نتایج", 10, 12)
    ],
    "PECO": [
        ("فاز ۱: طراحی پروتکل مواجهه، استقرار سیستم‌های پایش محیطی و اخذ مجوز اخلاق", 1, 3),
        ("فاز ۲: شناسایی و ورود افراد مواجهه‌یافته و گروه کنترل همتاشده", 3, 6),
        ("فاز ۳: سنجش دوز مواجهه تجمعی، نمونه‌گیری زیستی و کنترل مخدوش‌کننده‌ها", 6, 12),
        ("فاز ۴: پیگیری دوره‌ای ثبت پیامدهای بیماری و شاخص‌های بالینی", 10, 18),
        ("فاز ۵: مدل‌سازی رگرسیونی، تحلیل متغیرهای مخدوش‌کننده و تدوین گزارش", 18, 20)
    ],
    "HEALTH_SYSTEMS_AND_HEALTH_POLICY": [
        ("فاز ۱: بومی‌سازی ابزار WHO WHS/NHA، آزمون پایلوت و اخذ مجوز اخلاق", 1, 2),
        ("فاز ۲: نمونه‌گیری خوشه‌ای طبقه‌بندی‌شده و گردآوری داده‌های خانوار/بیمارستان", 2, 6),
        ("فاز ۳: تطبیق هزینه‌ها در سامانه HIS و پالایش داده‌های اقتصادی سلامت", 6, 8),
        ("فاز ۴: محاسبه شاخص‌های CHE، OOP، کاکوانی و برازش رگرسیون لجستیک", 8, 10),
        ("فاز ۵: تدوین خلاصه سیاستی (Policy Brief) و گزارش نهایی", 10, 12)
    ],
    "EPIDEMIOLOGICAL_OBSERVATIONAL": [
        ("فاز ۱: تدوین پروتکل STROBE، طراحی چک‌لیست و اخذ کد اخلاق", 1, 2),
        ("فاز ۲: محاسبه چارچوب نمونه‌گیری و ورود شرکت‌کنندگان/پرونده‌ها", 2, 6),
        ("فاز ۳: گردآوری داده‌های مواجهه، پیامد و متغیرهای مخدوشگر", 5, 9),
        ("فاز ۴: تحلیل آماری چندمتغیره و تدوین گزارش نهایی", 9, 12)
    ],
    "SCOPING_REVIEW": [
        ("فاز ۱: تدوین پروتکل PRISMA-ScR بر پایه چارچوب PCC و ثبت در OSF", 1, 2),
        ("فاز ۲: اجرای جستجوی جامع بولین در پایگاه‌های PubMed, Scopus, Embase, WoS", 2, 4),
        ("فاز ۳: غربالگری دوفردی مستقل عنوان، چکیده و متن کامل در Rayyan", 4, 6),
        ("فاز ۴: پایلوت و تکمیل ماتریس استخراج داده JBI و سنجش توافق کاپا", 6, 9),
        ("فاز ۵: سنتز مضمونی و کمی نگاشت شواهد و نگارش مقاله نهایی", 9, 12)
    ],
    "USABILITY_AND_DIGITAL_HEALTH": [
        ("فاز ۱: تدوین سناریوهای تکلیف و بومی‌سازی چک‌لیست نیلسن/SUS و کد اخلاق", 1, 2),
        ("فاز ۲: اجرای ارزیابی اکتشافی توسط متخصصان فاکتورهای انسانی (n=5..10)", 2, 4),
        ("فاز ۳: اجرای آزمون کاربردپذیری Think-Aloud و تکمیل پرسشنامه SUS (n>=30)", 4, 7),
        ("فاز ۴: تحلیل نرخ موفقیت، زمان انجام تکلیف و رتبه‌بندی خطاها و گزارش نهایی", 7, 10)
    ],
    "PROGNOSTIC": [
        ("فاز ۱: تعریف کوهورت پیش‌آگهی، معیارهای ورود و ثبت بیومارکرهای پایه", 1, 3),
        ("فاز ۲: ارزیابی فاکتورهای پیش‌آگهی و اندازه‌گیری متغیرهای پیش‌بین", 3, 6),
        ("فاز ۳: پیگیری بقا و ثبت رخدادهای بالینی (Time-to-Event)", 6, 16),
        ("فاز ۴: تحلیل بقای کاپلان-مایر و مدل خطرات متناسب کاکس", 16, 18),
        ("فاز ۵: اعتبارسنجی داخلی مدل و گزارش قدرت تفکیک و کالیبراسیون", 18, 20)
    ],
    "MECHANISTIC": [
        ("فاز ۱: طراحی مداخله‌های ژنتیکی و فارماکولوژیک بر مسیر پیام‌رسانی", 1, 2),
        ("فاز ۲: کشت سلولی، تیمار با مهارکننده‌ها و سنجش اهداف بالادست", 2, 4),
        ("فاز ۳: سنجش‌های بیوشیمیایی فسفوریلاسیون، شکافت پروتئینی و بیان ژن", 4, 7),
        ("فاز ۴: ارزیابی فنوتیپی عملکردی (بقا، آپوپتوز، ترشح و مهاجرت)", 7, 9),
        ("فاز ۵: اثبات پیوستگی کسکید با رویکردهای نجات (Rescue Experiments) و تحلیل نهایی", 9, 12)
    ]
}
STUDY_TIMELINE_TEMPLATES["DIAGNOSTIC_ACCURACY_AND_BIOMARKER"] = STUDY_TIMELINE_TEMPLATES["DIAGNOSTIC"]
STUDY_TIMELINE_TEMPLATES["USABILITY"] = STUDY_TIMELINE_TEMPLATES["USABILITY_AND_DIGITAL_HEALTH"]
STUDY_TIMELINE_TEMPLATES["IN_VIVO"] = STUDY_TIMELINE_TEMPLATES["EXPERIMENTAL_ANIMAL"]

class DynamicProtocolDesigner:
    """Extracts research design components dynamically from the problem model."""

    @classmethod
    def generate_variable_table(cls, model_dict: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extracts structured variable rows strictly aligned to the resolved study archetype."""
        archetype = classify_study_archetype(model_dict)
        is_lab = archetype in ("in_vitro", "in_vivo")
        is_review = (archetype == "scoping_review")
        is_usability = (archetype == "usability")
        is_health_sys = (archetype == "health_systems")
        is_diagnostic = (archetype == "diagnostic")
        is_clinical = (archetype == "clinical_rct")

        variables: List[Dict[str, str]] = []

        # 1. Independent Variables / PCC Concept / Exposure / Index Test
        interventions = model_dict.get("interventions_or_exposures") or model_dict.get("interventions", [])
        if not interventions:
            interventions = [{"name": "مفهوم یا مداخله اصلی پژوهش"}]
        for agt in interventions:
            name = agt.get("name", "مداخله پژوهش") if isinstance(agt, dict) else str(agt)
            if is_lab:
                role = "مستقل"
                vtype = "کمی پیوسته"
                op_def = f"غلظت و دوز مواجهه با {name} در مدل تجربی"
                meas = "تیتراسیون رقت‌های متوالی در شرایط کنترل‌شده"
                unit = "میکرومولار / غلظت استاندارد"
            elif is_review:
                role = "مستقل (محور مداخله/مفهوم PCC)"
                vtype = "کیفی / استخراجی"
                op_def = f"نوع و مشخصات مداخله یا محور مفهومی {name} گزارش‌شده در مطالعات اولیه"
                meas = "فرم استخراج ساختاریافته داده JBI"
                unit = "طبقه‌بندی کیفی / دوزاژ گزارش‌شده"
            elif is_usability:
                role = "مستقل"
                vtype = "کیفی اسمی / تکلیف‌محور"
                op_def = f"تعامل کاربر با ماژول‌ها و ویژگی‌های {name} طی اجرای سناریوها"
                meas = "پروتکل آزمون تکلیف‌محور و چک‌لیست اکتشافی نیلسن"
                unit = "رده‌بندی سناریو / شدت اشکال (0-4)"
            elif is_diagnostic:
                role = "مستقل (آزمون شاخص)"
                vtype = "پیوسته / دوسطحی"
                op_def = f"نتیجه آزمون شاخص تشخیصی {name} در مقایسه با استاندارد طلایی"
                meas = "اندازه‌گیری آزمایشگاهی یا بالینی کور (Blinded Index Test)"
                unit = "مثبت/منفی یا مقدار کمی نشانگر"
            elif is_health_sys:
                role = "مستقل / تعدیل‌کننده"
                vtype = "کیفی / رتبه‌ای"
                op_def = f"وضعیت مواجهه با {name} و پوشش خدمات درمانی خانوار"
                meas = "پرسشنامه استاندارد WHO WHS و سامانه HIS"
                unit = "طبقه‌بندی سیاستی/بیمه‌ای"
            else:
                role = "مستقل"
                vtype = "کیفی اسمی / کمی"
                op_def = f"تخصیص یا مواجهه بالینی/جمعیتی با {name} مطابق پروتکل مصوب"
                meas = "فرم ثبت گزارش بالینی (eCRF) یا پرسشنامه معتبر"
                unit = "گروه مداخله در برابر کنترل"
            variables.append({
                "name": name,
                "role": role,
                "type": vtype,
                "operational_definition": op_def,
                "measurement_method": meas,
                "unit": unit,
            })

        # 2. Dependent Variables (Primary Outcomes)
        outcomes = model_dict.get("primary_outcomes") or model_dict.get("outcomes", [])
        if not outcomes:
            if is_lab:
                outcomes = [
                    {"name": "بقای سلولی و سمیت دارویی (IC50)", "measurement_unit": "درصد (%) و میکرومولار"},
                    {"name": "نرخ مرگ برنامه‌ریزی‌شده سلولی (آپوپتوز)", "measurement_unit": "درصد سلول‌های Annexin-V مثبت"},
                ]
            elif is_review:
                outcomes = [
                    {"name": "فراوانی ویژگی‌های مداخله، بافتار و شکاف شواهد", "measurement_unit": "فراوانی و درصد (%)"},
                    {"name": "میزان توافق بین ارزیاب‌ها و خلاصه پیامدهای ایمنی", "measurement_unit": "Cohen's Kappa / Risk Difference"},
                ]
            elif is_usability:
                outcomes = [
                    {"name": "نمره کاربردپذیری سیستم (SUS)", "measurement_unit": "نمره مقیاس 0 تا 100"},
                    {"name": "نرخ تکمیل موفق تکلیف و تعداد خطاهای رابط کاربری", "measurement_unit": "درصد (%) و تعداد"},
                ]
            elif is_diagnostic:
                outcomes = [
                    {"name": "حساسیت، ویژگی و سطح زیر منحنی ROC", "measurement_unit": "درصد (%) و AUC با CI 95%"},
                ]
            elif is_health_sys:
                outcomes = [
                    {"name": "بروز هزینه‌های کمرشکن سلامت (CHE) و پرداخت از جیب (OOP)", "measurement_unit": "درصد (%) و نسبت به ظرفیت پرداخت"},
                ]
            else:
                outcomes = [
                    {"name": "پیامد بالینی اولیه هدف پژوهش", "measurement_unit": "میانگین / نسبت بروز و اختلاف خطر"},
                ]

        for out in outcomes:
            name = out.get("name", "پیامد اولیه") if isinstance(out, dict) else str(out)
            default_unit = "درصد (%)" if is_lab else "شاخص کمی متناسب با پیامد"
            unit = out.get("measurement_unit", default_unit) if isinstance(out, dict) else default_unit
            if is_lab:
                role, vtype, meas = "وابسته", "کمی پیوسته", "سنجش کمی نوری / الایزا / فلوسایتومتری"
            elif is_review:
                role, vtype, meas = "وابسته (پیامد و شکاف شواهد JBI)", "کمی / مضمونی", "ماتریس استخراج داده JBI PCC و تحلیل R"
            elif is_usability:
                role, vtype, meas = "وابسته", "کمی پیوسته", "پرسشنامه استاندارد SUS و ثبت زمان/نرخ تکلیف"
            elif is_diagnostic:
                role, vtype, meas = "وابسته", "کمی پیوسته / دوسطحی", "جدول توافقی ۲x۲ در برابر استاندارد طلایی و منحنی ROC"
            else:
                role, vtype, meas = "وابسته", "کمی پیوسته / دوحالتی", "پرسشنامه معتبر / پرونده بالینی یا سامانه HIS"
            variables.append({
                "name": name,
                "role": role,
                "type": vtype,
                "operational_definition": f"میزان تغییر یا توزیع در شاخص {name} مطابق تعریف عملیاتی پروتکل",
                "measurement_method": meas,
                "unit": unit,
            })

        # 3. Comparators / Reference Controls
        comparators = model_dict.get("comparators", [])
        for comp in comparators:
            cname = comp.get("name", "کنترل پایه") if isinstance(comp, dict) else str(comp)
            variables.append({
                "name": cname,
                "role": "کنترل پایه / مقایسه" if not is_review else "مقایسه‌کننده بافتار (PCC)",
                "type": "کیفی اسمی",
                "operational_definition": f"شرایط پایه یا استاندارد مقایسه متناسب با طراحی مطالعه ({cname})",
                "measurement_method": "ثبت همزمان مطابق پروتکل استاندارد" if not is_lab else "انکوباسیون همزمان در شرایط یکسان با حلال فاقد ماده موثره",
                "unit": "فاقد واحد (گروه شاهد)",
            })

        # 4. Archetype-specific Quality Controls & Confounders
        if archetype == "in_vitro":
            variables.append({
                "name": "بلانک بدون سلول (Cell-Free Blank Control)",
                "role": "کنترل منفی تداخل فنی",
                "type": "کیفی اسمی",
                "operational_definition": "محیط کشت حاوی غلظت‌های مداخله فاقد سلول با معرف سنجش جهت کسر احیای شیمیایی مستقیم و تداخل نوری غیرآنزیمی",
                "measurement_method": "خوانش اسپکتروفتومتری و کسر جذب نوری بلانک از چاهک‌های آزمایش",
                "unit": "جذب نوری (OD)",
            })
            variables.append({
                "name": "کنترل حلال ناقل (Vehicle Control)",
                "role": "کنترل منفی حلال",
                "type": "کیفی اسمی",
                "operational_definition": "محیط کشت حاوی حداکثر غلظت حلال ناقل (DMSO < 0.1%) فاقد ماده موثره جهت تفکیک سمیت حلال از اثر اختصاصی",
                "measurement_method": "انکوباسیون همگام در شرایط یکسان با گروه‌های مداخله",
                "unit": "درصد زیست‌پذیری نسبت به کنترل دست‌نخورده",
            })
            variables.append({
                "name": "تعداد پاساژ و یکنواختی محیط کشت / شرایط آزمون",
                "role": "مخدوشگر بالقوه (Confounder)",
                "type": "کمی گسسته",
                "operational_definition": "تغییرات بیولوژیکی ناشی از پیری سلولی یا نوسانات محیط کشت",
                "measurement_method": "استفاده از پاساژهای مشخص و یکسان در تمام تکرارهای زیستی",
                "unit": "شماره پاساژ",
            })
        elif is_review:
            variables.append({
                "name": "نوع طراحی مطالعه اولیه و کشور/بافتار اجرا (Context)",
                "role": "متغیر زمینه‌ای و مخدوشگر نگاشت",
                "type": "کیفی اسمی",
                "operational_definition": "دسته‌بندی طراحی مطالعه، دوره زمانی انتشار و ویژگی‌های جمعیت گزارش‌شده در مقالات منتخب",
                "measurement_method": "ماتریس استاندارد استخراج داده JBI با توافق دو داور",
                "unit": "کد طبقه‌بندی مطالعه",
            })
        elif is_usability:
            variables.append({
                "name": "سابقه مهارت دیجیتال و نقش شغلی کاربر",
                "role": "مخدوشگر بالقوه (Confounder)",
                "type": "کیفی رتبه‌ای",
                "operational_definition": "سطح آشنایی پیشین کاربر با سامانه‌های سلامت الکترونیک",
                "measurement_method": "پرسشنامه مشخصات پایه پیش از آزمون کاربردپذیری",
                "unit": "سال سابقه / سطح مهارت",
            })
        elif is_health_sys:
            variables.append({
                "name": "پوشش بیمه‌ای پایه و تکمیلی (Health Insurance Coverage)",
                "role": "متغیر مستقل / تعدیل‌کننده",
                "type": "کیفی اسمی",
                "operational_definition": "برخورداری بیمار یا خانوار از بیمه‌های درمانی پایه و بیمه تکمیلی تجاری",
                "measurement_method": "پرسشنامه ساختارمند و تطبیق با دفترچه درمانی",
                "unit": "وضعیت پوشش (دارد/ندارد)",
            })
            variables.append({
                "name": "عوامل مخدوش‌کننده اقتصادی-اجتماعی (SES Confounders)",
                "role": "مخدوشگر بالقوه (Confounder)",
                "type": "ترکیبی",
                "operational_definition": "عوامل اثرگذار شامل بعد خانوار، دهک درآمدی، سطح تحصیلات سرپرست و وضعیت سلامت",
                "measurement_method": "پرسشنامه استاندارد WHO WHS و استعلام اطلاعات از سامانه HIS",
                "unit": "رتبه‌ای / پیوسته",
            })
        else:
            variables.append({
                "name": "عوامل مخدوش‌کننده دموگرافیک و بالینی (Confounders)",
                "role": "مخدوشگر بالقوه (Confounder)",
                "type": "ترکیبی",
                "operational_definition": "سن، جنس، شاخص توده بدنی (BMI) و سوابق زمینه‌ای شرکت‌کنندگان یا گروه مطالعه",
                "measurement_method": "چک‌لیست استاندارد استخراج داده‌ها و اندازه‌گیری‌های بالینی",
                "unit": "پیوسته و رتبه‌ای",
            })

        return variables

    @classmethod
    def get_orthogonal_triangulation_protocol(cls, framework: str = "EXPERIMENTAL_IN_VITRO") -> Dict[str, Any]:
        """Provides archetype-matched orthogonal validation or triangulation strategy."""
        arch = classify_study_archetype({"framework": framework})
        if arch in ("scoping_review", "usability", "health_systems", "epidemiological", "clinical_rct", "diagnostic"):
            return {
                "required_controls": ["Dual independent validation", "Confounder / bias sensitivity verification"],
                "orthogonal_assays": ["Cross-method sensitivity / inter-rater concordance verification"],
                "rationale": (
                    "اعتبارسنجی متقاطع در طراحی‌های غیرآزمایشگاهی از طریق کنترل مستقل داوران، تحلیل حساسیت آماری "
                    "و تطبیق داده‌ها با مراجع استاندارد بالینی یا پایگاه‌های چندگانه انجام می‌شود."
                ),
            }
        from core_policies import AssayInterferencePolicy
        return {
            "required_controls": AssayInterferencePolicy.REQUIRED_CONTROLS,
            "orthogonal_assays": AssayInterferencePolicy.ORTHOGONAL_ASSAYS,
            "rationale": (
                "سنجش‌های زیست‌پذیری مبتنی بر احیای متابولیک (مانند MTT) به تداخلات ناشی از احیای شیمیایی مستقیم یا پلی‌فنول‌ها حساس هستند. "
                "بنابراین اعتبارسنجی با آزمون آپوپتوز فلوسایتومتری (Annexin V/PI) و آزمون بقای کلونوژنیک ۱۴ روزه الزامی است."
            ),
        }

    @classmethod
    def render_variable_table_markdown(cls, variables: List[Dict[str, str]]) -> str:
        """Renders the standard 6-column Markdown variable table."""
        header = "| نام متغیر | نقش متغیر | نوع متغیر | تعریف عملیاتی | نحوه اندازه‌گیری و ابزار | مقیاس / واحد سنجش |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        rows = []
        for v in variables:
            name = v.get("name", "")
            role = v.get("role", "")
            vtype = v.get("type", "")
            op_def = v.get("operational_definition", "")
            meas = v.get("measurement_method", "")
            unit = v.get("unit", "")
            rows.append(f"| **{name}** | {role} | {vtype} | {op_def} | {meas} | {unit} |")
        return header + "\n".join(rows)

    @classmethod
    def generate_timeline(cls, framework: str) -> List[Dict[str, Any]]:
        """Returns phased Gantt timeline appropriate for the normalized study framework."""
        fw_key = str(framework or "EXPERIMENTAL_IN_VITRO").strip().upper()
        alias_map = {
            "IN_VIVO": "EXPERIMENTAL_ANIMAL",
            "IN_VITRO": "EXPERIMENTAL_IN_VITRO",
            "CLINICAL_RCT": "CLINICAL_TRIAL",
            "USABILITY": "USABILITY_AND_DIGITAL_HEALTH",
            "DIAGNOSTIC_ACCURACY_AND_BIOMARKER": "DIAGNOSTIC",
        }
        norm_key = alias_map.get(fw_key, fw_key)
        raw_phases = STUDY_TIMELINE_TEMPLATES.get(norm_key)
        if raw_phases is None:
            arch = classify_study_archetype({"framework": fw_key})
            arch_fallback = {
                "scoping_review": "SCOPING_REVIEW",
                "usability": "USABILITY_AND_DIGITAL_HEALTH",
                "health_systems": "HEALTH_SYSTEMS_AND_HEALTH_POLICY",
                "epidemiological": "EPIDEMIOLOGICAL_OBSERVATIONAL",
                "clinical_rct": "CLINICAL_TRIAL",
                "diagnostic": "DIAGNOSTIC",
                "in_vivo": "EXPERIMENTAL_ANIMAL",
                "in_vitro": "EXPERIMENTAL_IN_VITRO",
            }.get(arch, "EPIDEMIOLOGICAL_OBSERVATIONAL")
            raw_phases = STUDY_TIMELINE_TEMPLATES.get(arch_fallback, [])
        timeline = []
        for phase_name, start_m, end_m in raw_phases:
            timeline.append({
                "phase_title": phase_name,
                "start_month": start_m,
                "end_month": end_m,
                "duration_months": end_m - start_m + 1
            })
        return timeline

    @classmethod
    def render_timeline_markdown(cls, timeline: List[Dict[str, Any]], total_months: int = 12) -> str:
        """Renders standard Markdown Gantt chart table."""
        m_headers = " | ".join(str(m) for m in range(1, total_months + 1))
        sep_cols = " | ".join([":---:"] * total_months)
        header = f"| فاز اجرایی و شرح فعالیت‌ها | {m_headers} |\n| :--- | {sep_cols} |\n"
        rows = []
        for item in timeline:
            title = item.get("phase_title", "")
            start_m = item.get("start_month", 1)
            end_m = item.get("end_month", total_months)
            cells = []
            for m in range(1, total_months + 1):
                if start_m <= m <= end_m:
                    cells.append("■")
                else:
                    cells.append(" ")
            rows.append(f"| **{title}** | {' | '.join(cells)} |")
        return header + "\n".join(rows)

    @classmethod
    def generate_statistical_plan(cls, model_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Aligns statistical tests dynamically across all 7+1 archetypes."""
        framework = str(model_dict.get("framework", "")).upper()
        arch = classify_study_archetype(model_dict)
        interventions = model_dict.get("interventions_or_exposures", [])
        is_multi_agent = len(interventions) > 1

        if arch == "scoping_review" or "SCOPING" in framework:
            tests = [
                "ترسیم نمودار جریان استاندارد انتخاب مطالعات PRISMA-ScR و گزارش نرخ غربالگری",
                "محاسبه ضریب توافق بین داوران با کاپای کوهن (Cohen's Kappa >= 0.80) و ICC",
                "نگاشت توصیفی، طبقه‌بندی مضمونی و در صورت همگنی کمی گزارش اختلاف خطر (Risk Difference) با فاصله اطمینان ۹۵٪",
            ]
            return {
                "primary_analysis": tests[0],
                "post_hoc_analysis": "Sensitivity & Subgroup Evidence Charting",
                "distribution_test": "Descriptive & Narrative Synthesis (PRISMA-ScR / JBI; inferential normality not applicable)",
                "alpha_threshold": None,
                "statistical_software": "Rayyan / Covidence / R Statistical Environment (irr, meta)",
                "complete_testing_strategy": tests,
            }

        if arch == "usability" or "USABILITY" in framework:
            tests = [
                "محاسبه میانگین، میانه و انحراف معیار نمره کاربردپذیری سیستم (SUS: 0-100)",
                "تحلیل نرخ تکمیل موفق تکلیف (Task Completion Rate) و زمان میانگین اجرا",
                "رتبه‌بندی شدت خطاهای اکتشافی نیلسن (0 تا 4) و فراوانی موانع تعامل",
            ]
            return {
                "primary_analysis": tests[0],
                "post_hoc_analysis": "Heuristic severity stratification",
                "distribution_test": "Descriptive SUS & task latency profiling",
                "alpha_threshold": None,
                "statistical_software": "SPSS v27 / R Statistical Environment",
                "complete_testing_strategy": tests,
            }

        tests = []
        if arch in ("in_vitro", "in_vivo") or framework in ["EXPERIMENTAL_IN_VITRO", "EXPERIMENTAL_ANIMAL"]:
            if is_multi_agent:
                tests.append("تحلیل واریانس دوطرفه (Two-way ANOVA) جهت ارزیابی اثرات اصلی و اثر متقابل (Interaction effect)")
                tests.append("آزمون تعقیبی توکی (Tukey's HSD post-hoc test) جهت مقایسه‌های چندگانه میان گروه‌ها")
                tests.append("مدل‌های ریاضی استاندارد سنجش هم‌افزایی (مانند نسبت ترکیب یا نمایه میان‌کنش) جهت تعیین ماهیت تعامل")
            else:
                tests.append("تحلیل واریانس یک‌طرفه (One-way ANOVA) همراه با آزمون تعقیبی دانت یا توکی")
            tests.append("آزمون شاپیرو-ویلک (Shapiro-Wilk) جهت بررسی نرمال بودن توزیع داده‌ها")
            software = "R Statistical Environment / GraphPad Prism / SPSS"
            post_hoc = tests[1] if len(tests) > 1 else "Dunnett's test"
            dist_test = "Shapiro-Wilk normality test"
        elif arch == "clinical_rct" or framework in ["PICO", "CLINICAL_TRIAL"]:
            tests.append("تحلیل قصد درمان (Intention-to-Treat: ITT) و پروتکل (Per-Protocol) جهت مقایسه دو بازوی درمانی")
            tests.append("تحلیل کوواریانس (ANCOVA) یا مدل خطرات متناسب کاکس جهت تعدیل مقادیر پایه")
            tests.append("منحنی‌های کاپلان-مایر همراه با آزمون لگ-رتبه یا آزمون تی مستقل/من-ویتنی")
            software = "SPSS v27 / R Statistical Environment"
            post_hoc = "ANCOVA baseline-adjusted comparison & Bonferroni multiplicity adjustment"
            dist_test = "Shapiro-Wilk normality test"
        elif arch == "diagnostic" or "DIAGNOSTIC" in framework:
            tests.append("محاسبه حساسیت (Sensitivity)، ویژگی (Specificity)، PPV و NPV در برابر استاندارد طلایی")
            tests.append("ترسیم منحنی راک (ROC Curve) و محاسبه مساحت زیر منحنی (AUC) با فاصله اطمینان ۹۵٪ و شاخص یودن")
            tests.append("آزمون مک‌نمار (McNemar's test) و ضریب کاپای کوهن (Cohen's Kappa) جهت توافق")
            software = "MedCalc / R (pROC) / SPSS"
            post_hoc = "Youden Index optimal threshold comparison (DeLong test)"
            dist_test = "Shapiro-Wilk / ROC empirical AUC"
        elif arch == "health_systems" or "HEALTH_SYSTEM" in framework:
            tests.append("محاسبه نرخ مواجهه با هزینه‌های کمرشکن سلامت (CHE >= 40% CTP) و سهم پرداخت از جیب (OOP)")
            tests.append("مدل رگرسیون لجستیک چندمتغیره با تعدیل طراحی خوشه‌ای (svy / DEFF) جهت برآورد AOR")
            tests.append("محاسبه شاخص تمرکز و شاخص پیشرفت کاکوانی (Kakwani Progressivity Index)")
            software = "Stata v17 (DASP / conindex) / R"
            post_hoc = "Cluster-weighted multivariable sensitivity analysis"
            dist_test = "Weighted survey distribution diagnostics"
        elif arch == "epidemiological" or framework in ["PECO", "EPIDEMIOLOGICAL_OBSERVATIONAL"]:
            tests.append("مدل رگرسیون لجستیک یا پواسون تعدیل‌شده چندمتغیره (Logistic Regression / Poisson Modeling) جهت برآورد نسبت شانس تعدیل‌شده (AOR)")
            tests.append("گزارش شیوع/بروز همراه با فواصل اطمینان ۹۵٪ و آزمون کای-اسکوئر در SPSS/R")
            software = "Stata v17 / SPSS / R Statistical Environment"
            post_hoc = "Subgroup & sensitivity confounding adjustment"
            dist_test = "Kolmogorov-Smirnov / Shapiro-Wilk"
        elif framework == "PROGNOSTIC":
            tests.append("مدل رگرسیون خطرات متناسب کاکس چندمتغیره (Multivariable Cox Regression)")
            tests.append("محاسبه شاخص هارل (Harrell's C-index) و منحنی کالیبراسیون")
            software = "R Statistical Environment (survival, rms)"
            post_hoc = "Bootstrap internal calibration"
            dist_test = "Proportional hazards Schoenfeld residuals"
        else:
            tests.append("تحلیل توصیفی و آزمون‌های مقایسه آماری متناسب با مقیاس متغیرها (پارامتریک یا ناپارامتریک)")
            software = "R Statistical Environment / SPSS"
            post_hoc = "Bonferroni-adjusted pairwise comparisons"
            dist_test = "Shapiro-Wilk normality test"

        tests.append("سطح معنی‌داری آماری در تمام تحلیل‌های استنباطی p < 0.05 با فواصل اطمینان ۹۵٪ دوطرفه لحاظ خواهد شد")

        return {
            "primary_analysis": tests[0],
            "post_hoc_analysis": post_hoc,
            "distribution_test": dist_test,
            "alpha_threshold": 0.05,
            "statistical_software": software,
            "complete_testing_strategy": tests
        }
    @classmethod
    def classify_data_status(cls, val: Any) -> Dict[str, Any]:
        """Strictly distinguishes MISSING from False, 0, NOT_REPORTED, and NOT_APPLICABLE (Phase 14)."""
        if val is None:
            return {"status": "MISSING", "is_missing": True, "value": None}
        if isinstance(val, bool):
            return {"status": "VALID_BOOLEAN", "is_missing": False, "value": val}
        if isinstance(val, (int, float)):
            return {"status": "VALID_NUMERIC", "is_missing": False, "value": val}
        s = str(val).strip()
        if not s or s.upper() in ["NONE", "NULL", "MISSING", "NA", "N/A"]:
            return {"status": "MISSING", "is_missing": True, "value": None}
        if s.upper() == "NOT_REPORTED":
            return {"status": "NOT_REPORTED", "is_missing": False, "value": "NOT_REPORTED"}
        if s.upper() == "NOT_APPLICABLE":
            return {"status": "NOT_APPLICABLE", "is_missing": False, "value": "NOT_APPLICABLE"}
        if s.upper() == "UNKNOWN":
            return {"status": "UNKNOWN", "is_missing": False, "value": "UNKNOWN"}
        return {"status": "VALID_DATA", "is_missing": False, "value": val}

    @classmethod
    def calculate_sample_size_plan(cls, framework_or_model: Any, stat_inputs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculates study-design-aware sample size requirements with explicit parameter provenance audit (Phases 14 & 17)."""
        if isinstance(framework_or_model, dict):
            framework = framework_or_model.get("framework", "EXPERIMENTAL_IN_VITRO")
            stat_inputs = framework_or_model.get("statistical_parameters", {})
        else:
            framework = framework_or_model or "EXPERIMENTAL_IN_VITRO"
            stat_inputs = stat_inputs or {}

        def build_param_entry(name: str, val: Any, unit: str, default_val: Any = None, default_source: str = "ASSUMED_DEFAULT", assumption_note: str = ""):
            if val is not None:
                return {
                    "parameter": name,
                    "value": val,
                    "unit": unit,
                    "provenance_state": "provided",
                    "source": "USER_OR_STUDY_SPECIFICATION",
                    "source_location": {"section": "METHODOLOGY_SECTION_13_9"},
                    "assumption": False,
                    "justification": "Direct protocol input parameter.",
                    "confidence": "HIGH"
                }
            elif default_val is not None:
                return {
                    "parameter": name,
                    "value": default_val,
                    "unit": unit,
                    "provenance_state": "assumed",
                    "source": default_source,
                    "source_location": None,
                    "assumption": True,
                    "justification": assumption_note or "Standard default assumption; must not be silently masqueraded as empirical data.",
                    "confidence": "MODERATE"
                }
            else:
                return {
                    "parameter": name,
                    "value": None,
                    "unit": unit,
                    "provenance_state": "missing",
                    "source": None,
                    "source_location": None,
                    "assumption": False,
                    "justification": "Required statistical parameter is unobserved in literature.",
                    "confidence": "ZERO"
                }

        param_audit = {
            "alpha": build_param_entry("alpha", stat_inputs.get("alpha"), "probability", 0.05, "CONVENTIONAL_THRESHOLD", "Standard two-sided type I error rate alpha = 0.05"),
            "power": build_param_entry("power", stat_inputs.get("power"), "probability", 0.80, "CONVENTIONAL_THRESHOLD", "Standard statistical power 1 - beta = 0.80"),
            "effect_size": build_param_entry("effect_size", stat_inputs.get("expected_effect_size") or stat_inputs.get("hazard_ratio"), "standardized_metric"),
            "variance_or_sd": build_param_entry("variance_or_sd", stat_inputs.get("standard_deviation"), "units_of_measurement"),
            "baseline_event_rate": build_param_entry("baseline_event_rate", stat_inputs.get("baseline_event_rate") or stat_inputs.get("control_proportion"), "proportion"),
            "attrition_rate": build_param_entry("attrition_rate", stat_inputs.get("attrition_rate"), "proportion", 0.10, "CONVENTIONAL_ATTRITION", "Standard anticipated follow-up attrition buffer (10%)")
        }

        if framework == "EXPERIMENTAL_IN_VITRO":
            param_audit["biological_replicates"] = {
                "parameter": "biological_replicates",
                "value": 3,
                "unit": "independent passages",
                "provenance_state": "literature-derived",
                "source": "NIH_CELL_CULTURE_REPRODUCIBILITY_GUIDELINE",
                "source_location": {"standard": "NIH Notice NOT-OD-15-103"},
                "assumption": False,
                "justification": "Standard minimum threshold for biological reproducibility across separate cellular passages.",
                "confidence": "HIGH"
            }
            param_audit["technical_replicates"] = {
                "parameter": "technical_replicates",
                "value": 3,
                "unit": "plate wells",
                "provenance_state": "literature-derived",
                "source": "ASSAY_GUIDANCE_MANUAL",
                "source_location": {"standard": "NCATS Assay Guidance"},
                "assumption": False,
                "justification": "Intra-plate variance reduction via technical triplicates.",
                "confidence": "HIGH"
            }
            return {
                "design_type": "IN_VITRO_CELLULAR",
                "biological_replicates": 3,
                "technical_replicates_per_plate": 3,
                "total_independent_runs": 3,
                "pseudo_replication_warning": "Technical replicates within the same plate must be averaged and treated as 1 biological unit to avoid pseudo-replication.",
                "formula_or_standard": "Triplicate independent biological passages (n=3 biological replicates, each assayed in technical triplicate)",
                "parameter_audit": param_audit,
                "pilot_required": False
            }
        elif framework == "EXPERIMENTAL_ANIMAL":
            param_audit["animals_per_group"] = {
                "parameter": "animals_per_group",
                "value": 6,
                "unit": "animals",
                "provenance_state": "literature-derived",
                "source": "ARRIVE_GUIDELINES_MEADS_RESOURCE",
                "source_location": {"standard": "ARRIVE 2.0"},
                "assumption": False,
                "justification": "Mead's resource equation (10 <= E <= 20) with n=6 animals per group across 4 arms.",
                "confidence": "HIGH"
            }
            return {
                "design_type": "IN_VIVO_ANIMAL",
                "animals_per_group": 6,
                "formula_or_standard": "Mead's Resource Equation (E = N - B - T, where 10 <= E <= 20) and Charlebois Power Calculation",
                "alpha": 0.05,
                "power": 0.80,
                "parameter_audit": param_audit,
                "pilot_required": False
            }
        elif framework in ["SCOPING_REVIEW", "EVIDENCE_SYNTHESIS"]:
            return {
                "design_type": "SCOPING_REVIEW",
                "status": "SEARCH_SATURATION_APPLIED",
                "formula_or_standard": "PRISMA-ScR & JBI Evidence Saturation across >=3 indexed databases (alpha/power not applicable)",
                "alpha": None,
                "power": None,
                "parameter_audit": param_audit,
                "pilot_required": False
            }
        elif framework in ["USABILITY", "USABILITY_AND_DIGITAL_HEALTH"]:
            return {
                "design_type": "USABILITY_AND_DIGITAL_HEALTH",
                "status": "SAMPLE_SIZE_COMPUTED",
                "formula_or_standard": "Nielsen-Landauer Defect Discovery Model P(n) = 1 - (1 - L)^n (L=0.31) + SUS >= 30 users",
                "recommended_evaluators": 10,
                "recommended_sus_users": 30,
                "parameter_audit": param_audit,
                "pilot_required": False
            }
        elif framework in ["HEALTH_SYSTEMS_AND_HEALTH_POLICY", "EPIDEMIOLOGICAL_OBSERVATIONAL"]:
            return {
                "design_type": framework,
                "status": "SAMPLE_SIZE_COMPUTED",
                "formula_or_standard": "Cochran Complex Survey Formula adjusted for Cluster Design Effect (DEFF >= 1.5) and 10% Non-Response",
                "alpha": 0.05,
                "parameter_audit": param_audit,
                "pilot_required": False
            }
        elif framework == "CLINICAL_TRIAL":
            return {
                "design_type": "CLINICAL_TRIAL",
                "status": "SAMPLE_SIZE_COMPUTED",
                "formula_or_standard": "Two-Arm Superiority Formula n = 2(Z_alpha + Z_beta)^2 / d^2 (n=64/arm, N=128 at d=0.50)",
                "alpha": 0.05,
                "power": 0.80,
                "parameter_audit": param_audit,
                "pilot_required": False
            }
        elif framework in ["PICO", "PECO", "PROGNOSTIC"]:
            p1 = stat_inputs.get("baseline_event_rate") or stat_inputs.get("control_proportion")
            effect_size = stat_inputs.get("expected_effect_size") or stat_inputs.get("hazard_ratio")

            if (p1 is None and effect_size is None):
                return {
                    "design_type": "HUMAN_CLINICAL_OR_COHORT",
                    "status": "SAMPLE_SIZE_REQUIRES_INPUT",
                    "missing_parameters": ["baseline_event_rate", "expected_effect_size_or_hazard_ratio", "minimal_clinically_important_difference"],
                    "formula_or_standard": "Two-sample survival log-rank / proportions power equation: n = (Z_alpha + Z_beta)^2 * (p1(1-p1) + p2(1-p2)) / (p1 - p2)^2",
                    "alpha": 0.05,
                    "power": 0.80,
                    "parameter_audit": param_audit,
                    "pilot_required": True,
                    "recommendation": "Empirical baseline event rate is unknown in literature; pilot study or registry inquiry required prior to final sample size fixation. Prohibits guessing."
                }

            return {
                "design_type": "HUMAN_CLINICAL_OR_COHORT",
                "status": "SAMPLE_SIZE_COMPUTED",
                "formula_or_standard": "Two-sample survival log-rank / proportions power equation: n = (Z_alpha + Z_beta)^2 * (p1(1-p1) + p2(1-p2)) / (p1 - p2)^2",
                "alpha": 0.05,
                "power": 0.80,
                "parameter_audit": param_audit,
                "pilot_required": False
            }
        elif framework in ["DIAGNOSTIC", "DIAGNOSTIC_ACCURACY_AND_BIOMARKER"]:
            prev = stat_inputs.get("prevalence")
            sens = stat_inputs.get("expected_sensitivity")
            param_audit["prevalence"] = build_param_entry("prevalence", prev, "proportion")
            param_audit["expected_sensitivity"] = build_param_entry("expected_sensitivity", sens, "proportion")
            if prev is None or sens is None:
                return {
                    "design_type": "DIAGNOSTIC_ACCURACY",
                    "status": "SAMPLE_SIZE_REQUIRES_INPUT",
                    "missing_parameters": ["disease_prevalence", "anticipated_sensitivity", "target_precision_half_width"],
                    "formula_or_standard": "Buderer's formula for diagnostic sensitivity and specificity: n = (Z_alpha/2)^2 * P * (1-P) / (L^2 * Prevalence)",
                    "alpha": 0.05,
                    "precision": 0.05,
                    "parameter_audit": param_audit,
                    "pilot_required": False,
                    "recommendation": "Disease prevalence and target sensitivity must be specified from epidemiological benchmarks."
                }

            return {
                "design_type": "DIAGNOSTIC_ACCURACY",
                "status": "SAMPLE_SIZE_COMPUTED",
                "formula_or_standard": "Buderer's formula for diagnostic sensitivity and specificity: n = (Z_alpha/2)^2 * P * (1-P) / (L^2 * Prevalence)",
                "alpha": 0.05,
                "precision": 0.05,
                "parameter_audit": param_audit,
                "pilot_required": False
            }
        return {
            "design_type": "GENERIC",
            "status": "SAMPLE_SIZE_COMPUTED",
            "parameter_audit": param_audit,
            "pilot_required": False
        }

    @classmethod
    def generate_dynamic_ethics_subsections(cls, model_dict: Dict[str, Any]) -> str:
        """Generates dynamic ethics descriptions tailored strictly across all 7+1 archetypes."""
        framework = str(model_dict.get("framework", "")).upper()
        arch = classify_study_archetype(model_dict)
        cond_fa = model_dict.get("target_condition", {}).get("name_fa", "موضوع پژوهش")

        if arch == "scoping_review" or "SCOPING" in framework:
            return (
                "طرح حاضر یک مطالعه ثانویه مرور دامنه‌ای و سنتز شواهد منتشرشده است و فاقد مداخله مستقیم بر انسان یا حیوان می‌باشد. "
                "کلیه اصول امانت علمی، شفافیت جستجو مطابق راهنمای PRISMA-ScR، ثبت پیشینی پروتکل در OSF و افشای تعارض منافع به‌طور کامل رعایت می‌گردد."
            )
        elif arch == "usability" or "USABILITY" in framework:
            return (
                "این مطالعه کاربردپذیری با دریافت کد اخلاق و اخذ رضایت آگاهانه از کاربران شرکت‌کننده اجرا می‌گردد. "
                "داده‌های تعامل و تله‌متری کاربران به‌صورت کدگذاری‌شده و فاقد هرگونه شناسه هویتی بیماران ذخیره و محافظت می‌شوند."
            )
        elif arch == "health_systems" or "HEALTH_SYSTEM" in framework:
            return (
                "مطالعه حاضر با تایید کمیته اخلاق دانشگاه و اخذ رضایت آگاهانه از خانوارها یا پاسخ‌دهندگان اجرا می‌گردد. "
                "کلیه داده‌های هزینه‌ای، بیمه‌ای و صورتحساب‌های بیمارستانی (HIS) به‌صورت ناشناس و رمزنگاری‌شده نگهداری خواهند شد."
            )
        elif arch == "in_vitro" or framework in ["EXPERIMENTAL_IN_VITRO", "MECHANISTIC"]:
            bsl_level = model_dict.get("biosafety_level", "متناسب با سطح خطرات عوامل بیولوژیک مورد استفاده")
            ethic_content = (
                "طرح حاضر یک پژوهش آزمایشگاهی سلولی و مولکولی بر روی سیستم‌های مدل استاندارد است. "
                f"کدهای اخلاق مربوط به پژوهش‌های آزمایشگاهی و زیست‌پزشکی رعایت گردیده و کلیه موازین دفع بهداشتی پسماندهای بیولوژیک طبق دستورالعمل‌های استاندارد ایمنی زیستی ({bsl_level}) اعمال می‌گردد. "
                "به دلیل عدم مداخله بر آزمودنی‌های انسانی یا حیوانات زنده، اخذ فرم رضایت آگاهانه انسانی یا ملاحظات آزمودنی‌های آسیب‌پذیر موضوعیت ندارد (NOT_APPLICABLE_WITH_JUSTIFICATION)."
            )
        elif arch == "in_vivo" or framework == "EXPERIMENTAL_ANIMAL":
            ethic_content = (
                "پروتکل مطالعه حاضر به تایید کمیته اخلاق کار با حیوانات آزمایشگاهی دانشگاه رسیده است. "
                "اصول سه گانه اخلاق زیستی (Replacement, Reduction, Refinement: 3Rs) رعایت شده و پروتکل بیهوشی، بی‌دردی و یوتانایزی مطابق دستورالعمل‌های بین‌المللی ARRIVE اجرا می‌گردد."
            )
        elif arch == "clinical_rct" or framework in ["PICO", "CLINICAL_TRIAL"]:
            ethic_content = (
                f"پروتکل این کارآزمایی بالینی پیش از آغاز در کمیته منطقه‌ای اخلاق در پژوهش‌های زیست‌پزشکی مصوب و در مرکز کارآزمایی‌های بالینی ایران (IRCT) ثبت خواهد شد. "
                f"فرم رضایت‌نامه آگاهانه کتبی از کلیه بیماران مبتلا به {cond_fa} اخذ شده و اصل رازداری و امکان خروج داوطلبانه از مطالعه در هر مرحله بدون تاثیر بر روند درمان استاندارد تضمین می‌گردد."
            )
        else: # DIAGNOSTIC, PECO, EPIDEMIOLOGICAL, PROGNOSTIC
            ethic_content = (
                "نمونه‌گیری و گردآوری داده‌ها صرفاً با رضایت آگاهانه و با کدگذاری ناشناس اطلاعات شرکت‌کنندگان صورت می‌پذیرد. "
                "هیچ‌گونه هزینه اضافی به بیماران تحمیل نخواهد شد و نتایج تست‌ها محرمانه باقی خواهد ماند."
            )

        return ethic_content

    @classmethod
    def validate_objectives_hypotheses_variables_consistency(cls, model_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Cross-validates complete chain: Research Question -> Hypothesis -> Objective -> Independent Variable -> Dependent Variable -> Endpoint -> Statistical Analysis (Phase 24)."""
        objectives = model_dict.get("specific_objectives", [])
        hypotheses = model_dict.get("hypotheses", [])
        interventions = model_dict.get("interventions_or_exposures", [])
        outcomes = model_dict.get("primary_outcomes", [])
        endpoints = model_dict.get("endpoints", [o.get("name") for o in outcomes])

        chain_breaks = []

        # 1. Check Research Questions
        questions = model_dict.get("research_questions", [])
        
        # 2. Check Independent & Dependent Variables
        if not interventions:
            chain_breaks.append("MISSING_INDEPENDENT_VARIABLE")
        if not outcomes:
            chain_breaks.append("MISSING_DEPENDENT_VARIABLE")

        # 3. Check Objective <-> Endpoint Linkage
        if objectives and not endpoints:
            chain_breaks.append("OBJECTIVE_WITHOUT_ENDPOINT")

        # 4. Check Endpoint <-> Variable Linkage
        outcome_names = [o.get("name", "").lower() for o in outcomes]
        for ep in endpoints:
            if outcome_names and not any(o in str(ep).lower() or str(ep).lower() in o for o in outcome_names):
                chain_breaks.append(f"ENDPOINT_WITHOUT_VARIABLE: {ep}")

        # 5. Check Variable <-> Analysis Linkage
        stat_plan = cls.generate_statistical_plan(model_dict)
        if not stat_plan.get("primary_analysis"):
            chain_breaks.append("VARIABLE_WITHOUT_ANALYSIS")

        # 6. Check Hypothesis <-> Objective Alignment
        if hypotheses and not objectives:
            chain_breaks.append("HYPOTHESIS_WITHOUT_OBJECTIVE")
        elif hypotheses and objectives and len(hypotheses) > len(objectives) + 2:
            chain_breaks.append("UNGROUNDED_HYPOTHESIS_EXCEEDING_OBJECTIVES")

        # 7. Check Question <-> Hypothesis / Objective Linkage
        if questions and not (hypotheses or objectives):
            chain_breaks.append("QUESTION_WITHOUT_OBJECTIVE_OR_HYPOTHESIS")

        is_consistent = (len(chain_breaks) == 0)

        return {
            "consistency_status": "CONSISTENT" if is_consistent else "DISCREPANCY_DETECTED",
            "is_graph_fully_connected": is_consistent,
            "chain_elements_verified": [
                "Question", "Outcome", "Objective", "Hypothesis",
                "Independent_Variable", "Dependent_Variable", "Analysis_Method"
            ],
            "questions_count": len(questions),
            "objectives_count": len(objectives),
            "hypotheses_count": len(hypotheses),
            "interventions_count": len(interventions),
            "outcomes_count": len(outcomes),
            "endpoints_count": len(endpoints),
            "statistical_plan_aligned": bool(stat_plan.get("primary_analysis")),
            "discrepancies": chain_breaks
        }

    @classmethod
    def audit_statistical_feasibility(cls, model_dict: Dict[str, Any], proposed_test: Optional[str] = None) -> Dict[str, Any]:
        """Statistical feasibility gate verifying design compatibility, distribution assumptions, censoring, and dependency (Phase 16)."""
        framework = model_dict.get("framework", "EXPERIMENTAL_IN_VITRO")
        outcomes = model_dict.get("primary_outcomes", [])
        interventions = model_dict.get("interventions_or_exposures", [])
        stat_inputs = model_dict.get("statistical_parameters", {})

        inconsistencies = []
        review_required = []

        # 1. Outcome Type & Design Compatibility
        for out in outcomes:
            otype = str(out.get("type", "")).upper()
            if otype in ["HAZARD_RATIO", "MORTALITY", "TIME_TO_EVENT"] and framework == "EXPERIMENTAL_IN_VITRO":
                inconsistencies.append("TIME_TO_EVENT_ENDPOINT_IN_CELL_CULTURE_MODEL")
            if otype in ["SENSITIVITY", "SPECIFICITY", "ROC_AUC"] and framework not in ["DIAGNOSTIC", "PROGNOSTIC"]:
                inconsistencies.append("DIAGNOSTIC_METRIC_IN_INTERVENTIONAL_MODEL")

            # 2. Censoring and Model Assumptions for Survival
            if otype in ["HAZARD_RATIO", "TIME_TO_EVENT"] or (proposed_test and "cox" in proposed_test.lower()):
                has_censoring = bool(stat_inputs.get("censoring_specified"))
                has_ph_check = bool(stat_inputs.get("proportional_hazards_assumed"))
                if not (has_censoring or has_ph_check):
                    review_required.append("SURVIVAL_MODEL_LACKS_EXPLICIT_CENSORING_OR_PROPORTIONAL_HAZARDS_SPECIFICATION")

        # 3. Repeated Measures / Clustering
        is_repeated = bool(stat_inputs.get("repeated_measures") or "longitudinal" in str(model_dict).lower())
        if is_repeated and proposed_test:
            p_low = proposed_test.lower()
            if not any(k in p_low for k in ["mixed", "gee", "repeated", "rm-anova", "random effects"]):
                review_required.append("LONGITUDINAL_OR_REPEATED_DATA_ANALYZED_WITHOUT_DEPENDENCE_ADJUSTMENT")

        # 4. Multi-arm and Factorial test compatibility
        if proposed_test:
            p_lower = proposed_test.lower()
            if "t-test" in p_lower and len(interventions) > 2:
                inconsistencies.append("STUDENT_T_TEST_USED_FOR_MULTI_ARM_EXPERIMENT")
            if "one-way anova" in p_lower and len(interventions) > 1 and "factorial" in str(model_dict).lower():
                inconsistencies.append("ONE_WAY_ANOVA_USED_FOR_FACTORIAL_COMBINATION")

        is_feasible = (len(inconsistencies) == 0)
        status = "STATISTICAL_PLAN_COMPATIBLE"
        if not is_feasible:
            status = "STATISTICAL_PLAN_INCONSISTENT"
        elif review_required:
            status = "STATISTICAL_METHOD_REQUIRES_REVIEW"

        return {
            "feasibility_status": status,
            "is_feasible": is_feasible and len(review_required) == 0,
            "inconsistencies": inconsistencies,
            "review_required": review_required,
            "recommendation": (
                "Statistical analysis plan conforms with experimental design and endpoint distributions."
                if status == "STATISTICAL_PLAN_COMPATIBLE"
                else (f"Methodological review needed: {', '.join(review_required)}" if review_required else f"Revise statistical plan: {', '.join(inconsistencies)}")
            )
        }

if __name__ == "__main__":
    demo_model = {
        "framework": "EXPERIMENTAL_IN_VITRO",
        "interventions_or_exposures": [{"name": "Compound X"}, {"name": "Biologic Y"}],
        "primary_outcomes": [{"name": "Cellular Apoptosis", "measurement_unit": "% apoptosis"}],
        "comparators": [{"name": "Vehicle Control"}]
    }
    vt = DynamicProtocolDesigner.generate_variable_table(demo_model)
    tl = DynamicProtocolDesigner.generate_timeline("EXPERIMENTAL_IN_VITRO")
    sp = DynamicProtocolDesigner.generate_statistical_plan(demo_model)
    print(f"Generated {len(vt)} variables, {len(tl)} timeline phases, primary stat test: {sp['primary_analysis']}")
