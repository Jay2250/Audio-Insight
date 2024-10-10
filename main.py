# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
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
        self.voice_capture.stop_recording()
        self.voice_capture.save_recording()
        self.data_analysis.load_data()
        df = self.data_analysis.analyze_data()
        self.data_analysis.visualize_data(df)


class MyApp(App):
    def build(self):
        return LectureApp()


if __name__ == '__main__':
    MyApp().run()
