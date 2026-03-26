"""
Analytics Routes - E-commerce Analytics API
"""

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from ecommerce_analytics.api.auth import get_current_user
from ecommerce_analytics.services.analytics_service import AnalyticsService

router = APIRouter()


def get_analytics_service() -> AnalyticsService:
    return AnalyticsService()


@router.get("/dashboard")
def get_dashboard(
    current_user: dict = Depends(get_current_user),
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Obter dados do dashboard via BigQuery.
    Retorna métricas principais e tendências.
    """
    try:
        # Busca real no BigQuery
        dashboard_data = service.get_dashboard_data()

        logger.info(f"📊 Dashboard data retrieved for user: {current_user['username']}")
        return dashboard_data

    except Exception as e:
        logger.error(f"❌ Error retrieving dashboard data: {e}")
        raise HTTPException(
            status_code=500, detail="Error retrieving dashboard data from BigQuery"
        ) from e
