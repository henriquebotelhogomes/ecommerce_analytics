"""
Recommendations Routes
Endpoints para recomendações de produtos.
"""

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from pydantic import BaseModel

from ecommerce_analytics.api.auth import get_current_user
from ecommerce_analytics.services.ml_service import RecommendationService

router = APIRouter()

def get_recommendation_service() -> RecommendationService:
    return RecommendationService()

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
def get_product_recommendations(
    request: RecommendationRequest,
    current_user: dict = Depends(get_current_user),
    service: RecommendationService = Depends(get_recommendation_service)
):
    """
    Retorna recomendações de produtos para um cliente usando SQL heurístico (BigQuery).
    Requer autenticação.
    """
    try:
        if not request.customer_id:
            raise ValueError("customer_id é obrigatório")

        logger.info(f"💡 Recomendações solicitadas por: {current_user['username']} para o cliente {request.customer_id}")

        recommendations = service.get_product_recommendations(customer_id=request.customer_id, limit=3)

        return {
            "status": "success",
            "recommendations": recommendations,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error(f"❌ Erro ao gerar recomendações: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e
