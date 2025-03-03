""" Prologue
 *  Module Name: logger.py
 *  Purpose: Initialization of the singleton TaskWarrior Logger object
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
import os
import datetime
from utils.singleton import singleton

@singleton
class Logger:
    """Handles all logging functionality for the application"""
    def __init__(self, is_debug : bool = False):
        # Create and open the log with the datetime the app was started.
        os.makedirs('logs/', exist_ok = True)  # Create the logs directory if it doesn't exist.
        self.log_file = open(f"logs/taskchampion-log-{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.log", "w")  # Open the log file.
        self.is_debug : bool = is_debug  # Set the debug flag.

    def log_info(self, info : str) -> str:
        """Log information about the applicaton. This should be used for notifying the user of something that is not a concern."""
        info_out : str = f"[INFO: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: {info}"  # Create the info output.

        print(info_out)  # Print the info output.
        self.log_file.write(info_out + "\n")  # Write the info output to the log file.

        return info_out  # Return the info output.
    
    def log_debug(self, debug : str) -> str:
        """Log debug information about the application. Anything we only want to print when debugging should be put here."""
        if not self.is_debug:  # If we are not in debug mode.
            return

        debug_out : str = f"[DEBUG: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: {debug}"  # Create the debug output.

        print(debug_out)
        self.log_file.write(debug_out + "\n")  # Write the debug output to the log file.

        return debug_out  # Return the debug output.

    def log_error(self, error : str) -> str:
        """Log errors about the application. This should be called whenever we catch an error within a try-catch."""
        error_out : str = f"[ERROR: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: {error}"  # Create the error output.

        print(error_out)  # Print the error output.
        self.log_file.write(error_out + "\n")  # Write the error output to the log file.

        return error_out  # Return the error output.

    def log_warn(self, warn : str) -> str:
        """Log warnings about the application. These should identify failures that are not critical and won't stop the functionality of the program."""
        warn_out : str = f"[WARN: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: {warn}"  # Create the warn output.

        print(warn_out)  # Print the warn output.
        self.log_file.write(warn_out + "\n")  # Write the warn output to the log file.

        return warn_out  # Return the warn output.

    def exit(self) -> None:
        if not self.log_file.closed:  # If the log file is not closed.
            self.log_file.close()  # Close the log file.

logger = Logger(is_debug=True) # remove flag when not debugging