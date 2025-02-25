"""
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
from components.GUI.xpbar import XpBar
from .menubar import MenuBar
from utils.task_api import api


class TaskChampionWidget(QtWidgets.QWidget):
    '''The main widget for the Task Champion application.'''
    def __init__(self):
        super().__init__()  # Call the parent constructor.
        self.setObjectName('MainWidget')  # Set the object name for styling.
        
        # Initialize the layout
        self.main_layout = QtWidgets.QHBoxLayout(self)
        
        # Create a vertical layout. Currently, contains grid + Add Task button.
        self.task_layout = QtWidgets.QVBoxLayout()

        
        # TODO: put another layout in the 'gamefication' part of the screen, and do something with it.
        self.main_layout.addLayout(self.task_layout)  # Set the layout of the widget to be the vertical layout.
        
        self.main_tab = QtWidgets.QTabWidget()  # Create a tab widget.
        self.add_button = QtWidgets.QPushButton("Add Task")  # Create a push button.

        self.xp_bar = XpBar(self)
        self.xp_bar.set_max_xp(5) # TODO: Replace this with a meaningful value.

        # Set grid widget to take up 75% of the app's width.
        self.main_layout.setStretch(0, 3)
        self.main_layout.setStretch(1, 1)

        self.add_button.setMaximumWidth(100)  # Set the maximum width of the push button.
        self.add_button.clicked.connect(lambda: self.add_task())  # Connect the clicked signal of the push button to the addTask method.
 
        self.task_layout.addWidget(self.add_button)  # Add the push button to the layout.
        
        self.task_layout.addWidget(self.main_tab)  # Add the tab widget to the layout.
        self.grids = [GridWidget(), GridWidget()]  # Create a list of grid widgets.
        self.main_tab.addTab(self.grids[0].scroll_area, "Example Tab")  # Add the first grid widget to the tab widget.
        self.main_tab.addTab(self.grids[1].scroll_area, "Example Empty Tab")  # Add the second grid widget to the tab widget.

        self.current_grid = 0  # Set the current grid to 0.

        self.add_task_dialog : AddTaskDialog = AddTaskDialog()  # Create an instance of the AddTaskDialog class.

        self.menu_bar = None    # declare the window's menu bar
        self.set_menu_bar()     # set the window's menu bar
    
    def add_task(self):
        '''Add a task to the GUI list and link it to a new task in TaskWarrior.'''
        # TODO: Do something meaningful with this, remove it from this function!
        print(self.xp_bar.add_xp(1))

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
