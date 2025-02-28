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
from utils.task_api import TaskAPIImpl, register_api
register_api(TaskAPIImpl) # Order matters.

import sys
from utils.logger import logger
from components.GUI.task_champion_gui import TaskChampionGUI  # Import the GUI class

# Program entry point
if __name__ == "__main__":
    app = TaskChampionGUI()  # Create a new TaskChampionGUI object.
    app.load_tasks()
    sys.exit(app.on_exit())  # Exit the application.
    logger.exit()
