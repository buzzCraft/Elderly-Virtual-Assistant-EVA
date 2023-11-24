from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import uuid
import logging
import os
import atexit

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


def delete_response_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".wav") and filename.startswith("response_"):
            os.remove(os.path.join(directory, filename))


app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)
delete_response_files(app.static_folder)


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


def get_latest_video_path(directory):
    latest_video = None
    latest_mod_time = 0

    for filename in os.listdir(directory):
        if filename.endswith(".mp4") and filename.startswith("response_"):
            file_path = os.path.join(directory, filename)
            mod_time = os.path.getmtime(file_path)
            if mod_time > latest_mod_time:
                latest_mod_time = mod_time
                latest_video = filename

    return f"/static/{latest_video}" if latest_video else None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process_audio", methods=["POST", "GET"])
def process_media():
    unique_id = str(uuid.uuid4())

    # POST request: handle incoming media
    if request.method == "POST":
        feedback = None

        # Handle audio data
        if "audio_data" in request.files:
            audio_file = request.files["audio_data"]
            audio_filename = f"response_{unique_id}.wav"
            audio_file.save(os.path.join(app.static_folder, audio_filename))
            feedback = "Audio processed."

        # Handle video data
        if "video_data" in request.files:
            video_file = request.files["video_data"]
            video_filename = f"response_video_{unique_id}.mp4"
            video_file.save(os.path.join(app.static_folder, video_filename))
            feedback = "Video processed."

        return jsonify(
            {
                "feedback": feedback,
                "file_path": f"/static/{audio_filename if 'audio_data' in request.files else video_filename}",
            }
        )

    # GET request: check for latest video
    if request.method == "GET":
        latest_video_path = get_latest_video_path(app.static_folder)
        if latest_video_path:
            return jsonify({"file_path": latest_video_path})
        else:
            return jsonify({"error": "No video available"}), 404


if __name__ == "__main__":
    atexit.register(delete_response_files, app.static_folder)
    app.run(host="0.0.0.0", port=4999)
