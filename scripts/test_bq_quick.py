"""Teste rápido de BigQuery"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from ecommerce_analytics.core.config import settings
from ecommerce_analytics.bigquery.client import BigQueryClient

print(f"🔍 Testando BigQuery...")
print(f"   Projeto: {settings.gcp_project_id}")
print(f"   Dataset: {settings.gcp_dataset_id}\n")

try:
    bq = BigQueryClient()
    print("✅ Cliente criado com sucesso!\n")

    print("📊 Buscando métricas...")
    metrics = bq.get_customer_metrics()

    if metrics:
        print("✅ Métricas obtidas:")
        for key, value in metrics.items():
            print(f"   {key}: {value}")
    else:
        print("⚠️  Métricas vazias (possível problema na query)")

except Exception as e:
    print(f"❌ Erro: {str(e)}")
    import traceback

    traceback.print_exc()