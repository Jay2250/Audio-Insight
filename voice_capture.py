# voice_capture.py
import sounddevice as sd
import numpy as np
import wave


class VoiceCapture:
    def __init__(self, filename='lecture.wav', fs=44100):
        self.filename = filename
        self.fs = fs
        self.recording = []

    def start_recording(self):
        print("Recording started...")
        self.recording = sd.rec(
            int(10 * self.fs), samplerate=self.fs, channels=2, dtype='int16')
        sd.wait()  # Wait until recording is finished

    def stop_recording(self):
        print("Recording stopped.")
        sd.stop()

    def save_recording(self):
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(self.fs)
            wf.writeframes(self.recording.tobytes())
        print(f"Recording saved as {self.filename}")
