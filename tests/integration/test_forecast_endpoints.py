"""
Testes de integração para endpoints de forecast
"""

from unittest.mock import patch

import pandas as pd
from ecommerce_analytics.core.exceptions import BigQueryError
from fastapi.testclient import TestClient


class TestForecastEndpoints:
    """Testes para o endpoint de previsão (/api/v1/forecast/revenue)"""

    def test_forecast_revenue_success(self, fastapi_client: TestClient, auth_token: str) -> None:
        """Testa GET /api/v1/forecast/revenue com token válido e dados mockados."""
        with patch("ecommerce_analytics.api.routes.forecast.BigQueryClient") as mock_bq:
            mock_instance = mock_bq.return_value
            mock_instance.query.return_value = pd.DataFrame(
                {
                    "date": pd.to_datetime(["2026-01-01", "2026-02-01", "2026-03-01"]),
                    "revenue": [10000.0, 11000.0, 12000.0],
                }
            )

            headers = {"Authorization": f"Bearer {auth_token}"}
            months_param = 3
            response = fastapi_client.get(
                f"/api/v1/forecast/revenue?months={months_param}", headers=headers
            )

            assert response.status_code == 200
            data = response.json()
            assert "forecast" in data
            assert data["months"] == months_param
            mock_instance.query.assert_called_once()

    def test_forecast_revenue_no_token(self, fastapi_client: TestClient) -> None:
        """Testa acesso sem token."""
        response = fastapi_client.get("/api/v1/forecast/revenue")
        assert response.status_code == 403

    def test_forecast_revenue_invalid_token(self, fastapi_client: TestClient) -> None:
        """Testa acesso com token inválido."""
        headers = {"Authorization": "Bearer invalid_jwt_token_xyz"}
        response = fastapi_client.get("/api/v1/forecast/revenue", headers=headers)
        assert response.status_code == 401
        assert "Token inválido ou expirado" in response.json()["detail"]

    def test_forecast_revenue_bigquery_error(
        self, fastapi_client: TestClient, auth_token: str
    ) -> None:
        """Testa erro do BigQuery."""
        with patch("ecommerce_analytics.api.routes.forecast.BigQueryClient") as mock_bq:
            mock_instance = mock_bq.return_value
            mock_instance.query.side_effect = BigQueryError("Erro de conexão com BigQuery")

            headers = {"Authorization": f"Bearer {auth_token}"}
            response = fastapi_client.get("/api/v1/forecast/revenue", headers=headers)

            assert response.status_code == 500
            assert "Erro ao gerar previsão" in response.json()["detail"]
