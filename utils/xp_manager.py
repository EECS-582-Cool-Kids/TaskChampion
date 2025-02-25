from singleton import singleton

@singleton
class XpManager:
    '''Singletone manager for all XP in the application.'''
    COMPLETION_XP = 1
    HIGH_PRIORITY_MULT = 3
    MED_PRIORITY_MULT = 2
    LOW_PRIORITY_MULT = 1

    def __init__(self):
        self.total_xp = 0
        self.xp_bars = []
    
    def add_progress_bar(self, bar) -> None:
        '''
        Handles adding a progress bar that can be used by the application.
        This allows for 
        '''
        pass
    

xp_manager = XpManager()