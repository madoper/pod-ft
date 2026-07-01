# pod-ft

LLM RAG platform for Russian AML/CFT (ПОД/ФТ/ФРОМУ) regulatory compliance.

## Architecture

18 microservices behind `gateway`, 6 infrastructure services (PostgreSQL 16, Neo4j 5, Qdrant, MinIO, Redis, Nginx). Full spec: `../production-tech-project-podft-rag-dev-spec.md`.

## Quick start

```bash
cp .env.example .env
docker compose up -d
uv sync --group dev
uv run alembic upgrade head
uv run --directory backend/apps/gateway uvicorn app.main:app --reload --port 8000
```

## Semantic anchors

Every module carries `__anchor__` referencing `project-schema.yaml`. See `project-schema.yaml` for the complete service map.

## Development

```bash
uv sync --group dev
ruff check .
mypy backend/
uv run pytest
```
