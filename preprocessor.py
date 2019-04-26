import pandas as pd
import numpy as np

import os

from datetime import datetime
from matplotlib import pyplot as plt


class Preprocessor:

    def __init__(self, file):
        self.cols = ['date', 'open', 'high', 'low', 'close', 'volume']
        self.df = pd.read_csv(file, delimiter=',', usecols=self.cols)
        self.df = self.df.sort_values('date')
        self.file = file
        self.location = os.path.split(file)[0]

    def show_plot(self):
        plt.figure(figsize=(18, 9))
        plt.plot(range(self.df.shape[0]), (self.df['low'] + self.df['high'])/2.0)
        plt.xticks(range(0, self.df.shape[0], 500),
                   self.df['date'].loc[::500],
                   rotation=45)
        plt.xlabel('Date', fontsize=20)
        plt.ylabel('Avg Price', fontsize=20)
        plt.show()

    def return_df(self):
        return self.df
