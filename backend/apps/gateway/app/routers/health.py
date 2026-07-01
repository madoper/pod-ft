__anchor__ = "gateway"
# schema-ref: project-schema.yaml#/services/0/api/public

from fastapi import APIRouter

from backend.apps.gateway.app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", service="gateway", anchor="gateway")


@router.get("/api/v1/health", response_model=HealthResponse)
async def api_health() -> HealthResponse:
    return HealthResponse(status="ok", service="gateway", version="0.1.0", anchor="gateway")
