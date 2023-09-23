import os
import whisper
import json
from helpers import InvalidAudioFormatError, TranscriptionError


# Function to hold the magic
def transcribe_magic(audio_file):
    # The user recording will be saved as a .wav file with name audio.wav in the audio_asset folder
    script_dir = os.path.dirname(os.path.realpath(__file__))
    audio_file = os.path.join(script_dir, "audio_asset", "audio.wav")

    if not audio_file.lower().endswith(".wav"):
        raise InvalidAudioFormatError("Audio file must be a .wav file")

    try:
        model = whisper.load_model("base.en")
        output = model.transcribe(audio_file)
        transcription = output["text"]
        # return output["text"]
        # Save the transcription to a JSON file
        with open(os.path.join(script_dir, "transcription.json"), "w") as json_file:
            json.dump({"transcription": transcription}, json_file)

    except Exception as e:
        raise TranscriptionError(f"There was an error transcribing the audio file: {e}")
