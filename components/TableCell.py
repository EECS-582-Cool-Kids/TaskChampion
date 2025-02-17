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
from utils import taskWarriorInstance
from typing import Callable, Optional

class TableCell(QtWidgets.QLabel):
    '''Base class for all table cells.'''
    def __init__(self, row_num: int, get_task: Callable[[], Optional[Task]], attribute: str =""):
        super().__init__()
        self.active: bool
        self.task: Task | None
        self.attribute = attribute
        self.get_task = get_task
        
        self.layout = QtWidgets.QHBoxLayout(self)

        # Defined by subclass
        self.getSubWidget: Optional[Callable[[], QtWidgets.QWidget]]

        self.update_task()

        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        
        self.setProperty('row-even', f"{row_num % 2}")

    def _addSubWidget(self):
        assert self.getSubWidget
        self.layout.addWidget(self.getSubWidget())

    def update_task(self):
        self.task = self.get_task()
        self.active = self.task != None

        self.setProperty('row-active', str(self.active))

        
