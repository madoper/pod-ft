__anchor__ = "tests"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.graph_service.app.main import app


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_sync_document(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/sync", json={
        "document_id": "doc-1",
        "document_version_id": "v1",
        "regulator_code": "rosfinmonitoring",
        "fragments": [
            {"fragment_id": "f1", "fragment_text": "Text one"},
            {"fragment_id": "f2", "fragment_text": "Text two"},
        ],
        "norms": [{"norm_id": "n1", "title": "Norm 1"}],
        "obligations": [
            {
                "obligation_id": "o1", "norm_id": "n1",
                "risk_level": "high", "source_fragment_ids": ["f1"],
            },
        ],
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["nodes_created"] >= 4
    assert data["edges_created"] >= 3
    assert data["anchor"] == "graph-service"


@pytest.mark.asyncio
async def test_query_graph(client: AsyncClient) -> None:
    await client.post("/api/v1/sync", json={
        "document_id": "doc-2",
        "document_version_id": "v1",
        "regulator_code": "cbr",
        "fragments": [{"fragment_id": "f3", "fragment_text": "Some text"}],
        "norms": [],
        "obligations": [],
    })
    resp = await client.post("/api/v1/query", json={
        "query": "MATCH (n:Document) RETURN n",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["node_count"] >= 1


@pytest.mark.asyncio
async def test_list_regulators(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/nodes/regulator")
    assert resp.status_code == 200
    assert len(resp.json()) > 0


@pytest.mark.asyncio
async def test_obligation_sources(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/obligations/nonexistent/sources")
    assert resp.status_code == 200
