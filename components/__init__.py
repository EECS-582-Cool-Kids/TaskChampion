from utils.task import Task
from PySide6 import QtCore, QtWidgets
# from taskw_ng import TaskWarrior
from utils import taskWarriorInstance
from .checkbox import Checkbox
from .textbox import Textbox
from typing import Final

# The names of the columns.
# TODO: in the image Richard posted, the second col was Age instead of 'start', but taskw_ng doesn't have an age.
# Should we keep it as start? do something else? Idk what start even means.
COLS: Final = ('id', 'start', 'priority', 'project', 'recur', 'due', 'until', 'description', 'urgency')

class ALIGN:
    # Declare where at in a layout an item aligns itself to.
    TL = QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft
    TC = QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter
    CC = QtCore.Qt.AlignmentFlag.AlignCenter
    CL = QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft

class TaskRow:
    def __init__(self, taskID: str):

        self.check = Checkbox(taskID)
        self.cols = [Textbox(taskID, attr) for attr in COLS]
        # TODO: Temporary, edit button and delete button should be declared separately, 
        # but the address book demo used this so I took a shortcut for proof-of-concept.
        self.buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Discard)

        self.edit_button = None
        self.delete_button = None

    def insert(self, grid: QtWidgets.QGridLayout, rowNum: int):
        # Row stretch of 0 means take up bare minimum amount of space?
        # TODO: Figure out how to make it so that if we have two tasks, they are pushed towards the top
        # Instead of being evenly distributed.
        grid.setRowStretch(rowNum, 0)
        
        grid.addWidget(self.check, rowNum, 0)
        self.check.setProperty('row-even',f"{rowNum % 2}")
        
        for i in range(len(self.cols)):

            self.cols[i].setProperty('row-even',f"{rowNum % 2}")
            # self.cols[i].setObjectName('TableText')
            grid.addWidget(self.cols[i], rowNum, i + 1)

        # TODO: Whenever we use the `self.edit_button` / `self.delete_button` vars,
        # this will need to be changed.
        grid.addWidget(self.buttons, rowNum, len(self.cols) + 1)
        # self.buttons.setProperty('row-even',f"rowNum % 2")
        self.buttons.setObjectName(f'Button')
