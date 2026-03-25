"""
Testes de integração para API
"""

import pytest


@pytest.mark.integration
class TestAPI:
    """Testes da API"""

    def test_health_check(self, fastapi_client):
        """Testa health check"""
        response = fastapi_client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_root_endpoint(self, fastapi_client):
        """Testa endpoint raiz"""
        response = fastapi_client.get("/")

        assert response.status_code == 200
        assert "message" in response.json()

    def test_login_success(self, fastapi_client):
        """Testa login bem-sucedido"""
        response = fastapi_client.post("/login", json={"username": "admin", "password": "admin123"})

        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_failure(self, fastapi_client):
        """Testa falha no login"""
        response = fastapi_client.post("/login", json={"username": "admin", "password": "wrong"})

        assert response.status_code == 401
