.PHONY: test format lint clean

run:
	python main.py

visualize:
	python main.py --mode visualize

scrape:
	python main.py --mode scrape

test:
	python -m pytest tests

format:
	ruff format .

lint:
	ruff check . --fix

lint-unsafe-fix:
	ruff check . --fix --unsafe-fixes

all: format lint test
