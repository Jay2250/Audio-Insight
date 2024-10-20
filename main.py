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
        self.voice_capture.start_recording()

    def stop_recording(self):
        # Get the audio data from voice capture and pass it to data analysis for transcription
        audio_data = self.voice_capture.get_audio_data()
        if audio_data:
            self.data_analysis.speech_to_text(audio_data)

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
