import pandas as pd
import numpy as np
from features.data_trans import LowPassFilter
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt

def findFreqs(df, goal=10):
    results = []
    for i in df.columns:
        column = i

        d = {0.05:0, 0.1: 0, 0.15:0, 0.2:0, 0.25:0, 0.3:0, 0.35:0, 0.4:0, 0.5:0, 0.6:0, 0.7:0, 0.8:0, 0.9:0}
        print(f'Calculating for {i}')
        for key in d.keys():
            freq = key
            print(f'Doing freq {freq}')

            lp = LowPassFilter()
            filtered = lp.low_pass_filter(df, column, 2, freq, 10)

            op = argrelextrema(filtered[column + '_lowpass'].values, np.greater)
            peaks = filtered.iloc[op]
            d[freq] = len(peaks)
            print(d[freq])

            # fig, ax = plt.subplots()
            # plt.plot(df[f"{column}"])
            # # plt.plot(peaks [f"{column}"], "o", color="red") 
            # ax.set_ylabel(f"{column}")
            # plt.show()

            # fig, ax = plt.subplots()
            # plt.plot(df[f"{column}_lowpass"])
            # plt.plot(peaks [f"{column}_lowpass"], "o", color="red") 
            # ax.set_ylabel(f"{column}_lowpass")
            # plt.show()
            
        print(d)

        minf = 0.1
        minp = d[0.1]
        for key, value in d.items():
            print('Running loop')
            print(f'Comparing {abs(value - goal)} < {abs(minp - goal)}')
            if abs(value - goal) < abs(minp - goal):
                print(f'{abs(value - goal)} < {abs(minp - goal)}')
                minf = key
                minp = value
        print((minf, minp))
        results.append(minf)
    results = {'x_a':results[0], 'y_a':results[1], 'z_a':results[2], 'x_g':results[3], 'y_g':results[4], 'z_g':results[5]}
    return results
