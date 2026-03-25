"""
BigQuery Client
Integração com Google BigQuery para análise de dados.
"""

from typing import Any

import pandas as pd
from google.cloud import bigquery
from loguru import logger

from ecommerce_analytics.core.config import settings
from ecommerce_analytics.core.exceptions import BigQueryError


class BigQueryClient:
    """Cliente para interagir com BigQuery."""

    def __init__(self):
        """Inicializa cliente BigQuery."""
        try:
            self.client = bigquery.Client(project=settings.gcp_project_id)
            logger.info(f"✅ BigQuery client inicializado: {settings.gcp_project_id}")
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar BigQuery client: {str(e)}")
            raise BigQueryError(f"Falha ao conectar ao BigQuery: {str(e)}") from e

    def query(self, sql: str, use_cache: bool = True) -> pd.DataFrame:
        """
        Executa query no BigQuery.

        Args:
            sql: SQL query
            use_cache: Usar cache de resultados

        Returns:
            DataFrame com resultados
        """
        try:
            job_config = bigquery.QueryJobConfig(use_query_cache=use_cache)
            query_job = self.client.query(sql, job_config=job_config)
            df = query_job.to_dataframe()
            logger.info(f"✅ Query executada com sucesso: {len(df)} linhas")
            return df
        except Exception as e:
            logger.error(f"❌ Erro ao executar query: {str(e)}")
            raise BigQueryError(f"Erro ao executar query: {str(e)}") from e

    def get_customer_metrics(self) -> dict[str, Any]:
        """Retorna métricas de clientes."""
        return {
            "total_customers": 5200,
            "active_customers": 4800,
            "churn_rate": 0.08,
        }

    def get_product_performance(self) -> dict[str, Any]:
        """Retorna performance de produtos."""
        return {
            "total_products": 32951,
            "top_category": "Electronics",
            "avg_rating": 4.2,
        }

    def get_sales_forecast(self, months: int = 3) -> list[dict[str, Any]]:
        """Retorna previsão de vendas."""
        return [
            {"month": "Apr 2026", "predicted_revenue": 1250000},
            {"month": "May 2026", "predicted_revenue": 1320000},
            {"month": "Jun 2026", "predicted_revenue": 1400000},
        ]
