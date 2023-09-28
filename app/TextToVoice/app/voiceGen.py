import json
from transformers import AutoProcessor, BarkModel
import soundfile as sf
import os
import time

with open("/text-to-voice-app/transcription.json", "r") as json_file:
    transcription = json.load(json_file)

# Extract text from transcription json file
text = transcription["results"][0]["transcript"]
print(f"Processing text: {text}")

model_path = ".models/"
model_name = "suno/bark-small"

# Check if the model exists locally
if not os.path.exists(os.path.join(model_path, "config.json")):
    # If not, download and save
    processor = AutoProcessor.from_pretrained(model_name)
    model = BarkModel.from_pretrained(model_name)
    processor.save_pretrained(model_path)
    model.save_pretrained(model_path)
else:
    # If yes, load from the local directory
    processor = AutoProcessor.from_pretrained(model_path)
    model = BarkModel.from_pretrained(model_path)

voice_preset = "v2/en_speaker_1"

inputs = processor(
    "text",
    voice_preset=voice_preset,
)

audio_array = model.generate(**inputs)
audio_array = audio_array.cpu().numpy().squeeze()
# sample_rate = model.generation_config.sample_rate

save_dr = "/text-to-voice-app/"
output_path = os.path.join(save_dr, f"outaudio{time.time()}.wav")
sf.write(output_path, audio_array, 22050, "PCM_24")
