from transcribeMagic import transcribe_magic
from flask import Flask, request, jsonify, abort
import sounddevice as sd
import soundfile as sf
import subprocess
import json
import os

app = Flask(__name__)


@app.route("/record", methods=["POST"])
def record():
    try:
        fs = 44100
        seconds = 5
        print("Please talk ...")
        sd.default.device = 1
        my_recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        print("Thank you ...")

        record_path = "audio.wav"
        sf.write(record_path, my_recording, fs)

        # Run the command container for the whisper AI model
        command = f"docker run --rm -v {os.getcwd()}:/app transcribe python transcribeMain.py --audio {record_path}"
        subprocess.call(command, shell=True)

        # Read the generated JSON file
        with open("transcription.json", "r") as json_file:
            result = json.load(json_file)

        return jsonify(result)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
