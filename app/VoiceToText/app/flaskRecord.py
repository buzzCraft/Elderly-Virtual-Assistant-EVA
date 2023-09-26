from flask import Flask, jsonify, request
import os
import requests
import librosa

# TODO: RENAME THE FILE TO FLASKRECORDED.PY FOR CLARITY
app = Flask(__name__)

print("Starting flaskRecord.py...")


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/recorded_file", methods=["POST"])
def record_and_transcribe():
    audio_file = request.files.get("audio")
    if not audio_file:
        return jsonify({"error": "No audio file provided"}), 400

    audio_path = "audio_asset/recorded_audio.wav"
    audio_file.save(audio_path)

    # Process the audio file into numpy array using librosa
    try:
        audio_data, _ = librosa.load(audio_path, sr=None)
    except Exception as e:
        return jsonify({"error": f"Failed to process audio file: {e}"}), 500

    # Make an HTTP request to the transcribe service

    response = requests.post(
        "http://transcribe:5000/transcribe", json={"audio_data": audio_data.tolist()}
    )

    if response.status_code != 200:
        return (
            jsonify(
                {
                    "error": f"Transcribe service returned {response.status_code}: {response.text}"
                }
            ),
            500,
        )

    try:
        transcription = response.json().get("transcription")
        return jsonify(
            {"status": "Transcription complete", "transcription": transcription}
        )
    except requests.exceptions.JSONDecodeError:
        return jsonify({"error": "Failed to decode JSON from transcribe service"}), 500


print("Starting Flask server...")
app.run(host="0.0.0.0", port=6000, debug=True)
