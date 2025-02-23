"""
 *  Module Name: buttonbox.py
 *  Purpose: Initialization of buttons within GUI.
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

from utils.task import Task
from PySide6 import QtCore, QtWidgets, QtGui
from typing import Final
from .TableCell import TableCell
from typing import Callable, Optional


class Buttonbox(TableCell):
    def __init__(self, row_num:int, get_task: Callable[[], Optional[Task]], attribute: str="", action: Optional[Callable[[], None]] = None):
        
        self.my_button = QtWidgets.QPushButton(attribute)  # Create a push button with the attribute as the text.
        self.my_button.setObjectName(f"button-{attribute}")  # Set the object name of the button.
        
        self.get_sub_widget = lambda: self.my_button  # Create a lambda function that returns the button.

        super().__init__(row_num, get_task, attribute)  # Call the parent constructor.

        self.addSubWidget()  # Add the button to the sub widgets list.
        if action:  # If an action is provided.
            self.my_button.clicked.connect(action)  # Connect the clicked signal of the button to the action.

    def update_task(self):
        super().update_task()  # Call the parent update task method.
        if self.active:  # If the cell is active.
            self.my_button.setEnabled(True)  # Enable the button.
        else:   # If the cell is not active.
            self.my_button.setEnabled(False)  # Disable the button.
        self.update()  # Update the cell.