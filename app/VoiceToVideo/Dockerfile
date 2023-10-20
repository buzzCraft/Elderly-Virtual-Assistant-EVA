# Use an official Python runtime as the base image
FROM python:3.8-slim-buster

# Set the maintainer label
LABEL maintainer="jacksonherberts@gmail.com"

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    ffmpeg \
    git \
    && apt-get clean

# Clone the SadTalker repository
RUN git clone https://github.com/Winfredy/SadTalker /VoiceToVideo-app

# Set the working directory
WORKDIR /VoiceToVideo-app
COPY . /VoiceToVideo-app

# Install Python dependencies
RUN pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
RUN pip install -r requirements.txt

RUN apt-get install -y wget

# Download pre-trained models
RUN bash scripts/download_models.sh

# Expose any ports the app is expecting in the environment
# If the application runs on a specific port, expose it. For example:
EXPOSE 5005

# Define the command to run on container start
CMD ["python3.8", "main.py"]
