FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y portaudio19-dev libsndfile1 apt-utils


RUN pip install --upgrade pip && \
    pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY app/ ./


EXPOSE 5001