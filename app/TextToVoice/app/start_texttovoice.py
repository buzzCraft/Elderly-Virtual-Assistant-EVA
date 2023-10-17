import os
import time
import subprocess


def wait_for_transcription(file_path, timeout=200):
    """Wait for the transcription file to be ready.

    Args:
        file_path (str): Path to the transcription file.
        timeout (int, optional): Maximum wait time in seconds. Defaults to 300.

    Returns:
        float: Modification time of the file if found.

    Raises:
        TimeoutError: If the file is not found within the specified timeout.
    """
    start_time = time.time()

    while not os.path.exists(file_path):
        time.sleep(5)  # Check every 5 seconds
        elapsed_time = time.time() - start_time

        if elapsed_time > timeout:
            raise TimeoutError(
                f"Waited for {timeout} seconds, but {file_path} was not found."
            )

    return os.path.getmtime(file_path)


def process_transcription(transcription_path):
    """Process the transcription file and start text-to-voice processing.

    Args:
        transcription_path (str): Path to the transcription file.
    """
    current_timestamp = wait_for_transcription(transcription_path)
    print(f"New {transcription_path} detected. Starting texttovoice processing...")
    os.system("python /text-to-voice-app/voiceGen.py")

    # Rename the transcription file after voiceGen.py is done
    renamed_file = f"/text-to-voice-app/transcription_{int(current_timestamp)}.json"
    subprocess.run(
        ["python", "/text-to-voice-app/voiceGen.py"]
    )  # Wait for the process to finish
    os.rename(transcription_path, renamed_file)


if __name__ == "__main__":
    transcription_path = "/text-to-voice-app/transcription.json"

    while True:
        process_transcription(transcription_path)
        time.sleep(10)
