from flask import Flask, request, jsonify
import numpy as np
import whisper
import json
import soundfile as sf
from helpers import InvalidAudioFormatError, TranscriptionError

app = Flask(__name__)


@app.route("/")
def welcome():
    return "Welcome to the Transcription Service!"


# Temporary path to save audio from numpy array
TMP_AUDIO_PATH = "tmp_audio.wav"


# Function to hold the magic
def transcribe_magic(np_audio_data):
    save_path = "/text-to-voice-app/transcription.json"

    # Convert the numpy array to float32
    np_audio_data = np_audio_data.astype(np.float32)

    try:
        model = whisper.load_model("base.en")
        output = model.transcribe(np_audio_data)
        transcription = output["text"]

        with open(save_path, "w") as json_file:
            json.dump({"transcription": transcription}, json_file)

        return transcription

    except Exception as e:
        raise TranscriptionError(f"There was an error transcribing the audio file: {e}")


@app.route("/transcribe", methods=["POST"])
def transcribe_endpoint():
    audio_data = request.json.get("audio_data")
    if audio_data is None:
        return jsonify({"error": "No audio data provided"}), 400

    np_audio_data = np.array(audio_data)

    try:
        transcription = transcribe_magic(np_audio_data)
        return jsonify({"transcription": transcription})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Using port 5000 for the transcribe service
