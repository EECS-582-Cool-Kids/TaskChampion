""" Prologue
 *  Module Name: menubar.py
 *  Purpose: Module for the MenuBar class, which is a class for creating the menu bar in the application window.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Mo Morgan
 *  Date: 2/15/2025
 *  Last Modified: 2/23/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from PySide6 import QtWidgets, QtGui

class MenuBar(QtWidgets.QMenuBar):
    """Creates the window menu for the application."""
    def __init__(self, parent=None): # parent=None means that the parent is the main window. This might wrap the macOS's system-wide menu bar.
        super().__init__(parent)    # Call the parent class's constructor

        self.file_menu = self.addMenu("File")  # Create the File menu
        self.exit_action = QtGui.QAction("Exit", self)  # Create the Exit action
        self.exit_action.triggered.connect(QtWidgets.QApplication.quit) # Connect the Exit action to the quit function
        self.file_menu.addAction(self.exit_action)   # Add the Exit action to the File menu

        help_menu = self.addMenu("Help")  # Create the Help menu
        self.about_action = QtGui.QAction("About", self) # Create the About action
        self.about_action.triggered.connect(self.show_about_dialogue) # Connect the About action to the show_about_dialogue function
        help_menu.addAction(self.about_action)   # Add the About action to the Help menu


    def show_about_dialogue(self):
        """Shows the about dialogue."""
        about_dialogue = QtWidgets.QMessageBox() # Create a message box
        about_dialogue.setWindowTitle("About Task Champion") # Set the title of the dialogue box window
        about_dialogue.setText("Task Champion is a customizable task manager application designed to help you manage the things you gotta get done.")

        # Show the dialogue box. exec() is used to show the dialogue box and wait for the user
        # to close it before continuing execution. It should only be called after all of the
        # desired properties of the dialogue box have been set.
        about_dialogue.exec()
