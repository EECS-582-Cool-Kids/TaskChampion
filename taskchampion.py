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




class GridWidget(QtWidgets.QWidget):
    '''The widget that corresponds to a module'''
    ROW_HEIGHT=50
    def __init__(self):
        super().__init__()
        self.setObjectName('GridWidget')
        self.setFixedHeight(200)

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self)

        self.grid = QtWidgets.QGridLayout()

        self.grid.rowMinimumHeight(self.ROW_HEIGHT)

        # print(self.scrollArea.alignment())
        self.setLayout(self.grid)

        self.rows = 0
        self.addHeader()

    def addTask(self, newTask: Task) -> None:
        self.rows += 1
        
        uuid = str(newTask.get_uuid())
        row = TaskRow(uuid)
        # Row inserts itself into the grid, insertion logic is handled in `TaskRow` obj.
        # Note that this may be tricky when changing order of tasks w.r.t column sorting, 
        # as that logic will happen in this class.
        # but idk what method we will use for sorting, for all I know qt makes it very easy.
        row.insert(self.grid, self.rows)

        # self.setMinimumHeight(self.rows * self.ROW_HEIGHT)
        self.setFixedHeight(self.rows * self.ROW_HEIGHT)

    def addHeader(self):
        # Make header row take up as little vertical space as it needs.
        self.grid.setRowStretch(0, 0)
        # self.grid.setContentsMargins(0, 0, 0, 0)
        # self.grid.setHorizontalSpacing(0)
        self.grid.setSpacing(0)
        
        # QLabel is just simple text.
        self.grid.addWidget(QtWidgets.QLabel("Completed?"), 0, 0)
        # TODO: may be no point in setting column stretch like this and below,
        # Consider changing.
        self.grid.setColumnStretch(0, 0)

        for i in range(len(COLS)):
            self.grid.addWidget(QtWidgets.QLabel(COLS[i]), 0, i+1)
            self.grid.setColumnStretch(i+1, 0)



class TaskChampionWidget(QtWidgets.QWidget):
    '''The main widget for the Task Champion application.'''
    def __init__(self):
        super().__init__()
        self.setObjectName('MainWidget')
        
        # Initialize the layout
        # Will be used for more than just holding the grid at some point.
        self.qtLayout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.qtLayout)
        
        self.mainTab = QtWidgets.QTabWidget()
        self.mainTab.setFixedHeight(200)
        self.qtLayout.addWidget(self.mainTab)
        self.grids = [GridWidget()]
        self.mainTab.addTab(self.grids[0].scrollArea, "Example Tab")

class TaskChampionGUI:
    '''The main application class for Task Champion.'''
    def __init__(self):
        # Initialize the Qt App and TaskWarrior objects
        self.qtapp = QtWidgets.QApplication([])
        with open ('styles/test.qss', 'r')as f:
            self.qtapp.setStyleSheet(f.read())

        # Initialize the main Qt Widget
        self.mainWidget = TaskChampionWidget()
        self.mainWidget.setWindowTitle("Task Champion")
        self.mainWidget.resize(800, 100) # set basic window size.
        self.mainWidget.show() # show the window

    def onExit(self) -> int:
        '''The behavior for exiting the application.'''
        return self.qtapp.exec()

# Program entry point
if __name__ == "__main__":
    app = TaskChampionGUI()
    tasks = taskWarriorInstance.load_tasks()

    # Add both pending and completed tasks.
    wid: GridWidget = app.mainWidget.grids[0]
    for task in [*tasks['pending'], *tasks['completed']]:
        wid.addTask(Task(task))
        

    sys.exit(app.onExit())