from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pylabhelper.biologic as biologic

import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

# Suppress the TK window, since only the dialog is intended
tk.Tk().withdraw()

# Ask the user for the first file in the series
mainPath = askopenfilename(filetypes=[("BioLogic .mpt", "*.mpt")])  # Full path will be returned as string

data = biologic.read_mpt(mainPath)

root = tk.Tk()
root.title("FC Analysis - BioLogic Data version")
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

fig = Figure(figsize=(5,4), dpi=100)
ax = fig.add_subplot()
ax.plot([1,2,3], [1,2,3])

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
