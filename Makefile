.PHONY: run test lint format migrate docker-up docker-down

run:
	uvicorn app.main:app --reload

test:
	pytest tests/

lint:
	flake8 app tests
	mypy app tests

format:
	black app tests
	isort app tests

migrate:
	alembic upgrade head

docker-up:
	docker-compose -f docker/docker-compose.yml up -d --build

docker-down:
	docker-compose -f docker/docker-compose.yml down
