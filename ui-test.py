# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from tabs.file_input import FileInputTab


class MainApplicationWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        loadUi("matplotlib-test.ui", self)

        self.window_tabs.addTab(FileInputTab(), 'Input Data')

        self.actionOpen_CV_Files.triggered.connect(self.open_files)

    def open_files(self):
        path = QFileDialog.getOpenFileName(self, 'Open CV File', '', "BioLogic (*.mpt)")
        print(path[0])


app = QApplication([])
window = MainApplicationWindow()
window.show()
app.exec_()