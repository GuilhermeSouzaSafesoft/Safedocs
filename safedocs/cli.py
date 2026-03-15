import argparse
from pathlib import Path
import json

from .config import JSON_FILE, OUTPUT_DIR, OUTPUT_FILE, PLACEHOLDER_IMAGE, TEMPLATE_FILE
from .generator import gerar_documento, validar_arquivos
from .models import DocumentData, load_document_data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera documentos DOCX a partir de arquivos JSON usando o template Safesoft."
    )

    parser.add_argument(
        "--json",
        type=Path,
        default=JSON_FILE,
        help=f"Caminho do arquivo JSON de entrada (padrão: {JSON_FILE})",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=TEMPLATE_FILE,
        help=f"Caminho do arquivo DOCX de template (padrão: {TEMPLATE_FILE})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_FILE,
        help=f"Caminho do arquivo DOCX de saída (padrão: {OUTPUT_FILE})",
    )
    parser.add_argument(
        "--placeholder-image",
        type=Path,
        default=PLACEHOLDER_IMAGE,
        help=f"Imagem padrão para capa ou imagens faltantes (padrão: {PLACEHOLDER_IMAGE})",
    )

    return parser.parse_args()


def run_from_cli() -> None:
    args = parse_args()

    output_dir = args.output.parent
    output_dir.mkdir(exist_ok=True, parents=True)

    validar_arquivos(args.template, args.json)

    with args.json.open("r", encoding="utf-8") as f:
        raw_data = json.load(f)

    document_data: DocumentData = load_document_data(raw_data)

    gerar_documento(
        dados=document_data,
        template_file=args.template,
        output_file=args.output,
        placeholder_image=args.placeholder_image,
    )

    print(f"Documento gerado com sucesso em: {args.output}")


if __name__ == "__main__":
    run_from_cli()

