# Use the specific PyTorch image with CUDA support
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# Set non-interactive mode for apt-get and update
RUN DEBIAN_FRONTEND=noninteractive apt-get update

# Add NVIDIA's official repository for CUDA and install the required libraries
RUN apt-get install -y wget software-properties-common && \
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin && \
    mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600 && \
    wget https://developer.download.nvidia.com/compute/cuda/11.7.0/local_installers/cuda-repo-ubuntu2004-11-7-local_11.7.0-470.57.02-1_amd64.deb && \
    dpkg -i cuda-repo-ubuntu2004-11-7-local_11.7.0-470.57.02-1_amd64.deb && \
    apt-key add /var/cuda-repo-ubuntu2004-11-7-local/7fa2af80.pub && \
    apt-get update && \
    apt-get -y install cuda-cufft-11-7 cuda-cublas-11-7 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cuda-repo-ubuntu2004-11-7-local

# Install additional required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    portaudio19-dev \
    libsndfile1 \
    apt-utils

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
