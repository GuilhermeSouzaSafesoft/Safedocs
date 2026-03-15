from __future__ import annotations

from pathlib import Path
from typing import Mapping

from safedocs.config import OUTPUT_DIR, PLACEHOLDER_IMAGE, TEMPLATE_FILE
from safedocs.generator import gerar_documento
from safedocs.models import DocumentData, load_document_data
from safedocs.utils import slugify_for_filename


def generate_docx_from_payload(payload: Mapping[str, object], *, output_dir: Path | None = None) -> Path:
    """
    Converte o JSON recebido pela API em DocumentData e chama o gerador existente.
    Retorna o path para o arquivo gerado.
    """
    document_data: DocumentData = load_document_data(payload)

    target_dir = output_dir or OUTPUT_DIR
    target_dir.mkdir(exist_ok=True, parents=True)

    filename = f"{slugify_for_filename(document_data.meta.codigo)}-{slugify_for_filename(document_data.meta.tipo_do_documento)}.docx"
    output_file = target_dir / filename

    gerar_documento(
        dados=document_data,
        template_file=TEMPLATE_FILE,
        output_file=output_file,
        placeholder_image=PLACEHOLDER_IMAGE,
    )

    return output_file
