'''Entry point for the TaskChampion Application.'''

import sys
from PySide6 import QtCore, QtWidgets
from taskw_ng import TaskWarrior

class TaskChampionWidget(QtWidgets.QWidget):
    '''The main widget for the Task Champion application.'''
    def __init__(self):
        super().__init__()

        # Initialize the layout
        self.qtLayout = QtWidgets.QVBoxLayout(self)

class TaskChampionGUI:
    '''The main application class for Task Champion.'''
    def __init__(self):
        # Initialize the Qt App and TaskWarrior objects
        self.qtapp = QtWidgets.QApplication([])
        self.warrior = TaskWarrior()

        # Initialize the main Qt Widget
        self.mainWidget = TaskChampionWidget()
        self.mainWidget.setWindowTitle("Task Champion")
        self.mainWidget.resize(800, 600) # set basic window size.
        self.mainWidget.show() # show the window

    def onExit(self) -> int:
        '''The behavior for exiting the application.'''
        return self.qtapp.exec()

# Program entry point
if __name__ == "__main__":
    app = TaskChampionGUI()
    sys.exit(app.onExit())