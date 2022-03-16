# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QSizePolicy

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure


class MplWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        loadUi("mplWidget.ui", self)

        self.canvas = FigureCanvas(Figure())
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.canvasContainer.addWidget(self.canvas)
        self.toolbarContainer.addWidget(self.toolbar)
        #
        # toolbar_frame = QHBoxLayout()
        # spacer = QSpacerItem(0, 0, QSizePolicy.Expanding)
        # toolbar_frame.addSpacerItem(spacer)
        # toolbar_frame.addWidget()
        # toolbar_frame.addSpacerItem(spacer)
        #
        # vertical_layout.addItem(toolbar_frame)
        # vertical_layout.setContentsMargins(0, 0, 0, 0)
        #
        # self.setLayout(vertical_layout)