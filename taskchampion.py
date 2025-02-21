"""
 *  Module Name: taskchampion.py
 *  Purpose: Entry point for the TaskChampion Application.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Jacob Wilkus, Ethan Berkley, Mo Morgan, Richard Moser
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
from taskw_ng import TaskWarrior
from typing import TypeAlias, Literal
from utils.task import Task, status_t, priority_t
from components import AddTaskDialog, TaskRow, COLS, ALIGN, menubar
from utils import TaskWarriorInstance

import sys
from components.task_champion_gui import TaskChampionGUI  # Import the GUI class
from utils import TaskWarriorInstance

# Program entry point
if __name__ == "__main__":
    app = TaskChampionGUI()  # Create a new TaskChampionGUI object.
    tasks = TaskWarriorInstance.load_tasks()  # Load the tasks from TaskWarrior.

    # Add both pending and completed tasks.
    for task in [*tasks['pending'], *tasks['completed']]:  # Loop through the tasks.
        app.main_widget.grids[0].add_task(Task(task))  # Add the task to the first grid.
    
    app.load_styles()  # Load the styles.
  
    sys.exit(app.on_exit())  # Exit the application.
