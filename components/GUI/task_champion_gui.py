""" Prologue:
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

from PySide6 import QtWidgets
from components.GUI.task_champion_widget import TaskChampionWidget
from PySide6.QtCore import qInstallMessageHandler, Qt


def handler(msg_type, context, msg):
    """Suppresses QSS style sheet warnings (which are not errors)."""
    if "Could not parse" in msg:  # If the message contains "Could not parse"
        pass  # Do nothing.

qInstallMessageHandler(handler)  # Install the message handler.


class TaskChampionGUI:
    """The main application class for Task Champion."""  
    def __init__(self): 
        # Initialize the Qt App and TaskWarrior objects  
        self.qtapp = QtWidgets.QApplication([])  # Create a new Qt Application.
        
        # Initialize the main Qt Widget 
        self.main_widget = TaskChampionWidget(self.load_styles)  # Create a new TaskChampionWidget.
        self.main_widget.setWindowTitle("Task Champion")  # Set the window title.
        # self.main_widget.resize(800, 400) # set basic window size.
        self.main_widget.resize(1100, 400)
        self.main_widget.show() # show the window

        # self.main_widget.move(0, 0)
        self.move_window()


        self.style_str = ""  # Initialize the style string.
        with open ('styles/style.qss', 'r')as f:  # Open the style file.
            self.style_str = f.read()  # Read the style file.

        # self.main_widget.show() # show the window
        # self.main_widget.move(0, 0) # move the window to 0,0

        self.load_styles()  # Load the styles.
    
    def move_window(self, x=None, y=None):
        if x is None or y is None:
            # put the window in the upper right corner
            screen = QtWidgets.QApplication.primaryScreen()  # Get the primary screen.
            screen_size = screen.size()  # Get the size of the screen.
            screen_width = screen_size.width()  # Get the width of the screen.
            screen_height = screen_size.height()  # Get the height of the screen.
            window_width = self.main_widget.width()  # Get the width of the window.
            window_height = self.main_widget.height()  # Get the height of the window.
            x = screen_width - window_width  # Calculate the x position of the window.
            y = 0  # Calculate the y position of the window
        # print(f"Moving window to {x}, {y}")
        self.main_widget.move(x, y)  # Move the window to the x, y position.

    def load_tasks(self):
        self.main_widget.grids[0].fillGrid()  # Fill the grid.
        self.load_styles()  # Load the styles.


    def load_styles(self):
        self.qtapp.setStyleSheet(self.style_str)  # Set the style sheet of the Qt Application to be the style string.

    def load_tasks(self):
        self.main_widget.grids[0].fill_grid()  # Fill the grid.
        self.main_widget.xp_bars.update_bars()  # Update the XP bars.
        self.load_styles()  # Load the styles.

    def on_exit(self) -> int:
        """The behavior for exiting the application."""
        return self.qtapp.exec()  # Execute the Qt Application.