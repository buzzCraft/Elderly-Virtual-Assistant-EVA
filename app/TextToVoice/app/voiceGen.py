import os
import time
import logging
import torch
import torchaudio
from flask import Flask, jsonify, request

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

language = "en"
model_id = "v3_en"
speaker = "en_64"  # en_0, en_1, ..., en_117, random
sample_rate = 48000
silero_model, _ = torch.hub.load(
    repo_or_dir="snakers4/silero-models",
    model="silero_tts",
    language=language,
    speaker=model_id,
)

device = "gpu" if torch.cuda.is_available() else "cpu"
silero_model.to(device)  # gpu or cpu

app = Flask(__name__)


def _get_wave(text):
    with torch.no_grad():
        waveform = silero_model.apply_tts(
            text=text, speaker=speaker, sample_rate=sample_rate
        )
    return waveform


@app.route("/generate_voice", methods=["POST"])
def generate_audio():
    logging.info(f"Started processing audio generation request.")
    feedback_text = request.json.get("feedback-text")

    waveform = _get_wave(feedback_text)
    output_filename = f"silero_audio_{int(time.time())}.wav"
    output_path = os.path.join("/text-to-voice-app/", output_filename)
    torchaudio.save(output_path, waveform.unsqueeze(0).cpu(), sample_rate)

    logging.info(f"Finished processing audio. Saved to {output_path}.")
    return jsonify(
        {"status": "success", "audio_path": output_path, "filename": output_filename}
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=False)
