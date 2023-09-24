from flask import Flask, request, jsonify
from model import initialize_model
import torch

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# CONSTANTS
MODEL_NAME = "meta-llama/Llama-2-7b"
HF_AUTH = "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"
SAVE_DIRECTORY = "./llama_models"

# Initialize the chatbot
chatbot = initialize_model(MODEL_NAME, HF_AUTH, SAVE_DIRECTORY)

# Initialize the Flask app
app = Flask(__name__)

@app.route("/generate_response", methods=["POST"])
def generate_response():
    try:
        # Get the request data
        user_input = request.json.get("user_input")

        # Check if the user input is empty
        if not user_input:
            return jsonify({"error": "Empty user input"})
        
        # Generate the response
        response = chatbot(human_input=user_input)

        # Return the response
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)