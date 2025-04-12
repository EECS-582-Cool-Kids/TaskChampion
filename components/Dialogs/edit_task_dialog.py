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

from utils.task_api import api


class EditTaskDialog(QtWidgets.QDialog):
    def __init__(self, delete_task, description="", due="", priority="", project="", tags=[]):
        super().__init__()
        self.setWindowTitle("Edit Task")  # Set the title of the dialog
        self.form = QtWidgets.QFormLayout()  # Create a form layout for the dialog
        self.deletion_function = delete_task  # Function to delete the task

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

        # OK and Cancel buttons
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok
                                      | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        self.delete_button = QtWidgets.QPushButton("Delete Task")  # Create a delete button
        self.delete_button.clicked.connect(self.delete)  # Connect the delete button to the delete function

        layout = QtWidgets.QVBoxLayout()  # Create a vertical layout for the dialog
        layout.addLayout(self.form)  # Add the form layout to the vertical layout
        layout.addWidget(button_box)  # Add the button box to the vertical layout
        layout.addWidget(self.delete_button)  # Add the delete button to the vertical layout

        self.setLayout(layout)  # Set the layout of the dialog to the vertical layout

        # delete confirmation popup
        button_box.accepted.connect(self.accept)  # Connect the OK button to accept the dialog
        button_box.rejected.connect(self.reject)  # Connect the Cancel button to reject the dialog

        # handle projects
        # Create a line edit for the project input
        self.projects = QtWidgets.QComboBox()  # Create a combo box for the project
        self.new_project = QtWidgets.QLineEdit()  # Create a line edit for the new project input

        # Store previously used projects
        self.project_history = []  # List to store previously used projects
        self.project_list = []  # List to store currently added projects

        # Create a layout to hold the project input field and button side by side
        self.project_layout = QtWidgets.QHBoxLayout()  # Create a horizontal layout for the project input field and button

        self.populate_project_list() # Populate the project list with existing projects


        # handle tags
        # Create a line edit for the tag input
        self.tag = QtWidgets.QLineEdit()  # Create a line edit for the tag input
        self.tag.setPlaceholderText("Enter tag name")  # Set the placeholder text for the tag input field

        # Store previously used tags
        self.tag_history = []  # List to store previously used tags
        self.tags_list = []  # List to store currently added tags

        # Create "Add Tag" button
        self.add_tag_button = QtWidgets.QPushButton("Add Tag")  # Create a button to add a tag
        self.add_tag_button.clicked.connect(self.add_tag_to_list)  # Connect the button to the add tag function

        # Create a layout to hold the tag input field and button side by side
        self.tag_layout = QtWidgets.QHBoxLayout()  # Create a horizontal layout for the tag input field and button
        self.tag_layout.addWidget(self.tag)  # Add the tag input field to the layout
        self.tag_layout.addWidget(self.add_tag_button)  # Add the button to the layout
        self.tag_layout.addStretch()  # Add stretch to the layout to push the button to the right


        # Create a layout to hold the added tag "bubbles"
        self.tag_bubble_widget = QtWidgets.QWidget()  # Create a widget to hold the tag bubbles
        self.tag_bubble_layout = QtWidgets.QHBoxLayout(self.tag_bubble_widget)  # Create a horizontal layout for the tag bubbles
        self.tag_bubble_layout.setContentsMargins(0, 0, 0, 0)  # Set the margins of the layout to 0
        self.tag_bubble_layout.setSpacing(2)  # Space between tags

        self.populate_tag_list(tags)  # Populate the tag list with existing tags


        self.tag.mousePressEvent = lambda event: self.show_tag_menu() # Connect tag input field to show menu on focus

        # Add all the widgets to the form layout
        self.form.addRow("Description", self.description_text)      # description
        self.form.addRow("Priority", self.priority_text)            # priority
        self.form.addRow("Project", self.projects)                  # project
        self.form.addRow("New Project", self.new_project)           # new project input
        self.form.addRow("Due Date", self.due_date)                 # due date
        self.form.addRow("Tags", self.tag_layout)                   # tag input field and button
        self.form.addRow(self.tag_bubble_widget)                    # tag bubbles

    # These properties make using this dialog a little cleaner. It's much
    # nicer to type "addDialog.address" to retrieve the address as compared
    # to "addDialog.addressText.toPlainText()"
    @property
    def description(self):
        return self.description_text.text()

    @property
    def priority(self):
        if self.priority_text.currentText() == "None":
            return ""
        return self.priority_text.currentText()

    @property
    def due(self):
        return self.due_date.date().toString("yyyy-MM-dd")

    @property
    def project(self):
        if self.projects.currentText() == "New Project...":
            return self.new_project.text()  # If the user selects "New Project...", return the text from the new project input field
        if self.projects.currentText() == "":
            return None  # If the user doesn't select a project, return None
        return self.projects.currentText()  # Return the selected project from the combo box

    @property
    def tags(self):
        return self.tags_list  # Return the list of tags

    def delete(self):
        response = QtWidgets.QMessageBox.question(self, "Delete Task", "Are you sure you want to delete this task?",
                                                  QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

        if response == QtWidgets.QMessageBox.StandardButton.Yes: # If the user clicks Yes, the task will be deleted.
            self.deletion_function()  # Call the deletion function passed to the dialog
            self.accept()  # Accept the dialog to close it

        else: # If the user doesn't want to delete the task, then the dialog will close.
            return  # Return to close the dialog

    def populate_project_list(self):
        project_history = []  # List to store previously used projects
        for task in api.task_list:  # Iterate through the task list
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

        self.tag.clear()  # Clear the input field after adding the tag

    def show_tag_menu(self):
        menu = QtWidgets.QMenu(self)
        for tag in self.tag_history:
            action = menu.addAction(tag)
            action.triggered.connect(lambda checked, t=tag: self.tag.setText(t))
        menu.setFixedWidth(self.tag.width())
        menu.exec(self.tag.mapToGlobal(self.tag.rect().bottomLeft()))

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