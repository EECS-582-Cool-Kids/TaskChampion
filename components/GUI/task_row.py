"""
 *  Module Name: task_row.py
 *  Purpose: Defines the details within each row of the task manager app.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Mo Morgan, Richard Moser, Derek Norton
 *  Date: 2/15/2025
 *  Last Modified: 2/27/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from PySide6 import QtWidgets
from utils.task import Task
from utils.task_api import api
from components.GUI.checkbox import Checkbox
from components.GUI.textbox import Textbox
from components.GUI.buttonbox import ButtonBox
from components.GUI.xpbar import XpBar
from components.GUI.xp_controller_widget import HIGH_PRIORITY_MULT, MED_PRIORITY_MULT, LOW_PRIORITY_MULT
from components.Dialogs.edit_task_dialog import EditTaskDialog
from typing import Callable, Final

# The names of the columns.
# TODO: in the image Richard posted, the second col was Age instead of 'start', but taskw_ng doesn't have an age.
# Should we keep it as start? do something else? Idk what start even means.
COLS: Final = ('id', 'start', 'priority', 'project', 'recur', 'due', 'until', 'description', 'urgency')

class TaskRow:
    def __init__(self, row_num: int, fetch_xp_brs : Callable[[Task], list[XpBar]]):
        self.idx = row_num

        self.task = api.task_at(self.idx)
        self.check = Checkbox(row_num, self.get_task, self._update_xp_bars)
        self.cols = [Textbox(row_num, self.get_task, attr) for attr in COLS]

        self.edit_button = ButtonBox(row_num, self.get_task, "edit", self.edit_task)
        self.delete_button = ButtonBox(row_num, self.get_task, "delete", self.delete_task)

        self.xp_add_calls : list[Callable[[int], int]] = [] # list of function calls to call when a task is checked
        self.xp_sub_calls : list[Callable[[int], int]] = [] # list of function calls to call when a task is unchecked
        self.fetch_xp_brs : Callable[[Task], list[XpBar]] = fetch_xp_brs # call to fetch relevant xp functions

        # Initial fetch of function calls
        if self.task != None:
            self._bind_xp_fns(self.fetch_xp_brs(self.task))

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
        self.task = api.task_at(self.idx)

        self.check.update_task()
        for i in range(len(self.cols)):
            self.cols[i].update_task()
        self.edit_button.update_task()
        self.delete_button.update_task()

        if self.task != None:
            self._bind_xp_fns(self.fetch_xp_brs(self.task))
    
    def edit_task(self):
        if not self.task:
            return

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
        api.delete_at(self.idx)
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
        grid.addWidget(QtWidgets.QLabel(), grid.count(), 0)

    def annihilate(self):
        # Get the parent grid layout
        grid = self.check.parentWidget().layout()
        if not grid:
            return
    
        # Loop through the widgets in the row and remove them
        for widget in [self.check] + self.cols + [self.edit_button, self.delete_button]:
            grid.removeWidget(widget)
            widget.deleteLater()
        # add an empty row to the grid to maintain the same number of rows
        grid.addWidget(QtWidgets.QLabel(), grid.row_count(), 0)

    def _bind_xp_fns(self, xp_bars : list[XpBar]) -> None:
        # clear the lists and reset them every time.
        self.xp_add_calls.clear()
        self.xp_sub_calls.clear()

        for xp_bar in xp_bars:
            self.xp_add_calls.append(xp_bar.add_xp)
            self.xp_sub_calls.append(xp_bar.sub_xp)
    
    def _update_xp_bars(self, checkbox_state : bool) -> None:
        val : int = HIGH_PRIORITY_MULT if self.task.get_priority() == 'H' else MED_PRIORITY_MULT if self.task.get_priority() == 'M' else LOW_PRIORITY_MULT

        if checkbox_state:
            for add_fn in self.xp_add_calls:
                add_fn(val)
        else:
            for sub_fn in self.xp_sub_calls:
                sub_fn(val)