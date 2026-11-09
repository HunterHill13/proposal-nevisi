#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Persian Academic Word Document (.docx) Generator for Proposal-Nevisi Skill
Implements the approved, publication-grade academic layout:
- Dubai typography (10.5pt body, 1.15 line spacing)
- Official Cover Page with University header, title card, 5-member team table, and submission box
- Navy (#1A365D) 14pt Bold Section Headings (H1) with classic 55-character blue line (─────────────────────────────────────────────────────── #2B6CB0)
- Burgundy (#742A2A) 11.5pt Bold Subheadings (H2 / ###)
- Steel Blue / Navy (#2B6CB0) 10.5pt Bold Level 3 Subheadings (H3 / ####)
- Teal (#0D5C75) Callout Boxes with light shading (#F0F4F8) for Epistemic Transparency (>)
- Publication-Grade Tables: Navy (#1A365D) header, alternating zebra shading (#F8FAFC / #FFFFFF), subtle horizontal borders (#E2E8F0), cantSplit and tblHeader
- Native Microsoft Word OMML equations and formulas
- Zero Soft Line Breaks to permanently prevent Word justification stretching bugs
- Robust bidi tokens (\u200F / \u200E) and markdown bold parsing
"""

import os
import sys
import re
import shutil
import tempfile
import argparse
from typing import Dict, List, Any, Optional
import docx
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

try:
    from scripts.native_omml_math_engine import NativeOmmlMathEngine
except ImportError:
    try:
        from native_omml_math_engine import NativeOmmlMathEngine
    except ImportError:
        NativeOmmlMathEngine = None

# Optional MathML to OMML XSLT converter
HAS_XSLT_OMML = False
xslt_transform = None
try:
    from lxml import etree
    from latex2mathml.converter import convert as latex2mathml_convert
    xslt_path = r'C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL'
    if os.path.exists(xslt_path):
        xslt_doc = etree.parse(xslt_path)
        xslt_transform = etree.XSLT(xslt_doc)
        HAS_XSLT_OMML = True
except Exception:
    HAS_XSLT_OMML = False

def latex_to_omml_element(latex_code: str):
    """Converts LaTeX math string to Word native OMML XML element using Microsoft XSLT."""
    if not HAS_XSLT_OMML or xslt_transform is None:
        return None
    try:
        mathml = latex2mathml_convert(latex_code)
        dom = etree.fromstring(mathml)
        new_dom = xslt_transform(dom)
        omml_str = etree.tostring(new_dom.getroot(), encoding='utf-8').decode('utf-8')
        return parse_xml(omml_str)
    except Exception:
        return None

def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def apply_rtl_right(p, space_before=2.5, space_after=3.5, line_spacing=1.15):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing

    pPr = p._p.get_or_add_pPr()
    bidi = pPr.find(qn('w:bidi'))
    if bidi is None:
        pPr.append(parse_xml(f'<w:bidi {nsdecls("w")} w:val="1"/>'))
    else:
        bidi.set(qn('w:val'), '1')

    jc = pPr.find(qn('w:jc'))
    if jc is None:
        pPr.append(parse_xml(f'<w:jc {nsdecls("w")} w:val="start"/>'))
    else:
        jc.set(qn('w:val'), 'start')

def apply_rtl_justify(p, space_before=2.5, space_after=3.5, line_spacing=1.15):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing

    pPr = p._p.get_or_add_pPr()
    bidi = pPr.find(qn('w:bidi'))
    if bidi is None:
        pPr.append(parse_xml(f'<w:bidi {nsdecls("w")} w:val="1"/>'))
    else:
        bidi.set(qn('w:val'), '1')

    jc = pPr.find(qn('w:jc'))
    if jc is None:
        pPr.append(parse_xml(f'<w:jc {nsdecls("w")} w:val="both"/>'))
    else:
        jc.set(qn('w:val'), 'both')

def apply_rtl_center(p, space_before=2.5, space_after=3.5, line_spacing=1.15):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing

    pPr = p._p.get_or_add_pPr()
    bidi = pPr.find(qn('w:bidi'))
    if bidi is None:
        pPr.append(parse_xml(f'<w:bidi {nsdecls("w")} w:val="1"/>'))
    else:
        bidi.set(qn('w:val'), '1')

    jc = pPr.find(qn('w:jc'))
    if jc is None:
        pPr.append(parse_xml(f'<w:jc {nsdecls("w")} w:val="center"/>'))
    else:
        jc.set(qn('w:val'), 'center')

def set_p_rtl(p, space_before=2.5, space_after=3.5, line_spacing=1.15, align="both"):
    if align in ["center", "middle"]:
        apply_rtl_center(p, space_before, space_after, line_spacing)
    elif align in ["right", "start"]:
        apply_rtl_right(p, space_before, space_after, line_spacing)
    else:
        apply_rtl_justify(p, space_before, space_after, line_spacing)

def add_r(p, text, font_name="Dubai", size_pt=10.5, bold=False, italic=False, color_rgb=(0x2D, 0x37, 0x48), is_rtl=True):
    if text is None:
        return
    text = str(text).replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'[^\x09\x0A\x0D\x20-\uD7FF\uE000-\uFFFD]', '', text)
    run = p.add_run(text)
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)

    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:hAnsi="{font_name}" w:cs="{font_name}"/>')
        rPr.append(rFonts)
    else:
        rFonts.set(qn('w:cs'), font_name)
        rFonts.set(qn('w:ascii'), font_name)
        rFonts.set(qn('w:hAnsi'), font_name)

    rtl_elem = rPr.find(qn('w:rtl'))
    if is_rtl:
        if rtl_elem is None:
            rPr.append(parse_xml(f'<w:rtl {nsdecls("w")} w:val="1"/>'))
        else:
            rtl_elem.set(qn('w:val'), '1')
    else:
        if rtl_elem is not None:
            rPr.remove(rtl_elem)

    sz_half_pts = str(int(round(size_pt * 2)))
    sz_elem = rPr.find(qn('w:sz'))
    if sz_elem is None:
        rPr.append(parse_xml(f'<w:sz {nsdecls("w")} w:val="{sz_half_pts}"/>'))
    else:
        sz_elem.set(qn('w:val'), sz_half_pts)

    szCs_elem = rPr.find(qn('w:szCs'))
    if szCs_elem is None:
        rPr.append(parse_xml(f'<w:szCs {nsdecls("w")} w:val="{sz_half_pts}"/>'))
    else:
        szCs_elem.set(qn('w:val'), sz_half_pts)

    bCs_elem = rPr.find(qn('w:bCs'))
    if bold:
        if bCs_elem is None:
            rPr.append(parse_xml(f'<w:bCs {nsdecls("w")}/>'))
    else:
        if bCs_elem is not None:
            rPr.remove(bCs_elem)

    iCs_elem = rPr.find(qn('w:iCs'))
    if italic:
        if iCs_elem is None:
            rPr.append(parse_xml(f'<w:iCs {nsdecls("w")}/>'))
    else:
        if iCs_elem is not None:
            rPr.remove(iCs_elem)

    return run

def add_bidi_text(p, text, font_name="Dubai", size_pt=10.5, bold=False, italic=False, color_rgb=(0x2D, 0x37, 0x48)):
    if not text:
        return
    if NativeOmmlMathEngine is not None:
        try:
            text = NativeOmmlMathEngine.clean_text_of_latex(text)
        except Exception:
            pass
    text = str(text).replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
    pattern = r'(\[[0-9,\s\-–]+\]|\([A-Za-z0-9_\-\s,\./%α-ωΑ-Ω→⇌⇄<>=\+\^±":]+\)|[A-Za-z0-9_\-\./%α-ωΑ-Ω\+\^±"]+(?:\s+[A-Za-z0-9_\-\./%α-ωΑ-Ω\+\^±":<>=→⇌⇄]+)*|[→⇌⇄]|(?:<=|>=|[<>=])\s*\d+(?:\.\d+)?)'
    tokens = re.split(pattern, text)
    for tok in tokens:
        if not tok:
            continue
        has_persian = any('\u0600' <= c <= '\u06FF' for c in tok)
        if re.match(r'^\s*\[[0-9,\s\-–]+\]\s*$', tok):
            clean_tok = tok.strip()
            add_r(p, f"\u200F{clean_tok}\u200F", font_name=font_name, size_pt=size_pt, bold=True, color_rgb=(0x1A, 0x36, 0x5D), is_rtl=True)
        elif tok.startswith('(') and tok.endswith(')') and not has_persian:
            inner = tok[1:-1]
            add_r(p, "\u200F(", font_name=font_name, size_pt=size_pt, bold=bold, italic=italic, color_rgb=color_rgb, is_rtl=True)
            add_r(p, f"\u200E{inner}\u200E", font_name="Times New Roman", size_pt=size_pt, bold=bold, italic=italic, color_rgb=color_rgb, is_rtl=False)
            add_r(p, ")\u200F", font_name=font_name, size_pt=size_pt, bold=bold, italic=italic, color_rgb=color_rgb, is_rtl=True)
        elif not has_persian and re.search(r'[A-Za-z0-9→⇌⇄<>=]', tok):
            add_r(p, f"\u200E{tok}\u200E", font_name="Times New Roman", size_pt=size_pt, bold=bold, italic=italic, color_rgb=color_rgb, is_rtl=False)
        else:
            add_r(p, tok, font_name=font_name, size_pt=size_pt, bold=bold, italic=italic, color_rgb=color_rgb, is_rtl=True)

def add_formatted_bidi_text(p, text, font_name="Dubai", size_pt=10.5, default_bold=False, default_italic=False, color_rgb=(0x2D, 0x37, 0x48)):
    segments = re.split(r'(\*\*.*?\*\*|\*.*?\*)', text)
    for seg in segments:
        if not seg:
            continue
        b = default_bold
        it = default_italic
        clean = seg
        if seg.startswith('**') and seg.endswith('**') and len(seg) >= 4:
            b = True
            clean = seg[2:-2]
        elif seg.startswith('*') and seg.endswith('*') and len(seg) >= 2:
            it = True
            clean = seg[1:-1]
        add_bidi_text(p, clean, font_name=font_name, size_pt=size_pt, bold=b, italic=it, color_rgb=color_rgb)

def add_title(doc, main_title):
    """Title heading: Navy (#1A365D) 16pt bold center."""
    p = doc.add_paragraph()
    apply_rtl_center(p, space_before=16, space_after=12)
    add_r(p, main_title, font_name="Dubai", size_pt=16, bold=True, color_rgb=(0x1A, 0x36, 0x5D))
    return p

def add_h1(doc, text, with_blue_line=True):
    """Section Heading 1: Navy (#1A365D) 14pt bold right-aligned followed by 55-char blue line."""
    p = doc.add_paragraph()
    apply_rtl_right(p, space_before=16, space_after=3)
    add_formatted_bidi_text(p, text, font_name="Dubai", size_pt=14, default_bold=True, color_rgb=(0x1A, 0x36, 0x5D))

    if with_blue_line:
        p_line = doc.add_paragraph()
        apply_rtl_right(p_line, space_before=0, space_after=8)
        add_r(p_line, "───────────────────────────────────────────────────────", font_name="Dubai", size_pt=8.5, bold=False, color_rgb=(0x2B, 0x6C, 0xB0), is_rtl=True)
    return p

def add_h2(doc, text):
    """Subheading 2: Burgundy (#742A2A) 11.5pt bold right-aligned."""
    p = doc.add_paragraph()
    apply_rtl_right(p, space_before=12, space_after=4)
    add_formatted_bidi_text(p, text, font_name="Dubai", size_pt=11.5, default_bold=True, color_rgb=(0x74, 0x2A, 0x2A))
    return p

def add_h3(doc, text):
    """Subheading 3: Steel Blue / Navy (#2B6CB0) 10.5pt bold right-aligned."""
    p = doc.add_paragraph()
    apply_rtl_right(p, space_before=8, space_after=3)
    add_formatted_bidi_text(p, text, font_name="Dubai", size_pt=10.5, default_bold=True, color_rgb=(0x2B, 0x6C, 0xB0))
    return p

def add_body_p(doc, text):
    """Standard body paragraph: Dubai 10.5pt, line_spacing 1.15, fully justified without soft breaks."""
    p = doc.add_paragraph()
    apply_rtl_justify(p, space_before=2.5, space_after=3.5, line_spacing=1.15)
    add_formatted_bidi_text(p, text, font_name="Dubai", size_pt=10.5, color_rgb=(0x2D, 0x37, 0x48))
    return p

def add_bullet_p(doc, text):
    """Standard bullet paragraph with stylish #2B6CB0 square bullet."""
    p = doc.add_paragraph()
    apply_rtl_justify(p, space_before=2.0, space_after=2.5, line_spacing=1.15)
    add_r(p, "▪ ", font_name="Dubai", size_pt=10, bold=True, color_rgb=(0x2B, 0x6C, 0xB0), is_rtl=True)
    add_formatted_bidi_text(p, text, font_name="Dubai", size_pt=10.5, color_rgb=(0x2D, 0x37, 0x48))
    return p

def add_numbered_p(doc, num, text):
    """Numbered item paragraph with bold prefix and crisp justified body."""
    p = doc.add_paragraph()
    apply_rtl_justify(p, space_before=2.5, space_after=3.0, line_spacing=1.15)
    add_formatted_bidi_text(p, f"{num}. {text}", font_name="Dubai", size_pt=10.5, color_rgb=(0x2D, 0x37, 0x48))
    return p

def add_callout_box(doc, text):
    """Epistemic transparency or policy note callout box with teal border and light fill."""
    clean_q = text.replace('>', '').replace('[!NOTE]', '').strip()
    clean_q = re.sub(r'^\*?\*?شفافیت معرفتی پیرامون سوگیری انتشار(?:\s*\(Publication Bias\))?:?\*?\*?:?\s*', '', clean_q).strip()
    if not clean_q:
        return None
    p = doc.add_paragraph()
    apply_rtl_justify(p, space_before=5, space_after=5)
    pPr = p._p.get_or_add_pPr()
    pBdr = parse_xml(f'''<w:pBdr {nsdecls("w")}>
        <w:right w:val="single" w:sz="24" w:space="12" w:color="0D5C75"/>
    </w:pBdr>''')
    pPr.append(pBdr)
    pPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F0F4F8"/>'))
    add_r(p, "◄ شفافیت معرفتی پیرامون سوگیری انتشار (Publication Bias): ", font_name="Dubai", size_pt=10.5, bold=True, color_rgb=(0x0D, 0x5C, 0x75))
    add_formatted_bidi_text(p, clean_q, font_name="Dubai", size_pt=10, default_italic=True, color_rgb=(0x2D, 0x37, 0x48))
    return p

def add_formula_box(doc, formula_text, explanation=None):
    """Inserts math equation using native OMML or fallback formula box."""
    omml_elem = latex_to_omml_element(formula_text)
    if omml_elem is not None:
        p = doc.add_paragraph()
        pPr = p._p.get_or_add_pPr()
        jc = parse_xml(f'<w:jc {nsdecls("w")} w:val="center"/>')
        spacing = parse_xml(f'<w:spacing {nsdecls("w")} w:before="100" w:after="80"/>')
        pPr.append(spacing)
        pPr.append(jc)
        p._p.append(omml_elem)
        if explanation:
            p_exp = doc.add_paragraph()
            apply_rtl_right(p_exp, space_before=1, space_after=4)
            add_r(p_exp, explanation, font_name="Dubai", size_pt=9.5, italic=True, color_rgb=(0x4A, 0x55, 0x68))
        return p

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    pPr = p._p.get_or_add_pPr()
    pPr.append(parse_xml(f'<w:bidi {nsdecls("w")}/>'))
    pPr.append(parse_xml(f'<w:jc {nsdecls("w")} w:val="center"/>'))
    pPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8F9FA"/>'))
    pBdr = parse_xml(f'''<w:pBdr {nsdecls("w")}>
        <w:top w:val="single" w:sz="4" w:space="4" w:color="CBD5E0"/>
        <w:left w:val="single" w:sz="4" w:space="4" w:color="CBD5E0"/>
        <w:bottom w:val="single" w:sz="4" w:space="4" w:color="CBD5E0"/>
        <w:right w:val="single" w:sz="24" w:space="8" w:color="1A365D"/>
    </w:pBdr>''')
    pPr.append(pBdr)

    if NativeOmmlMathEngine is not None:
        try:
            NativeOmmlMathEngine.insert_math_into_paragraph(p, formula_text, is_display=True)
            return p
        except Exception:
            pass

    run = p.add_run(formula_text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.bold = True
    run.font.color.rgb = RGBColor(0x1A, 0x20, 0x2C)
    return p

def add_ref_item(doc, text):
    """English or Persian reference item with clean hanging indent."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15

    has_persian_letters = any('\u0620' <= c <= '\u06EF' or c in ('\u067E', '\u0686', '\u0698', '\u06AF', '\u06A9', '\u06CC') for c in text)
    if has_persian_letters:
        apply_rtl_justify(p, space_before=2, space_after=3, line_spacing=1.15)
        add_formatted_bidi_text(p, text, font_name="Dubai", size_pt=10, color_rgb=(0x2D, 0x37, 0x48))
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        fa_to_en = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
        clean_ref_text = text.translate(fa_to_en)
        add_r(p, clean_ref_text, font_name="Times New Roman", size_pt=9.5, color_rgb=(0x2D, 0x37, 0x48), is_rtl=False)
    return p

def is_table_separator(line: str) -> bool:
    clean = line.strip()
    if not clean or not clean.startswith('|'):
        return False
    inner = clean.strip('|')
    parts = [p.strip() for p in inner.split('|')]
    return bool(parts) and all(bool(re.match(r'^:?-+:?$', p)) for p in parts)

def render_styled_table(doc, table_lines):
    """Publication-grade table with navy header, zebra striping, cantSplit, and tblHeader."""
    rows = []
    for line in table_lines:
        line_clean = line.strip()
        if not line_clean or is_table_separator(line_clean):
            continue
        cells = [c.strip() for c in line_clean.split('|')[1:-1]]
        if cells:
            rows.append(cells)

    if not rows:
        return

    num_rows = len(rows)
    num_cols = len(rows[0])
    table = doc.add_table(rows=num_rows, cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    tblPr = table._tbl.tblPr
    tblPr.append(parse_xml(f'<w:bidiVisual {nsdecls("w")}/>'))
    tblBorders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="single" w:sz="8" w:color="1A365D"/><w:bottom w:val="single" w:sz="12" w:color="1A365D"/><w:insideH w:val="single" w:sz="4" w:color="E2E8F0"/><w:insideV w:val="none"/><w:left w:val="none"/><w:right w:val="none"/></w:tblBorders>')
    tblPr.append(tblBorders)

    for r_idx, row_data in enumerate(rows):
        is_header = (r_idx == 0)
        tr = table.rows[r_idx]._tr
        trPr = tr.get_or_add_trPr()
        if is_header:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        for c_idx, cell_value in enumerate(row_data):
            if c_idx < len(table.rows[r_idx].cells):
                cell = table.cell(r_idx, c_idx)
                cell.text = ""
                p = cell.paragraphs[0]

                if is_header:
                    set_cell_shading(cell, "1A365D")
                    set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
                    apply_rtl_center(p, space_before=2, space_after=2, line_spacing=1.15)
                    add_formatted_bidi_text(p, cell_value, font_name="Dubai", size_pt=9.5, default_bold=True, color_rgb=(0xFF, 0xFF, 0xFF))
                else:
                    bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
                    set_cell_shading(cell, bg)
                    set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
                    align_fn = apply_rtl_center if c_idx == 0 else apply_rtl_right
                    align_fn(p, space_before=2, space_after=2, line_spacing=1.15)
                    if "■" in cell_value or "●" in cell_value:
                        add_r(p, "●", font_name="Dubai", size_pt=10, bold=True, color_rgb=(0x2B, 0x6C, 0xB0))
                    else:
                        add_formatted_bidi_text(p, cell_value, font_name="Dubai", size_pt=9.0, default_bold=False, color_rgb=(0x2D, 0x37, 0x48))

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def render_official_cover_page(doc, main_title: str, english_title: Optional[str] = None):
    """Generates the official cover page with university header, title card, and team table."""
    p_uni = doc.add_paragraph()
    apply_rtl_center(p_uni, space_before=4, space_after=2)
    add_r(p_uni, "دانشگاه علوم پزشکی و خدمات بهداشتی درمانی بقیه‌الله (عج)", font_name="Dubai", size_pt=14.0, bold=True, color_rgb=(0x1A, 0x36, 0x5D))

    p_sub = doc.add_paragraph()
    apply_rtl_center(p_sub, space_before=0, space_after=3)
    add_r(p_sub, "کمیته تحقیقات و فناوری دانشجویی — رویداد ملی ایده‌پردازی «جوانی جمعیت؛ از چالش تا راهکار»", font_name="Dubai", size_pt=11.0, bold=True, color_rgb=(0x74, 0x2A, 0x2A))

    p_axis = doc.add_paragraph()
    apply_rtl_center(p_axis, space_before=2, space_after=6)
    add_r(p_axis, "محور تخصصی ۵: خانواده در شرایط واقعی زندگی؛ طراحی حمایت‌های مؤثر و قابل دسترس", font_name="Dubai", size_pt=11.0, bold=True, color_rgb=(0x0D, 0x5C, 0x75))

    t_box = doc.add_table(rows=1, cols=1)
    t_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_box._tbl.tblPr.append(parse_xml(f'<w:bidiVisual {nsdecls("w")}/>'))
    cell_t = t_box.cell(0, 0)
    cell_t.width = Inches(6.8)
    set_cell_shading(cell_t, "F8FAFC")
    set_cell_margins(cell_t, top=100, bottom=100, left=140, right=140)

    tcPr_t = cell_t._tc.get_or_add_tcPr()
    tcPr_t.append(parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="6" w:color="CBD5E0"/><w:left w:val="single" w:sz="6" w:color="CBD5E0"/><w:bottom w:val="single" w:sz="6" w:color="CBD5E0"/><w:right w:val="single" w:sz="36" w:color="1A365D"/></w:tcBorders>'))

    pt1 = cell_t.paragraphs[0]
    apply_rtl_center(pt1, space_before=2, space_after=2)
    add_r(pt1, "پروپوزال رسمی طرح پژوهشی / ایده سیاستی و مداخله‌ای", font_name="Dubai", size_pt=10.5, bold=True, color_rgb=(0x0D, 0x5C, 0x75))

    pt2 = cell_t.add_paragraph()
    apply_rtl_center(pt2, space_before=2, space_after=4)
    add_r(pt2, main_title, font_name="Dubai", size_pt=11.5, bold=True, color_rgb=(0x1A, 0x20, 0x2C))

    if english_title:
        pt3 = cell_t.add_paragraph()
        pt3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pt3.paragraph_format.space_before = Pt(2)
        pt3.paragraph_format.space_after = Pt(2)
        add_r(pt3, english_title, font_name="Times New Roman", size_pt=9.0, italic=True, color_rgb=(0x4A, 0x55, 0x68), is_rtl=False)

    p_thdr = doc.add_paragraph()
    apply_rtl_right(p_thdr, space_before=6, space_after=4)
    add_r(p_thdr, "مشخصات کامل اعضای گروه پژوهشی (۳ الی ۵ نفره) — ضوابط صفحه ۱۰ دفترچه راهنما:", font_name="Dubai", size_pt=10, bold=True, color_rgb=(0x1A, 0x36, 0x5D))

    team_headers = ["ردیف", "نام و نام خانوادگی", "رشته و مقطع تحصیلی", "دانشگاه / دانشکده", "نقش در پروژه"]
    team_rows = [
        ["۱", "[نام عضو اول - سرپرست]", "پزشکی عمومی / بالینی", "علوم پزشکی بقیه‌الله (عج)", "پژوهشگر اصلی و مسئول مکاتبات"],
        ["۲", "[نام عضو دوم]", "پزشکی عمومی / فیزیوپاتولوژی", "علوم پزشکی بقیه‌الله (عج)", "تحلیل‌گر داده‌های کمی و بیواستاتیک"],
        ["۳", "[نام عضو سوم]", "مدیریت خدمات بهداشتی", "علوم پزشکی بقیه‌الله (عج)", "مسئول متدولوژی کیفی و مصاحبه‌ها"],
        ["۴", "[نام عضو چهارم]", "مامایی و سلامت باروری", "علوم پزشکی بقیه‌الله (عج)", "کارشناس ارزیابی بسته‌های بارداری"],
        ["۵", "[نام عضو پنجم - اختیاری]", "اقتصاد سلامت / سیاست‌گذاری", "علوم پزشکی بقیه‌الله (عج)", "مدل‌سازی اقتصادی و ارزیابی CHE"]
    ]

    col_w_team = [Inches(0.6), Inches(1.8), Inches(1.5), Inches(1.4), Inches(1.5)]
    t_team = doc.add_table(rows=len(team_rows) + 1, cols=5)
    t_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_team._tbl.tblPr.append(parse_xml(f'<w:bidiVisual {nsdecls("w")}/>'))

    for c_i, h_text in enumerate(team_headers):
        cell = t_team.cell(0, c_i)
        cell.text = ""
        set_cell_shading(cell, "1A365D")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        apply_rtl_center(p, space_before=2, space_after=2)
        add_r(p, h_text, font_name="Dubai", size_pt=9.5, bold=True, color_rgb=(0xFF, 0xFF, 0xFF))

    for r_i, r_vals in enumerate(team_rows):
        bg = "F8FAFC" if r_i % 2 == 1 else "FFFFFF"
        for c_i, val in enumerate(r_vals):
            cell = t_team.cell(r_i + 1, c_i)
            cell.text = ""
            set_cell_shading(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            align_fn = apply_rtl_center if c_i in [0, 3] else apply_rtl_right
            align_fn(p, space_before=2, space_after=2)
            add_r(p, val, font_name="Dubai", size_pt=9, bold=(c_i == 1), color_rgb=(0x2D, 0x37, 0x48))

    p_box_sub = doc.add_paragraph()
    apply_rtl_justify(p_box_sub, space_before=6, space_after=6)
    p_box_sub_pr = p_box_sub._p.get_or_add_pPr()
    p_box_sub_pr.append(parse_xml(f'''<w:pBdr {nsdecls("w")}>
        <w:right w:val="single" w:sz="24" w:space="12" w:color="2B6CB0"/>
    </w:pBdr>'''))
    p_box_sub_pr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F0F4F8"/>'))
    add_r(p_box_sub, "راهنمای ارسال اثر طبق دفترچه راهنما: این پروپوزال باید به صورت هم‌زمان در دو قالب Word (.docx) و PDF (.pdf) به نشانی پست الکترونیک دبیرخانه رویداد (bmsusrc.a@gmail.com) با موضوع مشخص «رویداد ایده پردازی: جوانی جمعیت» ارسال گردد.", font_name="Dubai", size_pt=9.0, color_rgb=(0x2D, 0x37, 0x48))

    doc.add_page_break()

def build_proposal_docx(md_path: str, output_docx_path: str, font_name: str = "Dubai"):
    doc = Document()

    for s in doc.sections:
        s.page_width = Inches(8.27)
        s.page_height = Inches(11.69)
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)
        s._sectPr.append(parse_xml(f'<w:bidi {nsdecls("w")}/>'))
        s._sectPr.append(parse_xml(f'<w:rtlGutter {nsdecls("w")}/>'))

        hp = s.header.paragraphs[0]
        apply_rtl_right(hp, space_before=0, space_after=0)
        add_r(hp, "رویداد ملی ایده‌پردازی جوانی جمعیت | کمیته تحقیقات دانشجویی — سند مصوب پروپوزال", font_name="Dubai", size_pt=8.5, color_rgb=(0x71, 0x80, 0x96))

        fp = s.footer.paragraphs[0]
        apply_rtl_center(fp, space_before=0, space_after=0)
        add_r(fp, "پروپوزال رسمی مصوب دانشگاه علوم پزشکی بقیه‌الله (عج)", font_name="Dubai", size_pt=8.5, color_rgb=(0xA0, 0xAE, 0xC0))

    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    lines = md_text.splitlines()

    # Determine if this is a full research proposal requiring official cover page and blue heading rules
    has_sec1 = any(re.match(r'^##\s+(?:۱|1)\.', l.strip()) for l in lines)
    is_full_proposal = len(lines) >= 15 or has_sec1

    in_table = False
    table_lines = []
    is_refs = False
    cover_rendered = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith('|') and stripped.endswith('|'):
            in_table = True
            table_lines.append(stripped)
            continue
        elif in_table:
            render_styled_table(doc, table_lines)
            table_lines = []
            in_table = False

        if not stripped or stripped == '---':
            continue

        if (('۱۴.' in stripped or '14.' in stripped) or ('۲۸.' in stripped or '28.' in stripped)) and 'منابع' in stripped:
            is_refs = True

        if stripped.startswith('# '):
            title_text = stripped[2:].strip()
            if is_full_proposal and not cover_rendered:
                render_official_cover_page(doc, title_text)
                cover_rendered = True
            else:
                add_title(doc, title_text)
            continue
        elif stripped.startswith('## '):
            h1_text = stripped[3:].strip()
            add_h1(doc, h1_text, with_blue_line=is_full_proposal)
            continue
        elif stripped.startswith('### '):
            add_h2(doc, stripped[4:].strip())
            continue
        elif stripped.startswith('#### '):
            add_h3(doc, stripped[5:].strip())
            continue
        elif stripped.startswith('>'):
            add_callout_box(doc, stripped)
            continue
        elif is_refs and (re.match(r'^\d+\.\s+', stripped) or re.match(r'^\[\d+\]\s*', stripped)):
            add_ref_item(doc, stripped)
            continue

        is_formula_line = (
            (stripped.startswith('$$') and stripped.endswith('$$') and len(stripped) > 4) or
            (stripped.startswith(r'\[') and stripped.endswith(r'\]')) or
            (stripped.startswith('$') and stripped.endswith('$') and len(stripped) > 2 and ('=' in stripped or r'\frac' in stripped)) or
            stripped.startswith('Growth Inhibition (%) =') or
            stripped.startswith('CI =') or
            stripped.startswith('E = N - B - T') or
            (r'\frac{' in stripped and ('=' in stripped or 'n' in stripped.lower())) or
            bool(re.match(r'^[nN]\s*=\s*\\frac', stripped))
        )
        if is_formula_line:
            clean_form = stripped
            if clean_form.startswith('$$') and clean_form.endswith('$$'):
                clean_form = clean_form[2:-2].strip()
            elif clean_form.startswith(r'\[') and clean_form.endswith(r'\]'):
                clean_form = clean_form[2:-2].strip()
            elif clean_form.startswith('$') and clean_form.endswith('$'):
                clean_form = clean_form[1:-1].strip()
            add_formula_box(doc, clean_form)
        elif stripped.startswith('* ') or stripped.startswith('- '):
            add_bullet_p(doc, stripped[2:].strip())
        elif re.match(r'^\d+\.\s+', stripped):
            m = re.match(r'^(\d+)\.\s+(.*)', stripped)
            add_numbered_p(doc, m.group(1), m.group(2).strip())
        else:
            add_body_p(doc, stripped)

    if in_table and table_lines:
        render_styled_table(doc, table_lines)

    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tf:
        temp_docx = tf.name
    try:
        doc.save(temp_docx)
        shutil.copy2(temp_docx, output_docx_path)
    finally:
        if os.path.exists(temp_docx):
            try:
                os.remove(temp_docx)
            except Exception:
                pass

    print(f"Master Word DOCX successfully generated at: {output_docx_path}", file=sys.stderr)

class DocxBuilder:
    @classmethod
    def build_docx_from_markdown(cls, md_content_or_path: str, output_docx_path: str, font_name: str = "Dubai"):
        cls.build_docx(md_content_or_path, output_docx_path, font_name=font_name)

    @classmethod
    def build_docx(cls, md_content_or_path: str, output_docx_path: str, font_name: str = "Dubai"):
        if os.path.isfile(md_content_or_path):
            build_proposal_docx(md_content_or_path, output_docx_path, font_name=font_name)
        else:
            temp_dir = tempfile.gettempdir()
            temp_md = os.path.join(temp_dir, "temp_proposal_input.md")
            with open(temp_md, "w", encoding="utf-8") as tf:
                tf.write(md_content_or_path)
            try:
                build_proposal_docx(temp_md, output_docx_path, font_name=font_name)
            finally:
                if os.path.exists(temp_md):
                    os.remove(temp_md)

    @classmethod
    def inspect_docx_file(cls, docx_path: str) -> Dict[str, Any]:
        if not os.path.exists(docx_path):
            return {"inspection_status": "FILE_NOT_FOUND", "file_exists": False, "verified": False}

        try:
            doc = Document(docx_path)
        except Exception as e:
            return {"inspection_status": "MALFORMED_DOCX", "verified": False, "error": str(e)}

        if len(doc.paragraphs) == 0 and len(doc.tables) == 0:
            return {"inspection_status": "EMPTY_DOCX", "verified": False, "paragraphs_count": 0, "tables_count": 0}

        h1_headings: List[str] = []
        h2_headings: List[str] = []
        h1_numbers: List[int] = []
        has_bidi = False
        has_dubai = False

        digits_map = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")

        for p in doc.paragraphs:
            p_xml = p._p.xml
            if "<w:bidi" in p_xml:
                has_bidi = True
            if 'w:cs="Dubai"' in p_xml or 'w:ascii="Dubai"' in p_xml:
                has_dubai = True
            
            p_text = p.text.strip()
            m_h1 = re.match(r'^([0-9]{1,2}|[۰-۹]{1,2})\.\s+', p_text)
            is_h1_size = ('w:sz w:val="28"' in p_xml or 'w:szCs w:val="28"' in p_xml or any(r.font.size and r.font.size.pt >= 13.5 for r in p.runs))
            
            if m_h1 and is_h1_size:
                num_str = m_h1.group(1).translate(digits_map)
                num_val = int(num_str) if num_str.isdigit() else None
                if num_val and 1 <= num_val <= 28:
                    h1_headings.append(p_text)
                    h1_numbers.append(num_val)
            elif re.match(r'^(?:13|۱۳)\-(?:[0-9]{1,2}|[۰-۹]{1,2})\.\s+', p_text):
                h2_headings.append(p_text)

        tables_count = len(doc.tables)
        has_table_headers = False
        if tables_count > 0:
            first_tbl = doc.tables[0]
            if len(first_tbl.rows) > 0 and len(first_tbl.rows[0].cells) > 0:
                has_table_headers = True

        is_28_section = (max(h1_numbers) > 14) if h1_numbers else False
        if is_28_section:
            sections_present = len(h1_headings) >= 28
            subsecs_present = True
        else:
            sections_present = len(h1_headings) >= 14
            subsecs_present = len(h2_headings) >= 14

        has_duplicate_h1 = len(h1_numbers) != len(set(h1_numbers))
        is_strictly_ordered = (h1_numbers == sorted(h1_numbers)) if h1_numbers else False

        is_valid = bool(sections_present and subsecs_present and has_bidi and has_dubai and tables_count >= 1 and not has_duplicate_h1 and is_strictly_ordered)

        status = "INSPECTION_PASSED"
        if not is_valid:
            if has_duplicate_h1:
                status = "DUPLICATED_SECTION_DETECTED"
            elif not is_strictly_ordered:
                status = "WRONG_SECTION_ORDER"
            else:
                status = "STRUCTURAL_DEFECT"

        return {
            "inspection_status": status,
            "verified": is_valid,
            "paragraphs_count": len(doc.paragraphs),
            "h1_headings_count": len(h1_headings),
            "h1_headings_detected": h1_headings[:15],
            "h1_numbers": h1_numbers,
            "has_duplicate_sections": has_duplicate_h1,
            "is_strictly_ordered": is_strictly_ordered,
            "all_14_sections_present": sections_present,
            "h2_subsections_count": len(h2_headings),
            "sec_13_subsections_present": subsecs_present,
            "tables_count": tables_count,
            "has_table_headers": has_table_headers,
            "openxml_rtl_bidi_detected": has_bidi,
            "dubai_font_detected": has_dubai
        }

def main():
    parser = argparse.ArgumentParser(description="Master Persian Research Proposal Word Docx Generator")
    parser.add_argument("input_md", help="Path to input Markdown proposal file")
    parser.add_argument("output_docx", help="Path to output Word .docx file")
    parser.add_argument("--font", default="Dubai", help="Persian font name (default: Dubai)")
    args = parser.parse_args()
    build_proposal_docx(args.input_md, args.output_docx, font_name=args.font)

if __name__ == "__main__":
    main()
