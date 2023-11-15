import logging
import os
import re

import requests
import torch
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from model import initialize_model

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
        response = chatbot(user_input)
        chatbot_response = response.get("text", "")
        chatbot_response = re.sub(
            r"^\w+EVA:\s*", "", chatbot_response
        )  # Remove the EVA prefix
        chatbot_response = re.sub(
            r"\*.*?\*", "", chatbot_response
        )  # Remove the *emphasis*
        chatbot_response = re.sub(
            r"[^A-Za-z .]", "", chatbot_response
        )  # Remove all non-alphabetical characters
        chatbot_response = (
            chatbot_response.strip()
        )  # Remove leading and trailing whitespace
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
    app.run(host="0.0.0.0", port=5002, debug=False)
