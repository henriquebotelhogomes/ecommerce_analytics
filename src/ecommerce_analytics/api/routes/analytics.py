"""
Analytics Routes - E-commerce Analytics API
"""

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from ecommerce_analytics.api.auth import get_current_user
from ecommerce_analytics.core.config import settings

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard(current_user: dict = Depends(get_current_user)):
    """
    Obter dados do dashboard.
    Retorna métricas principais e tendências.
    """
    try:
        # AQUI você buscaria dados do BigQuery
        # Por enquanto, retornando dados mock para teste

        dashboard_data = {
            "total_revenue": 125000.50,
            "total_orders": 450,
            "avg_order_value": 277.78,
            "total_customers": 320,
            "revenue_trend": [10000, 15000, 12000, 18000, 20000, 22000],
            "orders_trend": [50, 75, 60, 90, 100, 110],
            "top_products": [
                {"name": "Product A", "sales": 5000},
                {"name": "Product B", "sales": 4500},
                {"name": "Product C", "sales": 4000},
                {"name": "Product D", "sales": 3500},
                {"name": "Product E", "sales": 3000},
            ],
            "sales_by_category": [
                {"category": "Electronics", "sales": 45000},
                {"category": "Clothing", "sales": 35000},
                {"category": "Home", "sales": 25000},
                {"category": "Sports", "sales": 20000},
            ],
        }

        logger.info(f"📊 Dashboard data retrieved for user: {current_user['username']}")
        return dashboard_data

    except Exception as e:
        logger.error(f"❌ Error retrieving dashboard data: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving dashboard data")