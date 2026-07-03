import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.shared.db.redis import redis_client
from backend.shared.rate_limiter import RateLimitMiddleware


@pytest.fixture
def app() -> FastAPI:
    app = FastAPI()

    @app.get("/test")
    async def test_endpoint():
        return {"status": "ok"}

    app.add_middleware(RateLimitMiddleware, max_requests=5, window_sec=60)  # type: ignore[arg-type]
    return app


@pytest.mark.asyncio
async def test_rate_limiter_passes_when_under_limit(app: FastAPI) -> None:
    with TestClient(app) as client:
        for _ in range(5):
            resp = client.get("/test")
            assert resp.status_code == 200


@pytest.mark.asyncio
async def test_rate_limiter_blocks_when_over_limit(app: FastAPI) -> None:
    with TestClient(app) as client:
        for _ in range(5):
            client.get("/test")
        resp = client.get("/test")
        if await redis_client.is_available():
            assert resp.status_code == 429
            data = resp.json()
            assert "too many requests" in data["detail"].lower()
        else:
            assert resp.status_code == 200


@pytest.mark.asyncio
async def test_rate_limiter_rate_limit_headers(app: FastAPI) -> None:
    with TestClient(app) as client:
        resp = client.get("/test")
        if await redis_client.is_available():
            assert "x-ratelimit-limit" in resp.headers
            assert "x-ratelimit-remaining" in resp.headers
