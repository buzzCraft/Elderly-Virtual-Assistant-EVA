import pytest
from app.VoiceToText.transcribeMagic import transcribe_magic


def test_transcribe_magic_with_existing_files(mocker):
    # Mocks the load_model and transcribe functions from whisper to simulate a successful transcription without
    # actually running the functions
    mocker.patch("app.VoiceToText.transcribeMagic.whisper.load_model")
    mocker.patch(
        "app.VoiceToText.transcribeMagic.whisper.transcribe",
        return_value={"text": "mocked transcription"},
    )

    result = transcribe_magic()
    assert result == "mocked transcription"


def test_transcribe_magic_missing_model(mocker):
    # Mocks a successful transcription but simulate a FileNotFoundError when trying to load the model
    mocker.patch(
        "app.VoiceToText.transcribeMagic.whisper.load_model",
        side_effect=FileNotFoundError,
    )
    mocker.patch(
        "app.VoiceToText.transcribeMagic.whisper.transcribe",
        return_value={"text": "mocked transcription"},
    )

    with pytest.raises(FileNotFoundError):
        transcribe_magic()


def test_transcribe_magic_missing_audio(mocker):
    # Mocks a successful transcription but simulate a FileNotFoundError when trying to load the audio
    mocker.patch("app.VoiceToText.transcribeMagic.whisper.load_model")
    mocker.patch(
        "app.VoiceToText.transcribeMagic.whisper.transcribe",
        side_effect=FileNotFoundError,
    )

    with pytest.raises(FileNotFoundError):
        transcribe_magic()
