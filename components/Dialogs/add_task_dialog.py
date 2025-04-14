""" Prologue:
 *  Module Name: add_task_dialog.py
 *  Purpose: Adds details of a task once created.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Mo Morgan, Richard Moser, Derek Norton
 *  Date: 2/15/2025
 *  Last Modified: 3/26/2025
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

        self.priorities.addItems(["None", "H", "M", "L"])
        self.recurrence.addItems(["daily", "weekly", "monthly", "yearly"])

        self.buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok
                                      | QtWidgets.QDialogButtonBox.StandardButton.Cancel)

        # Add all the widgets to the form layout
        self.form.addRow("Description*", self.description)
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

        # Store previously used tags
        self.tag_history = []
        self.tags_list = []

        # Create "Add Tag" button
        self.add_tag_button = QtWidgets.QPushButton("Add Tag")
        self.add_tag_button.clicked.connect(self.add_tag_to_list)

        # Create a layout to hold the tag input field and button side by side
        self.tag_layout = QtWidgets.QHBoxLayout()
        self.tag_layout.addWidget(self.tag)
        self.tag_layout.addWidget(self.add_tag_button)

        # Add this new layout to the form
        self.form.addRow("Tags", self.tag_layout)

        # Create a layout to hold the added tag "bubbles"
        self.tag_bubble_widget = QtWidgets.QWidget()
        self.tag_bubble_layout = QtWidgets.QHBoxLayout(self.tag_bubble_widget)
        self.tag_bubble_layout.setContentsMargins(0, 0, 0, 0)
        self.tag_bubble_layout.setSpacing(5)  # Space between tags
        self.form.addRow(self.tag_bubble_widget)

        self.tag.mousePressEvent = self.show_tag_menu # Connect tag input field to show menu on focus

    def show_tag_menu(self):
        menu = QtWidgets.QMenu(self)

        for tag in self.tag_history: # Add tag actions from the history
            action = menu.addAction(tag)
            action.triggered.connect(lambda t=tag: self.tag.setText(t))

        menu.setFixedWidth(self.tag.width()) # Set menu width equal to tag input field width

        menu.exec(self.tag.mapToGlobal(self.tag.rect().bottomLeft()))  # Show menu below the input field

    def add_tag_to_list(self):
        tag_text = self.tag.text().strip()
        if tag_text == '': #if button is pressed while empty skips adding
            return
        if tag_text and tag_text not in self.tag_history: 
            self.tag_history.append(tag_text)  # Add the tag to history

        if tag_text not in self.tags_list: #if tag is already added don't add the new tag
            self.tags_list.append(tag_text) #add the new tag name to the list of tags present
            tag_button = QtWidgets.QPushButton(tag_text)
            tag_button.setStyleSheet("""  
                QPushButton {
                    background-color: white;
                    border: 2px solid #ccc;
                    border-radius: 12px;
                    padding: 5px 10px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
            """) # Create a button for the tag, styled like a bubble

            tag_button.clicked.connect(lambda: self.remove_tag(tag_button)) # remove tag when clicked

            tag_button.setFixedSize(tag_button.sizeHint())  # Ensure the size is adjusted properly
            self.tag_bubble_layout.addWidget(tag_button)  # Add the tag button to the layout

        self.tag.clear()  # Clear the input field after adding the tag

    def add_task(self, module: str) -> Optional[TaskDetails]:
        """TODO: This will have to read the list of nonstandard columns somehow."""
        # Define the projects
        self.projects.clear()
        self.projects.addItem("New Project...")
        prev_proj = []

        for task in api.task_dict[module]:  # Iterate through the task list
            task_project = task.get_project()  # Get the project of the task
            if task_project is not None and not task_project in prev_proj:  # If the project is not already in the list
                self.projects.addItem(str(task_project))  # Add the project to the projects list
                prev_proj.append(task_project)  # Add the project to the previous projects list

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

            # set the variable `module` to the current text of the annotation field

            task_details = AddTaskDialog.TaskDetails(self.description.text(), self.tag.text(), self.priorities.currentText(),
                                                     task_project, self.recurrence, self.due_date) # create a variable for the task details

            # Reset the input fields after adding the task
            self.tag.clear()
            self.tags_list.clear()
            self.description.clear()
            self.projects.clear()
            self.priorities.setCurrentIndex(0)
            self.remove_all_tags()

            return task_details # Return the task details

        self.description.clear() # Clear the description field so the text doesn't repopulate on the next task creation
        return None

    def remove_tag(self, tag_button):
        """Remove a tag from the UI only."""
        self.tags_list.remove(tag_button.text()) #remove the tag from the tags list
        self.tag_bubble_layout.removeWidget(tag_button)  # Remove from layout
        tag_button.deleteLater()  # Delete the widget

    def remove_all_tags(self):
        for i in reversed(range(self.tag_bubble_layout.count())): #iterates through the tags to remove all tag bubbles
            widget = self.tag_bubble_layout.itemAt(i).widget()
            if widget:
                self.tag_bubble_layout.removeWidget(widget) #removes widget
                widget.deleteLater()  # Remove the widget and free memory

    def open_recurrence(self) -> None:
        self.is_recurring = self.recurring_box.isChecked()
