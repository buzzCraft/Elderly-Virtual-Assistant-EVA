import whisper
from helpers import InvalidAudioFormatError, TranscriptionError


# Function to hold the magic
def transcribe_magic():
    # The user recording will be saved as a .wav file with name audio.wav in the audio_asset folder
    audio_file = "audio_asset/audio.wav"

    if not audio_file.lower().endswith(".wav"):
        raise InvalidAudioFormatError("Audio file must be a .wav file")

    try:
        model = whisper.load_model("base.en")
        output = model.transcribe(audio_file)
        return output["text"]

    except Exception as e:
        raise TranscriptionError(f"There was an error transcribing the audio file: {e}")
