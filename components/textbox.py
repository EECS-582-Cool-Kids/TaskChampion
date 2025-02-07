from utils.task import Task
from PySide6 import QtCore, QtWidgets
# from taskw_ng import TaskWarrior
from utils import taskWarriorInstance



class Textbox:
    def __init__(self, taskID : str, attribute: str):
        self.attribute = attribute
        self.task_id = taskID 

        self.task: Task | None = None
        self.text: str | None = None

        self.textbox = QtWidgets.QLabel("")
        
        self.update()


        # self.textbox.textChanged.connect(lambda: self.set_attr())

    # @QtCore.Slot()
    # def set_attr(self):
    #     self.text = self.textbox.toPlainText()
    #     print(self.text)
    #     self.task = w.task_update({'uuid': self.task_id, self.attribute: self.text})[1]

    def linkToLayout(self, layout : QtWidgets.QVBoxLayout):
        layout.addWidget(self.textbox)
    
    def update(self) -> None:
        self.task = Task(taskWarriorInstance.get_task(uuid=self.task_id)[1])
        self.text = str(self.task.get(self.attribute) or "") 
        self.textbox.setText(self.text)
        
