'''Entry point for the TaskChampion Application.'''

import sys
from PySide6 import QtCore, QtWidgets
from taskw_ng import TaskWarrior
from typing import TypeAlias, Literal
from utils.task import Task, status_t, priority_t
# from components.checkbox import Checkbox
# from components.textbox import Textbox
from components import AddTaskDialog, TaskRow, COLS, ALIGN
from utils import taskWarriorInstance

class GridWidget(QtWidgets.QWidget):
    '''The widget that corresponds to a module'''
    ROW_HEIGHT=50
    DEFAULT_ROWS=10

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
        self.rowArr: list[TaskRow] = []

        self.addHeader()
        self.fillGrid()

    def addTask(self, newTask: Task) -> None:
        
        self.rows += 1
            
        uuid = str(newTask.get_uuid())

        if self.grid.rowCount() == self.rows:
            self.setMinimumHeight(self.rows * self.ROW_HEIGHT)

            self.rowArr.append(TaskRow(self.rows, uuid))
            # Row inserts itself into the grid, insertion logic is handled in `TaskRow` obj.
            # Note that this may be tricky when changing order of tasks w.r.t column sorting, 
            # as that logic will happen in this class.
            # but idk what method we will use for sorting, for all I know qt makes it very easy.    
        
        self.rowArr[self.rows-1].update_task(uuid)
        self.rowArr[self.rows-1].insert(self.grid, self.rows)

        

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

    def fillGrid(self):
        for i in range(self.DEFAULT_ROWS):
            self.rowArr.append(TaskRow(i, ""))
            self.rowArr[i].insert(self.grid, i+1)
        self.setMinimumHeight(self.DEFAULT_ROWS * self.ROW_HEIGHT)

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
        self.addButton = QtWidgets.QPushButton("Add Task")

        self.addButton.setMaximumWidth(100)
        self.addButton.clicked.connect(lambda: self.addTask())
        # self.addButton.connect(self.addButton, QtCore.SIGNAL("clicked()"), self.addTask)

        self.qtLayout.addWidget(self.addButton)
        
        self.qtLayout.addWidget(self.mainTab)
        self.grids = [GridWidget(), GridWidget()]
        self.mainTab.addTab(self.grids[0].scrollArea, "Example Tab")
        self.mainTab.addTab(self.grids[1].scrollArea, "Example Empty Tab")

        self.currentGrid = 0

        self.addTaskDialog : AddTaskDialog = AddTaskDialog()
    
    def addTask(self):
        '''Add a task to the GUI list and link it to a new task in TaskWarrior.'''

        newTaskDetails : AddTaskDialog.TaskDetails | None = self.addTaskDialog.addTask()
        
        if newTaskDetails == None:
            return

        newTask : Task = Task(taskWarriorInstance.task_add(newTaskDetails.description, newTaskDetails.tag))
        
        newTask.set_priority(newTaskDetails.priority)
        newTask.set_project(newTaskDetails.project)
        newTask.set_recur(newTaskDetails.recurrence)

        taskWarriorInstance.task_update(newTask)
        self.grids[self.currentGrid].addTask(newTask)

class TaskChampionGUI:
    '''The main application class for Task Champion.'''
    def __init__(self):
        # Initialize the Qt App and TaskWarrior objects
        self.qtapp = QtWidgets.QApplication([])
        

        # Initialize the main Qt Widget
        self.mainWidget = TaskChampionWidget()
        self.mainWidget.setWindowTitle("Task Champion")
        self.mainWidget.resize(800, 400) # set basic window size.
        self.mainWidget.show() # show the window
        self._styleStr = ""
        with open ('styles/test.qss', 'r')as f:
            self._styleStr = f.read()

        self.loadStyles()

    def loadStyles(self):
        self.qtapp.setStyleSheet(self._styleStr)

    def onExit(self) -> int:
        '''The behavior for exiting the application.'''
        return self.qtapp.exec()

# Program entry point
if __name__ == "__main__":
    app = TaskChampionGUI()
    tasks = taskWarriorInstance.load_tasks()

    # Add both pending and completed tasks.
    for task in [*tasks['pending'], *tasks['completed']]:
        app.mainWidget.grids[0].addTask(Task(task))
    
    app.loadStyles()

    sys.exit(app.onExit())
