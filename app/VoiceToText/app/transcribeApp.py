from flask import Flask, abort, request
from tempfile import NamedTemporaryFile
import whisper
from whisper import _download, _MODELS
import torch
import json
import os
import time

torch.cuda.is_available()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# Download the base model
def model_exists(model_path, filename):
    """Check if the model file exists at the specified path."""
    return os.path.exists(os.path.join(model_path, filename))


model_path = "models/"
if not model_exists(model_path, "base.pt"):
    _download(_MODELS["base"], model_path, False)

# Load the model:
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
        # Rename the old transcription.json file if it exists
    if os.path.exists(f"{save_path}transcription.json"):
        current_timestamp = int(time.time())
        renamed_file = f"{save_path}transcription_{current_timestamp}.json"
        os.rename(f"{save_path}transcription.json", renamed_file)
    # Save to transcription.json
    try:
        with open(f"{save_path}transcription.json", "w") as outfile:
            json.dump({"results": results}, outfile, indent=4)
        #

    except Exception as e:
        print("Error saving file:", e)
    # This will be automatically converted to JSON.
    return {"results": results}


# Using port 5000 for the transcribe service
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
