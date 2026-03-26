"""
Test BigQuery directly - Debug script
"""

from loguru import logger
from ecommerce_analytics.core.bigquery_client import get_bigquery_client


def test_bigquery_direct():
    """Testar BigQuery diretamente."""
    try:
        logger.info("🔍 Testing BigQuery client directly...")

        # Inicializar cliente
        logger.info("📡 Initializing BigQuery client...")
        bq_client = get_bigquery_client()
        logger.info("✅ BigQuery client initialized")

        # Testar get_dashboard_metrics
        logger.info("\n📊 Testing get_dashboard_metrics()...")
        metrics = bq_client.get_dashboard_metrics()
        logger.info(f"✅ Metrics: {metrics}")

        # Testar get_top_products
        logger.info("\n🏆 Testing get_top_products(limit=5)...")
        products = bq_client.get_top_products(limit=5)
        logger.info(f"✅ Products: {products}")

        # Testar get_sales_by_category
        logger.info("\n📈 Testing get_sales_by_category()...")
        categories = bq_client.get_sales_by_category()
        logger.info(f"✅ Categories: {categories}")

        logger.info("\n✅ ALL TESTS PASSED!")
        return True

    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


if __name__ == "__main__":
    success = test_bigquery_direct()
    exit(0 if success else 1)