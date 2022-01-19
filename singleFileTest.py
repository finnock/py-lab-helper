# import sys
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import matplotlib.pyplot as plt
import pandas as pd

import pylabhelper.biologic as biologic

from progress.bar import Bar


# Suppress the TK window, since only the dialog is intended
Tk().withdraw()

# Ask the user for the first file in the series
pathList = askopenfilenames(filetypes=[("BioLogic .mpt", "*.mpt")])  # Full path will be returned as string
# mainPath = "C:/Users/Jan/Documents/data/testdaten-fuer-FC-Auswertung/B21-11-MPNC-23-1000-etched-CV 0.1 mVs to 300 mVs_0.02V to 3.0 Vstart-10.11.2021_01_CV_C08.mpt"

bar = Bar('Processing', max=len(pathList))

data, original_data = biologic.read_mpt_series(pathList, upper_vertice=3.0, lower_vertice=0.02, resolution=0.001, bar=bar)

bar.finish()

import numpy as np
from sklearn.linear_model import LinearRegression

x = np.sqrt(list(data.columns.values[2:])).reshape((-1, 1))
cycle = data[data.cycle == 4]

fc_data = {
    'index': [],
    'potential': [],
    'faradayic': [],
    'capacitive': [],
    'rSq': []
}

speeds = data.columns.values[2:]
cutoff = 4

for index, row in cycle.iterrows():
    y = []
    for speed in speeds:
        y.append(row[speed]/np.sqrt(speed))
    model = LinearRegression().fit(x[:cutoff], y[:cutoff])
    rSq = model.score(x[:cutoff], y[:cutoff])
    faradayic = model.intercept_
    capacitive = model.coef_[0]

    fc_data['index'].append(index)
    fc_data['potential'].append(row['potential'])
    fc_data['faradayic'].append(faradayic)
    fc_data['capacitive'].append(capacitive)
    fc_data['rSq'].append(rSq)

fc_data = pd.DataFrame(fc_data)

print('done')

# x = fc_data['potential']
# y = np.divide(list(fc_data.faradayic.values), list(fc_data.capacitive.values))
#
# fig, ax = plt.subplots()
# plt.xlabel(r'potential in $V$')
# plt.ylabel(r'faradayic/capacitive')
# ax.plot(x, y, linewidth=2.0) #label="Potential: {potential} V".format(potential=row['potential']))
# ax.legend()
# plt.show()



selector = 11
x_original = original_data[selector][original_data[selector].cycle == 4].potential
y_original = original_data[selector][original_data[selector].cycle == 4].current

x_interp = cycle.potential
y_interp = cycle[300]

fig, ax = plt.subplots()
plt.xlabel(r'potential in $V$')
plt.ylabel(r'current in $mA$')
ax.plot(x_interp, y_interp, color='blue', linewidth=2.0, label='interpolated 1 mv/s')
ax.plot(x_original, y_original, color='red', linewidth=2.0, label='original 1 mv/s')
ax.legend()
plt.show()

x = fc_data['potential']
y = np.divide(list(fc_data.faradayic.values), list(fc_data.capacitive.values))

fig, ax = plt.subplots()
plt.xlabel(r'potential in $V$')
plt.ylabel(r'a.u.')
ax.plot(x, fc_data.faradayic, color='red', linewidth=2.0, label="faradayic")
ax.plot(x, fc_data.capacitive, color='blue', linewidth=2.0, label="capacitive")
ax.plot(x, fc_data.rSq, color='green', linewidth=2.0, label=r'$R^2$')
ax.legend()
plt.show()


x = np.sqrt(list(data.columns.values[2:])).reshape((-1, 1))

def subplot(row_index):
    fig, ax = plt.subplots()
    plt.xlabel(r'$\sqrt{v}$')
    plt.ylabel(r'$I/\sqrt{v}$')

    y = []
    row = cycle.loc[row_index]
    for speed in speeds:
        y.append(row[speed] / np.sqrt(speed))

    ax.plot(x, y, linewidth=2.0, marker="x", label="Potential: {potential} V".format(potential=row['potential']))

    model = LinearRegression().fit(x[:4], y[:4])
    rSq = model.score(x[:4], y[:4])
    faradayic = model.intercept_
    capacitive = model.coef_[0]

    print('R²:', rSq)
    ax.axline((0, faradayic), color='green', slope=capacitive, label='Linear Fit R²: {rsq:.2f}'.format(rsq=rSq))

    ax.legend()
    plt.show()

# sys.exit(0)

# for speed in sorted(mainData):
#     xList.append(math.sqrt(speed))
#     yList.append(mainData[speed]['loops'][4]['current'][1700]/math.sqrt(speed))



