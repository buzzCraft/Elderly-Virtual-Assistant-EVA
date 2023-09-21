import os
import torch
from torch import cuda
from transformers import (
    pipeline,
    LlamaTokenizer,
    LlamaForCausalLM,
)
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
from langchain.llms import HuggingFacePipeline
from langchain.schema import SystemMessage
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

# Initialize cuda
device = torch.device("cuda" if cuda.is_available() else "cpu")

# Authorization token
hf_auth = "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"

# Model name
model_name = "meta-llama/Llama-2-7b-chat-hf"
save_directory = "./llama_models"


def load_from_hf(model_name, hf_auth):
    tokenizer = LlamaTokenizer.from_pretrained(
        model_name, use_auth_token=hf_auth, legacy=False, return_tensors="pt"
    )
    model = LlamaForCausalLM.from_pretrained(
        model_name, use_auth_token=hf_auth, load_in_8bit=True
    )
    return tokenizer, model


def save_to_local(tokenizer, model, save_dir):
    model.save_pretrained(save_dir)
    tokenizer.save_pretrained(save_dir)


def load_from_local(save_dir):
    tokenizer = LlamaTokenizer.from_pretrained(
        save_dir, return_tensors="pt", legacy=False
    )
    model = LlamaForCausalLM.from_pretrained(save_dir, load_in_8bit=True)
    return tokenizer, model


if not os.path.exists(save_directory):
    # Load model and tokenizer from Hugging Face and then save locally
    tokenizer, model = load_from_hf(model_name, hf_auth)
    save_to_local(tokenizer, model, save_directory)
else:
    # Load model and tokenizer from the local directory
    tokenizer, model = load_from_local(save_directory)

# Initialize the pipeline
llm_pipeline = pipeline(
    task="text-generation",
    model=model,
    tokenizer=tokenizer,
    return_full_text=True,
    max_new_tokens=10,
    repetition_penalty=1.2,
)

llm = HuggingFacePipeline(pipeline=llm_pipeline)

# Define the prompt
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="You are a assistant to an elderly person."),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{human_input}"),
    ]
)

# Define the memory
memory = ConversationBufferWindowMemory(
    k=3,
    return_messages=True,
    memory_key="chat_history",
)

# Define the chain
chain = LLMChain(llm=llm, prompt=prompt, memory=memory, verbose=True)
