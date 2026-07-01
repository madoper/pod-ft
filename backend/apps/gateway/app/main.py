__anchor__ = "gateway"
# schema-ref: project-schema.yaml#/services/0

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from backend.apps.answer_service.app.routers.answer import router as answer_router
from backend.apps.auth_billing.app.routers.auth import router as auth_router
from backend.apps.crawler.app.routers.crawl import router as crawl_router
from backend.apps.doc_check.app.routers.check import router as check_router
from backend.apps.drafting.app.routers.draft import router as draft_router
from backend.apps.export.app.routers.export import router as export_router
from backend.apps.gateway.app.routers import health
from backend.apps.graph_service.app.routers.graph import router as graph_router
from backend.apps.obligation_extractor.app.routers.extract import router as extract_router
from backend.apps.parser.app.routers.parse import router as parse_router
from backend.apps.retrieval.app.routers.search import router as search_router
from backend.apps.scheduler.app.routers.schedule import router as schedule_router
from backend.apps.source_registry.app.routers.sources import router as sources_router
from backend.apps.vector_indexer.app.routers.index import router as index_router
from backend.apps.verification.app.routers.verify import router as verify_router
from backend.apps.versioning.app.routers.version import router as version_router
from backend.apps.workers.app.routers.job import router as job_router
from backend.shared.logging import configure_logging, logger


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    logger.info("gateway starting", anchor="gateway")
    yield
    logger.info("gateway stopped", anchor="gateway")


app = FastAPI(
    title="pod-ft Gateway",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/openapi.json",
)

app.include_router(health.router)


@app.get("/")
async def root() -> RedirectResponse:
    return RedirectResponse(url="/api/v1/docs")


app.include_router(auth_router, prefix="/api/v1")
app.include_router(schedule_router, prefix="/api/v1")
app.include_router(sources_router, prefix="/api/v1")
app.include_router(job_router, prefix="/api/v1")
app.include_router(crawl_router, prefix="/api/v1")
app.include_router(parse_router, prefix="/api/v1")
app.include_router(version_router, prefix="/api/v1")
app.include_router(extract_router, prefix="/api/v1")
app.include_router(graph_router, prefix="/api/v1")
app.include_router(search_router, prefix="/api/v1")
app.include_router(verify_router, prefix="/api/v1")
app.include_router(answer_router, prefix="/api/v1")
app.include_router(index_router, prefix="/api/v1")
app.include_router(check_router, prefix="/api/v1")
app.include_router(draft_router, prefix="/api/v1")
app.include_router(export_router, prefix="/api/v1")
