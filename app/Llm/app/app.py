import os
import random
from flask import Flask, request, jsonify
from model import initialize_model
import torch
from dotenv import load_dotenv
import requests
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


def is_acceptable_question(response):
    # List of acceptable questions that EVA can ask
    acceptable_questions = [
        "Do you need more assistance?",
        "Is there anything else I can help with?",
        "Would you like more information on this topic?",
    ]
    return response in acceptable_questions


def get_default_response():
    return random.choice(DEFAULT_RESPONSES)


def respond_to_input(user_input):
    if chatbot:
        response = chatbot(user_input).get("text", "").strip()

        # Check if the response is a question and if it's acceptable
        if response.endswith("?") and not is_acceptable_question(response):
            response = (
                "I'm here to assist you. Please let me know how I can help further."
            )

        # If the response is empty or doesn't make sense, use a default response
        if not response:
            response = get_default_response()

        return response
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
