"""
Script para criar tabelas otimizadas no BigQuery
"""

from google.cloud import bigquery
from ecommerce_analytics.core.config import settings
import logging

logger = logging.getLogger(__name__)


def create_optimized_tables():
    """Cria tabelas particionadas e clusterizadas"""

    client = bigquery.Client(project=settings.gcp_project_id)

    # 1. Tabela orders otimizada
    orders_query = f"""
    CREATE OR REPLACE TABLE `{settings.gcp_project_id}.{settings.gcp_dataset_id}.orders_optimized`
    PARTITION BY DATE(order_purchase_timestamp)
    CLUSTER BY customer_id, order_status
    AS
    SELECT
      order_id,
      customer_id,
      order_status,
      order_purchase_timestamp,
      order_approved_at,
      order_delivered_carrier_date,
      order_delivered_customer_date,
      order_estimated_delivery_date
    FROM `{settings.gcp_project_id}.{settings.gcp_dataset_id}.orders`
    WHERE order_purchase_timestamp IS NOT NULL
    """

    print("📊 Criando tabela orders_optimized...")
    client.query(orders_query).result()
    print("✅ Tabela orders_optimized criada!")

    # 2. Materialized View para vendas diárias
    daily_sales_query = f"""
    CREATE OR REPLACE TABLE `{settings.gcp_project_id}.{settings.gcp_dataset_id}.daily_sales` AS
    SELECT
      DATE(o.order_purchase_timestamp) as sale_date,
      COUNT(DISTINCT o.order_id) as total_orders,
      COUNT(DISTINCT c.customer_unique_id) as unique_customers,
      SUM(oi.price) as total_revenue,
      AVG(oi.price) as avg_order_value,
      COUNT(DISTINCT p.product_category_name) as categories_sold
    FROM `{settings.gcp_project_id}.{settings.gcp_dataset_id}.orders_optimized` o
    LEFT JOIN `{settings.gcp_project_id}.{settings.gcp_dataset_id}.order_items` oi ON o.order_id = oi.order_id
    LEFT JOIN `{settings.gcp_project_id}.{settings.gcp_dataset_id}.products` p ON oi.product_id = p.product_id
    LEFT JOIN `{settings.gcp_project_id}.{settings.gcp_dataset_id}.customers` c ON o.customer_id = c.customer_id
    GROUP BY sale_date
    ORDER BY sale_date DESC
    """

    print("📊 Criando table daily_sales...")
    client.query(daily_sales_query).result()
    print("✅ Table daily_sales criada!")


if __name__ == "__main__":
    create_optimized_tables()