#!/usr/bin/env python3
"""
Master Persian Academic Word Document (.docx) Generator for Proposal-Nevisi Skill
Faithfully implements the approved layout: Dubai typography, section-level and paragraph-level
Word-native RTL (<w:bidi/>, <w:rtlGutter/>), Complex Script bolding (<w:bCs/>), bidi text tokenization,
no horizontal dashes, clean formula callout boxes, and styled tables.
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

def set_p_rtl(p, space_before=2.5, space_after=3.5, line_spacing=1.15, align="both"):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    pPr = p._p.get_or_add_pPr()
    
    bidi = pPr.find(qn('w:bidi'))
    if bidi is None:
        pPr.append(parse_xml(r'<w:bidi {}/>'.format(nsdecls('w'))))
        
    target_jc = "both" if align in ["justify", "both"] else align
    jc = pPr.find(qn('w:jc'))
    if jc is None:
        pPr.append(parse_xml(r'<w:jc {} w:val="{}"/>'.format(nsdecls('w'), target_jc)))
    else:
        jc.set(qn('w:val'), target_jc)

def add_r(p, text, font_name="Dubai", size_pt=11, bold=False, italic=False, color_rgb=(0x00, 0x00, 0x00), is_rtl=True):
    if text is not None:
        text = str(text).replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
    run = p.add_run(text)
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)
    rPr = run._r.get_or_add_rPr()
    
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = parse_xml(r'<w:rFonts {} w:ascii="{}" w:hAnsi="{}" w:cs="{}"/>'.format(nsdecls('w'), font_name, font_name, font_name))
        rPr.append(rFonts)
    else:
        rFonts.set(qn('w:cs'), font_name)
        rFonts.set(qn('w:ascii'), font_name)
        rFonts.set(qn('w:hAnsi'), font_name)
        
    rtl_elem = rPr.find(qn('w:rtl'))
    if is_rtl:
        if rtl_elem is None:
            rPr.append(parse_xml(r'<w:rtl {} w:val="1"/>'.format(nsdecls('w'))))
        else:
            rtl_elem.set(qn('w:val'), '1')
    else:
        if rtl_elem is not None:
            rPr.remove(rtl_elem)
            
    sz_half_pts = str(int(round(size_pt * 2)))
    sz_elem = rPr.find(qn('w:sz'))
    if sz_elem is None:
        rPr.append(parse_xml(r'<w:sz {} w:val="{}"/>'.format(nsdecls('w'), sz_half_pts)))
    else:
        sz_elem.set(qn('w:val'), sz_half_pts)
        
    szCs_elem = rPr.find(qn('w:szCs'))
    if szCs_elem is None:
        rPr.append(parse_xml(r'<w:szCs {} w:val="{}"/>'.format(nsdecls('w'), sz_half_pts)))
    else:
        szCs_elem.set(qn('w:val'), sz_half_pts)
        
    bCs_elem = rPr.find(qn('w:bCs'))
    if bold:
        if bCs_elem is None:
            rPr.append(parse_xml(r'<w:bCs {}/>'.format(nsdecls('w'))))
    else:
        if bCs_elem is not None:
            rPr.remove(bCs_elem)
            
    iCs_elem = rPr.find(qn('w:iCs'))
    if italic:
        if iCs_elem is None:
            rPr.append(parse_xml(r'<w:iCs {}/>'.format(nsdecls('w'))))
    else:
        if iCs_elem is not None:
            rPr.remove(iCs_elem)
            
    return run

def add_bidi_text(p, text, font_name="Dubai", size_pt=11, bold=False, italic=False, color_rgb=(0x00, 0x00, 0x00)):
    if not text:
        return
    if NativeOmmlMathEngine is not None:
        try:
            text = NativeOmmlMathEngine.clean_text_of_latex(text)
        except Exception:
            pass
    text = str(text).replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
    pattern = r'(\([A-Za-z0-9_\-\s,\./%α-ωΑ-Ω→⇌⇄<>=\+\^±]+\)|\[\d+(?:,\s*\d+)*\]|[A-Za-z0-9_\-\./%α-ωΑ-Ω\+\^±]+(?:\s*(?:→|->|⇌|<->|⇄|<=|>=|<|>|=)\s*[A-Za-z0-9_\-\./%α-ωΑ-Ω\+\^±]+)+|[A-Za-z0-9_\-\./%α-ωΑ-Ω\+\^±]{2,}|[→⇌⇄]|(?:<=|>=|[<>=])\s*\d+(?:\.\d+)?)'
    tokens = re.split(pattern, text)
    for tok in tokens:
        if not tok:
            continue
        has_persian = any('\u0600' <= c <= '\u06FF' for c in tok)
        if re.match(r'^\[\d+(?:,\s*\d+)*\]$', tok.strip()):
            add_r(p, " " + tok.strip() + " ", font_name=font_name, size_pt=size_pt, bold=True, italic=False, color_rgb=(0x00, 0x00, 0x00), is_rtl=False)
        elif not has_persian and (re.search(r'[A-Za-z0-9→⇌⇄<>=]', tok) or tok.startswith('(')):
            add_r(p, " " + tok.strip() + " ", font_name=font_name, size_pt=size_pt, bold=bold, italic=italic, color_rgb=color_rgb, is_rtl=False)
        else:
            add_r(p, tok, font_name=font_name, size_pt=size_pt, bold=bold, italic=italic, color_rgb=color_rgb, is_rtl=True)

def add_formatted_bidi_text(p, text, font_name="Dubai", size_pt=11, default_bold=False, default_italic=False, color_rgb=(0x00, 0x00, 0x00)):
    segments = re.split(r'(\*\*.*?\*\*|\*.*?\*)', text)
    for seg in segments:
        if not seg:
            continue
        b = default_bold
        it = default_italic
        clean = seg
        if seg.startswith('**') and seg.endswith('**'):
            b = True
            clean = seg[2:-2]
        elif seg.startswith('*') and seg.endswith('*'):
            it = True
            clean = seg[1:-1]
        add_bidi_text(p, clean, font_name=font_name, size_pt=size_pt, bold=b, italic=it, color_rgb=color_rgb)

def add_title(doc, main_title):
    p = doc.add_paragraph()
    set_p_rtl(p, space_before=18, space_after=14, align="both")
    add_r(p, main_title, font_name="Dubai", size_pt=16, bold=True, color_rgb=(0x00, 0x00, 0x00))
    return p

def add_h1(doc, text):
    p = doc.add_paragraph()
    set_p_rtl(p, space_before=16, space_after=6, align="both")
    add_formatted_bidi_text(p, text, font_name="Dubai", size_pt=14, default_bold=True, color_rgb=(0x00, 0x00, 0x00))
    return p

def add_h2(doc, text):
    p = doc.add_paragraph()
    set_p_rtl(p, space_before=12, space_after=4, align="both")
    add_formatted_bidi_text(p, text, font_name="Dubai", size_pt=11.5, default_bold=True, color_rgb=(0x00, 0x00, 0x00))
    return p

def add_h3(doc, text):
    p = doc.add_paragraph()
    set_p_rtl(p, space_before=10, space_after=3, align="both")
    add_formatted_bidi_text(p, text, font_name="Dubai", size_pt=11, default_bold=True, color_rgb=(0x00, 0x00, 0x00))
    return p

def add_body_p(doc, text):
    p = doc.add_paragraph()
    set_p_rtl(p, space_before=2.5, space_after=3.5, line_spacing=1.15, align="both")
    add_formatted_bidi_text(p, text, font_name="Dubai", size_pt=11, color_rgb=(0x00, 0x00, 0x00))
    return p

def add_bullet_p(doc, text):
    p = doc.add_paragraph()
    set_p_rtl(p, space_before=2, space_after=2, align="both")
    add_r(p, "▪  ", font_name="Dubai", size_pt=10.5, bold=True, color_rgb=(0x00, 0x00, 0x00))
    add_formatted_bidi_text(p, text, font_name="Dubai", size_pt=11, color_rgb=(0x00, 0x00, 0x00))
    return p

def add_numbered_p(doc, num, text):
    p = doc.add_paragraph()
    set_p_rtl(p, space_before=2.5, space_after=2.5, align="both")
    add_r(p, f"{num}. ", font_name="Dubai", size_pt=11, bold=True, color_rgb=(0x00, 0x00, 0x00))
    add_formatted_bidi_text(p, text, font_name="Dubai", size_pt=11, color_rgb=(0x00, 0x00, 0x00))
    return p

def add_ref_item(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    pPr = p._p.get_or_add_pPr()
    jc = pPr.find(qn('w:jc'))
    if jc is None:
        pPr.append(parse_xml(r'<w:jc {} w:val="both"/>'.format(nsdecls('w'))))
    else:
        jc.set(qn('w:val'), 'both')
    add_r(p, text, font_name="Times New Roman", size_pt=10, bold=False, color_rgb=(0x00, 0x00, 0x00), is_rtl=False)
    return p

def add_formula_box(doc, formula_text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.2
    pPr = p._p.get_or_add_pPr()
    
    pPr.append(parse_xml(r'<w:bidi {}/>'.format(nsdecls('w'))))
    jc = pPr.find(qn('w:jc'))
    if jc is None:
        pPr.append(parse_xml(r'<w:jc {} w:val="both"/>'.format(nsdecls('w'))))
    else:
        jc.set(qn('w:val'), 'both')
        
    pPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8F9FA"/>'))
    
    pBdr = parse_xml(f'''<w:pBdr {nsdecls("w")}>
        <w:top w:val="single" w:sz="4" w:space="4" w:color="D5D8DC"/>
        <w:left w:val="single" w:sz="12" w:space="8" w:color="5D6D7E"/>
        <w:bottom w:val="single" w:sz="4" w:space="4" w:color="D5D8DC"/>
        <w:right w:val="single" w:sz="4" w:space="4" w:color="D5D8DC"/>
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
    run.font.color.rgb = RGBColor(0x1B, 0x26, 0x31)
    rPr = run._r.get_or_add_rPr()
    rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>')
    rPr.append(rFonts)
    return p

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_cell_borders(cell, color="D3D3D3"):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)

def render_styled_table(doc, table_lines):
    rows = []
    for line in table_lines:
        line_clean = line.strip()
        if not line_clean or line_clean.startswith('|:--') or line_clean.startswith('|---'):
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
                set_p_rtl(p, space_before=2, space_after=2, align="center")

                if is_header:
                    add_r(p, cell_value, font_name="Dubai", size_pt=10.5, bold=True, color_rgb=(0x1B, 0x26, 0x31))
                    tcPr = cell._tc.get_or_add_tcPr()
                    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F1F4F8"/>'))
                else:
                    if cell_value == '■■■■':
                        add_r(p, cell_value, font_name="Dubai", size_pt=10, bold=True, color_rgb=(0x2E, 0x86, 0xC1))
                    else:
                        add_r(p, cell_value, font_name="Dubai", size_pt=10, bold=False, color_rgb=(0x2C, 0x3E, 0x50))

                set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
                set_cell_borders(cell, color="D3D3D3")

    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(4)
    sp.paragraph_format.space_after = Pt(6)

def build_proposal_docx(md_path, output_docx_path, font_name="Dubai"):
    doc = Document()

    # Section-level native RTL and Page Setup
    for s in doc.sections:
        s.page_width = Inches(8.27)
        s.page_height = Inches(11.69)
        s.top_margin = Inches(1)
        s.bottom_margin = Inches(1)
        s.left_margin = Inches(1)
        s.right_margin = Inches(1)
        s._sectPr.append(parse_xml(f'<w:bidi {nsdecls("w")}/>'))
        s._sectPr.append(parse_xml(f'<w:rtlGutter {nsdecls("w")}/>'))

    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_table = False
    table_lines = []
    is_refs = False

    for line in lines:
        stripped = line.strip()

        # Handle Markdown Tables
        if stripped.startswith('|') and stripped.endswith('|'):
            in_table = True
            table_lines.append(stripped)
            continue
        elif in_table:
            render_styled_table(doc, table_lines)
            table_lines = []
            in_table = False

        # Strictly skip empty lines and horizontal rule dashes
        if not stripped or stripped == '---':
            continue

        if (('۱۴.' in stripped or '14.' in stripped) or ('۲۸.' in stripped or '28.' in stripped)) and 'منابع' in stripped:
            is_refs = True

        if stripped.startswith('# '):
            add_title(doc, stripped[2:])
        elif stripped.startswith('## '):
            add_h1(doc, stripped[3:])
        elif stripped.startswith('### '):
            add_h2(doc, stripped[4:])
        elif stripped.startswith('#### '):
            add_h3(doc, stripped[5:])
        elif is_refs and re.match(r'^\d+\.\s+', stripped):
            add_ref_item(doc, stripped)
        # Check for formula blocks ($$...$$, \[...\], n = \frac, CI =, etc.)
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
            add_bullet_p(doc, stripped[2:])
        elif re.match(r'^\d+\.\s+', stripped):
            m = re.match(r'^(\d+)\.\s+(.*)', stripped)
            add_numbered_p(doc, m.group(1), m.group(2))
        else:
            add_body_p(doc, stripped)

    if in_table and table_lines:
        render_styled_table(doc, table_lines)

    # Save via temporary ASCII path to avoid Windows path encoding bugs
    temp_dir = tempfile.gettempdir()
    temp_docx = os.path.join(temp_dir, "master_temp_out.docx")
    doc.save(temp_docx)

    shutil.copy2(temp_docx, output_docx_path)
    if os.path.exists(temp_docx):
        os.remove(temp_docx)

    print(f"Master Word DOCX successfully generated at: {output_docx_path}", file=sys.stderr)

class DocxBuilder:
    """Wrapper class providing programmatic interface for document generation."""

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
        """Performs authentic structural and typographic inspection of a generated Word .docx file (Phase 22).
        Verifies presence of 14 sections, Section 13 subsections, tables, bidi RTL, Dubai font, and section ordering.
        """
        if not os.path.exists(docx_path):
            return {
                "inspection_status": "FILE_NOT_FOUND",
                "file_exists": False,
                "verified": False
            }

        try:
            doc = Document(docx_path)
        except Exception as e:
            return {
                "inspection_status": "MALFORMED_DOCX",
                "verified": False,
                "error": str(e)
            }

        if len(doc.paragraphs) == 0 and len(doc.tables) == 0:
            return {
                "inspection_status": "EMPTY_DOCX",
                "verified": False,
                "paragraphs_count": 0,
                "tables_count": 0
            }

        # Check headings
        h1_headings: List[str] = []
        h2_headings: List[str] = []
        h1_numbers: List[int] = []
        has_bidi = False
        has_dubai = False

        PERSIAN_TO_INT = {
            "۱": 1, "۲": 2, "۳": 3, "۴": 4, "۵": 5, "۶": 6, "۷": 7, "۸": 8, "۹": 9,
            "۱۰": 10, "۱۱": 11, "۱۲": 12, "۱۳": 13, "۱۴": 14
        }

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
                num_str = m_h1.group(1)
                num_val = int(num_str) if num_str.isdigit() else PERSIAN_TO_INT.get(num_str)
                if num_val and 1 <= num_val <= 14:
                    h1_headings.append(p_text)
                    h1_numbers.append(num_val)
            elif re.match(r'^(?:13|۱۳)\-(?:[0-9]{1,2}|[۰-۹]{1,2})\.\s+', p_text):
                h2_headings.append(p_text)

        # Check tables
        tables_count = len(doc.tables)
        has_table_headers = False
        if tables_count > 0:
            first_tbl = doc.tables[0]
            if len(first_tbl.rows) > 0 and len(first_tbl.rows[0].cells) > 0:
                has_table_headers = True

        all_14_present = len(h1_headings) >= 14
        sec_13_subsecs_present = len(h2_headings) >= 14

        # Check order and duplicates
        has_duplicate_h1 = len(h1_numbers) != len(set(h1_numbers))
        is_strictly_ordered = (h1_numbers == sorted(h1_numbers)) if h1_numbers else False

        is_valid = bool(all_14_present and sec_13_subsecs_present and has_bidi and has_dubai and tables_count >= 2 and not has_duplicate_h1 and is_strictly_ordered)

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
            "all_14_sections_present": all_14_present,
            "h2_subsections_count": len(h2_headings),
            "sec_13_subsections_present": sec_13_subsecs_present,
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
