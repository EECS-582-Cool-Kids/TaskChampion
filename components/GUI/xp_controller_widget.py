from components.GUI.xp_bar import XpBar
from PySide6 import QtWidgets
from utils.task import priority_t, Task
from utils.task_api import api

PRIORITY_MULT_MAP : dict[priority_t, int] = { 'H':3, 'M':2, 'L':1 }
PROJECT_MULT_MAP : dict[str, int] = {}
TAG_MULT_MAP : dict[str, int] = {}

def get_completion_value(priority : priority_t, project : str | None, tags : list[str] | None) -> int:
    completion_value : int = PRIORITY_MULT_MAP[priority]

    if project in PROJECT_MULT_MAP:
        completion_value *= PROJECT_MULT_MAP[project]

    if tags is not None:
        for tag in tags:
            if tag in TAG_MULT_MAP:
                completion_value *= TAG_MULT_MAP[tag]
    
    return completion_value

class XpControllerWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.total_xp = 0
        self.xp_bars : list[XpBar] = []
        self.main_layout = QtWidgets.QVBoxLayout()

        self.main_xp_bar = XpBar(self)
        self.main_xp_bar.set_max_xp(5)
        self.main_layout.addWidget(self.main_xp_bar)
        self.xp_bars.append(self.main_xp_bar)

        self.setLayout(self.main_layout)
    
    def add_xp_bar(self, task : Task, max_xp : int, title : str) -> None:
        completion_value : int = get_completion_value(task.get_priority(), task.get_project(), task.get_tags())

        new_xp_bar = XpBar(self, completion_value)
        new_xp_bar.set_max_xp(max_xp)
        new_xp_bar.set_attributes(task.get_priority(), task.get_project(), task.get_tags())

        new_xp_bar.title_label = title
        new_xp_bar.update_text()

        self.xp_bars.append(new_xp_bar)
        self.main_layout.addWidget(new_xp_bar)
    
    def get_relevant_xp_bars(self, task : Task) -> list[XpBar]:
        bars_to_return = []

        for bar in self.xp_bars:
            if bar.attributes is None:
                continue
            
            if bar.attributes.priority == task.get_priority():
                bars_to_return.append(bar)
            elif bar.attributes.project == task.get_project().deserialize():
                bars_to_return.append(bar)
            elif bar.attributes.tags == task.get_tags().deserialize():
                bars_to_return.append(bar)
        
        return bars_to_return + [self.main_xp_bar]
        
    def update_bars(self) -> None:
        for bar in self.xp_bars:
            bar.reset_xp()

            # update the xp of all bars but the main xp bar
            if bar != self.main_xp_bar:
                bar.update_xp()

        xp_poss : int = 0
        xp_gain : int = 0

        for i in range(0, api.num_tasks()):
            task : Task = api.task_at(i)

            if task is None:
                continue
            
            completion_value : int = get_completion_value(task.get_priority(), task.get_project(), task.get_tags())

            xp_poss += completion_value
            xp_gain += completion_value if task.get_status() == "completed" else 0
        
        self.main_xp_bar.set_max_xp(xp_poss)
        self.main_xp_bar.add_xp(xp_gain)