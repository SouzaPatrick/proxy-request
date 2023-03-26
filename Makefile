## @ Pre-commit
.PHONY: format
format: ## Format all code files
	@pre-commit run --all-files


## @ Start project
.PHONY: install reset_db

install: reset_db## Create/Reset the database

reset_db:
	@python generate_db.py

## @ Commands proxy
.PHONY: proxy console update test
proxy: ## Download lists of public proxies
	@python main.py

console: ## List all valid proxies
	@python console.py

update: ## Revalidate valid proxies
	@python update.py

test: ## Run tests
	@pytest --cov-report term-missing --cov=app tests/

.PHONY: help
help:
	python help.py
