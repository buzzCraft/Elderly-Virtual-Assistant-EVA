from flask import Flask, jsonify, request
import subprocess
import logging
import os
import glob

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

app = Flask(__name__)

IMG_PATH = "/sadTalker/photos/face.png"
RESULT_DIR = "/VoiceToVideo-app"


@app.route("/receive_voice", methods=["POST"])
def run_inference():
    if "VoiceFile" not in request.files:
        return jsonify({"error": "VoiceFile not provided"}), 400

    feedback_voice = request.files["VoiceFile"]
    temp_voice_path = os.path.join(
        "/tmp", feedback_voice.filename
    )  # Use the original filename
    feedback_voice.save(temp_voice_path)

    logging.info(f"Processing image: {IMG_PATH}")
    logging.info(f"Using audio: {temp_voice_path}")

    subprocess.run(
        [
            "python3.8",
            "inference.py",
            "--driven_audio",
            temp_voice_path,  # Use the temporary voice file path
            "--source_image",
            IMG_PATH,
            "--result_dir",
            RESULT_DIR,
            "--still",
            "--preprocess",
            "full",
            "--enhancer",
            "gfpgan",
        ]
    )
    logging.info()
    os.remove(temp_voice_path)  # Clean up the temporary file
    return jsonify({"message": "Inference completed"}), 200


def get_latest_video(result_dir):
    video_files = glob.glob(os.path.join(result_dir, "*.mp4"))
    if not video_files:
        return None
    latest_video = max(video_files, key=os.path.getmtime)
    return latest_video


if __name__ == "__main__":
    previous_video_path = get_latest_video(RESULT_DIR)
    if previous_video_path:
        logging.info(
            f"Using persistent avatar from previous video: {previous_video_path}"
        )
    else:
        logging.info("No previous video found. Generating a new avatar.")
    app.run(host="0.0.0.0", port=5005, debug=False)
