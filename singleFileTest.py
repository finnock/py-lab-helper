# import sys
import sys
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilenames
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import pylabhelper.biologic as biologic
from matplotlib.figure import Figure

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from sklearn.linear_model import LinearRegression


# Suppress the TK window, since only the dialog is intended
#tk.Tk().withdraw()


# x = fc_data['potential']
# y = np.divide(list(fc_data.faradayic.values), list(fc_data.capacitive.values))
#
# fig, ax = plt.subplots()
# plt.xlabel(r'potential in $V$')
# plt.ylabel(r'faradayic/capacitive')
# ax.plot(x, y, linewidth=2.0) #label="Potential: {potential} V".format(potential=row['potential']))
# ax.legend()
# plt.show()

# ############################ UI ############################
#

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

# ###################


# Ask the user for the list of Files used for the analysis
pathList = askopenfilenames(filetypes=[("BioLogic .mpt", "*.mpt")])  # Full path will be returned as string

# Read all files as an interpolated series indexed by the measurement speed. Vertices and resolution are used for the
# interpolation. Optional: set interpolation_method using argument (list found in pylabhelper.math.py)
interpolated_data, original_data = biologic.read_mpt_series(pathList,
                                                            upper_vertice=3.0,
                                                            lower_vertice=0.02,
                                                            resolution=0.001)

fc_data = biologic.fc_analysis(interpolated_data, 4)

print('fc analysis done')


# ##################### Input Data Tab ########################
#

input_data_tab.columnconfigure(0, weight=1)
input_data_tab.columnconfigure(1, weight=1)
input_data_tab.rowconfigure(1, weight=1)
input_data_tab.rowconfigure(3, weight=1)

cycle_val = tk.IntVar()

speed_list = interpolated_data.columns[2:]
speed_val = tk.StringVar()

org_df = {}

# org_df = next(item for item in original_data if item['speed'] == float(speed_val.get()))['data']
# org_pot = org_df.potential
# org_tim = org_df.time

# ### INTERPOLATION PLOT ###
interpolation_fig, interpolation_ax = plt.subplots()
interpolation_ax.set_xlabel(r'potential in $V$')
interpolation_ax.set_ylabel(r'current in $mA$')

interpolation_canvas = FigureCanvasTkAgg(interpolation_fig, master=input_data_tab)
interpolation_canvas.draw()
interpolation_canvas.get_tk_widget().grid(column=1, row=1, sticky='NEWS')

interpolation_toolbar = NavigationToolbar2Tk(interpolation_canvas, input_data_tab, pack_toolbar=False)
interpolation_toolbar.update()
interpolation_toolbar.grid(column=1, row=2)

def interpolation_update_cycle(cycle_number):
    org_df = next(item for item in original_data if item['speed'] == float(speed_val.get()))['data']
    org_pot = org_df[org_df.cycle == int(cycle_number)].potential
    org_cur = org_df[org_df.cycle == int(cycle_number)].current
    interpolation_ax.clear()
    interpolation_ax.plot(
        interpolated_data[interpolated_data.cycle == int(cycle_number)].potential,
        interpolated_data[interpolated_data.cycle == int(cycle_number)][float(speed_val.get())],
        color='blue', linewidth=2.0, label='interpolated ___ mv/s'
    )
    interpolation_ax.plot(org_pot, org_cur, color='red', linewidth=1.0, label='original ___ mv/s')
    interpolation_ax.legend()
    interpolation_canvas.draw()

# ### TIME POTENTIAL PLOT ###

time_potential_fig, time_potential_axes = plt.subplots(2, 1)
colors_tab_20 = plt.cm.tab20(np.linspace(0,1,20))

time_potential_axes[0].set_xlabel(r'time in s')
time_potential_axes[0].set_ylabel(r'potential in $V$')

time_potential_axes[1].set_xlabel(r'time in s')
time_potential_axes[1].set_ylabel(r'potential in $V$')
time_potential_axes[1].set_prop_cycle(color=colors_tab_20)

time_potential_canvas = FigureCanvasTkAgg(time_potential_fig, master=input_data_tab)
time_potential_canvas.draw()
time_potential_canvas.get_tk_widget().grid(column=0, row=1, sticky='NEWS')

time_potential_toolbar = NavigationToolbar2Tk(time_potential_canvas, input_data_tab, pack_toolbar=False)
time_potential_toolbar.update()
time_potential_toolbar.grid(column=0, row=2)


def update_speed(speed):
    print(speed)
    org_df = next(item for item in original_data if item['speed'] == float(speed))['data']
    org_pot = org_df.potential
    org_tim = org_df.time
    time_potential_axes[0].clear()
    time_potential_axes[0].plot(org_tim, org_pot, color='grey', linewidth=2.0, label='Complete File')
    time_potential_axes[0].legend()
    time_potential_axes[1].clear()
    for cycle in org_df.cycle.unique():
        if cycle in ['start', 'end']:
            time_potential_axes[1].plot(
                org_df[org_df.cycle == cycle].time,
                org_df[org_df.cycle == cycle].potential, linestyle='dashed', color='grey'
            )
        else:
            time_potential_axes[1].plot(
                org_df[(org_df.cycle == cycle) & (org_df.direction == 'down')].time,
                org_df[(org_df.cycle == cycle) & (org_df.direction == 'down')].potential
            )
            time_potential_axes[1].plot(
                org_df[(org_df.cycle == cycle) & (org_df.direction == 'up')].time,
                org_df[(org_df.cycle == cycle) & (org_df.direction == 'up')].potential
            )
    time_potential_axes[1].legend()
    time_potential_canvas.draw()
    interpolation_update_cycle(cycle_val.get())

cycle_slider = tk.Scale(input_data_tab, variable=cycle_val, orient=tk.HORIZONTAL, from_=1, to=5, label='Cycle', command=interpolation_update_cycle)

# interpolation_update_cycle(cycle_slider.get())
cycle_slider.grid(column=1, row=3)

speed_opt = ttk.OptionMenu(input_data_tab, speed_val, speed_list[0], *speed_list, command=update_speed)
speed_opt.grid(column=0, row=0, columnspan=2)

update_speed(speed_val.get())
# ###########################



#
# ##################### FC Analysis Tab ########################


fc_analysis_tab.columnconfigure(0, weight=1)
fc_analysis_tab.rowconfigure(0, weight=1)

x = fc_data['potential']
y = np.divide(list(fc_data.faradayic.values), list(fc_data.capacitive.values))

fig, ax = plt.subplots()
plt.xlabel(r'potential in $V$')
plt.ylabel(r'a.u.')
ax.plot(x, fc_data.faradayic, color='red', linewidth=2.0, label="faradayic")
ax.plot(x, fc_data.capacitive, color='blue', linewidth=2.0, label="capacitive")
ax.plot(x, fc_data.rSq, color='green', linewidth=2.0, label=r'$R^2$')
ax.legend()

canvas = FigureCanvasTkAgg(fig, master=fc_analysis_tab)
canvas.draw()
canvas.get_tk_widget().grid(column=0, row=0, sticky='NEWS')

toolbar = NavigationToolbar2Tk(canvas, fc_analysis_tab, pack_toolbar=False)
toolbar.update()
toolbar.grid(column=0, row=1)


# regression tab



def subplot(row_index):
    #row_index = int(subplotentry.get())
    data = interpolated_data
    speeds = list(data.columns.values[2:])
    cycle = data[data.cycle == 4]
    x = np.sqrt(list(data.columns.values[2:])).reshape((-1, 1))

    spfig, ax = plt.subplots()
    plt.xlabel(r'$\sqrt{v}$')
    plt.ylabel(r'$I/\sqrt{v}$')

    y = []
    row = cycle.loc[row_index]
    for speed in speeds:
        y.append(row[speed] / np.sqrt(speed))

    ax.plot(x, y, linewidth=2.0, marker="x", label="Potential: {potential} V".format(potential=row['potential']))

    upper = 3

    model = LinearRegression().fit(x[:upper], y[:upper])
    rSq = model.score(x[:upper], y[:upper])
    faradayic = model.intercept_
    capacitive = model.coef_[0]

    print('R²:', rSq)
    ax.axline((0, faradayic), color='green', slope=capacitive, label='Linear Fit R²: {rsq:.2f}'.format(rsq=rSq))

    ax.legend()
    plt.show()

    # spcanvas = FigureCanvasTkAgg(spfig, master=regression_data_tab)
    # spcanvas.draw()
    # spcanvas.get_tk_widget().grid(column=0, row=0, sticky='NEWS')
    #
    # sptoolbar = NavigationToolbar2Tk(canvas, regression_data_tab, pack_toolbar=False)
    # sptoolbar.update()
    # sptoolbar.grid(column=0, row=1)


# subplotentry = tk.Entry(regression_data_tab, text='18211')
# subplotentry['state'] = 'normal'
# subplotentry.pack()
#
# tk.Button(regression_data_tab, text='Plot', command=subplot).pack()

root.mainloop()




