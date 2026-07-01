__anchor__ = "tests"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.answer_service.app.main import app


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_answer_question(client: AsyncClient) -> None:
    # First index some fragments
    from backend.apps.answer_service.app.services.answering_service import AnsweringService
    svc = AnsweringService()
    await svc._retrieval.index_fragments([
        {
            "fragment_id": "a1",
            "document_title": "AML Law",
            "fragment_text": (
                "Субъект обязан разработать правила внутреннего контроля"
                " в соответствии с требованиями."
            ),
            "citation_label": "ст. 7",
            "tier": 1,
            "source_domain": "fedsfm.ru",
        },
        {
            "fragment_id": "a2",
            "document_title": "AML Law",
            "fragment_text": "Правила внутреннего контроля утверждаются руководителем организации.",
            "citation_label": "ст. 8",
            "tier": 1,
            "source_domain": "fedsfm.ru",
        },
    ])

    # Also need to re-init the service instance created by the router
    from backend.apps.answer_service.app.routers.answer import _service
    await _service._retrieval.index_fragments([
        {
            "fragment_id": "a1",
            "document_title": "AML Law",
            "fragment_text": (
                "Субъект обязан разработать правила внутреннего контроля"
                " в соответствии с требованиями."
            ),
            "citation_label": "ст. 7",
            "tier": 1,
            "source_domain": "fedsfm.ru",
        },
        {
            "fragment_id": "a2",
            "document_title": "AML Law",
            "fragment_text": "Правила внутреннего контроля утверждаются руководителем организации.",
            "citation_label": "ст. 8",
            "tier": 1,
            "source_domain": "fedsfm.ru",
        },
    ])

    resp = await client.post("/api/v1/questions/answer", json={
        "channel": "web",
        "question": "Какие требования к правилам внутреннего контроля?",
        "subject_type": "article_7_1",
        "regulator": "fedsfm.ru",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["answer"]["summary"]
    assert len(data["answer"]["citations"]) >= 1
    assert data["anchor"] == "answer-service"


@pytest.mark.asyncio
async def test_answer_no_fragments(client: AsyncClient) -> None:
    """Should refuse when no indexed fragments match."""
    resp = await client.post("/api/v1/questions/answer", json={
        "channel": "web",
        "question": "Очень специфичный вопрос ни о чём конкретном что не найдётся в фрагментах",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "refused"
    assert data["reason_code"] is not None


@pytest.mark.asyncio
async def test_get_session(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/questions/nonexistent")
    assert resp.status_code == 404
