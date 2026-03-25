.PHONY: help install dev test lint format clean run-api run-dashboard

help:
	@echo "📚 Comandos disponíveis:"
	@echo "  make install        - Instala dependências"
	@echo "  make dev            - Instala dependências de desenvolvimento"
	@echo "  make test           - Executa testes"
	@echo "  make lint           - Verifica código (ruff + mypy)"
	@echo "  make format         - Formata código (black + ruff)"
	@echo "  make clean          - Remove arquivos temporários"
	@echo "  make run-api        - Executa FastAPI"
	@echo "  make run-dashboard  - Executa Plotly Dash"
	@echo "  make setup-bq       - Cria tabelas otimizadas no BigQuery"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=src --cov-report=html

lint:
	ruff check src/ tests/
	mypy src/

format:
	black src/ tests/ scripts/
	ruff check --fix src/ tests/ scripts/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov

run-api:
	uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

run-dashboard:
	python -m src.dashboard.app

setup-bq:
	python scripts/create_bigquery_tables.py

all: clean install dev lint test