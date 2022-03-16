from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

import numpy as np
import random

# DEPRECT

class FileInputTab(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        loadUi('tabs/file_input.ui', self)