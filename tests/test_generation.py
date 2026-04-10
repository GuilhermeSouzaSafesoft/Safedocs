from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from safedocs.config import BASE_DIR, DATA_DIR, TEMPLATE_FILE
from safedocs.generator import gerar_documento
from safedocs.models import DocumentData, load_document_data


def test_generate_document_from_sample_json(tmp_path: Path) -> None:
    """
    Gera um documento a partir do JSON de exemplo apenas para garantir
    que não ocorra nenhuma exceção durante o fluxo principal.
    """
    json_path = DATA_DIR / "dados_json.json"
    assert json_path.exists()
    assert TEMPLATE_FILE.exists()

    with json_path.open("r", encoding="utf-8") as f:
        raw_data = json.load(f)

    data: DocumentData = load_document_data(raw_data)

    output_file = tmp_path / "doc_test.docx"
    gerar_documento(
        dados=data,
        template_file=TEMPLATE_FILE,
        output_file=output_file,
        placeholder_image=BASE_DIR / "templates" / "imagem.png",
    )

    assert output_file.exists()
