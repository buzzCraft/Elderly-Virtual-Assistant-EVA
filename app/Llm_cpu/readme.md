
Downloading and running Llama-2 7b-gguf on Windows OS without gpu:

Pre-requirements:
-docker on your desktop

- Navigatto the empty folder llama.cpp/model:

cd llama.cpp/model

- So run the following command:

wget 'https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q2_K.gguf'



1. Using Docker:
To run this model, all you need is to run the docker file by this three commands:

docker build -t llm_img .

docker run -d -p 5000:5000 --name llm_con llm_img 


docker exec -it llm_con python3 client.py

Then you are ready to interect with the model using the terminal for now.



..............................................................

2. Without docker:

However, if there are some challanges related to docker you can set up  the model on you local mchine without running docker but following the following steps:

I used vscode/powershell.

1-
Mkdir llm
Install miniconda on you pc (remember to cross over  C++ and  add path as a variable environement )


git clone https://github.com/ggerganov/llama.cpp


Git clone https://huggingface.co/substratusai/Llama-2-7B-chat-GGUF
cd llama.cpp


install make (https://github.com/skeeto/w64devkit/releases) inside this terminal, navigate to folder “llm > llama.cpp ”
So run “make”   

Pip install wget

Cd llama.cpp 

“Go to the cloned repo and copy the full path of  a gguf-file for ex. Q2_K.gguf
, the smallest version of llama-7b.”

Back to llama.cpp
Mkdir model


Cd model

Wget <paste the full path which looks like: C:\Users\majdi\llm\Llama-2-7b-Chat-GGUF\llama-2-7b-chat.Q2_K.gguf >

Cd ..


In the terminal within llama.cpp run:

./main -t 12 -m C:\Users\majdi\llm\llama.cpp\model\model.q2_k.gguf --color -c 4096 --temp 0.7 --repeat_penalty 1.1 -n -1 -p "<s>[INST] <<SYS>> you are a friendly assistant for older people. <</SYS>> i’m feeling bored, and body would like to spend time with me. </s>"

( Remember to change 12 to the number of cores on you pc)




