""" Prologue:
 *  Module Name: add_module_dialog.py
 *  Purpose: The dialog box for adding a module. 
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Mo Morgan
 *  Date: 3/26/2025
 *  Last Modified: 3/26/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects:   Updates the `self.config` dictionary with the new module and its attributes.
                    Saves the updated configuration to the configuration file using `save_module_config`.

 *  Invariants: None
 *  Known Faults: None encountered
"""

from PySide6.QtWidgets import QDialog, QLineEdit, QGroupBox, QVBoxLayout, QCheckBox, \
    QDialogButtonBox, QFormLayout, QPushButton, QMessageBox
from PySide6.QtCore import Signal
from typing import Optional
import os
from utils.config_loader import load_module_config, save_module_config
from utils.config_paths import CONFIG_DIR, MODULES_CONFIG_FILE
from components.Dialogs.preset_modules_dialog import PresetModulesDialog


class AddModuleDialog(QDialog):
    class ModuleDetails:
        def __init__(self, module_name: str, attributes: list[str]):
            self.grid_name = module_name
            self.attributes = attributes

    def __init__(self, config_file=MODULES_CONFIG_FILE):
        super().__init__()
        os.makedirs(CONFIG_DIR, exist_ok=True)
        self.setWindowTitle("Add Module")
        self.form = QFormLayout() # Create a form layout for the dialog
        self.layout = QVBoxLayout()

        self.config_file = config_file
        self.config: dict[str, list[str]] = load_module_config(self.config_file)

        self.new_module = QLineEdit()
        self.new_module.setPlaceholderText("Module Name")

        # List of Taskwarrior attributes with checkboxes
        self.attributes_group = QGroupBox("Task Attributes")
        self.attributes_layout = QVBoxLayout()

        # Annotations field will not be offered, uuid field will be automatically generated for all tasks
        self.task_attributes = ['Priority', 'Due Date', 'Project', 'Tags', 'Recur', 'Status', 'Start', 'Urgency']

        self.form.addRow("New Module", self.new_module)

        for attr in self.task_attributes:
            checkbox = QCheckBox(attr)
            checkbox.setStyleSheet("color: black;")  # Make text black
            self.attributes_layout.addWidget(checkbox)

        self.attributes_group.setLayout(self.attributes_layout)
        self.form.addWidget(self.attributes_group)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok
                                                  | QDialogButtonBox.StandardButton.Cancel)
        self.layout.addLayout(self.form)
        self.layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.buttons.setStyleSheet("background-color: #8aa1f6; ")

        self.setLayout(self.layout)

        #Add "Preset Modules" button to the dialog
        self.preset_modules_button = QPushButton("Preset Modules") # Create a button for preset modules
        self.preset_modules_button.clicked.connect(self.open_preset_modules_dialog) # Connect the button to the open_preset_modules_dialog method
        self.layout.addWidget(self.preset_modules_button) # Add the button to the layout

        # Signal to notify when a module is created
        self.module_created = Signal()


    def add_module(self) -> Optional[ModuleDetails]:
        """Add a module to the GUI and save it to the configuration file."""
        new_module = {} # Create an empty dictionary to store the new module.
        attributes = [] # Create an empty list to store the attributes.

        if self.exec(): # If the dialog is accepted...
            module_name = self.new_module.text() # Get the module name from the textbox.

            # Get the attributes from the dialog, only if the checkbox is checked.
            checkboxes = (self.attributes_layout.itemAt(i).widget() for i in range(self.attributes_layout.count()))
            for checkbox in checkboxes:
                if checkbox.isChecked():
                    attributes.append(checkbox.text())

            attributes.append('Description') # Easier this way imo

            new_module[module_name] = attributes # Add the module and its attributes to the dictionary.
            self.config[module_name] = attributes # Add the module and its attributes to the configuration.

            save_module_config(self.config, self.config_file) # Save the configuration to the file.

            self.new_module.clear() # Clear the module name to prevent it showing upon the next module creation.
            return AddModuleDialog.ModuleDetails(module_name, attributes)

        self.new_module.clear() # Clear the module name if the dialog is cancelled to prevent it showing upon the next module creation.
        # uncheck all checkboxes
        for i in range(self.attributes_layout.count()):
            self.attributes_layout.itemAt(i).widget().setChecked(False)
        return None

    def open_preset_modules_dialog(self):
        """Opens the Preset Modules dialog, allowing the user to select a predefined module."""
        dialog = PresetModulesDialog()
        dialog.setStyleSheet("background-color: #8aa1f6; color: black;")
        if dialog.exec():
            selected_module = dialog.get_selected_module()
            if selected_module:
                self.create_preset_module(selected_module)

    def create_preset_module(self, selected_module):
        """ Creates a preset module with predefined attributes based on the selected module name.
            The module and its attributes are saved to the configuration file.

            Args:
                selected_module (str): The name of the selected preset module.
                                       Expected values are "Workouts", "Personal Finance", or "Programming Project".
        """
        if selected_module == "Workouts":
            attributes = ["Description", "Type of Workout", "Number of Sets", "Number of Reps", "Weight", "Duration"]
            self.config["Workouts"] = attributes
            save_module_config(self.config, self.config_file)
        elif selected_module == "Personal Finance":
            attributes = ["Description", "Cash In", "Cash Out", "Transaction Type", "Transaction Date", "Date"]
            self.config["Personal Finance"] = attributes
            save_module_config(self.config, self.config_file)
        else:
            attributes = ["Description", "Project", "Due Date", "Priority"]
            self.config["Programming Project"] = attributes
            save_module_config(self.config, self.config_file)

        # Tell the user that the app has to be reset to see the new preset module using a message box
        user_notice = QMessageBox()
        user_notice.setStyleSheet("background-color: #8aa1f6; color: black;")
        user_notice.setWindowTitle("Restart Required")
        user_notice.setText(f"Please restart TaskChampion to see the new preset module: {selected_module}.")
        user_notice.setStandardButtons(QMessageBox.StandardButton.Ok)
        user_notice.exec()

