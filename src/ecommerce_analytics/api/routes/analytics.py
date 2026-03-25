"""
Endpoints de análise
"""

import logging
import traceback
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ecommerce_analytics.api.auth import verify_token
from ecommerce_analytics.bigquery.client import BigQueryClient
from ecommerce_analytics.core.exceptions import BigQueryError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/analytics", tags=["analytics"])


class AnalyticsResponse(BaseModel):
    """Resposta de análise"""

    total_customers: int
    total_orders: int
    avg_order_value: float
    max_order_value: float
    total_revenue: float


@router.get("/dashboard", response_model=AnalyticsResponse)
async def get_analytics_dashboard(
    token: dict[str, Any] = Depends(verify_token)
) -> AnalyticsResponse:
    """Retorna métricas principais do dashboard"""
    try:
        logger.info("📊 Iniciando requisição de dashboard...")
        logger.info(f"✅ Usuário autenticado: {token.get('sub')}")

        bq = BigQueryClient()
        logger.info("✅ Cliente BigQuery criado com sucesso")

        logger.info("📈 Buscando métricas de clientes...")
        metrics = bq.get_customer_metrics()
        logger.info(f"✅ Métricas obtidas: {metrics}")

        if not metrics:
            logger.error("❌ Métricas vazias!")
            raise BigQueryError("Nenhuma métrica encontrada")

        response = AnalyticsResponse(
            total_customers=int(metrics.get("total_customers", 0)),
            total_orders=int(metrics.get("total_orders", 0)),
            avg_order_value=float(metrics.get("avg_order_value", 0)),
            max_order_value=float(metrics.get("max_order_value", 0)),
            total_revenue=float(metrics.get("total_revenue", 0)),
        )

        logger.info(f"✅ Dashboard retornado com sucesso: {response}")
        return response

    except BigQueryError as e:
        logger.error(f"❌ Erro BigQuery: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar métricas: {str(e)}",
        )
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}",
        )


@router.get("/top-products")
async def get_top_products(
    limit: int = 10, token: dict[str, Any] = Depends(verify_token)
) -> list[dict[str, Any]]:
    """Retorna produtos mais vendidos"""
    try:
        logger.info(f"📦 Buscando top {limit} produtos...")
        bq = BigQueryClient()
        df = bq.get_top_products(limit=limit)

        result: list[dict[str, Any]] = [
            {str(k): v for k, v in row.items()} for row in df.to_dict(orient="records")
        ]
        logger.info(f"✅ Top products retornado: {len(result)} produtos")
        return result

    except BigQueryError as e:
        logger.error(f"❌ Erro BigQuery: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar produtos: {str(e)}",
        )
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}",
        )


@router.get("/sales-by-category")
async def get_sales_by_category(
    token: dict[str, Any] = Depends(verify_token)
) -> list[dict[str, Any]]:
    """Retorna vendas por categoria"""
    try:
        logger.info("🏷️  Buscando vendas por categoria...")
        bq = BigQueryClient()
        df = bq.get_sales_by_category()

        result: list[dict[str, Any]] = [
            {str(k): v for k, v in row.items()} for row in df.to_dict(orient="records")
        ]
        logger.info(f"✅ Sales by category retornado: {len(result)} categorias")
        return result

    except BigQueryError as e:
        logger.error(f"❌ Erro BigQuery: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar categorias: {str(e)}",
        )
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}",
        )
