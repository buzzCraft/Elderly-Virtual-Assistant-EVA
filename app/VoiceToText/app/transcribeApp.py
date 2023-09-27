from flask import Flask, abort, request
from tempfile import NamedTemporaryFile
import whisper
import torch
import json
import tqdm

# Check if NVIDIA GPU is available
torch.cuda.is_available()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load the Whisper model:
model = whisper.load_model("base", device=DEVICE)
save_path = "/text-to-voice-app/"

app = Flask(__name__)


@app.route("/")
def test():
    return "Our API is Working!"


@app.route("/transcribe-service", methods=["POST"])
def transcribe_magic():
    if not request.files:
        abort(400)

    results = []

    for filename, handle in request.files.items():
        # Create a temporary file.
        temp = NamedTemporaryFile()

        handle.save(temp)

        result = model.transcribe(temp.name)

        results.append(
            {
                "transcript": result["text"],
            }
        )
    # Save to transcription.json
    try:
        with open(f"{save_path}transcription.json", "w") as outfile:
            json.dump({"results": results}, outfile, indent=4)
    except Exception as e:
        print("Error saving file:", e)
    # This will be automatically converted to JSON.
    return {"results": results}


# Using port 5000 for the transcribe service
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
