from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from audio_capture import AudioCapture
from data_analysis import DataAnalysis
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label




Builder.load_file('interface.kv')



class LectureApp(BoxLayout):
    def __init__(self, **kwargs):
        super(LectureApp, self).__init__(**kwargs)
        self.audio_capture = AudioCapture()
        self.data_analysis = DataAnalysis()
        self.selected_file = None

    def open_file_chooser(self):
        # Create the popup and add the FileChooserIconView directly in the main class
        filechooser = FileChooserIconView()

        # Create the popup
        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(filechooser)

        # Add a load button
        load_button = Button(text="Load File", size_hint_y=None, height=50)
        load_button.bind(on_press=lambda instance: self.load_audio_file(
            filechooser.selection, popup))
        popup_layout.add_widget(load_button)

        popup = Popup(title="Choose Audio File",
                      content=popup_layout, size_hint=(0.9, 0.9))
        popup.open()

    def load_audio_file(self, selection, popup):
        if selection:
            self.selected_file = selection[0]
            print(f"Selected file: {self.selected_file}")
            popup.dismiss()

    def process_audio_file(self):
        if self.selected_file:
            # Convert and process the selected file
            self.audio_capture.load_audio_file(self.selected_file)
            self.data_analysis.speech_to_text(
                self.audio_capture.get_audio_data())
            print(f"Processed file: {self.selected_file}")
        else:
            print("No file selected to process.")

    def show_word_frequency(self):
        df = self.data_analysis.word_count_analysis()
        if df is not None:
            self.data_analysis.visualize_data(df)

    def show_summary(self):
        summary = self.data_analysis.summarize_text()
        if summary:
            self.display_result("Summary", summary)
        else:
            self.display_result("Summary", "No summary available.")


    def show_key_points(self):
        key_points = self.data_analysis.key_points()
        if key_points:
            # Convert list of key points to a formatted string
            key_points_text = "\n".join([f"- {point}" for point in key_points])
            self.display_result("Key Points", key_points_text)
        else:
            self.display_result("Key Points", "No key points available.")

    def show_wordcloud(self):
        self.data_analysis.generate_wordcloud()

    def display_result(self, title, result_text):
        # Create a popup to display the result text
        result_popup = Popup(title=title, size_hint=(0.9, 0.9))
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # ScrollView to handle long text
        scroll_view = ScrollView(size_hint=(1, 1))

        # Label for displaying the result (summary or key points)
        result_label = Label(text=result_text, size_hint_y=None,
                             text_size=(800, None), halign='left', valign='top')

        # Adjust the height of the label based on the content
        result_label.bind(texture_size=lambda instance,
                          size: setattr(result_label, 'height', size[1]))

        # Adding the label inside the scroll view
        scroll_view.add_widget(result_label)
        layout.add_widget(scroll_view)

        # Close button
        close_button = Button(text="Close", size_hint_y=None, height=50)
        close_button.bind(on_press=result_popup.dismiss)
        layout.add_widget(close_button)

        result_popup.content = layout
        result_popup.open()



class MyApp(App):
    def build(self):
        return LectureApp()


if __name__ == '__main__':
    MyApp().run()
