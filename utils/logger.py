"""
 *  Module Name: __init__.py
 *  Purpose: Initialization of the singleton TaskWarrior Logger object
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Derek Norton
 *  Date: 2/15/2025
 *  Last Modified: 2/23/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

@singleton
class Logger:
    '''Handles all logging functionality for the application'''
    def __init__(self, is_debug : bool = False):
        # Create and open the log with the datetime the app was started.
        os.makedirs('logs/', exist_ok = True)
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

logger = Logger(is_debug=True) # remove flag when not debugging