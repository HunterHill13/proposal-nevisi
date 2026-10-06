#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
combination_interaction_model_selector.py - Universal Combination Interaction Model Selector
Proposal-Nevisi Engine v9.1 (Layer 2: Structural Compliance)

Selects the scientifically and mathematically sound Combination Interaction Model:
- Chou-Talalay (Median-Effect Equation / Combination Index CI)
- Bliss Independence (Multiplicative Survival Probability)
- Loewe Additivity (Dose-Equivalence / Isobologram)
- Highest Single Agent (HSA / Gaddum's Non-Interaction)
- Zero Interaction Potency (ZIP Model)

Evaluates:
- Agent types (small molecule, biologic, live oncolytic virus, antibody)
- Dose-response matrix architecture (checkerboard, fixed ratio, single concentration)
- Replication dynamics & viral kinetics (titers, scheduling, antiviral interference)
- Avoids rigid dogmatism: outputs recommended model, alternatives, assumptions, limitations, and required data.

100% General-Purpose: Zero hardcoded project subjects.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class CombinationInteractionResult:
    recommended_model: str
    recommended_model_fa: str
    decision_rationale: str
    decision_rationale_fa: str
    alternative_models: List[Dict[str, str]]
    required_data: List[str]
    model_assumptions: List[str]
    model_limitations: List[str]
    viral_kinetic_considerations: List[str] = field(default_factory=list)
    schedule_dependence_notes: Optional[str] = None
    software_tools: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "recommended_model": self.recommended_model,
            "recommended_model_fa": self.recommended_model_fa,
            "decision_rationale": self.decision_rationale,
            "decision_rationale_fa": self.decision_rationale_fa,
            "alternative_models": self.alternative_models,
            "required_data": self.required_data,
            "model_assumptions": self.model_assumptions,
            "model_limitations": self.model_limitations,
            "viral_kinetic_considerations": self.viral_kinetic_considerations,
            "schedule_dependence_notes": self.schedule_dependence_notes,
            "software_tools": self.software_tools
        }


class CombinationInteractionModelSelector:
    """Universal selector determining synergy/antagonism interaction models from assay geometry."""

    @classmethod
    def select(
        cls,
        agent_a_type: str = "small_molecule",
        agent_b_type: str = "oncolytic_virus",
        dose_matrix_type: str = "checkerboard",  # "checkerboard", "fixed_ratio", "single_dose_pair", "sparse_matrix"
        num_dose_levels_a: int = 5,
        num_dose_levels_b: int = 5,
        endpoint_type: str = "cell_viability",
        live_virus_involved: Optional[bool] = None,
        schedule_dependent: bool = True
    ) -> CombinationInteractionResult:
        """
        Selects combination interaction model based on agent biological types and dose matrix geometry.
        """
        a_type = str(agent_a_type).lower().strip()
        b_type = str(agent_b_type).lower().strip()
        matrix_type = str(dose_matrix_type).lower().strip()

        is_virus = (
            live_virus_involved is True or
            any("virus" in t for t in [a_type, b_type]) or
            live_virus_involved is None and ("virus" in a_type or "virus" in b_type)
        )

        has_full_curves = (num_dose_levels_a >= 4 and num_dose_levels_b >= 4)
        is_fixed_ratio = (matrix_type in ["fixed_ratio", "constant_ratio"])
        is_checkerboard = (matrix_type in ["checkerboard", "grid", "surface", "matrix"])
        is_single_point = (matrix_type in ["single_dose_pair", "single_point"] or (num_dose_levels_a <= 2 and num_dose_levels_b <= 2))

        viral_notes = []
        if is_virus:
            viral_notes = [
                "تکثیر دینامیک ویروسی (Viral Replication Kinetics): اثر ویروس به دلیل تکثیر درون‌سلولی تابع زمان و MOI است؛ ارزیابی هم‌افزایی باید هم در سطح بقای سلولی و هم در سطح بازده ویروسی (Viral Yield / Titer) صورت پذیرد.",
                "تداخل احتمالی ضدویروسی (Antiviral Interference Guard): بررسی عدم مهار مستقیم تکثیر یا ورود ویروس توسط ترکیب شیمیایی پیش از تفسیر هم‌افزایی انکولیتیک ضروری است.",
                "وابستگی زمانی مواجهه (Schedule Dependence): اثربخشی ممکن است بر اساس تقدم/تاخر مداخله (Pre-treatment vs Co-treatment vs Post-infection) دگرگون شود."
            ]

        # Case 1: Single concentration pair or sparse screening
        if is_single_point:
            rec = "Highest Single Agent (HSA) / Excess over Highest Single Agent"
            rec_fa = "مدل بالاترین تک‌عامل (HSA / Gaddum's Non-Interaction)"
            rat_en = (
                "When only a single dose pair or limited concentrations are evaluated, full parametric "
                "models (Chou-Talalay or Loewe) cannot be fitted reliably. HSA directly tests whether "
                "combination efficacy significantly exceeds the most active individual agent."
            )
            rat_fa = (
                "در شرایطی که تنها غلظت‌های منفرد یا معدود بررسی می‌شوند، برازش مدل‌های پارامتریک (نظیر چاو-تالالی) "
                "فاقد قابلیت اتکا است. مدل HSA مشخص می‌کند آیا اثر ترکیب فراتر از قوی‌ترین تک‌عامل است یا خیر."
            )
            alts = [
                {"model": "Bliss Independence", "note": "قابل استفاده به شرط فرض استقلال آماری احتمال بقا."},
                {"model": "Webb's Fractional Product", "note": "معادل کلاسیک بلیس برای نقاط منفرد."}
            ]
            assumptions = [
                "فرض می‌کند اثر ترکیب حداقل باید از حداکثر اثر هر یک از دو عامل به تنهایی بیشتر باشد.",
                "اطلاعاتی پیرامون مکانیسم مشترک یا شیب اثر ارائه نمی‌دهد."
            ]
            limitations = [
                "محافظه‌کارانه است؛ تمایزی بین اثر افزایشی واقعی (Additivity) و هم‌افزایی قائل نمی‌شود.",
                "شاخص عددی CI یا منحنی ایزوبولوگرام تولید نمی‌کند."
            ]
            req_data = ["پاسخ تک‌عاملی عامل A", "پاسخ تک‌عاملی عامل B", "پاسخ ترکیب همزمان A+B در تکرار بیولوژیک"]
            tools = ["GraphPad Prism", "R (synergyfinder)", "Python"]

            return CombinationInteractionResult(
                recommended_model=rec,
                recommended_model_fa=rec_fa,
                decision_rationale=rat_en,
                decision_rationale_fa=rat_fa,
                alternative_models=alts,
                required_data=req_data,
                model_assumptions=assumptions,
                model_limitations=limitations,
                viral_kinetic_considerations=viral_notes,
                schedule_dependence_notes="ارزیابی زمان‌بندی مواجهه در غلظت‌های منفرد توصیه می‌شود.",
                software_tools=tools
            )

        # Case 2: Checkerboard matrix with live virus or independent mechanisms
        if is_virus or (is_checkerboard and not is_fixed_ratio):
            rec = "Zero Interaction Potency (ZIP) / Bliss Independence Surface"
            rec_fa = "مدل استقلال بلیس (Bliss Independence) و پتانسیل برهم‌کنش صفر (ZIP Model)"
            rat_en = (
                "For multi-agent systems where one agent has dynamic, self-replicating biological kinetics (such as oncolytic viruses) "
                "or independent target sites, Bliss Independence assumes mutational/probabilistic independence without requiring "
                "mutually exclusive binding or equal hill slopes. ZIP captures shift in dose-response potency."
            )
            rat_fa = (
                "در مطالعات ترکیبی شامل ویروس‌های انکولیتیک یا دو عامل با مکانیسم‌های هدف مستقل، مدل بلیس بر پایه "
                "استقلال احتمالات عمل نموده و برخلاف مدل چاو-تالالی نیازمند فرض دگماتیک اتصال رقابتی متقابل یا شیب اثر یکسان نیست."
            )
            alts = [
                {"model": "Chou-Talalay Median-Effect Equation (CI)", "note": "در صورت رعایت نسبت ثابت غلظت‌ها و خطی بودن رگرسیون میانه اثر (r >= 0.95)."},
                {"model": "Loewe Additivity", "note": "در صورت شباهت منحنی‌های دوز-پاسخ و فرض رقابت بر سر هدف مشترک."}
            ]
            assumptions = [
                "دو عامل از طریق مسیرهای بیولوژیک مستقل عمل می‌کنند (Probabilistic independence).",
                "پاسخ ترکیبی مورد انتظار بدون برهم‌کنش برابر است با: E_AB = E_A + E_B - (E_A × E_B)."
            ]
            limitations = [
                "در غلظت‌های بسیار بالا نزدیک به ۱۰۰٪ کشندگی ممکن است خطای فشرده‌سازی اثر (Compression artifact) رخ دهد.",
                "نیازمند سنجش دقیق درصد مهار واقعی نرمال‌شده نسبت به کنترل منفی است."
            ]
            req_data = [
                "ماتریس دوز-پاسخ کامل تک‌عاملی عامل A (حداقل ۴ غلظت)",
                "ماتریس دوز-پاسخ کامل تک‌عاملی عامل B / ویروس (حداقل ۴ رقت/MOI)",
                "ماتریس متقاطع اثرات ترکیبی (Checkerboard grid)"
            ]
            tools = ["SynergyFinder 3.0 (R package)", "CompuSyn", "Python (synergy)"]

            return CombinationInteractionResult(
                recommended_model=rec,
                recommended_model_fa=rec_fa,
                decision_rationale=rat_en,
                decision_rationale_fa=rat_fa,
                alternative_models=alts,
                required_data=req_data,
                model_assumptions=assumptions,
                model_limitations=limitations,
                viral_kinetic_considerations=viral_notes,
                schedule_dependence_notes="وابستگی زمانی مواجهه: اثربخشی ممکن است بر اساس ترتیب زمانی مواجهه (Pre-treatment vs Co-treatment vs Post-infection) دگرگون شود؛ ارزیابی تیتراژ ویروسی (TCID50 یا Plaque Assay) در کنار تست MTT/سنجش حیات الزامی است.",
                software_tools=tools
            )

        # Case 3: Fixed-ratio classic pharmacological titration (Constant Ratio)
        rec = "Chou-Talalay Median-Effect Equation (Combination Index; CI)"
        rec_fa = "معادله میانه اثر چاو-تالالی (شاخص ترکیب؛ Chou-Talalay Combination Index)"
        rat_en = (
            "For small-molecule combinations evaluated at constant equipotent molar ratios (e.g. 1:1, 1:2 IC50 ratios) "
            "across multiple dilutions, the Chou-Talalay method provides rigorous quantification of Synergism (CI < 1), "
            "Additivity (CI = 1), and Antagonism (CI > 1) using the median-effect equation."
        )
        rat_fa = (
            "برای ترکیب مولکول‌های کوچک با نسبت‌های غلظتی ثابت (نظیر نسبت ۱:۱ یا ۱:۲ از IC50) در چندین رقت متوالی، "
            "روش چاو-تالالی چارچوب مرجع جهت کمی‌سازی هم‌افزایی (CI < ۱)، اثر جمع‌پذیر (CI = ۱) و آنتاگونیسم (CI > ۱) است."
        )
        alts = [
            {"model": "Loewe Additivity (Classical Isobologram)", "note": "پایه ترمودینامیکی و فیزیکوشیمیایی چاو-تالالی."},
            {"model": "Bliss Independence", "note": "مناسب در صورت انحراف از فرض رقابت متقابل."}
        ]
        assumptions = [
            "قانون اثر توده (Mass-Action Law) در برهم‌کنش دارو-گیرنده برقرار است.",
            "رگرسیون میانه اثر خطی بوده و ضریب همبستگی خطی r >= 0.95 حاصل می‌شود.",
            "نسبت غلظت‌های ترکیب در تمامی رقت‌ها ثابت نگه داشته شده است."
        ]
        limitations = [
            "برای ویروس‌های خودتکثیرشونده زنده که دوز اولیه با گذر زمان به دلیل تکثیر افزایش می‌یابد ممکن است دوز موثر دقیقاً ثابت نماند.",
            "به داده‌های پاسخ ناقص یا غیریکنواخت حساس است."
        ]
        req_data = [
            "حداقل ۴ تا ۶ غلظت منفرد از هر ماده در نسبت‌های مساوی IC50",
            "ترکیب همزمان در همان نسبت‌های ثابت",
            "سنجش درصد مهار سلولی (Fraction Affected, Fa)"
        ]
        tools = ["CompuSyn", "CalcuSyn", "R (drc, synergyfinder)"]

        return CombinationInteractionResult(
            recommended_model=rec,
            recommended_model_fa=rec_fa,
            decision_rationale=rat_en,
            decision_rationale_fa=rat_fa,
            alternative_models=alts,
            required_data=req_data,
            model_assumptions=assumptions,
            model_limitations=limitations,
            viral_kinetic_considerations=viral_notes,
            schedule_dependence_notes="ارزیابی زمان‌بندی مواجهه در صورت تفاوت در نیمه‌عمر داروها توصیه می‌شود.",
            software_tools=tools
        )
