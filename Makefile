.PHONY: test format lint clean

run:
	python main.py

visualize:
	curl http://localhost:1234/visualize

scrape:
	curl http://localhost:1234/scrape

test:
	python -m pytest tests

format:
	ruff format .

lint:
	ruff check . --fix

lint-unsafe-fix:
	ruff check . --fix --unsafe-fixes

pre-ci: format lint test
