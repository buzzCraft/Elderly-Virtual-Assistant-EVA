import pyaudio
import wave
import audioop
from pygame import mixer
import time
import subprocess

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
THRESHOLD_SILENCE = 100  # Number of silent chunks before ending recording
AMPLITUDE_THRESHOLD = 1000  # Amplitude threshold for detecting silence

frames = []


def play_welcome_message():
    """Play the welcome message."""
    mixer.init()
    mixer.music.load("welcome.mp3")
    mixer.music.play()

    while mixer.music.get_busy():
        time.sleep(0.1)


def send_file_to_endpoint(filename):
    """Send the file to the transcription endpoint."""
    send_command = ["curl.exe", "-F", f"file=@{filename}", "http://localhost:5000/transcribe-service"]
    subprocess.run(send_command)


def is_audio_reproduced():
    """Check if the audio has been reproduced on the server side."""
    # TODO: Implement check function
    # Completion flag or poll an endpoint to check if the audio was reproduced
    time.sleep(10)
    return True


def save_as_wav(filename):
    """Save recorded frames as WAV file."""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))
    print(f"File saved as {filename}")


def record_and_save(filename="recorded_audio.wav"):
    """Record audio and save to file."""
    global frames  # To be modified in this function
    while True:
        frames = []  # Reset frames for multiple recordings
        stream = audio.open(
            format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
        )

        print(
            "Recording... Start talking. Be silent for a few seconds to end and save the recording."
        )
        silent_chunks = 0

        while True:
            data = stream.read(CHUNK)
            frames.append(data)
            amplitude = audioop.rms(data, 2)

            if amplitude < AMPLITUDE_THRESHOLD:
                silent_chunks += 1
            else:
                silent_chunks = 0

            if silent_chunks > THRESHOLD_SILENCE:
                break

        print("Finished recording.")
        stream.stop_stream()
        stream.close()

        save_as_wav(filename)
        send_file_to_endpoint(filename)

        # Wait for audio to be reproduced
        while not is_audio_reproduced():
            time.sleep(1)

        # Audio was reproduced, ask to record again
        choice = input("Do you want to record again? (y/n): ").lower()
        if choice != "y":
            print("Exiting...")
            break


if __name__ == "__main__":
    play_welcome_message()
    audio = pyaudio.PyAudio()
    record_and_save()
