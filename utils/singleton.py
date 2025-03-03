""" Prologue
 *  Module Name: singleton.py
 *  Purpose: Initialization of the singleton TaskWarrior API object
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

def singleton(cls):
    instances = {}  # Create a dictionary to store instances of the class.
    def getinstance(*args, **kwargs):  # Create a function that returns the instance of the class.
        if cls not in instances:  # If the class is not in the instances dictionary.
            instances[cls] = cls(*args, **kwargs)  # Create a new instance of the class.
        return instances[cls]  # Return the instance of the class.
    return getinstance  # Return the function that returns the instance of the class.