"""
BigQuery Client - E-commerce Analytics
Handles all BigQuery operations with real data from olist_ecommerce dataset.
"""

from google.cloud import bigquery
from google.cloud.bigquery import QueryJobConfig
from google.api_core.exceptions import GoogleAPIError, NotFound
from loguru import logger
from ecommerce_analytics.core.config import settings
from typing import List, Dict, Any, Optional


class BigQueryClient:
    """Cliente para operações com BigQuery com tratamento robusto de erros."""

    def __init__(self):
        """Inicializar cliente BigQuery."""
        try:
            self.client = bigquery.Client(project=settings.gcp_project_id)
            self.dataset_id = settings.gcp_dataset_id

            # Testar conexão
            self._test_connection()

            logger.info(f"✅ BigQuery client inicializado")
            logger.info(f"   Projeto: {settings.gcp_project_id}")
            logger.info(f"   Dataset: {settings.gcp_dataset_id}")

        except Exception as e:
            logger.error(f"❌ Erro ao inicializar BigQuery client: {e}")
            raise

    def _test_connection(self) -> bool:
        """Testar conexão com BigQuery."""
        try:
            # Tentar listar datasets
            list(self.client.list_datasets(max_results=1))
            logger.info("✅ Conexão com BigQuery validada")
            return True
        except NotFound as e:
            logger.error(f"❌ Projeto não encontrado: {e}")
            raise
        except GoogleAPIError as e:
            logger.error(f"❌ Erro de autenticação: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Erro ao testar conexão: {e}")
            raise

    def _execute_query(self, query: str, query_params: Optional[List] = None) -> Any:
        """
        Executar query com tratamento de erros.

        Args:
            query: SQL query string
            query_params: Parâmetros da query (opcional)

        Returns:
            Resultado da query
        """
        try:
            job_config = QueryJobConfig()

            if query_params:
                job_config.query_parameters = query_params

            query_job = self.client.query(query, job_config=job_config)
            results = query_job.result(timeout=30)

            return results

        except NotFound as e:
            logger.error(f"❌ Tabela/Dataset não encontrado: {e}")
            raise
        except GoogleAPIError as e:
            logger.error(f"❌ Erro na query: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Erro ao executar query: {e}")
            raise

    def get_dashboard_metrics(self) -> Dict[str, Any]:
        """
        Obter métricas do dashboard usando colunas reais da tabela orders.

        Retorna:
            - total_orders: Número total de pedidos
            - total_customers: Número de clientes únicos
            - avg_delivery_time: Tempo médio de entrega em dias
            - orders_by_status: Contagem de pedidos por status
        """
        try:
            query = f"""
            SELECT
                COUNT(DISTINCT order_id) as total_orders,
                COUNT(DISTINCT customer_id) as total_customers,
                ROUND(AVG(
                    DATE_DIFF(
                        order_delivered_customer_date,
                        order_purchase_timestamp,
                        DAY
                    )
                ), 2) as avg_delivery_time
            FROM `{settings.gcp_project_id}.{self.dataset_id}.orders`
            WHERE order_status IN ('delivered', 'shipped', 'processing')
                AND order_purchase_timestamp >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
            """

            results = self._execute_query(query)
            row = next(results)

            metrics = {
                "total_orders": int(row.total_orders or 0),
                "total_customers": int(row.total_customers or 0),
                "avg_delivery_time": float(row.avg_delivery_time or 0),
            }

            logger.info(f"✅ Dashboard metrics obtidas")
            return metrics

        except Exception as e:
            logger.error(f"❌ Erro ao obter dashboard metrics: {e}")
            return {
                "total_orders": 0,
                "total_customers": 0,
                "avg_delivery_time": 0,
            }

    def get_orders_by_status(self) -> List[Dict[str, Any]]:
        """
        Obter contagem de pedidos por status.

        Retorna:
            Lista com status e contagem de pedidos
        """
        try:
            query = f"""
            SELECT
                order_status as status,
                COUNT(DISTINCT order_id) as count
            FROM `{settings.gcp_project_id}.{self.dataset_id}.orders`
            WHERE order_purchase_timestamp >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
            GROUP BY order_status
            ORDER BY count DESC
            """

            results = self._execute_query(query)

            status_data = [
                {
                    "status": row.status or "unknown",
                    "count": int(row.count),
                }
                for row in results
            ]

            logger.info(f"✅ Orders by status obtidas: {len(status_data)} status")
            return status_data

        except Exception as e:
            logger.error(f"❌ Erro ao obter orders by status: {e}")
            return []

    def get_orders_trend(self, months: int = 6) -> List[Dict[str, Any]]:
        """
        Obter tendência de pedidos por mês.

        Args:
            months: Número de meses para análise

        Retorna:
            Lista com data e contagem de pedidos
        """
        try:
            query = f"""
            SELECT
                DATE_TRUNC(DATE(order_purchase_timestamp), MONTH) as month,
                COUNT(DISTINCT order_id) as order_count,
                COUNT(DISTINCT customer_id) as customer_count
            FROM `{settings.gcp_project_id}.{self.dataset_id}.orders`
            WHERE order_purchase_timestamp >= DATE_SUB(CURRENT_DATE(), INTERVAL {months} MONTH)
            GROUP BY DATE_TRUNC(DATE(order_purchase_timestamp), MONTH)
            ORDER BY month ASC
            """

            results = self._execute_query(query)

            trend = [
                {
                    "month": str(row.month),
                    "orders": int(row.order_count),
                    "customers": int(row.customer_count),
                }
                for row in results
            ]

            logger.info(f"✅ Orders trend obtida: {len(trend)} meses")
            return trend

        except Exception as e:
            logger.error(f"❌ Erro ao obter orders trend: {e}")
            return []

    def get_delivery_performance(self) -> Dict[str, Any]:
        """
        Obter performance de entrega.

        Retorna:
            - on_time: Percentual de entregas no prazo
            - late: Percentual de entregas atrasadas
            - avg_days: Dias médios de entrega
        """
        try:
            query = f"""
            SELECT
                ROUND(
                    SUM(CASE 
                        WHEN order_delivered_customer_date <= order_estimated_delivery_date 
                        THEN 1 ELSE 0 
                    END) * 100.0 / COUNT(*),
                    2
                ) as on_time_percentage,
                ROUND(
                    SUM(CASE 
                        WHEN order_delivered_customer_date > order_estimated_delivery_date 
                        THEN 1 ELSE 0 
                    END) * 100.0 / COUNT(*),
                    2
                ) as late_percentage,
                ROUND(AVG(
                    DATE_DIFF(
                        order_delivered_customer_date,
                        order_purchase_timestamp,
                        DAY
                    )
                ), 2) as avg_delivery_days
            FROM `{settings.gcp_project_id}.{self.dataset_id}.orders`
            WHERE order_status = 'delivered'
                AND order_delivered_customer_date IS NOT NULL
                AND order_estimated_delivery_date IS NOT NULL
                AND order_purchase_timestamp >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
            """

            results = self._execute_query(query)
            row = next(results)

            performance = {
                "on_time": float(row.on_time_percentage or 0),
                "late": float(row.late_percentage or 0),
                "avg_days": float(row.avg_delivery_days or 0),
            }

            logger.info(f"✅ Delivery performance obtida")
            return performance

        except Exception as e:
            logger.error(f"❌ Erro ao obter delivery performance: {e}")
            return {
                "on_time": 0,
                "late": 0,
                "avg_days": 0,
            }

    def get_customer_analysis(self) -> Dict[str, Any]:
        """
        Obter análise de clientes.

        Retorna:
            - total_customers: Total de clientes
            - repeat_customers: Clientes que repetiram compra
            - avg_orders_per_customer: Média de pedidos por cliente
        """
        try:
            query = f"""
            WITH customer_orders AS (
                SELECT
                    customer_id,
                    COUNT(DISTINCT order_id) as order_count
                FROM `{settings.gcp_project_id}.{self.dataset_id}.orders`
                WHERE order_purchase_timestamp >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
                GROUP BY customer_id
            )
            SELECT
                COUNT(DISTINCT customer_id) as total_customers,
                SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) as repeat_customers,
                ROUND(AVG(order_count), 2) as avg_orders_per_customer
            FROM customer_orders
            """

            results = self._execute_query(query)
            row = next(results)

            analysis = {
                "total_customers": int(row.total_customers or 0),
                "repeat_customers": int(row.repeat_customers or 0),
                "avg_orders_per_customer": float(row.avg_orders_per_customer or 0),
            }

            logger.info(f"✅ Customer analysis obtida")
            return analysis

        except Exception as e:
            logger.error(f"❌ Erro ao obter customer analysis: {e}")
            return {
                "total_customers": 0,
                "repeat_customers": 0,
                "avg_orders_per_customer": 0,
            }


# ========== SINGLETON ==========
_bigquery_client: Optional[BigQueryClient] = None


def get_bigquery_client() -> BigQueryClient:
    """Obter instância singleton do BigQuery client."""
    global _bigquery_client
    if _bigquery_client is None:
        _bigquery_client = BigQueryClient()
    return _bigquery_client