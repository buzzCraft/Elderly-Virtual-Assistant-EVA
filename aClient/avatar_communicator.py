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
SERVER_PATH = os.getenv("SERVER_PATH_ENV")
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
        hostname=SERVER_HOST,
        username=SERVER_USERNAME,
        password=SERVER_PASSWORD
    )

    with SCPClient(ssh.get_transport()) as scp:
        scp.put(recordedfilename, SERVER_PATH + recordedfilename)

    ssh.close()


def download_response_from_server(responsefilename):
    """Download the response audio file from the server using SCP."""
    response_filename = responsefilename.replace(".wav", "_response.wav")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=SERVER_HOST,
        username=SERVER_USERNAME,
        password=SERVER_PASSWORD
    )

    with SCPClient(ssh.get_transport()) as scp:
        scp.get(SERVER_PATH + response_filename, response_filename)

    ssh.close()
    return response_filename


def play_response_from_server(responsefilename):
    """Play the response audio file."""
    mixer.init()
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

        response = requests.get(CHECK_ENDPOINT)
        data = response.json()
        if data["available"]:
            audio_filename = data["filename"]
            responsefilename = download_response_from_server(audio_filename)
            play_response_from_server(responsefilename)

        choice = input("Do you want to record again? (y/n): ")
        if choice != "y":
            print("Exiting...")
            break

        os.remove(recordfilename)
        os.remove(responsefilename)


if __name__ == "__main__":
    play_welcome_message()
    audio = pyaudio.PyAudio()
    record_and_save()
