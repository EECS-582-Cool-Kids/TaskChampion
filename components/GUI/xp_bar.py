""" Prologue
* Module Name: xp_bar.py
* Purpose: Module for the XpBar class, which is a class for creating an XP bar in the GUI.
* Inputs: None
* Outputs: None
* Additional code sources: None
* Developers: Jacob Wilkus, Mo Morgan
* Date: 2/25/2025
* Last Modified: 2/28/2025
* Preconditions: None
* Postconditions: None
* Error/Exception conditions:
* Side effects: None
* Invariants: None
* Known Faults: None encountered
"""

from PySide6 import QtCore, QtWidgets

from utils.task_api import api
from utils.task import Task, priority_t

class XpBar(QtWidgets.QWidget):
    """Wrapper around an XP Bar.
    
    Just the XP bar + label."""

    class XpBarAttributes:
        def __init__(self, priority, project, tags):
            self.priority : priority_t | None = priority  # type: ignore
            self.project : str | None = project  # type: ignore
            self.tags : list[str] | None = tags  # type: ignore

    def __init__(self, completion_value : int, parent=None, bar_type="Main", bar_name="Main XP Bar"):
        super().__init__(parent)  # Call the parent constructor.
        self.cur_xp = 0  # Set the current XP to 0.
        self.bar_type = bar_type  # Set the bar type.
        self.completion_value = completion_value  # Set the completion value.
        self.attributes : XpBar.XpBarAttributes | None = None  # Set the attributes to None.

        self.xp_bar = XpBarChild(self, bar_type)  # Create an instance of the XpBarChild class.
        self.lay = QtWidgets.QGridLayout()  # Create a grid layout.
        self.setLayout(self.lay)  # Set the layout of the widget to be the grid layout.
        self.title_label = QtWidgets.QLabel(bar_name, self)  # Create a label.

        self.progress_label = QtWidgets.QLabel(self)  # Create a label.
        
        self.lay.setRowStretch(0, 0)  # Set the row stretch of the grid layout to 0.
        self.lay.setRowStretch(1, 1)  # Set the row stretch of the grid layout to 1.
        self.lay.addWidget(self.title_label, 0, 0)  # Add the title label to the grid layout.
        self.lay.addWidget(self.progress_label, 0, 2)  # Add the progress label to the grid layout.
        self.lay.addWidget(self.xp_bar, 1, 0, 1, 3)  # Add the XP bar to the grid layout.
        
    def set_attributes(self, priority, project, tags):
        if self.attributes is None:  # If the attributes are None.
            self.attributes = XpBar.XpBarAttributes(priority, project, tags)  # Create an instance of the XpBarAttributes class.
            return  # Return.
        
        if self.attributes.priority != priority:  # If the priority of the attributes is not equal to the priority.
            self.attributes.priority = priority  # Set the priority of the attributes to the priority.
        if self.attributes.project != project:  # If the project of the attributes is not equal to the project.
            self.attributes.project = project  # Set the project of the attributes to the project.
        if self.attributes.tags != tags:  # If the tags of the attributes are not equal to the tags.
            self.attributes.tags = tags  # Set the tags of the attributes to the tags.

    def update_text(self):        
        self.progress_label.setText(f"{self.cur_xp} XP / {self.xp_bar.max_xp} XP")  # Set the text of the progress label to the current XP and the maximum XP.

    def set_max_xp(self, val: int):
        if val == 0:  # If the value is 0.
            val += 1 # prevents division by zero
        self.xp_bar.set_max_xp(val)  # Set the maximum XP of the XP bar to the value.
        self.update_text()  # Update the text.

    def complete_task(self) -> None:
        """
        This method is responsible for marking a task as complete.

        Upon completion, it grants experience points to the user based on
        the task's completion value attribute. This operation updates the
        user's XP progress as a result of task fulfillment.

        Returns: None
        """
        self.add_xp(self.completion_value)  # Add the completion value to the XP.

    def uncomplete_task(self) -> None:
        """
        Mark a task as uncompleted, triggering a reduction in experience points.

        This method reverses the completion of a task and subtracts a defined value 
        from the current experience points by invoking the `sub_xp()` method.

        Returns: None
        """
        self.sub_xp(self.completion_value)  # Subtract the completion value from the XP.
        
    def add_xp(self, val : int) -> None:
        """
        Increments the current experience (XP) value with the provided input and updates
        the associated XP bar and text display. If the maximum XP in the XP bar is non-zero,
        the method calculates the new XP by wrapping its value around the maximum XP.
        Otherwise, a default value of 1 is set for the XP.

        Args:
            val (int): The amount of experience to be added.

        Returns:
            None
        """
        self.cur_xp = (self.cur_xp + val) % self.xp_bar.max_xp if self.xp_bar.max_xp != 0 else 1  # Calculate the current XP.
        self.update_text()  # Update the text.
        self.xp_bar._add_xp(val)  # Add the XP to the XP bar.
    
    def sub_xp(self, val : int) -> None:
        self.cur_xp = (self.cur_xp - val) % self.xp_bar.max_xp  # Calculate the current XP.
        self.update_text()  # Update the text.
        self.xp_bar._sub_xp(val)  # Subtract the XP from the XP bar.
    
    def reset_xp(self) -> None:
        """
        Resets the experience points (XP) of the user.

        This method resets the current XP by subtracting it from the XP bar, sets
        the XP bar's value to zero, and updates the current XP to zero. It is
        used to initialize or reset a user's progress.

        Raises:
            None
        """
        self.xp_bar._sub_xp(self.cur_xp)  # Subtract the current XP from the XP bar.
        self.xp_bar.setValue(0)  # Set the value of the XP bar to 0.
        self.cur_xp = 0  # Set the current XP to 0.

    def update_xp(self) -> None:
        """
        Updates the experience points (XP) for the current object based on the
        tasks from the TaskAPI. This includes calculating the maximum possible
        XP from relevant tasks and the amount of XP gained from completed tasks.
        Relevance of tasks is determined by comparing their attributes such as
        priority, project, and tags with the current object's attributes.

        Attributes
        ----------
        xp_poss : int
            Represents the total potential XP that can be gained from all relevant
            tasks.
        xp_gain : int
            Represents the actual XP gained from tasks that are completed.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        xp_poss : int = 0  # Set the potential XP to 0.
        xp_gain : int = 0  # Set the XP gain to 0.

        # calculate all tasks relevant to set the max_xp value.
        for i in range(0, api.num_tasks()):  # Loop through the tasks.
            task : Task = api.task_at(i)  # Get the task at the index.

            if task is None:  # If the task is None.
                continue  # Continue.

            valid = False  # Set the valid flag to False.
            valid |= task.get_priority() == self.attributes.priority  # Check if the priority of the task is equal to the priority.
            valid |= task.get_project() == self.attributes.project  # Check if the project of the task is equal to the project.
            valid |= task.get_tags() == self.attributes.tags  # Check if the tags of the task are equal to the tags.

            if valid:  # If the task is valid.
                xp_poss += self.completion_value  # Add the completion value to the potential XP.
                xp_gain += self.completion_value if task.get_status() == "completed" else 0  # Add the completion value to the XP gain if the task is completed.
        
        self.set_max_xp(xp_poss)  # Set the maximum XP to the potential XP.
        self.add_xp(xp_gain)  # Add the XP gain to the XP.

class XpBarChild(QtWidgets.QProgressBar):
    """Class representing an XP Bar. 

    internally, even if a 'level' is only 5 xp points,
    we still put `XpBar.MAX_VAL` steps in the bar so that it supports a smooth animation."""
    MAX_VAL=50_000   # 50,000
    ANIMATION_DUR_MSECS=2_000  # 2 seconds
    EASING_CURVE=QtCore.QEasingCurve.Type.OutQuad  # OutQuad

    def __init__(self, parent=None, bar_type="Main"):
        super().__init__(parent)  # Call the parent constructor.

        self.setObjectName(f"XpBar{bar_type}")   # Set the object name.

        self.max_xp: int = 0  # Set the maximum XP to 0.
        self.multiplier: float = 0.0  # Set the multiplier to 0.0.
        self.adjusted_value: float = 0.0  # Set the adjusted value to 0.0.

        self.animation = QtCore.QPropertyAnimation(self, QtCore.QByteArray(b"value"))  # Create a property animation.

        self.animation.setDuration(self.ANIMATION_DUR_MSECS)  # Set the duration of the animation.
        self.animation.setEasingCurve(self.EASING_CURVE)  # Set the easing curve of the animation.
        
        self.setRange(0, self.MAX_VAL)  # Set the range of the XP bar.

    def set_max_xp(self, val: int):
        if val == 0:  # If the value is 0.
            raise ValueError("Cannot set max xp to 0.")  # Raise a value
        self.max_xp = val  # Set the maximum XP to the value.
        self.multiplier = self.MAX_VAL / (1 if val == 0 else val)  # Set the multiplier.

    
    def _add_xp(self, val: int) -> None:
        self.animation.stop()  # Stop the animation.
        adjusted = val * self.multiplier  # Calculate the adjusted value.
        
        self.adjusted_value += adjusted  # Add the adjusted value.
        
        while self.adjusted_value >= self.MAX_VAL:  # While the adjusted value is greater than or equal to the maximum value.
            self.adjusted_value -= 0.1  # Subtract 0.1 from the adjusted value.
        
        self.adjusted_value %= self.MAX_VAL  # Set the adjusted value to the adjusted value modulo the maximum value.
        self.animation.setStartValue(self.value())  # Set the start value of the animation to the current value.
        self.animation.setEndValue(int(self.adjusted_value))  # Set the end value of the animation to the adjusted value.
        self.animation.start()  # Start the animation.

    def _sub_xp(self, val : int) -> None:
        self.animation.stop()  # Stop the animation.
        adjusted = val * self.multiplier  # Calculate the adjusted value.
        
        self.adjusted_value -= adjusted  # Subtract the adjusted value.

        while self.adjusted_value <= 0:
            self.adjusted_value += 0.1  # Add 0.1 to the adjusted value.
        
        self.adjusted_value %= self.MAX_VAL  # Set the adjusted value to the adjusted value modulo the maximum value.
        self.animation.setStartValue(self.value())  # Set the start value of the animation to the current value.
        self.animation.setEndValue(int(self.adjusted_value))  # Set the end value of the animation to the adjusted value.
        self.animation.start()  # Start the animation.
        