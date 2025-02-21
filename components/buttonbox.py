from utils.task import Task
from PySide6 import QtCore, QtWidgets, QtGui
from utils import TaskWarriorInstance
from typing import Final
from .TableCell import TableCell
from typing import Callable, Optional


class Buttonbox(TableCell):
    def __init__(self, row_num:int, get_task: Callable[[], Optional[Task]], attribute: str="", action: Optional[Callable[[], None]] = None):
        
        self.my_button = QtWidgets.QPushButton(attribute)  # Create a push button with the attribute as the text.
        self.my_button.setObjectName(f"button-{attribute}")  # Set the object name of the button.
        
        self.get_sub_widget = lambda: self.my_button  # Create a lambda function that returns the button.

        super().__init__(row_num, get_task, attribute)  # Call the parent constructor.

        self.add_sub_widget()  # Add the button to the sub widgets list.
        if action:  # If an action is provided.
            self.my_button.clicked.connect(action)  # Connect the clicked signal of the button to the action.

    def update_task(self):
        super().update_task()  # Call the parent update task method.
        if self.active:  # If the cell is active.
            self.my_button.setEnabled(True)  # Enable the button.
        else:   # If the cell is not active.
            self.my_button.setEnabled(False)  # Disable the button.
        self.update()  # Update the cell.