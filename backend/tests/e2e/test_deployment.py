__anchor__ = "tests"
# E2E smoke tests for pod-ft deployment on VPS Beget
# Usage: pytest backend/tests/e2e/ -v --base-url=https://vectornode.ru

import os

import httpx
import pytest

BASE_URL = os.getenv("E2E_BASE_URL", "http://localhost:8000")


@pytest.fixture
def client() -> httpx.Client:
    return httpx.Client(base_url=BASE_URL, timeout=10)


def test_gateway_health(client: httpx.Client) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["service"] == "gateway"


def test_api_health(client: httpx.Client) -> None:
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json()["version"] == "0.1.0"


def test_auth_register(client: httpx.Client) -> None:
    body = {"email": "e2e@podft.ru", "password": "e2etest123"}
    resp = client.post("/api/v1/auth/register", json=body)
    assert resp.status_code == 201
    assert resp.json()["anchor"] == "auth-billing"


def test_auth_login(client: httpx.Client) -> None:
    body = {"email": "e2e_login@podft.ru", "password": "e2etest123"}
    client.post("/api/v1/auth/register", json=body)
    resp = client.post("/api/v1/auth/login", json=body)
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_sources_active(client: httpx.Client) -> None:
    resp = client.get("/api/v1/sources/active")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 3
    for src in data:
        assert src["tier"] == 1
        assert src["anchor"] == "source-registry"


def test_root_redirect(client: httpx.Client) -> None:
    resp = client.get("/api/v1/docs")
    assert resp.status_code == 200
