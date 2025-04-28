""" Prologue:
 *  Module Name: preset_modules_dialog.py
 *  Purpose: The dialog box for adding a preset module to TaskChampion.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Mo Morgan
 *  Date: 4/25/2025
 *  Last Modified: 4/27/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""
from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton

class PresetModulesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preset Modules")
        self.layout = QVBoxLayout()

        # Add "Workouts" button
        self.workouts_button = QPushButton("Workouts")
        self.workouts_button.clicked.connect(lambda: self.set_selected_module("Workouts"))  # Connect the button to the select_workouts method
        self.layout.addWidget(self.workouts_button)

        # Add "Personal Finance" button
        self.personal_finance_button = QPushButton("Personal Finance")
        self.personal_finance_button.clicked.connect(lambda: self.set_selected_module("Personal Finance"))
        self.layout.addWidget(self.personal_finance_button)

        # Add "Programming Project" button
        self.programming_project_button = QPushButton("Programming Project")
        self.programming_project_button.clicked.connect(lambda: self.set_selected_module("Programming Project"))
        self.layout.addWidget(self.programming_project_button)

        self.selected_module = None
        self.setLayout(self.layout)

    # setter for selected_module
    def set_selected_module(self, module_name):
        self.selected_module = module_name
        self.accept()

    def get_selected_module(self):

        return self.selected_module