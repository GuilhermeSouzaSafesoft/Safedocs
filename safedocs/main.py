import json

from .config import JSON_FILE, OUTPUT_DIR, OUTPUT_FILE, PLACEHOLDER_IMAGE, TEMPLATE_FILE
from .generator import gerar_documento, validar_arquivos
from .models import DocumentData, load_document_data


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    validar_arquivos(TEMPLATE_FILE, JSON_FILE)

    with JSON_FILE.open("r", encoding="utf-8") as f:
        raw_data = json.load(f)

    document_data: DocumentData = load_document_data(raw_data)

    gerar_documento(
        dados=document_data,
        template_file=TEMPLATE_FILE,
        output_file=OUTPUT_FILE,
        placeholder_image=PLACEHOLDER_IMAGE,
    )

    print(f"Documento gerado com sucesso em: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()