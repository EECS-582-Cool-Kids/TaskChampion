""" Prologue:
 *  Module Name: add_task_dialog.py
 *  Purpose: Adds details of a task once created.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Mo Morgan, Richard Moser, Derek Norton
 *  Date: 2/15/2025
 *  Last Modified: 2/28/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from PySide6 import QtWidgets
from typing import Optional

class AddTaskDialog(QtWidgets.QDialog):
    class TaskDetails:
        def __init__(self, description : str, tag : str, priority : str, project : str, recurrence : Optional[str], due : Optional[object]):
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

    def add_task(self) -> Optional[TaskDetails]:
        if self.exec():
            if self.is_recurring:
                return AddTaskDialog.TaskDetails(self.description.text(), self.tag.text(), self.priorities.currentText(), 
                                             self.project.text(), self.recurrence.currentText(), self.due_date.dateTime().toPython())
            else:
                return AddTaskDialog.TaskDetails(self.description.text(), self.tag.text(), self.priorities.currentText(), 
                                             self.project.text(), None, None)
        else:
            return None
    
    def open_recurrence(self) -> None:
        self.is_recurring = self.recurring_box.isChecked()