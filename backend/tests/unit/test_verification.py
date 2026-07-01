__anchor__ = "tests"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.verification.app.main import app


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_precheck_sufficient(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/precheck", json={
        "question": "Какие требования к ПВК?",
        "candidate_fragments": [
            {
                "fragment_id": "f1",
                "fragment_text": "Требования к правилам внутреннего контроля...",
                "citation_label": "ст. 7",
                "tier": 1,
                "confidence": 0.95,
            },
            {
                "fragment_id": "f2",
                "fragment_text": "Субъект обязан разработать ПВК...",
                "citation_label": "п. 3",
                "tier": 1,
                "confidence": 0.88,
            },
        ],
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["allowed"] is True
    assert data["anchor"] == "verification"


@pytest.mark.asyncio
async def test_precheck_insufficient_fragments(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/precheck", json={
        "question": "Test",
        "candidate_fragments": [
            {
                "fragment_id": "f1",
                "fragment_text": "Single fragment...",
                "citation_label": "п. 1",
                "tier": 1,
                "confidence": 0.95,
            },
        ],
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["allowed"] is False
    assert data["reason_code"] == "INSUFFICIENT_TIER1_EVIDENCE"


@pytest.mark.asyncio
async def test_precheck_non_tier1(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/precheck", json={
        "question": "Test",
        "candidate_fragments": [
            {
                "fragment_id": "f1", "fragment_text": "T1",
                "citation_label": "п. 1", "tier": 1, "confidence": 0.9,
            },
            {
                "fragment_id": "f2", "fragment_text": "T2",
                "citation_label": None, "tier": 2, "confidence": 0.6,
            },
        ],
    })
    assert resp.status_code == 200
    assert resp.json()["allowed"] is False
    assert resp.json()["reason_code"] == "NON_TIER1_FRAGMENT_PRESENT"

    resp2 = await client.post("/api/v1/precheck", json={
        "question": "Test",
        "candidate_fragments": [
            {
                "fragment_id": "f1", "fragment_text": "T1",
                "citation_label": "п. 1", "tier": 2, "confidence": 0.9,
            },
            {
                "fragment_id": "f2", "fragment_text": "T2",
                "citation_label": "п. 2", "tier": 2, "confidence": 0.6,
            },
        ],
    })
    assert resp2.json()["reason_code"] == "NON_TIER1_FRAGMENT_PRESENT"


@pytest.mark.asyncio
async def test_finalize_approved(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/finalize", json={
        "question": "Test",
        "candidate_fragments": [
            {
                "fragment_id": "f1", "fragment_text": "F1",
                "citation_label": "п. 1", "tier": 1, "confidence": 0.9,
            },
            {
                "fragment_id": "f2", "fragment_text": "F2",
                "citation_label": "п. 2", "tier": 1, "confidence": 0.8,
            },
        ],
        "draft_summary": "This is a sufficiently long draft summary for testing purposes.",
        "citations": ["п. 1", "п. 2"],
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["allowed"] is True
    assert data["verifier_status"] == "approved"
    assert data["llm_verdict"] == {
        "passed": True, "confidence": 1.0, "reason": "llm_not_configured",
    }


@pytest.mark.asyncio
async def test_finalize_no_citations(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/finalize", json={
        "question": "Test",
        "candidate_fragments": [
            {
                "fragment_id": "f1", "fragment_text": "F1",
                "citation_label": "п. 1", "tier": 1, "confidence": 0.9,
            },
            {
                "fragment_id": "f2", "fragment_text": "F2",
                "citation_label": "п. 2", "tier": 1, "confidence": 0.8,
            },
        ],
        "draft_summary": "Long enough draft summary for testing verification purposes.",
        "citations": [],
    })
    assert resp.json()["allowed"] is False
    assert resp.json()["reason_code"] == "ANSWER_MISSING_CITATIONS"
