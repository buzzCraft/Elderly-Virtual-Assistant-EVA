import json
import os
import time
import torch
from transformers import AutoProcessor, BarkModel
import soundfile as sf


device = "cuda" if torch.cuda.is_available() else "cpu"


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


def save_audio_to_file(audio_array, sample_rate, directory):
    """Save the generated audio to a WAV file."""
    output_path = os.path.join(directory, f"outaudio{time.time()}.wav")
    sf.write(output_path, audio_array, sample_rate, "PCM_24")
    return output_path


def main():
    # Constants and paths
    TRANSCRIPTION_FILE = "/text-to-voice-app/transcription.json"
    MODEL_NAME = "suno/bark-small"
    MODEL_PATH = "models/"
    SAVE_DIR = "/text-to-voice-app/"
    VOICE_PRESET = "v2/en_speaker_1"
    SAMPLE_RATE = 22050

    # Extract text from transcription
    text = load_transcription_from_file(TRANSCRIPTION_FILE)
    print(f"Processing text: {text}")

    # Get model and processor
    model, processor = get_model_and_processor(MODEL_NAME, MODEL_PATH)

    # Generate audio from text
    audio_array = generate_audio_from_text(model, processor, text, VOICE_PRESET)

    # Save the generated audio
    output_path = save_audio_to_file(audio_array, SAMPLE_RATE, SAVE_DIR)
    print(f"Audio saved to {output_path}")


if __name__ == "__main__":
    main()
