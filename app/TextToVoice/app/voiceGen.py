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

processor = AutoProcessor.from_pretrained("suno/bark-small")
model = BarkModel.from_pretrained("suno/bark-small")

voice_preset = "v2/en_speaker_1"

inputs = processor(
    text,
    voice_preset=voice_preset,

)

audio_array = model.generate(**inputs)
audio_array = audio_array.cpu().numpy().squeeze()
# sample_rate = model.generation_config.sample_rate

save_dr = "/text-to-voice-app/"
output_path = os.path.join(save_dr, f"outaudio{time.time()}.wav")
sf.write(output_path, audio_array, 22050, "PCM_24")
