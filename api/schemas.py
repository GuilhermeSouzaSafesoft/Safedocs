from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class MetaSchema(BaseModel):
    tipo_do_documento: str
    nome_do_item: str
    codigo: str
    revisao: str
    data: str


class BlockSchema(BaseModel):
    type: str
    text: str | None = None
    level: int | None = None
    items: List[str] | None = None
    columns: List[str] | None = None
    rows: List[List[str]] | None = None

    class Config:
        extra = "allow"


class DocumentSchema(BaseModel):
    meta: MetaSchema
    blocks: List[BlockSchema]

    class Config:
        schema_extra = {
            "example": {
                "meta": {
                    "tipo_do_documento": "Guia rápido",
                    "nome_do_item": "Produto Exemplo",
                    "codigo": "GD-0001",
                    "revisao": "A",
                    "data": "2026-03-15",
                },
                "blocks": [
                    {"type": "secao", "text": "Seção 1"},
                    {"type": "paragrafo", "text": "Texto de exemplo."},
                    {
                        "type": "tabela",
                        "columns": ["Coluna A", "Coluna B"],
                        "rows": [["Valor 1", "Valor 2"]],
                    },
                ],
            }
        }


class ActionFile(BaseModel):
    name: str
    content: str
    mime_type: str = Field(
        default="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


class ActionResponse(BaseModel):
    openaiFileResponse: List[ActionFile]


class PowerAutomateResponse(BaseModel):
    success: bool = True
    filename: str
    mime_type: str = Field(
        default="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    content_base64: str


class RootResponse(BaseModel):
    status: str
    message: str


class HealthResponse(BaseModel):
    status: str
