# Use the NVIDIA CUDA image
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# Install Python, pip, and other utilities
RUN apt-get update && apt-get install -y python3 python3-pip curl && apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install necessary packages
RUN pip3 install --upgrade pip && \
    pip3 install transformers==4.30 accelerate && \
    pip3 install -i https://test.pypi.org/simple/ bitsandbytes && \
    pip3 install poetry

# Configure poetry to not create a virtual environment and install dependencies
RUN poetry config virtualenvs.create false

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

RUN curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    tee /etc/apt/sources.list.d/nvidia-container-toolkit.list \
  && apt-get update && apt-get install -y nvidia-container-toolkit && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy only the contents of the app directory
COPY app/ ./

EXPOSE 6000

CMD ["python3", "app.py"]
