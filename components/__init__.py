"""
 *  Module Name: __init__.py
 *  Purpose: Initialization of most internal objects related to the GUI.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Mo Morgan, Richard Moser
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
from utils import TaskWarriorInstance
from .checkbox import Checkbox
from .textbox import Textbox
from .buttonbox import Buttonbox
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

class AddTaskDialog(QtWidgets.QDialog):
    class TaskDetails:
        def __init__(self, description : str, tag : str, priority : str, project : str, recurrence : str | None, due : object | None):
            self.description = description
            self.tag = tag
            self.priority = priority
            self.project = project
            self.recurrence = recurrence
            self.due = due

    def __init__(self):
        super().__init__()

        self.form = QtWidgets.QFormLayout()

        self.description = QtWidgets.QLineEdit()
        self.tag = QtWidgets.QLineEdit()
        self.priorities = QtWidgets.QComboBox()
        self.project = QtWidgets.QLineEdit()
        self.recurring_box = QtWidgets.QCheckBox()

        self.is_recurring = False

        self.recurring_box.stateChanged.connect(self.open_recurrence)

        self.recurrence = QtWidgets.QComboBox()
        self.due_date = QtWidgets.QDateEdit()
        self.due_date.setDateTime(self.due_date.dateTime().currentDateTime())

        self.priorities.addItem("H")
        self.priorities.addItem("M")
        self.priorities.addItem("L")

        self.recurrence.addItem("daily")
        self.recurrence.addItem("weekly")
        self.recurrence.addItem("monthly")
        self.recurrence.addItem("yearly")

        self.buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok
                                      | QtWidgets.QDialogButtonBox.StandardButton.Cancel)

        self.form.addRow("Description*", self.description)
        self.form.addRow("Tag", self.tag)
        self.form.addRow("Priority", self.priorities)
        self.form.addRow("Project", self.project)
        self.form.addRow("Is Recurring?", self.recurring_box)
        self.form.addRow("Recurrence", self.recurrence)
        self.form.addRow("Due Date", self.due_date)

        self.layout : QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.form)
        self.layout.addWidget(self.buttons)

        self.setLayout(self.layout)
        self.setWindowTitle("Add Task")

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def add_task(self) -> TaskDetails | None:
        if self.exec():
            if self.is_recurring:
                test = self.due_date.dateTime().toPython()

                return AddTaskDialog.TaskDetails(self.description.text(), self.tag.text(), self.priorities.currentText(), 
                                             self.project.text(), self.recurrence.currentText(), self.due_date.dateTime().toPython())
            else:
                return AddTaskDialog.TaskDetails(self.description.text(), self.tag.text(), self.priorities.currentText(), 
                                             self.project.text(), None, None)
        else:
            return None
    
    def open_recurrence(self) -> None:
        self.is_recurring = self.recurring_box.isChecked()

class EditTaskDialog(QtWidgets.QDialog):
    def __init__(self, description="", due="", priority=""):
        super().__init__()
        self.form = QtWidgets.QFormLayout()

        self.description_text = QtWidgets.QLineEdit(description)
        self.due_text = QtWidgets.QLineEdit(due)
        self.priority_text = QtWidgets.QLineEdit(priority)

        self.form.addRow("Description", self.description_text)
        self.form.addRow("Due", self.due_text)
        self.form.addRow("Priority", self.priority_text)


        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok
                                      | QtWidgets.QDialogButtonBox.StandardButton.Cancel)



        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(self.form)
        layout.addWidget(button_box)

        self.setLayout(layout)

        self.setWindowTitle("Edit Task")

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

    # These properties make using this dialog a little cleaner. It's much
    # nicer to type "addDialog.address" to retrieve the address as compared
    # to "addDialog.addressText.toPlainText()"
    @property
    def description(self):
        return self.description_text.text()

    @property
    def due(self):
        return self.due_text.text()

    @property
    def priority(self):
        return self.priority_text.text()


class TaskRow:
    def __init__(self, row_num: int, taskID: str):
        self.task = Task(TaskWarriorInstance.get_task(uuid=taskID)[1]) if taskID else None
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

        # TODO: Whenever we use the `self.edit_button` / `self.delete_button` vars,
        # this will need to be changed.
        grid.addWidget(self.edit_button, rowNum, len(self.cols) + 1)  # add the edit button to the grid
        grid.addWidget(self.delete_button, rowNum, len(self.cols) + 2)  # add the delete button to the grid

    def update_task(self, taskID: str= ""):
        
        self.task = Task(TaskWarriorInstance.get_task(uuid=taskID)[1]) if taskID else None
        
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
            TaskWarriorInstance.task_update(self.task)
            self.update_task(str(self.task.get_uuid()))
            
    def delete_task(self):
        assert self.task  # throw error if called without a task
        uuid = self.task.get_uuid()
        TaskWarriorInstance.task_delete(uuid=uuid)  # delete task with the corresponding id
        self._remove_task_row()  # remove the task row from the UI

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
        
