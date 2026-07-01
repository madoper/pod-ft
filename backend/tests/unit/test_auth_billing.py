__anchor__ = "tests"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.auth_billing.app.main import app


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_register(client: AsyncClient) -> None:
    body = {"email": "test@podft.ru", "password": "secret123"}
    resp = await client.post("/api/v1/auth/register", json=body)
    assert resp.status_code == 201
    data = resp.json()
    assert "user_id" in data
    assert data["anchor"] == "auth-billing"


@pytest.mark.asyncio
async def test_register_duplicate(client: AsyncClient) -> None:
    body = {"email": "dup@podft.ru", "password": "secret"}
    await client.post("/api/v1/auth/register", json=body)
    resp = await client.post("/api/v1/auth/register", json=body)
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_login(client: AsyncClient) -> None:
    body = {"email": "login_test@podft.ru", "password": "pass123"}
    await client.post("/api/v1/auth/register", json=body)
    resp = await client.post("/api/v1/auth/login", json=body)
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient) -> None:
    body = {"email": "nonexist@podft.ru", "password": "wrong"}
    resp = await client.post("/api/v1/auth/login", json=body)
    assert resp.status_code == 401
