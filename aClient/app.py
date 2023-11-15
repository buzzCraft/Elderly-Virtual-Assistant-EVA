from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import uuid
import logging
import os

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)


def get_latest_file_path(directory):
    latest_file = None
    latest_mod_time = 0

    for filename in os.listdir(directory):
        if filename.endswith(".wav") and "response_" in filename:
            file_path = os.path.join(directory, filename)
            mod_time = os.path.getmtime(file_path)
            if mod_time > latest_mod_time:
                latest_mod_time = mod_time
                latest_file = filename

    return f"/static/{latest_file}" if latest_file else None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process_audio", methods=["POST"])
def process_audio():
    unique_id = str(uuid.uuid4())
    feedback = None

    if "audio_data" in request.files:
        audio_file = request.files["audio_data"]
        audio_filename = f"{unique_id}_transcript.wav"
        audio_file.save(audio_filename)

        try:
            with open(audio_filename, "rb") as audio_data:
                transcription_response = requests.post(
                    "http://transcribe:5000/receive_audio",
                    files={"audio_data": audio_data},
                    timeout=60,
                )
                transcription_response.raise_for_status()
            feedback = transcription_response.json().get("response", "")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error in transcription request: {e}")
            os.remove(audio_filename)  # Cleanup if error occurs
            return jsonify({"error": str(e)}), 500

        os.remove(audio_filename)  # Cleanup after successful transcription

    if "response_file" in request.files:
        response_file = request.files["response_file"]
        response_filename = f"response_{unique_id}.wav"
        save_path = os.path.join(app.static_folder, response_filename)
        response_file.save(save_path)

    # Get the latest file path from the static folder
    file_path = get_latest_file_path(app.static_folder)

    response_data = {"feedback": feedback, "file_path": file_path}
    logging.info(f"Response data: {response_data}")
    return jsonify(response_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4999)
