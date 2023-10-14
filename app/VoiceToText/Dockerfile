# Use the specific PyTorch image with CUDA support
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# Set non-interactive mode for apt-get and update packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    portaudio19-dev \
    libsndfile1 \
    apt-utils

# Install the latest version of pip and poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Set the working directory in the container
WORKDIR /app

# Copy the required files for poetry
COPY pyproject.toml poetry.lock ./

# Copy the app contents
COPY app/ ./

# Configure poetry settings and install the dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

# Expose the specified port
EXPOSE 5000

# Command to run the application
CMD ["python", "/app/transcribeApp.py"]
