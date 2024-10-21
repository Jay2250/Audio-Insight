from pydub import AudioSegment
import os
import speech_recognition as sr
from moviepy.editor import AudioFileClip

class AudioCapture:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.audio_data = None  # Store the audio data

    def convert_to_wav(self, file_path):
        """Convert any audio file to .wav format."""
        file_format = file_path.split('.')[-1].lower()
        
        # Generate the new file path by changing the extension to .wav
        wav_file_path = file_path.rsplit('.', 1)[0] + ".wav"
        
        try:
            # Check if the file is already in .wav format
            if file_format == 'wav':
                print(f"File is already in .wav format: {file_path}")
                return file_path
            
            audio = AudioFileClip(file_path)
            # Write as WAV
            audio.write_audiofile('output.wav', codec='pcm_s16le')
            print(f"Converted '{file_path}' to 'output.wav'")

            # Convert the file to .wav using pydub
            print(f"Converting {file_path} to .wav format...")
            audio = AudioSegment.from_file('output.wav', format=file_format)
            audio.export(wav_file_path, format="wav")
            print(f"File successfully converted to {wav_file_path}")
            
            return wav_file_path
        except Exception as e:
            print(f"Error during file conversion: {e}")
            return None

    def load_audio_file(self, file_path):
        """Load audio data from a file."""
        try:
            # Convert file to .wav format if necessary
            wav_file_path = self.convert_to_wav(file_path)
            if wav_file_path:
                with sr.AudioFile(wav_file_path) as source:
                    self.audio_data = self.recognizer.record(source)
                print(f"Audio loaded successfully from {wav_file_path}")
            else:
                print("Failed to load the audio file.")
        except Exception as e:
            print(f"Error during loading audio file: {e}")
    
    def get_audio_data(self):
        """Returns the in-memory audio data."""
        return self.audio_data
