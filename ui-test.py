# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

import numpy as np
import random


class MatplotlibWidget(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        loadUi("matplotlib-test.ui", self)

        self.setWindowTitle("PyQt5 & Matplotlib Example GUI")

        self.pushButton_generate_random_signal.clicked.connect(self.update_graph)

    def update_graph(self):
        fs = 500
        f = random.randint(1, 100)
        ts = 1 / fs
        length_of_signal = 100
        t = np.linspace(0, 1, length_of_signal)

        cosinus_signal = np.cos(2 * np.pi * f * t)
        sinus_signal = np.sin(2 * np.pi * f * t)

        self.MplWidget.canvas.left_plot = self.MplWidget.canvas.figure.add_subplot(1, 2, 1)
        ax = self.MplWidget.canvas.left_plot
        ax.clear()
        ax.plot(t, cosinus_signal, label='cos')
        ax.plot(t, sinus_signal, label='sin')
        ax.legend()
        ax.set_title('Cosinus - Sinus Signal')

        self.MplWidget.canvas.right_plot = self.MplWidget.canvas.figure.add_subplot(1, 2, 2, sharex=self.MplWidget.canvas.left_plot)
        self.MplWidget.canvas.right_plot.clear()
        self.MplWidget.canvas.right_plot.plot(t, cosinus_signal)
        self.MplWidget.canvas.right_plot.plot(t, sinus_signal)
        self.MplWidget.canvas.right_plot.legend(('cosinus', 'sinus'), loc='upper right')
        self.MplWidget.canvas.right_plot.set_title('Cosinus - Sinus Signal')

        # self.MplWidget.canvas.axes[0] = self.MplWidget.canvas.figure.add_subplot(1, 2, 2)
        # self.MplWidget.canvas.axes[1].clear()
        # self.MplWidget.canvas.axes[1].plot(t, cosinus_signal)
        # self.MplWidget.canvas.axes[1].plot(t, sinus_signal)
        # self.MplWidget.canvas.axes[1].legend(('cosinus', 'sinus'), loc='upper right')
        # self.MplWidget.canvas.axes[1].set_title('Cosinus - Sinus Signal')
        self.MplWidget.canvas.draw()


app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()