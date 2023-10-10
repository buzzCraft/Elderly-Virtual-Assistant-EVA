# Use the Python 3.10 image
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04
RUN pip install transformers==4.30
RUN pip install accelerate
RUN pip install -i https://test.pypi.org/simple/ bitsandbytes

# Install the latest version of poetry
RUN pip install --upgrade pip && \
    pip install poetry


# Set the working directory
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create a virtual environment and install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy only the contents of the app directory
COPY app/ ./

EXPOSE 6000

CMD ["python", "app.py"]