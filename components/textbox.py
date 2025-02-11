from utils.task import Task
from PySide6 import QtCore, QtWidgets, QtGui
# from taskw_ng import TaskWarrior
from utils import taskWarriorInstance
from typing import Callable, Optional
from .TableCell import TableCell

class Textbox(TableCell):
    def __init__(self, row_num:int, get_task: Callable[[], Optional[Task]], attribute: str=""):

        self.my_text = ""
        self.my_label = QtWidgets.QLabel()
        
        self.getSubWidget = lambda: self.my_label

        super().__init__(row_num, get_task, attribute)

        self._addSubWidget()

    def update_task(self):
        super().update_task()
        if self.active:
            assert self.task
            assert self.attribute
            self.my_text = str(self.task.get(self.attribute) or "") 
            self.my_label.setText(self.my_text)
        self.update()
