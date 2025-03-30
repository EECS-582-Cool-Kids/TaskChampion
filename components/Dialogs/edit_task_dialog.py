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
    def __init__(self, delete_task, description="", due="", priority="",   project="", tags=[]):
        super().__init__()
        self.form = QtWidgets.QFormLayout()
        self.deletion_function = delete_task

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

        # handle tags
        # Create a line edit for the tag input
        self.tag = QtWidgets.QLineEdit()
        self.tag.setPlaceholderText("Enter tag name")

        # Store previously used tags
        self.tag_history = []  # List to store previously used tags
        self.tags_list = []  # List to store currently added tags

        # Create "Add Tag" button
        self.add_tag_button = QtWidgets.QPushButton("Add Tag")
        self.add_tag_button.clicked.connect(self.add_tag_to_list)

        # Create a layout to hold the tag input field and button side by side
        self.tag_layout = QtWidgets.QHBoxLayout()
        self.tag_layout.addWidget(self.tag)
        self.tag_layout.addWidget(self.add_tag_button)

        # Create a layout to hold the added tag "bubbles"
        self.tag_bubble_widget = QtWidgets.QWidget()
        self.tag_bubble_layout = QtWidgets.QHBoxLayout(self.tag_bubble_widget)
        self.tag_bubble_layout.setContentsMargins(0, 0, 0, 0)
        self.tag_bubble_layout.setSpacing(5)  # Space between tags
        # self.form.addRow(self.tag_bubble_widget)

        # for each existing tag, call populate_tag_list to create a button
        # for tag in tags:
            # self.tag_history.append(tag)
            # self.populate_tag_list(tag)
        self.populate_tag_list(tags)


        self.tag.mousePressEvent = lambda event: self.show_tag_menu() # Connect tag input field to show menu on focus

        self.tag_layout.addWidget(self.tag)
        # Add the tag input field to the layout
        self.tag_layout.addWidget(self.add_tag_button)

        # Add all the widgets to the form layout
        self.form.addRow("Description", self.description_text)
        self.form.addRow("Priority", self.priority_text)
        # self.form.addRow("Project", self.projects)
        # self.form.addRow("New Project", self.new_project)
        self.form.addRow("Due Date", self.due_date)
        self.form.addRow("Tags", self.tag_layout)
        self.form.addRow(self.tag_bubble_widget)

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


    def tags(self):
        return self.tags_list

    def delete(self):
        response = QtWidgets.QMessageBox.question(self, "Delete Task", "Are you sure you want to delete this task?",
                                                  QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

        if response == QtWidgets.QMessageBox.StandardButton.Yes: # If the user clicks Yes, the task will be deleted.
            self.deletion_function()
            self.accept()

        else: # If the user doesn't want to delete the task, then the dialog will close.
            return

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