"""
Script para limpar o arquivo olist_order_reviews_dataset.csv
Remove linhas problemáticas e normaliza encoding
"""

import pandas as pd
from pathlib import Path
import sys


def clean_reviews_csv():
    """
    Limpa o arquivo de reviews com problemas de encoding
    """
    data_path = Path(__file__).parent.parent / "data" / "olist"
    input_file = data_path / "olist_order_reviews_dataset.csv"
    output_file = data_path / "olist_order_reviews_dataset_clean.csv"

    print(f"📖 Lendo arquivo: {input_file}")

    try:
        # Tentar ler com diferentes encodings
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        df = None

        for encoding in encodings:
            try:
                print(f"   Tentando encoding: {encoding}...")
                df = pd.read_csv(
                    input_file,
                    encoding=encoding,
                    on_bad_lines='skip',  # Pula linhas problemáticas
                    engine='python',  # Usa parser mais flexível
                )
                print(f"   ✅ Sucesso com encoding: {encoding}")
                break
            except Exception as e:
                print(f"   ❌ Falhou: {str(e)[:50]}")
                continue

        if df is None:
            print("❌ Não foi possível ler o arquivo com nenhum encoding")
            sys.exit(1)

        print(f"\n📊 Dados carregados:")
        print(f"   Linhas: {len(df)}")
        print(f"   Colunas: {list(df.columns)}")

        # Limpar dados
        print(f"\n🧹 Limpando dados...")

        # Remover linhas com valores nulos nas colunas principais
        df = df.dropna(subset=['review_id', 'order_id'])
        print(f"   ✅ Removidas linhas com review_id ou order_id nulos")

        # Normalizar comentários (remover quebras de linha extras)
        if 'review_comment_message' in df.columns:
            df['review_comment_message'] = df['review_comment_message'].fillna('')
            df['review_comment_message'] = df['review_comment_message'].str.replace(
                r'\n+', ' ', regex=True
            )
            df['review_comment_message'] = df['review_comment_message'].str.strip()
            print(f"   ✅ Normalizados comentários")

        # Remover duplicatas
        initial_count = len(df)
        df = df.drop_duplicates(subset=['review_id'])
        removed = initial_count - len(df)
        if removed > 0:
            print(f"   ✅ Removidas {removed} linhas duplicadas")

        # Salvar arquivo limpo
        print(f"\n💾 Salvando arquivo limpo: {output_file}")
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"   ✅ Arquivo salvo com sucesso!")

        print(f"\n📈 Resultado final:")
        print(f"   Linhas: {len(df)}")
        print(f"   Colunas: {list(df.columns)}")

        return output_file

    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    clean_reviews_csv()