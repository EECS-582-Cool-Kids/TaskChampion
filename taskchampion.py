"""
 *  Module Name: taskchampion.py
 *  Purpose: Entry point for the TaskChampion Application.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Jacob Wilkus, Ethan Berkley, Mo Morgan, Richard Moser
 *  Date: 2/15/2025
 *  Last Modified: 2/15/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

import sys
from PySide6 import QtCore, QtWidgets
from typing import TypeAlias, Literal, Callable
from components import AddTaskDialog, TaskRow, COLS, ALIGN, menubar, EditTaskDialog
from utils import api

refresh_styles: Callable[[], None]

class GridWidget(QtWidgets.QWidget):
    '''The widget that corresponds to a module'''
    ROW_HEIGHT=50  # Height of each row in the grid.
    DEFAULT_ROWS=10  # Default number of rows to display.

    def __init__(self):
        super().__init__()  # Call the parent constructor.
        self.setObjectName('GridWidget')  # Set the object name for styling.
        self.setFixedHeight(200)  # Set the fixed height of the widget. 

        self.scrollArea = QtWidgets.QScrollArea()  # Create a scroll area.
        self.scrollArea.setWidgetResizable(True)  # Set the scroll area to be resizable.
        self.scrollArea.setWidget(self)  # Set the widget of the scroll area to be this widget.

        self.grid = QtWidgets.QGridLayout()  # Create a grid layout.

        self.grid.rowMinimumHeight(self.ROW_HEIGHT)  # Set the minimum height of the rows in the grid.

        self.setLayout(self.grid)  # Set the layout of the widget to be the grid layout.

        self.rowArr: list[TaskRow] = []  # Initialize the row array to an empty list.

        self.addHeader()  # Add the header to the grid.

        self.menu_bar = None    # declare the window's menu bar
        self.set_menu_bar()     # set the window's menu bar

    def addTask(self) -> None:
        """Assumes that addTask has already been called in TaskChampionGUI. 
        
        Since that means TaskAPI has the updated list of tasks, 
        all we need to do is:

        1) See if we need to add a new `TaskRow`
        2) broadcast to all `TaskRow`s to update their current task.
        """
        num_tasks = api.num_tasks()  # Increment the number of rows.
            
        if self.grid.rowCount() == num_tasks:  # If the row count of the grid is equal to the number of rows.
            self.setMinimumHeight(num_tasks * self.ROW_HEIGHT)  # Set the minimum height of the widget to be the number of rows times the row height.

            self.rowArr.append(TaskRow(num_tasks, self._edit_task, self._delete_task))  # Append a new task row to the row array.
            self.rowArr[num_tasks-1].insert(self.grid, num_tasks)

            # Row inserts itself into the grid, insertion logic is handled in `TaskRow` obj.
            
        for row in range(len(self.rowArr)):
            self.rowArr[row].update_task()
        
        refresh_styles()

    def addHeader(self):
        # Make header row take up as little vertical space as it needs.
        self.grid.setRowStretch(0, 0)  # Set the row stretch of the grid to 0.
        # self.grid.setContentsMargins(0, 0, 0, 0)
        # self.grid.setHorizontalSpacing(0)
        self.grid.setSpacing(0)  # Set the spacing of the grid to 0.
        
        # QLabel is just simple text.
        self.grid.addWidget(QtWidgets.QLabel("Completed?"), 0, 0)  # Add a label to the grid.
        # TODO: may be no point in setting column stretch like this and below,
        # Consider changing.
        self.grid.setColumnStretch(0, 0)  # Set the column stretch of the grid to 0.

        for i in range(len(COLS)):  # Loop through the columns.
            self.grid.addWidget(QtWidgets.QLabel(COLS[i]), 0, i+1)  # Add a label to the grid.
            self.grid.setColumnStretch(i+1, 0)  # Set the column stretch of the grid to 0.

    def set_menu_bar(self):
        """Sets the menu bar for the application."""
        self.menu_bar = menubar.MenuBar()  # Create a new menu bar.

    def fillGrid(self):
        # Also adds tasks to the grid, which doesn't work for the "example" tab. So for now, it's empty.

        for i in range(self.DEFAULT_ROWS):  # Loop through the default number of rows.
            self.rowArr.append(TaskRow(i, self._edit_task, self._delete_task))  # Append a new task row to the row array.
            self.rowArr[i].insert(self.grid, i+1)  # Insert the row into the grid.
        self.setMinimumHeight(self.DEFAULT_ROWS * self.ROW_HEIGHT)  # Set the minimum height of the widget to be the default number of rows times the row height.

    def _edit_task(self, idx: int):
        """Passed to taskrows."""
        cur_task = api.task_at(idx)
        assert cur_task

        edit_task_dialog = EditTaskDialog(str(cur_task.get("description") or ""), 
            str(cur_task.get("due") or ""), 
            str(cur_task.get("priority") or ""))
        
        if edit_task_dialog.exec():
            cur_task.set("description", edit_task_dialog.description or None)
            cur_task.set("due", edit_task_dialog.due or None)
            cur_task.set("priority", edit_task_dialog.priority or None)
            api.update_task(cur_task)

            for i in range(api.num_tasks()):
                self.rowArr[i].update_task()

        refresh_styles()
            
    def _delete_task(self, idx: int):
        """passed to taskrows."""
        api.delete_at(idx)
        
        num_tasks = api.num_tasks()

        if num_tasks > self.DEFAULT_ROWS:
            self.rowArr.pop(-1).annihilate()
        
        for i in range(len(self.rowArr)):
            self.rowArr[i].update_task()

        refresh_styles()

class TaskChampionWidget(QtWidgets.QWidget):
    '''The main widget for the Task Champion application.'''
    def __init__(self):
        super().__init__()  # Call the parent constructor.
        self.setObjectName('MainWidget')  # Set the object name for styling.
        
        # Initialize the layout
        # Will be used for more than just holding the grid at some point.
        self.qtLayout = QtWidgets.QVBoxLayout(self)   # Create a vertical layout.    
        self.setLayout(self.qtLayout)  # Set the layout of the widget to be the vertical layout.
        
        self.mainTab = QtWidgets.QTabWidget()  # Create a tab widget.
        self.addButton = QtWidgets.QPushButton("Add Task")  # Create a push button.

        self.addButton.setMaximumWidth(100)  # Set the maximum width of the push button.
        self.addButton.clicked.connect(lambda: self.addTask())  # Connect the clicked signal of the push button to the addTask method.
 
        self.qtLayout.addWidget(self.addButton)  # Add the push button to the layout.
        
        self.qtLayout.addWidget(self.mainTab)  # Add the tab widget to the layout.
        self.grids = [GridWidget(), GridWidget()]  # Create a list of grid widgets.
        self.mainTab.addTab(self.grids[0].scrollArea, "Example Tab")  # Add the first grid widget to the tab widget.
        self.mainTab.addTab(self.grids[1].scrollArea, "Example Empty Tab")  # Add the second grid widget to the tab widget.

        self.currentGrid = 0  # Set the current grid to 0.

        self.addTaskDialog : AddTaskDialog = AddTaskDialog()  # Create an instance of the AddTaskDialog class.

        self.menu_bar = None    # declare the window's menu bar
        self.set_menu_bar()     # set the window's menu bar
    
    def addTask(self):
        '''Add a task to the GUI list and link it to a new task in TaskWarrior.'''

        newTaskDetails : AddTaskDialog.TaskDetails | None = self.addTaskDialog.addTask()  # Get the details of the new task from the add task dialog.
        
        if newTaskDetails == None:  # If the new task details are None.
            return  # Return.

        api.add_new_task(
            description = newTaskDetails.description, 
            tag         = newTaskDetails.tag,
            priority    = newTaskDetails.priority,
            project     = newTaskDetails.project,
            recur       = newTaskDetails.recurrence,
            due         = newTaskDetails.due,
        )  # Create a new task with the details from the add task dialog.
        
        self.grids[self.currentGrid].addTask()  # Add the new task to the current grid.

    def set_menu_bar(self):
        """Sets the menu bar for the application."""  
        self.menu_bar = menubar.MenuBar()  # Create a new menu bar.
        self.layout().setMenuBar(self.menu_bar)  # Set the menu bar of the layout to be the new menu bar.

class TaskChampionGUI:
    """The main application class for Task Champion."""  
    def __init__(self): 
        # Initialize the Qt App and TaskWarrior objects  
        self.qtapp = QtWidgets.QApplication([])  # Create a new Qt Application.
        
        # Initialize the main Qt Widget 
        self.mainWidget = TaskChampionWidget()  # Create a new TaskChampionWidget.
        self.mainWidget.setWindowTitle("Task Champion")  # Set the window title.
        self.mainWidget.resize(800, 400) # set basic window size.
        self.mainWidget.show() # show the window

        self.mainWidget.move(0, 0)

        self._styleStr = ""  # Initialize the style string.
        with open ('styles/style.qss', 'r')as f:  # Open the style file.
            self._styleStr = f.read()  # Read the style file.

        self.loadStyles()  # Load the styles.

    def loadTasks(self):
        self.mainWidget.grids[0].fillGrid()

    def loadStyles(self):
        self.qtapp.setStyleSheet(self._styleStr)  # Set the style sheet of the Qt Application to be the style string.

    def on_exit(self) -> int:
        """The behavior for exiting the application."""
        return self.qtapp.exec()  # Execute the Qt Application.

# Program entry point
if __name__ == "__main__":
    app = TaskChampionGUI()  # Create a new TaskChampionGUI object.
    app.loadTasks()
    # TODO: Consider doing this in a better way.
    refresh_styles = app.loadStyles
    sys.exit(app.on_exit())  # Exit the application.
