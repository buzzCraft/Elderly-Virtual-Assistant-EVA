import os
from flask import Flask, request, jsonify
from model import initialize_model
import torch
from dotenv import load_dotenv
import requests
import time
import logging
logging.basicConfig(level=logging.INFO)


# def wait_for_flag():
#     while not os.path.exists("/llm-app/transcription_done.flag"):
#         time.sleep(10)  # Sleep for 10 seconds before checking again


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

        # Check if the user input is empty
        if not user_input:
            return jsonify({"error": "Empty user input"})

        # Wait for the transcription to be done
       # wait_for_flag()
        # Generate the response
        response = chatbot(user_input)
        chatbot_response = response.get("text", "")
        logging.info(f"Generated response: {chatbot_response}")

        #os.remove("/llm-app/transcription_done.flag")

        # Flag done processing
        # with open("/llm-app/llm_done.flag", "w") as flag_file:
        #     flag_file.write("done")

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
