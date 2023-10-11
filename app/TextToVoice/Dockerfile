# Use the specific PyTorch image with CUDA support
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# Set non-interactive mode for apt-get, update and install necessary packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    portaudio19-dev \
    libsndfile1 \
    apt-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

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
