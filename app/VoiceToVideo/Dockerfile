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

# Clone the SadTalker repository into a temporary directory
RUN git clone https://github.com/OpenTalker/SadTalker /tmp/SadTalker

# Set the working directory
WORKDIR /VoiceToVideo-app

# Move the cloned repository contents into the working directory
RUN mv /tmp/SadTalker/* /tmp/SadTalker/.[!.]* .
COPY app/videoGen.py /VoiceToVideo-app/
COPY app/photos /VoiceToVideo-app/photos/

# Install Python dependencies
RUN pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
RUN pip install -r requirements.txt
RUN pip install Flask

RUN apt-get install -y wget

# Download pre-trained models
RUN bash scripts/download_models.sh

# Expose the required port
EXPOSE 5005

# Define the command to run on container start
CMD ["python3.8", "videoGen.py"]
