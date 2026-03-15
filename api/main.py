import base64

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from api.schemas import (
    ActionFile,
    ActionResponse,
    DocumentSchema,
    HealthResponse,
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
        return payload.model_dump()
    return payload.dict()


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


@app.post("/generate-docx-action", response_model=ActionResponse)
def generate_docx_action(payload: DocumentSchema) -> ActionResponse:
    try:
        doc_path = generate_docx_from_payload(_payload_to_dict(payload))
    except InvalidDocumentError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    with doc_path.open("rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")

    action_file = ActionFile(
        name=doc_path.name,
        content=encoded,
    )

    return ActionResponse(openaiFileResponse=[action_file])
