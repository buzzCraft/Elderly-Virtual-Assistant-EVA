# Write dockerfile for the client
FROM python:3.10-alpine

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install poetry

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

EXPOSE 4999

CMD ["python", "app.py"]
