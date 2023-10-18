import os
from flask import Flask, request, jsonify
from model import initialize_model
import torch
from dotenv import load_dotenv
import requests
import time
import logging

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

load_dotenv(".env")

# CONSTANTS
MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"
SAVE_DIRECTORY = "/llm-app/llama_models/"
HF_KEY = os.getenv("HF_KEY")

# Initialize the chatbot
chatbot = initialize_model(MODEL_NAME, HF_KEY, SAVE_DIRECTORY)

# Default responses for unclear input
DEFAULT_RESPONSES = [
    "I'm sorry, I didn't quite understand that. Could you please rephrase or provide more details?",
    "I apologize for the confusion. Can you clarify what you meant?",
    "I'm here to help, but I'm not sure about your request. Can you provide more context or rephrase it?",
    "I'm not certain about your query. Can you explain it a bit more?",
]


def get_default_response():
    return random.choice(DEFAULT_RESPONSES)


def respond_to_input(user_input):
    if chatbot:
        response = chatbot(user_input)
        return response.get("text", "")
    else:
        return get_default_response()


# Initialize the Flask app
app = Flask(__name__)


@app.route("/")
def test():
    return "Our API is Working!"


@app.route("/generate_response", methods=["POST"])
def generate_response():
    try:
        # Get the request data
        user_input = request.json.get("user_input")
        logging.info(f"Received transcription: {user_input}")

        # Check if the user input is empty
        if not user_input:
            return jsonify({"error": "Empty user input"})

        # Generate the response
        chatbot_response = respond_to_input(user_input)
        logging.info(f"Generated response: {chatbot_response}")

        # Notify voiceGen of the response
        voice_response = requests.post(
            "http://texttovoice:5003/generate_voice",
            json={"feedback-text": chatbot_response},
        )
        voice_status = voice_response.json().get("status", "")

        # Return the response
        return jsonify({"response": chatbot_response, "voice_status": voice_status})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
