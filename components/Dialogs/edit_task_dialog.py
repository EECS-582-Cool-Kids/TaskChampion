""" Prologue:
 *  Module Name: edit_task_dialog.py
 *  Purpose: Allows users to edit tasks when selected.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Mo Morgan, Richard Moser, Derek Norton
 *  Date: 2/15/2025
 *  Last Modified: 3/14/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from PySide6 import QtWidgets

class EditTaskDialog(QtWidgets.QDialog):
    def __init__(self, delete_task, description="", due="", priority="", project="", tags=[], module_name="Main"):
        super().__init__()
        self.form = QtWidgets.QFormLayout()
        self.deletion_function = delete_task

        self.module_name=module_name

        self.description_text = QtWidgets.QLineEdit(description) # set the description text to the description of the task

        self.due_date = QtWidgets.QDateEdit() # Create a date edit object for the due date
        # set the due date to the current date + 1 day
        self.due_date.setDate(self.due_date.date().currentDate().addDays(1))
        # and bring up the calendar if the arrow is clicked
        self.due_date.setCalendarPopup(True)
        if due:
            # if the format of `due` isn't yyy-MM-dd, then the date will be set to the current date + 1 day. The user will have
            # to use the calendar to set the date to the correct one.

            self.due_date.setDate(self.due_date.date().fromString(due, "yyyy-MM-dd"))


        self.priority_text = QtWidgets.QComboBox() # Create a combo box for the priority
        self.priority_text.addItems(["None", "H", "M", "L"]) # Add the priority options to the combo box
        self.priority_text.setCurrentText(priority) # Set the current text to the priority of the task

        self.form.addRow("Description", self.description_text)
        self.form.addRow("Due", self.due_date)
        self.form.addRow("Priority", self.priority_text)


        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok
                                      | QtWidgets.QDialogButtonBox.StandardButton.Cancel)

        self.delete_button = QtWidgets.QPushButton("Delete Task")
        self.delete_button.clicked.connect(self.delete)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(self.form)
        layout.addWidget(button_box)
        layout.addWidget(self.delete_button)

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
        """
        Returns the due date of the task as a string in the format 'yyyy-MM-dd'.

         Returns:
             str: The due date of the task
             """
        return self.due_date.date().toString("yyyy-MM-dd")

    @property
    def priority(self):
        if self.priority_text.currentText() == "None":
            return ""
        return self.priority_text.currentText()

    def delete(self):
        response = QtWidgets.QMessageBox.question(self, "Delete Task", "Are you sure you want to delete this task?",
                                                  QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

        if response == QtWidgets.QMessageBox.StandardButton.Yes: # If the user clicks Yes, the task will be deleted.
            self.deletion_function()
            self.accept()

        else: # If the user doesn't want to delete the task, then the dialog will close.
            return  # Return to close the dialog

    def populate_project_list(self):
        project_history = []  # List to store previously used projects
        for task in api.task_dict[self.module_name]:  # Iterate through the task list
            task_project = task.get_project()  # Get the project of the task
            if task_project is not None and not task_project in project_history:  # If the project is not already in the list
                self.projects.addItem(task_project)  # Add the project to the projects list
                project_history.append(task_project)  # Add the project to the previous projects list
        self.projects.addItem("New Project...")

    def add_project_to_list(self):
        project_text = self.new_project.text().strip()  # Get the text from the project input field
        if project_text == '':  #if button is pressed while empty skips adding
            return
        if project_text and project_text not in self.project_history:  # Add the project to history
            self.project_history.append(project_text)


    def remove_project(self, project_button):
        """Remove a project from the UI only."""
        self.project_list.remove(project_button.text())
        project_button.deleteLater()  # Delete the widget

    def populate_tag_list(self, tags):
        for tag_text in tags:
            if tag_text and tag_text not in self.tag_history:
                self.tag_history.append(tag_text)  # Add the tag to history
            if tag_text not in self.tags_list: #if tag is already added dont add the new tag
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

    def add_tag_to_list(self):
        tag_text = self.tag.text().strip()
        if tag_text == '': #if button is pressed while empty skips adding
            return
