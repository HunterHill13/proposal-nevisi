#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
native_omml_math_engine.py - Office Math Markup Language (OMML) Math Engine
Proposal-Nevisi Engine v9.0 (Layer 4: Formatting & Typesetting)

Converts LaTeX math expressions into Microsoft Word native OMML (<m:oMath> / <m:oMathPara>)
and clean Unicode representations, preventing raw LaTeX syntax leakage ($...$, \\frac, \\sqrt)
into DOCX documents and narrative texts.

100% General-Purpose: Zero hardcoded project subjects.
"""

import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional, Tuple

try:
    import latex2mathml.converter
    HAS_LATEX2MATHML = True
except ImportError:
    HAS_LATEX2MATHML = False

from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

class NativeOmmlMathEngine:
    """Converts LaTeX mathematical equations into native OMML XML and clean Unicode."""

    # Unicode Greek and Math Symbol Mappings
    LATEX_TO_UNICODE = {
        r'\alpha': 'α', r'\beta': 'β', r'\gamma': 'γ', r'\delta': 'δ',
        r'\epsilon': 'ε', r'\zeta': 'ζ', r'\eta': 'η', r'\theta': 'θ',
        r'\iota': 'ι', r'\kappa': 'κ', r'\lambda': 'λ', r'\mu': 'μ',
        r'\nu': 'ν', r'\xi': 'ξ', r'\pi': 'π', r'\rho': 'ρ',
        r'\sigma': 'σ', r'\tau': 'τ', r'\upsilon': 'υ', r'\phi': 'φ',
        r'\chi': 'χ', r'\psi': 'ψ', r'\omega': 'ω',
        r'\Gamma': 'Γ', r'\Delta': 'Δ', r'\Theta': 'Θ', r'\Lambda': 'Λ',
        r'\Xi': 'Ξ', r'\Pi': 'Π', r'\Sigma': 'Σ', r'\Phi': 'Φ',
        r'\Psi': 'Ψ', r'\Omega': 'Ω',
        r'\pm': '±', r'\mp': '∓', r'\times': '×', r'\div': '÷',
        r'\cdot': '·', r'\approx': '≈', r'\neq': '≠', r'\ne': '≠',
        r'\le': '≤', r'\leq': '≤', r'\ge': '≥', r'\geq': '≥',
        r'\infty': '∞', r'\partial': '∂', r'\nabla': '∇',
        r'\sum': '∑', r'\prod': '∏', r'\int': '∫',
        r'\in': '∈', r'\notin': '∉', r'\subset': '⊂', r'\subseteq': '⊆',
        r'\rightarrow': '→', r'\leftarrow': '←', r'\leftrightarrow': '↔',
        r'\Rightarrow': '⇒', r'\Leftarrow': '⇐', r'\Leftrightarrow': '⇔',
        r'\sqrt': '√'
    }

    SUPERSCRIPTS = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
        '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾',
        'n': 'ⁿ', 'i': 'ⁱ'
    }

    SUBSCRIPTS = {
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
        '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
        '+': '₊', '-': '₋', '=': '₌', '(': '₍', ')': '₎',
        'a': 'ₐ', 'e': 'ₑ', 'h': 'ₕ', 'i': 'ᵢ', 'j': 'ⱼ',
        'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ', 'o': 'ₒ',
        'p': 'ₚ', 'r': 'ᵣ', 's': 'ₛ', 't': 'ₜ', 'u': 'ᵤ',
        'v': 'ᵥ', 'x': 'ₓ'
    }

    @classmethod
    def strip_latex_delimiters(cls, expr: str) -> Tuple[str, bool]:
        """Strips $, $$, \\[, \\], \\(, \\) and indicates whether it was display math."""
        s = expr.strip()
        is_display = False
        if s.startswith('$$') and s.endswith('$$'):
            return s[2:-2].strip(), True
        if s.startswith(r'\[') and s.endswith(r'\]'):
            return s[2:-2].strip(), True
        if s.startswith('$') and s.endswith('$'):
            return s[1:-1].strip(), False
        if s.startswith(r'\(') and s.endswith(r'\)'):
            return s[2:-2].strip(), False
        return s, is_display

    @classmethod
    def convert_latex_to_unicode(cls, latex_expr: str) -> str:
        """
        Translates a LaTeX expression into a clean, human-readable Unicode representation.
        Zero raw backslashes or braces remain.
        """
        clean, _ = cls.strip_latex_delimiters(latex_expr)
        
        # 1. Replace fractions \frac{a}{b} -> (a / b)
        frac_pattern = re.compile(r'\\frac\{([^{}]+)\}\{([^{}]+)\}')
        while frac_pattern.search(clean):
            clean = frac_pattern.sub(r'(\1 / \2)', clean)

        # 2. Replace square roots \sqrt{x} -> √(x)
        sqrt_pattern = re.compile(r'\\sqrt\{([^{}]+)\}')
        while sqrt_pattern.search(clean):
            clean = sqrt_pattern.sub(r'√(\1)', clean)

        # 3. Replace hats \hat{p} -> p̂
        clean = re.sub(r'\\hat\{([a-zA-Z])\}', r'\1̂', clean)

        # 4. Replace Greek & Math symbols
        for sym, uni in cls.LATEX_TO_UNICODE.items():
            clean = clean.replace(sym, uni)

        # 5. Replace superscripts ^2 or ^{...}
        def _sub_sup(m):
            val = m.group(1) or m.group(2)
            return "".join(cls.SUPERSCRIPTS.get(c, c) for c in val)
        clean = re.sub(r'\^\{([^{}]+)\}|\^([0-9a-zA-Z])', _sub_sup, clean)

        # 6. Replace subscripts _1 or _{...}
        def _sub_sub(m):
            val = m.group(1) or m.group(2)
            return "".join(cls.SUBSCRIPTS.get(c, c) for c in val)
        clean = re.sub(r'_\{([^{}]+)\}|_([0-9a-zA-Z])', _sub_sub, clean)

        # 7. Clean residual braces, backslashes, and extra spaces
        clean = clean.replace('{', '').replace('}', '').replace('\\', '').strip()
        clean = re.sub(r'\s+', ' ', clean)
        return clean

    @classmethod
    def convert_latex_to_omml(cls, latex_expr: str, is_display: bool = False) -> str:
        """
        Converts LaTeX mathematical expression to OMML XML string.
        Falls back to building OMML from MathML or Unicode text.
        """
        clean_latex, disp = cls.strip_latex_delimiters(latex_expr)
        is_display = is_display or disp

        if HAS_LATEX2MATHML:
            try:
                mathml_str = latex2mathml.converter.convert(clean_latex)
                omml_body = cls._convert_mathml_to_omml(mathml_str)
                if omml_body:
                    if is_display:
                        return (
                            f'<m:oMathPara {nsdecls("m")}>'
                            f'<m:oMath>{omml_body}</m:oMath>'
                            f'</m:oMathPara>'
                        )
                    else:
                        return f'<m:oMath {nsdecls("m")}>{omml_body}</m:oMath>'
            except Exception:
                pass

        # Fallback: Clean Unicode embedded in standard OMML run
        unicode_math = cls.convert_latex_to_unicode(clean_latex)
        escaped_text = (
            unicode_math.replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
        )
        run_xml = f'<m:r><m:t>{escaped_text}</m:t></m:r>'
        if is_display:
            return (
                f'<m:oMathPara {nsdecls("m")}>'
                f'<m:oMath>{run_xml}</m:oMath>'
                f'</m:oMathPara>'
            )
        else:
            return f'<m:oMath {nsdecls("m")}>{run_xml}</m:oMath>'

    @classmethod
    def _convert_mathml_to_omml(cls, mathml_str: str) -> str:
        """Parses MathML XML tree and converts supported mathematical elements into OMML XML."""
        root = ET.fromstring(mathml_str)
        return cls._elem_to_omml(root)

    @classmethod
    def _elem_to_omml(cls, elem: ET.Element) -> str:
        tag = elem.tag.split('}')[-1]  # ignore namespace

        if tag in ['math', 'mrow', 'mstyle']:
            return "".join(cls._elem_to_omml(child) for child in elem)

        elif tag == 'mfrac':
            children = list(elem)
            if len(children) >= 2:
                num = cls._elem_to_omml(children[0])
                den = cls._elem_to_omml(children[1])
                return f'<m:f><m:num>{num}</m:num><m:den>{den}</m:den></m:f>'
            return "".join(cls._elem_to_omml(c) for c in children)

        elif tag == 'msqrt':
            inner = "".join(cls._elem_to_omml(c) for c in elem)
            return f'<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:e>{inner}</m:e></m:rad>'

        elif tag == 'mroot':
            children = list(elem)
            if len(children) >= 2:
                base = cls._elem_to_omml(children[0])
                deg = cls._elem_to_omml(children[1])
                return f'<m:rad><m:deg>{deg}</m:deg><m:e>{base}</m:e></m:rad>'
            return "".join(cls._elem_to_omml(c) for c in children)

        elif tag == 'msup':
            children = list(elem)
            if len(children) >= 2:
                base = cls._elem_to_omml(children[0])
                sup = cls._elem_to_omml(children[1])
                return f'<m:sSup><m:e>{base}</m:e><m:sup>{sup}</m:sup></m:sSup>'
            return "".join(cls._elem_to_omml(c) for c in children)

        elif tag == 'msub':
            children = list(elem)
            if len(children) >= 2:
                base = cls._elem_to_omml(children[0])
                sub = cls._elem_to_omml(children[1])
                return f'<m:sSub><m:e>{base}</m:e><m:sub>{sub}</m:sub></m:sSub>'
            return "".join(cls._elem_to_omml(c) for c in children)

        elif tag == 'mover':
            children = list(elem)
            if len(children) >= 2:
                base = cls._elem_to_omml(children[0])
                accent = children[1].text or "^"
                return f'<m:acc><m:accPr><m:chr m:val="{accent}"/></m:accPr><m:e>{base}</m:e></m:acc>'
            return "".join(cls._elem_to_omml(c) for c in children)

        elif tag in ['mi', 'mn', 'mo', 'mtext']:
            text = elem.text or ""
            escaped = (
                text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
            )
            return f'<m:r><m:t>{escaped}</m:t></m:r>'

        else:
            return "".join(cls._elem_to_omml(child) for child in elem)

    @classmethod
    def clean_text_of_latex(cls, text: str) -> str:
        """
        Replaces all inline ($...$) and display ($$...$$) LaTeX expressions
        with clean, legible Unicode text.
        """
        if not text:
            return ""

        # Display math first: $$...$$ or \[...\]
        def _repl_disp(m):
            return " " + cls.convert_latex_to_unicode(m.group(0)) + " "
        text = re.sub(r'\$\$([^$]+)\$\$|\\\[([\s\S]+?)\\\]', _repl_disp, text)

        # Inline math: $...$ or \(...\)
        def _repl_inline(m):
            return cls.convert_latex_to_unicode(m.group(0))
        text = re.sub(r'\$([^$\n]+)\$|\\\(([\s\S]+?)\\\)', _repl_inline, text)

        return text

    @classmethod
    def insert_math_into_paragraph(cls, paragraph, latex_expr: str, is_display: bool = False):
        """
        Inserts native OMML XML equation into a python-docx Paragraph.
        Falls back to run text if XML parsing fails.
        """
        omml_xml = cls.convert_latex_to_omml(latex_expr, is_display=is_display)
        try:
            elem = parse_xml(omml_xml)
            paragraph._p.append(elem)
            return elem
        except Exception:
            clean_uni = cls.convert_latex_to_unicode(latex_expr)
            run = paragraph.add_run(clean_uni)
            run.italic = True
            return run

native_omml_math_engine = NativeOmmlMathEngine
