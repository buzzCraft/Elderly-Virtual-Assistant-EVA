from ctransformers import AutoModelForCausalLM
from ctransformers.pipeline import pipeline

# Set up the model and its settings
# Set up the model pathp
model_path = "llama-2-7b-chat.Q2_K.gguf"

# Load the model and configure it directly
llm = AutoModelForCausalLM.from_pretrained(
    model_path,
    gpu_layers=0,  # Use 0 for CPU
    temperature=0.7
   
)

# Load the model
llm = AutoModelForCausalLM.from_pretrained(
    model_path, model_type="llama"
)
# Set up the pipeline
chat_pipeline = pipeline(
    "text-generation",
    model=llm,
    tokenizer=None,  # Replace with the path to your tokenizer
)
# Define your prompt
prompt = "You: Hi, Llama! Tell me a joke."

# Generate a response
response = chat_pipeline(prompt)

# Print the response
print(response)