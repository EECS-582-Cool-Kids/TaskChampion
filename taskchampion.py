"""
 *  Module Name: taskchampion.py
 *  Purpose: Entry point for the TaskChampion Application.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Jacob Wilkus, Ethan Berkley, Mo Morgan, Richard Moser, Derek Norton
 *  Date: 2/15/2025
 *  Last Modified: 2/23/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

import sys
from PySide6 import QtCore, QtWidgets
from taskw_ng import TaskWarrior
from typing import TypeAlias, Literal
from utils.task import Task, status_t, priority_t
from components.add_task_dialog import AddTaskDialog
from components.task_row import TaskRow, COLS
from components.align import ALIGN
from components.menubar import MenuBar 
from components.edit_task_dialog import EditTaskDialog
from utils import api
from components.task_champion_gui import TaskChampionGUI  # Import the GUI class

# Program entry point
if __name__ == "__main__":
    app = TaskChampionGUI()  # Create a new TaskChampionGUI object.
    app.load_tasks()
    # TODO: Consider doing this in a better way.
    refresh_styles = app.load_styles
    sys.exit(app.on_exit())  # Exit the application.
    logger.exit()
