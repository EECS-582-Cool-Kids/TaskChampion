""" Prologue
 *  Module Name: task_api.py
 *  Purpose: Initialization of the singleton TaskWarrior API object
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Derek Norton
 *  Date: 2/15/2025
 *  Last Modified: 3/26/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from taskw_ng.warrior import TaskWarrior

# from components.GUI.grid_widget import GridWidget as Module
from utils.singleton import singleton
from utils.sortmetric import SortMetric
from utils.task import Task
from typing import Callable, Optional
import uuid
from PySide6 import QtCore
import json

class TaskAPI:
    def __init__(self):
        self.sort_metric: SortMetric = SortMetric.DESCRIPTION_ASCENDING

        # The list that is sorted according to some criteria.
        self.task_dict: dict[str, list[Task]] = {}  # List of tasks.
        # self.module_list: list[Module] = []  # List of modules.
        self.module_list: set[str] = set()
        self._init_task_list()  # Initialize the task list.
        
    def _init_task_list(self) -> None:
        k, r = self._get_sort_params(self.sort_metric)  # Get the sort parameters.
        for key in self.task_dict:
            self.task_dict[key].sort(key=k, reverse=r)  # Sort the task list.

        # We gotta do this bc otherwise deleting every task in a module will raise an error later on.
        for mod in self.module_list:
            if self.task_dict.get(mod, None) == None:
                self.task_dict[mod] = []
    
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
                return str(t[attr_name]).lower()  # Lowercase the attribute.
            
            return sub_fn

        def priority_sorting(t: Task): 
            match t.get_priority():
                case 'H':  # High priority
                    return 1
                case 'M':  # Medium priority
                    return 2
                case 'L':  # Low priority
                    return 3
                case _:  # No priority
                    return 0

        match metric:
            case SortMetric.ID_ASCENDING:
                return alpha_sorting('id'), False  # Sort by ID in ascending order.
            case SortMetric.ID_DESCENDING:
                return alpha_sorting('id'), True  # Sort by ID in descending order.
            case SortMetric.PRIORITY_ASCENDING:
                return priority_sorting, False  # Sort by priority in ascending order.
            case SortMetric.PRIORITY_DESCENDING:
                return priority_sorting, True  # Sort by priority in descending order.
            case SortMetric.DESCRIPTION_ASCENDING:
                return alpha_sorting('description'), False  # Sort by description in ascending order.
            case SortMetric.DESCRIPTION_DESCENDING:
                return alpha_sorting('description'), True  # Sort by description in descending order.

    def num_tasks(self, mod: str) -> int:
        return len(self.task_dict[mod])  # Return the number of tasks.
    
    def add_module(self, mod: str):
        if self.task_dict.get(mod, None) == None:
            self.task_dict[mod] = []
        self.module_list.add(mod)

        

    def task_at(self, idx: int, mod: str) -> Optional[Task]:
        if len(self.task_dict[mod]) <= idx:  # If the index is out of bounds.
            return None  # Return None.
        
        return self.task_dict[mod][idx]  # Return the task at the index.
    
    def add_new_task(self, description: str, tags=None,  module="Main", nonstandard_cols: dict[str, str]={}, **kw) -> Task: ...  # Add a new task.
    def add_task(self, t: Task) -> None: ...  # Add a task.
    def delete_at(self, idx: int, module: str) -> None: ...  # Delete a task at the index.
    def update_task(self, new_task: Task) -> None: ...  # Update a task.
    def set_sort_metric(self, metric: SortMetric): ...      # Set the sort metric.
    def clear_tasks(self): ...  # Clear the tasks.

@singleton
class TaskAPIImpl(TaskAPI):
    def __init__(self):  # Initialize the TaskAPIImpl class.
        self.warrior = TaskWarrior()  # Create a TaskWarrior object.
        super().__init__()  # Call the parent constructor.

    def _init_task_list(self) -> None:
        """Refreshes the task list. Private.

        Called after any operation that would require re-sorting the list of tasks."""
        self.task_dict.clear()  # Clear the task list.

        tasks = self.warrior.load_tasks()  # Load the tasks.
        task_list = [Task(x) for x in tasks['pending'] + tasks['completed']]  # Load the tasks into the task list.
        for t in task_list:
            # TODO: I'm no python expert, can somebody verify that there isn't a better way to do this?
            self.task_dict[t.get_module()] = self.task_dict.get(t.get_module(), []) + [t]

        super()._init_task_list()  # Call the parent init task list method.
    
    def add_new_task(self, description: str, tags=None, module="Main", nonstandard_cols: dict[str, str]={}, **kw) -> Task:  # Add a new task.
        """TODO: This needs to be updated to allow for module to be set here."""
        if kw.get("due"):
            due = QtCore.QDate.fromString(kw.get("due"), "yyyy-MM-dd").toString("yyyy-MM-dd")
        
        # Idk how to init a task without taskwarrior's help so we just do after.
        task = Task(self.warrior.task_add(description, tags, **kw))  # Add a task.
        
        task.set_module(module)
        for col in nonstandard_cols:
            task.set_nonstandard_col(col, nonstandard_cols[col])
        # There's no task_annotations_update method afaik, so we have to delete them
        # and then update them. Otherwise it will just add a new annotation.
        annotations = task.get_annotations()
        
        
        task = self.warrior.task_annotate(task, annotations)

        self._init_task_list()  # Initialize the task list.

        return Task(task)  # Return the task.

    def add_task(self, t: Task) -> None:
        self.warrior.task_add(t)  # Add a task.
        self._init_task_list()  # Initialize the task list.

    def delete_at(self, idx: int, module: str) -> None:
        if len(self.task_dict[module]) <= idx:  # If the index is out of bounds.
            return  # Return.

        t = self.task_dict[module].pop(idx)  # Pop the task at the index.
        self.warrior.task_delete(uuid=str(t['uuid']))  # Delete the task.

    def update_task(self, new_task: Task) -> None:
        if new_task.get_due() is not None:  # If the task has a due date.
            new_task['due'] = QtCore.QDate.fromString(new_task['due'], "yyyy-MM-dd").toString("yyyy-MM-dd")  # Set the due date.
        
        annotations=new_task.get_annotations()
        if len(annotations) > 3:
            new_task=Task(self.warrior.task_denotate(new_task, ""))
        
        self.warrior.task_update(new_task)  # Update the task.
        self.warrior.task_annotate(new_task, annotations)
        self._init_task_list()  # Initialize the task list.

    def set_sort_metric(self, metric: SortMetric):
        self.sort_metric = metric  # Set the sort metric.
        self._init_task_list()  # Initialize the task list.

    def clear_tasks(self):
        raise RuntimeError("clear_tasks should only be called in a test environment.")

@singleton
class FakeTaskAPI(TaskAPI):
    def __init__(self):
        super().__init__()  # Call the parent constructor.

        # increments every time a new task is created.
        self.cur_id = 0  # Initialize the current ID to 0.
    
    def num_tasks(self, module: str) -> int:
        return len(self.task_dict[module])  # Return the number of tasks.
        
    def task_at(self, idx: int, module: str) -> Optional[Task]:
        if len(self.task_dict[module]) <= idx:  # If the index is out of bounds.
            return None  # Return None.
        
        return self.task_dict[module][idx]  # Return the task at the index.
    
    def add_new_task(self, description: str = "", tags=None, priority="", project="", recur="", due="", module="Main", nonstandard_cols: dict[str, str]={}) -> Task:
        if due:
            due = QtCore.QDate.fromString(due, "yyyy-MM-dd").toString("yyyy-MM-dd")
        d = dict({'uuid': str(uuid.uuid1()), 'id': str(self.cur_id), 'description': description, 'tags': [tags], 'priority': priority, 'project': project, 'recur': recur, 'due': due})
        self.cur_id += 1  # Increment the current ID.
        
        task = Task(d)  # Create a task.
        task.set_module(module)
        for col in nonstandard_cols:
            task.set_nonstandard_col(col, nonstandard_cols[col])

        self.task_dict[module].append(task)  # Append the task to the task list.
        self._init_task_list()  # Initialize the task list.

        return task  # Return the task.

    def add_task(self, t: Task) -> None:
        # Unused at the moment.

        self.task_dict[t.get_module()].append(t)  # Append the task to the task list.
        self._init_task_list()  # Initialize the task list.

    def delete_at(self, idx: int, module: str) -> None:
        if len(self.task_dict[module]) <= idx:  # If the index is out of bounds.
            return  # Return.

        self.task_dict[module].pop(idx)  # Pop the task at the index.

    def update_task(self, new_task: Task) -> None:
        found = False  # Initialize found to False.
        if new_task.get_due():
            new_task['due'] = QtCore.QDate.fromString(new_task['due'], "yyyy-MM-dd").toString("yyyy-MM-dd")
        for idx in range(self.num_tasks(new_task.get_module())):  # For each task.
            if self.task_dict[new_task.get_module()][idx].get_uuid() == new_task.get_uuid():  # If the UUIDs match.
                self.task_dict[new_task.get_module()][idx] = new_task  # Update the task.
                found = True  # Set found to True.
                break
        
        if not found:
            raise ValueError(f"task {new_task} not found.")  # Raise a value error.
        
        self._init_task_list()  # Initialize the task list.

    def set_sort_metric(self, metric: SortMetric):
        self.sort_metric = metric  # Set the sort metric.
        self._init_task_list()  # Initialize the task list.

    def clear_tasks(self):
        self.task_dict.clear()  # Clear the task list.

api: TaskAPI

def register_api(cls: type[TaskAPI]):
    global api  # Declare api as global.
    api = cls()  # Set api to an instance of the class.

