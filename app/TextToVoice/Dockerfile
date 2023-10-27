# Use the specific PyTorch image with CUDA support
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# Set non-interactive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Update and install system packages
RUN apt-get update -q && apt-get install -yq \
    python3-pip \
    portaudio19-dev \
    libsndfile1 \
    apt-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip, install PyTorch libraries and poetry
RUN pip install --upgrade pip && \
    pip install torchaudio && \
    pip install poetry

# Set the working directory in the container
WORKDIR /app

# Copy the required files for poetry and install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy the app contents
COPY app/ ./

# Expose the specified port
EXPOSE 5003
