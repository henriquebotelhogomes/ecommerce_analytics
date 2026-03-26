"""
Plotly Dash Dashboard - E-commerce Analytics
Interactive visualization with real data from FastAPI API.
"""

import os

import plotly.graph_objects as go
import requests
from dash import Dash, Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate
from loguru import logger

# ========== CONFIGURAÇÃO ==========
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080")
DASH_HOST = os.getenv("DASH_HOST", "0.0.0.0")
DASH_PORT = int(os.getenv("DASH_PORT", 8050))

logger.info("🎨 Dashboard iniciando...")
logger.info(f"📡 API Base URL: {API_BASE_URL}")

# ========== VARIÁVEIS GLOBAIS ==========
AUTH_TOKEN = None  # Será preenchido após login

# ========== CRIAR APP DASH ==========
app = Dash(
    __name__,
    title="E-commerce Analytics Dashboard",
    suppress_callback_exceptions=True,
)

# ========== LAYOUT ==========
app.layout = html.Div(
    [
        # ========== HEADER ==========
        html.Div(
            [
                html.H1("📊 E-Commerce Analytics Dashboard", style={"color": "#1f77b4"}),
                html.P("Real-time insights powered by BigQuery ML", style={"color": "#666"}),
            ],
            style={
                "padding": "20px",
                "backgroundColor": "#f8f9fa",
                "borderBottom": "2px solid #1f77b4",
                "marginBottom": "20px",
            },
        ),
        # ========== AUTENTICAÇÃO ==========
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Usuário:", style={"fontWeight": "bold"}),
                        dcc.Input(
                            id="username-input",
                            type="text",
                            placeholder="admin",
                            value="admin",
                            style={"padding": "8px", "marginRight": "10px", "width": "150px"},
                        ),
                        html.Label("Senha:", style={"fontWeight": "bold", "marginLeft": "20px"}),
                        dcc.Input(
                            id="password-input",
                            type="password",
                            placeholder="admin123",
                            value="admin123",
                            style={"padding": "8px", "marginRight": "10px", "width": "150px"},
                        ),
                        html.Button(
                            "Entrar",
                            id="login-button",
                            n_clicks=0,
                            style={
                                "padding": "8px 20px",
                                "backgroundColor": "#1f77b4",
                                "color": "white",
                                "border": "none",
                                "borderRadius": "4px",
                                "cursor": "pointer",
                                "marginLeft": "10px",
                            },
                        ),
                        html.Div(id="login-status", style={"marginLeft": "20px", "color": "green"}),
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "padding": "15px",
                        "backgroundColor": "#f0f0f0",
                        "borderRadius": "4px",
                        "marginBottom": "20px",
                    },
                ),
            ],
            style={"padding": "0 20px"},
        ),
        # ========== TABS ==========
        dcc.Tabs(
            id="tabs",
            value="tab-1",
            children=[
                # ========== TAB 1: OVERVIEW ==========
                dcc.Tab(
                    label="📈 Visão Geral",
                    value="tab-1",
                    children=[
                        html.Div(
                            [
                                # Métricas principais
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H3(
                                                    "Receita Total", style={"margin": "0 0 10px 0"}
                                                ),
                                                html.H2(
                                                    id="total-revenue",
                                                    children="R$ 0,00",
                                                    style={"margin": "0", "color": "#1f77b4"},
                                                ),
                                            ],
                                            className="metric-card",
                                            style={
                                                "padding": "20px",
                                                "backgroundColor": "#f8f9fa",
                                                "borderRadius": "8px",
                                                "border": "1px solid #ddd",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                html.H3(
                                                    "Total de Pedidos",
                                                    style={"margin": "0 0 10px 0"},
                                                ),
                                                html.H2(
                                                    id="total-orders",
                                                    children="0",
                                                    style={"margin": "0", "color": "#1f77b4"},
                                                ),
                                            ],
                                            className="metric-card",
                                            style={
                                                "padding": "20px",
                                                "backgroundColor": "#f8f9fa",
                                                "borderRadius": "8px",
                                                "border": "1px solid #ddd",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                html.H3(
                                                    "Ticket Médio", style={"margin": "0 0 10px 0"}
                                                ),
                                                html.H2(
                                                    id="avg-order-value",
                                                    children="R$ 0,00",
                                                    style={"margin": "0", "color": "#1f77b4"},
                                                ),
                                            ],
                                            className="metric-card",
                                            style={
                                                "padding": "20px",
                                                "backgroundColor": "#f8f9fa",
                                                "borderRadius": "8px",
                                                "border": "1px solid #ddd",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                html.H3(
                                                    "Total de Clientes",
                                                    style={"margin": "0 0 10px 0"},
                                                ),
                                                html.H2(
                                                    id="total-customers",
                                                    children="0",
                                                    style={"margin": "0", "color": "#1f77b4"},
                                                ),
                                            ],
                                            className="metric-card",
                                            style={
                                                "padding": "20px",
                                                "backgroundColor": "#f8f9fa",
                                                "borderRadius": "8px",
                                                "border": "1px solid #ddd",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "grid",
                                        "gridTemplateColumns": "repeat(4, 1fr)",
                                        "gap": "20px",
                                        "marginBottom": "30px",
                                    },
                                ),
                                # Gráficos
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Graph(id="revenue-trend-graph"),
                                            ],
                                            style={"flex": "1"},
                                        ),
                                        html.Div(
                                            [
                                                dcc.Graph(id="orders-trend-graph"),
                                            ],
                                            style={"flex": "1"},
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "gap": "20px",
                                        "marginBottom": "20px",
                                    },
                                ),
                            ],
                            style={"padding": "20px"},
                        )
                    ],
                ),
                # ========== TAB 2: TOP PRODUCTS ==========
                dcc.Tab(
                    label="🏆 Top Produtos",
                    value="tab-2",
                    children=[
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Label("Quantidade:", style={"fontWeight": "bold"}),
                                        dcc.Slider(
                                            id="top-products-limit",
                                            min=5,
                                            max=20,
                                            step=5,
                                            value=10,
                                            marks={i: str(i) for i in range(5, 21, 5)},
                                        ),
                                    ],
                                    style={"marginBottom": "20px"},
                                ),
                                dcc.Graph(id="top-products-graph"),
                            ],
                            style={"padding": "20px"},
                        )
                    ],
                ),
                # ========== TAB 3: SALES BY CATEGORY ==========
                dcc.Tab(
                    label="📊 Vendas por Categoria",
                    value="tab-3",
                    children=[
                        html.Div(
                            [
                                dcc.Graph(id="sales-by-category-graph"),
                            ],
                            style={"padding": "20px"},
                        )
                    ],
                ),
                # ========== TAB 4: FORECASTING ==========
                dcc.Tab(
                    label="🔮 Previsões",
                    value="tab-4",
                    children=[
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Label("Meses à frente:", style={"fontWeight": "bold"}),
                                        dcc.Slider(
                                            id="forecast-months",
                                            min=1,
                                            max=12,
                                            step=1,
                                            value=3,
                                            marks={i: str(i) for i in range(1, 13)},
                                        ),
                                    ],
                                    style={"marginBottom": "20px"},
                                ),
                                dcc.Graph(id="forecast-graph"),
                            ],
                            style={"padding": "20px"},
                        )
                    ],
                ),
                # ========== TAB 5: RECOMMENDATIONS ==========
                dcc.Tab(
                    label="💡 Recomendações",
                    value="tab-5",
                    children=[
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Label("ID do Cliente:", style={"fontWeight": "bold"}),
                                        dcc.Input(
                                            id="customer-id-input",
                                            type="text",
                                            placeholder="C001",
                                            value="C001",
                                            style={
                                                "padding": "8px",
                                                "marginRight": "10px",
                                                "width": "150px",
                                            },
                                        ),
                                        html.Label(
                                            "Top N:",
                                            style={"fontWeight": "bold", "marginLeft": "20px"},
                                        ),
                                        dcc.Slider(
                                            id="recommendations-limit",
                                            min=3,
                                            max=10,
                                            step=1,
                                            value=5,
                                            marks={i: str(i) for i in range(3, 11)},
                                        ),
                                    ],
                                    style={"marginBottom": "20px"},
                                ),
                                dcc.Graph(id="recommendations-graph"),
                            ],
                            style={"padding": "20px"},
                        )
                    ],
                ),
            ],
        ),
        # ========== STORES ==========
        dcc.Store(id="auth-token-store"),
        dcc.Store(id="dashboard-data-store"),
        # ========== INTERVAL PARA ATUALIZAR DADOS ==========
        dcc.Interval(id="interval-component", interval=300000, n_intervals=0),  # 5 minutos
    ],
    style={"fontFamily": "Arial, sans-serif", "backgroundColor": "#fff"},
)

# ========== CALLBACKS ==========


@callback(
    [Output("auth-token-store", "data"), Output("login-status", "children")],
    Input("login-button", "n_clicks"),
    [State("username-input", "value"), State("password-input", "value")],
    prevent_initial_call=True,
)
def login(n_clicks, username, password):
    """Fazer login e obter token JWT."""
    if not username or not password:
        return None, "❌ Username e password são obrigatórios"

    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"username": username, "password": password},
            timeout=30,
        )

        if response.status_code == 200:
            token = response.json().get("access_token")
            logger.info(f"✅ Login bem-sucedido para {username}")
            return token, f"✅ Logado como {username}"
        else:
            logger.error(f"❌ Login falhou: {response.status_code}")
            return None, "❌ Login falhou. Verifique credenciais."
    except Exception as e:
        logger.error(f"❌ Erro ao fazer login: {e}")
        return None, f"❌ Erro: {str(e)}"


@callback(
    Output("dashboard-data-store", "data"),
    [Input("interval-component", "n_intervals"), Input("auth-token-store", "data")],
)
def fetch_dashboard_data(n_intervals, token):
    """Buscar dados do dashboard da API."""
    if not token:
        raise PreventUpdate

    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_BASE_URL}/api/v1/analytics/dashboard", headers=headers, timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            logger.info("✅ Dados do dashboard obtidos com sucesso")
            return data
        else:
            logger.error(f"❌ Erro ao buscar dados: {response.status_code}")
            return {}
    except Exception as e:
        logger.error(f"❌ Erro ao buscar dados: {e}")
        return {}


@callback(
    [
        Output("total-revenue", "children"),
        Output("total-orders", "children"),
        Output("avg-order-value", "children"),
        Output("total-customers", "children"),
        Output("revenue-trend-graph", "figure"),
        Output("orders-trend-graph", "figure"),
    ],
    Input("dashboard-data-store", "data"),
)
def update_overview(data):
    """Atualizar overview com dados do dashboard."""
    if not data:
        empty_fig = go.Figure()
        return "R$ 0,00", "0", "R$ 0,00", "0", empty_fig, empty_fig

    # Extrair dados
    total_revenue = data.get("total_revenue", 0)
    total_orders = data.get("total_orders", 0)
    avg_order_value = data.get("avg_order_value", 0)
    total_customers = data.get("total_customers", 0)

    # Formatar valores
    revenue_text = f"R$ {total_revenue:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    orders_text = f"{total_orders:,}".replace(",", ".")
    avg_text = f"R$ {avg_order_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    customers_text = f"{total_customers:,}".replace(",", ".")

    # Gráfico de tendência de receita
    revenue_fig = go.Figure()
    revenue_fig.add_trace(
        go.Scatter(
            x=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            y=data.get("revenue_trend", [1000, 1500, 1200, 1800, 2000, 2200]),
            mode="lines+markers",
            name="Revenue",
            line={"color": "#1f77b4", "width": 3},
            marker={"size": 8},
        )
    )
    revenue_fig.update_layout(
        title="Evolução da Receita",
        xaxis_title="Mês",
        yaxis_title="Receita (R$)",
        hovermode="x unified",
        template="plotly_white",
    )

    # Gráfico de tendência de pedidos
    orders_fig = go.Figure()
    orders_fig.add_trace(
        go.Scatter(
            x=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            y=data.get("orders_trend", [50, 75, 60, 90, 100, 110]),
            mode="lines+markers",
            name="Orders",
            line={"color": "#ff7f0e", "width": 3},
            marker={"size": 8},
        )
    )
    orders_fig.update_layout(
        title="Evolução de Pedidos",
        xaxis_title="Mês",
        yaxis_title="Quantidade de Pedidos",
        hovermode="x unified",
        template="plotly_white",
    )

    return revenue_text, orders_text, avg_text, customers_text, revenue_fig, orders_fig


@callback(
    Output("top-products-graph", "figure"),
    [Input("dashboard-data-store", "data"), Input("top-products-limit", "value")],
)
def update_top_products(data, limit):
    """Atualizar gráfico de top produtos."""
    if not data or "top_products" not in data:
        return go.Figure()

    products = data.get("top_products", [])[:limit]

    if not products:
        return go.Figure()

    product_names = [p.get("name", "Unknown") for p in products]
    product_sales = [p.get("sales", 0) for p in products]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=product_names, y=product_sales, name="Vendas", marker={"color": "#1f77b4"})
    )
    fig.update_layout(
        title=f"Top {limit} Produtos",
        xaxis_title="Produto",
        yaxis_title="Vendas",
        hovermode="x unified",
        template="plotly_white",
    )
    return fig


@callback(
    Output("sales-by-category-graph", "figure"),
    Input("dashboard-data-store", "data"),
)
def update_sales_by_category(data):
    """Atualizar gráfico de vendas por categoria."""
    if not data or "sales_by_category" not in data:
        return go.Figure()

    categories = data.get("sales_by_category", [])

    if not categories:
        return go.Figure()

    category_names = [c.get("category", "Unknown") for c in categories]
    category_sales = [c.get("sales", 0) for c in categories]

    fig = go.Figure()
    fig.add_trace(go.Pie(labels=category_names, values=category_sales, name="Vendas"))
    fig.update_layout(title="Vendas por Categoria", template="plotly_white")
    return fig


@callback(
    Output("forecast-graph", "figure"),
    [
        Input("dashboard-data-store", "data"),
        Input("forecast-months", "value"),
        Input("auth-token-store", "data"),
    ],
)
def update_forecast(data, months, token):
    """Atualizar gráfico de forecasting."""
    if not token:
        return go.Figure()

    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{API_BASE_URL}/api/v1/forecast/revenue",
            json={"months_ahead": months},
            headers=headers,
            timeout=30,
        )

        if response.status_code == 200:
            forecast_data = response.json()
            forecast_values = forecast_data.get("forecast", [])
            x_vals = [f.get("month", f"M{i}") for i, f in enumerate(forecast_values)]
            y_vals = [f.get("predicted_revenue", 0) for f in forecast_values]

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=y_vals,
                    mode="lines+markers",
                    name="Forecast",
                    line={"color": "#2ca02c", "width": 3},
                    marker={"size": 8},
                )
            )
            fig.update_layout(
                title=f"Previsão de Receita - {months} Meses",
                xaxis_title="Mês",
                yaxis_title="Receita (R$)",
                hovermode="x unified",
                template="plotly_white",
            )
            return fig
    except Exception as e:
        logger.error(f"❌ Erro ao buscar forecast: {e}")

    return go.Figure()


@callback(
    Output("recommendations-graph", "figure"),
    [
        Input("customer-id-input", "value"),
        Input("recommendations-limit", "value"),
        Input("auth-token-store", "data"),
    ],
)
def update_recommendations(customer_id, top_n, token):
    """Atualizar gráfico de recomendações."""
    if not token or not customer_id:
        return go.Figure()

    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{API_BASE_URL}/api/v1/recommendations/products",
            json={"customer_id": customer_id, "top_n": top_n},
            headers=headers,
            timeout=30,
        )

        if response.status_code == 200:
            recs_data = response.json()
            recommendations = recs_data.get("recommendations", [])

            if not recommendations:
                return go.Figure()

            product_names = [r.get("name", "Unknown") for r in recommendations]
            scores = [r.get("score", 0) for r in recommendations]

            fig = go.Figure()
            fig.add_trace(
                go.Bar(x=product_names, y=scores, name="Relevância", marker={"color": "#1f77b4"})
            )
            fig.update_layout(
                title=f"Recomendações para {customer_id}",
                xaxis_title="Produto",
                yaxis_title="Relevância",
                hovermode="x unified",
                template="plotly_white",
            )
            return fig
    except Exception as e:
        logger.error(f"❌ Erro ao buscar recomendações: {e}")

    return go.Figure()


# ========== ENTRY POINT ==========
if __name__ == "__main__":
    logger.info(f"🚀 Dashboard rodando em http://{DASH_HOST}:{DASH_PORT}")

    app.run(host=DASH_HOST, port=DASH_PORT, debug=True)
