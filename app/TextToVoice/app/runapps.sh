#!/bin/bash

# Start the first Flask app in the background
python3 voiceGen.py &

# Start the second Flask app
python3 audio_check_server.py
