from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class BlockType(str, Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    BULLETS = "bullets"
    NUMBERED = "numbered"
    TABLE = "table"
    IMAGE = "image"
    PAGE_BREAK = "page_break"


@dataclass
class Meta:
    document_type: str
    item_name: str
    document_code: str
    revision: str
    date: str
    cover_image_path: Optional[Path] = None


@dataclass
class Block:
    type: BlockType
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentData:
    meta: Meta
    blocks: List[Block]


class InvalidDocumentError(ValueError):
    """Erro de validação para o JSON de entrada."""


def _ensure_key(data: Dict[str, Any], key: str) -> Any:
    if key not in data:
        raise InvalidDocumentError(f"Campo obrigatório ausente: '{key}'")
    return data[key]


def load_document_data(json_data: Dict[str, Any]) -> DocumentData:
    """
    Converte o dicionário carregado do JSON em um objeto DocumentData validado.
    """
    meta_raw = _ensure_key(json_data, "meta")
    blocks_raw = _ensure_key(json_data, "blocks")

    if not isinstance(meta_raw, dict):
        raise InvalidDocumentError("Campo 'meta' deve ser um objeto.")

    if not isinstance(blocks_raw, list):
        raise InvalidDocumentError("Campo 'blocks' deve ser uma lista.")

    meta = Meta(
        document_type=str(meta_raw.get("document_type", "")).strip(),
        item_name=str(meta_raw.get("item_name", "")).strip(),
        document_code=str(meta_raw.get("document_code", "")).strip(),
        revision=str(meta_raw.get("revision", "")).strip(),
        date=str(meta_raw.get("date", "")).strip(),
        cover_image_path=Path(meta_raw["cover_image_path"]) if meta_raw.get("cover_image_path") else None,
    )

    blocks: List[Block] = []
    for index, block_raw in enumerate(blocks_raw):
        if not isinstance(block_raw, dict):
            raise InvalidDocumentError(f"Bloco na posição {index} deve ser um objeto.")

        block_type_value = block_raw.get("type")
        if not block_type_value:
            raise InvalidDocumentError(f"Bloco na posição {index} está sem o campo 'type'.")

        try:
            block_type = BlockType(block_type_value)
        except ValueError:
            raise InvalidDocumentError(f"Tipo de bloco não suportado na posição {index}: '{block_type_value}'.")

        blocks.append(Block(type=block_type, raw=block_raw))

    return DocumentData(meta=meta, blocks=blocks)

