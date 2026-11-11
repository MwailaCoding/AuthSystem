import os
from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse

from mock_db import db
from schemas import (
    SignupRequest,
    LoginRequest,
    PasswordResetRequest,
    UserResponse,
    TokenResponse,
    MessageResponse,
    HealthResponse,
)

app = FastAPI(
    title="PrimeCloud Auth API",
    description="Mock Authentication System (Signup, Login, Password Reset) built for PrimeCloud deployment testing.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for cross-origin frontend or cloud API tests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer(auto_error=True)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = db.get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.get("/", include_in_schema=False)
def root():
    """Redirect root to interactive Swagger UI documentation"""
    return RedirectResponse(url="/docs")


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
    summary="Health and platform status check",
)
def health_check():
    """PrimeCloud Health Check endpoint for readiness and liveness probes."""
    return {
        "status": "healthy",
        "service": "PrimeCloud Auth Backend",
        "platform": os.environ.get("CLOUD_PLATFORM", "PrimeCloud"),
        "active_users": len(db.users),
        "active_tokens": len(db.tokens),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post(
    "/auth/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"],
    summary="Register a new user account",
)
def signup(payload: SignupRequest):
    """Registers a new user into the in-memory mock store."""
    try:
        new_user = db.create_user(
            name=payload.name, email=str(payload.email), password=payload.password
        )
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post(
    "/auth/login",
    response_model=TokenResponse,
    tags=["Authentication"],
    summary="User login with email and password",
)
def login(payload: LoginRequest):
    """Authenticates credentials and returns an opaque Bearer token."""
    user = db.get_user_by_email(str(payload.email))
    if not user or user["password"] != payload.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = db.create_token(user["email"])
    return {
        "access_token": token,
        "token_type": "Bearer",
        "user": user,
    }


@app.post(
    "/auth/reset-password",
    response_model=MessageResponse,
    tags=["Authentication"],
    summary="Single-step password reset by email",
)
def reset_password(payload: PasswordResetRequest):
    """Resets the user's password directly using email and new password."""
    try:
        db.reset_password(email=str(payload.email), new_password=payload.new_password)
        return {
            "message": "Password updated successfully",
            "detail": f"Password for {payload.email} has been updated.",
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.get(
    "/auth/me",
    response_model=UserResponse,
    tags=["Authentication"],
    summary="Get current authenticated user profile",
)
def get_me(current_user: dict = Depends(get_current_user)):
    """Protected endpoint to verify Bearer token authenticity."""
    return current_user


@app.post(
    "/auth/logout",
    response_model=MessageResponse,
    tags=["Authentication"],
    summary="Logout and invalidate token",
)
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Revokes the current Bearer token."""
    token = credentials.credentials
    revoked = db.revoke_token(token)
    if not revoked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token is already invalid or does not exist",
        )
    return {
        "message": "Logged out successfully",
        "detail": "Session token has been invalidated.",
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run("main:app", host=host, port=port, reload=True)
