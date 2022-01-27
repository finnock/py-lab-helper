from tkinter import *
from tkinter import scrolledtext
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

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

mainPath = askopenfilename(filetypes=[("BioLogic .mpt", "*.mpt")])

mainData = biologic.read_mpt(mainPath)
originalData = biologic.reset_cycles(mainData['file_data'])

root = tk.Tk()
root.title("Tab Widget")
tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Tab 1')
tabControl.add(tab2, text='Tab 2')
tabControl.pack(expand=1, fill="both")

ttk.Label(tab2,
          text="Lets dive into the\
          world of computers").grid(column=0,
                                    row=0,
                                    padx=30,
                                    pady=30)

fig = Figure()
ax = fig.add_subplot()
colors = plt.cm.tab20(np.linspace(0,1,20))
ax.set_prop_cycle(color=colors)

df = mainData['file_data']

for cycle in df.cycle.unique():
    if cycle in ['start', 'end']:
        ax.plot(df[df.cycle == cycle].time, df[df.cycle == cycle].potential, linestyle='dashed', color='grey')
    else:
        ax.plot(df[(df.cycle == cycle) & (df.direction == 'down')].time, df[(df.cycle == cycle) & (df.direction == 'down')].potential)
        ax.plot(df[(df.cycle == cycle) & (df.direction == 'up')].time, df[(df.cycle == cycle) & (df.direction == 'up')].potential)

canvas = FigureCanvasTkAgg(fig, master=tab1)
canvas.draw()

# canvas2 = FigureCanvasTkAgg(fig, master=tab1)
# canvas2.draw()

def update_cycle(cycle_number):
    ax.clear()
    ax.plot(df[df.cycle == int(cycle_number)].potential, df[df.cycle == int(cycle_number)].current)
    canvas.draw()


toolbar = NavigationToolbar2Tk(canvas, tab1, pack_toolbar=False)
toolbar.update()

# toolbar2 = NavigationToolbar2Tk(canvas2, tab1, pack_toolbar=False)
# toolbar2.update()

cycle_slider = Scale(tab1, orient=HORIZONTAL, from_=1, to=5, label='Cycle', command=update_cycle)

canvas.get_tk_widget().grid(column=0, row=0, sticky=E+W+N+S)
# canvas2.get_tk_widget().grid(column=1, row=0, sticky=E+W+N+S)
toolbar.grid(column=0, row=2)
cycle_slider.grid(column=0, row=1)
# toolbar2.grid(column=1, row=2)
tab1.rowconfigure(0, weight=1)
tab1.columnconfigure(0, weight=1)
tab1.columnconfigure(1, weight=1)

root.mainloop()