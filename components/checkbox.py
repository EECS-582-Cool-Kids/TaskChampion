from utils.task import Task
from PySide6 import QtCore, QtWidgets
# from taskw_ng import TaskWarrior
from utils import taskWarriorInstance



class Checkbox(QtWidgets.QLabel):
    # TODO: `Checkbox` forgets the taskID string and just keeps track of the taskID, while `Textbox` keeps both.
    # Is this ok? 
    
    def __init__(self, taskID : str):
        super().__init__()
        # Note: get_task(uuid) returns tuple(taskid, taskw_ng.Task), 
        # so we take second item and convert it to our modified version (utils.task.Task)
        self.task = Task(taskWarriorInstance.get_task(uuid=taskID)[1])
        self.setObjectName('TableText')
        self.checkbox = QtWidgets.QCheckBox(self)
        self.l = QtWidgets.QHBoxLayout(self)
        self.l.addWidget(self.checkbox)
        # If task has been completed in task warrior, init the checkbox checked.
        self.checkbox.setChecked(self.task.get_status() == 'completed')
        # we use a lambda fn here because a fn passed to connect can't take arguments, 
        # and python methods technically do I guess.
        self.checkbox.stateChanged.connect(lambda: self.checkCheckbox()) 
        
    @QtCore.Slot()
    def checkCheckbox(self):
        # TODO: There are more statuses than `completed` and `pending`. Do we care?
        if self.checkbox.isChecked():
            taskWarriorInstance.task_update({"uuid": self.task.get_uuid(), "status": 'completed'})

        else:
            taskWarriorInstance.task_update({"uuid": self.task.get_uuid(), "status": 'pending'})

    def linkToLayout(self, layout : QtWidgets.QVBoxLayout):
        # I don't remember if I even use this in the code
        layout.addWidget(self.checkbox)
