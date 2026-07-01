__anchor__ = "tests"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.versioning.app.main import app


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_register_new_document(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/documents/register", json={
        "canonical_url": "https://test.ru/doc1",
        "document_title": "First Document",
        "document_kind": "guideline",
        "content_hash": "abc123",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["is_new_version"] is True
    assert data["version_label"] == "v1"
    assert data["is_current"] is True
    assert data["anchor"] == "versioning"


@pytest.mark.asyncio
async def test_register_same_content_no_new_version(client: AsyncClient) -> None:
    await client.post("/api/v1/documents/register", json={
        "canonical_url": "https://test.ru/dup",
        "document_title": "Duplicate",
        "document_kind": "memo",
        "content_hash": "samehash",
    })
    resp = await client.post("/api/v1/documents/register", json={
        "canonical_url": "https://test.ru/dup",
        "document_title": "Duplicate",
        "document_kind": "memo",
        "content_hash": "samehash",
    })
    assert resp.status_code == 201
    assert resp.json()["is_new_version"] is False


@pytest.mark.asyncio
async def test_register_new_version(client: AsyncClient) -> None:
    await client.post("/api/v1/documents/register", json={
        "canonical_url": "https://test.ru/doc3",
        "document_title": "Doc 3",
        "document_kind": "law",
        "content_hash": "hash_v1",
    })
    resp = await client.post("/api/v1/documents/register", json={
        "canonical_url": "https://test.ru/doc3",
        "document_title": "Doc 3 Updated",
        "document_kind": "law",
        "content_hash": "hash_v2",
    })
    assert resp.status_code == 201
    assert resp.json()["is_new_version"] is True
    assert resp.json()["version_label"] == "v2"


@pytest.mark.asyncio
async def test_list_versions(client: AsyncClient) -> None:
    await client.post("/api/v1/documents/register", json={
        "canonical_url": "https://test.ru/doc4",
        "document_title": "Doc 4",
        "document_kind": "order",
        "content_hash": "h1",
    })
    await client.post("/api/v1/documents/register", json={
        "canonical_url": "https://test.ru/doc4",
        "document_title": "Doc 4",
        "document_kind": "order",
        "content_hash": "h2",
    })
    # Get doc_id by re-registering and reading response
    resp = await client.post("/api/v1/documents/register", json={
        "canonical_url": "https://test.ru/doc4",
        "document_title": "Doc 4",
        "document_kind": "order",
        "content_hash": "h2",
    })
    doc_id = resp.json()["document_id"]
    list_resp = await client.get(f"/api/v1/documents/{doc_id}/versions")
    assert list_resp.status_code == 200
    versions = list_resp.json()
    assert len(versions) >= 2
    # v2 should be current, v1 should not
    v1 = next(v for v in versions if v["version_label"] == "v1")
    v2 = next(v for v in versions if v["version_label"] == "v2")
    assert v1["is_current"] is False
    assert v2["is_current"] is True


@pytest.mark.asyncio
async def test_timeline(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/documents/nonexistent/timeline")
    assert resp.status_code == 404
