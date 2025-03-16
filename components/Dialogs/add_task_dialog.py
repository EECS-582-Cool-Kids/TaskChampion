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
from utils.task_api import api

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
        self.projects = QtWidgets.QComboBox()
        self.new_project = QtWidgets.QLineEdit()
        self.recurring_box = QtWidgets.QCheckBox()

        self.is_recurring = False

        self.recurring_box.stateChanged.connect(self.open_recurrence)

        self.recurrence = QtWidgets.QComboBox()
        self.due_date = QtWidgets.QDateEdit()
        self.due_date.setDateTime(self.due_date.dateTime().currentDateTime())

        self.priorities.addItem("None")
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
        self.form.addRow("Project", self.projects)
        self.form.addRow("New Project", self.new_project)
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
        # Define the projects
        self.projects.clear()
        self.projects.addItem("New Project...")
        prev_proj = []
        
        for task in api.task_list:
            task_project = task.get_project()
            if task_project != None and not task_project in prev_proj:
                self.projects.addItem(task_project)
                prev_proj.append(task_project)

        if self.exec():
            if not self.is_recurring:  # If the task is not recurring
                self.recurrence = None  # Set the recurrence to None
                self.due_date = None  # Set the due date to None
            else:  # If the task is recurring
                self.recurrence = self.recurrence.currentText()  # Set the recurrence to the current text of the recurrence field
                self.due_date = self.due_date.dateTime().toPython()  # Set the due date to the due date field

            if self.priorities.currentText() == "None":  # If the priority is None
                self.priorities.clear()  # Clear the priority field

            task_project = self.projects.currentText()
            if self.projects.currentText() == "New Project...":
                task_project = self.new_project.text()
                
            task_details = AddTaskDialog.TaskDetails(self.description.text(), self.tag.text(), self.priorities.currentText(),
                                             task_project, self.recurrence, self.due_date)  # Return the task details
            
            self.description.clear() # Clear the description field so the text doesn't repopulate on the next task creation
            return task_details
          
        else:
            self.description.clear() # Clear the description field so the text doesn't repopulate on the next task creation
            return None
        #
    def open_recurrence(self) -> None:
        self.is_recurring = self.recurring_box.isChecked()