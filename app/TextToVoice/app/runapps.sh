#!/bin/bash

python3 voiceGen.py &
python3 audio_check_server.py
wait
