import datetime
from typing import Any, Dict, List

from loguru import logger

from ecommerce_analytics.bigquery.client import BigQueryClient
from ecommerce_analytics.core.config import settings


class ForecastService:
    def __init__(self):
        self.bq_client = BigQueryClient()
        self.project = settings.gcp_project_id
        self.dataset = settings.gcp_dataset_id

    def get_revenue_forecast(self, months_ahead: int) -> List[Dict[str, Any]]:
        """
        Extrapolação heurística da previsão com base nos últimos dados de receita diária.
        (Aguardando treinamento de modelo BQML para integração final).
        """
        logger.info(f"Executando heurística de previsão de {months_ahead} meses...")

        # Agrupar últimos meses disponíveis e calcular média de crescimento (M-o-M) simplificada
        forecast_sql = f"""
        WITH monthly_sales AS (
            SELECT
                EXTRACT(YEAR FROM sale_date) as year,
                EXTRACT(MONTH FROM sale_date) as month,
                SUM(total_revenue) as revenue
            FROM `{self.project}.{self.dataset}.daily_sales`
            GROUP BY 1, 2
            HAVING SUM(total_revenue) > 0
            ORDER BY year DESC, month DESC
            LIMIT 6
        )
        SELECT * FROM monthly_sales ORDER BY year, month
        """
        df = self.bq_client.query(forecast_sql)

        if df.empty or len(df) < 2:
            return []

        # Calcular crescimento médio mensal e taxa base
        revenues = [float(r or 0) for r in df["revenue"].tolist()]
        growth_rates = []
        for i in range(1, len(revenues)):
            rate = (revenues[i] - revenues[i - 1]) / revenues[i - 1] if revenues[i - 1] > 0 else 0
            growth_rates.append(rate)

        avg_growth = (
            sum(growth_rates) / len(growth_rates) if growth_rates else 0.05
        )  # default 5% capado
        avg_growth = max(-0.1, min(0.15, avg_growth))  # Cap entre -10% e +15% para não estourar

        last_revenue = revenues[-1]

        # Pega o último ano/mês (ou assume o atual se falhar)
        last_year = int(df.iloc[-1]["year"])
        last_month = int(df.iloc[-1]["month"])

        current_date = datetime.date(last_year, last_month, 1)

        forecast_data = []
        projected_rev = last_revenue

        for _ in range(months_ahead):
            # Próximo mês
            if current_date.month == 12:
                current_date = datetime.date(current_date.year + 1, 1, 1)
            else:
                current_date = datetime.date(current_date.year, current_date.month + 1, 1)

            projected_rev = projected_rev * (1 + avg_growth)
            month_name = current_date.strftime("%b %Y")  # ex: Apr 2026

            forecast_data.append(
                {"month": month_name, "predicted_revenue": float(max(0, projected_rev))}
            )

        return forecast_data
