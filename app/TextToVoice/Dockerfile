# Use the specific PyTorch image with CUDA support
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime
#FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y python3-pip && \
    pip3 install torch torchaudio

# Set non-interactive mode for apt-get, update and install necessary packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    portaudio19-dev \
    libsndfile1 \
    apt-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y libcufft11 libcublas11 && apt-get clean

# Upgrade pip and install poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Set the working directory in the container
WORKDIR /app

# Copy the required files for poetry
COPY pyproject.toml poetry.lock ./

# Configure poetry settings and install the dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy the app contents
COPY app/ ./

# Expose the specified port
EXPOSE 5003
