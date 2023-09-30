from flask import Flask, request, jsonify
import subprocess
import re

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    instruction = data['instruction']
    prompt = data['prompt']

    cmd = ["wine",
        "/app/main.exe",
        "-t", "12",
        "-m", "/app/model/llama-2-7b-chat.Q2_K.gguf",
        "--color",
        "-c", "4096",
        "--temp", "0.7",
        "--repeat_penalty", "1.1",
        "-n", "-1",
        "-p", f"<s>[INST] <<SYS>> {instruction} <</SYS>>  {prompt}! </s>"
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    cleaned_output = re.search(r'\[0m\s*(.*?)\s*$', result.stdout)
    if cleaned_output:
        cleaned_output = cleaned_output.group(1)

        return jsonify({"response": cleaned_output})
    else:
        error_data = {"error": "Failed to generate response"}
        return jsonify(error_data), 500
    
if __name__ == '__main__':
    app.run(port=5000)