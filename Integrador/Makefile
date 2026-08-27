install:
    poetry install

format:
    poetry run ruff format .
    poetry run ruff check . --fix

lint:
    poetry run ruff check .
    poetry run mypy src

test:
    poetry run pytest

security:
    poetry run pip-audit

run:
    poetry run uvicorn orders_service.main:app --reload

db-up:
    docker compose up -d db

db-down:
    docker compose down

docker-up:
    docker compose up --build -d

docker-down:
    docker compose down
