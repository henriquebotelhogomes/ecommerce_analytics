# ========== STAGE 1: Builder ==========
FROM python:3.12-slim AS builder

WORKDIR /build

# Instalar dependências de build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar pyproject.toml e README.md
COPY pyproject.toml README.md ./

# Criar venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instalar dependências
RUN pip install --upgrade pip setuptools wheel && \
    pip install -e .

# ========== STAGE 2: Runtime ==========
FROM python:3.12-slim

LABEL authors="henrique botelho gomes"
LABEL description="E-commerce Analytics with FastAPI + Plotly Dash"
LABEL version="1.0.0"

WORKDIR /app

# Instalar apenas curl para healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar venv do builder
COPY --from=builder /opt/venv /opt/venv

# Copiar código-fonte
COPY src/ /app/src/
COPY pyproject.toml README.md /app/

# Configurar PATH e PYTHONPATH
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Reinstalar o pacote em Stage 2 (CRÍTICO!)
# Isso garante que os paths estejam corretos em /app
WORKDIR /app
RUN /opt/venv/bin/pip install -e .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8080}/health || exit 1

EXPOSE 8080

# Comando para rodar API
CMD exec uvicorn src.ecommerce_analytics.api.main:app \
    --host 0.0.0.0 \
    --port 8080 \
    --workers 1