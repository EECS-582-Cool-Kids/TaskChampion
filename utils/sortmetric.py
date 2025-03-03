""" Prologue
 *  Module Name: sortmetric.py
 *  Purpose: Initialization of the SortMetric TaskWarrior API enum
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
from enum import Enum

class SortMetric(Enum):
    ID_ASCENDING           = 0  # Create an enum for the sort metric.
    ID_DESCENDING          = 1  # Create an enum for the sort metric.
    PRIORITY_ASCENDING     = 2  # Create an enum for the sort metric.
    PRIORITY_DESCENDING    = 3  # Create an enum for the sort metric.
    DESCRIPTION_ASCENDING  = 4  # Create an enum for the sort metric
    DESCRIPTION_DESCENDING = 5  # Create an enum for the sort metric
    # TODO: Add wayy more