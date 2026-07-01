__anchor__ = "tests"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.source_registry.app.main import app


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_list_active_sources(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/sources/active")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 3
    for src in data:
        assert src["tier"] == 1
        assert src["is_active"] is True
        assert src["anchor"] == "source-registry"


@pytest.mark.asyncio
async def test_list_all_sources(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/admin/sources")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 4


@pytest.mark.asyncio
async def test_create_source(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/admin/sources", json={
        "domain": "test.ru", "source_type": "test", "regulator_name": "Test", "tier": 2,
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["domain"] == "test.ru"


@pytest.mark.asyncio
async def test_update_source(client: AsyncClient) -> None:
    resp = await client.patch("/api/v1/admin/sources/1", json={"is_active": False})
    assert resp.status_code == 200
    assert resp.json()["is_active"] is False


@pytest.mark.asyncio
async def test_update_not_found(client: AsyncClient) -> None:
    resp = await client.patch("/api/v1/admin/sources/999", json={"is_active": False})
    assert resp.status_code == 404
