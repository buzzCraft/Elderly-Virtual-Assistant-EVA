from flask import Flask, render_template, request, jsonify
import requests
import uuid
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


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
            "http://transcribe:5003/receive_audio",
            files=files,
            timeout=60,  # Set a timeout of 60 seconds
        )
        response.raise_for_status()
        feedback = response.json().get("response", "")
    except requests.Timeout:
        logging.info("Error: Request to v2t timed out")
        feedback = "Error: The request to v2t timed out"
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        feedback = f"Error: {e}"

    return jsonify({"feedback": feedback})


@app.route("/receive_response", methods=["POST"])
def receive_response():
    if "response_file" not in request.files:
        return jsonify({"error": "No response file received"})

    response_file = request.files["response_file"]
    unique_id = str(uuid.uuid4())
    response_filename = f"response_{unique_id}.wav"
    response_file.save(response_filename)

    return jsonify(
        {
            "status": "success",
            "message": f"Received and saved response file as {response_filename}",
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4999)
