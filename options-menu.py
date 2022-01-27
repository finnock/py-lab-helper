# test-optionmenu.py

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
optionList7 = (1,2,3)

# Set up the StringVars for each OptionMenu
v7 = tk.IntVar()

# -------------------------------------------
# om7 is the proper way to declare a
# ttk.OptionMenu, with a default option
# initially set.
om7 = ttk.OptionMenu(root, v7, optionList7[2], *optionList7)

om7.pack()

speed_list = (1, 2, 3)
speed_var = tk.IntVar()

speed_opt = ttk.OptionMenu(root, speed_var, speed_list[2], *speed_list)
speed_opt.pack()

# Execute the mainloop
root.mainloop()