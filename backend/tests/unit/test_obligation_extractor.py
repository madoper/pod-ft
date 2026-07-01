__anchor__ = "tests"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.obligation_extractor.app.main import app


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


SAMPLE_FRAGMENTS = [
    {
        "fragment_id": "f1",
        "fragment_no": 1,
        "fragment_text": (
            "Субъект обязан разработать правила внутреннего контроля"
            " в соответствии с требованиями статьи 7.1."
        ),
        "citation_label": "п. 1",
    },
    {
        "fragment_id": "f2",
        "fragment_no": 2,
        "fragment_text": "Запрещается предоставлять услуги без идентификации клиента.",
        "citation_label": "п. 2",
    },
    {
        "fragment_id": "f3",
        "fragment_no": 3,
        "fragment_text": "Данный раздел описывает общие положения.",
        "citation_label": "п. 3",
    },
]


@pytest.mark.asyncio
async def test_extract_obligations(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/extract", json={
        "document_id": "doc-1",
        "document_version_id": "v1",
        "fragments": SAMPLE_FRAGMENTS,
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["norm_count"] >= 1
    assert data["obligation_count"] >= 1
    assert data["anchor"] == "obligation-extractor"


@pytest.mark.asyncio
async def test_list_norms(client: AsyncClient) -> None:
    await client.post("/api/v1/extract", json={
        "document_id": "doc-2",
        "document_version_id": "v1",
        "fragments": SAMPLE_FRAGMENTS,
    })
    resp = await client.get("/api/v1/norms")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


@pytest.mark.asyncio
async def test_list_obligations(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/obligations")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_norm_obligations_not_found(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/norms/nonexistent/obligations")
    assert resp.status_code == 404
