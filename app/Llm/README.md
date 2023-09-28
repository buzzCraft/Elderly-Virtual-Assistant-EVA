# LLM

Setting up docker image, and running llm docker container.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installing CUDA Toolkit](#installing-cuda-toolkit)
- [Installing NVIDIA Container Toolkit](#installing-nvidia-container-toolkit)
- [Docker Commands](#docker-commands)
  - [Building the Docker Image](#building-the-docker-image)
  - [Running the Docker Container](#running-the-docker-container)

## Prerequisites

- A CUDA-capable GPU is required.
- Ensure you have Docker installed on your machine. If not, you can install it by following the instructions from the [official Docker documentation](https://docs.docker.com/get-docker/).

## Installing CUDA Toolkit

1. Visit the [CUDA Toolkit download page](https://developer.nvidia.com/cuda-downloads).
2. Follow the instructions on the website to download and install the CUDA Toolkit for your system.
3. Reboot your system after installation is complete.
4. Verify the installation by running the following command in your terminal:
   ```bash
   nvcc --version
   ```

## Installing NVIDIA Container Toolkit

1. Visit the [NVIDIA Container Toolkit download page](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) for installation instructions.
2. Follow the instructions to install the NVIDIA Container Toolkit.

## Docker Commands

### Building the Docker Image

To build your Docker image, navigate to the directory containing your `Dockerfile` and run:

```bash
docker build -t LLM:latest .
```

### Running the Docker Container

To run your Docker container with published ports and utilizing the GPU, use the following command:

```bash
docker run --rm --gpus all -p 5000:5000 LLM:latest
```

---

End of README example.

---