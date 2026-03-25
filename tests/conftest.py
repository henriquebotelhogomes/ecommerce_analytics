"""
Pytest Configuration and Fixtures
Configuração centralizada para testes.
"""

import pytest
from fastapi.testclient import TestClient

from ecommerce_analytics.api.main import app


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
