__anchor__ = "tests"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.retrieval.app.main import app


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_index_and_search(client: AsyncClient) -> None:
    # Index fragments
    idx_resp = await client.post("/api/v1/index", json={
        "fragments": [
            {
                "fragment_id": "r1",
                "document_title": "Law on AML",
                "fragment_text": "Субъект обязан разработать правила внутреннего контроля",
                "citation_label": "ст. 7",
                "tier": 1,
                "source_domain": "fedsfm.ru",
            },
            {
                "fragment_id": "r2",
                "document_title": "CBR Guidelines",
                "fragment_text": "Банк России устанавливает требования к идентификации",
                "citation_label": "п. 3",
                "tier": 1,
                "source_domain": "cbr.ru",
            },
            {
                "fragment_id": "r3",
                "document_title": "General Info",
                "fragment_text": "Общие положения о противодействии легализации доходов",
                "citation_label": "п. 1",
                "tier": 2,
                "source_domain": "consultant.ru",
            },
        ],
    })
    assert idx_resp.status_code == 200
    assert idx_resp.json()["indexed_count"] == 3

    # Search
    search_resp = await client.post("/api/v1/search", json={
        "query": "правила внутреннего контроля",
        "top_k": 5,
        "min_confidence": 0.0,
    })
    assert search_resp.status_code == 200
    data = search_resp.json()
    assert data["total_count"] >= 1
    assert data["anchor"] == "retrieval"
    # Best match should be first
    assert data["results"][0]["fragment_id"] == "r1"


@pytest.mark.asyncio
async def test_list_fragments(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/fragments")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_delete_fragment(client: AsyncClient) -> None:
    resp = await client.delete("/api/v1/fragments/nonexistent")
    assert resp.status_code == 204
