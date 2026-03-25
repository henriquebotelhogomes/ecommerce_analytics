"""
Aplicação FastAPI principal
"""

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from ecommerce_analytics.api.routes import analytics, forecast, recommendations
from ecommerce_analytics.api.schemas import LoginRequest, LoginResponse
from ecommerce_analytics.core.config import settings
from ecommerce_analytics.core.logger import setup_logger

# Configurar logger
logger = setup_logger(__name__)


# ============================================================================
# LIFESPAN EVENTS
# ============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    """Gerencia o ciclo de vida da aplicação"""
    # Startup
    logger.info("🚀 Iniciando E-commerce Analytics API")
    yield
    # Shutdown
    logger.info("🛑 Encerrando E-commerce Analytics API")


# ============================================================================
# CRIAR APLICAÇÃO
# ============================================================================

app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)

# ============================================================================
# CONFIGURAR CORS
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

# ============================================================================
# REGISTRAR ROTAS
# ============================================================================

app.include_router(analytics.router, prefix="/api/v1")
app.include_router(forecast.router, prefix="/api/v1")
app.include_router(recommendations.router, prefix="/api/v1")


# ============================================================================
# ENDPOINTS PÚBLICOS
# ============================================================================


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint"""
    return {"status": "ok"}


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint"""
    return {"message": "E-commerce Analytics API"}


@app.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest) -> LoginResponse:
    """Endpoint de login"""
    from ecommerce_analytics.api.auth import authenticate_user, create_access_token

    user = await authenticate_user(request.username, request.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha inválidos"
        )

    access_token = create_access_token(data={"sub": user["username"], "email": user["email"]})

    return LoginResponse(access_token=access_token, token_type="bearer")
