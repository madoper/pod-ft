__anchor__ = "tests"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.doc_check.app.main import app


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_check_document_submit(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/check", json={
        "tenant_id": "tenant-1",
        "document_text": "Тестовый внутренний документ",
        "document_title": "Test Internal Policy",
        "document_type": "internal_policy",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["anchor"] == "doc-check"
    assert data["status"] == "pending"
    assert data["job_id"]


@pytest.mark.asyncio
async def test_check_document_then_poll(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/check", json={
        "tenant_id": "tenant-1",
        "document_text": "правила внутреннего контроля",
        "document_title": "ПВК",
    })
    assert resp.status_code == 200
    job_id = resp.json()["job_id"]

    import asyncio
    for _ in range(20):
        poll = await client.get(f"/api/v1/check/{job_id}")
        assert poll.status_code == 200
        data = poll.json()
        if data["status"] == "completed":
            assert data["result"]["coverage_summary"]
            assert "export_links" in data["result"]
            assert len(data["result"]["export_links"]) == 4
            formats = {el["format"] for el in data["result"]["export_links"]}
            assert formats == {"json", "docx", "pdf", "xlsx"}
            return
        await asyncio.sleep(0.05)

    raise AssertionError("Job did not complete in time")


@pytest.mark.asyncio
async def test_get_job_not_found(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/check/nonexistent")
    assert resp.status_code == 404
