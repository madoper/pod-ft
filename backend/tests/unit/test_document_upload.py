__anchor__ = "doc-check"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.document_upload.app.main import app


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_upload_document(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/v1/documents/upload",
        files={"file": ("test.txt", b"hello world", "text/plain")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["anchor"] == "document-upload"
    assert data["status"] == "uploaded"
    assert data["filename"] == "test.txt"
    assert data["content_type"] == "text/plain"
    assert data["size_bytes"] == 11


@pytest.mark.asyncio
async def test_list_documents(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/documents")
    assert resp.status_code == 200
    data = resp.json()
    assert data["anchor"] == "document-upload"
    assert "documents" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_list_after_upload(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/documents/upload",
        files={"file": ("a.txt", b"aaa", "text/plain")},
    )
    resp = await client.get("/api/v1/documents")
    data = resp.json()
    assert data["total"] >= 1
    assert any(d["filename"] == "a.txt" for d in data["documents"])
