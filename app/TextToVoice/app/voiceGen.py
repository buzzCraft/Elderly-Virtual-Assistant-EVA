import json
import os
import time
import subprocess
import torch
from transformers import AutoProcessor, BarkModel
import soundfile as sf
from flask import Flask, request, jsonify
import logging
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

device = "cuda" if torch.cuda.is_available() else "cpu"
app = Flask(__name__)


def load_transcription_from_file(file_path):
    """Load and return transcription from a JSON file."""
    with open(file_path, "r") as json_file:
        transcription = json.load(json_file)
    return transcription["results"][0]["transcript"]


def get_model_and_processor(model_name, model_path):
    """Retrieve the model and processor. If not available locally, download them."""
    if not os.path.exists(os.path.join(model_path, "config.json")):
        # Download and save model and processor if they don't exist locally
        processor = AutoProcessor.from_pretrained(model_name)
        model = BarkModel.from_pretrained(model_name)
        processor.save_pretrained(model_path)
        model.save_pretrained(model_path)
    else:
        # Load model and processor from local directory
        processor = AutoProcessor.from_pretrained(model_path)
        model = BarkModel.from_pretrained(model_path).to(device)
    return model, processor


def generate_audio_from_text(model, processor, text, voice_preset):
    """Generate audio from the given text."""
    inputs = processor(text, voice_preset=voice_preset)
    audio_array = model.generate(**inputs)
    return audio_array.cpu().numpy().squeeze()


@app.route("/generate_voice", methods=["POST"])
def generate_audio():
    logging.info(f"Started processing audio generation request.")

    feedback_text = request.json.get("feedback-text")
    # Constants and paths
    # TRANSCRIPTION_FILE = "/text-to-voice-app/transcription.json"
    MODEL_NAME = "suno/bark-small"
    MODEL_PATH = "/text-to-voice-app/models/"
    SAVE_DIR = "/text-to-voice-app/"
    VOICE_PRESET = "v2/en_speaker_6"
    SAMPLE_RATE = 22050

    # Get model and processor
    model, processor = get_model_and_processor(MODEL_NAME, MODEL_PATH)

    # Generate audio from text
    audio_array = generate_audio_from_text(
        model, processor, feedback_text, VOICE_PRESET
    )

    # Save the generated audio
    # output_path = os.path.join(SAVE_DIR, f"barkaudio{time.time()}.wav")
    output_filename = f"bark_audio_{int(time.time())}.wav"
    output_path = os.path.join(SAVE_DIR, output_filename)

    sf.write(output_path, audio_array, SAMPLE_RATE, "PCM_24")
    print(f"Audio saved to {output_path}")
    time.sleep(1)  # Ensure the file is completely written

    logging.info(f"Finished processing audio. Saved to {output_path}.")
    return jsonify(
        {"status": "success", "audio_path": output_path, "filename": output_filename}
    )


if __name__ == "__main__":
    current_directory = "/text-to-voice-app/"

    # List all files in the current directory
    files = os.listdir(current_directory)

    # Filter files with .wav extension and delete them
    for file in files:
        if file.endswith(".wav"):
            file_path = os.path.join(current_directory, file)
            os.remove(file_path)
            print(f"Deleted: {file_path}")

    logging.info(f"Deletion of .wav files in the current directory complete.")

    app.run(host="0.0.0.0", port=5003, debug=True)
