"""
Unit Tests - Configuration Module
Testa carregamento e validação de configurações.
"""

from ecommerce_analytics.core.config import settings


class TestSettings:
    """Testes para configurações da aplicação."""

    def test_settings_loaded(self):
        """Testa se as configurações foram carregadas."""
        assert settings is not None
        assert settings.app_name == "E-commerce Analytics API"

    def test_settings_default_values(self):
        """Testa valores padrão das configurações."""
        assert settings.environment == "development"
        assert settings.debug is True
        assert settings.port == 8000
        assert settings.host == "0.0.0.0"

    def test_settings_secret_key_exists(self):
        """Testa se secret_key está configurada."""
        assert settings.secret_key is not None
        assert len(settings.secret_key) >= 32

    def test_settings_cors_origins(self):
        """Testa se CORS origins estão configurados."""
        # cors_origins é armazenado como string no Settings
        assert isinstance(settings.cors_origins, str)
        assert len(settings.cors_origins) > 0

    def test_settings_cors_origins_list(self):
        """Testa se cors_origins_list retorna uma lista válida."""
        # cors_origins_list é a propriedade que converte para lista
        cors_list = settings.cors_origins_list
        assert isinstance(cors_list, list)
        assert len(cors_list) > 0
        assert "http://localhost" in cors_list

    def test_settings_bigquery_config(self):
        """Testa se configurações do BigQuery estão presentes."""
        assert settings.gcp_project_id is not None
        assert settings.gcp_dataset_id is not None

    def test_is_development(self):
        """Testa se is_development() funciona."""
        assert settings.is_development() is True

    def test_is_production(self):
        """Testa se is_production() funciona."""
        assert settings.is_production() is False

    def test_cors_origins_list_parsing(self):
        """Testa se cors_origins_list faz parsing correto."""
        cors_list = settings.cors_origins_list
        # Verificar que não há strings vazias
        assert all(origin for origin in cors_list)
        # Verificar que todos começam com http
        assert all(origin.startswith("http") for origin in cors_list)
