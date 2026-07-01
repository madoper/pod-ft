__anchor__ = "tests"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.workers.app.main import app


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_submit_job(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/workers/jobs", json={
        "task_type": "crawl",
        "params": {"url": "https://example.com"},
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["task_type"] == "crawl"
    assert data["status"] == "running"
    assert data["job_id"]


@pytest.mark.asyncio
async def test_get_job(client: AsyncClient) -> None:
    create = await client.post("/api/v1/workers/jobs", json={"task_type": "test"})
    job_id = create.json()["job_id"]
    resp = await client.get(f"/api/v1/workers/jobs/{job_id}")
    assert resp.status_code == 200
    assert resp.json()["job_id"] == job_id


@pytest.mark.asyncio
async def test_get_job_not_found(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/workers/jobs/nonexistent")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_list_jobs(client: AsyncClient) -> None:
    for _ in range(3):
        await client.post("/api/v1/workers/jobs", json={"task_type": "crawl"})
    resp = await client.get("/api/v1/workers/jobs")
    assert resp.status_code == 200
    assert len(resp.json()) >= 3


@pytest.mark.asyncio
async def test_worker_status(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/workers/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["worker_id"] == "default"
    assert "uptime_seconds" in data


@pytest.mark.asyncio
async def test_job_respects_priority(client: AsyncClient) -> None:
    low = await client.post("/api/v1/workers/jobs", json={
        "task_type": "low", "priority": 0,
    })
    high = await client.post("/api/v1/workers/jobs", json={
        "task_type": "high", "priority": 10,
    })
    resp = await client.get("/api/v1/workers/jobs?limit=10")
    jobs = resp.json()
    low_idx = next(i for i, j in enumerate(jobs) if j["job_id"] == low.json()["job_id"])
    high_idx = next(i for i, j in enumerate(jobs) if j["job_id"] == high.json()["job_id"])
    assert high_idx < low_idx  # higher priority first
