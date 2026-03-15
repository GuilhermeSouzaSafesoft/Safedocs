import json

from config import JSON_FILE, TEMPLATE_FILE, OUTPUT_DIR, OUTPUT_FILE, PLACEHOLDER_IMAGE
from generator import gerar_documento


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        dados_json = json.load(f)

    gerar_documento(
        dados_json=dados_json,
        template_file=TEMPLATE_FILE,
        output_file=OUTPUT_FILE,
        placeholder_image=PLACEHOLDER_IMAGE
    )

    print(f"Documento gerado com sucesso em: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()