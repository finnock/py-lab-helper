import math

import pylabhelper.CV as cv
from typing import List
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
from scipy.optimize import curve_fit


def read_cv_file(path):
    return cv.CV(path)


def fitting_function(speed, capacitive, faradayic):
    current = capacitive * speed + faradayic * np.sqrt(speed)
    return current


def fc_analysis(files: List[cv.CV], cycle_number, cutoff=-1):

    # Sort cycles list by speed
    files.sort(key=lambda item: item.speed)

    lin_reg_list = []
    f_reg_list = []

    speeds = []
    cycles = []
    for file in files:
        speeds.append(file.speed)
        cycles.append(file.interp_data[file.interp_data['cycle'] == cycle_number])

    x = np.sqrt(speeds).reshape((-1, 1))
    speeds_squared = np.sqrt(speeds)

    fc_data = {
        'index': [],
        'potential': [],
        'faradayic': [],
        'capacitive': [],
        'direction': [],
        'rSq': []
    }

    for index, row in cycles[0].iterrows():
        y = []
        for speed_index in range(len(speeds)):
            y.append(cycles[speed_index].current[index])

        popt, pcov = curve_fit(fitting_function, np.array(speeds), y)

        rSq = np.sqrt(np.diag(pcov))
        capacitive = popt[0]
        faradayic = popt[1]

        f_reg_list.append([row.potential] + y + [rSq, faradayic, capacitive, row.direction])

    for index, row in cycles[0].iterrows():
        y = []
        for speed_index in range(len(speeds)):
            y.append(cycles[speed_index].current[index] / np.sqrt(speeds[speed_index]))

        model = LinearRegression().fit(x[:cutoff], y[:cutoff])
        rSq = model.score(x[:cutoff], y[:cutoff])
        faradayic = model.intercept_
        capacitive = model.coef_[0]

        fc_data['index'].append(index)
        fc_data['potential'].append(row['potential'])
        fc_data['faradayic'].append(faradayic)
        fc_data['capacitive'].append(capacitive)
        fc_data['direction'].append(row['direction'])
        fc_data['rSq'].append(rSq)

        lin_reg_list.append([cycles[speed_index].potential[index]] + y + [rSq, faradayic, capacitive, row['direction']])

    return \
        pd.DataFrame(fc_data),\
        pd.DataFrame(
            lin_reg_list,
            columns=['potential'] + list(speeds_squared) + ['rSq', 'faradayic', 'capacitive', 'direction']
        ),\
        pd.DataFrame(
            f_reg_list,
            columns=['potential'] + list(speeds) + ['rSq', 'faradayic', 'capacitive', 'direction']
        )
