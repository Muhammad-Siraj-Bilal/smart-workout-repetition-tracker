import pandas as pd
import numpy as np
from features.data_trans import LowPassFilter
from scipy.signal import argrelextrema
import os
# import matplotlib.pyplot as plt

def findReps(df, freqs, weights):
    reps = []
    for i in df.columns[:3]:  # Removed 3 from ...[3:]:
        column = i
        freq = freqs.get(i)
        # print(column, freq)
        lp = LowPassFilter()
        filtered = lp.low_pass_filter(df, column, 5, freq, 10)

        op = argrelextrema(filtered[column + '_lowpass'].values, np.greater)
        peaks = filtered.iloc[op]
        reps.append(len(peaks))
        # print(reps)
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
    
    # Now we must choose which prediction to consider
    # If 2 weights are 1 and both preds are same, then choose that pred
    if weights['x'] == weights['y'] == 1:
        if reps[0] == reps[1]:
            result = reps[0]
        else:
            if abs(reps[2] - reps[0]) < abs(reps[2] - reps[1]):
                result = reps[0]
            else:
                result = reps[1]
    elif weights['x'] == weights['z'] == 1:
        if reps[0] == reps[2]:
            result = reps[0]
        else:
            if abs(reps[1] - reps[0]) < abs(reps[1] - reps[2]):
                result = reps[0]
            else:
                result = reps[2]
    elif weights['y'] == weights['z'] == 1:
        if reps[1] == reps[2]:
            result = reps[1]
        else:
            if abs(reps[0] - reps[1]) < abs(reps[0] - reps[2]):
                result = reps[1]
            else:
                result = reps[2]
    elif weights['x'] == 1:
        if abs(reps[0]-reps[1]) > 1 and abs(reps[0]-reps[2]) > 1:
            result = reps[0] + 1
        elif abs(reps[0]-reps[1]) < 1 and abs(reps[0]-reps[2]) < 1:
            result = reps[0] - 1
        else:
            result = reps[0]
    elif weights['y'] == 1:
        if abs(reps[1]-reps[0]) > 1 and abs(reps[1]-reps[2]) > 1:
            result = reps[1] + 1
        elif abs(reps[1]-reps[0]) < 1 and abs(reps[1]-reps[2]) < 1:
            result = reps[1] - 1
        else:
            result = reps[1]
    elif weights['z'] == 1:
        if abs(reps[2]-reps[1]) > 1 and abs(reps[2]-reps[0]) > 1:
            result = reps[2] + 1
        elif abs(reps[2]-reps[1]) < 1 and abs(reps[2]-reps[0]) < 1:
            result = reps[2] - 1
        else:
            result = reps[2]
    else:
        result = reps[0]
    return result

# Test to execute only if this file is executed directly    
if __name__ == '__main__':
    path = 'sorted_data'
    ex = 'row_heavy'
    f_acc = "A-row-heavy_MetaWear_2019-01-14T15.04.06.123_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv"
    f_gyr = "A-row-heavy_MetaWear_2019-01-14T15.04.06.123_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv"

    df_acc = pd.read_csv(os.path.join(path, ex, f_acc))
    df_gyr = pd.read_csv(os.path.join(path, ex, f_gyr))

    freqs_acc = {'x':0.3, 'y':0.3, 'z':0.3}
    freqs_gyr = {'x':0.2, 'y':0.2, 'z':0.2}

    weights_acc = {'x':0.5, 'y':1, 'z':1}
    weights_gyr = {'x':1, 'y':0.5, 'z':0.5}

    print(findReps(df_acc, freqs_acc, weights_acc))