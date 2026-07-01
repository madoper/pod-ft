__anchor__ = "answer-service"
# schema-ref: project-schema.yaml#/services/10

from fastapi import APIRouter

from backend.apps.answer_service.app.schemas.answer import (
    AnswerDto,
    AnswerQuestionRequest,
    AnswerQuestionResponse,
)
from backend.apps.answer_service.app.services.answering_service import AnsweringService

router = APIRouter(tags=["questions"])
_service = AnsweringService()


@router.post("/questions/answer", response_model=AnswerQuestionResponse)
async def answer_question(payload: AnswerQuestionRequest) -> AnswerQuestionResponse:
    result = await _service.answer(
        question=payload.question,
        channel=payload.channel,
        subject_type=payload.subject_type,
        regulator=payload.regulator,
        as_of_date=payload.as_of_date,
    )
    return AnswerQuestionResponse(
        answer_session_id=result["session_id"],
        status=result["status"],
        answer=AnswerDto(**result["answer"]) if result.get("answer") else None,
        reason_code=result.get("reason_code"),
        evidence_count=result.get("evidence_count", 0),
        verifier_status=result.get("verifier_status"),
        anchor="answer-service",
    )


@router.get("/questions/{session_id}", response_model=AnswerQuestionResponse)
async def get_answer_status(session_id: str) -> AnswerQuestionResponse:
    result = await _service.get_session(session_id)
    if not result:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Session not found")
    return AnswerQuestionResponse(
        answer_session_id=result["session_id"],
        status=result["status"],
        answer=AnswerDto(**result["answer"]) if result.get("answer") else None,
        reason_code=result.get("reason_code"),
        evidence_count=result.get("evidence_count", 0),
        verifier_status=result.get("verifier_status"),
        anchor="answer-service",
    )
