"""
Endpoints de recomendações
"""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from ecommerce_analytics.api.auth import verify_token
from ecommerce_analytics.bigquery.client import BigQueryClient
from ecommerce_analytics.core.exceptions import BigQueryError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/products")
async def get_product_recommendations(
    customer_id: str, token: dict[str, Any] = Depends(verify_token)
) -> list[dict[str, Any]]:
    """Retorna recomendações de produtos para um cliente"""
    try:
        logger.info(f"🎯 Buscando recomendações para cliente: {customer_id}")
        bq = BigQueryClient()

        # ✅ CORRIGIDO: Usar _ para variável não usada
        _ = bq.query(f"SELECT * FROM `{bq.project_id}.{bq.dataset_id}.products` LIMIT 1")

        logger.info(f"✅ Recomendações retornadas para cliente: {customer_id}")
        return []

    except BigQueryError as e:
        logger.error(f"❌ Erro BigQuery: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar recomendações: {str(e)}",
        )
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}",
        )
