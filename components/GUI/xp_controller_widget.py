from components.GUI.xpbar import XpBar
from PySide6 import QtWidgets
from typing import Callable

class XpControllerWidget(QtWidgets.QWidget):
    '''Singletone manager for all XP in the application.'''
    COMPLETION_XP = 1
    HIGH_PRIORITY_MULT = 3
    MED_PRIORITY_MULT = 2
    LOW_PRIORITY_MULT = 1

    def __init__(self):
        super().__init__()

        self.total_xp = 0
        self.xp_bars = []
        self.main_layout = QtWidgets.QVBoxLayout()

        main_xp_bar = XpBar(self)
        main_xp_bar.set_max_xp(100)

        self.xp_bars.append(main_xp_bar)
        self.main_layout.addWidget(main_xp_bar)

        # TO-DO in configuration ticket, load in XP bar info and add those as well

        self.setLayout(self.main_layout)