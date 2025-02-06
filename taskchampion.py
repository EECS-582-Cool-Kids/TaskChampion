'''Entry point for the TaskChampion Application.'''

import sys
from PySide6 import QtCore, QtWidgets
from taskw_ng import TaskWarrior
from typing import TypeAlias, Literal
from utils.task import Task, status_t, priority_t
from components.checkbox import Checkbox
from components.textbox import Textbox
from components import TaskRow, COLS, ALIGN
from utils import w


class TaskChampionWidget(QtWidgets.QWidget):
    '''The main widget for the Task Champion application.'''
    def __init__(self):
        super().__init__()

        # Initialize the layout
        self.qtLayout = QtWidgets.QVBoxLayout(self)
        self.grid = QtWidgets.QGridLayout()
        self.qtLayout.addLayout(self.grid)

        
        
        self.addHeader()
        self.rows = 1

        # self.grid.setColumnStretch()

        # self.headers = QtWidgets.
        # self.tabs = QtWidgets.QTabWidget()
        # self.lesserLayout = QtWidgets.QVBoxLayout()
        # self.tabs.addTab(self.lesserLayout, 'Tab Name')
        # self.qtLayout.addChildWidget(self.tabs)
    
    def addTask(self, newTask: Task) -> None:
        # layout = QtWidgets.QHBoxLayout()
        # # task_name = QtWidgets.QTextEdit(str(newTask.get_description()))
        uuid = str(newTask.get_uuid())
        # task_check = Checkbox(uuid)
        # task_name = Textbox(uuid, 'description')

        # layout.addWidget(task_check.checkbox)
        # layout.addWidget(task_name.textbox)

        row = TaskRow(uuid)
        row.insert(self.grid, self.rows)
        self.rows += 1
        
        # self.qtLayout.addLayout(layout.row)
        
    def addHeader(self):
        self.grid.setRowStretch(0, 0)

        self.grid.addWidget(QtWidgets.QLabel("Completed?"), 0, 0, ALIGN.TL)
        self.grid.setColumnStretch(0, 4)

        for i in range(len(COLS)):
            self.grid.addWidget(QtWidgets.QLabel(COLS[i]), 0, i+1, ALIGN.TL)
            self.grid.setColumnStretch(i, 0)



class TaskChampionGUI:
    '''The main application class for Task Champion.'''
    def __init__(self):
        # Initialize the Qt App and TaskWarrior objects
        self.qtapp = QtWidgets.QApplication([])
        # self.warrior = TaskWarrior()

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
    tasks = w.load_tasks()

    for task in [*tasks['pending'], *tasks['completed']]:
        app.mainWidget.addTask(Task(task))
        

    sys.exit(app.onExit())