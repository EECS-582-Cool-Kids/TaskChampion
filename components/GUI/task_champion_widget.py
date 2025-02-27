""" Prologue:
 *  Module Name: task_champion_widget.py
 *  Purpose: Initialization of GUI widgets.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Mo Morgan, Richard Moser, Derek Norton
 *  Date: 2/15/2025
 *  Last Modified: 2/23/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from PySide6 import QtWidgets
from components.Dialogs.add_task_dialog import AddTaskDialog
from components.GUI.grid_widget import GridWidget
from utils.task_api import api
from .menubar import MenuBar
from typing import Callable

class TaskChampionWidget(QtWidgets.QWidget):
    '''The main widget for the Task Champion application.'''
    def __init__(self, load_styles : Callable[[], None]):
        super().__init__()  # Call the parent constructor.
        self.setObjectName('MainWidget')  # Set the object name for styling.
        
        # Initialize the layout
        # Will be used for more than just holding the grid at some point.
        self.qt_layout = QtWidgets.QVBoxLayout(self)   # Create a vertical layout.    
        self.setLayout(self.qt_layout)  # Set the layout of the widget to be the vertical layout.
        
        self.main_tab = QtWidgets.QTabWidget()  # Create a tab widget.
        self.add_button = QtWidgets.QPushButton("Add Task")  # Create a push button.

        self.add_button.setMaximumWidth(100)  # Set the maximum width of the push button.
        self.add_button.clicked.connect(lambda: self.add_task())  # Connect the clicked signal of the push button to the addTask method.
 
        self.qt_layout.addWidget(self.add_button)  # Add the push button to the layout.
        
        self.qt_layout.addWidget(self.main_tab)  # Add the tab widget to the layout.
        self.grids = [GridWidget(load_styles), GridWidget(load_styles)]  # Create a list of grid widgets.
        self.main_tab.addTab(self.grids[0].scroll_area, "Example Tab")  # Add the first grid widget to the tab widget.
        self.main_tab.addTab(self.grids[1].scroll_area, "Example Empty Tab")  # Add the second grid widget to the tab widget.

        self.current_grid = 0  # Set the current grid to 0.

        self.add_task_dialog : AddTaskDialog = AddTaskDialog()  # Create an instance of the AddTaskDialog class.

        self.menu_bar = None    # declare the window's menu bar
        self.set_menu_bar()     # set the window's menu bar
    
    def add_task(self):
        '''Add a task to the GUI list and link it to a new task in TaskWarrior.'''

        newTaskDetails : AddTaskDialog.TaskDetails | None = self.add_task_dialog.add_task()  # Get the details of the new task from the add task dialog.
        
        if newTaskDetails == None:  # If the new task details are None.
            return  # Return.

        api.add_new_task(
            description = newTaskDetails.description, 
            tag         = newTaskDetails.tag,
            priority    = newTaskDetails.priority,
            project     = newTaskDetails.project,
            recur       = newTaskDetails.recurrence,
            due         = newTaskDetails.due,
        )  # Create a new task with the details from the add task dialog.

        self.grids[self.current_grid].add_task()  # Add the new task to the current grid.

    def set_menu_bar(self):
        """Sets the menu bar for the application."""  
        self.menu_bar = MenuBar()  # Create a new menu bar.
