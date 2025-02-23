"""
 *  Module Name: task_row.py
 *  Purpose: Defines the details within each row of the task manager app.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Mo Morgan, Richard Moser, Derek Norton
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
from .checkbox import Checkbox
from .textbox import Textbox
from .buttonbox import Buttonbox
from .edit_task_dialog import EditTaskDialog
from typing import Final, Optional
from utils import api

# The names of the columns.
# TODO: in the image Richard posted, the second col was Age instead of 'start', but taskw_ng doesn't have an age.
# Should we keep it as start? do something else? Idk what start even means.
COLS: Final = ('id', 'start', 'priority', 'project', 'recur', 'due', 'until', 'description', 'urgency')

class TaskRow:
    def __init__(self, row_num: int):
        self.idx = row_num

        self.task = api.task_at(self.idx)
        self.check = Checkbox(row_num, self.get_task)
        self.cols = [Textbox(row_num, self.get_task, attr) for attr in COLS]

        self.edit_button = Buttonbox(row_num, self.get_task, "edit", self.edit_task)
        self.delete_button = Buttonbox(row_num, self.get_task, "delete", self.delete_task)

    def get_task(self): return self.task

    def insert(self, grid: QtWidgets.QGridLayout, rowNum: int):
        # Row stretch of 0 means take up bare minimum amount of space?
        grid.setRowStretch(rowNum, 0)
        grid.addWidget(self.check, rowNum, 0)
        
        for i in range(len(self.cols)):
            grid.addWidget(self.cols[i], rowNum, i + 1)

        grid.addWidget(self.edit_button, rowNum, len(self.cols) + 1)  # add the edit button to the grid
        grid.addWidget(self.delete_button, rowNum, len(self.cols) + 2)  # add the delete button to the grid

    def update_task(self):

        # Uncomment the print lines for debugging, if necessary.
        # if self.task:
        #     print(f"taskID: {self.task.get_id()} => ", end="")
        # else:
        #     print("taskID: None => ", end="")

        self.task = api.task_at(self.idx)

        # if self.task:
        #     print(self.task.get_id())
        # else:
        #     print("None")
        self.check.update_task()
        for i in range(len(self.cols)):
            self.cols[i].update_task()
        self.edit_button.update_task()
        self.delete_button.update_task()
    
    def edit_task(self):
        assert self.task

        edit_task_dialog = EditTaskDialog(str(self.task.get("description") or ""), 
          str(self.task.get("due") or ""), 
          str(self.task.get("priority") or ""))
        
        if edit_task_dialog.exec():
            self.task.set("description", edit_task_dialog.description or None)
            self.task.set("due", edit_task_dialog.due or None)
            self.task.set("priority", edit_task_dialog.priority or None)
            api.update_task(self.task)
            self.update_task()
            
    def delete_task(self):
        assert self.task  # throw error if called without a task
        uuid = self.task.get_uuid()
        TaskWarriorInstance.task_delete(uuid=uuid)  # delete task with the corresponding id
        self.remove_task_row()  # remove the task row from the UI

    def remove_task_row(self):
        # Get the parent grid layout
        grid = self.check.parentWidget().layout()
        if not grid:
            return
    
        # Loop through the widgets in the row and remove them
        for widget in [self.check] + self.cols + [self.edit_button, self.delete_button]:
            grid.removeWidget(widget)
            widget.deleteLater()
        # add an empty row to the grid to maintain the same number of rows
        grid.addWidget(QtWidgets.QLabel(), grid.rowCount(), 0)