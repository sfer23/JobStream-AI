from fpdf import FPDF
import os
import re
from .asset_manager import get_emoji_path, ensure_assets

class CV_PDF(FPDF):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_font_family = "helvetica"

    def footer(self):
        # Footer removed as per user request
        pass

def generate_pdf(md_content, output_path, photo_path=None, assets_dir="assets/icons", hidden_prompt=None):
    # Ensure assets exist before generation
    ensure_assets(assets_dir)

    # 1. Pre-process markdown
    clean_content = md_content.strip()
    if clean_content.startswith("```"):
        first_newline = clean_content.find('\n')
        if first_newline != -1:
            clean_content = clean_content[first_newline:].strip()
        if clean_content.endswith("```"):
            clean_content = clean_content[:-3].strip()

    pdf = CV_PDF()
    pdf.alias_nb_pages()
    pdf.set_margins(15, 15, 15)
    page_width = 180 
    usable_page_height = 282 - 15 
    
    # Load Fonts
    windir = os.environ.get('WINDIR', 'C:\\Windows')
    fonts_dir = os.path.join(windir, 'Fonts')
    
    main_font_family = "helvetica"
    try:
        # Try to use existing project fonts if available, or system fonts
        pdf.add_font("SegoeUI", "", os.path.join(fonts_dir, "segoeui.ttf"))
        pdf.add_font("SegoeUI", "B", os.path.join(fonts_dir, "segoeuib.ttf"))
        pdf.add_font("SegoeUI", "I", os.path.join(fonts_dir, "segoeuii.ttf"))
        
        symbol_font = os.path.join(fonts_dir, "seguisym.ttf")
        if os.path.exists(symbol_font):
            pdf.add_font("SymbolFont", "", symbol_font)
            pdf.add_font("SymbolFont", "B", symbol_font)
            pdf.set_fallback_fonts(["SymbolFont"])
            
        pdf.set_font("SegoeUI", size=11)
        pdf.main_font_family = "SegoeUI"
        main_font_family = "SegoeUI"
    except Exception as e:
        print(f"Font loading failed: {e}")
        pdf.set_font("helvetica", size=11)

    pdf.add_page()
    
    # --- Parse content ---
    lines = clean_content.split('\n')
    header_lines = []
    body_lines = []
    found_first_hr = False
    for line in lines:
        if not found_first_hr and line.startswith('---'):
            found_first_hr = True
            continue
        if not found_first_hr:
            header_lines.append(line)
        else:
            body_lines.append(line)

    def render_styled_line(text, indent=0):
        """Advanced parser for MD links, bold, and raw URLs/emails/phones"""
        pdf.set_left_margin(15 + indent)
        pdf.set_x(15 + indent)
        
        regex = (
            r'(\[.*?\]\(.*?\))|'              # [label](url)
            r'(\*\*.*?\*\*)|'                 # **bold**
            r'(https?://[^\s)\]]+)|'          # raw URL
            r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})|' # raw Email
            r'(\+\d[\d\s]{7,15}\d)'           # raw Phone
        )
        parts = re.split(regex, text)
        for part in parts:
            if part is None or part == "": continue
            m = re.match(r'\[(.*?)\]\((.*?)\)', part)
            if m:
                label, url = m.groups()
                pdf.set_text_color(41, 128, 185)
                pdf.write(6, label, link=url)
                pdf.set_text_color(0, 0, 0)
                continue
            m = re.match(r'\*\*(.*?)\*\*', part)
            if m:
                pdf.set_font(main_font_family, "B", 11)
                pdf.write(6, m.group(1))
                pdf.set_font(main_font_family, "", 11)
                continue
            if part.startswith('http'):
                pdf.set_text_color(41, 128, 185)
                pdf.write(6, part, link=part)
                pdf.set_text_color(0, 0, 0)
                continue
            if '@' in part and '.' in part:
                pdf.set_text_color(41, 128, 185)
                pdf.write(6, part, link=f"mailto:{part}")
                pdf.set_text_color(0, 0, 0)
                continue
            if part.startswith('+') and any(c.isdigit() for c in part):
                clean_phone = re.sub(r'[^\d+]', '', part)
                pdf.set_text_color(41, 128, 185)
                pdf.write(6, part, link=f"tel:{clean_phone}")
                pdf.set_text_color(0, 0, 0)
                continue
            pdf.write(6, part)
        
        pdf.ln(6)
        pdf.set_left_margin(15)

    # --- Header Section ---
    original_y = pdf.get_y()
    info_start_x = 15
    if photo_path and os.path.exists(photo_path):
        pdf.image(photo_path, x=15, y=original_y, w=35)
        info_start_x = 55
    
    pdf.set_xy(info_start_x, original_y)
    pdf.set_text_color(44, 62, 80)
    for line in header_lines:
        text = line.strip()
        if not text: continue
        if line.startswith('# '):
            pdf.set_font(main_font_family, "B", 18)
            pdf.multi_cell(page_width - (info_start_x - 15), 10, text[2:])
            pdf.set_font(main_font_family, size=11)
        else:
            render_styled_line(text, indent=info_start_x - 15)

    if pdf.get_y() < original_y + 42 and info_start_x > 15:
        pdf.set_y(original_y + 42)
    else:
        pdf.ln(5)

    # --- Body Content Structuring ---
    sections = []
    current_section = []
    for line in body_lines:
        if line.startswith('## '):
            if current_section: sections.append(current_section)
            current_section = [line]
        else:
            current_section.append(line)
    if current_section: sections.append(current_section)

    def get_emoji_info_local(text):
        for char in text:
            if ord(char) > 0x2000:
                path = get_emoji_path(char, assets_dir)
                if path: return path, char
        return None, None

    def calculate_section_height(section_lines):
        h = 0
        h += 5
        for l in section_lines:
            lr = l.strip()
            if not lr: h += 1
            elif lr.startswith('---'): h += 8
            elif lr.startswith('## '): h += 15
            elif lr.startswith('### '): h += 10
            else:
                txt_clean = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', lr)
                txt_clean = re.sub(r'\*\*(.*?)\*\*', r'\1', txt_clean)
                lines_count = len(pdf.multi_cell(page_width, 6, txt_clean, split_only=True))
                h += lines_count * 6
        return h

    # --- Render Sections ---
    pdf.set_text_color(0, 0, 0)
    pending_hr = False

    for i, section in enumerate(sections):
        section_h = calculate_section_height(section)
        remaining_h = usable_page_height - pdf.get_y()
        if section_h > remaining_h and section_h <= (usable_page_height - 30):
            pdf.add_page()
            pending_hr = False
        
        if pending_hr and pdf.get_y() > 30:
            pdf.set_draw_color(200, 200, 200)
            pdf.line(15, pdf.get_y() + 2, 195, pdf.get_y() + 2)
            pdf.ln(4)
        pending_hr = False

        in_list = False 
        for line in section:
            line_raw_stripped = line.strip()
            if not line_raw_stripped:
                in_list = False
                pdf.ln(1)
                continue
            if line_raw_stripped.startswith('---'):
                in_list = False
                pending_hr = True
                continue
            
            if line_raw_stripped.startswith('## '):
                in_list = False
                pdf.ln(2)
                header_text = line_raw_stripped[3:].strip()
                icon_path, emoji_char = get_emoji_info_local(header_text)
                if icon_path:
                    header_text = header_text.replace(emoji_char, "").strip()
                    pdf.image(icon_path, x=16, y=pdf.get_y() + 1, h=6)
                    pdf.set_x(24)
                else:
                    pdf.set_x(15)
                pdf.set_font(main_font_family, "B", 14)
                pdf.set_text_color(41, 128, 185)
                pdf.multi_cell(0, 8, header_text)
                pdf.set_font(main_font_family, size=11)
                pdf.set_text_color(0, 0, 0)
                
            elif line_raw_stripped.startswith('### '):
                in_list = False
                if pdf.get_y() > usable_page_height - 10: pdf.add_page()
                pdf.set_font(main_font_family, "B", 12)
                pdf.multi_cell(0, 8, line_raw_stripped[4:])
                pdf.set_font(main_font_family, size=11)
                
            elif line_raw_stripped.startswith('- '):
                in_list = True 
                if pdf.get_y() > usable_page_height - 10: pdf.add_page()
                pdf.set_x(20)
                pdf.write(6, "- ")
                render_styled_line(line_raw_stripped[2:], indent=10)
                
            else:
                if pdf.get_y() > usable_page_height - 10: pdf.add_page()
                if in_list:
                    render_styled_line(line_raw_stripped, indent=10)
                else:
                    render_styled_line(line_raw_stripped, indent=0)
        
        if i < len(sections) - 1: pending_hr = True

    if hidden_prompt:
        # Invisible text injection
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(main_font_family, size=1)
        #pdf.ln(5)
        pdf.write(1, hidden_prompt)

    pdf.output(output_path)
