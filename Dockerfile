FROM python:3.10-slim-buster
RUN pip install poetry

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml
RUN poetry install --no-root --no-dev

RUN mkdir -p /ticker
COPY ticker/ /ticker/
RUN poetry install --no-dev
COPY tests/ /tests/

WORKDIR /