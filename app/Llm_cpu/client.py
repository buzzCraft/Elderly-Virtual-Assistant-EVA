import requests
import json
import time
# from langchain import *
# from langchain.prompts import PromptTemplate
# from langchain.agents import Agent


def create_prompt_template(template):
    """Creates a PromptTemplate instance from a template string.

    Args:
      template: A string containing the prompt template.

    Returns:
      A PromptTemplate instance.
    """

    return PromptTemplate(template=template, input_variables=[])

# template = create_prompt_template("Hello, I'm your friendly assistant. How can I help you today?")
# agent = Agent(template)
# memory = Memory(3)


url = "http://127.0.0.1:5000/generate"
while True:
    # template = template("Hello, I'm your friendly assistant. How can I help you today?")
    
    prompt = input("You: ")
    data = {
        "instruction": "You are a friendly assistant to old people. Answer with no more than two sentences.",
        "prompt": prompt
    }

    start_time = time.time()


    response = requests.post(url, json=data)

    end_time = time.time()

    # Calculate the difference
    dif = end_time - start_time

    if response.status_code == 200 and response.text:
        try:
            res = response.json()
            generated_text = res['response']
            print(f"Assistent: {generated_text} {dif:.2f} sec)")

        except json.decoder.JSONDecodeError:
            print("Error: Received an invalid JSON response from the server.")
            
    else:
        print("Error: Did not receive a valid response from the server.")
