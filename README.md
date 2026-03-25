# E-commerce Analytics

Solução completa de análise de e-commerce com BigQuery, FastAPI e Plotly Dash.

## 🚀 Quick Start

### Pré-requisitos
- Python 3.12+
- Windows PowerShell ou Linux/Mac bash
- Conta Google Cloud com BigQuery habilitado

### Instalação
```bash
# 1. Clonar repositório
cd ecommerce-analytics

# 2. Criar venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate     # Linux/Mac

# 3. Instalar dependências
pip install -e ".[dev]"

# 4. Configurar autenticação GCP
gcloud auth application-default login

# 5. Criar arquivo .env
cp .env.example .env
```

## Executar
```
# API
make run-api
# Acesse: http://localhost:8000/docs

# Dashboard
make run-dashboard
# Acesse: http://localhost:8050
```

## Testes
```
make test
```

## 📚 Documentação
* API: http://localhost:8000/docs
* Dashboard: http://localhost:8050

## 🔐 Credenciais Demo
* Username: admin
* Password: admin123
---
## 🎯 Guia de Execução (Windows PowerShell)
```
# 1. Navegar até o projeto
cd C:\Users\henri\OneDrive\Documents\python_projects\ecommerce_analytics

# 2. Ativar venv
.\.venv\Scripts\Activate.ps1

# 3. Instalar dependências
pip install -e ".[dev]"

# 4. Executar testes
pytest tests/ -v

# 5. Executar API
uvicorn src.ecommerce_analytics.api.main:app --host 0.0.0.0 --port 8000 --reload

# 6. Em outro terminal, executar Dashboard
python -m src.ecommerce_analytics.dashboard.app
```
---
## ✅ Checklist
* [ ] Criei estrutura de pastas 
* [ ] Copiei todos os arquivos
* [ ] Executei pip install -e ".[dev]"
* [ ] Executei pytest tests/ -v
* [ ] Executei uvicorn src.ecommerce_analytics.api.main:app --reload
* [ ] Acessei http://localhost:8000/docs