from PySide6 import QtCore, QtWidgets



class XpBar(QtWidgets.QProgressBar):
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
        self.multiplier = self.MAX_VAL / val

    
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