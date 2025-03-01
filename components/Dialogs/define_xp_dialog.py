"""
 *  Module Name: define_xp_dialog.py
 *  Purpose: Defines the XP configuration dialog.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Mo Morgan
 *  Date: 2/15/2025
 *  Last Modified: 2/28/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: FileNotFoundError: if the configuration file does not exist, json.JSONDecodeError:
                                if the contents of the configuration file are not valid JSON.
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

import json

from PySide6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, \
    QMessageBox, QComboBox


class XPConfigDialog(QDialog):

    # Add a class attribute to store the priority values
    PRIORITY_T = ["H", "M","L"]

    def __init__(self, config_file):
        super().__init__()
        self.setWindowTitle("Edit XP Configuration")
        self.config_file = config_file
        self.config: dict[str, any] = self.load_config()

        # Layout
        layout = QVBoxLayout(self)

        # Table for priorities
        self.priority_table = QTableWidget(len(self.config['priorities']), 2)
        self.priority_table.setHorizontalHeaderLabels(["Priority", "XP"])
        layout.addWidget(self.priority_table)

        # Populate table from config
        for row, (priority, xp) in enumerate(self.config['priorities'].items()):
            priority_dropdown = QComboBox() # Create a dropdown for the priority
            priority_dropdown.addItems(self.PRIORITY_T) # Add the priority values to the dropdown
            priority_dropdown.setCurrentText(priority) # Set the current text to the priority
            priority_dropdown.setDisabled(True) # Disable editing of priority

            self.priority_table.setCellWidget(row, 0, priority_dropdown) # Set the priority cell
            self.priority_table.setItem(row, 1, QTableWidgetItem(str(xp))) # Set the xp cell

        # Table for tags
        self.tag_table = QTableWidget(len(self.config['tags']), 2)
        self.tag_table.setHorizontalHeaderLabels(["Tag", "XP"])
        layout.addWidget(self.tag_table)

        for row, (tag, xp) in enumerate(self.config['tags'].items()):
            self.tag_table.setItem(row, 0, QTableWidgetItem(tag))
            self.tag_table.setItem(row, 1, QTableWidgetItem(str(xp)))

        add_tag_button = QPushButton("Add Tag")
        add_tag_button.clicked.connect(self.add_tag_row)
        layout.addWidget(add_tag_button)

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_config)
        layout.addWidget(save_button)

    def load_config(self):
        """
        Loads configuration data from a file into a dictionary attribute.

        This method reads a JSON formatted configuration file specified by the
        `config_file` attribute and populates the `config` attribute with the
        parsed content.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            json.JSONDecodeError: If the configuration file's contents are not
                valid JSON.
        """
        try:
            with open(self.config_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # return some arbitrary default config if the file doesn't exist
            return {"priorities": {'H': 10, 'M': 5, 'L': 1}, "tags": {}}


    def save_config(self):
        # Save table data back to the config file
        priorities = {}
        for row in range(self.priority_table.rowCount()):
            # assign a variable `priority` to the current text of the priority dropdown
            priority = self.priority_table.cellWidget(row, 0).currentText()
            xp = int(self.priority_table.item(row, 1).text())
            priorities[priority] = xp
        #TODO: we will eventually need to figure out what

        self.config['priorities'] = priorities
        with open(self.config_file, 'w') as file:
            json.dump(self.config, file)

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