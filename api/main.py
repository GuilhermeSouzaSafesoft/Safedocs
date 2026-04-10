import base64
from io import BytesIO

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from docx import Document

from api.schemas import (
    AppendHistoryTableRequest,
    DocumentSchema,
    HealthResponse,
    PowerAutomateResponse,
    RootResponse,
)
from api.services import generate_docx_from_payload
from safedocs.models import InvalidDocumentError

app = FastAPI(
    title="Safedocs Docx API",
    version="0.1.0",
    servers=[
        {"url": "https://safedocs.onrender.com", "description": "Production"}
    ],
)


@app.get("/", response_model=RootResponse)
def root() -> RootResponse:
    return RootResponse(status="ok", message="Safedocs API pronta para gerar DOCX")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="healthy")


def _payload_to_dict(payload: DocumentSchema) -> dict:
    if hasattr(payload, "model_dump"):
        return payload.model_dump(exclude_none=True)
    return payload.dict(exclude_none=True)


@app.post("/generate-docx")
def generate_docx(payload: DocumentSchema) -> FileResponse:
    try:
        doc_path = generate_docx_from_payload(_payload_to_dict(payload))
    except InvalidDocumentError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return FileResponse(
        path=str(doc_path),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=doc_path.name,
        headers={"Content-Disposition": f'attachment; filename="{doc_path.name}"'},
    )


@app.post("/generate-docx-action", response_model=PowerAutomateResponse)
def generate_docx_action(payload: DocumentSchema) -> PowerAutomateResponse:
    try:
        doc_path = generate_docx_from_payload(_payload_to_dict(payload))
    except InvalidDocumentError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno ao gerar o DOCX.")

    with doc_path.open("rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")

    return PowerAutomateResponse(
        success=True,
        filename=doc_path.name,
        content_base64=encoded,
    )


@app.post("/append-history-table", response_model=PowerAutomateResponse)
def append_history_table(payload: AppendHistoryTableRequest) -> PowerAutomateResponse:
    try:
        source_bytes = base64.b64decode(payload.content_base64)
        document = Document(BytesIO(source_bytes))

        document.add_paragraph()
        document.add_heading("Histórico de Revisões", level=2)

        table = document.add_table(rows=2, cols=3)
        table.rows[0].cells[0].text = "Versão"
        table.rows[0].cells[1].text = "Data"
        table.rows[0].cells[2].text = "Autor"

        table.rows[1].cells[0].text = payload.versao
        table.rows[1].cells[1].text = payload.data
        table.rows[1].cells[2].text = payload.autor

        output = BytesIO()
        document.save(output)
        encoded = base64.b64encode(output.getvalue()).decode("ascii")

        filename = payload.filename
        if filename.lower().endswith(".docx"):
            filename = f"{filename[:-5]}_modificado.docx"
        else:
            filename = f"{filename}_modificado.docx"

        return PowerAutomateResponse(
            success=True,
            filename=filename,
            content_base64=encoded,
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao adicionar tabela de histórico ao DOCX.",
        )
