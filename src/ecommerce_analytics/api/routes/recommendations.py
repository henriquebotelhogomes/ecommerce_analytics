"""
Recommendations Routes
Endpoints para recomendações de produtos.
"""

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from pydantic import BaseModel

from ecommerce_analytics.api.auth import get_current_user

router = APIRouter()


# ========== SCHEMAS ==========
class RecommendationRequest(BaseModel):
    """Recommendation request schema."""

    customer_id: str


class RecommendationResponse(BaseModel):
    """Recommendation response schema."""

    status: str
    recommendations: list


# ========== ENDPOINTS ==========
@router.post("/products", response_model=RecommendationResponse)
async def get_product_recommendations(
    request: RecommendationRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Retorna recomendações de produtos para um cliente.
    Requer autenticação.
    """
    try:
        if not request.customer_id:
            raise ValueError("customer_id é obrigatório")

        logger.info(f"💡 Recomendações solicitadas por: {current_user['username']}")

        return {
            "status": "success",
            "recommendations": [
                {"product_id": "P001", "name": "Product A", "score": 0.95},
                {"product_id": "P002", "name": "Product B", "score": 0.87},
                {"product_id": "P003", "name": "Product C", "score": 0.79},
            ],
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error(f"❌ Erro ao gerar recomendações: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e
