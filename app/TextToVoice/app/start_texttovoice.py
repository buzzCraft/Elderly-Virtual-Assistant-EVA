import os
import time


def wait_for_transcription(file_path, timeout=300):
    """Wait for the transcription file to be ready."""
    start_time = time.time()
    while not os.path.exists(file_path):
        time.sleep(5)  # Check every 5 seconds
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            raise TimeoutError(
                f"Waited for {timeout} seconds, but {file_path} was not found."
            )

    print(f"{file_path} is ready. Starting texttovoice processing...")


if __name__ == "__main__":
    transcription_path = "/text-to-voice-app/transcription.json"
    wait_for_transcription(transcription_path)

    # Once the transcription file is ready, start the main processing script
    os.system("python /text-to-voice-app/voiceGen.py")
