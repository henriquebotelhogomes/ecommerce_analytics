"""
Integration Tests - API Endpoints
Testa endpoints principais da API.
"""


class TestAPI:
    """Testes da API principal."""

    def test_health_check(self, client):
        """Testa health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "ecommerce-analytics-api"

    def test_root_endpoint(self, client):
        """Testa root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "E-commerce Analytics API"

    def test_login_success(self, client):
        """Testa login bem-sucedido."""
        response = client.post("/auth/login", json={"username": "admin", "password": "admin123"})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_failure(self, client):
        """Testa login com credenciais inválidas."""
        response = client.post(
            "/auth/login", json={"username": "admin", "password": "wrong_password"}
        )
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data


class TestAnalyticsEndpoints:
    """Testes dos endpoints de analytics."""

    def test_get_dashboard_success(self, client, auth_headers):
        """Testa obtenção do dashboard com autenticação."""
        response = client.get("/api/v1/analytics/dashboard", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_revenue" in data
        assert "top_products" in data
        assert "sales_by_category" in data

    def test_get_dashboard_no_auth(self, client):
        """Testa obtenção do dashboard sem autenticação."""
        response = client.get("/api/v1/analytics/dashboard")
        # HTTPBearer retorna 401 (Unauthorized) quando token falta, não 403
        assert response.status_code == 401


class TestForecastEndpoints:
    """Testes dos endpoints de forecasting."""

    def test_forecast_revenue_success(self, client, auth_headers):
        """Testa previsão de receita com autenticação."""
        response = client.post(
            "/api/v1/forecast/revenue", json={"months_ahead": 3}, headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "forecast" in data

    def test_forecast_revenue_no_auth(self, client):
        """Testa previsão de receita sem autenticação."""
        response = client.post("/api/v1/forecast/revenue", json={"months_ahead": 3})
        # HTTPBearer retorna 401 (Unauthorized) quando token falta, não 403
        assert response.status_code == 401


class TestRecommendationsEndpoints:
    """Testes dos endpoints de recomendações."""

    def test_get_recommendations_success(self, client, auth_headers):
        """Testa obtenção de recomendações com autenticação."""
        response = client.post(
            "/api/v1/recommendations/products",
            json={"customer_id": "CUST001"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "recommendations" in data

    def test_get_recommendations_no_auth(self, client):
        """Testa obtenção de recomendações sem autenticação."""
        response = client.post("/api/v1/recommendations/products", json={"customer_id": "CUST001"})
        # HTTPBearer retorna 401 (Unauthorized) quando token falta, não 403
        assert response.status_code == 401
