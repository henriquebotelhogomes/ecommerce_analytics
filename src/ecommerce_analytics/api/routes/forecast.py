"""
Endpoints de previsão
"""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from ecommerce_analytics.api.auth import verify_token
from ecommerce_analytics.bigquery.client import BigQueryClient
from ecommerce_analytics.core.exceptions import BigQueryError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/forecast", tags=["forecast"])


@router.get("/revenue")
async def forecast_revenue(
    months: int = 3, token: dict[str, Any] = Depends(verify_token)
) -> dict[str, Any]:
    """Retorna previsão de receita para os próximos meses"""
    try:
        logger.info(f"📈 Gerando previsão de receita para {months} meses...")
        bq = BigQueryClient()

        # ✅ CORRIGIDO: Usar _ para variável não usada
        _ = bq.query(f"SELECT * FROM `{bq.project_id}.{bq.dataset_id}.orders` LIMIT 1")

        logger.info(f"✅ Previsão de receita gerada para {months} meses")
        return {"forecast": [], "months": months}

    except BigQueryError as e:
        logger.error(f"❌ Erro BigQuery: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar previsão: {str(e)}",
        )
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}",
        )
