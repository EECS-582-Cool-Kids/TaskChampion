"""
 *  Module Name: grid_widget.py
 *  Purpose: Initialization of the grid used within the GUI.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Mo Morgan, Richard Moser, Derek Norton
 *  Date: 2/15/2025
 *  Last Modified: 2/15/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from PySide6 import QtCore, QtWidgets
from .task_row import TaskRow
from utils import TaskWarriorInstance

class GridWidget(QtWidgets.QWidget):
    '''The widget that corresponds to a module'''
    ROW_HEIGHT=50  # Height of each row in the grid.
    DEFAULT_ROWS=10  # Default number of rows to display.

    def __init__(self):
        super().__init__()  # Call the parent constructor.
        self.setObjectName('GridWidget')  # Set the object name for styling.
        self.setFixedHeight(200)  # Set the fixed height of the widget. 

        self.scroll_area = QtWidgets.QScrollArea()  # Create a scroll area.
        self.scroll_area.setWidgetResizable(True)  # Set the scroll area to be resizable.
        self.scroll_area.setWidget(self)  # Set the widget of the scroll area to be this widget.

        self.grid = QtWidgets.QGridLayout()  # Create a grid layout.

        self.grid.rowMinimumHeight(self.ROW_HEIGHT)  # Set the minimum height of the rows in the grid.

        # print(self.scrollArea.alignment())  
        self.setLayout(self.grid)  # Set the layout of the widget to be the grid layout.

        self.rows = 0  # Initialize the number of rows to 0.
        self.row_arr: list[TaskRow] = []  # Initialize the row array to an empty list.

        self.add_header()  # Add the header to the grid.
        self.fill_grid()  # Fill the grid with the default number of rows.

        self.menu_bar = None    # declare the window's menu bar
        self.set_menu_bar()     # set the window's menu bar

    def add_task(self, newTask: Task) -> None:
        
        self.rows += 1  # Increment the number of rows.
            
        uuid = str(newTask.get_uuid())  # Get the UUID of the new task.

        if self.grid.rowCount() == self.rows:  # If the row count of the grid is equal to the number of rows.
            self.setMinimumHeight(self.rows * self.ROW_HEIGHT)  # Set the minimum height of the widget to be the number of rows times the row height.

            self.row_arr.append(TaskRow(self.rows, uuid))  # Append a new task row to the row array.
            # Row inserts itself into the grid, insertion logic is handled in `TaskRow` obj.
            # Note that this may be tricky when changing order of tasks w.r.t column sorting, 
            # as that logic will happen in this class.
            # but idk what method we will use for sorting, for all I know qt makes it very easy.    
           
        self.row_arr[self.rows-1].update_task(uuid)  # Update the task in the row array.
        self.row_arr[self.rows-1].insert(self.grid, self.rows)  # Insert the row into the grid.

    def add_header(self):
        # Make header row take up as little vertical space as it needs.
        self.grid.setRowStretch(0, 0)  # Set the row stretch of the grid to 0.
        # self.grid.setContentsMargins(0, 0, 0, 0)
        # self.grid.setHorizontalSpacing(0)
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
        self.menu_bar = menubar.MenuBar()  # Create a new menu bar.

    def fill_grid(self):
        for i in range(self.DEFAULT_ROWS):  # Loop through the default number of rows.
            self.row_arr.append(TaskRow(i, ""))  # Append a new task row to the row array.
            self.row_arr[i].insert(self.grid, i+1)  # Insert the row into the grid.
        self.setMinimumHeight(self.DEFAULT_ROWS * self.ROW_HEIGHT)  # Set the minimum height of the widget to be the default number of rows times the row height.
