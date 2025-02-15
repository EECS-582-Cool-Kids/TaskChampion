from PySide6 import QtWidgets, QtGui

class MenuBar(QtWidgets.QMenuBar):
    """Creates the window menu for the application."""
    def __init__(self, parent=None): # parent=None means that the parent is the main window. This might wrap the macOS's system-wide menu bar.
        super().__init__(parent)

        self.file_menu = self.addMenu("File")  # Create the File menu
        self.exit_action = QtGui.QAction("Exit", self)
        self.exit_action.triggered.connect(QtWidgets.QApplication.quit)
        self.file_menu.addAction(exit_action)

        help_menu = self.addMenu("Help")  # Create the Help menu
        about_action = QtGui.QAction("About", self)
        about_action.triggered.connect(self.show_about_dialogue)
        help_menu.addAction(about_action)


    def show_about_dialogue(self):
        """Shows the about dialogue."""
        about_dialogue = QtWidgets.QMessageBox() # Create a message box
        about_dialogue.setWindowTitle("About Task Champion") # Set the title of the dialogue box window
        about_dialogue.setText("Task Champion is a customizable task manager application designed to help you manage the things you gotta get done.")

        # Show the dialogue box. exec() is used to show the dialogue box and wait for the user
        # to close it before continuing execution. It should only be called after all of the
        # desired properties of the dialogue box have been set.
        about_dialogue.exec()
