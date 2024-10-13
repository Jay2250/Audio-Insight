# voice_capture.py
import threading
import sounddevice as sd
import numpy as np
import wave

from pydub import AudioSegment
from pydub.effects import normalize

class VoiceCapture:
    def __init__(self, filename='lecture.wav', fs=44100):
        self.filename = filename
        self.fs = fs
        self.recording = []
        self.is_recording = False

    def preprocess_audio(self, filename):
        # Load audio file
        audio = AudioSegment.from_wav(filename)

        # Convert to mono and normalize
        mono_audio = audio.set_channels(1)
        normalized_audio = normalize(mono_audio)

        # Export the processed audio to a new file
        processed_filename = "processed_" + filename
        normalized_audio.export(processed_filename, format="wav")
        return processed_filename
    
    def _record_audio(self, duration):
        """The actual recording logic that runs in a separate thread."""
        print("Recording started...")
        self.recording = sd.rec(int(duration * self.fs), samplerate=self.fs, channels=2, dtype='int16')
        sd.wait()  # Wait until recording is finished
        print("Recording finished.")
    
    def start_recording(self, duration=60):  # Record for 60 seconds
        print("Recording started...")
        self.is_recording = True
        self.recording_thread = threading.Thread(target=self._record_audio, args=(duration,))
        self.recording_thread.start()
    
    def convert_to_mono(self, filename):
        """Convert the audio to mono."""
        audio = AudioSegment.from_wav(filename)
        mono_audio = audio.set_channels(1)
        mono_filename = "mono_" + filename
        mono_audio.export(mono_filename, format="wav")
        return mono_filename

    def save_recording(self):
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(self.fs)
            wf.writeframes(self.recording.tobytes())
        print(f"Recording saved as {self.filename}")


    def stop_recording(self):
        """Stop the recording."""
        if self.is_recording:
            sd.stop()
            self.is_recording = False
            print("Recording stopped.")
