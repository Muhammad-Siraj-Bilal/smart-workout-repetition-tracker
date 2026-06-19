import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from features.data_trans import LowPassFilter
from scipy.signal import argrelextrema

def findWeights(df, freqs, goal=10):
    preds = []
    for col in df.columns[:6]:
        lp = LowPassFilter()
        # print(col)
        # print(freqs[col])
        # freq = freqs.get(col)
        # for key in freqs.keys():
            # print(f'comparing {key} and {col}')
        #     if key[0] == col[0]:
        #         freq = df[key]
        # print('checking for freq ', freq)
        filtered = lp.low_pass_filter(df, col, 2, freqs[col], 10)
        op = argrelextrema(filtered[col + '_lowpass'].values, np.greater)
        peaks = filtered.iloc[op]
        preds.append(len(peaks))
    print(preds)
    weights = []
    for i in preds:
        if i == goal:
            weights.append(1)
        else:
            weights.append(round(1/(abs(i - goal)+1), 2))
    weights = {'x_a':weights[0], 'y_a':weights[1], 'z_a':weights[2], 'x_g':weights[3], 'y_g':weights[4], 'z_g':weights[5]}
    return weights
