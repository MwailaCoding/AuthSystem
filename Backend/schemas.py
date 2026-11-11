from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class SignupRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, examples=["John Doe"])
    email: EmailStr = Field(..., examples=["john@example.com"])
    password: str = Field(..., min_length=6, max_length=128, examples=["secret123"])

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., examples=["test@primecloud.io"])
    password: str = Field(..., min_length=1, examples=["password123"])

class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(..., examples=["test@primecloud.io"])
    new_password: str = Field(..., min_length=6, max_length=128, examples=["newpassword123"])

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    created_at: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    user: UserResponse

class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    service: str
    platform: str
    active_users: int
    active_tokens: int
    timestamp: str
