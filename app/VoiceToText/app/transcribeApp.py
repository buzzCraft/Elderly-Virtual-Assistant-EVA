import logging
import os
import requests
import torch
import whisper
from flask import Flask, request, jsonify

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_PATH = "models/"
SAVE_PATH = "/text-to-voice-app/"

app = Flask(__name__)


def model_exists(model_path, filename):
    """Check if the model file exists at the specified path."""
    return os.path.exists(os.path.join(model_path, filename))


def download_and_load_model(model_name, model_path, device):
    """Download the model if not present and load it."""
    if not model_exists(model_path, f"{model_name}.pt"):
        whisper._download(whisper._MODELS[model_name], model_path, False)
    return whisper.load_model(model_name, device=device)


model = download_and_load_model("base", MODEL_PATH, DEVICE)


def transcribe_magic(file_path):
    results = []

    result = model.transcribe(file_path)
    results.append(
        {
            "transcript": result["text"],
        }
    )
    logging.info(f"Transcribed file")

    # Notify Llama2 to process the transcription
    try:
        response = requests.post(
            "http://llm:5002/generate_response",
            json={"user_input": results[0]["transcript"]},
            timeout=60,  # Set a timeout of 60 seconds
        )

        response.raise_for_status()
        feedback = response.json().get("response", "")

    except requests.Timeout:
        logging.info("Error notifying Llama2: Request timed out")
        feedback = "Error: The request to llama2 timed out"

    except requests.RequestException as e:
        logging.info(f"Error notifying Llama2: {e}")
        feedback = f"Error sending transcription to llama2: {e}"

    return results, feedback


@app.route("/receive_audio", methods=["POST"])
def receive_audio():
    if "audio_data" not in request.files:
        return jsonify({"error": "No audio file received"}), 400

    audio_file = request.files["audio_data"]
    temp_filepath = os.path.join(SAVE_PATH, audio_file.filename)
    audio_file.save(temp_filepath)  # Save the file temporarily

    # process the audio file
    results, feedback = transcribe_magic(temp_filepath)
    os.remove(temp_filepath)  # Delete the temporary file
    return jsonify({"transcription": results, "feedback": feedback})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
