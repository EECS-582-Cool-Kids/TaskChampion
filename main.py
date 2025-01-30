# This is a test example of the libraries we are using. 
# This is what I made in the lab earlier while bored.

import sys
from PySide6 import QtCore, QtWidgets
from taskw_ng import TaskWarrior

class MyCheckbox:
    def __init__(self, task : str):
        self.checkbox = QtWidgets.QCheckBox(task)
        self.task_text : str = task
        self.checkbox.stateChanged.connect(self.checkCheckbox)
    
    @QtCore.Slot()
    def checkCheckbox(self):
        if self.checkbox.isChecked():
            self.checkbox.setText("Completed: " + self.checkbox.text())
        else:
            self.checkbox.setText(self.task_text)

    def linkToLayout(self, layout : QtWidgets.QVBoxLayout):
        layout.addWidget(self.checkbox)

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.checkboxes : list[QtWidgets.QCheckBox] = []

        self.title = QtWidgets.QLabel("To-Do List", parent=self, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.title)
    
    def addTask(self, task : str) -> None:
        self.checkboxes.append(QtWidgets.QCheckBox(task, parent=self))
        self.layout.addWidget(self.checkboxes[-1])
        self.checkboxes[-1].stateChanged.connect(())
    
    @QtCore.Slot()
    def finishTask(self):
        self.title.setText("Partially Completed To-Do List")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    w = TaskWarrior()

    checkboex : list[MyCheckbox] = []

    tasks = w.load_tasks()
    for task in tasks['pending']:
        checkbox = MyCheckbox(task['description'])
        checkboex.append(checkbox)

    for box in checkboex:
        box.linkToLayout(widget.layout)

    sys.exit(app.exec())