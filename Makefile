## @ Pre-commit
.PHONY: format
format: ## Format all code files
	@pre-commit run --all-files


## @ Start project
.PHONY: install
install: ## Create/Reset the database
	@python generate_db.py

## @ Commands
.PHONY: proxy console update
proxy: ## Download lists of public proxies
	@python main.py

console: ## List all valid proxies
	@python console.py

update: ## Revalidate valid proxies
	@python update.py

test: ## Run tests
	@pytest -v

.PHONY: help
help:
	python help.py
