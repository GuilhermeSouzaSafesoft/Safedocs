import re
from typing import Any

from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import RGBColor


def slugify_for_filename(value: str) -> str:
    """
    Normalize a string for use as a filename segment.
    """
    if not value:
        return "documento"

    cleaned = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    cleaned = cleaned.strip()
    cleaned = re.sub(r"[\s]+", "_", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned)

    if not cleaned:
        return "documento"

    return cleaned


def hex_to_rgb(hex_color: str) -> RGBColor:
    """
    Converte uma string de cor hexadecimal (com ou sem '#') em RGBColor.
    """
    hex_color = hex_color.replace("#", "").strip()
    return RGBColor(
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )


def set_cell_shading(cell: Any, fill: str) -> None:
    """
    Define a cor de preenchimento de uma célula de tabela DOCX usando um valor hex.
    """
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)
