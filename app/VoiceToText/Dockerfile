# Use the Python 3.10 image
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y portaudio19-dev libsndfile1 apt-utils


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

EXPOSE 5000
#CMD ["python", "/app/transcribemagic.py"]

CMD ["python", "/app/transcribeApp.py"]
