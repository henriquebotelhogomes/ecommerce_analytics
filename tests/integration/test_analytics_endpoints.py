"""
Testes de integração abrangentes para os endpoints de analytics da API.

Estratégia: Usar patch() dentro de cada teste para mockar BigQueryClient
com o path correto: 'ecommerce_analytics.api.routes.analytics.BigQueryClient'
"""

from unittest.mock import patch

import pandas as pd
import pytest
from ecommerce_analytics.core.exceptions import BigQueryError
from fastapi.testclient import TestClient


class TestAnalyticsEndpoints:
    """Testes para os endpoints de analytics (/api/v1/analytics/*)"""

    # ========== TESTES DE SUCESSO COM MOCK ==========

    def test_get_dashboard_success(self, fastapi_client: TestClient, auth_token: str) -> None:
        """
        Testa GET /api/v1/analytics/dashboard com token válido e dados mockados.
        """
        # Patch correto: sem 'src.' no início
        with patch("ecommerce_analytics.api.routes.analytics.BigQueryClient") as mock_bq:
            # Configurar mock
            mock_instance = mock_bq.return_value
            mock_instance.get_customer_metrics.return_value = {
                "total_customers": 100,
                "total_orders": 150,
                "avg_order_value": 200.0,
                "max_order_value": 1000.0,
                "total_revenue": 30000.0,
            }

            # Fazer requisição
            headers = {"Authorization": f"Bearer {auth_token}"}
            response = fastapi_client.get("/api/v1/analytics/dashboard", headers=headers)

            # Validar
            assert response.status_code == 200
            data = response.json()
            assert data["total_customers"] == 100
            assert data["total_orders"] == 150
            assert data["avg_order_value"] == 200.0
            mock_instance.get_customer_metrics.assert_called_once()

    def test_get_top_products_success(self, fastapi_client: TestClient, auth_token: str) -> None:
        """
        Testa GET /api/v1/analytics/top-products com token válido e limite customizado.
        """
        with patch("ecommerce_analytics.api.routes.analytics.BigQueryClient") as mock_bq:
            mock_instance = mock_bq.return_value
            mock_instance.get_top_products.return_value = pd.DataFrame(
                [
                    {
                        "product_id": "prod1",
                        "category": "cat1",
                        "total_sales": 10,
                        "revenue": 1000.0,
                    },
                    {"product_id": "prod2", "category": "cat2", "total_sales": 5, "revenue": 500.0},
                ]
            )

            headers = {"Authorization": f"Bearer {auth_token}"}
            limit = 5
            response = fastapi_client.get(
                f"/api/v1/analytics/top-products?limit={limit}", headers=headers
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["product_id"] == "prod1"
            assert data[1]["revenue"] == 500.0
            mock_instance.get_top_products.assert_called_once_with(limit=limit)

    def test_get_top_products_default_limit(
        self, fastapi_client: TestClient, auth_token: str
    ) -> None:
        """
        Testa GET /api/v1/analytics/top-products sem especificar limit.
        """
        with patch("ecommerce_analytics.api.routes.analytics.BigQueryClient") as mock_bq:
            mock_instance = mock_bq.return_value
            mock_instance.get_top_products.return_value = pd.DataFrame(
                [
                    {
                        "product_id": "prod1",
                        "category": "cat1",
                        "total_sales": 10,
                        "revenue": 1000.0,
                    },
                    {"product_id": "prod2", "category": "cat2", "total_sales": 5, "revenue": 500.0},
                ]
            )

            headers = {"Authorization": f"Bearer {auth_token}"}
            response = fastapi_client.get("/api/v1/analytics/top-products", headers=headers)

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            mock_instance.get_top_products.assert_called_once_with(limit=10)

    def test_get_sales_by_category_success(
        self, fastapi_client: TestClient, auth_token: str
    ) -> None:
        """
        Testa GET /api/v1/analytics/sales-by-category com token válido.
        """
        with patch("ecommerce_analytics.api.routes.analytics.BigQueryClient") as mock_bq:
            mock_instance = mock_bq.return_value
            mock_instance.get_sales_by_category.return_value = pd.DataFrame(
                [
                    {"category": "cat1", "total_orders": 50, "revenue": 5000.0, "avg_price": 100.0},
                    {"category": "cat2", "total_orders": 30, "revenue": 3000.0, "avg_price": 100.0},
                ]
            )

            headers = {"Authorization": f"Bearer {auth_token}"}
            response = fastapi_client.get("/api/v1/analytics/sales-by-category", headers=headers)

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["category"] == "cat1"
            assert data[1]["revenue"] == 3000.0
            mock_instance.get_sales_by_category.assert_called_once()

    # ========== TESTES DE AUTENTICAÇÃO (SEM TOKEN) ==========

    @pytest.mark.parametrize("endpoint", ["dashboard", "top-products", "sales-by-category"])
    def test_analytics_no_token(self, fastapi_client: TestClient, endpoint: str) -> None:
        """
        Testa acesso aos endpoints de analytics SEM token.
        HTTPBearer retorna 403 Forbidden.
        """
        response = fastapi_client.get(f"/api/v1/analytics/{endpoint}")
        assert response.status_code == 403

    # ========== TESTES DE AUTENTICAÇÃO (TOKEN INVÁLIDO) ==========

    @pytest.mark.parametrize("endpoint", ["dashboard", "top-products", "sales-by-category"])
    def test_analytics_invalid_token(self, fastapi_client: TestClient, endpoint: str) -> None:
        """
        Testa acesso aos endpoints de analytics com token INVÁLIDO.
        """
        headers = {"Authorization": "Bearer invalid_jwt_token_xyz"}
        response = fastapi_client.get(f"/api/v1/analytics/{endpoint}", headers=headers)
        assert response.status_code == 401
        assert "Token inválido ou expirado" in response.json()["detail"]

    # ========== TESTES DE ERRO DO BIGQUERY ==========

    def test_dashboard_bigquery_error(self, fastapi_client: TestClient, auth_token: str) -> None:
        """
        Testa GET /api/v1/analytics/dashboard quando BigQuery levanta erro.
        """
        with patch("ecommerce_analytics.api.routes.analytics.BigQueryClient") as mock_bq:
            mock_instance = mock_bq.return_value
            mock_instance.get_customer_metrics.side_effect = BigQueryError("Erro de conexão BQ")

            headers = {"Authorization": f"Bearer {auth_token}"}
            response = fastapi_client.get("/api/v1/analytics/dashboard", headers=headers)

            assert response.status_code == 500
            assert "Erro ao buscar métricas" in response.json()["detail"]
            mock_instance.get_customer_metrics.assert_called_once()

    def test_top_products_bigquery_error(self, fastapi_client: TestClient, auth_token: str) -> None:
        """
        Testa GET /api/v1/analytics/top-products quando BigQuery levanta erro.
        """
        with patch("ecommerce_analytics.api.routes.analytics.BigQueryClient") as mock_bq:
            mock_instance = mock_bq.return_value
            mock_instance.get_top_products.side_effect = BigQueryError("Erro de query BQ")

            headers = {"Authorization": f"Bearer {auth_token}"}
            response = fastapi_client.get("/api/v1/analytics/top-products", headers=headers)

            assert response.status_code == 500
            assert "Erro ao buscar produtos" in response.json()["detail"]
            mock_instance.get_top_products.assert_called_once()

    def test_sales_by_category_bigquery_error(
        self, fastapi_client: TestClient, auth_token: str
    ) -> None:
        """
        Testa GET /api/v1/analytics/sales-by-category quando BigQuery levanta erro.
        """
        with patch("ecommerce_analytics.api.routes.analytics.BigQueryClient") as mock_bq:
            mock_instance = mock_bq.return_value
            mock_instance.get_sales_by_category.side_effect = BigQueryError("Erro de dados BQ")

            headers = {"Authorization": f"Bearer {auth_token}"}
            response = fastapi_client.get("/api/v1/analytics/sales-by-category", headers=headers)

            assert response.status_code == 500
            assert "Erro ao buscar categorias" in response.json()["detail"]
            mock_instance.get_sales_by_category.assert_called_once()
