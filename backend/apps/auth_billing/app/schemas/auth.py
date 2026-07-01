__anchor__ = "auth-billing"
# schema-ref: project-schema.yaml#/services/1

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ProfileResponse(BaseModel):
    user_id: str
    email: str
    tenant_id: str
    role: str
    anchor: str = "auth-billing"
