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
from taskw_ng import TaskWarrior
from typing import TypeAlias, Literal
from utils.task import Task, status_t, priority_t
from components import AddTaskDialog, TaskRow, COLS, ALIGN, menubar
from utils import TaskWarriorInstance

class GridWidget(QtWidgets.QWidget):
    '''The widget that corresponds to a module'''
    ROW_HEIGHT=50  # Height of each row in the grid.
    DEFAULT_ROWS=10  # Default number of rows to display.

    def __init__(self):
        super().__init__()  # Call the parent constructor.
        self.setObjectName('GridWidget')  # Set the object name for styling.
        self.setFixedHeight(200)  # Set the fixed height of the widget. 

        self.scroll_area = QtWidgets.QScrollArea()  # Create a scroll area.
        self.scroll_area.setWidgetResizable(True)  # Set the scroll area to be resizable.
        self.scroll_area.setWidget(self)  # Set the widget of the scroll area to be this widget.

        self.grid = QtWidgets.QGridLayout()  # Create a grid layout.

        self.grid.rowMinimumHeight(self.ROW_HEIGHT)  # Set the minimum height of the rows in the grid.

        # print(self.scrollArea.alignment())  
        self.setLayout(self.grid)  # Set the layout of the widget to be the grid layout.

        self.rows = 0  # Initialize the number of rows to 0.
        self.row_arr: list[TaskRow] = []  # Initialize the row array to an empty list.

        self.add_header()  # Add the header to the grid.
        self.fill_grid()  # Fill the grid with the default number of rows.

        self.menu_bar = None    # declare the window's menu bar
        self.set_menu_bar()     # set the window's menu bar

    def add_task(self, newTask: Task) -> None:
        
        self.rows += 1  # Increment the number of rows.
            
        uuid = str(newTask.get_uuid())  # Get the UUID of the new task.

        if self.grid.rowCount() == self.rows:  # If the row count of the grid is equal to the number of rows.
            self.setMinimumHeight(self.rows * self.ROW_HEIGHT)  # Set the minimum height of the widget to be the number of rows times the row height.

            self.row_arr.append(TaskRow(self.rows, uuid))  # Append a new task row to the row array.
            # Row inserts itself into the grid, insertion logic is handled in `TaskRow` obj.
            # Note that this may be tricky when changing order of tasks w.r.t column sorting, 
            # as that logic will happen in this class.
            # but idk what method we will use for sorting, for all I know qt makes it very easy.    
           
        self.row_arr[self.rows-1].update_task(uuid)  # Update the task in the row array.
        self.row_arr[self.rows-1].insert(self.grid, self.rows)  # Insert the row into the grid.

    def add_header(self):
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

    def fill_grid(self):
        for i in range(self.DEFAULT_ROWS):  # Loop through the default number of rows.
            self.row_arr.append(TaskRow(i, ""))  # Append a new task row to the row array.
            self.row_arr[i].insert(self.grid, i+1)  # Insert the row into the grid.
        self.setMinimumHeight(self.DEFAULT_ROWS * self.ROW_HEIGHT)  # Set the minimum height of the widget to be the default number of rows times the row height.

class TaskChampionWidget(QtWidgets.QWidget):
    '''The main widget for the Task Champion application.'''
    def __init__(self):
        super().__init__()  # Call the parent constructor.
        self.setObjectName('MainWidget')  # Set the object name for styling.
        
        # Initialize the layout
        # Will be used for more than just holding the grid at some point.
        self.qt_layout = QtWidgets.QVBoxLayout(self)   # Create a vertical layout.    
        self.setLayout(self.qt_layout)  # Set the layout of the widget to be the vertical layout.
        
        self.main_tab = QtWidgets.QTabWidget()  # Create a tab widget.
        self.add_button = QtWidgets.QPushButton("Add Task")  # Create a push button.

        self.add_button.setMaximumWidth(100)  # Set the maximum width of the push button.
        self.add_button.clicked.connect(lambda: self.add_task())  # Connect the clicked signal of the push button to the addTask method.
 
        self.qt_layout.addWidget(self.add_button)  # Add the push button to the layout.
        
        self.qt_layout.addWidget(self.main_tab)  # Add the tab widget to the layout.
        self.grids = [GridWidget(), GridWidget()]  # Create a list of grid widgets.
        self.main_tab.addTab(self.grids[0].scroll_area, "Example Tab")  # Add the first grid widget to the tab widget.
        self.main_tab.addTab(self.grids[1].scroll_area, "Example Empty Tab")  # Add the second grid widget to the tab widget.

        self.current_grid = 0  # Set the current grid to 0.

        self.add_task_dialog : AddTaskDialog = AddTaskDialog()  # Create an instance of the AddTaskDialog class.

        self.menu_bar = None    # declare the window's menu bar
        self.set_menu_bar()     # set the window's menu bar
    
    def add_task(self):
        '''Add a task to the GUI list and link it to a new task in TaskWarrior.'''

        newTaskDetails : AddTaskDialog.TaskDetails | None = self.add_task_dialog.add_task()  # Get the details of the new task from the add task dialog.
        
        if newTaskDetails == None:  # If the new task details are None.
            return  # Return.

        newTask : Task = Task(TaskWarriorInstance.task_add(newTaskDetails.description, newTaskDetails.tag))  # Create a new task with the details from the add task dialog.
        
        newTask.set_priority(newTaskDetails.priority)  # Set the priority of the new task.
        newTask.set_project(newTaskDetails.project)   # Set the project of the new task.

        if newTaskDetails.recurrence != None:  # If the recurrence of the new task is not None.
            newTask.set_recur(newTaskDetails.recurrence)  # Set the recurrence of the new task.
        if newTaskDetails.due != None:  # If the due date of the new task is not None.
            newTask.set_due(newTaskDetails.due)  # Set the due date of the new task.

        TaskWarriorInstance.task_update(newTask)  # Update the new task in TaskWarrior.
        self.grids[self.current_grid].add_task(newTask)  # Add the new task to the current grid.

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
        self.main_widget = TaskChampionWidget()  # Create a new TaskChampionWidget.
        self.main_widget.setWindowTitle("Task Champion")  # Set the window title.
        self.main_widget.resize(800, 400) # set basic window size.
        self.main_widget.show() # show the window
        self.style_str = ""  # Initialize the style string.
        with open ('styles/style.qss', 'r')as f:  # Open the style file.
            self.style_str = f.read()  # Read the style file.

        self.load_styles()  # Load the styles.

    def load_styles(self):
        self.qtapp.setStyleSheet(self.style_str)  # Set the style sheet of the Qt Application to be the style string.

    def on_exit(self) -> int:
        """The behavior for exiting the application."""
        return self.qtapp.exec()  # Execute the Qt Application.

# Program entry point
if __name__ == "__main__":
    app = TaskChampionGUI()  # Create a new TaskChampionGUI object.
    tasks = TaskWarriorInstance.load_tasks()  # Load the tasks from TaskWarrior.

    # Add both pending and completed tasks.
    for task in [*tasks['pending'], *tasks['completed']]:  # Loop through the tasks.
        app.main_widget.grids[0].add_task(Task(task))  # Add the task to the first grid.
    
    app.load_styles()  # Load the styles.
  
    sys.exit(app.on_exit())  # Exit the application.
