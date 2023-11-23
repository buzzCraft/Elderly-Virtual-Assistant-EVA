from flask import Flask, jsonify, request
import subprocess
import logging
import os
import glob
import requests
import uuid

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

app = Flask(__name__)

IMG_PATH = "/SadTalker/photos/eva.png"
RESULT_DIR = "/SadTalker/results"
CLIENT_RECEIVE_ENDPOINT = (
    "http://record:4999/process_audio"  # Endpoint to send the video
)


def get_latest_video(result_dir):
    video_files = glob.glob(os.path.join(result_dir, "*.mp4"))
    if not video_files:
        return None
    return max(video_files, key=os.path.getmtime)


@app.route("/receive_voice", methods=["POST"])
def run_inference():
    if "VoiceFile" not in request.files:
        return jsonify({"error": "VoiceFile not provided"}), 400

    feedback_voice = request.files["VoiceFile"]
    temp_voice_path = f"/tmp/{str(uuid.uuid4())}.wav"  # Generate a unique filename
    feedback_voice.save(temp_voice_path)

    logging.info(f"Processing image: {IMG_PATH}")
    logging.info(f"Using audio: {temp_voice_path}")

    subprocess.run(
        [
            "python3.8",
            "inference.py",
            "--driven_audio",
            temp_voice_path,
            "--source_image",
            IMG_PATH,
            "--result_dir",
            RESULT_DIR,
        ]
    )
    logging.info("Inference completed")

    # Get the latest generated video
    latest_video_path = get_latest_video(RESULT_DIR)
    if latest_video_path:
        # Send the video file to the client's receive_response endpoint
        try:
            with open(latest_video_path, "rb") as video_file:
                files = {"video_data": video_file}
                response = requests.post(
                    CLIENT_RECEIVE_ENDPOINT, files=files, timeout=60
                )
                response.raise_for_status()
                logging.info(f"Sent video to client successfully.")
        except requests.RequestException as e:
            logging.error(f"Error occurred while sending video to client: {e}")
            return jsonify({"error": str(e)}), 500

    os.remove(temp_voice_path)  # Clean up the temporary file
    return jsonify({"message": "Inference and video sending completed"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=False)
