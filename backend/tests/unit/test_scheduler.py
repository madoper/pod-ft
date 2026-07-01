__anchor__ = "tests"

from httpx import ASGITransport, AsyncClient

from backend.apps.scheduler.app.main import app


async def _client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


async def test_create_schedule() -> None:
    async with await _client() as client:
        resp = await client.post("/api/v1/schedules", json={
            "task_type": "crawl",
            "cron_expr": "0 6 * * *",
            "params": {"url": "https://example.com"},
            "label": "daily crawl",
        })
    assert resp.status_code == 201
    data = resp.json()
    assert data["task_type"] == "crawl"
    assert data["cron_expr"] == "0 6 * * *"
    assert data["label"] == "daily crawl"
    assert data["enabled"] is True
    assert data["schedule_id"]


async def test_list_schedules() -> None:
    async with await _client() as client:
        await client.post("/api/v1/schedules", json={"task_type": "reindex"})
        resp = await client.get("/api/v1/schedules")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


async def test_get_schedule_not_found() -> None:
    async with await _client() as client:
        resp = await client.get("/api/v1/schedules/nonexistent")
    assert resp.status_code == 404


async def test_delete_schedule() -> None:
    async with await _client() as client:
        create = await client.post("/api/v1/schedules", json={"task_type": "cleanup"})
        sid = create.json()["schedule_id"]
        resp = await client.delete(f"/api/v1/schedules/{sid}")
    assert resp.status_code == 204


async def test_delete_schedule_not_found() -> None:
    async with await _client() as client:
        resp = await client.delete("/api/v1/schedules/nonexistent")
    assert resp.status_code == 404


async def test_get_schedule_history() -> None:
    async with await _client() as client:
        create = await client.post("/api/v1/schedules", json={"task_type": "crawl"})
        sid = create.json()["schedule_id"]
        resp = await client.get(f"/api/v1/schedules/{sid}/history")
    assert resp.status_code == 200
    assert resp.json() == []


async def test_tick_schedules() -> None:
    async with await _client() as client:
        create = await client.post("/api/v1/schedules", json={
            "task_type": "crawl", "cron_expr": "30 10 * * *",
        })
        sid = create.json()["schedule_id"]
        tick = await client.post("/api/v1/schedules/tick")
    assert tick.status_code == 200
    executed = tick.json()
    # Schedule with future next_run should NOT be executed
    # (30 10 at current 10:25 means candidate=10:30 which is in the future)
    assert len(executed) == 0
    # Verify schedule still exists
    async with await _client() as get_client:
        get = await get_client.get(f"/api/v1/schedules/{sid}")
    assert get.status_code == 200


async def test_tick_executes_due_schedule() -> None:
    from backend.apps.scheduler.app.services.scheduler_service import SchedulerService
    svc = SchedulerService()
    sched = await svc.create_schedule(
        task_type="test", cron_expr="0 6 * * *", params={}, label="",
    )
    # Force next_run into the past
    from datetime import UTC, datetime, timedelta
    past = (datetime.now(UTC) - timedelta(hours=1)).isoformat()
    svc._schedules[sched.schedule_id]["next_run"] = past
    executed = await svc.execute_due()
    assert len(executed) == 1
    assert executed[0].schedule_id == sched.schedule_id
    assert executed[0].status == "completed"


async def test_schedule_defaults() -> None:
    async with await _client() as client:
        resp = await client.post("/api/v1/schedules", json={})
    assert resp.status_code == 201
    data = resp.json()
    assert data["task_type"] == "crawl"
    assert data["cron_expr"] == "0 6 * * *"
