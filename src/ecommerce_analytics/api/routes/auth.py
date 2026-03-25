"""
Authentication Routes
JWT token generation and user authentication.
"""

from fastapi import APIRouter, HTTPException
from loguru import logger
from pydantic import BaseModel

from ecommerce_analytics.api.auth import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from ecommerce_analytics.core.exceptions import InvalidCredentialsError

router = APIRouter()


# ========== SCHEMAS ==========
class LoginRequest(BaseModel):
    """Login request schema."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"


# ========== HARDCODED USERS (Para testes) ==========
DEMO_USERS = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@example.com",
        "hashed_password": get_password_hash("admin123"),
        "disabled": False,
    }
}


# ========== ENDPOINTS ==========
@router.post("/login", response_model=TokenResponse, tags=["Authentication"])
async def login(credentials: LoginRequest) -> TokenResponse:
    """
    Login endpoint - Gera JWT token.

    **Credenciais de teste:**
    - username: admin
    - password: admin123
    """
    try:
        user = DEMO_USERS.get(credentials.username)

        # ✅ CORRETO: Validar tipo antes de usar
        if not user:
            logger.warning(f"❌ Login falhou para usuário: {credentials.username}")
            raise InvalidCredentialsError()

        hashed_password = user.get("hashed_password")
        if not isinstance(hashed_password, str):
            logger.warning(f"❌ Login falhou para usuário: {credentials.username}")
            raise InvalidCredentialsError()

        if not verify_password(credentials.password, hashed_password):
            logger.warning(f"❌ Login falhou para usuário: {credentials.username}")
            raise InvalidCredentialsError()

        access_token = create_access_token(data={"sub": user["username"]})
        logger.info(f"✅ Login bem-sucedido para: {credentials.username}")

        return TokenResponse(access_token=access_token, token_type="bearer")

    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.to_dict(),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except Exception as e:
        logger.error(f"❌ Erro inesperado no login: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"error": "INTERNAL_ERROR", "message": "Erro interno do servidor"},
        ) from e


@router.get("/me", tags=["Authentication"])
async def get_current_user(current_user: dict) -> dict:
    """Retorna informações do usuário autenticado."""
    return current_user
