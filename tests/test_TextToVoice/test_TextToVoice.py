import json

# Simulate reading a JSON object from a file or API
transcription_str = '{"text": "Hello, world!"}'

# Parse the JSON-formatted string
try:
    transcription = json.loads(transcription_str)
except json.JSONDecodeError:
    print("Error decoding JSON")
    exit(1)

# Access the 'text' field
try:
    text = transcription["text"]
except KeyError:
    print("Key 'text' not found in JSON object")
    exit(1)

print(f"Extracted text: {text}")
