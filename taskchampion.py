import sys
from PySide6 import QtCore, QtWidgets
from taskw_ng import TaskWarrior

class TaskChampionWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.qtLayout = QtWidgets.QVBoxLayout(self)

class TaskChampionGUI:
    def __init__(self):
        self.qtapp = QtWidgets.QApplication([])
        self.warrior = TaskWarrior()

        self.mainWidget = TaskChampionWidget()
        self.mainWidget.setWindowTitle("Task Champion")
        self.mainWidget.resize(800, 600) # set basic window size.
        self.mainWidget.show() # show the window

    def onExit(self) -> int:
        return self.qtapp.exec()

if __name__ == "__main__":
    app = TaskChampionGUI()
    sys.exit(app.onExit())