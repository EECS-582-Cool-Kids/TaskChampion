"""
 *  Module Name: edit_task_dialog.py
 *  Purpose: Allows users to edit tasks when selected.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Mo Morgan, Richard Moser, Derek Norton
 *  Date: 2/15/2025
 *  Last Modified: 2/15/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from PySide6 import QtCore, QtWidgets
from .buttonbox import Buttonbox
from .textbox import Textbox

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