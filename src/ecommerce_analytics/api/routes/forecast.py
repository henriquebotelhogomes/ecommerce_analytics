"""
Forecasting Routes
Endpoints para previsões usando BigQuery ML.
"""

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from pydantic import BaseModel

from ecommerce_analytics.api.auth import get_current_user
from ecommerce_analytics.services.forecast_service import ForecastService

router = APIRouter()


def get_forecast_service() -> ForecastService:
    return ForecastService()


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
def forecast_revenue(
    request: ForecastRequest,
    current_user: dict = Depends(get_current_user),
    service: ForecastService = Depends(get_forecast_service),
):
    """
    Prevê receita para os próximos meses via BigQuery Heuristics.
    Requer autenticação.
    """
    try:
        if request.months_ahead < 1 or request.months_ahead > 12:
            raise ValueError("months_ahead deve estar entre 1 e 12")

        logger.info(f"🔮 Previsão de receita solicitada por: {current_user['username']}")

        forecast_results = service.get_revenue_forecast(months_ahead=request.months_ahead)

        return {
            "status": "success",
            "forecast": forecast_results,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error(f"❌ Erro ao gerar previsão: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e
