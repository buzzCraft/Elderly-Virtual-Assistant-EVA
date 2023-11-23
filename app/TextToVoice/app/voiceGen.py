import logging
import os
import torch
import requests
import torchaudio
from flask import Flask, jsonify, request
import uuid
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="torch.hub")
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

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
device = "cuda" if torch.cuda.is_available() else "cpu"
silero_model.to(device)

CLIENT_RECEIVE_ENDPOINT = "http://record:4999/process_audio"


def _get_wave(text):
    with torch.no_grad():
        waveform = silero_model.apply_tts(
            text=text, speaker=speaker, sample_rate=sample_rate
        )
    return waveform


def remove_old_files():
    current_directory = "/text-to-voice-app/"
    files = os.listdir(current_directory)
    for file in files:
        if file.endswith(".wav"):
            file_path = os.path.join(current_directory, file)
            os.remove(file_path)
            logging.info(f"Deleted old file: {file_path}")


def generate_unique_filename(extension=".wav"):
    unique_id = str(uuid.uuid4())
    return f"{unique_id}{extension}"


@app.route("/generate_voice", methods=["POST"])
def generate_audio():
    logging.info("Started processing audio generation request.")
    remove_old_files()

    feedback_text = request.json.get("feedback-text")
    waveform = _get_wave(feedback_text)
    unique_output_filename = generate_unique_filename()
    output_path = os.path.join("/text-to-voice-app/", unique_output_filename)
    torchaudio.save(output_path, waveform.unsqueeze(0).cpu(), sample_rate)
    video_generator = False
    if video_generator:
        # """
        try:
            with open(output_path, "rb") as f:
                files = {"VoiceFile": (unique_output_filename, f)}
                video_response = requests.post(
                    "http://voicetovideo:5005/receive_voice", files=files
                )
                video_status = video_response.json().get("status", "")
            logging.info(f"VideoGen status: {video_status}")
        except Exception as e:
            logging.error(f"Error occurred while sending audio to VideoGen: {e}")
    # """
    else:
        try:
            with open(output_path, "rb") as audio_file:
                files = {"response_file": audio_file}
                response = requests.post(
                    CLIENT_RECEIVE_ENDPOINT, files=files, timeout=60
                )
                response.raise_for_status()
                logging.info(f"Sent {unique_output_filename} to client successfully.")
        except requests.RequestException as e:
            logging.error(f"Error occurred while sending audio to client: {e}")

    return jsonify(
        {
            "status": "success",
            "audio_path": output_path,
            "filename": unique_output_filename,
        }
    )


if __name__ == "__main__":
    remove_old_files()
    app.run(host="0.0.0.0", port=5003, debug=False)
