# Use the Python 3.10 image
# If CUDA is needed, go for this image
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# Install the latest version of poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Set the working directory
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Copy only the contents of the app directory
COPY app/ ./

# Configure poetry to not create a virtual environment and install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev