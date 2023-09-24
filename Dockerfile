FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    git \
    git-lfs \
    wget \
    curl \
    # python build dependencies \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    # gradio dependencies \
    ffmpeg \
    # fairseq2 dependencies \
    libsndfile-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:${PATH}
WORKDIR ${HOME}/app

RUN curl https://pyenv.run | bash
ENV PATH=${HOME}/.pyenv/shims:${HOME}/.pyenv/bin:${PATH}
ARG PYTHON_VERSION=3.10.12
RUN pyenv install ${PYTHON_VERSION} && \
    pyenv global ${PYTHON_VERSION} && \
    pyenv rehash && \
    pip install --no-cache-dir -U pip setuptools wheel

RUN pip install --no-cache-dir torch==2.0.1 gradio==3.40.1 && \
    pip install --extra-index-url https://test.pypi.org/simple/ fairseq2==0.1.0rc0
# Set the working directory to /app
WORKDIR /app

# Copy the seamless_communication-main directory to the container
COPY seamless_communication-main /app/seamless_communication-main
USER root
RUN chown -R user:user /app/seamless_communication-main
USER user
# Install the required dependencies
#RUN pip install -r /app/seamless_communication-main/requirements.txt
WORKDIR /app/seamless_communication-main
RUN pip install --user .
# Set the default command to run the m4t_predict script
CMD ["python", "/app/seamless_communication-main/scripts/m4t/predict/predict.py", "english_speech.wav", "s2tt", "eng", "--src_lang", "eng"]

