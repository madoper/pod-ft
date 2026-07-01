__anchor__ = "drafting"
# schema-ref: project-schema.yaml#/services/13

from fastapi import APIRouter

from backend.apps.drafting.app.schemas.draft import (
    DraftRequest,
    DraftResponse,
)
from backend.apps.drafting.app.services.drafting_service import DraftingService

router = APIRouter(tags=["drafting"])
_service = DraftingService()


@router.post("/draft", response_model=DraftResponse)
async def generate_draft(payload: DraftRequest) -> DraftResponse:
    return await _service.generate_draft(
        document_type=payload.document_type,
        subject_type=payload.subject_type,
        context=payload.context,
    )
