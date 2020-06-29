import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from . import settings


def build():
    if os.path.isfile('report/vid_em_report.csv'):
        dataset = pd.read_csv('report/vid_em_report.csv')
        time = dataset.iloc[:, :-1].values
        em_score = dataset.iloc[:, -1].values
        em_score = np.reshape(em_score, (len(em_score), 1))
        av_em_score = np.average(em_score)

        em_dict = dict((v, k) for k, v in settings.EMOTIONS_SCORE.items())
        label = settings.EMOTIONS_DICT.get(em_dict.get(int(av_em_score), None), 'Uknown')

        if av_em_score < 3.7:
            color = 'red'
        elif 3.7 < av_em_score < 4.7:
            color = 'blue'
        else:
            color = 'green'

        _, ax = plt.subplots()

        ax.plot(time, em_score, color=color)
        ax.set_xlim(np.min(time), np.max(time))
        ax.set_ylim(np.min(em_score), np.max(em_score))

        plt.ylabel('Emotion Score')
        plt.xlabel('Vide Time (seconds)')
        plt.title(f'Emotion Average Score: {label}')
        plt.savefig('report/vid_visual_report.png')
