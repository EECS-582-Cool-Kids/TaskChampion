"""
 *  Module Name: __init__.py
 *  Purpose: Initialization of most internal objects related to the GUI.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Mo Morgan, Richard Moser
 *  Date: 2/15/2025
 *  Last Modified: 2/15/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""
from .add_task_dialog import AddTaskDialog
from .edit_task_dialog import EditTaskDialog
from .task_row import TaskRow
from utils.task import Task
from PySide6 import QtCore, QtWidgets
from utils import TaskWarriorInstance
from .checkbox import Checkbox
from .textbox import Textbox
from .buttonbox import Buttonbox
from typing import Final

# The names of the columns.
# TODO: in the image Richard posted, the second col was Age instead of 'start', but taskw_ng doesn't have an age.
# Should we keep it as start? do something else? Idk what start even means.
COLS: Final = ('id', 'start', 'priority', 'project', 'recur', 'due', 'until', 'description', 'urgency')

class ALIGN:
    # Declare where at in a layout an item aligns itself to.
    TL = QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft
    TC = QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter
    CC = QtCore.Qt.AlignmentFlag.AlignCenter
    CL = QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft
