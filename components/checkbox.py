from utils.task import Task
from PySide6 import QtCore, QtWidgets
# from taskw_ng import TaskWarrior
from utils import taskWarriorInstance



class Checkbox:
    def __init__(self, taskID : str):
        self.task = Task(taskWarriorInstance.get_task(uuid=taskID)[1])
        # self.task_text: str = str(self.task.get_description())

        self.checkbox = QtWidgets.QCheckBox()
        self.checkbox.setChecked(self.task.get_status() == 'completed')

        self.checkbox.stateChanged.connect(lambda: self.checkCheckbox()) 
        
    @QtCore.Slot()
    def checkCheckbox(self):
        if self.checkbox.isChecked():
            taskWarriorInstance.task_update({"uuid": self.task.get_uuid(), "status": 'completed'})

        else:
            taskWarriorInstance.task_update({"uuid": self.task.get_uuid(), "status": 'pending'})

    def linkToLayout(self, layout : QtWidgets.QVBoxLayout):
        layout.addWidget(self.checkbox)
