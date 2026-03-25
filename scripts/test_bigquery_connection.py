"""
Test BigQuery Connection - E-commerce Analytics
Verifica se a conexão com BigQuery está funcionando.
"""

from google.cloud import bigquery
from loguru import logger


def test_bigquery_connection():
    """Testar conexão com BigQuery."""
    try:
        # Inicializar cliente
        client = bigquery.Client(project="ecommerce-analytics-491215")
        logger.info("✅ BigQuery client inicializado")

        # Listar datasets
        datasets = list(client.list_datasets())
        logger.info(f"✅ Datasets encontrados: {len(datasets)}")

        for dataset in datasets:
            logger.info(f"  - {dataset.dataset_id}")

        # Listar tabelas do dataset olist_ecommerce
        dataset_id = "olist_ecommerce"
        dataset = client.get_dataset(dataset_id)
        tables = list(client.list_tables(dataset))

        logger.info(f"✅ Tabelas no dataset '{dataset_id}': {len(tables)}")
        for table in tables:
            logger.info(f"  - {table.table_id}")

        # Executar query de teste
        query = """
                SELECT COUNT(*)                    as total_orders, \
                       COUNT(DISTINCT customer_id) as total_customers, \
                       999 AS total_revenue, \
                FROM ecommerce-analytics-491215.olist_ecommerce.orders \
                """

        query_job = client.query(query)
        results = query_job.result()

        for row in results:
            logger.info(f"✅ Query Results:")
            logger.info(f"  - Total Orders: {row.total_orders}")
            logger.info(f"  - Total Customers: {row.total_customers}")
            logger.info(f"  - Total Revenue: ${row.total_revenue}")

        return True

    except Exception as e:
        logger.error(f"❌ Erro ao conectar ao BigQuery: {e}")
        return False


if __name__ == "__main__":
    success = test_bigquery_connection()
    exit(0 if success else 1)