from utils.task import Task
from PySide6 import QtCore, QtWidgets
# from taskw_ng import TaskWarrior
from utils import taskWarriorInstance
from .TableCell import TableCell
from typing import Callable, Optional

class Checkbox(TableCell):

    def __init__(self, row_num: int, get_task: Callable[[], Optional[Task]], attribute:str=""):
        self.my_checkbox = QtWidgets.QCheckBox()
        self.getSubWidget = lambda: self.my_checkbox
        super().__init__(row_num, get_task, attribute)
        self.my_checkbox.stateChanged.connect(lambda: self.checkCheckbox())
        
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

