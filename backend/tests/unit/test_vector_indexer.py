__anchor__ = "tests"

import pytest
from httpx import ASGITransport, AsyncClient

from backend.apps.vector_indexer.app.main import app
from backend.apps.vector_indexer.app.services.embedding_service import (
    EmbeddingService,
)


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


class TestEmbeddingService:
    @pytest.mark.asyncio
    async def test_embed_returns_fixed_size_vector(self) -> None:
        svc = EmbeddingService()
        vec = await svc.embed("test text")
        assert len(vec) == 384
        assert all(isinstance(v, float) for v in vec)

    @pytest.mark.asyncio
    async def test_embed_deterministic(self) -> None:
        svc = EmbeddingService()
        v1 = await svc.embed("одинаковый текст")
        v2 = await svc.embed("одинаковый текст")
        assert v1 == v2

    @pytest.mark.asyncio
    async def test_embed_different_texts_different_vectors(self) -> None:
        svc = EmbeddingService()
        v1 = await svc.embed("правила внутреннего контроля")
        v2 = await svc.embed("идентификация клиента")
        assert v1 != v2

    @pytest.mark.asyncio
    async def test_embed_normalized(self) -> None:
        svc = EmbeddingService()
        vec = await svc.embed("test")
        norm = sum(v * v for v in vec) ** 0.5
        assert abs(norm - 1.0) < 1e-4

    @pytest.mark.asyncio
    async def test_embed_batch(self) -> None:
        svc = EmbeddingService()
        texts = ["text one", "text two", "text three"]
        vectors = await svc.embed_batch(texts)
        assert len(vectors) == 3
        assert all(len(v) == 384 for v in vectors)
        assert vectors[0] != vectors[1]


@pytest.mark.asyncio
async def test_vector_indexer_search_no_qdrant(client: AsyncClient) -> None:
    """Without Qdrant, the search should return empty results gracefully."""
    resp = await client.post("/api/v1/search", json={
        "query": "тестовый запрос",
        "top_k": 5,
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["query"] == "тестовый запрос"
    assert data["total_count"] == 0
    assert data["anchor"] == "vector-indexer"


@pytest.mark.asyncio
async def test_vector_indexer_delete_no_qdrant(client: AsyncClient) -> None:
    """Without Qdrant, delete should return zero gracefully."""
    resp = await client.post("/api/v1/delete", json={
        "fragment_ids": ["nonexistent"],
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["deleted_count"] == 0
    assert data["anchor"] == "vector-indexer"


@pytest.mark.asyncio
async def test_vector_indexer_health(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/docs")
    assert resp.status_code == 200
