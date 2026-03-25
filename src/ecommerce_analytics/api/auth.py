"""
Authentication Module
JWT token generation, validation, and password hashing.
Production-ready authentication with FastAPI integration.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from loguru import logger
from passlib.context import CryptContext
from pydantic import BaseModel

from ecommerce_analytics.core.config import settings
from ecommerce_analytics.core.exceptions import (
    InvalidTokenError,
    MissingTokenError,
)

# ========== PASSWORD HASHING ==========
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=65536,
    argon2__time_cost=3,
    argon2__parallelism=4,
)

# ========== JWT CONFIGURATION ==========
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ========== SECURITY SCHEME ==========
security = HTTPBearer()


# ========== SCHEMAS ==========
class TokenData(BaseModel):
    """Token payload schema."""

    username: Optional[str] = None
    exp: Optional[datetime] = None


class User(BaseModel):
    """User schema."""

    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = False


class UserInDB(User):
    """User in database schema."""

    hashed_password: str


# ========== PASSWORD FUNCTIONS ==========
def get_password_hash(password: str) -> str:
    """
    Hash a password using Argon2.

    Args:
        password: Plain text password

    Returns:
        Hashed password
    """
    try:
        hashed = pwd_context.hash(password)
        logger.debug("✅ Password hashed successfully")
        return hashed
    except Exception as e:
        logger.error(f"❌ Error hashing password: {str(e)}")
        raise


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password

    Returns:
        True if password matches, False otherwise
    """
    try:
        is_valid = pwd_context.verify(plain_password, hashed_password)
        if is_valid:
            logger.debug("✅ Password verified successfully")
        else:
            logger.warning("❌ Password verification failed")
        return is_valid
    except Exception as e:
        logger.error(f"❌ Error verifying password: {str(e)}")
        return False


# ========== TOKEN FUNCTIONS ==========
def create_access_token(
    data: dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a JWT access token.

    Args:
        data: Data to encode in token
        expires_delta: Token expiration time (default: 30 minutes)

    Returns:
        Encoded JWT token
    """
    try:
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=ALGORITHM,
        )

        logger.debug(f"✅ Token created for user: {data.get('sub')}")
        return encoded_jwt

    except Exception as e:
        logger.error(f"❌ Error creating token: {str(e)}")
        raise


def verify_token(token: str) -> dict[str, Any]:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token to verify

    Returns:
        Token payload

    Raises:
        InvalidTokenError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM],
        )
        username: str | None = payload.get("sub")

        if username is None:
            logger.warning("❌ Token missing 'sub' claim")
            raise InvalidTokenError("Token inválido: falta 'sub' claim") from None

        logger.debug(f"✅ Token verified for user: {username}")
        return payload

    except JWTError as e:
        logger.warning(f"❌ JWT error: {str(e)}")
        raise InvalidTokenError(f"Token inválido: {str(e)}") from e
    except InvalidTokenError:
        raise
    except Exception as e:
        logger.error(f"❌ Error verifying token: {str(e)}")
        raise InvalidTokenError(f"Erro ao verificar token: {str(e)}") from e


# ========== DEPENDENCY INJECTION ==========
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict[str, Any]:
    """
    Get current authenticated user from JWT token.

    Args:
        credentials: HTTP Bearer credentials (injected by FastAPI)

    Returns:
        User data from token

    Raises:
        MissingTokenError: If token is missing
        InvalidTokenError: If token is invalid
    """
    try:
        if not credentials:
            logger.warning("❌ Missing authentication credentials")
            raise MissingTokenError()

        token = credentials.credentials

        if not token:
            logger.warning("❌ Missing token in credentials")
            raise MissingTokenError()

        payload = verify_token(token)

        username: str | None = payload.get("sub")
        if username is None:
            logger.warning("❌ Username not found in token")
            raise InvalidTokenError("Username não encontrado no token") from None

        logger.debug(f"✅ User authenticated: {username}")

        return {
            "username": username,
            "email": payload.get("email"),
            "full_name": payload.get("full_name"),
        }

    except (MissingTokenError, InvalidTokenError) as e:
        logger.warning(f"❌ Authentication failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.to_dict() if hasattr(e, "to_dict") else str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except Exception as e:
        logger.error(f"❌ Unexpected error in authentication: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor",
        ) from e


async def get_current_active_user(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """
    Get current active user (not disabled).

    Args:
        current_user: Current authenticated user (injected by FastAPI)

    Returns:
        User data if active

    Raises:
        HTTPException: If user is disabled
    """
    if current_user.get("disabled"):
        logger.warning(f"❌ Disabled user attempted access: {current_user['username']}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário desativado",
        )

    logger.debug(f"✅ Active user verified: {current_user['username']}")
    return current_user
