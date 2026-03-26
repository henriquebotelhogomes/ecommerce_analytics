from typing import Any, Dict, List

import pandas as pd
from loguru import logger

from ecommerce_analytics.bigquery.client import BigQueryClient
from ecommerce_analytics.core.config import settings


class RecommendationService:
    def __init__(self):
        self.bq_client = BigQueryClient()
        self.project = settings.gcp_project_id
        self.dataset = settings.gcp_dataset_id

    def get_product_recommendations(self, customer_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Gera recomendações de produtos via SQL heurístico buscando os itens
        mais comprados pelos clientes da mesma cidade.
        Caso o cliente não tenha histórico, retorna os 'Best Sellers'.
        """
        logger.info(f"Calculando recomendação com heurística heurística SQL para {customer_id}")

        # Busca a cidade do cliente e usa como filtro ou faz um best seller geral
        reco_sql = f"""
        WITH user_loc AS (
            SELECT customer_city as city_name
            FROM `{self.project}.{self.dataset}.customers`
            WHERE customer_id = '{customer_id}'
            LIMIT 1
        ),
        best_sellers AS (
            SELECT
                p.product_id,
                MAX(p.product_category_name) as name,
                COUNT(*) as times_sold
            FROM `{self.project}.{self.dataset}.order_items` oi
            JOIN `{self.project}.{self.dataset}.products` p ON oi.product_id = p.product_id
            JOIN `{self.project}.{self.dataset}.orders` o ON oi.order_id = o.order_id
            JOIN `{self.project}.{self.dataset}.customers` c ON o.customer_id = c.customer_id
            WHERE
                NOT EXISTS (SELECT 1 FROM user_loc)
                OR c.customer_city = (SELECT city_name FROM user_loc LIMIT 1)
            GROUP BY 1
            ORDER BY times_sold DESC
            LIMIT {limit}
        )
        SELECT * FROM best_sellers
        """

        try:
            df = self.bq_client.query(reco_sql)

            # Fallback se a city view não retornar dados, pego os genéricos
            if df.empty:
                fallback_sql = f"""
                SELECT p.product_id, MAX(p.product_category_name) as name, COUNT(*) as times_sold
                FROM `{self.project}.{self.dataset}.order_items` oi
                JOIN `{self.project}.{self.dataset}.products` p ON oi.product_id = p.product_id
                GROUP BY 1 ORDER BY times_sold DESC LIMIT {limit}
                """
                df = self.bq_client.query(fallback_sql)

        except Exception as e:
            logger.error(f"Falha na recomendação SQL estendida: {e}")
            return []

        recommendations = []
        max_sold = (
            float(df["times_sold"].max()) if not df.empty and df["times_sold"].max() > 0 else 1.0
        )

        for _, row in df.iterrows():
            name_val = row["name"]
            score = round(float(row["times_sold"]) / max_sold, 2)  # Normaliza como um score 0-1

            recommendations.append(
                {
                    "product_id": str(row["product_id"]),
                    "name": name_val if pd.notna(name_val) else "Best Seller Product",
                    "score": min(0.99, score),
                }
            )

        return recommendations
