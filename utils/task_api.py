"""
 *  Module Name: task_api.py
 *  Purpose: Initialization of the singleton TaskWarrior API object
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Derek Norton
 *  Date: 2/15/2025
 *  Last Modified: 2/25/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from taskw_ng.warrior import TaskWarrior
from utils.singleton import singleton
from utils.sortmetric import SortMetric
from utils.task import Task
from typing import Callable, Optional
import uuid

class TaskAPI:
    def __init__(self):
        self.sort_metric: SortMetric = SortMetric.DESCRIPTION_ASCENDING

        # The list that is sorted according to some criteria.
        self.task_list: list[Task] = []

        self._init_task_list()
    def _init_task_list(self) -> None:
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
            
            def sub_fn(t: Task):
                return str(t[attr_name]).lower()
            
            return sub_fn

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
    
    def add_new_task(self, description: str, tags=None, **kw) -> dict: ...
    def add_task(self, t: Task) -> None: ...
    def delete_at(self, idx: int) -> None: ...
    def update_task(self, new_task: Task) -> None: ...
    def set_sort_metric(self, metric: SortMetric): ...    
    def clear_tasks(self): ...

@singleton
class TaskAPIImpl(TaskAPI):
    def __init__(self):
        self.warrior = TaskWarrior()
        super().__init__()

    def _init_task_list(self) -> None:
        """Refreshes the task list. Private.

        Called after any operation that would require re-sorting the list of tasks."""
        self.task_list.clear()

        tasks = self.warrior.load_tasks()
        self.task_list = [Task(x) for x in tasks['pending'] + tasks['completed']]
        
        super()._init_task_list()
    
    def add_new_task(self, description: str, tags=None, **kw) -> dict:
        task : dict = self.warrior.task_add(description, tags, **kw)
        self._init_task_list()

        return task

    def add_task(self, t: Task) -> None:
        # Unused at the moment.

        self.warrior.task_add(t)
        self._init_task_list()

    def delete_at(self, idx: int) -> None:
        if len(self.task_list) <= idx:
            return

        t = self.task_list.pop(idx)
        self.warrior.task_delete(uuid=str(t['uuid']))

    def update_task(self, new_task: Task) -> None:
        self.warrior.task_update(new_task)
        self._init_task_list()

    def set_sort_metric(self, metric: SortMetric):
        self.sort_metric = metric
        self._init_task_list()

    def clear_tasks(self):
        raise RuntimeError("clear_tasks should only be called in a test environment.")

@singleton
class FakeTaskAPI(TaskAPI):
    def __init__(self):
        super().__init__()

        # increments every time a new task is created.
        self.cur_id = 0
    
    def num_tasks(self) -> int:
        return len(self.task_list)
        
    def task_at(self, idx: int) -> Optional[Task]:
        if len(self.task_list) <= idx:
            return None
        
        return self.task_list[idx]
    
    def add_new_task(self, description: str = "", tags=None, priority="", project="", recur="", due="") -> dict:
        d = dict({'uuid': str(uuid.uuid1()), 'id': str(self.cur_id), 'description': description, 'tags': [tags], 'priority': priority, 'project': project, 'recur': recur, 'due': due})
        self.cur_id += 1
        
        task = Task(d)

        self.task_list.append(task)
        self._init_task_list()

        return task

    def add_task(self, t: Task) -> None:
        # Unused at the moment.

        self.task_list.append(t)
        self._init_task_list()

    def delete_at(self, idx: int) -> None:
        if len(self.task_list) <= idx:
            return

        self.task_list.pop(idx)

    def update_task(self, new_task: Task) -> None:
        found = False
        for idx in range(self.num_tasks()):
            if self.task_list[idx].get_uuid() == new_task.get_uuid():
                self.task_list[idx] = new_task
                found = True
                break
        
        if not found:
            raise ValueError(f"task {new_task} not found.")
        
        self._init_task_list()

    def set_sort_metric(self, metric: SortMetric):
        self.sort_metric = metric
        self._init_task_list()

    def clear_tasks(self):
        self.task_list.clear()

api: TaskAPI

def register_api(cls: type[TaskAPI]):
    global api
    api = cls()

