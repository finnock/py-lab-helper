from tkinter import Tk
from tkinter.filedialog import askopenfilename
import math
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import pylabhelper.biologic as biologic

# Suppress the TK window, since only the dialog is intended
Tk().withdraw()

# Ask the user for the first file in the series
mainPath = askopenfilename(filetypes=[("BioLogic .mpt", "*.mpt")])  # Full path will be returned as string

mainData = biologic.read_mpt_series(mainPath)

xList = []#[0.31622776601683794, 0.7071067811865476, 1.0, 2.23606797749979, 3.1622776601683795, 4.47213595499958, 7.0710678118654755, 8.366600265340756, 10.0, 11.180339887498949, 12.24744871391589, 13.038404810405298, 14.142135623730951, 15.811388300841896, 17.320508075688775]
yList = []#[-0.08591893769235956, -0.10915167890445245, -0.134795086816889, -0.25756079522422537, -0.30147575882182337, -0.35267842204766364, -0.4284477912588174, -0.4626164620242261, -0.495080268755553, -0.5230727786251737, -0.5445489094351784, -0.5613831839160777, -0.5748240959734214, -0.5969746363190107, -0.589636191623058]

for speed in sorted(mainData):
    xList.append(math.sqrt(speed))
    yList.append(mainData[speed]['loops'][4]['current'][1700]/math.sqrt(speed))

fig, ax = plt.subplots()
plt.xlabel(r'$\sqrt{v}$')
plt.ylabel(r'$I/\sqrt{v}$')

ax.plot(xList, yList, linewidth=2.0, marker="x", label="Current: ### mA")

rSq = 1
startCut = 3
colormap = plt.get_cmap('tab10')
while True:
    x = np.array(xList[:startCut]).reshape((-1, 1))
    y = np.array(yList[:startCut])

    model = LinearRegression().fit(x, y)

    rSq = model.score(x, y)
    print('R²:', rSq)
    ax.axline((0, model.intercept_), color=colormap((startCut-3)/10), slope=model.coef_[0], label='Linear Fit')
    startCut += 1
    if not (rSq > 0.935 and startCut <= 15):
        break

ax.legend()
plt.show()


