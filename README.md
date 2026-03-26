# 📊 E-Commerce Analytics Platform

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![BigQuery](https://img.shields.io/badge/BigQuery-Integrated-orange?style=flat-square&logo=google-cloud)](https://cloud.google.com/bigquery)
[![Plotly Dash](https://img.shields.io/badge/Plotly%20Dash-2.14+-purple?style=flat-square&logo=plotly)](https://dash.plotly.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat-square&logo=docker)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

> **Plataforma de analytics em tempo real para e-commerce** com BigQuery, FastAPI e Plotly Dash. Análise de vendas, comportamento de clientes e previsões com ML — **Production Ready** 🚀

---

## 🎯 Visão Geral

Solução **enterprise-grade** que integra:

- ✅ **API REST** profissional com FastAPI + JWT
- ✅ **Dashboard interativo** com Plotly Dash (callbacks em tempo real)
- ✅ **BigQuery** para análise de dados em escala (100M+ registros)
- ✅ **BigQuery ML** para previsão de vendas (ARIMA, Linear Regression)
- ✅ **Autenticação segura** com JWT + refresh tokens
- ✅ **Logging estruturado** com Loguru
- ✅ **Testes completos** (unit + integration, >80% cobertura)
- ✅ **Docker & Docker Compose** para ambiente consistente
- ✅ **CI/CD** com GitHub Actions
- ✅ **Deploy** em Google Cloud Run (serverless)

---

## 🚀 Quick Start (5 minutos)
### Pré-requisitos
```bash
Python 3.12+
Docker & Docker Compose
Google Cloud Account (BigQuery habilitado)
```
### Instalação Local
```bash
# 1. Clonar repositório
git clone https://github.com/henriquebotelhogomes/ecommerce_analytics
cd ecommerce_analytics

# 2. Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\Activate.ps1  # Windows

# 3. Instalar dependências
pip install -e ".[dev]"

# 4. Configurar Google Cloud
gcloud auth application-default login

# 5. Criar arquivo .env
cp .env.example .env
# Editar .env com suas credenciais GCP
```

### Executar  Localmente
```
# Terminal 1: API (http://localhost:8080)
make run-api

# Terminal 2: Dashboard (http://localhost:8050)
make run-dashboard

# Terminal 3: Testes
make test
```
### Com Docker Compose
```bash
docker-compose up -d

# API: http://localhost:8080/docs
# Dashboard: http://localhost:8050
# Logs: docker-compose logs -f
```
---

## 📊 Stack Técnico

| Camada        | Tecnologia       | Versão                   |
|---------------|------------------|--------------------------|
| API           | FastAPI          | 0.100+                   |
| Dashboard     | Plotly Dash      | 2.14+                    |
| Database      | BigQuery         | Cloud Native             |
| ML            | BigQuery ML      | ARIMA, Linear Regression |
| Auth          | JWT              | FastAPI Security         |
| Logging       | Loguru           | Estruturado              |
| Testing       | Pytest           | Unit + Integration       |
| Linting       | Ruff             | Zero Config              |
| Formatting    | Black            | Opinionated              |
| Type Checking | Mypy             | Strict Mode              |
| Container     | Docker           | Multi-stage              |
| Orchestration | Docker Compose   | Local Dev                |
| CI/CD         | GitHub Actions   | Automated                |
| Deploy        | Google Cloud Run | Serverless               |
---
## 📚 Documentação 
### API Endpoints
````
POST   /auth/login              → Autenticar usuário
GET    /auth/me                 → Obter usuário atual
POST   /auth/refresh            → Renovar token
POST   /auth/logout             → Logout

GET    /api/v1/analytics/dashboard              → Métricas gerais
GET    /api/v1/analytics/top-products           → Top 10 produtos
GET    /api/v1/analytics/sales-by-category      → Vendas por categoria

GET    /api/v1/forecast/sales-forecast          → Previsão 30 dias
GET    /health                                  → Health check
````
* Documentação Interativa: http://localhost:8080/docs (Swagger UI)
* **Credenciais Demo:**
  * **Username**: admin
  * **Password**: admin123
---

## 🧪 Testes
```
# Todos os testes
make test

# Com cobertura
pytest tests/ -v --cov=src/ecommerce_analytics --cov-report=html

# Teste específico
pytest tests/test_api.py::test_login -v

# Watch mode
pytest-watch tests/
```
**Cobertura esperada: >80%**
---

## 🔍 Qualidade de Código
```
# Lint
make lint

# Format
make format

# Type checking
make type-check

# Tudo junto
make quality
```

* **Critério**: 0 erros em ruff, black, mypy
---
## 🐳 Docker
```bash
# Build API
docker build -t ecommerce-analytics:latest .

# Build Dashboard
docker build -f Dockerfile.dash -t ecommerce-analytics-dash:latest .
```
### Run
```bash
# Com Docker Compose (recomendado)
docker-compose up -d

# Ou individual
docker run -p 8080:8080 ecommerce-analytics:latest
docker run -p 8050:8050 ecommerce-analytics-dash:latest
```
---

## ☁️ Deploy em Produção
### Google Cloud Run
```bash
# 1. Autenticar
gcloud auth login
gcloud config set project seu-projeto-gcp

# 2. Deploy API
gcloud run deploy ecommerce-analytics-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "ENVIRONMENT=production,GCP_PROJECT_ID=seu-projeto"

# 3. Deploy Dashboard
gcloud run deploy ecommerce-analytics-dashboard \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "API_BASE_URL=https://sua-api-url.run.app"

# 4. Testar
curl https://sua-api-url.run.app/health
```
---

## 📈 Arquitetura
```
┌─────────────────────────────────────────────────────────┐
│                    Client (Browser)                     │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌──────────────────┐      ┌──────────────────┐
│   FastAPI (8080) │      │  Plotly Dash     │
│   - Auth (JWT)   │      │  (8050)          │
│   - Analytics    │      │  - Callbacks     │
│   - Forecast     │      │  - Real-time     │
└────────┬─────────┘      └────────┬─────────┘
         │                         │
         └────────────┬────────────┘
                      │
                      ▼
            ┌──────────────────────┐
            │   BigQuery (GCP)     │
            │ - OLIST Dataset      │
            │ - ML Models          │
            │ - Real-time Queries  │
            └──────────────────────┘
```
---

## 🔐 Segurança
- ✅ JWT com refresh tokens
- ✅ CORS configurado
- ✅ Validação de entrada (Pydantic)
- ✅ Rate limiting (opcional)
- ✅ Secrets em variáveis de ambiente
- ✅ Logging de eventos sensíveis
- ✅ HTTPS em produção (Cloud Run)om SSO
---

## 📊 Métricas & Observabilidade
### Logging
```
from loguru import logger

logger.info("✅ Login bem-sucedido", extra={"user": "admin"})
logger.error("❌ Erro ao buscar dados", exc_info=True)
```

### Monitoramento (Cloud Run)
* Logs: Cloud Logging
* Métricas: Cloud Monitoring
* Alertas: Cloud Alerting
---
## 📝 Estrutura do Projeto
```
ecommerce_analytics/
├── src/ecommerce_analytics/
│   ├── api/
│   │   ├── main.py              # FastAPI app
│   │   ├── auth.py              # JWT logic
│   │   └── routes/
│   │       ├── auth.py          # Auth endpoints
│   │       ├── analytics.py      # Analytics endpoints
│   │       ├── forecast.py       # Forecast endpoints
│   │       └── recommendations.py # Recommendations endpoints
│   ├── core/
│   │   ├── config.py            # Settings
│   │   ├── exceptions.py         # Custom exceptions
│   │   └── error_handler.py      # Error handlers
│   ├── services/
│   │   ├── analytics_service.py  # Analytics logic
│   │   ├── forecast_service.py   # Forecast logic
│   │   └── ml_service.py         # ML logic
│   ├── dashboard/
│   │   └── app.py               # Plotly Dash app
│   └── __init__.py
├── tests/
│   ├── unit/
│   │   ├── test_config.py
│   │   └── test_auth.py
│   ├── integration/
│   │   └── test_api.py
│   └── conftest.py
├── .github/workflows/
│   └── ci.yml                   # CI/CD pipeline
├── Dockerfile                    # API container
├── Dockerfile.dash              # Dashboard container
├── docker-compose.yml           # Local development
├── pyproject.toml               # Project config
├── Makefile                     # Commands
└── README.md                    # This file
```
---
## 🎯 Próximos Passos
- [ ] Implementar rate limiting para proteger a API
- [ ] Adicionar webhooks para eventos importantes (ex: novas vendas)
- [ ] Expandir ML models (Prophet, XGBoost) para previsões mais avançadas
- [ ] Implementar cache com Redis para otimizar consultas frequentes
- [ ] Adicionar testes E2E com Playwright para garantir a experiência do usuário
- [ ] Configurar APM (Application Performance Monitoring) para monitorar performance
- [ ] Gerenciamento de usuários e permissões (RBAC) para controle de acesso
- [ ] Integração com ferramentas de visualização de dados (e.g., Looker Studio)
- [ ] Implementar streaming de dados em tempo real (e.g., Pub/Sub)
---

## 👤 Autor: 
### Henrique Botelho Gomes
- 🔗 GitHub: [henriquebotelhogomes](https://github.com/henriquebotelhogomes/)
- 💼 LinkedIn: [henriquebotelhogomes](https://www.linkedin.com/in/henriquebotelhogomes/)
- 📧 Email: [henriquebotelho1@gmail.com](gmailto:henriquebotelho1@gmail.com)
---

## 🙏 Agradecimentos
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Plotly Dash](https://dash.plotly.com/) - Interactive dashboards
- [Google BigQuery](https://cloud.google.com/bigquery) - Data warehouse
- [Pydantic](https://docs.pydantic.dev/latest/) - Data validation
