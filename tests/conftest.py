"""
Configuração global de fixtures para testes pytest
"""

import pytest
from ecommerce_analytics.api.main import app
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def fastapi_client() -> TestClient:
    """Fixture que fornece um cliente de teste para a API FastAPI."""
    return TestClient(app)


@pytest.fixture(scope="session")
def auth_token(fastapi_client: TestClient) -> str:
    """Fixture que obtém um token de autenticação válido para os testes."""
    response = fastapi_client.post("/login", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 200, f"Login falhou: {response.text}"
    return response.json()["access_token"]
