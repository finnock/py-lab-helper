# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QSizePolicy

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure


class MplWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        toolbar_frame = QHBoxLayout()
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding)
        toolbar_frame.addSpacerItem(spacer)
        toolbar_frame.addWidget(NavigationToolbar(self.canvas, self))
        toolbar_frame.addSpacerItem(spacer)

        vertical_layout.addItem(toolbar_frame)
        vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(vertical_layout)