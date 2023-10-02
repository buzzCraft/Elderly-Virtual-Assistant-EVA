FROM ubuntu:latest

WORKDIR /app


LABEL description="Please clone the model 'llama-2-7b-chat.Q2_K.gguf'on your local machine (inside llama/model) before running the image"

# Create the model directory
RUN mkdir -p /app/model/

#copy the model from the local folder to the working dir.
COPY llama/model/llama-2-7b-chat.Q2_K.gguf /app/model/llama-2-7b-chat.Q2_K.gguf

#Altarnative: install the model from huggingface
#RUN wget https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q2_K.gguf -O /app/model/llama-2-7b.Q2_K.gguf


# Install wget
RUN apt-get update && apt-get install -y wget



# Install Python
RUN apt-get update && apt-get install -y python3-pip


COPY requirements.txt .
COPY server.py .
COPY client.py .
COPY llama/main.exe .

# Install Wine and its dependencies ( allowing to run Windows applications on Linux-based system)
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y wine64 wine32 wine-binfmt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV WINEARCH win64
ENV WINEPREFIX /root/.wine64
RUN winecfg

RUN pip3 install --no-cache-dir -r requirements.txt --default-timeout=100


RUN chmod +x main.exe

EXPOSE 5000

CMD ["python3", "server.py"]


#docker build --cache-from llm_img .
#docker build  --build-arg TIMEOUT=100 -t llm_img .

#docker run -d -p 5000:5000 --name llm_con llm_img 


#docker exec -it llm_con python3 client.py


