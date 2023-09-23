import argparse
from transcribeMagic import transcribe_magic

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe an audio file")
    parser.add_argument(
        "--audio", help="Path to the audio file to be transcribed", required=True
    )
    args = parser.parse_args()

    transcribe_magic(args.audio)
