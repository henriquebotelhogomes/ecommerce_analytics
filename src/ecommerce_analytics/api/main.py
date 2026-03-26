"""
FastAPI Application - E-commerce Analytics Platform
Production-ready API with JWT authentication and BigQuery integration.
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from ecommerce_analytics.api.routes import analytics, auth, forecast, recommendations
from ecommerce_analytics.core.config import settings


# ========== LIFESPAN CONTEXT MANAGER ==========
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia startup e shutdown da aplicação."""
    # Startup
    logger.info("🚀 E-commerce Analytics API iniciando...")
    logger.info(f"📊 Ambiente: {settings.environment}")
    logger.info("🔐 Autenticação: JWT + OAuth2")
    logger.info(f"🌐 CORS Origins: {settings.cors_origins_list}")
    yield
    # Shutdown
    logger.info("🛑 E-commerce Analytics API encerrando...")


# ========== CRIAR APP ==========
app = FastAPI(
    title="E-commerce Analytics API",
    description="Production-ready analytics platform with BigQuery integration",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.is_development() else None,  # Desabilitar docs em produção
    redoc_url="/redoc" if settings.is_development() else None,
)

# ========== CORS MIDDLEWARE ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== HEALTH CHECK ==========
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint para Cloud Run."""
    return {
        "status": "healthy",
        "service": "ecommerce-analytics-api",
        "version": "1.0.0",
        "environment": settings.environment,
    }


# ========== ROOT ENDPOINT ==========
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "E-commerce Analytics API",
        "docs": "/docs" if settings.is_development() else None,
        "health": "/health",
    }


# ========== REGISTRAR ROUTERS ==========
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(forecast.router, prefix="/api/v1/forecast", tags=["Forecasting"])
app.include_router(
    recommendations.router, prefix="/api/v1/recommendations", tags=["Recommendations"]
)

logger.info("✅ Todos os routers registrados com sucesso")

# ========== ENTRY POINT ==========
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run(app, host=host, port=port, log_level="info")
