from flask import Flask, render_template, request, jsonify
import requests
import uuid
import logging
import os

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


def save_response_audio(response_file):
    unique_id = str(uuid.uuid4())
    response_filename = f"response_{unique_id}.wav"
    save_path = os.path.join(app.static_folder, response_filename)
    response_file.save(save_path)
    logging.info(f"Saved file size: {os.path.getsize(save_path)} bytes")
    return f"/static/{response_filename}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process_audio", methods=["POST"])
def process_audio():
    if "audio_data" not in request.files:
        return jsonify({"error": "No audio file received"})

    audio_file = request.files["audio_data"]
    unique_id = str(uuid.uuid4())
    audio_filename = f"{unique_id}.wav"
    audio_file.save(audio_filename)

    # Send audio file to the specified server endpoint
    files = {"audio_data": open(audio_filename, "rb")}
    try:
        response = requests.post(
            "http://transcribe:5000/receive_audio",
            files=files,
            timeout=60,  # Set a timeout of 60 seconds
        )
        response.raise_for_status()
        feedback = response.json().get("response", "")
    except requests.Timeout:
        logging.info("Error: Request to v2t timed out")
        feedback = "Error: The request to v2t timed out"
    except requests.RequestExceptiona as e:
        logging.error(f"Request failed: {e}")
        feedback = f"Error: {e}"

    if "response_file" in request.files:
        response_file = request.files["response_file"]
        file_path = save_response_audio(response_file)
        logging.info(f"Received response file saved as: {response_file.filename}")
        logging.info(f"Sending file path to client: {file_path}")

        return jsonify(
            {"status": "success", "message": "File received", "file_path": file_path}
        )

    return jsonify({"feedback": feedback})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4999)
