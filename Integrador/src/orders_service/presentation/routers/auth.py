from fastapi import APIRouter, HTTPException, status

from orders_service.infrastructure.security.jwt import create_access_token
from orders_service.presentation.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

DEMO_USER_EMAIL = "admin@example.com"
DEMO_USER_PASSWORD = "Admin1234!"


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest) -> TokenResponse:
    if data.email != DEMO_USER_EMAIL or data.password != DEMO_USER_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas.",
        )

    return TokenResponse(
        access_token=create_access_token(str(data.email)),
    )
