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

    # Handling transcription
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
            return jsonify({"error": str(e)}), 500
        finally:
            os.remove(audio_filename)

    # Handling response file
    if "response_file" in request.files:
        response_file = request.files["response_file"]
        response_filename = f"response_{unique_id}.wav"
        save_path = os.path.join(app.static_folder, response_filename)
        response_file.save(save_path)
        file_path = f"/static/{response_filename}"

    # Constructing response object
    response_data = {"feedback": feedback}
    if file_path:
        response_data["file_path"] = file_path

    return jsonify(response_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4999)
