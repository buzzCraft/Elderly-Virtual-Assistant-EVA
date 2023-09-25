from transformers import AutoProcessor, BarkModel
import soundfile as sf

processor = AutoProcessor.from_pretrained("suno/bark-small")
model = BarkModel.from_pretrained("suno/bark-small")

voice_preset = "v2/en_speaker_6"

inputs = processor(
    "[music] Hello, are you ready for a standup today [laugh] [woman]",
    voice_preset=voice_preset,
)

audio_array = model.generate(**inputs)
audio_array = audio_array.cpu().numpy().squeeze()


sf.write("test.wav", audio_array, 22050, "PCM_24")
