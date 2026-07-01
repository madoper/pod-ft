__anchor__ = "tests"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.doc_check.app.main import app


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_check_document_no_fragments(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/check", json={
        "tenant_id": "tenant-1",
        "document_text": "Тестовый внутренний документ",
        "document_title": "Test Internal Policy",
        "document_type": "internal_policy",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["anchor"] == "doc-check"
    assert data["status"] == "completed"
    assert "coverage_summary" in data


@pytest.mark.asyncio
async def test_check_document_with_fragments(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/check", json={
        "tenant_id": "tenant-1",
        "document_text": "правила внутреннего контроля",
        "document_title": "ПВК",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["anchor"] == "doc-check"
    assert data["status"] == "completed"


@pytest.mark.asyncio
async def test_get_job_not_found(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/check/nonexistent")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_job_found(client: AsyncClient) -> None:
    check_resp = await client.post("/api/v1/check", json={
        "tenant_id": "tenant-1",
        "document_text": "test",
        "document_title": "Test",
    })
    job_id = check_resp.json()["job_id"]
    resp = await client.get(f"/api/v1/check/{job_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "completed"
