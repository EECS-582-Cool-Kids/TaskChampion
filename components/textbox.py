from utils.task import Task
from PySide6 import QtCore, QtWidgets, QtGui
# from taskw_ng import TaskWarrior
from utils import taskWarriorInstance
from typing import Final


class Textbox(QtWidgets.QLabel):
    # Generic implementation of a label that contains an attribute for a task.
    # If the task get's updated, every textbox should have it's `update` method called 
    # so that the changes are reflected in real time.

    def __init__(self, taskID : str, attribute: str):
        super().__init__()
        # These two should be treated as a constant; 
        # a textbox object should be tied to a specific task's attribtue.
        self.attribute: Final = attribute
        self.task_id: Final = taskID 
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)

        # Note that these don't *really* need to store the task object,
        # If anything this should be stored in the `TaskRow` class.
        #
        # `self.task` and `self.text` both are modified in `update()` method
        self.task: Task | None = None
        self.text: str | None = None
        
        
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        
        # self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Maximum)
        
        
        
        # self.show()
        self.setObjectName('TableText')
        self.task_update()
        # self.setAutoFillBackground(True)
        # self.setBaseSize(150, 50)
        self.update()
        
        

    def linkToLayout(self, layout : QtWidgets.QVBoxLayout):
        layout.addWidget(self)
    
    def task_update(self) -> None:
        # This method should get called whenever a task get's updated by the user. 
        # Called in `__init__`, so doesn't need to be called by programmer on task creation,
        # And no point in calling after task deletion.
        # 
        # TODO: If checking the box to mark the task as completed *does* modify 
        # one of the attributes of a task besides status, we should be calling update on all textboxes 
        # whenever the user checks the box too.

        # Note: get_task(uuid) returns tuple(taskid, taskw_ng.Task), 
        # so we take second item and convert it to our modified version (utils.task.Task)
        self.task = Task(taskWarriorInstance.get_task(uuid=self.task_id)[1])
        
        # If attribute has not been defined, Task.get(attribute) returns `None`.
        # Therefore, we convert to the empty string before stringification.
        self.text = str(self.task.get(self.attribute) or "") 
        
        self.setText(self.text)
        
