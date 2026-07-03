__anchor__ = "tests"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.changes.app.main import app


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_list_changes_empty(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/changes")
    assert resp.status_code == 200
    data = resp.json()
    assert data["anchor"] == "changes"
    assert data["total"] == 0
    assert data["changes"] == []


@pytest.mark.asyncio
async def test_list_changes_with_limit(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/changes?limit=10")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 0


@pytest.mark.asyncio
async def test_diff_versions_not_found(client: AsyncClient) -> None:
    resp = await client.get(
        "/api/v1/changes/nonexistent/diff",
        params={"from_version_id": "v1", "to_version_id": "v2"},
    )
    assert resp.status_code == 404
