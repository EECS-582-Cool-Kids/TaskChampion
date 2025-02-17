"""
 *  Module Name: checkbox.py
 *  Purpose: Module for the Checkbox class, which is a class for creating a checkbox in the GUI.
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
from PySide6 import QtCore, QtWidgets
from utils import taskWarriorInstance
from .TableCell import TableCell
from typing import Callable, Optional

class Checkbox(TableCell):

    # def __init__(self, row_num: int, get_task: Callable[[], Optional[Task]], attribute:str=""):
    #     super().__init__(row_num, get_task, attribute)
    # 
    #     self.my_checkbox = QtWidgets.QCheckBox()
    #     self.getSubWidget = lambda: self.my_checkbox
    #     self.my_checkbox.stateChanged.connect(lambda: self.checkCheckbox())
    #     
    #     self._addSubWidget()

    def __init__(self, row_num: int, get_task: Callable[[], Optional[Task]], attribute:str=""):
        self.my_checkbox = QtWidgets.QCheckBox()
        self.getSubWidget = lambda: self.my_checkbox
        self.my_checkbox.stateChanged.connect(lambda: self.checkCheckbox())
    
        super().__init__(row_num, get_task, attribute)
    
        self._addSubWidget()

    def update_task(self):
        super().update_task()
        if self.active:
            assert self.task
            self.my_checkbox.setChecked(self.task.get_status() == 'completed')
        self.update()

    @QtCore.Slot()
    def checkCheckbox(self):
        # TODO: There are more statuses than `completed` and `pending`. Do we care?
        assert self.task

        if self.my_checkbox.isChecked():
            taskWarriorInstance.task_update({"uuid": self.task.get_uuid(), "status": 'completed'})

        else:
            taskWarriorInstance.task_update({"uuid": self.task.get_uuid(), "status": 'pending'})

