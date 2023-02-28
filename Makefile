## @ Pre-commit
.PHONY: format
format:
	@pre-commit run --all-files


## @ Commands
.PHONY: download-proxies console update
download-proxies:
	@python main.py

console:
	@python console.py

update:
	@python update.py
