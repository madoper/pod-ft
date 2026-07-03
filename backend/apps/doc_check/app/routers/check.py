__anchor__ = "doc-check"
# schema-ref: project-schema.yaml#/services/12

from fastapi import APIRouter, HTTPException

from backend.apps.doc_check.app.schemas.check import (
    CheckRequest,
    CheckResponse,
    JobStatusResponse,
)
from backend.apps.doc_check.app.services.check_service import DocCheckService

router = APIRouter(tags=["doc-check"])
_service = DocCheckService()


@router.post("/check", response_model=CheckResponse)
async def check_document(payload: CheckRequest) -> CheckResponse:
    return await _service.submit_check(
        tenant_id=payload.tenant_id,
        document_text=payload.document_text,
        document_title=payload.document_title,
        document_type=payload.document_type,
        subject_type=payload.subject_type,
    )


@router.get("/check/{job_id}", response_model=JobStatusResponse)
async def get_check_status(job_id: str) -> JobStatusResponse:
    result = await _service.get_job(job_id)
    if not result:
        raise HTTPException(status_code=404, detail="Job not found")
    return result
