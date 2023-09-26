FROM python:3.10-slim

RUN pip install --upgrade pip && \
    pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY app/ ./


EXPOSE 5001