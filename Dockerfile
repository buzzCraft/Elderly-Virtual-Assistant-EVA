FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip libsndfile1 git

RUN git clone https://github.com/facebookresearch/seamless_communication.git
#RUN cd seamless_communication

WORKDIR seamless_communication

#RUN pip3 install fairseq2
RUN pip3 install -r requirements.txt
RUN pip3 install .