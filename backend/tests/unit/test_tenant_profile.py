__anchor__ = "tests"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.tenant_profile.app.main import app


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_create_profile(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/v1/tenant-profile",
        json={"tenant_id": "tenant-1", "subject_type": "credit_organization", "regulator": "cbr"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["anchor"] == "tenant-profile"
    assert data["subject_type"] == "credit_organization"
    assert data["regulator"] == "cbr"
    assert data["tenant_id"] == "tenant-1"


@pytest.mark.asyncio
async def test_get_profile(client: AsyncClient) -> None:
    create = await client.post(
        "/api/v1/tenant-profile",
        json={"tenant_id": "tenant-2", "subject_type": "article_7_1"},
    )
    profile_id = create.json()["id"]

    resp = await client.get(f"/api/v1/tenant-profile/{profile_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["subject_type"] == "article_7_1"


@pytest.mark.asyncio
async def test_get_profile_not_found(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/tenant-profile/nonexistent")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_profiles_by_tenant(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/tenant-profile",
        json={"tenant_id": "tenant-3", "subject_type": "nfo"},
    )

    resp = await client.get("/api/v1/tenant-profile/by-tenant/tenant-3")
    assert resp.status_code == 200
    data = resp.json()
    assert data["anchor"] == "tenant-profile"
    assert len(data["profiles"]) >= 1


@pytest.mark.asyncio
async def test_update_profile(client: AsyncClient) -> None:
    create = await client.post(
        "/api/v1/tenant-profile",
        json={"tenant_id": "tenant-4", "subject_type": "credit_organization"},
    )
    profile_id = create.json()["id"]

    resp = await client.put(
        f"/api/v1/tenant-profile/{profile_id}",
        json={"subject_type": "professional"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["subject_type"] == "professional"


@pytest.mark.asyncio
async def test_delete_profile(client: AsyncClient) -> None:
    create = await client.post(
        "/api/v1/tenant-profile",
        json={"tenant_id": "tenant-5", "subject_type": "credit_organization"},
    )
    profile_id = create.json()["id"]

    resp = await client.delete(f"/api/v1/tenant-profile/{profile_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert "deleted" in data["message"].lower()

    resp = await client.get(f"/api/v1/tenant-profile/{profile_id}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_evaluate_applicability(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/v1/tenant-profile/tenant-6/applicability",
        json={"subject_type": "article_7_1", "regulator": "rosfinmonitoring"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["anchor"] == "tenant-profile"
    assert len(data["rules"]) > 0
    assert data["profile"]["subject_type"] == "article_7_1"
