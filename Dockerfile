# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the seamless_communication-main directory to the container
COPY seamless_communication-main /app/seamless_communication-main

# Install the required dependencies
RUN pip install -r /app/seamless_communication-main/requirements.txt && \
pip install --extra-index-url https://test.pypi.org/simple/ fairseq2==0.1.0rc0
# Set the default command to run the m4t_predict script
CMD ["python", "/app/seamless_communication-main/m4t_predict", "english_speech.wav", "s2tt", "eng", "--src_lang", "eng"]