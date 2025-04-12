""" Prologue
 *  Module Name: define_xp_dialog.py
 *  Purpose: Defines the XP configuration dialog.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Mo Morgan, Ethan Berkley
 *  Date: 2/15/2025
 *  Last Modified: 3/2/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: FileNotFoundError: if the configuration file does not exist, json.JSONDecodeError:
                                if the contents of the configuration file are not valid JSON.
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, \
    QMessageBox, QComboBox
from PySide6.QtCore import Signal
from typing import Any
from utils.config_loader import load_config, save_xp_config
import os
from utils.config_paths import CONFIG_DIR, XP_CONFIG_FILE

class XPConfigDialog(QDialog):

    # Add a class attribute to store the priority values
    PRIORITY_T = ["H", "M", "L"]
    xp_values_updated = Signal(dict) # Signal to indicate that the XP values have been updated

    def __init__(self, config_file=XP_CONFIG_FILE):
        super().__init__()
        os.makedirs(CONFIG_DIR, exist_ok=True)

        self.setWindowTitle("Edit XP Configuration")
        self.config_file = config_file
        self.config: dict[str, Any] = load_config(self.config_file)

        # Layout
        layout = QVBoxLayout(self)

        # Table for priorities
        self.priority_table = QTableWidget(len(self.config['priorities']), 2)
        self.priority_table.setHorizontalHeaderLabels(["Priority", "XP"])
        layout.addWidget(self.priority_table)

        # Populate table from config
        for row, (priority, xp) in enumerate(self.config['priorities'].items()):
            priority_dropdown = QComboBox()
            priority_dropdown.addItems(self.PRIORITY_T) # Add the priority values to the dropdown
            priority_dropdown.setCurrentText(priority) # Set the current text to the priority
            priority_dropdown.setDisabled(True) # Disable editing of priority
            self.priority_table.setItem(row, 0, QTableWidgetItem(priority))
            self.priority_table.setItem(row, 1, QTableWidgetItem(str(xp)))

        # Table for editing tag xp values
        self.tag_table = QTableWidget(len(self.config['tags']), 2)
        self.tag_table.setHorizontalHeaderLabels(["Tag", "XP"])
        layout.addWidget(self.tag_table)

       # Populate tag table using file
        for row, (tag, xp) in enumerate(self.config['tags'].items()):
            self.tag_table.setItem(row, 0, QTableWidgetItem(tag))
            self.tag_table.setItem(row, 1, QTableWidgetItem(str(xp)))

        # Table for editing project xp values
        self.project_table = QTableWidget(len(self.config['projects']), 2)
        self.project_table.setHorizontalHeaderLabels(["Project", "XP"])
        layout.addWidget(self.project_table)

        # Populate project table using file
        for row, (project, xp) in enumerate(self.config['projects'].items()):
            self.project_table.setItem(row, 0, QTableWidgetItem(project))
            self.project_table.setItem(row, 1, QTableWidgetItem(str(xp)))

        # Table for editing module xp values
        self.module_table = QTableWidget(len(self.config['modules']), 2)
        self.module_table.setHorizontalHeaderLabels(["Module", "XP"])
        layout.addWidget(self.module_table)

        # Add tag button
        add_tag_button = QPushButton("Add Tag")
        add_tag_button.clicked.connect(self.add_tag_row)
        layout.addWidget(add_tag_button)

        # Add project button
        add_project_button = QPushButton("Add Project")
        add_project_button.clicked.connect(self.add_project_row)
        layout.addWidget(add_project_button)

        # Add module button
        add_module_button = QPushButton("Add Module")
        add_module_button.clicked.connect(self.add_module_row)
        layout.addWidget(add_module_button)

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_config)
        layout.addWidget(save_button)

    def save_config(self):
        # Save table data back to the config file
        priorities = {}
        tags = {}
        projects = {}
        modules = {}

        for row in range(self.priority_table.rowCount()):
            priority = self.priority_table.item(row, 0).text()
            xp = float(self.priority_table.item(row, 1).text())
            priorities[priority] = xp

        for row in range(self.tag_table.rowCount()):
            tag = self.tag_table.item(row, 0).text()
            xp = float(self.tag_table.item(row, 1).text())
            tags[tag] = xp

        for row in range(self.project_table.rowCount()):
            project = self.project_table.item(row, 0).text()
            xp = float(self.project_table.item(row, 1).text())
            projects[project] = xp

        for row in range(self.module_table.rowCount()):
            module = self.module_table.item(row, 0).text()
            xp = float(self.module_table.item(row, 1).text())
            modules[module] = xp
            
        self.config['priorities'] = priorities # Update the priorities
        self.config['tags'] = tags # Update the tags
        self.config['projects'] = projects # Update the projects
        self.config['modules'] = modules # Update the modules

        # Tell XpControllerWidget to update stuff.
        self.xp_values_updated.emit(self.config)

        save_xp_config(self.config, self.config_file)

        QMessageBox.information(self, "Success", "Configuration saved!", QMessageBox.StandardButtons.Ok)

    def add_tag_row(self):
        """
        Inserts a new row into the tag table with two empty cells.

        The method dynamically determines the current number of rows in the
        tag_table, appends one additional row, and initializes the first two
        columns of the newly inserted row with empty QTableWidgetItem objects.

        Raises
        ------
        TypeError
            If the tag_table is not properly instantiated or configured.
        """
        row_position = self.tag_table.rowCount()
        self.tag_table.insertRow(row_position)
        self.tag_table.setItem(row_position, 0, QTableWidgetItem(""))
        self.tag_table.setItem(row_position, 1, QTableWidgetItem(""))

    def add_project_row(self):
        """
        Adds a new row to the project table within the Config menu. Each added row will have two
        empty cells initialized in the newly created row. The row is appended
        at the current count of rows in the table.

        Raises
        ------
        TypeError
            If the project_table is not properly instantiated or configured.
        """
        row_position = self.project_table.rowCount()
        self.project_table.insertRow(row_position)
        self.project_table.setItem(row_position, 0, QTableWidgetItem(""))
        self.project_table.setItem(row_position, 1, QTableWidgetItem(""))

    def add_module_row(self):
        """
        Adds a new row to the module table within the Config menu. Each added row will have two
        empty cells initialized in the newly created row. The row is appended
        at the current count of rows in the table.

        Raises
        ------
        TypeError
            If the module_table is not properly instantiated or configured.
        """
        row_position = self.module_table.rowCount()
        self.module_table.insertRow(row_position)
        self.module_table.setItem(row_position, 0, QTableWidgetItem(""))
        self.module_table.setItem(row_position, 1, QTableWidgetItem(""))

