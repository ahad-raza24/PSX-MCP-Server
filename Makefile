# PSX MCP Server Makefile

.PHONY: help install install-dev test test-cov lint format clean run-server run-demo run-examples build docs

help:  ## Show this help message
	@echo "PSX MCP Server - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package in development mode
	pip install -e .

install-dev:  ## Install development dependencies
	pip install -e ".[dev,test]"

test:  ## Run tests
	python -m pytest tests/ -v

test-cov:  ## Run tests with coverage
	python -m pytest tests/ -v --cov=src/psx_mcp --cov-report=html --cov-report=term

lint:  ## Run linting
	flake8 src/ tests/ examples/ scripts/

format:  ## Format code with black
	black src/ tests/ examples/ scripts/ --line-length 88

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run-server:  ## Start the MCP server
	python scripts/start_server.py

run-demo:  ## Run the demo
	python examples/demo_mcp_server.py

run-examples:  ## Run all examples
	python examples/demo_mcp_server.py
	python examples/demo_new_tools.py
	python examples/demo_simple_names.py

build:  ## Build the package
	python setup.py sdist bdist_wheel

docs:  ## Generate documentation
	@echo "Documentation is available in docs/ directory"
	@echo "API documentation: docs/API.md"

setup: install-dev  ## Setup development environment
	@echo "Development environment setup complete!"
	@echo "Run 'make test' to verify installation"
