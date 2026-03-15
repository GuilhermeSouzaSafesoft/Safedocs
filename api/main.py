from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from api.schemas import DocumentSchema
from api.services import generate_docx_from_payload
from safedocs.models import InvalidDocumentError

app = FastAPI(title="Safedocs Docx API", version="0.1.0")


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "message": "Safedocs API pronta para gerar DOCX"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/generate-docx")
def generate_docx(payload: DocumentSchema) -> FileResponse:
    try:
        doc_path = generate_docx_from_payload(payload.dict())
    except InvalidDocumentError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return FileResponse(
        path=str(doc_path),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=doc_path.name,
        headers={"Content-Disposition": f'attachment; filename="{doc_path.name}"'},
    )
