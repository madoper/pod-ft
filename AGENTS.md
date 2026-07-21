# pod-ft

LLM RAG platform for Russian AML/CFT (ПОД/ФТ/ФРОМУ) regulatory compliance.

## Status

**Sprint 8 in progress.** The single source of truth is `production-tech-project-podft-rag-dev-spec.md`. The `podft-rag-platform/` directory contains the implementation.

## Planned architecture

- **Monorepo** at `podft-rag-platform/` — backend (Python/FastAPI + SQLAlchemy), frontend (web + Telegram bot), data pipelines, infra
- **21 microservices** behind a `gateway`: ingestion pipeline (crawler → parser → versioning → obligation-extractor → graph → vector-indexer), retrieval → answer-service → verification, doc-check, drafting, export, auth-billing, scheduler, workers, admin, source-registry, changes, document-upload, tenant-profile
- **Infrastructure**: PostgreSQL, Neo4j, Qdrant (vector DB), MinIO (object storage), Redis
- **LLM abstraction**: all calls through `backend/shared/llm/provider_router.py` — no direct provider calls from feature code

## Key architectural rules

- Source of truth is the official document text, not the LLM
- Only Tier-1 (official regulatory) sources can be cited
- Extractive RAG — answers must cite specific paragraph-level fragments
- Rule engine (sufficiency policy) has priority over verifier LLM
- Heavy jobs are async with job_id polling
- Every answer has full evidence trail: source, version, fragment, prompt, verifier decision

## Developer commands

```bash
uv sync --group dev          # install all deps
ruff check .                 # lint
mypy backend/                # typecheck
uv run pytest                # run unit tests (111 pass)
uv run pytest backend/tests/e2e/ --base-url=<url>  # E2E against deployment
cd frontend/web && npm install && npm run build  # build web frontend
make infra                   # docker compose up for postgres/qdrant/minio/redis
make dev                     # infra + migrations + gateway dev server
make infra-vps               # docker compose up without neo4j (1 GB VPS)
```

## Sprint 10 — Superset BI

| Component | Location | Status |
|---|---|---|
| **Superset container** | `docker-compose.vps.yml` | Apache Superset BI on VPS, connects to PostgreSQL, accessible at `/superset/`; `apache/superset:latest` with `psycopg2-binary` + `gevent` installed via pip `--user` at startup |
| **Superset config** | `infra/superset-init/superset_config.py` | PostgreSQL backend, Redis caching, `/superset` base URL, pythonpath volume mount |
| **nginx proxy** | `infra/nginx/nginx-vps.conf` | `/superset/` → `localhost:8088` with `X-Script-Name` header |
| **Superset web** | `https://vectornode.ru/superset/` | HTTP 200, login page served via nginx SSL |

## Sprint 9 (implemented)

| Component | Location | Status |
|---|---|---|
| Rate limiting | `backend/shared/rate_limiter.py` | Redis-based sliding window, configurable limit + window, X-RateLimit headers, graceful degradation when Redis unavailable; 3 unit tests |
| Redis client | `backend/shared/db/redis.py` | async wrapper with connection pooling, ping healthcheck, graceful fallback |
| Gateway updated | `backend/apps/gateway/app/main.py` | CORS middleware, rate limiter, Redis lifespan, LLM provider support |
| Web admin | `frontend/web/src/components/AdminPanel.tsx` | blocked items view (documents/norms) |
| Web profile | `frontend/web/src/components/ProfilePanel.tsx` | subscription + quota display with progress bar |
| Web nav | `frontend/web/src/App.tsx` | 5 tabs (ask, check, sources, admin, profile) |
| VPS nginx | `infra/nginx/nginx-vps.conf` | production config for `/api/` → gateway, `/` → web-frontend |
| Tenant Profile Service | `backend/apps/tenant_profile/` | 6 endpoints (CRUD + evaluate) for subject profiles; in-memory store |
| LLM provider clients | `backend/shared/llm/clients/` | OpenAI-compatible + YandexGPT + OpenRouter + MockProvider |
| Prompt templates | `backend/shared/llm/prompts/` | verification, drafting, extraction Russian prompts |
| Scheduler tasks | `backend/apps/scheduler/` | ingestion, crawl, reindex, healthcheck with default schedules (6 AM daily + every 30 min) |
| Alembic migration | `backend/migrations/` | 5 ORM tables (auth_user, doc_check_job, internal_document, draft, subject_profile) |
| Frontend tabs | `frontend/web/src/App.tsx` | 11 tabs: about, dashboard, ask, check, sources, documents, changes, billing, profile, templates, admin |
| SSE streaming | `frontend/web/src/components/DocCheckPanel.tsx` | real-time doc-check progress via Server-Sent Events |
| Idempotency middleware | `backend/shared/idempotency.py` | Idempotency-Key header support for POST safety |
| Tests | `backend/tests/unit/` | 111 unit tests (15 new: rate_limiter, tenant_profile, scheduler, prompts, LLM provider) |
| **DocCheckResultPage** | `frontend/web/src/components/DocCheckResultPage.tsx` | coverage card, gaps section, findings table with type badges + confidence dots + citation labels, export download buttons |
| **VPS cron scheduling** | `backend/apps/scheduler/` | `_init_default_schedules()` auto-creates ingestion (0 6 * * *) + healthcheck (*/30 * * *); `_execute_task` dispatches real tasks |
| **E2E tests** | `backend/tests/e2e/test_deployment.py` | 9 tests all pass against `https://vectornode.ru` |
| **OpenRouter integration** | `backend/shared/llm/clients/openrouter.py` | OpenAI-compatible API, free model `poolside/laguna-xs-2.1:free`, Russian system prompt; LLM provider in `.env` |
| **Landing page** | VPS nginx | `/` routes to React app (port 8080), `/api/` routes to gateway (port 8000); SSL via Let's Encrypt |
| **About page + onboarding** | `frontend/web/src/components/AboutPanel.tsx` | pipeline schema, 9 feature cards with "Перейти", demo sandbox, welcome modal on first visit (localStorage) |
| **Rename** | `index.html`, `App.tsx` | Title changed to `ИИ помощник по ПОД/ФТ/ФРОМУ` |

## Sprint 7 (implemented)

| Component | Location | Status |
|---|---|---|
| Telegram bot | `frontend/telegram/` | python-telegram-bot, /start, /ask, /stats, /help handlers; question conversation flow; 4 unit tests |
| Web frontend | `frontend/web/` | React + Vite + TypeScript, two-panel layout (question + answer), citation drawer, doc-check tab, source list tab |
| nginx updated | `infra/nginx/nginx.conf` | `/api/` → gateway, `/` → web-frontend |
| Docker Compose | `docker-compose.yml` | `telegram-bot` + `web-frontend` services added |
| Eval harness | `data-pipelines/eval/` | golden question set, answer + doc-check regression eval with precision/recall/F1 |
| Prometheus | `infra/monitoring/prometheus/` | scrape config for gateway metrics endpoint |
| CI/CD updated | `.github/workflows/ci-cd.yml` | builds web-frontend + telegram-bot images, deploys frontend services to VPS |
| E2E tests | `backend/tests/e2e/` | 3 new frontend smoke tests (HTML, assets, CORS) |

## Sprint 6 (implemented)

| Component | Location | Status |
|---|---|---|
| Admin moderation | `backend/apps/admin/` | POST /admin/documents/{id}/block, /admin/norms/{id}/block, /admin/unblock/{id}, GET /admin/blocks; in-memory + PG-ready schema |
| Billing | `backend/apps/auth_billing/` | GET /billing/subscription/{id}, POST /billing/usage, GET /billing/quota/{id}; quotas, usage ledger |
| Observability | `backend/shared/metrics.py`, `backend/shared/logging.py` | Prometheus /metrics (request count, latency, in-flight), structured logging with trace IDs |
| Total tests | `backend/tests/unit/` + `frontend/telegram/tests/` | 96 backend + 4 telegram = 100 total |

## Sprint 5 (implemented)

| Component | Location | Status |
|---|---|---|
| Changes page | `backend/apps/changes/` | GET /api/v1/changes, GET /changes/{id}/diff; version diff detection |
| Document upload | `backend/apps/document_upload/` | POST /documents/upload (multipart), GET /documents; MinIO + PG |
| Doc check export links | `backend/apps/doc_check/` | export_links (JSON/DOCX/PDF/XLSX) in CheckResponse |
| Doc check async | `backend/apps/doc_check/` | submit_check returns pending, background _execute_check, poll via GET /check/{job_id} |
| Export real formats | `backend/apps/export/` | python-docx (.docx), fpdf2 (.pdf), openpyxl (.xlsx) |
| SQLAlchemy ORM | `backend/shared/models/orm/` | Base, models for users/doc_check_jobs/internal_documents/drafts |
| BaseRepository | `backend/shared/repositories/` | Generic CRUD repository with PG + in-memory fallback |
| PG migration | multiple services | doc_check, document_upload, auth_billing, drafting — dual-mode PG/in-memory |
| Drafting | `backend/apps/drafting/` | GET /draft/{id}, GET /drafts added; PG-backed |
| Total tests | `backend/tests/unit/` | 92 total (83 + 6 doc_check + 3 document_upload) |

## Sprint 4 (implemented)

| Component | Location | Status |
|---|---|---|
| Qdrant client | `backend/shared/db/qdrant.py` | async wrapper, collection mgmt, upsert/search/delete |
| Vector Indexer | `backend/apps/vector_indexer/` | POST /api/v1/index, /search, /delete; hash-based embeddings |
| Retrieval upgrade | `backend/apps/retrieval/` | hybrid BM25 + Qdrant vector search with RRF fusion |
| LLM Verifier | `backend/apps/verification/` | `LlmVerifier` integrated into `/finalize`; rule-engine-first, LLM fallback when no API key |
| Gateway wiring | `backend/apps/gateway/` | all 18 service routers imported; 45+ endpoints unified |
| Dockerfiles | `backend/apps/*/Dockerfile` | all 18 services have individual Dockerfiles |
| Docker Compose | `docker-compose.yml` | all 18 service containers defined |
| CI/CD | `.github/workflows/ci-cd.yml` | builds all 18 images; `docker compose up -d --force-recreate` |

## Sprint 3 (implemented)

| Component | Location | Status |
|---|---|---|
| Obligation Extractor | `backend/apps/obligation_extractor/` | POST /api/v1/extract, norm/obligation extraction |
| Graph Service | `backend/apps/graph_service/` | in-memory graph store, POST /api/v1/sync, /query |
| Retrieval | `backend/apps/retrieval/` | BM25 + substring fallback, POST /api/v1/search |
| Verification | `backend/apps/verification/` | rule engine (sufficiency gate), precheck + finalize |
| Answer Service | `backend/apps/answer_service/` | orchestration: retrieval → verification → compose |

## Sprint 2 (implemented)

| Component | Location | Status |
|---|---|---|
| Crawler | `backend/apps/crawler/` | POST /crawl, GET /crawl/{id}/results, httpx-based fetch |
| Parser | `backend/apps/parser/` | POST /parse/html, BeautifulSoup fragment extraction |
| Versioning | `backend/apps/versioning/` | POST /documents/register, version detection, timeline |
| Regulatory fragments model | `backend/shared/models/fragments.py` | FragmentDto, DocumentVersionDto, CrawlResultDto |
| Internal API contracts | `docs/api/internal-contracts.md` | Crawler→Parser, Parser→Versioning contracts |

## Sprint 1 (implemented)

| Component | Location | Status |
|---|---|---|
| Monorepo scaffold | `podft-rag-platform/` | done |
| Semantic anchor schema | `project-schema.yaml` | done |
| Docker Compose | `docker-compose.yml` | postgres, qdrant, minio, redis, nginx, gateway + 14 microservices |
| Gateway (FastAPI) | `backend/apps/gateway/` | all 14 service routers wired; 37 endpoints under `/api/v1/*` |
| Auth-Billing | `backend/apps/auth_billing/` | register, login, profile (in-memory store) |
| Source-Registry | `backend/apps/source_registry/` | active sources + admin CRUD (in-memory) |
| DB init SQL | `infra/postgres/init/init.sql` | all 22 tables + indexes + seeds |
| CI/CD | `.github/workflows/ci-cd.yml` | ruff → mypy → pytest → docker push (14 images) → VPS deploy |
| E2E tests | `backend/tests/e2e/` | smoke tests for VPS deployment |

## Key files to know

- `project-schema.yaml` — semantic anchor meta-schema; every module has `__anchor__` referencing it
- `backend/shared/settings.py` — central pydantic-settings from `.env`
- `backend/shared/security.py` — JWT + bcrypt (not passlib)
- `backend/shared/db/qdrant.py` — async Qdrant client wrapper (384-dim, cosine distance)
- `backend/shared/db/neo4j.py` — async Neo4j client wrapper with connection pooling
- `backend/shared/llm/provider_router.py` — LLM abstraction layer with OpenRouter, OpenAI, YandexGPT, Mock
- `backend/shared/llm/clients/openrouter.py` — OpenRouter client (free model `poolside/laguna-xs-2.1:free`)
- `infra/postgres/init/init.sql` — single source of truth for DB schema
- `frontend/web/src/components/AboutPanel.tsx` — product page, pipeline schema, demo sandbox
- `frontend/web/src/components/DocCheckResultPage.tsx` — coverage/gaps/findings display

## Setup notes

- **Python 3.12+** required (project uses `uv`)
- Neo4j is **optional** in docker-compose; comment out on 1 GB VPS (enabled for local dev)
- VPS Trusty Viola: `62.217.183.95`, domain `vectornode.ru`
- HTTPS via Let's Encrypt in CI/CD deploy step
- GitHub: `https://github.com/madoper/podft`
- `.env` needs `LLM_PROVIDER=openrouter`, `LLM_API_KEY=sk-or-v1-...`, `LLM_MODEL=poolside/laguna-xs-2.1:free`

## UI/UX Redesign (Sprint 9) — Phase 0-5 Complete

| Phase | Component | Status |
|---|---|---|
| 0 (Infrastructure) | Tailwind CSS + lucide-react installed, vite config, token JSON files (primitives/semantic/components), tailwind.css entry, variables.css, dark.css | ✅ |
| 1 (Theming) | useTheme hook (useSyncExternalStore), ThemeProvider context, flash prevention in index.html, dark/light CSS variables | ✅ |
| 2 (Navigation) | AppShell (sidebar+topbar+main grid), Sidebar (collapsible 240→64px, 5 main items + 2 footer), TopBar (theme toggle, notifications), MobileTabBar (<768px), responsive media queries | ✅ |
| 3 (Backend) | ackend/apps/chat/ app (sessions CRUD, message history, feedback), SSE streaming endpoint GET /answer/{session_id}/stream, chat router wired in gateway | ✅ |
| 4 (Chat Screen) | ChatPanel (with useReducer), ChatHistory (Q&A list with citations), ChatInput (auto-grow textarea + quick template chips), CitationCard, FeedbackBar, SkeletonAnswer | ✅ |
| 5 (Accessibility) | ria-live="polite" on chat log, ole="status" on skeleton, ria-current="page" on nav, focus-visible rings, responsive 768px breakpoint | ✅ |

### Key files added/modified

- rontend/web/src/styles/tailwind.css, ariables.css, dark.css — NEW
- rontend/web/src/tokens/primitives.json, semantic.json, components.json — NEW
- rontend/web/src/hooks/useTheme.ts, useChat.ts, useChatAPI.ts — NEW
- rontend/web/src/components/ThemeProvider.tsx — NEW
- rontend/web/src/components/layout/AppShell.tsx, Sidebar.tsx, TopBar.tsx, MobileTabBar.tsx — NEW
- rontend/web/src/components/chat/ChatPanel.tsx, ChatHistory.tsx, ChatInput.tsx, CitationCard.tsx, FeedbackBar.tsx, SkeletonAnswer.tsx — NEW
- ackend/apps/chat/ — NEW (schemas, service, router)
- ackend/apps/answer_service/app/routers/answer.py — UPDATED (SSE streaming)
- ackend/apps/gateway/app/main.py — UPDATED (chat router wired)
- rontend/web/src/App.tsx — UPDATED (ThemeProvider, AppShell, ChatPanel)
- rontend/web/src/main.tsx — UPDATED (tailwind.css import)
- rontend/web/index.html — UPDATED (flash prevention)
- rontend/web/vite.config.ts — UPDATED (Tailwind plugin)

### Verification

- ruff: ✅ 0 errors
- mypy: ✅ 0 errors in 297 files
- pytest: ✅ 111/111 passed
- npm run build: ✅ clean build
