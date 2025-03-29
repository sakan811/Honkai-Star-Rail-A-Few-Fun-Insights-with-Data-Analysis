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

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -name '.coverage' -delete
	find . -name '.pytest_cache' -exec rm -rf {} +

all: format lint test
