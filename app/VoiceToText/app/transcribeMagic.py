import os
import whisper
import json
from helpers import InvalidAudioFormatError, TranscriptionError


# Function to hold the magic
def transcribe_magic(audio_file):
    # The user recording will be saved as a .wav file with name audio.wav in the audio_asset folder
    save_path = "/app/transcription.json"

    if not audio_file.lower().endswith(".wav"):
        raise InvalidAudioFormatError("Audio file must be a .wav file")

    try:
        model = whisper.load_model("base.en")
        output = model.transcribe(audio_file)
        transcription = output["text"]
        # return output["text"]

        with open(save_path, "w") as json_file:
            json.dump({"transcription": transcription}, json_file)

    except Exception as e:
        raise TranscriptionError(f"There was an error transcribing the audio file: {e}")




# TODO: SAVE THE CACHED MODEL IN THE DOCKER CONTAINER, download the model if it doesn't exist, also image save it
