__anchor__ = "tests"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.drafting.app.main import app
from backend.apps.drafting.app.services.drafting_service import DraftingService


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


class TestDraftingService:
    @pytest.mark.asyncio
    async def test_generate_pvk(self) -> None:
        svc = DraftingService()
        result = await svc.generate_draft(
            document_type="pvk",
            subject_type="article_7_1",
        )
        assert result.document_type == "pvk"
        assert "Правила внутреннего контроля" in result.title
        assert len(result.sections) > 0
        assert result.anchor == "drafting"

    @pytest.mark.asyncio
    async def test_generate_unknown_type(self) -> None:
        svc = DraftingService()
        result = await svc.generate_draft(
            document_type="unknown_type",
        )
        assert result.document_type == "unknown_type"

    @pytest.mark.asyncio
    async def test_generate_order(self) -> None:
        svc = DraftingService()
        result = await svc.generate_draft(
            document_type="order",
        )
        assert len(result.sections) > 0

    @pytest.mark.asyncio
    async def test_generate_checklist(self) -> None:
        svc = DraftingService()
        result = await svc.generate_draft(
            document_type="checklist",
        )
        assert len(result.sections) > 0


@pytest.mark.asyncio
async def test_draft_endpoint(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/draft", json={
        "document_type": "pvk",
        "subject_type": "article_7_1",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["anchor"] == "drafting"
    assert len(data["sections"]) > 0
