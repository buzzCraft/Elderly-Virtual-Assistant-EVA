# record_audio.py

import sounddevice as sd
import soundfile as sf


def record_audio(filename="recorded_audio.wav", duration=5, fs=44100):
    print("Recording...")
    my_recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    sf.write(filename, my_recording, fs)
    print(f"Recording saved as {filename}")


if __name__ == "__main__":
    record_audio()
