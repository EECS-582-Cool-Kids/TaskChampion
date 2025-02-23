"""
 *  Module Name: sort_metric.py
 *  Purpose: Initialization of the singleton TaskWarrior SortMetric object
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

class SortMetric(Enum):
    ID_ASCENDING           = 0
    ID_DESCENDING          = 1
    PRIORITY_ASCENDING     = 2
    PRIORITY_DESCENDING    = 3
    DESCRIPTION_ASCENDING  = 4
    DESCRIPTION_DESCENDING = 5
    # TODO: Add wayy more