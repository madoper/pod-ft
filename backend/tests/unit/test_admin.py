__anchor__ = "tests"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.admin.app.main import app


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_block_document(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/v1/admin/documents/doc-123/block",
        json={"target_id": "doc-123", "reason": "Test moderation"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["anchor"] == "admin"
    assert data["override_type"] == "block_document"
    assert data["target_id"] == "doc-123"


@pytest.mark.asyncio
async def test_block_norm(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/v1/admin/norms/norm-456/block",
        json={"target_id": "norm-456", "reason": "Outdated"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["override_type"] == "block_norm"
    assert data["target_id"] == "norm-456"


@pytest.mark.asyncio
async def test_unblock(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/admin/documents/doc-789/block",
        json={"target_id": "doc-789", "reason": "Spam"},
    )
    resp = await client.post("/api/v1/admin/unblock/doc-789", json={})
    assert resp.status_code == 200
    data = resp.json()
    assert "unblocked" in data["message"]


@pytest.mark.asyncio
async def test_unblock_not_found(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/admin/unblock/nonexistent", json={})
    assert resp.status_code == 200
    data = resp.json()
    assert "was not blocked" in data["message"]


@pytest.mark.asyncio
async def test_list_blocks(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/admin/blocks")
    assert resp.status_code == 200
    data = resp.json()
    assert data["anchor"] == "admin"
    assert "entries" in data
