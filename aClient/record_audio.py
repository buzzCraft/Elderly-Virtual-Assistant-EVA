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
    send_command = [
        "curl.exe",
        "-F",
        f"file=@{filename}",
        "http://localhost:5000/transcribe-service",
    ]
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
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
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
    # play_welcome_message()
    audio = pyaudio.PyAudio()
    record_and_save()


import pyaudio
import wave
import audioop
from pygame import mixer
import time
import subprocess
import os
import requests
from dotenv import load_dotenv
import paramiko
from scp import SCPClient

load_dotenv(".env")

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
THRESHOLD_SILENCE = 100  # Number of silent chunks before ending recording
AMPLITUDE_THRESHOLD = 1000  # Amplitude threshold for detecting silence

frames = []
SERVER_HOST = os.getenv("SERVER_HOST_ENV")
SERVER_USERNAME = os.getenv("SERVER_USERNAME_ENV")
SERVER_PATH_UP = os.getenv("SERVER_PATH_ENV_UP")
SERVER_PATH_DOWN = os.getenv("SERVER_PATH_ENV_DOWN")
SERVER_PASSWORD = os.getenv("SERVER_PASSWORD_ENV")

CHECK_ENDPOINT = "http://sgpu1.cs.oslomet.no:5004/check_audio"


def play_welcome_message():
    """Play the welcome message."""
    mixer.init()
    mixer.music.load("welcome.mp3")
    mixer.music.play()

    while mixer.music.get_busy():
        time.sleep(0.1)


def send_file_to_server(recordedfilename):
    """Send the file to the server using SCP."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=SERVER_HOST, username=SERVER_USERNAME, password=SERVER_PASSWORD
    )
    destination = SERVER_PATH_UP + "/" + recordedfilename
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(recordedfilename, destination)

    ssh.close()


def download_response_from_server(responsefilename):
    """Download the response audio file from the server using SCP."""
    if os.path.exists(responsefilename):
        os.remove(responsefilename)

    source = f"{SERVER_USERNAME}@{SERVER_HOST}:{SERVER_PATH_DOWN}/{responsefilename}"
    destination = f"./{responsefilename}"

    try:
        subprocess.run(["scp", source, destination], check=True)
        print(f"Downloaded {responsefilename} from the server.")
        return responsefilename
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while downloading {responsefilename} using scp: {e}")
        return None


def play_response_from_server(responsefilename):
    """Play the response audio file."""
    mixer.init()
    mixer.music.unload()
    time.sleep(1)  # Wait for 1 second
    mixer.music.load(responsefilename)
    mixer.music.play()

    while mixer.music.get_busy():
        time.sleep(0.1)


def save_as_wav(recordfilename):
    """Save recorded frames as WAV file."""
    with wave.open(recordfilename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))
    print(f"File saved as {recordfilename}")


def record_and_save(recordfilename="recorded_audio.wav"):
    """Record audio and save to file."""
    global frames  # To be modified in this function
    while True:
        frames = []  # Reset frames for multiple recordings
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
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

        save_as_wav(recordfilename)
        send_file_to_server(recordfilename)
        time.sleep(20)  # wait for 10 seconds

        try:
            # Try downloading the response file directly
            processed_audio_filename = "bark_audio.wav"
            responsefilename = download_response_from_server(processed_audio_filename)
            if responsefilename:  # Check if the download was successful
                play_response_from_server(responsefilename)
                time.sleep(2)  # Wait for 2 second
                try:
                    os.remove(responsefilename)
                except Exception as e:
                    print(f"Error deleting {responsefilename}: {e}")

            else:
                print(
                    "No response received from the server. Please check and try again."
                )
        except Exception as e:
            print(f"An error occurred: {e}")

        os.remove(recordfilename)

        choice = input("Do you want to record again? (y/n): ")
        if choice != "y":
            print("Exiting...")
            break


if __name__ == "__main__":
    play_welcome_message()
    audio = pyaudio.PyAudio()
    record_and_save()
