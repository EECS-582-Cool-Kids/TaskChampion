""" Prologue
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
from PySide6 import QtCore, QtWidgets
from components.GUI.task_row import TaskRow, COLS
from components.GUI.xp_bar import XpBar
from styles.extra_styles import get_style
from typing import Optional
from utils.task import Task
from utils.task_api import api
from utils.logger import logger

class GridWidget(QtWidgets.QWidget):
    '''The widget that corresponds to a module'''
    ROW_HEIGHT=50  # Height of each row in the grid.
    DEFAULT_ROWS=10  # Default number of rows to display.
    DEFAULT_WIDTH=1000 # Default width, scrollable.
    #            Done,  Description,    id, start,  priority,   project, 
    COL_STRETCH=(0,     4,              0,  1,      0,          2, 

    #   recur,  due,    until,  urgency,    edit,   delete.
        0,      3,      0,      2,          1,      1)

    def __init__(self, load_styles : Callable[[], None], fetch_xp_fns : Callable[[Task], list[XpBar]], module_name="Main"):
        super().__init__()  # Call the parent constructor.
        self.setObjectName('GridWidget')  # Set the object name for styling.
        self.setFixedHeight(200)  # Set the fixed height of the widget.

        self.module_name = module_name # This will be set explicitly for the Main module and dynamically for other modules.
        self.scroll_area = QtWidgets.QScrollArea()  # Create a scroll area.
        self.scroll_area.setWidgetResizable(True)  # Set the scroll area to be resizable.
        self.scroll_area.setWidget(self)  # Set the widget of the scroll area to be this widget.

        # set a horizontal scroll bar policy
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)  # Set the horizontal scroll bar policy of the scroll area.

        self.grid = QtWidgets.QGridLayout()  # Create a grid layout.

        self.grid.rowMinimumHeight(self.ROW_HEIGHT)  # Set the minimum height of the rows in the grid.
 
        self.setLayout(self.grid)  # Set the layout of the widget to be the grid layout.

        self.row_arr: list[TaskRow] = []  # Initialize the row array to an empty list.

        self.add_header()  # Add the header to the grid.

        self.refresh_styles = load_styles
        self.fetch_xp_fns = fetch_xp_fns

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

            row = TaskRow(num_tasks, self.fetch_xp_fns, self.module_name)  # Create a new task row.
            row.insert(self.grid, num_tasks) # Row inserts itself into the grid, insertion logic is handled in `TaskRow` obj.
            self.row_arr.append(row)
            
        for row in range(len(self.row_arr)):
            self.row_arr[row].update_task()
        
        self.refresh_styles()


    def add_header(self):
        # Make header row take up as little vertical space as it needs.
        self.grid.setRowStretch(0, 0)  # Set the row stretch of the header row to 0.
        self.grid.setSpacing(0)  # Set the spacing of the grid to 0.
        
        # QLabel is just simple text.
        self.grid.addWidget(QtWidgets.QLabel("Done?"), 0, 0)  # Add a label to the grid.
        self.grid.addWidget(QtWidgets.QLabel(""), 0, 10)  # Add a blank label cell to the grid
        self.grid.addWidget(QtWidgets.QLabel(""), 0, 11)  # Add a blank label cell to the grid

        self.grid.itemAtPosition(0, 0).widget().setStyleSheet(get_style("rowLabels"))  # set the style for the "Done?" label
        self.grid.itemAtPosition(0, 10).widget().setStyleSheet(get_style("rowLabels"))  # set the style for the blank label cell
        self.grid.itemAtPosition(0, 11).widget().setStyleSheet(get_style("rowLabels"))  # set the style for the blank label cell

        for i in range(len(COLS)):  # Loop through the columns.
            self.grid.addWidget(QtWidgets.QLabel(COLS[i]), 0, i+1)  # Add a label to the grid.
            self.grid.itemAtPosition(0, i+1).widget().setStyleSheet(get_style("rowLabels"))  # Set the style of the label to be the row labels style.
            self.grid.itemAtPosition(0, i+1).widget().setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Set the alignment of the label to be centered.

        for i in range(len(self.COL_STRETCH)):
            self.grid.setColumnStretch(i, self.COL_STRETCH[i])

    def fill_grid(self):

        for i in range(self.DEFAULT_ROWS):
            
            row = TaskRow(i, self.fetch_xp_fns, self.module_name)
            row.insert(self.grid, i+1)
            self.row_arr.append(row)

        self.setMinimumHeight(self.DEFAULT_ROWS * self.ROW_HEIGHT)  # Set the minimum height of the widget to be the default number of rows times the row height.

