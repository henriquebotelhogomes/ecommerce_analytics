"""
Dashboard Plotly Dash para visualização de métricas de e-commerce.

Este módulo configura e executa um dashboard interativo usando Plotly Dash,
integrando-se com a API FastAPI para buscar dados analíticos do BigQuery.
"""

import logging
from typing import Any

import dash  # type: ignore[import-untyped]
import dash_bootstrap_components as dbc  # type: ignore[import-untyped]
import pandas as pd
import plotly.express as px  # type: ignore[import-untyped]
import plotly.graph_objects as go  # type: ignore[import-untyped]
import requests
from dash import Input, Output, callback, dcc, html

logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURAR DASH
# ============================================================================

# Inicializa a aplicação Dash com temas Bootstrap para um visual moderno
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ============================================================================
# FUNÇÕES AUXILIARES PARA INTERAÇÃO COM A API
# ============================================================================


def get_token() -> str:
    """
    Obtém um token JWT da API FastAPI para autenticação.
    Retorna o token como string ou uma string vazia em caso de falha.
    """
    try:
        response = requests.post(
            "http://localhost:8000/login", json={"username": "admin", "password": "admin123"}
        )
        if response.status_code == 200:
            token: str = response.json()["access_token"]  # Type cast explícito
            return token
        else:
            logger.error(f"❌ Erro ao fazer login: {response.status_code} - {response.text}")
            return ""
    except requests.exceptions.ConnectionError:
        logger.error("❌ Erro de conexão: API FastAPI não está rodando ou acessível.")
        return ""
    except Exception as e:
        logger.error(f"❌ Erro inesperado ao obter token: {str(e)}")
        return ""


def fetch_dashboard_metrics() -> dict[str, Any]:
    """
    Busca as métricas principais do dashboard na API FastAPI.
    Retorna um dicionário com as métricas ou um dicionário vazio em caso de falha.
    """
    token = get_token()
    if not token:
        return {}

    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get("http://localhost:8000/api/v1/analytics/dashboard", headers=headers)
        if response.status_code == 200:
            metrics: dict[str, Any] = response.json()  # Type cast explícito
            return metrics
        else:
            logger.error(f"❌ Erro ao buscar métricas: {response.status_code} - {response.text}")
            return {}
    except requests.exceptions.ConnectionError:
        logger.error(
            "❌ Erro de conexão ao buscar métricas: " "API FastAPI não está rodando ou acessível."
        )
        return {}
    except Exception as e:
        logger.error(f"❌ Erro inesperado ao buscar métricas: {str(e)}")
        return {}


def fetch_top_products() -> list[dict[str, Any]]:
    """
    Busca a lista dos produtos mais vendidos na API FastAPI.
    Retorna uma lista de dicionários com os produtos ou uma lista vazia em caso de falha.
    """
    token = get_token()
    if not token:
        return []

    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            "http://localhost:8000/api/v1/analytics/top-products?limit=10", headers=headers
        )
        if response.status_code == 200:
            products: list[dict[str, Any]] = response.json()  # Type cast explícito
            return products
        else:
            logger.error(f"❌ Erro ao buscar produtos: {response.status_code} - {response.text}")
            return []
    except requests.exceptions.ConnectionError:
        logger.error(
            "❌ Erro de conexão ao buscar top produtos: "
            "API FastAPI não está rodando ou acessível."
        )
        return []
    except Exception as e:
        logger.error(f"❌ Erro inesperado ao buscar top produtos: {str(e)}")
        return []


def fetch_sales_by_category() -> list[dict[str, Any]]:
    """
    Busca os dados de vendas por categoria na API FastAPI.
    Retorna uma lista de dicionários com as vendas por
    categoria ou uma lista vazia em caso de falha.
    """
    token = get_token()
    if not token:
        return []

    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            "http://localhost:8000/api/v1/analytics/sales-by-category", headers=headers
        )
        if response.status_code == 200:
            categories: list[dict[str, Any]] = response.json()  # Type cast explícito
            return categories
        else:
            logger.error(f"❌ Erro ao buscar categorias: {response.status_code} - {response.text}")
            return []
    except requests.exceptions.ConnectionError:
        logger.error(
            "❌ Erro de conexão ao buscar vendas por categoria: "
            "API FastAPI não está rodando ou acessível."
        )
        return []
    except Exception as e:
        logger.error(f"❌ Erro inesperado ao buscar vendas por categoria: {str(e)}")
        return []


# ============================================================================
# LAYOUT DO DASHBOARD
# ============================================================================

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [html.H1("📊 E-commerce Analytics Dashboard", className="mb-4 mt-4 text-center")]
                )
            ]
        ),
        # Seção de KPIs (Key Performance Indicators)
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4(
                                            "Total Clientes", className="card-title text-center"
                                        ),
                                        html.H2(
                                            id="total-customers",
                                            children="0",
                                            className="text-center",
                                        ),
                                    ]
                                )
                            ],
                            className="shadow-sm",
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
                                            "Total Pedidos", className="card-title text-center"
                                        ),
                                        html.H2(
                                            id="total-orders", children="0", className="text-center"
                                        ),
                                    ]
                                )
                            ],
                            className="shadow-sm",
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
                                        html.H4("Ticket Médio", className="card-title text-center"),
                                        html.H2(
                                            id="avg-order-value",
                                            children="R$ 0",
                                            className="text-center",
                                        ),
                                    ]
                                )
                            ],
                            className="shadow-sm",
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
                                            "Receita Total", className="card-title text-center"
                                        ),
                                        html.H2(
                                            id="total-revenue",
                                            children="R$ 0",
                                            className="text-center",
                                        ),
                                    ]
                                )
                            ],
                            className="shadow-sm",
                        )
                    ],
                    md=3,
                ),
            ],
            className="mb-4",
        ),
        # Seção de Gráficos
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4(
                                            "Top 10 Produtos por Receita",
                                            className="card-title text-center",
                                        ),
                                        dcc.Graph(
                                            id="top-products-chart",
                                            config={"displayModeBar": False},
                                        ),
                                    ]
                                )
                            ],
                            className="shadow-sm h-100",
                        )
                    ],
                    md=6,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4(
                                            "Distribuição de Receita por Categoria",
                                            className="card-title text-center",
                                        ),
                                        dcc.Graph(
                                            id="sales-by-category-chart",
                                            config={"displayModeBar": False},
                                        ),
                                    ]
                                )
                            ],
                            className="shadow-sm h-100",
                        )
                    ],
                    md=6,
                ),
            ],
            className="mb-4",
        ),
        # Componente de intervalo para atualizar os dados periodicamente
        dcc.Interval(
            id="interval-component",
            interval=30 * 1000,  # Atualiza a cada 30 segundos
            n_intervals=0,
        ),
    ],
    fluid=True,
    className="p-3",
)

# ============================================================================
# CALLBACKS DO DASHBOARD
# ============================================================================


@callback(  # type: ignore[misc]
    [
        Output("total-customers", "children"),
        Output("total-orders", "children"),
        Output("avg-order-value", "children"),
        Output("total-revenue", "children"),
    ],
    Input("interval-component", "n_intervals"),
)
def update_kpis(n: int) -> Any:  # ✅ CORRIGIDO: return type Any para decorator
    """
    Callback para atualizar os KPIs do dashboard.
    Acionado pelo componente dcc.Interval.
    """
    logger.info(f"Atualizando KPIs (intervalo: {n})")
    metrics = fetch_dashboard_metrics()

    if not metrics:
        logger.warning("Não foi possível obter métricas para atualizar KPIs.")
        return "Erro", "Erro", "R$ Erro", "R$ Erro"

    # Formata os números para exibição
    total_customers = f"{metrics.get('total_customers', 0):,}".replace(",", ".")

    total_orders = f"{metrics.get('total_orders', 0):,}".replace(",", ".")

    avg_order_value = (
        f"R$ {metrics.get('avg_order_value', 0):,.2f}".replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    total_revenue = (
        f"R$ {metrics.get('total_revenue', 0):,.2f}".replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    return (total_customers, total_orders, avg_order_value, total_revenue)


@callback(  # type: ignore[misc]
    Output("top-products-chart", "figure"), Input("interval-component", "n_intervals")
)
def update_top_products_chart(n: int) -> Any:  # ✅ CORRIGIDO: return type Any para decorator
    """
    Callback para atualizar o gráfico de produtos mais vendidos.
    Acionado pelo componente dcc.Interval.
    """
    logger.info(f"Atualizando gráfico de top produtos (intervalo: {n})")
    products = fetch_top_products()

    if not products:
        logger.warning("Não foi possível obter dados de top produtos para o gráfico.")
        return go.Figure().add_annotation(
            text="Sem dados para exibir", showarrow=False, x=0.5, y=0.5
        )

    df_products = pd.DataFrame(products)

    fig = px.bar(
        df_products,
        x="product_id",
        y="revenue",
        title="Top 10 Produtos por Receita",
        labels={"product_id": "Produto", "revenue": "Receita (R$)"},
        color_discrete_sequence=px.colors.qualitative.Pastel,
        template="plotly_white",
    )
    fig.update_layout(xaxis_title="Produto", yaxis_title="Receita (R$)")

    return fig


@callback(  # type: ignore[misc]
    Output("sales-by-category-chart", "figure"), Input("interval-component", "n_intervals")
)
def update_sales_by_category_chart(n: int) -> Any:  # ✅ CORRIGIDO: return type Any para decorator
    """
    Callback para atualizar o gráfico de vendas por categoria.
    Acionado pelo componente dcc.Interval.
    """
    logger.info(f"Atualizando gráfico de vendas por categoria (intervalo: {n})")
    categories = fetch_sales_by_category()

    if not categories:
        logger.warning("Não foi possível obter dados de vendas por categoria para o gráfico.")
        return go.Figure().add_annotation(
            text="Sem dados para exibir", showarrow=False, x=0.5, y=0.5
        )

    df_categories = pd.DataFrame(categories)

    fig = px.pie(
        df_categories,
        names="category",
        values="revenue",
        title="Distribuição de Receita por Categoria",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        template="plotly_white",
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")

    return fig


# ============================================================================
# EXECUTAR APLICAÇÃO DASH
# ============================================================================

if __name__ == "__main__":
    # Executa o servidor Dash. debug=True permite hot-reloading e depuração.
    # Host e porta configurados para acesso local.
    app.run_server(debug=True, host="127.0.0.1", port=8050)
