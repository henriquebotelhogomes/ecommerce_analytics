"""
Pytest Configuration and Fixtures
Configuração centralizada para testes com mocks para BigQuery.
"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from ecommerce_analytics.api.main import app

# ========== FIXTURES BÁSICAS ==========


@pytest.fixture
def client():
    """Cria cliente de teste para a API."""
    return TestClient(app)


@pytest.fixture
def auth_token(client):
    """Gera token de autenticação para testes."""
    response = client.post("/auth/login", json={"username": "admin", "password": "admin123"})

    assert response.status_code == 200, f"Login falhou: {response.text}"

    token = response.json()["access_token"]
    return token


@pytest.fixture
def auth_headers(auth_token):
    """Retorna headers com token de autenticação."""
    return {"Authorization": f"Bearer {auth_token}"}


# ========== FIXTURES PARA MOCKAR BIGQUERY ==========


@pytest.fixture
def mock_bigquery_client():
    """Mock BigQuery client para testes de integração."""
    with patch("google.cloud.bigquery.Client") as mock_client:
        client = MagicMock()
        mock_client.return_value = client
        yield client


@pytest.fixture
def mock_bigquery_query_job():
    """Mock BigQuery query job result."""
    mock_job = MagicMock()
    mock_job.result.return_value = [
        {
            "total_revenue": 1000000.0,
            "total_orders": 5000,
            "avg_order_value": 200.0,
            "total_customers": 1500,
        }
    ]
    return mock_job


@pytest.fixture
def mock_analytics_service(mock_bigquery_client, mock_bigquery_query_job):
    """Mock AnalyticsService com BigQuery client."""
    with patch("ecommerce_analytics.services.analytics_service.bigquery.Client") as mock_bq:
        mock_bq.return_value = mock_bigquery_client
        mock_bigquery_client.query.return_value = mock_bigquery_query_job

        from ecommerce_analytics.services.analytics_service import AnalyticsService

        service = AnalyticsService()
        service.client = mock_bigquery_client

        yield service


@pytest.fixture
def mock_forecast_service(mock_bigquery_client, mock_bigquery_query_job):
    """Mock ForecastService com BigQuery client."""
    with patch("ecommerce_analytics.services.forecast_service.bigquery.Client") as mock_bq:
        mock_bq.return_value = mock_bigquery_client
        mock_bigquery_client.query.return_value = mock_bigquery_query_job

        from ecommerce_analytics.services.forecast_service import ForecastService

        service = ForecastService()
        service.client = mock_bigquery_client

        yield service


@pytest.fixture
def mock_ml_service(mock_bigquery_client, mock_bigquery_query_job):
    """Mock MLService com BigQuery client."""
    with patch("ecommerce_analytics.services.ml_service.bigquery.Client") as mock_bq:
        mock_bq.return_value = mock_bigquery_client
        mock_bigquery_client.query.return_value = mock_bigquery_query_job

        from ecommerce_analytics.services.ml_service import MLService

        service = MLService()
        service.client = mock_bigquery_client

        yield service


# ========== FIXTURES PARA DADOS DE TESTE ==========


@pytest.fixture
def sample_dashboard_data():
    """Dados de exemplo para testes de dashboard."""
    return {
        "total_revenue": 1000000.0,
        "total_orders": 5000,
        "avg_order_value": 200.0,
        "total_customers": 1500,
    }


@pytest.fixture
def sample_forecast_data():
    """Dados de exemplo para testes de forecast."""
    return [
        {"forecast_date": "2026-04-01", "predicted_revenue": 50000.0},
        {"forecast_date": "2026-04-02", "predicted_revenue": 52000.0},
        {"forecast_date": "2026-04-03", "predicted_revenue": 51500.0},
    ]


@pytest.fixture
def sample_recommendations_data():
    """Dados de exemplo para testes de recomendações."""
    return [
        {"product_id": "prod_001", "product_name": "Produto A", "score": 0.95},
        {"product_id": "prod_002", "product_name": "Produto B", "score": 0.87},
        {"product_id": "prod_003", "product_name": "Produto C", "score": 0.76},
    ]
