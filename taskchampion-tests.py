""" Prologue:
 *  Module Name: taskchampion-tests.py
 *  Purpose: automated tests for program functionality
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Jacob Wilkus, Ethan Berkley, Mo Morgan, Richard Moser, Derek Norton
 *  Date: 2/23/2025
 *  Last Modified: 2/23/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from utils.task_api import api

class Tests:
    '''Taskwarrior API tests'''
    def test_api_add_task(self):
        '''Test Adding a basic task to the API'''

        task : dict = api.add_new_task(
            description = "Test Description", 
            tag         = "A",
            priority    = "H",
            project     = "Test Project",
        ) 

        assert task["description"] == "Test Description" # test if the description is set
        assert "A" in task["tags"] # test if the tag is set
        assert task["priority"] == "H" # test if the priority is set
        assert task["project"] == "Test Project" # test if the project is set
    
    def test_api_update_task(self):
        '''Test updating a task in the API'''

        task_idx = api.num_tasks() - 1
        assert task_idx != -1 # test that a task exists. If not, then the test method failed.

        task = api.task_at(task_idx)
        assert task != None

        task.set("description", "New Description")
        api.update_task(task)

        assert api.task_at(task_idx).get_description() == "New Description"
    
    def test_api_delete_task(self):
        '''Test deleting a task in the API'''

        task_idx = api.num_tasks() - 1
        assert task_idx != -1 # test that a task exists. If not, then the test method failed.

        api.delete_at(task_idx)
        assert api.num_tasks() == 0