from PySide6 import QtCore, QtWidgets

from utils.task_api import TaskAPI
from utils.task import Task, priority_t

class XpBar(QtWidgets.QWidget):
    """Wrapper around an XP Bar.
    
    Just the XP bar + label."""

    class XpBarAttributes:
        def __init__(self, priority, project, tags):
            self.priority : priority_t | None = priority
            self.project : str | None = project
            self.tags : list[str] | None = tags

    def __init__(self, completion_value : int, parent=None, bar_type="Main", bar_name="Main XP Bar"):
        super().__init__(parent)
        self.cur_xp = 0
        self.bar_type = bar_type
        self.completion_value = completion_value
        self.attributes : XpBar.XpBarAttributes | None = None

        self.xp_bar = XpBarChild(self, bar_type)
        self.lay = QtWidgets.QGridLayout()
        self.setLayout(self.lay)
        self.title_label = QtWidgets.QLabel(bar_name, self)

        self.progress_label = QtWidgets.QLabel(self)
        
        self.lay.setRowStretch(0, 0)
        self.lay.setRowStretch(1, 1)
        self.lay.addWidget(self.title_label, 0, 0)
        self.lay.addWidget(self.progress_label, 0, 2)
        self.lay.addWidget(self.xp_bar, 1, 0, 1, 3)
        
    def set_attributes(self, priority, project, tags):
        if self.attributes is None:
            self.attributes = XpBar.XpBarAttributes(priority, project, tags)
            return
        
        if self.attributes.priority != priority:
            self.attributes.priority = priority
        if self.attributes.project != project:
            self.attributes.project = project
        if self.attributes.tags != tags:
            self.attributes.tags = tags

    def update_text(self):        
        self.progress_label.setText(f"{self.cur_xp} XP / {self.xp_bar.max_xp} XP")

    def set_max_xp(self, val: int):
        if val == 0:
            val += 1 # prevents division by zero
        self.xp_bar.set_max_xp(val)
        self.update_text()

    def complete_task(self) -> None:
        """
        This method is responsible for marking a task as complete.

        Upon completion, it grants experience points to the user based on
        the task's completion value attribute. This operation updates the
        user's XP progress as a result of task fulfillment.

        Returns: None
        """
        self.add_xp(self.completion_value)
    
    def uncomplete_task(self) -> None:
        """
        Mark a task as uncompleted, triggering a reduction in experience points.

        This method reverses the completion of a task and subtracts a defined value 
        from the current experience points by invoking the `sub_xp()` method.

        Returns: None
        """
        self.sub_xp(self.completion_value)
        
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
        self.cur_xp = (self.cur_xp + val) % self.xp_bar.max_xp if self.xp_bar.max_xp != 0 else 1
        self.update_text()
        self.xp_bar._add_xp(val)
    
    def sub_xp(self, val : int) -> None:
        self.cur_xp = (self.cur_xp - val) % self.xp_bar.max_xp
        self.update_text()
        self.xp_bar._sub_xp(val)
    
    def reset_xp(self) -> None:
        """
        Resets the experience points (XP) of the user.

        This method resets the current XP by subtracting it from the XP bar, sets
        the XP bar's value to zero, and updates the current XP to zero. It is
        used to initialize or reset a user's progress.

        Raises:
            None
        """
        self.xp_bar._sub_xp(self.cur_xp)
        self.xp_bar.setValue(0)
        self.cur_xp = 0

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
        xp_poss : int = 0
        xp_gain : int = 0

        # calculate all tasks relevant to set the max_xp value.
        for i in range(0, TaskAPI.num_tasks(self)):
            task : Task = TaskAPI.task_at(i)

            if task is None:
                continue

            valid = False
            valid |= task.get_priority() == self.attributes.priority
            valid |= task.get_project() == self.attributes.project
            valid |= task.get_tags() == self.attributes.tags

            if valid:
                xp_poss += self.completion_value
                xp_gain += self.completion_value if task.get_status() == "completed" else 0
        
        self.set_max_xp(xp_poss)
        self.add_xp(xp_gain)
            

class XpBarChild(QtWidgets.QProgressBar):
    """Class representing an XP Bar. 

    internally, even if a 'level' is only 5 xp points,
    we still put `XpBar.MAX_VAL` steps in the bar so that it supports a smooth animation."""
    MAX_VAL=50_000 
    ANIMATION_DUR_MSECS=2_000
    EASING_CURVE=QtCore.QEasingCurve.Type.OutQuad

    def __init__(self, parent=None, bar_type="Main"):
        super().__init__(parent)
        
        self.setObjectName(f"XpBar{bar_type}")

        self.max_xp: int = 0
        self.multiplier: float = 0.0
        self.adjusted_value: float = 0.0

        self.animation = QtCore.QPropertyAnimation(self, QtCore.QByteArray(b"value"))

        self.animation.setDuration(self.ANIMATION_DUR_MSECS)
        self.animation.setEasingCurve(self.EASING_CURVE)
        
        self.setRange(0, self.MAX_VAL)

    def set_max_xp(self, val: int):
        if val == 0:
            raise ValueError("Cannot set max xp to 0.")
        self.max_xp = val
        self.multiplier = self.MAX_VAL / (1 if val == 0 else val)

    
    def _add_xp(self, val: int) -> None:
        self.animation.stop()
        adjusted = val * self.multiplier
        
        self.adjusted_value += adjusted
        
        while self.adjusted_value >= self.MAX_VAL:
            self.adjusted_value -= 0.1
        
        self.adjusted_value %= self.MAX_VAL
        self.animation.setStartValue(self.value())
        self.animation.setEndValue(int(self.adjusted_value))
        self.animation.start()

    def _sub_xp(self, val : int) -> None:
        self.animation.stop()
        adjusted = val * self.multiplier
        
        self.adjusted_value -= adjusted

        while self.adjusted_value <= 0:
            self.adjusted_value += 0.1
        
        self.adjusted_value %= self.MAX_VAL
        self.animation.setStartValue(self.value())
        self.animation.setEndValue(int(self.adjusted_value))
        self.animation.start()
        