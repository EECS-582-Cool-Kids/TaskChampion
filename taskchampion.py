'''Entry point for the TaskChampion Application.'''

import sys
from PySide6 import QtCore, QtWidgets
from taskw_ng import TaskWarrior
from typing import TypeAlias, Literal
from utils.task import Task, status_t, priority_t

# class TableRow()
w = TaskWarrior()

def hello():
    print("hello world")

class Checkbox:
    def __init__(self, taskID : str):
        self.task = Task(w.get_task(uuid=taskID)[1])
        self.task_text: str = str(self.task.get_description())

        self.checkbox = QtWidgets.QCheckBox(self.task_text)
        self.checkbox.setChecked(self.task.get_status() == 'completed')

        self.checkbox.stateChanged.connect(lambda: self.checkCheckbox()) # Have to pass 

        
    @QtCore.Slot()
    def checkCheckbox(self):
        if self.checkbox.isChecked():
            w.task_update({"uuid": self.task.get_uuid(), "status": 'completed'})

        else:
            w.task_update({"uuid": self.task.get_uuid(), "status": 'pending'})

    def linkToLayout(self, layout : QtWidgets.QVBoxLayout):
        layout.addWidget(self.checkbox)


class TaskChampionWidget(QtWidgets.QWidget):
    '''The main widget for the Task Champion application.'''
    def __init__(self):
        super().__init__()

        # Initialize the layout
        self.qtLayout = QtWidgets.QVBoxLayout(self)
    
    def addTask(self, newTask: Task) -> None:
        layout = QtWidgets.QHBoxLayout(self)
        task_name = QtWidgets.QTextEdit(str(newTask.get_description()))
        
        task_check = Checkbox(str(newTask.get_uuid()))

        # task_check_cell = QtWidgets.QTableWidgetItem()

        layout.addWidget(task_check.checkbox)
        layout.addWidget(task_name)
        # self.table.setItem(rowNum,  1, QtWidgets.QTableWidgetItem(task_check.checkbox))
        self.qtLayout.addLayout(layout)
        

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