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

mainData = biologic.read_mpt_series(mainPath, 0.02, 3.0, 2981)

# for speed in sorted(mainData):
#     xList.append(math.sqrt(speed))
#     yList.append(mainData[speed]['loops'][4]['current'][1700]/math.sqrt(speed))



