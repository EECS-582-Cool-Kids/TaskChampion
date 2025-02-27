from PySide6 import QtCore, QtWidgets

class XpBar(QtWidgets.QWidget):
    """Wrapper around an XP Bar.
    
    Just the XP bar + label."""

    def __init__(self, parent=None, bar_type="Main", bar_name="Main XP Bar"):
        super().__init__(parent)
        self.cur_xp = 0
        self.bar_type = bar_type

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
        
    def update_text(self):        
        self.progress_label.setText(f"{self.cur_xp} XP / {self.xp_bar.max_xp} XP")

    def set_max_xp(self, val: int):
        self.xp_bar.set_max_xp(val)
        self.update_text()
    
    def set_multiplier(self, mult: int):
        self.xp_bar.multiplier *= mult
        
    def add_xp(self, val : int) -> int:
        self.cur_xp = (self.cur_xp + val) % self.xp_bar.max_xp if self.xp_bar.max_xp != 0 else 1    
        self.update_text()
        return self.xp_bar.add_xp(val)
    
    def sub_xp(self, val : int) -> int:
        self.cur_xp = (self.cur_xp - val) % self.xp_bar.max_xp
        self.update_text()
        return self.xp_bar.sub_xp(val)
    
    def reset_xp(self) -> None:
        self.cur_xp = 0
        self.lay.removeWidget(self.xp_bar)
        self.xp_bar = XpBarChild(self, self.bar_type)
        self.lay.addWidget(self.xp_bar, 1, 0, 1, 3)

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
        self.max_xp = val
        self.multiplier = self.MAX_VAL / (1 if val == 0 else val)

    
    def add_xp(self, val: int) -> int:
        """returns how many levels we just gained."""
        
        adjusted = val * self.multiplier
        self.animation.setStartValue(self.adjusted_value)

        self.adjusted_value += adjusted
        
        levels = self.adjusted_value // self.MAX_VAL
        
        self.adjusted_value %= self.MAX_VAL

        self.animation.setEndValue(self.adjusted_value)
        self.animation.start()
        
        return int(levels)

    def sub_xp(self, val : int) -> int:
        '''Returns how many levels we just lost.'''

        adjusted = val * self.multiplier
        self.animation.setStartValue(self.adjusted_value)

        self.adjusted_value -= adjusted
        
        levels = self.adjusted_value // self.MAX_VAL
        
        self.adjusted_value %= self.MAX_VAL

        self.animation.setEndValue(self.adjusted_value)
        self.animation.start()
        
        return int(levels)