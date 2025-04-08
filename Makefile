.PHONY: test format lint clean image-remove

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

compose-up-build:
	docker compose -f docker-compose.build.yml up -d --build

compose-up:
	docker compose up -d

compose-down:
	docker compose down

image-remove:
	docker rmi sakanbeer88/hsr-data-analyzer:latest

compose-clean:
	docker compose down --volumes --remove-orphans
