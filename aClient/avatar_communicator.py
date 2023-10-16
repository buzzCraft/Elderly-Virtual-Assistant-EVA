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

MAX_RETRIES = 10
BASE_WAIT_TIME = 2  # seconds
TIMEOUT = 60  # seconds

frames = []
SERVER_HOST = os.getenv("SERVER_HOST_ENV")
SERVER_USERNAME = os.getenv("SERVER_USERNAME_ENV")
SERVER_PATH_UP = os.getenv("SERVER_PATH_ENV_UP")
SERVER_PATH_DOWN = os.getenv("SERVER_PATH_ENV_DOWN")
SERVER_PASSWORD = os.getenv("SERVER_PASSWORD_ENV")

CHECK_ENDPOINT = "http://sgpu1.cs.oslomet.no:5003/generate_voice"


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

        def is_audio_ready(filename):
            try:
                response = requests.post(
                    CHECK_ENDPOINT, data={"filename": filename}, timeout=60
                )
                server_response = response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error while making request: {e}")
                return None

            if server_response["status"] == "success":
                return server_response[
                    "filename"
                ]  # Return the generated audio filename
            return None

        retry_count = 0
        start_time = time.time()
        processed_audio_filename = None

        while retry_count < MAX_RETRIES:
            processed_audio_filename = is_audio_ready(recordfilename)

            if processed_audio_filename:
                # Download and play the audio using the returned filename
                responsefilename = download_response_from_server(
                    processed_audio_filename
                )
                if responsefilename:
                    play_response_from_server(responsefilename)
                    try:
                        os.remove(responsefilename)
                    except Exception as e:
                        print(f"Error deleting {responsefilename}: {e}")
                break
            else:
                retry_count += 1
                wait_time = BASE_WAIT_TIME * retry_count
                elapsed_time = time.time() - start_time
                if elapsed_time + wait_time > TIMEOUT:
                    wait_time = TIMEOUT - elapsed_time
                    if wait_time <= 0:
                        print("Timed out waiting for audio processing.")
                        break
                time.sleep(wait_time)

        choice = input("Do you want to record again? (y/n): ")
        if choice != "y":
            print("Exiting...")
            break


if __name__ == "__main__":
    play_welcome_message()
    audio = pyaudio.PyAudio()
    record_and_save()
