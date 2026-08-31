.PHONY: install test lint run demo-eval docker-build

install:
	uv sync

test:
	uv run pytest

lint:
	uv run ruff check .

run:
	uv run uvicorn app.main:app --reload --port 8080

demo-eval:
	uv run python -m app.cli evaluate

docker-build:
	docker build -t groundtruth:local .

