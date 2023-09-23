from flask import Flask, jsonify
import sounddevice as sd
import soundfile as sf
import subprocess
import os

app = Flask(__name__)


@app.route("/record_and_transcribe", methods=["POST"])
def record_and_transcribe():
    try:
        fs = 44100  # Sample rate
        seconds = 5  # Duration of recording

        print("Recording...")

        # Record audio
        my_recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished

        print("Recording complete, transcribing...")

        # Save as WAV file
        audio_path = "audio_asset/recorded_audio.wav"
        sf.write(audio_path, my_recording, fs)

        # Run Docker container for transcription
        command = f"docker run --rm -v {os.getcwd()}:/app transcribe python transcribeMain.py --audio {audio_path}"
        subprocess.call(command, shell=True)

        return jsonify({"status": "Transcription complete"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
