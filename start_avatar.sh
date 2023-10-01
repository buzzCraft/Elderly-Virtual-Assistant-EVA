#!/bin/bash

# Check if portaudio19-dev is installed
if ! dpkg -l | grep -q portaudio19-dev; then
    sudo apt-get install portaudio19-dev
fi

# Check if pyaudio is installed
if ! pip3 list | grep -q pyaudio; then
    pip3 install pyaudio
fi
# Check if pygame is installed
if ! pip3 list | grep -q pygame; then
    pip3 install pygame
fi

# Run recording script (record_audio.py)
python3 record_audio.py
