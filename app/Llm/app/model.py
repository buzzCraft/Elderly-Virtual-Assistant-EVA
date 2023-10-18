import os
import random
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


def load_from_hf(model_name, hf_auth):
    tokenizer = LlamaTokenizer.from_pretrained(
        model_name, use_auth_token=hf_auth, legacy=False, return_tensors="pt"
    )
    model = LlamaForCausalLM.from_pretrained(
        model_name, use_auth_token=hf_auth  # , load_in_8bit=True
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


# Load the model
def load_model(model_name, hf_auth, save_directory):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory, exist_ok=True)

        # Load model and tokenizer from Hugging Face and then save locally
        print("Downloading model from Hugging Face")
        tokenizer, model = load_from_hf(model_name, hf_auth)
        save_to_local(tokenizer, model, save_directory)
    else:
        # Load model and tokenizer from the local directory
        tokenizer, model = load_from_local(save_directory)
    return tokenizer, model


# Initialize the pipeline
def initialize_pipeline(model, tokenizer):
    llm_pipeline = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        return_full_text=True,
        max_new_tokens=100,
        repetition_penalty=1.2,
    )
    return HuggingFacePipeline(pipeline=llm_pipeline)


# Define the prompt
def define_prompt():
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="You are EVA, a friendly assistant to old people. Answer with no more than two sentences."
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{human_input}"),
        ]
    )
    return prompt


# Define the memory
def define_memory():
    memory = ConversationBufferWindowMemory(
        k=3,
        return_messages=True,
        memory_key="chat_history",
    )
    return memory


# Define the chain
def define_chain(llm, prompt, memory):
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
    )
    return chain


# Define the chatbot
def initialize_model(model_name, hf_auth, save_directory):
    tokenizer, model = load_model(model_name, hf_auth, save_directory)
    llm = initialize_pipeline(model, tokenizer)
    prompt = define_prompt()
    memory = define_memory()
    chain = define_chain(llm, prompt, memory)
    return chain
