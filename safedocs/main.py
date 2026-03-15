import json

from .config import JSON_FILE, OUTPUT_DIR, OUTPUT_FILE, PLACEHOLDER_IMAGE, TEMPLATE_FILE
from .generator import gerar_documento, validar_arquivos
from .models import DocumentData, load_document_data
from .utils import slugify_for_filename


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    validar_arquivos(TEMPLATE_FILE, JSON_FILE)

    with JSON_FILE.open("r", encoding="utf-8") as f:
        raw_data = json.load(f)

    document_data: DocumentData = load_document_data(raw_data)

    nome_arquivo = f"{slugify_for_filename(document_data.meta.codigo)}-{slugify_for_filename(document_data.meta.tipo_do_documento)}.docx"
    final_output = OUTPUT_DIR / nome_arquivo

    gerar_documento(
        dados=document_data,
        template_file=TEMPLATE_FILE,
        output_file=final_output,
        placeholder_image=PLACEHOLDER_IMAGE,
    )

    print(f"Documento gerado com sucesso em: {final_output}")


if __name__ == "__main__":
    main()
