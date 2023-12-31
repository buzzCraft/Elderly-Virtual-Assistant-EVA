import logging
import os
import re
from flask_cors import CORS
import requests
import torch
from dotenv import load_dotenv
from flask import Flask, jsonify, request, session
from flask_session import Session
from model import initialize_model
import warnings

load_dotenv(".env")

warnings.filterwarnings("ignore", category=UserWarning, module="transformers")
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# CONSTANTS
MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"
SAVE_DIRECTORY = "/llm-app/llama_models/"
HF_KEY = os.getenv("HF_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

# Initialize the chatbot
chatbot = initialize_model(MODEL_NAME, HF_KEY, SAVE_DIRECTORY)

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["PERMANENT_SESSION_LIFETIME"] = 3600  # Session expires after 1 hour
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CORS(app, supports_credentials=True)


@app.route("/")
def test():
    return "Our API is Working!"


LOG_FILE_PATH = "/llm-app/chat_logs.txt"
MAX_LOG_ENTRIES: int = 50
username = None


def should_clear_logs():
    with open(LOG_FILE_PATH, "r") as file:
        if len(file.readlines()) > MAX_LOG_ENTRIES:
            return True
    return False


# In your logging function
if should_clear_logs():
    open(LOG_FILE_PATH, "w").close()


def store_log(log_message, log_type):
    # Determine the class based on log type
    log_class = "log-entry " + (
        "user-input" if log_type == "user" else "chatbot-response"
    )

    # Create an HTML string with the appropriate class
    html_log_message = f'<div class="{log_class}"><span class="participant-name">{log_type.title()}:</span> {log_message}</div>'

    # Append log message to a file
    with open(LOG_FILE_PATH, "a") as file:
        file.write(html_log_message + "\n")


@app.route("/save_settings", methods=["POST"])
def save_settings():
    global username
    data = request.json
    username = data.get("userName")
    session["userName"] = data.get("userName")
    session["userHobbies"] = data.get("userHobbies")
    session["selectedLanguage"] = data.get("selectedLanguage")
    session.modified = True
    logging.info(
        f"Received settings - Name: {session['userName']}, Hobbies: {session['userHobbies']}, Language: {session['selectedLanguage']}"
    )

    return jsonify({"status": "Settings saved successfully"})


@app.route("/generate_response", methods=["POST"])
def generate_response():
    # Get the user name from the session
    global username
    user_name = username
    logging.info(f"Received user name: {user_name}")

    try:
        # Get the request data
        user_input = request.json.get("user_input")
        logging.info(f"Received transcription: {user_input}")
        store_log(f"{user_input}", user_name)

        if not user_input:
            return jsonify({"error": "Empty user input"})

        # Generate the response
        response = chatbot(user_input)
        chatbot_response = response.get("text", "")
        chatbot_response = re.sub(
            r"\*.*?\*", "", chatbot_response
        )  # Remove the *emphasis*
        if ":" in chatbot_response:
            response_parts = chatbot_response.split(":")
            processed_response = [resp.strip() for resp in response_parts[1:]]
            chatbot_response = " ".join(processed_response)
        else:
            chatbot_response = chatbot_response.strip()
        if not chatbot_response:
            chatbot_response = "Sorry, I didn't understand that."

        logging.info(f"Generated response: {chatbot_response}")
        store_log(f"{chatbot_response}", "Eva")

        # Notify voiceGen of the response
        voice_response = requests.post(
            "http://texttovoice:5003/generate_voice",
            json={"feedback-text": chatbot_response},
        )
        voice_status = voice_response.json().get("status", "")

        return jsonify({"response": chatbot_response, "voice_status": voice_status})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/get_chat_logs")
def get_chat_logs():
    try:
        with open(LOG_FILE_PATH, "r") as file:
            log_entries = file.readlines()
    except FileNotFoundError:
        log_entries = []

    return jsonify("".join(log_entries[-100:]))  # Send HTML logs as a single string


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
