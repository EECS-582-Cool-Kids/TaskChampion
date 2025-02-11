from utils.task import Task
from PySide6 import QtCore, QtWidgets, QtGui
# from taskw_ng import TaskWarrior
from utils import taskWarriorInstance
from typing import Final
from .TableCell import TableCell
from typing import Callable, Optional


class Buttonbox(TableCell):
    def __init__(self, row_num:int, get_task: Callable[[], Optional[Task]], attribute: str="", action: Optional[Callable[[], None]] = None):
        
        self.my_button = QtWidgets.QPushButton(attribute)
        self.my_button.setObjectName(f"button-{attribute}")
        
        self.getSubWidget = lambda: self.my_button

        super().__init__(row_num, get_task, attribute)

        self._addSubWidget()
        if action:
            self.my_button.clicked.connect(action)

    def update_task(self):
        super().update_task()
        if self.active:
            self.my_button.setEnabled(True)
        else:
            self.my_button.setEnabled(False)
        self.update()