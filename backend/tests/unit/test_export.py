__anchor__ = "tests"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.export.app.main import app
from backend.apps.export.app.schemas.export import ExportRequest, ExportSection
from backend.apps.export.app.services.export_service import ExportService


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


class TestExportService:
    @pytest.mark.asyncio
    async def test_export_json(self) -> None:
        svc = ExportService()
        result = await svc.export(ExportRequest(
            format="json",
            title="Test Report",
            sections=[
                ExportSection(title="Section 1", content="Content 1"),
            ],
        ))
        assert result.format == "json"
        assert result.filename.endswith(".json")
        assert "Test Report" in result.data
        assert result.anchor == "export"

    @pytest.mark.asyncio
    async def test_export_docx(self) -> None:
        import base64
        svc = ExportService()
        result = await svc.export(ExportRequest(
            format="docx",
            title="Doc",
            sections=[],
        ))
        assert result.format == "docx"
        assert result.filename.endswith(".docx")
        decoded = base64.b64decode(result.data)
        assert decoded[:2] == b"PK"

    @pytest.mark.asyncio
    async def test_export_pdf(self) -> None:
        import base64
        svc = ExportService()
        result = await svc.export(ExportRequest(
            format="pdf",
            title="PDF Doc",
            sections=[],
        ))
        assert result.format == "pdf"
        decoded = base64.b64decode(result.data)
        assert decoded[:4] == b"%PDF"

    @pytest.mark.asyncio
    async def test_export_xlsx(self) -> None:
        import base64
        svc = ExportService()
        result = await svc.export(ExportRequest(
            format="xlsx",
            title="XLSX Doc",
            sections=[],
        ))
        assert result.format == "xlsx"
        decoded = base64.b64decode(result.data)
        assert decoded[:2] == b"PK"

    @pytest.mark.asyncio
    async def test_export_defaults_to_json(self) -> None:
        svc = ExportService()
        result = await svc.export(ExportRequest(
            format="unknown",
            title="Fallback",
            sections=[],
        ))
        assert result.format == "unknown"
        assert result.filename.endswith(".json")


@pytest.mark.asyncio
async def test_export_endpoint(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/export", json={
        "format": "json",
        "title": "Integration Test",
        "sections": [
            {"title": "Sec 1", "content": "Some content", "citations": ["ст. 7"]},
        ],
        "summary": "Done",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["anchor"] == "export"
    assert data["format"] == "json"
    assert "Integration Test" in data["data"]
