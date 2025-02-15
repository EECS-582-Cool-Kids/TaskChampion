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
from PySide6 import QtWidgets
from utils import taskWarriorInstance



class Textbox:
    def __init__(self, taskID : str, attribute: str):
        self.attribute = attribute
        self.task_id = taskID 

        self.task: Task or None = None
        self.text: str or None = None

        self.textbox = QtWidgets.QLabel("")
        
        self.update()

    def link_to_layout(self, layout : QtWidgets.QVBoxLayout):
        layout.addWidget(self.textbox)
    
    def update(self) -> None:
        self.task = Task(taskWarriorInstance.get_task(uuid=self.task_id)[1])
        self.text = str(self.task.get(self.attribute) or "") 
        self.textbox.setText(self.text)
        
