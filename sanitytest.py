import tkinter as tk
from tkinter import ttk

# Suppress the TK window, since only the dialog is intended
#tk.Tk().withdraw()


root = tk.Tk()
root.title("Faradayic/Capacitive Current Analysis")
tabControl = ttk.Notebook(root)

input_data_tab = ttk.Frame(tabControl)
regression_data_tab = ttk.Frame(tabControl)
fc_analysis_tab = ttk.Frame(tabControl)

tabControl.add(input_data_tab, text='Input Data')
tabControl.add(regression_data_tab, text='Regression Data')
tabControl.add(fc_analysis_tab, text='FC-Analysis')
tabControl.pack(expand=1, fill="both")

input_data_tab.columnconfigure(0, weight=1)
input_data_tab.columnconfigure(1, weight=1)
input_data_tab.rowconfigure(1, weight=1)
input_data_tab.rowconfigure(3, weight=1)


def update_speed(speed_value):
    print(speed_value)


speed_list = (1, 2, 3)
speed_val = tk.IntVar()

speed_opt = ttk.OptionMenu(root, speed_val, speed_list[2], *speed_list)
speed_opt.pack()

root.mainloop()




