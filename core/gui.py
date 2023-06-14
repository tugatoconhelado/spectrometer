import os
from PySide2.QtCore import QObject
from PySide2.QtWidgets import QApplication

class ExperimentGui(QObject):

    def __init__(self):

        super().__init__()

    def setTheme(self):

        path = os.path.join('themes', 'Darkeum.qss')
        with open(path, 'r') as file:
            stylesheet = file.read()

        QApplication.instance().setStyleSheet(stylesheet)


if __name__ == '__main__':

    gui = ExperimentGui()