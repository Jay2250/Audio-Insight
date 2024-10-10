# data_analysis.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class DataAnalysis:
    def __init__(self, filename='lecture.wav'):
        self.filename = filename
        self.data = None

    def load_data(self):
        self.data = np.fromfile(self.filename, dtype=np.int16)
        print("Data loaded.")

    def analyze_data(self):
        if self.data is not None:
            # Example analysis: simple statistics
            mean = np.mean(self.data)
            std_dev = np.std(self.data)
            # Create a DataFrame for analysis
            df = pd.DataFrame(
                {'Mean': [mean], 'Standard Deviation': [std_dev]})
            return df
        else:
            print("No data to analyze.")

    def visualize_data(self, df):
        plt.figure(figsize=(8, 4))
        df.plot(kind='bar')
        plt.title('Data Analysis')
        plt.xlabel('Statistics')
        plt.ylabel('Value')
        plt.grid()
        plt.show()
