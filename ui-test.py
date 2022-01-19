import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt

import pylabhelper.biologic as biologic
from tkinter.filedialog import askopenfilename

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np

# Suppress the TK window, since only the dialog is intended
tk.Tk().withdraw()

mainPath = askopenfilename(filetypes=[("BioLogic .mpt", "*.mpt")])  # Full path will be returned as string

print(mainPath)

mainData = biologic.read_mpt(mainPath)

root = tk.Tk()
root.title("Tab Widget")
tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Tab 1')
tabControl.add(tab2, text='Tab 2')
tabControl.pack(expand=1, fill="both")

ttk.Label(tab1,
          text="Welcome to \
          GeeksForGeeks").grid(column=0,
                               row=0,
                               padx=30,
                               pady=30)
ttk.Label(tab2,
          text="Lets dive into the\
          world of computers").grid(column=0,
                                    row=0,
                                    padx=30,
                                    pady=30)

colors = plt.cm.tab20(np.linspace(0,1,20))
fig = Figure()
ax = fig.add_subplot()
ax.set_prop_cycle(color=colors)

for cycle in mainData['cycles']:
    ax.plot(cycle[0]['time'], cycle[0]['potential'])
    ax.plot(cycle[1]['time'], cycle[1]['potential'])

canvas = FigureCanvasTkAgg(fig, master=tab1)
canvas.draw()

toolbar = NavigationToolbar2Tk(canvas, tab1, pack_toolbar=False)
toolbar.update()

canvas.get_tk_widget().grid(column=0,
                            row=0,
                            padx=0,
                            pady=15)
toolbar.grid(column=0, row=1)

root.mainloop()