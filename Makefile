.PHONY: setup install format lint type-check test deadcode yamllint check clean help

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Run interactive setup wizard
	@bash scripts/setup.sh

install: ## Install dependencies
	uv sync --all-extras

format: ## Format code with ruff and yamlfix
	uv run ruff format .
	uv run yamlfix --exclude .venv .

lint: ## Lint code with ruff
	uv run ruff check .

type-check: ## Type check with ty
	uv run ty check .

test: ## Run tests with pytest
	uv run pytest

deadcode: ## Check for dead code with vulture
	uv run vulture src/ --min-confidence 80

yamllint: ## Lint YAML files with yamllint
	uv run yamllint .

check: format lint type-check test deadcode yamllint ## Run all checks

clean: ## Clean up generated files
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
