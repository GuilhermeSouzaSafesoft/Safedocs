from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class BlockType(str, Enum):
    PARAGRAFO = "paragrafo"
    SECAO = "secao"
    SUBSECAO = "subsecao"
    SUBSUBSECAO = "subsubsecao"
    SUBSUBSUBSECAO = "subsubsubsecao"
    LISTA = "lista_com_marcadores"
    LISTA_NUMERADA = "lista_numerada"
    TABELA = "tabela"
    IMAGEM = "imagem"
    QUEBRA_DE_PAGINA = "quebra_de_pagina"


@dataclass
class Meta:
    tipo_do_documento: str
    nome_do_item: str
    codigo: str
    revisao: str
    data: str


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


def _normalize_block_type(block_raw: Dict[str, Any], index: int) -> BlockType:
    raw_type = str(block_raw.get("type", "")).strip().lower()
    if not raw_type:
        raise InvalidDocumentError(f"Bloco na posição {index} está sem o campo 'type'.")

    aliases = {
        "paragraph": BlockType.PARAGRAFO,
        "paragrafo": BlockType.PARAGRAFO,
        "heading": None,
        "secao": BlockType.SECAO,
        "subsecao": BlockType.SUBSECAO,
        "subsubsecao": BlockType.SUBSUBSECAO,
        "subsubsubsecao": BlockType.SUBSUBSUBSECAO,
        "title": BlockType.SECAO,
        "bullets": BlockType.LISTA,
        "lista_com_marcadores": BlockType.LISTA,
        "numbered": BlockType.LISTA_NUMERADA,
        "lista_numerada": BlockType.LISTA_NUMERADA,
        "table": BlockType.TABELA,
        "tabela": BlockType.TABELA,
        "image": BlockType.IMAGEM,
        "imagem": BlockType.IMAGEM,
        "page_break": BlockType.QUEBRA_DE_PAGINA,
        "quebra_de_pagina": BlockType.QUEBRA_DE_PAGINA,
    }

    mapped = aliases.get(raw_type)
    if mapped is not None:
        return mapped

    if raw_type == "heading":
        level = block_raw.get("level", 1)
        try:
            level_int = int(level)
        except (TypeError, ValueError):
            raise InvalidDocumentError(f"Valor inválido de 'level' no bloco {index}: '{level}'.")

        if level_int <= 1:
            return BlockType.SECAO
        if level_int == 2:
            return BlockType.SUBSECAO
        if level_int == 3:
            return BlockType.SUBSUBSECAO
        return BlockType.SUBSUBSUBSECAO

    raise InvalidDocumentError(f"Tipo de bloco não suportado na posição {index}: '{raw_type}'.")


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
        tipo_do_documento=str(meta_raw.get("tipo_do_documento", "")).strip(),
        nome_do_item=str(meta_raw.get("nome_do_item", "")).strip(),
        codigo=str(meta_raw.get("codigo", "")).strip(),
        revisao=str(meta_raw.get("revisao", "")).strip(),
        data=str(meta_raw.get("data", "")).strip(),
    )

    blocks: List[Block] = []
    for index, block_raw in enumerate(blocks_raw):
        if not isinstance(block_raw, dict):
            raise InvalidDocumentError(f"Bloco na posição {index} deve ser um objeto.")

        block_type = _normalize_block_type(block_raw, index)
        normalized_raw = {**block_raw, "type": block_type.value}
        blocks.append(Block(type=block_type, raw=normalized_raw))

    return DocumentData(meta=meta, blocks=blocks)
