"""
Testes unitários para configurações
"""

from ecommerce_analytics.core.config import Settings


class TestSettings:
    """Testes para a classe Settings"""

    def test_settings_default_values(self) -> None:
        """Testa valores padrão"""
        settings = Settings()

        assert settings.gcp_project_id == "ecommerce-analytics-491215"
        assert settings.gcp_dataset_id == "olist_ecommerce"
        assert settings.app_version == "1.0.0"  # ✅ CORRIGIDO: app_version em vez de api_version
        assert settings.app_name == "E-commerce Analytics API"
        assert settings.log_level == "INFO"

    def test_settings_custom_values(self) -> None:
        """Testa valores customizados via variáveis de ambiente"""
        import os

        # Salvar valores originais
        original_project = os.environ.get("GCP_PROJECT_ID")
        original_dataset = os.environ.get("GCP_DATASET_ID")

        try:
            # Definir valores customizados
            os.environ["GCP_PROJECT_ID"] = "custom-project"
            os.environ["GCP_DATASET_ID"] = "custom-dataset"

            # Criar nova instância com valores customizados
            settings = Settings()

            assert settings.gcp_project_id == "custom-project"
            assert settings.gcp_dataset_id == "custom-dataset"
        finally:
            # Restaurar valores originais
            if original_project:
                os.environ["GCP_PROJECT_ID"] = original_project
            else:
                os.environ.pop("GCP_PROJECT_ID", None)

            if original_dataset:
                os.environ["GCP_DATASET_ID"] = original_dataset
            else:
                os.environ.pop("GCP_DATASET_ID", None)
