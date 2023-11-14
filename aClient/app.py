from flask import Flask, render_template, request, jsonify
import requests
import uuid
import logging
import os

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process_audio", methods=["POST"])
def process_audio():
    unique_id = str(uuid.uuid4())
    file_path = None
    feedback = None

    # Handle initial audio data for transcription
    if "audio_data" in request.files:
        audio_file = request.files["audio_data"]
        audio_filename = f"{unique_id}_transcript.wav"
        audio_file.save(audio_filename)

        # Send audio file to transcription service and get feedback
        try:
            transcription_response = requests.post(
                "http://transcribe:5000/receive_audio",
                files={"audio_data": open(audio_filename, "rb")},
                timeout=60,
            )
            transcription_response.raise_for_status()
            feedback = transcription_response.json().get("response", "")
        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500

    # Handle response file (if included)
    if "response_file" in request.files:
        response_file = request.files["response_file"]
        response_filename = f"response_{unique_id}.wav"
        save_path = os.path.join(app.static_folder, response_filename)
        response_file.save(save_path)
        file_path = f"/static/{response_filename}"
        logging.info(f"Saved response file to {save_path}")
        logging.info(f"Response file path: {file_path}")
    return jsonify({"feedback": feedback, "file_path": file_path})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4999)
