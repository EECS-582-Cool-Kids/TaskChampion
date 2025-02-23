"""
 *  Module Name: TableCell.py
 *  Purpose: Module for the TableCell class, which is a class for creating a cell in the table in the GUI.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley
 *  Date: 2/15/2025
 *  Last Modified: 2/15/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from utils.task import Task
from PySide6 import QtCore, QtWidgets
from utils import api
from utils import TaskWarriorInstance
from typing import Callable, Optional

class TableCell(QtWidgets.QLabel):
    '''Base class for all table cells.'''
    def __init__(self, row_num: int, get_task: Callable[[], Optional[Task]], attribute: str =""):
        super().__init__()  # Call the parent constructor.
        self.active: bool  # Declare the active variable.
        self.task: Task | None  # Declare the task variable.
        self.attribute = attribute  # Set the attribute of the cell.
        self.get_task = get_task  # Set the get task method.
        
        self.layout = QtWidgets.QHBoxLayout(self)  # Create a horizontal layout.

        # Defined by subclass
        self.get_sub_widget: Optional[Callable[[], QtWidgets.QWidget]]  # Declare the get sub widget method.

        self.update_task()  # Update the task.

        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)  # Set the size policy of the cell to expanding.
        
        self.setProperty('row-even', f"{row_num % 2}")  # Set the row even property of the cell.

    def add_sub_widget(self):
        assert self.get_sub_widget  # Assert that the get sub widget method is not None.
        self.layout.addWidget(self.get_sub_widget())  # Add the sub widget to the layout.

    def update_task(self):
        self.task = self.get_task()  # Get the task from the get task method.
        self.active = self.task != None  # Set the active variable to True if the task is not None.

        self.setProperty('row-active', str(self.active))  # Set the row active property of the cell.

        
