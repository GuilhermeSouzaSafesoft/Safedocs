
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"

TEMPLATE_FILE = TEMPLATES_DIR / "template.docx"
JSON_FILE = DATA_DIR / "dados_json.json"
OUTPUT_FILE = OUTPUT_DIR / "documento_final.docx"
PLACEHOLDER_IMAGE = TEMPLATES_DIR / "imagem.png"
