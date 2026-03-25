"""
Plotly Dash Application for E-commerce Analytics.
Professional, production-ready dashboard with advanced interactivity.
"""

import os

import dash_bootstrap_components as dbc  # type: ignore[import-untyped]
import requests
from dash import Dash, Input, Output, dcc, html
from loguru import logger

# ========== CONFIGURAÇÃO ==========
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
DASH_PORT = int(os.getenv("DASH_PORT", 8050))

logger.info(f"🔗 Conectando à API: {API_BASE_URL}")

# ========== INICIALIZAR DASH APP ==========
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css",
    ],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.title = "AI E-commerce Analytics"

# ========== CUSTOM CSS ==========
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            :root {
                --primary-color: #FF6B6B;
                --secondary-color: #4ECDC4;
                --dark-bg: #1a1a1a;
                --light-bg: #f8f9fa;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: var(--light-bg);
            }

            .navbar {
                background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }

            .card {
                border: none;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                transition: transform 0.2s, box-shadow 0.2s;
            }

            .card:hover {
                transform: translateY(-4px);
                box-shadow: 0 4px 16px rgba(0,0,0,0.12);
            }

            .metric-card {
                background: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
            }

            .metric-value {
                font-size: 2.5rem;
                font-weight: bold;
                color: var(--primary-color);
            }

            .metric-label {
                font-size: 0.9rem;
                color: #666;
                margin-top: 8px;
            }

            .btn-primary {
                background-color: var(--primary-color);
                border: none;
            }

            .btn-primary:hover {
                background-color: #ff5252;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

# ========== LAYOUT ==========
app.layout = dbc.Container(
    [
        # Header
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H1("📊 E-commerce Analytics Dashboard", className="mb-0"),
                                html.P(
                                    "AI-powered insights powered by BigQuery",
                                    className="text-muted mb-0",
                                ),
                            ],
                            className="py-4",
                        )
                    ]
                )
            ],
            className="bg-light border-bottom mb-4",
        ),
        # Navigation Tabs
        dcc.Tabs(
            id="tabs",
            value="tab-1",
            children=[
                # ========== TAB 1: OVERVIEW ==========
                dcc.Tab(
                    label="📈 Overview",
                    value="tab-1",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H4(
                                                            "Total Sales",
                                                            className="card-title",
                                                        ),
                                                        html.H2(
                                                            "R$ 1.2M",
                                                            className="metric-value",
                                                        ),
                                                        html.P(
                                                            "+12% vs last month",
                                                            className="text-success",
                                                        ),
                                                    ]
                                                )
                                            ],
                                            className="metric-card",
                                        )
                                    ],
                                    md=3,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H4(
                                                            "Active Customers",
                                                            className="card-title",
                                                        ),
                                                        html.H2(
                                                            "5.2K",
                                                            className="metric-value",
                                                        ),
                                                        html.P(
                                                            "+8% vs last month",
                                                            className="text-success",
                                                        ),
                                                    ]
                                                )
                                            ],
                                            className="metric-card",
                                        )
                                    ],
                                    md=3,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H4(
                                                            "Conversion Rate",
                                                            className="card-title",
                                                        ),
                                                        html.H2(
                                                            "3.2%",
                                                            className="metric-value",
                                                        ),
                                                        html.P(
                                                            "-0.5% vs last month",
                                                            className="text-danger",
                                                        ),
                                                    ]
                                                )
                                            ],
                                            className="metric-card",
                                        )
                                    ],
                                    md=3,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        html.H4(
                                                            "Avg Order Value",
                                                            className="card-title",
                                                        ),
                                                        html.H2(
                                                            "R$ 245",
                                                            className="metric-value",
                                                        ),
                                                        html.P(
                                                            "+5% vs last month",
                                                            className="text-success",
                                                        ),
                                                    ]
                                                )
                                            ],
                                            className="metric-card",
                                        )
                                    ],
                                    md=3,
                                ),
                            ],
                            className="mb-4",
                        ),
                        # Charts
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Sales Trend"),
                                                dbc.CardBody([dcc.Graph(id="sales-trend-chart")]),
                                            ]
                                        )
                                    ],
                                    md=6,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Top Products"),
                                                dbc.CardBody([dcc.Graph(id="top-products-chart")]),
                                            ]
                                        )
                                    ],
                                    md=6,
                                ),
                            ],
                            className="mb-4",
                        ),
                    ],
                ),
                # ========== TAB 2: ANALYTICS ==========
                dcc.Tab(
                    label="🔍 Analytics",
                    value="tab-2",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Customer Segmentation"),
                                                dbc.CardBody([dcc.Graph(id="segmentation-chart")]),
                                            ]
                                        )
                                    ],
                                    md=6,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Product Performance"),
                                                dbc.CardBody([dcc.Graph(id="performance-chart")]),
                                            ]
                                        )
                                    ],
                                    md=6,
                                ),
                            ],
                            className="mb-4",
                        ),
                    ],
                ),
                # ========== TAB 3: FORECASTING ==========
                dcc.Tab(
                    label="🔮 Forecasting",
                    value="tab-3",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Sales Forecast"),
                                                dbc.CardBody([dcc.Graph(id="forecast-chart")]),
                                            ]
                                        )
                                    ],
                                    md=12,
                                ),
                            ],
                            className="mb-4",
                        ),
                    ],
                ),
                # ========== TAB 4: SETTINGS ==========
                dcc.Tab(
                    label="⚙️ Settings",
                    value="tab-4",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("API Status"),
                                                dbc.CardBody([html.Div(id="api-status")]),
                                            ]
                                        )
                                    ],
                                    md=6,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Documentation"),
                                                dbc.CardBody(
                                                    [
                                                        html.A(
                                                            "📚 API Docs",
                                                            href=f"{API_BASE_URL}/docs",
                                                            target="_blank",
                                                            className="btn btn-primary",
                                                        )
                                                    ]
                                                ),
                                            ]
                                        )
                                    ],
                                    md=6,
                                ),
                            ],
                            className="mb-4",
                        ),
                    ],
                ),
            ],
        ),
    ],
    fluid=True,
    className="py-4",
)


# ========== CALLBACKS ==========
@app.callback(Output("api-status", "children"), Input("tabs", "value"))
def update_api_status(tab):
    """Verifica status da API."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return dbc.Alert("✅ API Online", color="success", className="mb-0")
    except Exception as e:
        return dbc.Alert(f"❌ API Offline: {str(e)}", color="danger", className="mb-0")


@app.callback(Output("sales-trend-chart", "figure"), Input("tabs", "value"))
def update_sales_trend(tab):
    """Atualiza gráfico de tendência de vendas."""
    import plotly.graph_objects as go

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            y=[1000, 1200, 1400, 1300, 1500, 1600],
            mode="lines+markers",
            name="Sales",
            line={"color": "#FF6B6B", "width": 3},
            marker={"size": 8},
        )
    )

    fig.update_layout(
        title="Sales Trend",
        xaxis_title="Month",
        yaxis_title="Sales (R$)",
        hovermode="x unified",
        template="plotly_white",
    )

    return fig


@app.callback(Output("top-products-chart", "figure"), Input("tabs", "value"))
def update_top_products(tab):
    """Atualiza gráfico de top produtos."""
    import plotly.graph_objects as go

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=["Product A", "Product B", "Product C", "Product D"],
            y=[450, 380, 320, 280],
            marker={"color": "#4ECDC4"},
        )
    )

    fig.update_layout(
        title="Top Products",
        xaxis_title="Product",
        yaxis_title="Sales (R$)",
        template="plotly_white",
    )

    return fig


# ========== EXECUTAR ==========
if __name__ == "__main__":
    app.run_server(
        host="0.0.0.0",
        port=DASH_PORT,
        debug=os.getenv("DASH_DEBUG", "False") == "True",
    )
