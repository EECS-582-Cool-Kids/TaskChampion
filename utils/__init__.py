"""
 *  Module Name: __init__.py
 *  Purpose: Initialization of the singleton TaskWarrior object
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus
 *  Date: 2/15/2025
 *  Last Modified: 2/15/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from taskw_ng.warrior import TaskWarrior
from .task import Task
from enum import Enum
from typing import Callable, Optional

import datetime

def singleton(cls):
    instances = {}
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance

class SortMetric(Enum):
    ID_ASCENDING           = 0
    ID_DESCENDING          = 1
    PRIORITY_ASCENDING     = 2
    PRIORITY_DESCENDING    = 3
    DESCRIPTION_ASCENDING  = 4
    DESCRIPTION_DESCENDING = 5
    # TODO: Add wayy more

@singleton
class TaskAPI:
    def __init__(self):
        self.warrior = TaskWarrior()
        self.sort_metric: SortMetric = SortMetric.DESCRIPTION_ASCENDING

        # The list that is sorted according to some criteria.
        self.task_list: list[Task] = []

        self._init_task_list()

    def _init_task_list(self) -> None:
        """Refreshes the task list. Private.

        Called after any operation that would require re-sorting the list of tasks."""
        self.task_list.clear()

        tasks = self.warrior.load_tasks()
        self.task_list = [Task(x) for x in tasks['pending'] + tasks['completed']]
        
        k, r = self._get_sort_params(self.sort_metric)
        self.task_list.sort(key=k, reverse=r)
    
    @staticmethod
    def _get_sort_params(metric: SortMetric) -> tuple[Callable[[Task], str | int], bool]:
        """Meant to be called in `self._init_task_list()` by doing the following:
        
        ```
        k, r = self._get_sort_params(self.sort_metric)
        self.task_list.sort(key=k, reverse=r)
        ```
        That's it.

        """
        
        def alpha_sorting(attr_name: str):
            """Used whenever the attribute we are sorting by follows alphanumeric sorting rules.
            
            Ignores capitalization.

            Examples: description, id, project.
            Counterexamples: priority."""
            
            def subFn(t: Task):
                return str(t[attr_name]).lower()
            
            return subFn

        def priority_sorting(t: Task): 
            match t.get_priority():
                case 'H':
                    return 1
                case 'M':
                    return 2
                case 'L':
                    return 3
                case _:
                    return 0

        match metric:
            case SortMetric.ID_ASCENDING:
                return alpha_sorting('id'), False
            case SortMetric.ID_DESCENDING:
                return alpha_sorting('id'), True
            case SortMetric.PRIORITY_ASCENDING:
                return priority_sorting, False
            case SortMetric.PRIORITY_DESCENDING:
                return priority_sorting, True
            case SortMetric.DESCRIPTION_ASCENDING:
                return alpha_sorting('description'), False
            case SortMetric.DESCRIPTION_DESCENDING:
                return alpha_sorting('description'), True

    def num_tasks(self) -> int:
        return len(self.task_list)
        
    def task_at(self, idx: int) -> Optional[Task]:
        if len(self.task_list) <= idx:
            return None
        
        return self.task_list[idx]
    
    def add_new_task(self, description: str, tags=None, **kw):
        self.warrior.task_add(description, tags, **kw)
        self._init_task_list()

    def add_task(self, t: Task) -> None:
        # Unused at the moment.

        self.warrior.task_add(t)
        self._init_task_list()

    def delete_at(self, idx: int) -> None:
        if len(self.task_list) <= idx:
            return

        t = self.task_list.pop(idx)
        self.warrior.task_delete(uuid=str(t['uuid']))

    def update_task(self, newTask: Task) -> None:
        self.warrior.task_update(newTask)
        self._init_task_list()

    def set_sort_metric(self, metric: SortMetric):
        self.sort_metric = metric
        self._init_task_list()

@singleton
class Logger:
    '''Handles all logging functionality for the application'''
    def __init__(self, is_debug : bool = False):
        # Create and open the log with the datetime the app was started.
        self.log_file = open(f"logs/taskchampion-log-{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.log", "w")
        self.is_debug : bool = is_debug

    def log_info(self, info : str) -> None:
        '''Log information about the applicaton. This should be used for notifying the user of something that is not a concern.'''
        info_out : str = f"[INFO: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]: {info}"

        print(info_out)
        self.log_file.write(info_out + "\n")
    
    def log_debug(self, debug : str) -> None:
        '''Log debug information about the application. Anything we only want to print when debugging should be put here.'''
        if not self.is_debug:
            return

        debug_out : str = f"[DEBUG: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]: {debug}"

        print(debug_out)
        self.log_file.write(debug_out + "\n")

    def log_error(self, error : str) -> None:
        '''Log errors about the application. This should be called whenever we catch an error within a try-catch.'''
        error_out : str = f"[ERROR: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]: {error}"

        print(error_out)
        self.log_file.write(error_out + "\n")

    def log_warn(self, warn : str) -> None:
        '''Log warnings about the application. These should identify failures that are not critical and won't stop the functionality of the program.'''
        warn_out : str = f"[WARN: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]: {warn}"

        print(warn_out)
        self.log_file.write(warn_out + "\n")

    def exit(self) -> None:
        if not self.log_file.closed:
            self.log_file.close()

api = TaskAPI()
logger = Logger()