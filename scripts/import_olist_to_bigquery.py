"""
Script para importar Olist Dataset para BigQuery
Uso: python scripts/import_olist_to_bigquery.py
     (execute de qualquer diretório dentro do projeto)
"""

import os
import sys
from pathlib import Path
from google.cloud import bigquery

# ============================================================================
# CONFIGURAÇÃO - CAMINHOS ROBUSTOS
# ============================================================================

# Obter o diretório do script (onde este arquivo está)
SCRIPT_DIR = Path(__file__).parent.absolute()

# Obter o diretório raiz do projeto (um nível acima de scripts/)
PROJECT_ROOT = SCRIPT_DIR.parent

# Caminho para os dados (relativo ao projeto)
OLIST_DATA_PATH = PROJECT_ROOT / "data" / "olist"

# Substitua pelo seu Project ID do GCP
PROJECT_ID = "ecommerce-analytics-491215"

# Dataset no BigQuery
DATASET_ID = "olist_ecommerce"

# Mapeamento de arquivo CSV → nome da tabela no BigQuery
FILES_TO_IMPORT = {
    "olist_customers_dataset.csv": "customers",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset_clean.csv": "order_reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "olist_geolocation_dataset.csv": "geolocation",
}

# ============================================================================
# FUNÇÕES
# ============================================================================

def import_csv_to_bigquery(
    project_id: str,
    dataset_id: str,
    csv_path: Path,
    table_id: str
) -> None:
    """
    Importa um arquivo CSV para BigQuery.

    Args:
        project_id: ID do projeto GCP
        dataset_id: ID do dataset no BigQuery
        csv_path: Caminho para o arquivo CSV
        table_id: Nome da tabela no BigQuery
    """
    client = bigquery.Client(project=project_id)

    print(f"📥 Importando {csv_path.name} → {table_id}...")

    # Configuração do job de importação
    job_config = bigquery.LoadJobConfig(
        autodetect=True,  # Detecta schema automaticamente
        skip_leading_rows=1,  # Pula header
        source_format=bigquery.SourceFormat.CSV,
        allow_quoted_newlines=True,  # Permite quebras de linha em campos
    )

    try:
        with open(csv_path, "rb") as source_file:
            load_job = client.load_table_from_file(
                source_file,
                f"{project_id}.{dataset_id}.{table_id}",
                job_config=job_config,
            )

        # Aguarda conclusão do job
        load_job.result()
        print(f"✅ {table_id} importada com sucesso!")

    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {csv_path}")
        raise
    except Exception as e:
        print(f"❌ Erro ao importar {table_id}: {str(e)}")
        raise


def main() -> None:
    """
    Importa todos os arquivos CSV para BigQuery.
    """
    print(f"\n{'='*70}")
    print(f"🚀 Iniciando importação do Olist Dataset para BigQuery")
    print(f"{'='*70}\n")

    print(f"📍 Projeto GCP: {PROJECT_ID}")
    print(f"📍 Dataset: {DATASET_ID}")
    print(f"📍 Diretório raiz do projeto: {PROJECT_ROOT}")
    print(f"📍 Caminho dos dados: {OLIST_DATA_PATH}\n")

    # Verificar se a pasta existe
    if not OLIST_DATA_PATH.exists():
        print(f"❌ Pasta não encontrada: {OLIST_DATA_PATH}")
        print(f"\n💡 Crie a pasta e coloque os CSVs lá:")
        print(f"   mkdir {OLIST_DATA_PATH}")
        print(f"\n   Depois coloque os arquivos CSV em: {OLIST_DATA_PATH}\n")
        sys.exit(1)

    # Listar arquivos encontrados
    print(f"📂 Arquivos encontrados em {OLIST_DATA_PATH}:")
    csv_files = list(OLIST_DATA_PATH.glob("*.csv"))
    if csv_files:
        for f in csv_files:
            print(f"   ✅ {f.name}")
    else:
        print(f"   ❌ Nenhum arquivo CSV encontrado!")
        sys.exit(1)

    print()

    # Contar arquivos encontrados
    files_found = 0
    files_missing = 0

    for csv_file, table_name in FILES_TO_IMPORT.items():
        csv_path = OLIST_DATA_PATH / csv_file

        if not csv_path.exists():
            print(f"⚠️  Arquivo não encontrado: {csv_path}")
            files_missing += 1
            continue

        files_found += 1
        import_csv_to_bigquery(PROJECT_ID, DATASET_ID, csv_path, table_name)

    # Resumo
    print(f"\n{'='*70}")
    print(f"📊 Resumo da Importação:")
    print(f"   ✅ Importados: {files_found}")
    print(f"   ⚠️  Faltando: {files_missing}")
    print(f"{'='*70}\n")

    if files_missing > 0:
        print(f"💡 Dica: Verifique se todos os CSVs estão em:")
        print(f"   {OLIST_DATA_PATH.absolute()}")


if __name__ == "__main__":
    main()