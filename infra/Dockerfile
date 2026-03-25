FROM python:3.12-slim
LABEL authors="HENRIQUE BOTELHO GOMES"

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos
COPY pyproject.toml .
COPY src/ src/
COPY scripts/ scripts/

# Instalar dependências Python
RUN pip install --no-cache-dir -e .

# Expor portas
EXPOSE 8000 8050

# Comando padrão
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]