.PHONY: help clean

.DEFAULT_GOAL := help

help: ## 显示帮助信息
	@echo "Manage commands"
	@echo ""
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean: ## 清理运行产物
	@echo "Cleaning..."
	@rm -rf .ruff_cache .pytest_cache
	@find . -path .venv -prune -o -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*.egg-info' -exec rm -rf {} +
	@find . -type f -name '.DS_Store' -delete
	@find . -type f -name 'uv.lock' -delete
	@echo "Cleaning completed!"
