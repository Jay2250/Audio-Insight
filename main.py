import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from voice_capture import VoiceCapture
from data_analysis import DataAnalysis


Builder.load_file('interface.kv')

class LectureApp(BoxLayout):
    def __init__(self, **kwargs):
        super(LectureApp, self).__init__(**kwargs)
        self.voice_capture = VoiceCapture()
        self.data_analysis = DataAnalysis()

    def start_recording(self):
        """Start recording in the background."""
        threading.Thread(target=self.voice_capture.start_recording).start()

    def stop_recording(self):
        self.voice_capture.stop_recording()
        self.voice_capture.save_recording()

        # # Preprocess audio (convert to mono and normalize)
        # mono_audio = self.voice_capture.convert_to_mono("lecture.wav")
        # processed_audio = self.voice_capture.preprocess_audio(mono_audio)

        # # Load and analyze processed audio
        # self.data_analysis.load_data(processed_audio)
        # self.data_analysis.speech_to_text(processed_audio)
        threading.Thread(target=self.process_audio).start()

    def process_audio(self):
        """Preprocess and analyze the audio file."""
        processed_audio = self.voice_capture.preprocess_audio("lecture.wav")

        # Load and analyze processed audio
        self.data_analysis.load_data(processed_audio)
        self.data_analysis.speech_to_text(processed_audio)

    def show_word_frequency(self):
        df = self.data_analysis.word_count_analysis()
        if df is not None:
            self.data_analysis.visualize_data(df)

    def show_summary(self):
        summary = self.data_analysis.summarize_text()
        if summary:
            print("Summary:\n", summary)

    def show_key_points(self):
        key_points = self.data_analysis.key_points()
        if key_points:
            print("Key Points:\n", key_points)

    def show_wordcloud(self):
        self.data_analysis.generate_wordcloud()

class MyApp(App):
    def build(self):
        return LectureApp()

if __name__ == '__main__':
    MyApp().run()
