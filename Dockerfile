# ========== STAGE 1: Builder ==========
FROM python:3.12-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip setuptools wheel && \
    pip install -e .

# ========== STAGE 2: Runtime ==========
FROM python:3.12-slim

LABEL authors="henrique botelho gomes"
LABEL description="E-commerce Analytics with FastAPI + Plotly Dash"
LABEL version="1.0.0"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv
COPY src/ /app/src/
COPY pyproject.toml README.md /app/

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8080}/health || exit 1

EXPOSE 8080

# Comando para rodar API + Dashboard
CMD exec uvicorn src.ecommerce_analytics.api.main:app \
    --host 0.0.0.0 \
    --port 8080 \
    --workers 1