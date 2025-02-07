'''Entry point for the TaskChampion Application.'''

import sys
from PySide6 import QtCore, QtWidgets
from taskw_ng import TaskWarrior
from typing import TypeAlias, Literal
from utils.task import Task, status_t, priority_t
from components.checkbox import Checkbox
from components.textbox import Textbox
from components import TaskRow, COLS, ALIGN
from utils import taskWarriorInstance


class TaskChampionWidget(QtWidgets.QWidget):
    '''The main widget for the Task Champion application.'''
    def __init__(self):
        super().__init__()

        # Initialize the layout
        # Will be used for more than just holding the grid at some point.
        self.qtLayout = QtWidgets.QVBoxLayout(self)

        # The object that holds info on all the tasks *in this module*.
        # At some point, we *might* want to have an array of grids?
        self.grid = QtWidgets.QGridLayout()
        self.qtLayout.addLayout(self.grid)

        self.addHeader()
        self.rows = 1
    
    def addTask(self, newTask: Task) -> None:
        
        uuid = str(newTask.get_uuid())
        row = TaskRow(uuid)
        # Row inserts itself into the grid, insertion logic is handled in `TaskRow` obj.
        # Note that this may be tricky when changing order of tasks w.r.t column sorting, 
        # as that logic will happen in this class.
        # but idk what method we will use for sorting, for all I know qt makes it very easy.
        row.insert(self.grid, self.rows)
        self.rows += 1
        
    def addHeader(self):
        # Make header row take up as little vertical space as it needs.
        self.grid.setRowStretch(0, 0)

        # QLabel is just simple text.
        self.grid.addWidget(QtWidgets.QLabel("Completed?"), 0, 0, ALIGN.TL)
        # TODO: may be no point in setting column stretch like this and below,
        # Consider changing.
        self.grid.setColumnStretch(0, 4)

        for i in range(len(COLS)):
            self.grid.addWidget(QtWidgets.QLabel(COLS[i]), 0, i+1, ALIGN.TL)
            self.grid.setColumnStretch(i, 0)



class TaskChampionGUI:
    '''The main application class for Task Champion.'''
    def __init__(self):
        # Initialize the Qt App and TaskWarrior objects
        self.qtapp = QtWidgets.QApplication([])

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
    tasks = taskWarriorInstance.load_tasks()

    # Add both pending and completed tasks.
    for task in [*tasks['pending'], *tasks['completed']]:
        app.mainWidget.addTask(Task(task))
        

    sys.exit(app.onExit())