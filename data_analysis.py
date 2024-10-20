import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import speech_recognition as sr
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from scipy.io import wavfile

# Download NLTK data if necessary
nltk.download('punkt')
nltk.download('stopwords')

class DataAnalysis:
    def __init__(self, filename='lecture.wav'):
        self.filename = filename
        self.data = None
        self.transcript = None

    def load_data(self, filename=None):
        """Load the audio data from a file."""
        if filename:
            self.filename = filename
        try:
            self.fs, self.data = wavfile.read(self.filename)
            print("Audio data loaded.")
        except Exception as e:
            print(f"Error loading audio: {e}")

    def speech_to_text(self, filename='lecture.wav'):
        """Convert audio speech to text."""
        if filename:
            self.filename = filename
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(self.filename) as source:
                audio = recognizer.record(source)  # Record the audio from the file
                self.transcript = recognizer.recognize_google(audio)  # Store as self.transcript
                print("Transcription:", self.transcript)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    
    def word_count_analysis(self):
        if self.transcript is None:
            return None
        words = word_tokenize(self.transcript.lower())
        words = [word for word in words if word.isalpha()]  # Remove punctuation
        filtered_words = [word for word in words if word not in stopwords.words('english')]
        word_freq = Counter(filtered_words)

        df = pd.DataFrame(word_freq.most_common(10), columns=['Word', 'Frequency'])
        return df

    def summarize_text(self):
        if self.transcript is None:
            return None
        sentences = sent_tokenize(self.transcript)
        word_freq = Counter(word_tokenize(self.transcript.lower()))
        ranking = {}
        for i, sentence in enumerate(sentences):
            for word in word_tokenize(sentence.lower()):
                if word in word_freq:
                    if i not in ranking:
                        ranking[i] = word_freq[word]
                    else:
                        ranking[i] += word_freq[word]
        top_sentences = sorted(ranking, key=ranking.get, reverse=True)[:3]
        summary = ' '.join([sentences[i] for i in top_sentences])
        return summary

    def key_points(self):
        if self.transcript is None:
            return None
        words = word_tokenize(self.transcript.lower())
        words = [word for word in words if word.isalpha()]  # Remove punctuation
        filtered_words = [word for word in words if word not in stopwords.words('english')]
        key_words = Counter(filtered_words).most_common(5)
        return [word for word, _ in key_words]

    def visualize_data(self, df):
        plt.figure(figsize=(10, 6))
        df.plot(kind='bar', x='Word', y='Frequency', legend=False)
        plt.title('Top 10 Word Frequency in Lecture')
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def generate_wordcloud(self):
        if self.transcript is None:
            return None
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(self.transcript)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()
