""" Prologue
 *  Module Name: xp_controller_widget.py
 *  Purpose: Defines the XP controller widget, which manages the display of XP bars
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Jacob Wilkus, Mo Morgan
 *  Date: 2/25/2025
 *  Last Modified: 2/28/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions:
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from components.GUI.xp_bar import XpBar
from PySide6 import QtWidgets
from utils.task import priority_t, Task
from utils.task_api import api
from components.Dialogs.define_xp_dialog import XPConfigDialog



class XpControllerWidget(QtWidgets.QWidget):
    PRIORITY_MULT_MAP : dict[priority_t, int] = { 'H':3, 'M':2, 'L':1, 'None': 0.5}  # Default priority multipliers
    PROJECT_MULT_MAP : dict[str, int] = {}  # Default project multipliers
    TAG_MULT_MAP : dict[str, int] = {}  # Default tag multipliers

    @staticmethod
    def get_completion_value(priority : priority_t, projects : list[str] | None, tags : list[str] | None) -> int:
        """
        Determine the completion value based on priority, project, and tags.

        This function calculates a completion value utilizing multipliers found in
        pre-defined maps. The base value is retrieved using the provided priority
        and is potentially adjusted based on the existence and matching of the
        project and tags in their respective multiplier maps.

        Parameters
        ----------
        priority : priority_t
            The priority level used to determine the base completion value.
        projects : str | None
            The associated project name, if any, used to adjust the completion
            value. If the project matches one in the project multiplier map,
            the value is adjusted accordingly.
        tags : list[str] | None
            A list of tags that, if present in the tag multiplier map, are used
            to further modify the completion value.

        Returns
        -------
        int
            The computed completion value after applying all relevant multipliers.
        """

        completion_value = XpControllerWidget.PRIORITY_MULT_MAP.get(priority, 0.5)  # fixes no priority task error

        if projects is not None:
            for project in projects:  # For each project
                if project in XpControllerWidget.PROJECT_MULT_MAP:  # If the project is in the project multiplier map
                    completion_value *= XpControllerWidget.PROJECT_MULT_MAP[project]  # Adjust the completion value

        if tags is not None:
            for tag in tags:  # For each tag
                if tag in XpControllerWidget.TAG_MULT_MAP:  # If the tag is in the tag multiplier map
                    completion_value *= XpControllerWidget.TAG_MULT_MAP[tag]  # Adjust the completion value

        return completion_value  # Return the completion value

    def __init__(self):
        super().__init__()

        self.total_xp = 0  # The total XP value
        self.xp_bars : list[XpBar] = []  # A list of XP bars
        self.main_layout = QtWidgets.QVBoxLayout()  # Create a vertical layout

        self.config_button = QtWidgets.QPushButton('Config')  # Create a push button
        self.config_button.pressed.connect(self.popup_xp_config)  # Connect the pressed signal of the push button to the popupXPConfig method
        self.main_layout.addWidget(self.config_button)  # Add the push button to the layout

        self.main_xp_bar = XpBar(self)  # Create the main XP bar
        self.main_xp_bar.set_max_xp(5)  # Set the maximum XP value
        self.main_layout.addWidget(self.main_xp_bar)  # Add the main XP bar to the layout
        self.xp_bars.append(self.main_xp_bar)  # Add the main XP bar to the list of XP bars

        self.setLayout(self.main_layout)  # Set the layout of the widget to be the main layout

        self.xp_config_dialog = XPConfigDialog()  # Create an instance of the XPConfigDialog class
        self.xp_config_dialog.xp_values_updated.connect(self.update_priority_mult_map)  # Connect the xpValuesUpdated signal of the XPConfigDialog to the updatePriorityMultMap method
        self.update_priority_mult_map(self.xp_config_dialog.config)  # Update the priority multiplier map with the values from the XP configuration dialog
        
    def add_xp_bar(self, task : Task, max_xp : int, title : str) -> None:
        """
        Adds a new XP bar for a specific task to the user interface. The XP bar visually
        represents the progress of a task based on its completion value, maximum XP,
        and associated attributes like priority, project, and tags.

        Parameters:
        task : Task
            The task object containing details like priority, project, and tags
            used to determine the XP bar's attributes.
        max_xp : int
            The maximum XP value that the XP bar can display.
        title : str
            The title of the XP bar, which is displayed as a label.

        Returns:
        None
        """
        completion_value : int = self.get_completion_value(task.get_priority(), task.get_project(), task.get_tags())  # Get the completion value

        new_xp_bar = XpBar(completion_value)  # Create a new XP bar
        new_xp_bar.set_max_xp(max_xp)  # Set the maximum XP value
        new_xp_bar.set_attributes(task.get_priority(), task.get_project(), task.get_tags())  # Set the attributes

        new_xp_bar.title_label = title  # Set the title label
        new_xp_bar.update_text()  # Update the text

        self.xp_bars.append(new_xp_bar)  # Add the XP bar to the list of XP bars
        self.main_layout.addWidget(new_xp_bar)  # Add the XP bar to the layout
    
    def get_relevant_xp_bars(self, task : Task) -> list[XpBar]:
        """
        Retrieves experience bars relevant to the provided task based on task attributes,
        matching priority, project, or tags. The function also includes the main experience
        bar in the returned list.

        Parameters:

        task : Task
            The task object containing attributes that determine relevance to
            experience bars.

        Returns:
        list[XpBar]
            A list of experience bars relevant to the task. This includes any matching bars
            based on priority, project, or tags, as well as the main experience bar.
        """
        bars_to_return = []  # Initialize the list of bars to return

        for bar in self.xp_bars:  # For each XP bar
            if bar.attributes is None:  # If the attributes are None
                continue  # Continue
            
            if bar.attributes.priority == task.get_priority():
                bars_to_return.append(bar)  # Append the bar to the list of bars to return
            elif bar.attributes.project == task.get_project().deserialize():
                bars_to_return.append(bar)  # Append the bar to the list of bars to return
            elif bar.attributes.tags == task.get_tags().deserialize():
                bars_to_return.append(bar)  # Append the bar to the list of bars to return
        
        return bars_to_return + [self.main_xp_bar]  # Return the list of bars to return plus the main XP bar
        
    def update_bars(self) -> None:
        for bar in self.xp_bars:  # For each XP bar
            bar.reset_xp()  # Reset the XP value

            # update the xp of all bars but the main xp bar
            if bar != self.main_xp_bar:  # If the bar is not the main XP bar
                bar.update_xp()  # Update the XP value

        xp_poss : int = 0  # Initialize the possible XP value
        xp_gain : int = 0  # Initialize the gained XP value

        
        for module in api.task_dict:
            for i in range(0, api.num_tasks(module)):  # For each task
                task : Task | None = api.task_at(i, module)  # Get the task at the index

                if task is None:
                    continue  # Continue
                
                completion_value : int = self.get_completion_value(task.get_priority(), task.get_project(), task.get_tags())  # Get the completion value
                xp_poss += completion_value  # Add the completion value to the possible XP value
                xp_gain += completion_value if task.get_status() == "completed" else 0  # Add the completion value to the gained XP value if the task is completed
            
        self.main_xp_bar.set_max_xp(xp_poss)  # Set the maximum XP value of the main XP bar
        self.main_xp_bar.add_xp(xp_gain)  # Add the gained XP value to the main XP bar

    def popup_xp_config(self):
        self.xp_config_dialog.exec()  # Execute the XP configuration dialog
        
    def update_priority_mult_map(self, updated_values: dict):
        """
        Updates the priority multiplier map with the provided values from the XP configuration dialog.

        Parameters:
        updated_values : dict
            A dictionary containing updated priority multiplier values.
        """
        
        XpControllerWidget.PRIORITY_MULT_MAP = updated_values['priorities']  # Update the priority multiplier map
        XpControllerWidget.TAG_MULT_MAP = updated_values['tags']  # Update the tag multiplier map
        XpControllerWidget.PROJECT_MULT_MAP_MULT_MAP = updated_values['projects']  # Update the project multiplier map
        
        self.update_bars()    # update the XP bars to reflect the new values. This functionality may not be wanted.
                                # Discuss in PR