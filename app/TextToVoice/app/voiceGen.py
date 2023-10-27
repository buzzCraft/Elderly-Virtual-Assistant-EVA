import logging
import os
import time
import torch
import warnings
import requests
import nltk
import numpy as np
import torchaudio
from flask import Flask, jsonify, request
from omegaconf import OmegaConf

nltk.download("punkt")
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

app = Flask(__name__)

# Initialize Silero model
language = "en"
model_id = "v3_en"
speaker = "en_64"
sample_rate = 48000
silero_model, _ = torch.hub.load(
    repo_or_dir="snakers4/silero-models",
    model="silero_tts",
    language=language,
    speaker=model_id,
)
device = "cpu"
silero_model.to(device)


def _get_wave(text):
    with torch.no_grad():
        waveform = silero_model.apply_tts(
            text=text, speaker=speaker, sample_rate=sample_rate
        )
    return waveform


def remove_old_files():
    """Remove old audio files from the current directory."""
    current_directory = "/text-to-voice-app/"
    files = os.listdir(current_directory)
    for file in files:
        if file.endswith(".wav"):
            file_path = os.path.join(current_directory, file)
            os.remove(file_path)
            logging.info(f"Deleted old file: {file_path}")


@app.route("/generate_voice", methods=["POST"])
def generate_audio():
    logging.info(f"Started processing audio generation request.")
    remove_old_files()
    feedback_text = request.json.get("feedback-text")
    waveform = _get_wave(feedback_text)
    output_filename = f"silero_audio_{int(time.time())}.wav"
    output_path = os.path.join("/text-to-voice-app/", output_filename)
    torchaudio.save(output_path, waveform.unsqueeze(0).cpu(), sample_rate)

    # Notify VideoGen of the response
    try:
        with open(output_path, "rb") as f:
            files = {"VoiceFile": (output_filename, f)}
            video_response = requests.post(
                "http://voicetovideo:5005/receive_voice", files=files
            )
            video_status = video_response.json().get("status", "")
        logging.info(f"VideoGen status: {video_status}")
    except Exception as e:
        logging.error(f"Error occurred while sending audio to VideoGen: {e}")

    logging.info(f"Finished processing audio. Saved to {output_path}.")
    return jsonify(
        {"status": "success", "audio_path": output_path, "filename": output_filename}
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=False)
