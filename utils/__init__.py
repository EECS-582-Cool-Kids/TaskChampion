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

import os
import datetime
from taskw_ng.warrior import TaskWarrior
from .task import Task
from enum import Enum
from typing import Callable, Optional

def singleton(cls):
    instances = {}
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance

api = TaskAPI()
logger = Logger(is_debug=True) # remove flag when not debugging