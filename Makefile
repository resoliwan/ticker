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

local_test: unit inte e2e

unit:
	poetry run pytest tests/unit

inte:
	poetry run pytest tests/integration

e2e:
	poetry run pytest tests/e2e

logs:
	docker-compose logs --tail=25 api

format: black pylint

test: up
	docker-compose run --rm --no-deps --entrypoint='poetry run pytest' ticker /tests/unit /tests/integration /tests/e2e

unit-tests:
	docker-compose run --rm --no-deps --entrypoint='poetry run pytest' ticker /tests/unit

integration-tests: up
	docker-compose run --rm --no-deps --entrypoint='poetry run pytest' ticker /tests/integration

e2e-tests: up
	docker-compose run --rm --no-deps --entrypoint='poetry run pytest' ticker /tests/e2e

acceptance-tests: up
	docker-compose run --rm --no-deps --entrypoint='poetry run pytest' ticker /tests/acceptance

black:
	poetry run black -l 88 $$(find * -name '*.py')

pylint:
	poetry run pylint --rcfile pyproject.toml ticker
