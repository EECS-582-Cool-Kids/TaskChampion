"""
 *  Module Name: textbox.py
 *  Purpose: Module for the Textbox class, which is a class for creating a textbox in the GUI.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Mo Morgan
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
from utils import taskWarriorInstance
from typing import Callable, Optional
from .TableCell import TableCell

class Textbox(TableCell):
    def __init__(self, row_num:int, get_task: Callable[[], Optional[Task]], attribute: str=""): 

        self.my_text = ""  # Initialize the text of the textbox
        self.my_label = QtWidgets.QLabel()  # Create a label.
        
        self.getSubWidget = lambda: self.my_label  # Create a lambda function that returns the label.

        super().__init__(row_num, get_task, attribute)  # Call the parent constructor.

        self._addSubWidget()  # Add the label to the sub widgets list.

    def update_task(self):
        super().update_task()  # Call the parent update task method.
        if self.active:  # If the cell is active.
            assert self.task  # Assert that the task is not None.
            assert self.attribute  # Assert that the attribute is not None.
            self.my_text = str(self.task.get(self.attribute) or "")  # Set the text of the label to the attribute of the task.
            self.my_label.setText(self.my_text)  # Set the text of the label to the text.
        self.update()  # Update the cell.
