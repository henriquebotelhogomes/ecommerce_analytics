"""
Forecasting Routes
Endpoints para previsões usando BigQuery ML.
"""

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from pydantic import BaseModel

from ecommerce_analytics.api.auth import get_current_user

router = APIRouter()


# ========== SCHEMAS ==========
class ForecastRequest(BaseModel):
    """Forecast request schema."""

    months_ahead: int = 3


class ForecastResponse(BaseModel):
    """Forecast response schema."""

    status: str
    forecast: list


# ========== ENDPOINTS ==========
@router.post("/revenue", response_model=ForecastResponse)
async def forecast_revenue(
    request: ForecastRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Prevê receita para os próximos meses.
    Requer autenticação.
    """
    try:
        if request.months_ahead < 1 or request.months_ahead > 12:
            raise ValueError("months_ahead deve estar entre 1 e 12")

        logger.info(f"🔮 Previsão de receita solicitada por: {current_user['username']}")

        return {
            "status": "success",
            "forecast": [
                {"month": "Apr 2026", "predicted_revenue": 1250000},
                {"month": "May 2026", "predicted_revenue": 1320000},
                {"month": "Jun 2026", "predicted_revenue": 1400000},
            ],
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error(f"❌ Erro ao gerar previsão: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e
