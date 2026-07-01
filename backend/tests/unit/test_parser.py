__anchor__ = "tests"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.parser.app.main import app


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


SAMPLE_HTML = """
<html>
<body>
    <h1>Test Document</h1>
    <p>This is a sample paragraph with enough text to be captured as a fragment.</p>
    <p>This is another paragraph with enough text for a second fragment.</p>
    <ul>
        <li>List item with enough content to be extracted as a fragment.</li>
        <li>Another list item with enough text content for extraction.</li>
    </ul>
</body>
</html>
"""


@pytest.mark.asyncio
async def test_parse_html(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/parse/html", json={
        "url": "https://test.ru/doc",
        "html_content": SAMPLE_HTML,
        "document_title": "Test Document",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["document_title"] == "Test Document"
    assert data["fragment_count"] >= 2
    assert data["anchor"] == "parser"


@pytest.mark.asyncio
async def test_parse_fragments_have_citation_labels(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/parse/html", json={
        "url": "https://test.ru/doc",
        "html_content": SAMPLE_HTML,
    })
    data = resp.json()
    for f in data["fragments"]:
        assert "fragment_id" in f
        assert "citation_label" in f
        assert f["anchor"] == "parser"
