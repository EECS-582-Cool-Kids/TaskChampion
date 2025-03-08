""" Prologue:
 *  Module Name: edit_task_dialog.py
 *  Purpose: Allows users to edit tasks when selected.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Mo Morgan, Richard Moser, Derek Norton
 *  Date: 2/15/2025
 *  Last Modified: 3/7/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from PySide6 import QtWidgets

class EditTaskDialog(QtWidgets.QDialog):
    def __init__(self, description="", due="", priority=""):
        super().__init__()
        self.form = QtWidgets.QFormLayout()

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
        self.priority_text.addItems(["H", "M", "L"]) # Add the priority options to the combo box
        self.priority_text.setCurrentText(priority) # Set the current text to the priority of the task

        self.form.addRow("Description", self.description_text)
        self.form.addRow("Due", self.due_date)
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
        """
        Returns the due date of the task as a string in the format 'yyyy-MM-dd'.

         Returns:
             str: The due date of the task
             """
        return self.due_date.date().toString("yyyy-MM-dd")

    @property
    def priority(self):
        return self.priority_text.currentText()