from docx.shared import RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def hex_to_rgb(hex_color: str):
    hex_color = hex_color.replace("#", "").strip()
    return RGBColor(
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16)
    )


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)
