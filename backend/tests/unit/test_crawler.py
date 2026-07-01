__anchor__ = "tests"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.crawler.app.main import app


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_start_crawl(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/crawl", json={
        "source_domain": "fedsfm.ru",
        "url": "https://www.fedsfm.ru/news/7338",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] in ("running", "completed")
    assert data["anchor"] == "crawler"


@pytest.mark.asyncio
async def test_get_crawl_status(client: AsyncClient) -> None:
    create = await client.post("/api/v1/crawl", json={
        "source_domain": "test.ru",
        "url": "https://test.ru/doc",
    })
    job_id = create.json()["job_id"]
    resp = await client.get(f"/api/v1/crawl/{job_id}")
    assert resp.status_code == 200
    assert resp.json()["source_domain"] == "test.ru"


@pytest.mark.asyncio
async def test_get_crawl_results(client: AsyncClient) -> None:
    create = await client.post("/api/v1/crawl", json={
        "source_domain": "test.ru",
        "url": "https://test.ru/doc",
    })
    job_id = create.json()["job_id"]
    resp = await client.get(f"/api/v1/crawl/{job_id}/results")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_crawl_not_found(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/crawl/nonexistent")
    assert resp.status_code == 404
