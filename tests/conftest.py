"""
Pytest Configuration and Fixtures
Configuração centralizada para testes com mocks para BigQuery.
"""

from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from ecommerce_analytics.api.main import app

# ========== FIXTURES BÁSICAS ==========
from ecommerce_analytics.api.routes.analytics import get_analytics_service
from ecommerce_analytics.api.routes.forecast import get_forecast_service
from ecommerce_analytics.api.routes.recommendations import get_recommendation_service


@pytest.fixture
def client(mock_analytics_service, mock_forecast_service, mock_ml_service):
    """Cria cliente de teste para a API."""
    app.dependency_overrides[get_analytics_service] = lambda: mock_analytics_service
    app.dependency_overrides[get_forecast_service] = lambda: mock_forecast_service
    app.dependency_overrides[get_recommendation_service] = lambda: mock_ml_service
    yield TestClient(app)
    app.dependency_overrides.clear()


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


# ========== FIXTURES DE SERVIÇOS (MOCKS TOTAL) ==========

@pytest.fixture
def mock_analytics_service():
    service = MagicMock()
    service.get_dashboard_data.return_value = {
        "total_revenue": 1000000.0,
        "total_orders": 5000,
        "avg_order_value": 200.0,
        "total_customers": 1500,
        "revenue_trend": [100, 200],
        "orders_trend": [10, 20],
        "top_products": [{"name": "P1", "sales": 100}],
        "sales_by_category": [{"category": "C1", "sales": 100}],
    }
    return service

@pytest.fixture
def mock_forecast_service():
    service = MagicMock()
    # The integration tests expect forecast to return dict with "forecast" but wait, the endpoint returns:
    # return {"status": "success", "forecast": forecast} inside API. The service just returns list of dicts.
    service.get_revenue_forecast.return_value = [
        {"month": "Apr 2026", "predicted_revenue": 50000.0}
    ]
    return service

@pytest.fixture
def mock_ml_service():
    service = MagicMock()
    service.get_product_recommendations.return_value = [
        {"product_id": "P1", "name": "Prod A", "score": 0.9}
    ]
    return service
