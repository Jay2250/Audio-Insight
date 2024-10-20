import speech_recognition as sr
import wave

class VoiceCapture:
    def __init__(self, filename='lecture.wav'):
        self.filename = filename
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.audio_data_list = []  # Store audio chunks

    def start_recording(self):
        print("Recording started...")
        try:
            # Adjust microphone sensitivity to ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("Listening... (Press 'Stop Recording' to end)")
                # Record in chunks and accumulate audio data
                audio = self.recognizer.listen(source)
                self.audio_data_list.append(audio)  # Store the audio chunk
        except Exception as e:
            print(f"Error during recording: {e}")

    def stop_recording(self):
        print("Recording stopped.")
        if len(self.audio_data_list) > 0:
            # Concatenate all audio chunks
            combined_audio = b''.join([audio.get_wav_data() for audio in self.audio_data_list])
            # Save the combined audio as a single WAV file
            with wave.open(self.filename, 'wb') as wf:
                wf.setnchannels(1)  # Mono
                wf.setsampwidth(2)  # 2 bytes for 16-bit samples
                wf.setframerate(16000)  # Sample rate
                wf.writeframes(combined_audio)
            print(f"Recording saved as {self.filename}")
        else:
            print("No audio data to save.")
        # Clear the list after saving
        self.audio_data_list = []

    def speech_to_text(self):
        try:
            if self.audio_data_list:
                combined_audio = b''.join([audio.get_wav_data() for audio in self.audio_data_list])
                text = self.recognizer.recognize_google(self.audio_data_list[-1])  # Use the last chunk for now
                print(f"Transcription: {text}")
                return text
            else:
                print("No audio data available to transcribe.")
                return None
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
