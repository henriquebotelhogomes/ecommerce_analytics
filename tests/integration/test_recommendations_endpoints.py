"""
Testes de integração para endpoints de recomendações
"""

from unittest.mock import patch

from ecommerce_analytics.core.exceptions import BigQueryError
from fastapi.testclient import TestClient


class TestRecommendationsEndpoints:
    """Testes para os endpoints de recomendações (/api/v1/recommendations/*)"""

    def test_get_product_recommendations_success(
        self, fastapi_client: TestClient, auth_token: str
    ) -> None:
        """Testa GET /api/v1/recommendations/products com token válido."""
        customer_id = "customer_123"

        with patch("ecommerce_analytics.api.routes.recommendations.BigQueryClient"):
            headers = {"Authorization": f"Bearer {auth_token}"}
            response = fastapi_client.get(
                f"/api/v1/recommendations/products?customer_id={customer_id}", headers=headers
            )

            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)

    def test_recommendations_no_token(self, fastapi_client: TestClient) -> None:
        """Testa acesso sem token."""
        customer_id = "customer_123"
        response = fastapi_client.get(f"/api/v1/recommendations/products?customer_id={customer_id}")
        assert response.status_code == 403

    def test_recommendations_invalid_token(self, fastapi_client: TestClient) -> None:
        """Testa acesso com token inválido."""
        customer_id = "customer_123"
        headers = {"Authorization": "Bearer invalid_jwt_token_xyz"}
        response = fastapi_client.get(
            f"/api/v1/recommendations/products?customer_id={customer_id}", headers=headers
        )
        assert response.status_code == 401
        assert "Token inválido ou expirado" in response.json()["detail"]

    def test_recommendations_bigquery_error(
        self, fastapi_client: TestClient, auth_token: str
    ) -> None:
        """Testa erro do BigQuery."""
        customer_id = "customer_123"
        with patch("ecommerce_analytics.api.routes.recommendations.BigQueryClient") as mock_bq:
            mock_instance = mock_bq.return_value
            mock_instance.query.side_effect = BigQueryError("Erro ao buscar dados")

            headers = {"Authorization": f"Bearer {auth_token}"}
            response = fastapi_client.get(
                f"/api/v1/recommendations/products?customer_id={customer_id}", headers=headers
            )

            assert response.status_code == 500
            assert "Erro ao buscar recomendações" in response.json()["detail"]
