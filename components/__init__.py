from utils.task import Task
from PySide6 import QtCore, QtWidgets
# from taskw_ng import TaskWarrior
from utils import taskWarriorInstance
from .checkbox import Checkbox
from .textbox import Textbox
from typing import Final

COLS: Final = ('id', 'start', 'priority', 'project', 'recur', 'due', 'until', 'description', 'urgency')

class ALIGN:
    TL = QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft
    TC = QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter
    CC = QtCore.Qt.AlignmentFlag.AlignCenter
    CL = QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft

class TaskRow:
    def __init__(self, taskID: str):
        # self.row = QtWidgets.QHBoxLayout()
        self.check = Checkbox(taskID)
        self.cols = [Textbox(taskID, attr) for attr in COLS]
        self.buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Discard)
        self.edit_button = None
        self.delete_button = None


        # self.row.addWidget(self.check.checkbox)
        # for tb in self.cols:
        #     self.row.addWidget(tb.textbox)

    def insert(self, grid: QtWidgets.QGridLayout, rowNum: int):
        grid.setRowStretch(rowNum, 1)
        
        grid.addWidget(self.check.checkbox, rowNum, 0, ALIGN.CC)

        for i in range(len(self.cols)):
            grid.addWidget(self.cols[i].textbox, rowNum, i + 1, ALIGN.CL)
        
        grid.addWidget(self.buttons, rowNum, len(self.cols)+1, ALIGN.CL)
        
        