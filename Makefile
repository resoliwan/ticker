export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

all: build down up format test

dkbuild:
	docker build -f Dockerfile -t rw/ticker:latest .

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down --remove-orphans

testup:
	docker-compose up -d

test: unit inte e2e

unit:
	poetry run pytest tests/unit

inte:
	poetry run pytest tests/integration

e2e:
	poetry run pytest tests/e2e

logs:
	docker-compose logs --tail=25 api

format: black pylint

black:
	poetry run black -l 88 $$(find * -name '*.py')

pylint:
	poetry run pylint --rcfile pyproject.toml ticker
