from typing import Any, Dict

import pandas as pd
from loguru import logger

from ecommerce_analytics.bigquery.client import BigQueryClient
from ecommerce_analytics.core.config import settings


class AnalyticsService:
    def __init__(self):
        self.bq_client = BigQueryClient()
        self.project = settings.gcp_project_id
        self.dataset = settings.gcp_dataset_id

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Busca dados reais do dashboard estruturados a partir do BigQuery."""
        logger.info("Executando query para dados do dashboard...")

        # 1. Obter resumos e tendências dos últimos 30 dias (ou total)
        trends_sql = f"""
        SELECT
            SUM(total_revenue) as total_revenue,
            SUM(total_orders) as total_orders,
            SUM(unique_customers) as total_customers,
            SUM(total_revenue) / NULLIF(SUM(total_orders), 0) as avg_order_value,
            ARRAY_AGG(STRUCT(sale_date, total_revenue, total_orders) ORDER BY sale_date) as daily_trends
        FROM `{self.project}.{self.dataset}.daily_sales`
        """
        trends_df = self.bq_client.query(trends_sql)

        # 2. Obter Top Produtos (Por ID)
        top_products_sql = f"""
        SELECT
            p.product_id as name,
            SUM(oi.price) as sales
        FROM `{self.project}.{self.dataset}.order_items` oi
        JOIN `{self.project}.{self.dataset}.products` p ON oi.product_id = p.product_id
        GROUP BY 1
        ORDER BY sales DESC
        LIMIT 20
        """
        top_products_df = self.bq_client.query(top_products_sql)

        # 3. Obter Vendas por Categoria
        sales_by_category_sql = f"""
        SELECT
            p.product_category_name as category,
            SUM(oi.price) as sales
        FROM `{self.project}.{self.dataset}.order_items` oi
        JOIN `{self.project}.{self.dataset}.products` p ON oi.product_id = p.product_id
        WHERE p.product_category_name IS NOT NULL
        GROUP BY 1
        ORDER BY sales DESC
        LIMIT 20
        """
        categories_df = self.bq_client.query(sales_by_category_sql)

        # Tratar resultados
        if trends_df.empty:
            return {}

        row = trends_df.iloc[0]
        daily_trends = row.get("daily_trends", [])

        # Últimos 30 dias para os gráficos de tendência
        recent_trends = (
            daily_trends[-30:] if daily_trends is not None and len(daily_trends) > 0 else []
        )
        revenue_trend = [float(dt.get("total_revenue") or 0) for dt in recent_trends]
        orders_trend = [int(dt.get("total_orders") or 0) for dt in recent_trends]

        # Processar top_products
        top_products_list = []
        for _, p_row in top_products_df.iterrows():
            name = str(p_row["name"])[:8] + "..."  # Truncar ID como nome se não houver alias
            top_products_list.append({"name": name, "sales": float(p_row.get("sales") or 0)})

        # Processar categories
        categories_list = []
        for _, cat_row in categories_df.iterrows():
            cat_name = cat_row["category"] if pd.notna(cat_row["category"]) else "Desconhecido"
            categories_list.append(
                {"category": cat_name, "sales": float(cat_row.get("sales") or 0)}
            )

        # Mapeamento do dicionário final para a rota
        avg_ov = (
            float(row.get("avg_order_value", 0)) if pd.notna(row.get("avg_order_value", 0)) else 0.0
        )

        return {
            "total_revenue": float(row.get("total_revenue", 0) or 0),
            "total_orders": int(row.get("total_orders", 0) or 0),
            "avg_order_value": avg_ov,
            "total_customers": int(row.get("total_customers", 0) or 0),
            "revenue_trend": revenue_trend,
            "orders_trend": orders_trend,
            "top_products": top_products_list,
            "sales_by_category": categories_list,
        }
