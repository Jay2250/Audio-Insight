import speech_recognition as sr


class VoiceCapture:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.audio_data = None  # Store the audio data in-memory

    def start_recording(self):
        print("Recording started...")
        try:
            # Adjust microphone sensitivity to ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("Listening... (Press 'Stop Recording' to end)")
                # Listen and store the audio data in memory
                self.audio_data = self.recognizer.listen(source)
        except Exception as e:
            print(f"Error during recording: {e}")

    def get_audio_data(self):
        """Returns the in-memory audio data."""
        return self.audio_data
