from components.GUI.xpbar import XpBar
from PySide6 import QtWidgets
from utils.task import priority_t, Task
from utils.task_api import api

HIGH_PRIORITY_MULT = 3
MED_PRIORITY_MULT = 2
LOW_PRIORITY_MULT = 1

class XpControllerWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.total_xp = 0
        self.xp_bar_map : dict[priority_t, list[XpBar]] = {}
        self.main_layout = QtWidgets.QVBoxLayout()

        self.xp_bar_map['H'] = []
        self.xp_bar_map['M'] = []
        self.xp_bar_map['L'] = []

        self.main_xp_bar = XpBar(self)
        self.main_xp_bar.set_max_xp(5)
        self.main_layout.addWidget(self.main_xp_bar)

        self.setLayout(self.main_layout)
    
    def add_xp_bar(self, priority : priority_t, max_xp : int, title : str) -> None:
        new_xp_bar = XpBar(self)
        new_xp_bar.set_max_xp(max_xp)

        match priority:
            case 'H':
                new_xp_bar.set_multiplier(HIGH_PRIORITY_MULT)
            case 'M':
                new_xp_bar.set_multiplier(MED_PRIORITY_MULT)
            case 'L':
                new_xp_bar.set_multiplier(LOW_PRIORITY_MULT)

        new_xp_bar.title_label = title
        new_xp_bar.update_text()

        self.xp_bar_map[priority].append(new_xp_bar)
        self.main_layout.addWidget(new_xp_bar)
    
    def get_relevant_xp_bars(self, task : Task) -> list[XpBar]:
        return self.xp_bar_map[task.get_priority()] + [self.main_xp_bar] # TO-DO, fetch bars based on different attributes like project!
    
    def update_bars(self) -> None:
        self.main_xp_bar.reset_xp()
        
        for priority in ['H', 'M', 'L']:
            for bar in self.xp_bar_map[priority]:
                bar.reset_xp()
        
        total_xp_possible : int = 0
        total_hi_pri_poss : int = 0
        total_md_pri_poss : int = 0
        total_lw_pri_poss : int = 0

        xp_earned : int = 0
        hi_earned : int = 0
        md_earned : int = 0
        lw_earned : int = 0

        for i in range(0, api.num_tasks()):
            task : Task = api.task_at(i)

            if task == None:
                continue

            match task.get_priority():
                case 'H':
                    total_xp_possible += 3
                    total_hi_pri_poss += 3
                    xp_earned += 3 if task.get_status() == "completed" else 0
                    hi_earned += 3 if task.get_status() == "completed" else 0
                case 'M':
                    total_xp_possible += 2
                    total_md_pri_poss += 2
                    xp_earned += 2 if task.get_status() == "completed" else 0
                    md_earned += 2 if task.get_status() == "completed" else 0
                case 'L':
                    total_xp_possible += 1
                    total_lw_pri_poss += 1
                    xp_earned += 1 if task.get_status() == "completed" else 0
                    lw_earned += 1 if task.get_status() == "completed" else 0

        self.main_xp_bar.set_max_xp(total_xp_possible)
        self.main_xp_bar.add_xp(xp_earned)

        for bar in self.xp_bar_map['H']:
            bar.set_max_xp(total_hi_pri_poss)
            bar.set_multiplier(HIGH_PRIORITY_MULT)
            bar.add_xp(hi_earned)
        for bar in self.xp_bar_map['M']:
            bar.set_max_xp(total_md_pri_poss)
            bar.set_multiplier(MED_PRIORITY_MULT)
            bar.add_xp(md_earned)
        for bar in self.xp_bar_map['L']:
            bar.set_max_xp(total_lw_pri_poss)
            bar.set_multiplier(LOW_PRIORITY_MULT)
            bar.add_xp(lw_earned)