# Use the Python 3.10 image
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# Install the latest version of poetry
RUN pip install --upgrade pip && \
    pip install poetry


# Set the working directory
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create a virtual environment and install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev && \
    pip install flask-cors

# Copy only the contents of the app directory
COPY app/ ./

EXPOSE 5002

CMD ["python", "app.py"]
