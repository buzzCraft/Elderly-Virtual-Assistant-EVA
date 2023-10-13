from flask import Flask, abort, request, jsonify
from tempfile import NamedTemporaryFile
import whisper
import torch
import json
import os
import time
import requests
import logging

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_PATH = "models/"
SAVE_PATH = "/text-to-voice-app/"
AUDIO_DIR = "audio_asset"


# app = Flask(__name__)


def model_exists(model_path, filename):
    """Check if the model file exists at the specified path."""
    return os.path.exists(os.path.join(model_path, filename))


def download_and_load_model(model_name, model_path, device):
    """Download the model if not present and load it."""
    if not model_exists(model_path, f"{model_name}.pt"):
        whisper._download(whisper._MODELS[model_name], model_path, False)
    return whisper.load_model(model_name, device=device)


model = download_and_load_model("base", MODEL_PATH, DEVICE)


# @app.route("/")
# def test():
#     return "Our API is Working!"
#
#
# @app.route("/transcribe-service", methods=["POST"])
def transcribe_magic(filename):
    # if not request.files:
    #     abort(400)
    #
    results = []

    # for filename, handle in request.files.items():
    #     with NamedTemporaryFile() as temp:
    #         handle.save(temp.name)
    #         result = model.transcribe(temp.name)
    #         results.append(
    #             {
    #                 "transcript": result["text"],
    #             }
    #         )

    with open(filename, "rb") as file:
        result = model.transcribe(file.name)
        results.append(
            {
                "transcript": result["text"],
            }
        )

    # Notify llama2 to process the transcription
    try:
        response = requests.post(
            "http://llm:5002/generate_response",
            json={"user_input": results[0]["transcript"]},
            timeout=60,  # Set a timeout of 10 seconds
        )

        response.raise_for_status()

        feedback = response.json().get("response", "")

    except requests.Timeout:
        print("Error notifying Llama2: Request timed out")
        feedback = "Error: The request to llama2 timed out"

    except requests.RequestException as e:
        print(f"Error notifying Llama2: {e}")
        feedback = f"Error sending transcription to llama2: {e}"

    except Exception as e:
        # General exception handler for any other unexpected errors
        print(f"Unexpected error: {e}")
        feedback = "An unexpected error occurred"

    # save_transcription(results)

    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    while True:
        files = os.listdir(AUDIO_DIR)
        wav_files = [f for f in files if f.endswith(".wav")]

        if wav_files:  # If there are any .wav files
            for wav_file in wav_files:
                full_path = os.path.join(AUDIO_DIR, wav_file)
                try:
                    # Process the audio file
                    results = transcribe_magic(full_path)

                    # After processing, delete or move the file
                    os.remove(full_path)
                except Exception as e:
                    logging.error(f"Error processing file {wav_file}: {e}")

        else:  # If there are no .wav files
            logging.info("No .wav files found. Waiting for 10 seconds before checking again.")
            time.sleep(10)