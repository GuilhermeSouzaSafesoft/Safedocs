from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class MetaSchema(BaseModel):
    tipo_do_documento: str
    nome_do_item: str
    codigo: str
    revisao: str
    data: str


class RunSchema(BaseModel):
    text: str
    style: str | None = None


class BlockSchema(BaseModel):
    type: str
    text: str | None = None
    style: str | None = None
    run_style: str | None = None
    runs: List[RunSchema] | None = None
    items: List[Any] | None = None
    columns: List[str] | None = None
    rows: List[List[Any]] | None = None
    path: str | None = None
    caption: str | None = None

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


class RootResponse(BaseModel):
    status: str
    message: str


class HealthResponse(BaseModel):
    status: str
