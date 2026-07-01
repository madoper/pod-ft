__anchor__ = "auth-billing"
# schema-ref: project-schema.yaml#/services/1/api/internal

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from backend.apps.auth_billing.app.schemas.auth import (
    LoginRequest,
    ProfileResponse,
    RegisterRequest,
    TokenResponse,
)
from backend.shared.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])
_users: dict[str, dict[str, Any]] = {}  # in-memory store until postgres is wired


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest) -> dict[str, object]:
    if payload.email in _users:
        raise HTTPException(status_code=409, detail="Email already registered")
    user_id = str(len(_users) + 1)
    _users[payload.email] = {
        "id": user_id,
        "email": payload.email,
        "password_hash": hash_password(payload.password),
        "tenant_id": user_id,
    }
    return {"user_id": user_id, "tenant_id": user_id, "anchor": "auth-billing"}


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest) -> TokenResponse:
    user = _users.get(payload.email)
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(subject=user["id"], tenant_id=user["tenant_id"])
    refresh_token = create_refresh_token(subject=user["id"])
    return TokenResponse(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.get("/profile", response_model=ProfileResponse)
async def profile(_authorization: str = Depends(lambda: None)) -> ProfileResponse:
    return ProfileResponse(user_id="1", email="user@example.com", tenant_id="1", role="user")
