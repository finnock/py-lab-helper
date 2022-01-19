import os
import sys

import numpy as np
import pandas as pd

import pylabhelper.math as lm
import re
from scipy import interpolate


def read_mpt(path):
    """Read a biologic mpt file into a pandas dataframe, extracting the cycles as they are described in the data."""
    file_contents = open(path).readlines()
    header_lines = int(re.findall('Nb header lines : ([0-9]+)', file_contents[1])[0])

    header = file_contents[:(header_lines-1)]

    matching = [s for s in header if "dE/dt" in s]
    meas_speed = lm.to_float(matching[0][5:-3])

    # Default file type
    file_type = 'LSV'

    # Find the keys for the interesting numbers
    for key, header in enumerate(file_contents[header_lines - 1].split('\t')):
        if header == 'Ewe/V':
            potential_key = key
        if header == '<I>/mA':
            current_key = key
        if header == 'cycle number':
            cycle_key = key
            # Seems to be CV...
            file_type = 'CV'
        if header == 'Analog OUT/V':
            rpm_key = key
        if header == 'time/s':
            time_key = key

    # Go through file, line by line starting after Header
    if file_type == 'CV':
        loop_key = cycle_key

    if file_type == 'LSV':
        loop_key = rpm_key

    # prepare data structure for dataframe
    raw_data = {
        'potential': [],
        'current': [],
        'cycle': [], 
        'time': [],
    }

    for line in file_contents[header_lines:]:
        # Split the line at tabs
        line = line.split('\t')

        # extract the values from each line
        potential = lm.to_float(line[potential_key])
        current = lm.to_float(line[current_key])
        time = lm.to_float(line[time_key])
        cycle_number = round(lm.to_float(line[loop_key]))

        # save the values to the raw data structure for later
        raw_data['potential'].append(potential)
        raw_data['current'].append(current)
        raw_data['cycle'].append(cycle_number)
        raw_data['time'].append(time)

    raw_df = pd.DataFrame(raw_data)

    return {
        'file_data': raw_df,
        'speed': meas_speed,
        'path': path
    }


def extract_cycle_keys(file_data):

    # Extract Maxima and Minima from each cycle
    max_keys = []
    min_keys = []
    for cycle_number in file_data.cycle.unique():
        max_keys.append(file_data[file_data.cycle == cycle_number].potential.idxmax())
        min_keys.append(file_data[file_data.cycle == cycle_number].potential.idxmin())

    return [max_keys, min_keys]


def interpolate_cycles(measured_data, cycle_keys, upper_vertice, lower_vertice, resolution):
    # Prepare the cycles list for return
    cycles_df = []
    cycles_original = []

    max_keys, min_keys = cycle_keys

    file_data = measured_data['file_data']

    interp_potential_down = np.linspace(upper_vertice, lower_vertice, round((upper_vertice-lower_vertice)/resolution)+1)
    interp_potential_up = np.flipud(interp_potential_down)

    if max_keys[0] < min_keys[0]:
        # First extreme is upper vertex
        # --> Cycle is upper - lower - upper
        for max_key_index in range(len(max_keys)-1):
            # Get Measured X and Y Data and Interpolate
            down = file_data[max_keys[max_key_index]: min_keys[max_key_index] + 1]
            down = down.drop_duplicates(subset='potential', keep='last')

            up = file_data[min_keys[max_key_index]: max_keys[max_key_index + 1] + 1]
            up = up.drop_duplicates(subset='potential', keep='last')

            original = {
                'potential': np.concatenate([down.potential, up.potential]),
                'current': np.concatenate([down.current, up.current]),
                'cycle': max_key_index+1
            }

            down = down.sort_values(by=['potential'])
            up = up.sort_values(by=['potential'])
            interp_current_down = lm.interpolate(down.potential, down.current, interp_potential_down, method='interp1d')
            interp_current_up = lm.interpolate(up.potential, up.current, interp_potential_up, method='interp1d')

            # Stitch Interpolated Data together
            cycle = {
                'potential': np.concatenate([interp_potential_down[:-1], interp_potential_up]),
                'current': np.concatenate([interp_current_down[:-1], interp_current_up]),
                'cycle': max_key_index+1
            }

            # Append to the cycles list
            cycles_df.append(pd.DataFrame(cycle))
            cycles_original.append(pd.DataFrame(original))
    else:
        # First extreme is lower vertex
        # --> Cycle is lower - upper - lower
        raise Exception('direction yet unimplemented')

    return {
        'path': measured_data['path'],
        'speed': measured_data['speed'],
        'data': pd.concat(cycles_df),
        'original': pd.concat(cycles_original)
    }


def read_mpt_series(path_list, upper_vertice, lower_vertice, resolution, bar):

    # prepare data object
    series_data = []
    original_data = []

    for path in path_list:
        # read the files data into an object
        measured_data = read_mpt(path)
        cycle_keys = extract_cycle_keys(measured_data['file_data'])
        measurement = interpolate_cycles(measured_data, cycle_keys, upper_vertice, lower_vertice, resolution)

        original_data.append(measurement['original'])

        speed = measurement['speed']
        series_data.append(measurement)
        bar.next()

    print("finished reading {file_count} files".format(file_count=len(path_list)))

    series_data.sort(key=lambda file_data: file_data['speed'])

    print("sorted list by measurement speed")

    speed_series = {
        'cycle': series_data[0]['data'].cycle.values,
        'potential': series_data[0]['data'].potential.values,
    }

    for file_data in series_data:
        cycle = file_data['data']
        speed_series[file_data['speed']] = cycle.current.values

    print("finished converting to pandas data frame")

    return pd.DataFrame(speed_series), original_data
