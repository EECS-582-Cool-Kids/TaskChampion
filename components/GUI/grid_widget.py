"""
 *  Module Name: grid_widget.py
 *  Purpose: Initialization of the grid used within the GUI.
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

from typing import Callable
from PySide6 import QtWidgets
from components.GUI.task_row import TaskRow, COLS
from .menubar import MenuBar
from components.Dialogs.add_task_dialog import AddTaskDialog

from utils.task_api import api
from utils.logger import logger


class GridWidget(QtWidgets.QWidget):
    '''The widget that corresponds to a module'''
    ROW_HEIGHT=50  # Height of each row in the grid.
    DEFAULT_ROWS=10  # Default number of rows to display.
    DEFAULT_WIDTH=800 # Default width, scrollable.

    def __init__(self, load_styles : Callable[[], None]):
        super().__init__()  # Call the parent constructor.
        self.setObjectName('GridWidget')  # Set the object name for styling.
        self.setFixedWidth(self.DEFAULT_WIDTH)

        self.scroll_area = QtWidgets.QScrollArea()  # Create a scroll area.
        self.scroll_area.setWidgetResizable(True)  # Set the scroll area to be resizable.
        self.scroll_area.setWidget(self)  # Set the widget of the scroll area to be this widget.

        self.grid = QtWidgets.QGridLayout()  # Create a grid layout.

        self.grid.rowMinimumHeight(self.ROW_HEIGHT)  # Set the minimum height of the rows in the grid.
 
        self.setLayout(self.grid)  # Set the layout of the widget to be the grid layout.

        self.row_arr: list[TaskRow] = []  # Initialize the row array to an empty list.

        self.add_header()  # Add the header to the grid.

        self.refresh_styles = load_styles

    def add_task(self) -> None:
        """Assumes that addTask has already been called in TaskChampionGUI. 
        .
        Since that means TaskAPI has the updated list of tasks, 
        all we need to do is:

        1) See if we need to add a new `TaskRow`
        2) broadcast to all `TaskRow`s to update their current task.
        """
        num_tasks = api.num_tasks()  # Increment the number of rows.

            
        if self.grid.rowCount() == num_tasks:  # If the row count of the grid is equal to the number of rows.
            self.setMinimumHeight(num_tasks * self.ROW_HEIGHT)  # Set the minimum height of the widget to be the number of rows times the row height.

            # Append a new task row to the row array.
            try:
                self.row_arr.append(TaskRow(num_tasks))
                self.row_arr[num_tasks-1].insert(self.grid, num_tasks)
            except ValueError as err:
                logger.log_error(str(err))

            # Row inserts itself into the grid, insertion logic is handled in `TaskRow` obj.
            
        for row in range(len(self.row_arr)):
            self.row_arr[row].update_task()
        
        self.refresh_styles()


    def add_header(self):
        # Make header row take up as little vertical space as it needs.
        self.grid.setRowStretch(0, 0)  # Set the row stretch of the grid to 0.
        self.grid.setSpacing(0)  # Set the spacing of the grid to 0.
        
        # QLabel is just simple text.
        self.grid.addWidget(QtWidgets.QLabel("Completed?"), 0, 0)  # Add a label to the grid.
        # TODO: may be no point in setting column stretch like this and below,
        # Consider changing.
        self.grid.setColumnStretch(0, 0)  # Set the column stretch of the grid to 0.

        for i in range(len(COLS)):  # Loop through the columns.
            self.grid.addWidget(QtWidgets.QLabel(COLS[i]), 0, i+1)  # Add a label to the grid.
            self.grid.setColumnStretch(i+1, 0)  # Set the column stretch of the grid to 0.

    def set_menu_bar(self):
        """Sets the menu bar for the application."""
        self.menu_bar = MenuBar()  # Create a new menu bar.

    def fillGrid(self):
        # Also adds tasks to the grid, which doesn't work for the "example" tab. So for now, it's empty.

        for i in range(self.DEFAULT_ROWS):  # Loop through the default number of rows.
            # Append a new task row to the row array.
            try:
                self.row_arr.append(TaskRow(i))
                self.row_arr[i].insert(self.grid, i+1)  # Insert the row into the grid.
            except ValueError as err:
                logger.log_error(str(err))

        self.setMinimumHeight(self.DEFAULT_ROWS * self.ROW_HEIGHT)  # Set the minimum height of the widget to be the default number of rows times the row height.