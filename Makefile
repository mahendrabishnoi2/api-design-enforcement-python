.PHONY: install dev lint format test api-lint serve build clean help

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	uv sync

dev: ## Install development dependencies
	uv sync --all-extras

lint: ## Run code linting
	uv run ruff check .
	uv run black --check .

format: ## Format code
	uv run ruff check --fix .
	uv run black .

test: ## Run tests
	uv run pytest -v

serve: ## Start development server
	uv run uvicorn main:app --reload

build: ## Build and validate application
	uv run python -c "import main; print('✓ Application builds successfully')"

api-lint: ## Lint API design with Spectral
	@echo "Installing Spectral if not present..."
	@npm list -g @stoplight/spectral-cli || npm install -g @stoplight/spectral-cli
	@echo "Killing any existing uvicorn processes..."
	@pkill -f "uvicorn main:app" || true
	@sleep 1
	@echo "Starting FastAPI server on port 8001..."
	@uv run uvicorn main:app --host 0.0.0.0 --port 8001 &
	@sleep 3
	@echo "Generating OpenAPI spec..."
	@curl -s -o openapi.json http://localhost:8001/openapi.json || (echo "Failed to get OpenAPI spec" && pkill -f "uvicorn main:app" && exit 1)
	@echo "Running Spectral API linting..."
	@npx @stoplight/spectral-cli lint openapi.json --format stylish || true
	@pkill -f "uvicorn main:app" || true
	@rm -f openapi.json

clean: ## Clean up generated files
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -f openapi.json
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

ci: dev lint test build api-lint ## Run all CI checks locally