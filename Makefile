.PHONY: help install test lint format type-check quality run-api run-dashboard clean

help:
	@echo "E-Commerce Analytics - Available Commands"
	@echo "=========================================="
	@echo "make install          - Install dependencies"
	@echo "make test             - Run tests"
	@echo "make lint             - Run ruff linter"
	@echo "make format           - Format code with black"
	@echo "make type-check       - Run mypy type checking"
	@echo "make quality          - Run all quality checks"
	@echo "make run-api          - Run FastAPI server"
	@echo "make run-dashboard    - Run Plotly Dash dashboard"
	@echo "make clean            - Clean cache files"

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=src/ecommerce_analytics --cov-report=html

lint:
	ruff check src/ tests/ --fix

format:
	black src/ tests/

type-check:
	mypy src/

quality: lint format type-check test
	@echo "✅ All quality checks passed!"

run-api:
	uvicorn src.ecommerce_analytics.api.main:app --host 0.0.0.0 --port 8000 --reload

run-dashboard:
	python -m src.ecommerce_analytics.dashboard.app

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cache cleaned!"