DOCS_DIR = docs/
DOCS_BUILD_DIR = docs/build/html/
DOCS_PORT = 3000

.PHONY: test docs clean-docs check-style help

test: ## Run tests.
	pytest

docs: ## Build and serve the documentation.
	sphinx-autobuild --port $(DOCS_PORT) $(DOCS_DIR) $(DOCS_BUILD_DIR)

clean-docs: ## Clean up documentation files generated by the build process.
	rm -rf $(DOCS_DIR)/api-reference/*.rst $(DOCS_BUILD_DIR)

check-style: ## Check and format package style.
	pre-commit run --all-files

help: ## Show this help message and exit.
	@echo "usage: make <target>\n"
	@echo "targets:"
	@egrep '^[a-zA-Z_-]+:.*##.*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*##"}; {printf "  %-16s%s\n", $$1, $$2}'
