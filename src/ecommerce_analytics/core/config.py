"""
Configuração centralizada da aplicação usando Pydantic v2
"""


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação"""

    # ============================================================================
    # CONFIGURAÇÕES GERAIS
    # ============================================================================

    app_name: str = "E-commerce Analytics API"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"

    # ============================================================================
    # CONFIGURAÇÕES GCP / BIGQUERY
    # ============================================================================

    gcp_project_id: str = "ecommerce-analytics-491215"
    gcp_dataset_id: str = "olist_ecommerce"

    # ============================================================================
    # CONFIGURAÇÕES JWT / AUTENTICAÇÃO
    # ============================================================================

    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # ============================================================================
    # CONFIGURAÇÕES CORS
    # ============================================================================

    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:8050",
        "http://127.0.0.1:8050",
    ]
    cors_credentials: bool = True
    cors_methods: list[str] = ["*"]
    cors_headers: list[str] = ["*"]

    # ============================================================================
    # CONFIGURAÇÕES PYDANTIC V2
    # ============================================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


# Instância global de configurações
settings = Settings()
