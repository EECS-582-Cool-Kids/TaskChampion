""" Prologue
 *  Module Name: task_row.py
 *  Purpose: Defines the details within each row of the task manager app.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Mo Morgan, Richard Moser, Derek Norton
 *  Date: 2/15/2025
 *  Last Modified: 3/14/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: If attempting to add a task after another task has been deleted
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: RuntimeError: Internal C++ object (Checkbox) already deleted.
"""

from PySide6 import QtWidgets
from components.GUI.xp_controller_widget import XpControllerWidget
from utils.task import Task
from utils.task_api import api
from components.GUI.checkbox import Checkbox
from components.GUI.textbox import Textbox
from components.GUI.buttonbox import ButtonBox
from components.GUI.xp_bar import XpBar
from components.Dialogs.edit_task_dialog import EditTaskDialog
from typing import Callable, Final

# The names of the columns.
# TODO: in the image Richard posted, the second col was Age instead of 'start', but taskw_ng doesn't have an age.
# Should we keep it as start? do something else? Idk what start even means.
COLS: Final = ( 'description', 'id', 'start', 'priority', 'project', 'recur', 'due', 'until','urgency')

class TaskRow:
    # Minimum size for each column to maintain a consistent width
    COLUMN_WIDTHS = {
        'checkbox': 50,

        'description': 150,  # Set width per column as needed
        'id': 30,
        'start': 45,
        'priority': 60,
        'project': 80,
        'recur': 45,
        'due': 45,
        'until': 45,
        'urgency': 60,

        'edit': 60,
        'delete': 65
    }

    def __init__(self, row_num: int, fetch_xp_brs : Callable[[Task], list[XpBar]], module_name):
        self.idx = row_num

        self.xp_add_calls : list[Callable[[int], int]] = [] # list of function calls to call when a task is checked
        self.xp_sub_calls : list[Callable[[int], int]] = [] # list of function calls to call when a task is unchecked
        self.fetch_xp_brs : Callable[[Task], list[XpBar]] = fetch_xp_brs # call to fetch relevant xp functions
        self.module_name = module_name

        self.task = api.task_at(self.idx, module_name)  # Get the task at the index.
        self.check = Checkbox(row_num, self.get_task, self._update_xp_bars)  # Create a checkbox.
        self.cols = [Textbox(row_num, self.get_task, attr) for attr in COLS]  # Create a list of textboxes.

        self.edit_button = ButtonBox(row_num, self.get_task, "edit", self.edit_task)  # Create an edit button.

        # Initial fetch of function calls
        if self.task is not None:
            self._bind_xp_fns(self.fetch_xp_brs(self.task))  # Bind the xp functions.

    def get_task(self): return self.task

    def insert(self, grid: QtWidgets.QGridLayout, row_num: int):
        # Row stretch of 0 means take up bare minimum amount of space?
        grid.setRowStretch(row_num, 0)  # Set the row stretch of the grid.

        column_height = 50  # Set height per column as needed

        self.check.setMinimumWidth(self.COLUMN_WIDTHS['checkbox'])  # Checkbox width
        self.check.setFixedHeight(column_height)  # Checkbox height
        grid.addWidget(self.check, row_num, 0)  # Add the checkbox to the grid
        # set style for the checkbox
        # self.check.setStyleSheet(get_style("CheckBox"))

        for i in range(len(self.cols)):  # Loop through the columns.
            col_name = COLS[i]  # Get the name of the column.
            if col_name in self.COLUMN_WIDTHS:  # If the column name is in the column widths.
                self.cols[i].setMinimumWidth(self.COLUMN_WIDTHS[col_name])  # Apply fixed width
            self.cols[i].setFixedHeight(column_height)  # Apply fixed height
            grid.addWidget(self.cols[i], row_num, i + 1)

        # Set fixed sizes for buttons
        self.edit_button.setMinimumWidth(self.COLUMN_WIDTHS['edit'])  # Set the fixed width of the edit button.
        self.edit_button.setFixedHeight(column_height)  # Set the fixed height of the edit button.

        grid.addWidget(self.edit_button, row_num, len(self.cols) + 1)  # Add the edit button

    def update_task(self):
        """
        Updates the task elements and associated components within the application.
        This method retrieves the task at the specified index, updates associated
        checkbox, column elements, edit and delete buttons, and binds external
        functions if the task is valid.

        Returns:
            None
        """
        self.task = api.task_at(self.idx, self.module_name)  # Get the task at the index.

        self.check.update_task()  # Update the checkbox.
        for i in range(len(self.cols)):  # Loop through the columns.
            self.cols[i].update_task()  # Update the column.
        self.edit_button.update_task()  # Update the edit button.

        if self.task is not None:  # If the task is not None.
            self._bind_xp_fns(self.fetch_xp_brs(self.task))  # Bind the xp functions.

    def edit_task(self):
        if not self.task:  # If the task is None.
            return  # Return.

        # TODO: I bet we are gonna have to do something slightly awkward related to nonstandard cols here. Get ready for that.
        edit_task_dialog = EditTaskDialog(
            delete_task=self.delete_task,
            description=str(self.task.get("description") or ""),
            due=str(self.task.get("due") or ""),
            priority=str(self.task.get("priority") or ""),
            project=str(self.task.get("project") or ""),
            tags=[str(tag) for tag in self.task.get("tags") or []])  # Create an instance of the EditTaskDialog class.

        if edit_task_dialog.exec():  # If the dialog is executed.
            self.task.set("description", edit_task_dialog.description or None)  # Set the description of the task.
            self.task.set("due", edit_task_dialog.due or None)  # Set the due date of the task.
            self.task.set("priority", edit_task_dialog.priority or None)  # Set the priority of the task.
            self.task.set("project", edit_task_dialog.project or None)  # Set the project of the task.
            self.task.set("tags", edit_task_dialog.tags_list or None)  # Set the tags of the task.
            api.update_task(self.task)  # Update the task.
            self.update_task()  # Update the task.

    def delete_task(self):
        api.delete_at(self.idx, self.module_name)  # Delete the task at the index.
        self.remove_task_row()  # remove the task row from the UI

    def remove_task_row(self):
        # Get the parent grid layout
        grid = self.check.parentWidget().layout()  # Get the layout of the parent widget.
        if not grid:  # If the grid is None.
            return  # Return.

        # Get the current row index
        row_idx = grid.indexOf(self.check)  # Get the index of the checkbox.

        # Loop through the widgets in the row and remove them
        for widget in [self.check] + self.cols + [self.edit_button]:
            grid.removeWidget(widget)  # Remove the widget from the grid.
            widget.deleteLater()  # Delete the widget.
        # add an empty row to the grid to maintain the same number of rows
        grid.addWidget(QtWidgets.QLabel(), grid.count(), 0)  # Add a label to the grid.

    def annihilate(self):
        # Get the parent grid layout
        grid = self.check.parentWidget().layout()  # Get the layout of the parent widget.
        if not grid:  # If the grid is None.
            return  # Return.

        # Loop through the widgets in the row and remove them
        for widget in [self.check] + self.cols + [self.edit_button]:  # Loop through the widgets.
            grid.removeWidget(widget)  # Remove the widget from the grid.
            widget.deleteLater()  # Delete the widget.
        # add an empty row to the grid to maintain the same number of rows
        grid.addWidget(QtWidgets.QLabel(), grid.row_count(), 0)  # Add a label to the grid.

    def _bind_xp_fns(self, xp_bars : list[XpBar]) -> None:
        # clear the lists and reset them every time.
        self.xp_add_calls.clear()  # Clear the xp add calls.
        self.xp_sub_calls.clear()  # Clear the xp sub calls.

        for xp_bar in xp_bars:
            self.xp_add_calls.append(xp_bar.add_xp)  # Append the add xp function.
            self.xp_sub_calls.append(xp_bar.sub_xp)  # Append the sub xp function.

    def _update_xp_bars(self, checkbox_state : bool) -> None:
        if self.task is None:  # If the task is None.
            return  # Return.

        completion_value : int = XpControllerWidget.get_completion_value(self.task.get_priority(), self.task.get_project(), self.task.get_tags())

        if checkbox_state:  # If the checkbox state is True.
            for add_fn in self.xp_add_calls:  # Loop through the xp add calls.
                add_fn(completion_value)   # Call the add function.
        else:
            for sub_fn in self.xp_sub_calls:  # Loop through the xp sub calls.
                sub_fn(completion_value)  # Call the sub function.