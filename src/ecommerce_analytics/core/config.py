"""
Configuration Module
Application settings and environment variables.
"""

from loguru import logger
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # ========== APPLICATION ==========
    app_name: str = "E-commerce Analytics API"
    app_version: str = "1.0.0"
    environment: str = Field(
        default="development", description="Environment: development, staging, production"
    )
    debug: bool = Field(default=False, description="Debug mode (NEVER true in production)")

    # ========== SERVER ==========
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    reload: bool = Field(default=False, description="Auto-reload on code changes")

    # ========== SECURITY ==========
    secret_key: str = Field(
        default="change-me-in-production-min-32-chars",
        min_length=32,
        description="JWT secret key (min 32 chars)",
    )
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(default=30, description="Token expiration in minutes")

    # ========== CORS ==========
    cors_origins: str = Field(
        default="http://localhost,http://localhost:3000,http://localhost:8000,http://localhost:8501",
        description="Comma-separated CORS origins",
    )

    # ========== BIGQUERY ==========
    gcp_project_id: str = Field(
        default="ecommerce-analytics-491215", description="Google Cloud Project ID"
    )
    gcp_dataset_id: str = Field(default="olist_ecommerce", description="BigQuery Dataset ID")

    # ========== LOGGING ==========
    log_level: str = Field(default="INFO", description="Logging level")

    # ========== MODEL CONFIG ==========
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    # ========== VALIDATORS ==========
    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validar que secret_key tem pelo menos 32 caracteres."""
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        if v == "change-me-in-production-min-32-chars":
            logger.warning("⚠️  SECRET_KEY is using default value. Change it in production!")
        return v

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validar que environment é um valor válido."""
        valid_envs = ["development", "staging", "production"]
        if v not in valid_envs:
            raise ValueError(f"ENVIRONMENT must be one of {valid_envs}")
        return v

    @field_validator("debug")
    @classmethod
    def validate_debug(cls, v: bool, info) -> bool:
        """Validar que debug não está ativo em produção."""
        environment = info.data.get("environment")
        if v and environment == "production":
            raise ValueError("DEBUG cannot be True in production environment")
        return v

    @field_validator("cors_origins", mode="before")
    @classmethod
    def validate_cors_origins(cls, v) -> str:
        """Validar e normalizar CORS origins."""
        if isinstance(v, list):
            # Se vier como lista (do .env ou programaticamente), converter para string
            return ",".join(v)
        if isinstance(v, str):
            # Se vier como string, apenas retornar
            return v
        raise ValueError("CORS_ORIGINS must be a string or list")

    @property
    def cors_origins_list(self) -> list[str]:
        """Retornar CORS origins como lista."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    def is_production(self) -> bool:
        """Verificar se está em produção."""
        return self.environment == "production"

    def is_development(self) -> bool:
        """Verificar se está em desenvolvimento."""
        return self.environment == "development"


# ========== SINGLETON INSTANCE ==========
settings = Settings()

# ========== LOGGING ==========
logger.info(f"✅ Settings loaded: {settings.app_name} v{settings.app_version}")
logger.info(f"📍 Environment: {settings.environment}")
logger.info(f"🔐 Debug mode: {settings.debug}")
logger.info(f"🌐 CORS Origins: {settings.cors_origins_list}")

if settings.is_production():
    logger.warning("⚠️  PRODUCTION MODE ACTIVE - Ensure all secrets are properly configured!")
