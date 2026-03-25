"""
Autenticação JWT para FastAPI
"""

import logging
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from ecommerce_analytics.core.config import settings
from ecommerce_analytics.core.exceptions import AuthenticationError

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha corresponde ao hash"""
    try:
        result: bool = pwd_context.verify(plain_password, hashed_password)  # ✅ CORRIGIDO
        return result
    except Exception as e:
        logger.error(f"❌ Erro ao verificar senha: {str(e)}")
        return False


def get_password_hash(password: str) -> str:
    """Gera hash da senha com Argon2"""
    result: str = pwd_context.hash(password)  # ✅ CORRIGIDO
    return result


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None  # ✅ CORRIGIDO: type parameter
) -> str:
    """Cria um token JWT"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})

    try:
        encoded_jwt: str = jwt.encode(  # ✅ CORRIGIDO
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )
        return encoded_jwt
    except Exception as e:
        logger.error(f"❌ Erro ao criar token: {str(e)}")
        raise AuthenticationError("Erro ao criar token de acesso")


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict[str, Any]:  # ✅ CORRIGIDO: return type
    """Verifica e decodifica um token JWT"""
    token = credentials.credentials

    try:
        payload: dict[str, Any] = jwt.decode(  # ✅ CORRIGIDO
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        return payload
    except JWTError as e:
        logger.warning(f"⚠️  Token inválido: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ============================================================================
# USUÁRIOS DEMO - LAZY LOADING
# ============================================================================


def get_demo_users() -> dict[str, dict[str, Any]]:  # ✅ CORRIGIDO: type parameter
    """
    Retorna usuários demo com senhas hashadas.
    Usa lazy loading para evitar problemas de compatibilidade.
    """
    return {
        "admin": {
            "username": "admin",
            "full_name": "Admin User",
            "email": "admin@example.com",
            "hashed_password": get_password_hash("admin123"),
            "disabled": False,
        }
    }


async def authenticate_user(
    username: str, password: str
) -> dict[str, Any] | None:  # ✅ CORRIGIDO: return type
    """Autentica um usuário"""
    demo_users = get_demo_users()
    user = demo_users.get(username)

    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user
