"""
 *  Module Name: taskchampion.py
 *  Purpose: Entry point for the TaskChampion Application.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Jacob Wilkus, Ethan Berkley, Mo Morgan
 *  Date: 2/15/2025
 *  Last Modified: 2/15/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

import sys
from PySide6 import QtWidgets
from utils.task import Task
from components import TaskRow, COLS, ALIGN, menubar
from utils import taskWarriorInstance


class TaskChampionWidget(QtWidgets.QWidget):
    """The main widget for the Task Champion application."""
    def __init__(self):
        super().__init__()

        # Initialize the layout
        self.qtLayout = QtWidgets.QVBoxLayout(self)
        self.grid = QtWidgets.QGridLayout()
        self.qtLayout.addLayout(self.grid)

        self.add_header()
        self.rows = 1

        self.menu_bar = None    # declare the window's menu bar
        self.set_menu_bar()     # set the window's menu bar
    
    def add_task(self, new_task: Task) -> None:
        uuid = str(new_task.get_uuid())

        row = TaskRow(uuid)
        row.insert(self.grid, self.rows)
        self.rows += 1
        
    def add_header(self):
        self.grid.setRowStretch(0, 0)

        self.grid.addWidget(QtWidgets.QLabel("Completed?"), 0, 0, ALIGN.TL)
        self.grid.setColumnStretch(0, 4)

        for i in range(len(COLS)):
            self.grid.addWidget(QtWidgets.QLabel(COLS[i]), 0, i+1, ALIGN.TL)
            self.grid.setColumnStretch(i, 0)
            
    def set_menu_bar(self):
        """Sets the menu bar for the application."""
        self.menu_bar = menubar.MenuBar()
        self.layout().setMenuBar(self.menu_bar)

class TaskChampionGUI:
    """The main application class for Task Champion."""
    def __init__(self):
        # Initialize the Qt App and TaskWarrior objects
        self.qt_app = QtWidgets.QApplication([])

        # Initialize the main Qt Widget
        self.mainWidget = TaskChampionWidget()
        self.mainWidget.setWindowTitle("Task Champion")
        self.mainWidget.resize(800, 600) # set basic window size.
        self.mainWidget.show() # show the window

    def on_exit(self) -> int:
        """The behavior for exiting the application."""
        return self.qt_app.exec()

# Program entry point
if __name__ == "__main__":
    app = TaskChampionGUI()
    tasks = taskWarriorInstance.load_tasks()

    for task in [*tasks['pending'], *tasks['completed']]:
        app.mainWidget.add_task(Task(task))

    sys.exit(app.on_exit())