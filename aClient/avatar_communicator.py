import audioop
import logging
import os
import time
import wave
import paramiko
import pyaudio
from dotenv import load_dotenv
from pygame import mixer
from scp import SCPClient
from gtts import gTTS
import speech_recognition as sr

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

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
SSH_PRIVATE_KEY_PATH = os.getenv("SSH_PRIVATE_KEY_PATH")
mixer.init()


# CHECK_ENDPOINT = "http://sgpu1.cs.oslomet.no:5004/check_audio"


def play_welcome_message():
    """Play the welcome message."""
    mixer.init()
    mixer.music.load("welcome.wav")
    mixer.music.play()

    while mixer.music.get_busy():
        time.sleep(0.1)


def speak(filename):
    # Check if the file exists
    if not os.path.exists(filename):
        logging.error(f"File {filename} not found!")
        return

    mixer.music.load(filename)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.1)  # Wait until the file finishes playing

    # Release the file
    mixer.music.unload()


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that. Please try again.")
            return None
        except sr.RequestError:
            print("API unavailable. Please check your internet connection.")
            return None


def send_file_to_server(recordedfilename):
    """Send the file to the server using SCP."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    private_key = paramiko.Ed25519Key(filename=SSH_PRIVATE_KEY_PATH)

    ssh.connect(
        hostname=SERVER_HOST,
        username=SERVER_USERNAME,
        pkey=private_key,
    )
    destination = SERVER_PATH_UP + "/" + recordedfilename
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(recordedfilename, destination)

    logging.info(f"Sent file {recordedfilename} to server.")

    ssh.close()


def get_latest_bark_filename(timeout=240):  # Timeout in seconds
    start_time = time.time()

    while time.time() - start_time < timeout:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.Ed25519Key(filename=SSH_PRIVATE_KEY_PATH)
        ssh.connect(
            hostname=SERVER_HOST,
            username=SERVER_USERNAME,
            pkey=private_key,
        )
        stdin, stdout, stderr = ssh.exec_command(
            f"ls {SERVER_PATH_DOWN}/silero_audio_*.wav"
        )
        latest_filename = stdout.readline().strip()
        ssh.close()

        if latest_filename:
            logging.info(f"Latest filename: {latest_filename}")
            return latest_filename
        else:
            logging.warning("No filename retrieved from the server. Retrying...")
            time.sleep(5)  # wait for 5 seconds before retrying

    logging.error(
        "Failed to retrieve filename from the server after waiting for the timeout period."
    )
    return None


def download_response_from_server():
    full_path_on_server = get_latest_bark_filename()
    if not full_path_on_server:
        return None

    responsefilename = os.path.basename(full_path_on_server)
    logging.info(f"Attempting to download {responsefilename} from the server.")

    if os.path.exists(responsefilename):
        os.remove(responsefilename)

    source = f"{SERVER_PATH_DOWN}/{responsefilename}"
    destination = f"./{responsefilename}"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    private_key = paramiko.Ed25519Key(filename=SSH_PRIVATE_KEY_PATH)

    try:
        ssh.connect(hostname=SERVER_HOST, username=SERVER_USERNAME, pkey=private_key)
        with SCPClient(ssh.get_transport()) as scp:
            scp.get(source, destination)
        logging.info(f"Downloaded {responsefilename} from the server.")
        return responsefilename

    except Exception as e:
        logging.error(
            f"Error occurred while downloading {responsefilename} using scp: {e}"
        )
        return None


def play_response_from_server(responsefilename):
    """Play the response audio file."""
    mixer.music.unload()  # Unload any previously loaded sound
    mixer.music.load(responsefilename)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.1)


# def download_video_from_server():
#     """Download the response videofile from the server using SCP."""
#     full_path_on_server = get_latest_bark_filename()
#     if not full_path_on_server:
#         return None
#
#     # Extract only the filename from the full path
#     responsefilename = os.path.basename(full_path_on_server)
#     logging.info(f"Attempting to download {responsefilename} from the server.")
#     if os.path.exists(responsefilename):
#         os.remove(responsefilename)
#
#     # Build source and destination paths for scp
#     source = f"{SERVER_USERNAME}@{SERVER_HOST}:{SERVER_PATH_DOWN}/{responsefilename}"
#     destination = f"./{responsefilename}"
#
#     try:
#         subprocess.run(
#             ["scp", "-i", SSH_PRIVATE_KEY_PATH, source, destination], check=True
#         )
#         logging.info(f"Downloaded {responsefilename} from the server.")
#         return responsefilename
#     except subprocess.CalledProcessError as e:
#         logging.error(
#             f"Error occurred while downloading {responsefilename} using scp: {e}"
#         )
#         return None


def save_as_wav(recordfilename):
    """Save recorded frames as WAV file."""
    with wave.open(recordfilename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))
        logging.info(f"Saved file {recordfilename} to disk.")


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

        logging.info("Started recording.")

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

        logging.info("Stopped recording.")
        stream.stop_stream()
        stream.close()

        save_as_wav(recordfilename)
        send_file_to_server(recordfilename)
        time.sleep(20)  # wait for 10 seconds

        try:
            # Try downloading the response file directly
            responsefilename = download_response_from_server()
            if responsefilename:  # Check if the download was successful
                play_response_from_server(responsefilename)
                time.sleep(2)  # Wait for 2 second
                # try:
                #     os.remove(responsefilename)
                # except Exception as e:
                #     logging.error(
                #         f"Error occurred while deleting {responsefilename}: {e}"
                #     )
            else:
                logging.info("No response file found on the server.")

        except Exception as e:
            logging.error(
                f"Error occurred while downloading {responsefilename} using scp: {e}"
            )
        os.remove(recordfilename)

        speak("ask.wav")
        choice = recognize_speech()

        if choice == "no":
            speak("Exiting...")
            print("Exiting...")
            break


if __name__ == "__main__":
    play_welcome_message()
    audio = pyaudio.PyAudio()
    record_and_save()
