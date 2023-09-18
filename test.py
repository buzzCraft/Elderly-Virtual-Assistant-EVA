import torch
from torch import cuda
from transformers import (
    StoppingCriteriaList,
    pipeline,
    LlamaTokenizer,
    LlamaForCausalLM,
)
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain, LLMChain
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import StoppingCriteria
import gradio as gr
import os

# Initialize cuda
device = torch.device("cuda" if cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Authorization token
hf_auth = "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"

# Model name
model_name = "meta-llama/Llama-2-7b-chat-hf"

# Define a directory to save the model and tokenizer
save_directory = "./llama_model"

if not os.path.exists(save_directory):
    # Load model and tokenizer from Hugging Face and then save locally
    tokenizer = LlamaTokenizer.from_pretrained(
        model_name, use_auth_token=hf_auth, legacy=False, return_tensors="pt"
    )
    model = LlamaForCausalLM.from_pretrained(
        model_name, use_auth_token=hf_auth, load_in_8bit=True
    )

    # Save model and tokenizer
    model.save_pretrained(save_directory)
    tokenizer.save_pretrained(save_directory)
else:
    # Load model and tokenizer from the local directory
    tokenizer = LlamaTokenizer.from_pretrained(save_directory)
    model = LlamaForCausalLM.from_pretrained(save_directory)

stop_list = ["\nHuman:", "\n```\n"]
stop_token_ids = [tokenizer(x)["input_ids"] for x in stop_list]
stop_token_ids = [torch.LongTensor(x).to(device) for x in stop_token_ids]


class StopOnTokens(StoppingCriteria):
    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs
    ) -> bool:
        for stop_ids in stop_token_ids:
            if torch.eq(input_ids[0][-len(stop_ids) :], stop_ids).all():
                return True
        return False


# Define stopping criteria
stopping_criteria = StoppingCriteriaList([StopOnTokens()])

# Initialize pipeline
hf_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    return_full_text=True,
    max_new_tokens=100,
    repetition_penalty=1.5,
    stopping_criteria=stopping_criteria,
)

llm = HuggingFacePipeline(pipeline=hf_pipeline)

# Prompt
template = """You are a chatbot having a conversation with an elderly person. Talk like a normal person.

{chat_history}
Human: {human_input}
Chatbot:"""
prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"], template=template
)

# Initialize memory
memory = ConversationBufferWindowMemory(
    k=3, return_messages=True, memory_key="chat_history"
)

# Initialize conversation chain
chain = LLMChain(llm=llm, memory=memory, verbose=False, prompt=prompt)

global_display_history = ""
def chatbot_response(human_input, chat_history=""):
    global global_display_history
    response = chain.predict(human_input=human_input, chat_history=chat_history)
    global_display_history += f"Human: {human_input}\nChatbot: {response}\n\n"
    return global_display_history


# Custom CSS for styling
styles = """
    .gr-textbox {
        width: 100%;
        height: 100px;  # Adjusted height for the input box
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ccc;
        font-size: 16px;
    }
    .gr-textbox-output {
        width: 100%;
        height: 300px;  # Adjusted height for the output box
        background-color: #f7f7f7;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
        overflow-y: scroll;
    }
    .gr-interface {
        max-width: 600px;
        margin: auto;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        overflow: hidden;
    }
"""

# Define Gradio interface
iface = gr.Interface(
    fn=chatbot_response,
    inputs=gr.inputs.Textbox(lines=3, placeholder="Type your message here..."),
    outputs=gr.outputs.Textbox(label="Chat History"),
    live=False,
    title="Chatbot Assistant",
    description="ARE YOU LONELY? CHAT 'ERE.",
    css=styles,
    theme="huggingface",
    layout="vertical"  # Stack the boxes vertically
)

iface.launch()