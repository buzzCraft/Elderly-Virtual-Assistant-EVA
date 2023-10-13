from flask import Flask, jsonify
import os

app = Flask(__name__)

AUDIO_DIR = os.getcwd()

@app.route('/check_audio', methods=['GET'])
def check_audio():
    # Check if there's any .wav file in the directory
    audio_files = [f for f in os.listdir(AUDIO_DIR) if f.endswith('.wav')]
    if audio_files:
        # If there's a .wav file, return its name and available status
        return jsonify({"available": True, "filename": audio_files[0]})
    else:
        return jsonify({"available": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)
