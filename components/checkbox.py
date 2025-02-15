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



class Checkbox:
    def __init__(self, taskID : str):
        self.task = Task(taskWarriorInstance.get_task(uuid=taskID)[1])

        self.checkbox = QtWidgets.QCheckBox()
        self.checkbox.setChecked(self.task.get_status() == 'completed')

        self.checkbox.stateChanged.connect(lambda: self.checkCheckbox()) 
        
    @QtCore.Slot()
    def checkCheckbox(self):
        if self.checkbox.isChecked():
            taskWarriorInstance.task_update({"uuid": self.task.get_uuid(), "status": 'completed'})

        else:
            taskWarriorInstance.task_update({"uuid": self.task.get_uuid(), "status": 'pending'})

    def linkToLayout(self, layout : QtWidgets.QVBoxLayout):
        layout.addWidget(self.checkbox)
