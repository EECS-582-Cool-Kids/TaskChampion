"""
 *  Module Name: task_champion_gui.py
 *  Purpose: Initialization of the GUI.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Mo Morgan, Richard Moser, Derek Norton
 *  Date: 2/15/2025
 *  Last Modified: 2/25/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from typing import Callable
from PySide6 import QtWidgets
from .task_champion_widget import TaskChampionWidget

class TaskChampionGUI:
    """The main application class for Task Champion."""  
    def __init__(self): 
        # Initialize the Qt App and TaskWarrior objects  
        self.qtapp = QtWidgets.QApplication([])  # Create a new Qt Application.
        
        # Initialize the main Qt Widget 
        self.main_widget = TaskChampionWidget(self.load_styles)  # Create a new TaskChampionWidget.
        self.main_widget.setWindowTitle("Task Champion")  # Set the window title.
        self.main_widget.resize(800, 400) # set basic window size.

        self.style_str = ""  # Initialize the style string.
        with open ('styles/style.qss', 'r')as f:  # Open the style file.
            self.style_str = f.read()  # Read the style file.

        self.main_widget.show() # show the window
        self.main_widget.move(0, 0) # move the window to 0,0

        self.load_styles()  # Load the styles.
    
    def load_styles(self):
        self.qtapp.setStyleSheet(self.style_str)  # Set the style sheet of the Qt Application to be the style string.

    def load_tasks(self):
        self.main_widget.grids[0].fillGrid()
        self.load_styles()

    def on_exit(self) -> int:
        """The behavior for exiting the application."""
        return self.qtapp.exec()  # Execute the Qt Application.