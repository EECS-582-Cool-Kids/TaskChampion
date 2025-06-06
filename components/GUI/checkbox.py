""" Prologue:
 *  Module Name: checkbox.py
 *  Purpose: Module for the Checkbox class, which is a class for creating a checkbox in the GUI.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Mo Morgan, Derek Norton
 *  Date: 2/15/2025
 *  Last Modified: 2/23/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from PySide6 import QtCore, QtWidgets
from utils.task_api import api
from components.GUI.tablecell import TableCell
from typing import Callable, Optional
from utils.task import Task

class Checkbox(TableCell):
    def __init__(self, row_num: int, get_task: Callable[[], Optional[Task]], on_update : Callable[[bool], None], attribute:str=""):
        self.my_checkbox = QtWidgets.QCheckBox()  # Create a checkbox.
        self.get_sub_widget = lambda: self.my_checkbox  # Create a lambda function that returns the checkbox.
        self.my_checkbox.stateChanged.connect(lambda: self.check_checkbox())  # Connect the state changed signal of the checkbox to the check checkbox method.
        self.on_update = on_update  # Set the on update method.

        super().__init__(row_num, get_task, attribute)  # Call the parent constructor.
    
        self.add_sub_widget()  # Add the checkbox to the sub widgets list.

    def update_task(self):
        super().update_task()  # Call the parent update task method.
        if self.active:  # If the cell is active.
            assert self.task  # Assert that the task is not None.
            self.my_checkbox.setEnabled(True)  # Enable the checkbox.
            self.my_checkbox.setChecked(self.task.get_status() == 'completed')  # Set the checked state of the checkbox to the status of the task.
        else:
            self.my_checkbox.setChecked(False)  # Set the checkbox to be unchecked.
            self.my_checkbox.setEnabled(False)  # Disable the checkbox.
        self.update()  # Update the cell.

    @QtCore.Slot()
    def check_checkbox(self):  # Check the checkbox.
        # TODO: There are more statuses than `completed` and `pending`. Do we care?
        assert self.task  # Assert that the task is not None.

        if self.my_checkbox.isChecked():  # If the checkbox is checked.
            self.task.set('status', 'completed')  # Set the status of the task to completed.

        else:  # If the checkbox is not checked.
            self.task.set('status', 'pending')  # Set the status of the task to pending.
            
        api.update_task(self.task)  # Update the task status.
        self.on_update(self.my_checkbox.isChecked()) # handle the xp updates
