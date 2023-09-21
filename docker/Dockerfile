FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install poetry and dependencies
RUN curl -sSL https://install.python-poetry.org | python3 -

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev

COPY . .
