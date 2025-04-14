""" Prologue:
 *  Module Name: task_champion_widget.py
 *  Purpose: Initialization of GUI widgets.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Mo Morgan, Richard Moser, Derek Norton
 *  Date: 2/15/2025
 *  Last Modified: 3/26/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from PySide6 import QtWidgets
from components.Dialogs.add_task_dialog import AddTaskDialog
from components.Dialogs.add_module_dialog import AddModuleDialog
from components.GUI.grid_widget import GridWidget
from components.GUI.xp_controller_widget import XpControllerWidget
from components.GUI.menubar import MenuBar
from utils.task_api import api
from typing import Callable
from styles.extra_styles import get_style


class TaskChampionWidget(QtWidgets.QWidget):
    """The main widget for the Task Champion application."""
    def __init__(self, load_styles : Callable[[], None]):
        super().__init__()  # Call the parent constructor.
        self.setObjectName('MainWidget')  # Set the object name for styling.
        
        # Initialize the layout
        self.main_layout = QtWidgets.QHBoxLayout()
        
        # Create a vertical layout. Currently, contains grid + Add Task button.
        self.task_layout = QtWidgets.QVBoxLayout()
        
        self.main_layout.addLayout(self.task_layout)  # Set the layout of the widget to be the vertical layout.
        # TODO: put another layout in the 'gamification' part of the screen, and do something with it.
        
        self.setLayout(self.main_layout)

        self.main_tab = QtWidgets.QTabWidget()  # Create a tab widget.
        self.add_button = QtWidgets.QPushButton("Add Task")  # Create a push button.
        self.add_mod_button = QtWidgets.QPushButton("Add Module")  # Create a push button for adding a new module.
        self.xp_bars = XpControllerWidget() # Create XP Controller Widget

        self.add_button.setMaximumWidth(80)  # Set the maximum width of the push button.
        self.add_button.clicked.connect(self.add_task)  # Connect the clicked signal of the push button to the addTask method.
        self.add_mod_button.setMaximumWidth(100)  # Set the maximum width of the push button for adding a new module.

        self.button_layout = QtWidgets.QHBoxLayout() # Create a horizontal layout for the buttons.


        self.button_layout.addWidget(self.add_button)  # Add the push button to the layout.
        self.button_layout.addWidget(self.add_mod_button)  # Add the push button for adding a new module to the layout.

        self.task_layout.addLayout(self.button_layout)  # Add the button layout to the task layout.
        self.task_layout.addWidget(self.main_tab)  # Add the tab widget to the layout.
        self.main_layout.addWidget(self.xp_bars) # Add the xp bar widget to the layout.

        self.grids = [GridWidget(load_styles, self.xp_bars.get_relevant_xp_bars)]  # Create a list of grid widgets. Initially only has the Main grid.
        self.grids[0].module_name = "Main"
        self.add_mod_button.clicked.connect(lambda: self.add_new_module(load_styles)) # Connect the clicked signal of the push button for adding a new module to the addNewModule method.

        self.main_tab.addTab(self.grids[0].scroll_area, "Main")  # Add the first grid widget to the tab widget.
        self.main_tab.setStyleSheet(get_style('example_tab'))  # Set the style of the tab widget.
        self.main_tab.currentChanged.connect(lambda: self.update_current_grid(self.main_tab.currentIndex()))


        # Set grid widget to take up 75% of the app's width.
        self.main_layout.setStretch(0, 3)  # Set the stretch of the first grid widget to 3.
        self.main_layout.setStretch(1, 1)  # Set the stretch of the second grid widget to 1.

        self.current_grid = 0  # Set the current grid to 0.

        self.add_task_dialog : AddTaskDialog = AddTaskDialog()  # Create an instance of the AddTaskDialog class.
        self.new_mod_dialog: AddModuleDialog = AddModuleDialog()  # Create an instance of the AddModuleDialog class.

        self.menu_bar = None    # declare the window's menu bar
        self.set_menu_bar()     # set the window's menu bar

        modules_data = self.load_modules()
        self.create_all_grids(modules_data, load_styles, self.xp_bars.get_relevant_xp_bars)


    def add_task(self) -> None:
        """Add a task to the GUI list and link it to a new task in TaskWarrior."""
        module_name = self.grids[self.current_grid].module_name # Get the annotations for the task. This will link tasks to their respective modules.
        new_task_details : AddTaskDialog.TaskDetails | None = self.add_task_dialog.add_task(module_name)  # Get the details of the new task from the add task dialog.
        
        if new_task_details is None:  # If the new task details are None.
            return  # Return.

        api.add_new_task(
            description = new_task_details.description, 
            tags        = new_task_details.tag.split(),
            priority    = new_task_details.priority,
            project     = new_task_details.project,
            recur       = new_task_details.recurrence,
            due         = new_task_details.due,
            module      = module_name
        )  # Create a new task with the details from the add task dialog.

        self.grids[self.current_grid].add_task()  # Add the new task to the current grid.
        self.xp_bars.update_bars()  # Update the XP bars.

    def set_menu_bar(self):
        """Sets the menu bar for the application."""
        self.menu_bar = MenuBar()  # Create a new menu bar.

    def add_new_module(self, load_styles : Callable[[], None]) -> None:
        """Adds a new module to the GUI."""
        new_mod_details: AddModuleDialog.ModuleDetails | None = self.new_mod_dialog.add_module()
        if new_mod_details is None:
            return # Do nothing if the module name is None.
        api.add_module(new_mod_details.grid_name)
        new_grid = GridWidget(load_styles, self.xp_bars.get_relevant_xp_bars, new_mod_details.grid_name)  # Create a new grid widget.

        self.main_tab.addTab(new_grid.scroll_area, f"{new_mod_details.grid_name}")  # Add the new grid widget to the tab widget.
        new_grid.fill_grid()
        self.grids.append(new_grid)  # Append the new grid widget to the list of grid widgets.

    def update_current_grid(self, idx) -> None:
        """Updates the current grid to the selected grid."""
        # use qt library to change self.current_grid to the index of the selected tab
        self.current_grid = idx # Set the current grid to the index of the selected tab.

    def load_modules(self):
        return self.new_mod_dialog.config

    def create_all_grids(self, modules_data, load_styles, fetch_xp_fns):
        """Creates all the grids for the modules. The grids are created based on the data in the modules_data dictionary
        which is stored in a config file. All module tabs are created and added to the main tab widget."""
        for module_name, headers in modules_data.items():
            api.add_module(module_name)
            new_grid = GridWidget(load_styles, fetch_xp_fns, module_name)
            self.main_tab.addTab(new_grid.scroll_area, f"{module_name}")
            new_grid.fill_grid()
            self.grids.append(new_grid)

        return self.grids

