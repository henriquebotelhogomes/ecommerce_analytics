"""
Analytics Routes
Endpoints para análise de dados do e-commerce.
"""

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from ecommerce_analytics.api.auth import get_current_user
from ecommerce_analytics.core.exceptions import InvalidLocationError

router = APIRouter()

# ========== VALIDAÇÃO ==========
VALID_LOCATIONS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]


def validate_location(location: str) -> None:
    """Valida se localização é válida."""
    if location not in VALID_LOCATIONS:
        raise InvalidLocationError(
            location=location,
            valid_locations=VALID_LOCATIONS,
        )


# ========== ENDPOINTS ==========
@router.get("/dashboard")
async def get_dashboard(current_user: dict = Depends(get_current_user)):
    """
    Retorna dashboard com métricas principais.
    Requer autenticação.
    """
    try:
        logger.info(f"📊 Dashboard acessado por: {current_user['username']}")

        return {
            "status": "success",
            "data": {
                "total_sales": 1200000,
                "active_customers": 5200,
                "conversion_rate": 3.2,
                "avg_order_value": 245,
            },
        }
    except Exception as e:
        logger.error(f"❌ Erro ao gerar dashboard: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"error": "DASHBOARD_ERROR", "message": str(e)},
        ) from e


@router.get("/top-products")
async def get_top_products(
    limit: int = 10,
    current_user: dict = Depends(get_current_user),
):
    """
    Retorna top N produtos por vendas.
    Requer autenticação.
    """
    try:
        if limit < 1 or limit > 100:
            raise ValueError("Limit deve estar entre 1 e 100")

        logger.info(f"🏆 Top produtos solicitados por: {current_user['username']}")

        return {
            "status": "success",
            "limit": limit,
            "data": [
                {"product_id": "P001", "name": "Product A", "sales": 450},
                {"product_id": "P002", "name": "Product B", "sales": 380},
                {"product_id": "P003", "name": "Product C", "sales": 320},
            ],
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error(f"❌ Erro ao buscar top produtos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/sales-by-category")
async def get_sales_by_category(current_user: dict = Depends(get_current_user)):
    """
    Retorna vendas por categoria.
    Requer autenticação.
    """
    try:
        logger.info(f"📈 Vendas por categoria solicitadas por: {current_user['username']}")

        return {
            "status": "success",
            "data": {
                "Electronics": 450000,
                "Clothing": 380000,
                "Home": 320000,
                "Sports": 280000,
            },
        }
    except Exception as e:
        logger.error(f"❌ Erro ao buscar vendas por categoria: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e
