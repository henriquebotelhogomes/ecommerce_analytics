"""
Cliente BigQuery para integração com a API
"""


import logging
from typing import Any

import pandas as pd
from google.cloud import bigquery

from ecommerce_analytics.core.config import settings
from ecommerce_analytics.core.exceptions import BigQueryError

logger = logging.getLogger(__name__)


class BigQueryClient:
    """Cliente para operações no BigQuery"""

    def __init__(self, project_id: str | None = None) -> None:
        """Inicializa o cliente BigQuery"""
        self.project_id = project_id or settings.gcp_project_id
        self.dataset_id = settings.gcp_dataset_id

        try:
            self.client = bigquery.Client(project=self.project_id)
            logger.info(f"✅ BigQuery client inicializado para projeto: {self.project_id}")
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar BigQuery client: {str(e)}")
            raise BigQueryError(f"Falha ao conectar ao BigQuery: {str(e)}")

    def query(self, sql: str, use_cache: bool = True) -> pd.DataFrame:
        """
        Executa uma query SQL e retorna DataFrame

        Args:
            sql: Query SQL
            use_cache: Usar cache de resultados

        Returns:
            DataFrame com resultados
        """
        try:
            job_config = bigquery.QueryJobConfig(use_query_cache=use_cache)
            query_job = self.client.query(sql, job_config=job_config)
            df = query_job.to_dataframe()

            logger.info(f"✅ Query executada com sucesso. Linhas: {len(df)}")
            return df
        except Exception as e:
            logger.error(f"❌ Erro ao executar query: {str(e)}")
            raise BigQueryError(f"Erro ao executar query: {str(e)}")

    def get_customer_metrics(self) -> dict[str, Any]:
        """
        Retorna métricas agregadas de clientes

        Calcula:
        - Total de clientes únicos
        - Total de pedidos
        - Ticket médio (price + freight_value)
        - Maior valor de pedido
        - Receita total
        """
        sql = f"""
        SELECT
          COUNT(DISTINCT o.customer_id) as total_customers,
          COUNT(DISTINCT o.order_id) as total_orders,
          ROUND(AVG(order_value), 2) as avg_order_value,
          ROUND(MAX(order_value), 2) as max_order_value,
          ROUND(SUM(order_value), 2) as total_revenue
        FROM (
          SELECT
            o.customer_id,
            o.order_id,
            SUM(oi.price + oi.freight_value) as order_value
          FROM {self.project_id}.{self.dataset_id}.orders o
          LEFT JOIN {self.project_id}.{self.dataset_id}.order_items oi
            ON o.order_id = oi.order_id
          GROUP BY o.customer_id, o.order_id
        ) o
        """
        df = self.query(sql)
        return df.iloc[0].to_dict() if len(df) > 0 else {}

    def get_sales_by_category(self) -> pd.DataFrame:
        """
        Retorna vendas por categoria de produto

        Agrupa por categoria e calcula:
        - Total de itens vendidos
        - Receita total (price + freight_value)
        - Preço médio
        """
        sql = f"""
        SELECT
          p.product_category_name as category,
          COUNT(oi.order_item_id) as total_orders,
          ROUND(SUM(oi.price + oi.freight_value), 2) as revenue,
          ROUND(AVG(oi.price), 2) as avg_price
        FROM {self.project_id}.{self.dataset_id}.order_items oi
        LEFT JOIN {self.project_id}.{self.dataset_id}.products p
          ON oi.product_id = p.product_id
        WHERE p.product_category_name IS NOT NULL
        GROUP BY p.product_category_name
        ORDER BY revenue DESC
        """
        return self.query(sql)

    def get_top_products(self, limit: int = 10) -> pd.DataFrame:
        """
        Retorna produtos mais vendidos

        Agrupa por produto e calcula:
        - Total de vendas (quantidade de order_items)
        - Receita total (price + freight_value)
        """
        sql = f"""
        SELECT
          p.product_id,
          p.product_category_name as category,
          COUNT(oi.order_item_id) as total_sales,
          ROUND(SUM(oi.price + oi.freight_value), 2) as revenue
        FROM {self.project_id}.{self.dataset_id}.order_items oi
        LEFT JOIN {self.project_id}.{self.dataset_id}.products p
          ON oi.product_id = p.product_id
        WHERE p.product_category_name IS NOT NULL
        GROUP BY p.product_id, p.product_category_name
        ORDER BY revenue DESC
        LIMIT {limit}
        """
        return self.query(sql)
