""" Prologue
 *  Module Name: data-tests.py
 *  Purpose: Unit Tests for the internal TaskChampion Data objects.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Jacob Wilkus
 *  Date: 2/25/2025
 *  Last Modified: 2/25/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from utils.task_api import register_api, FakeTaskAPI
register_api(FakeTaskAPI) # Order matters.

from utils.task_api import api
from utils.logger import logger

class TestClass:
    def test_fake_api_add_task(self):
        '''Fake API task addition Test'''

        api.clear_tasks()  # Clear the tasks in the API
        task : dict = api.add_new_task(
            description = "Test Description", 
            tags        = "A",
            priority    = "H",
            project     = "Test Project",
        )   # Add a new task to the API

        assert task["description"] == "Test Description" # test if the description is set
        assert "A" in task["tags"] # test if the tag is set
        assert task["priority"] == "H" # test if the priority is set
        assert task["project"] == "Test Project" # test if the project is set
    
    def test_fake_api_update_task(self):
        '''Test updating a task in the Fake API'''

        api.clear_tasks()  # Clear the tasks in the API
        api.add_new_task("Test Description")  # Add a new task to the API

        task_idx = api.num_tasks("Main") - 1  # get the index of the last task
        assert task_idx != -1 # test that a task exists. If not, then the test method failed.

        task = api.task_at(task_idx, "Main")  # get the task at the index
        assert task != None  # test that the task exists. If not, then the test method failed.

        task.set("description", "New Description")  # set the description of the task
        api.update_task(task)  # update the task in the API
        
        t = api.task_at(task_idx, "Main")  # get the task at the index
        assert t != None  # test that the task exists. If not, then the test method failed.
        assert t.get_description() == "New Description"  # test if the description is set
    
    def test_fake_api_delete_task(self):
        '''Test deleting a task in the Fake API'''

        api.clear_tasks()  # Clear the tasks in the API
        api.add_new_task("Test Description")  # Add a new task to the API

        task_idx = api.num_tasks("Main") - 1  # get the index of the last task
        assert task_idx != -1 # test that a task exists. If not, then the test method failed.

        api.delete_at(task_idx, "Main")  # delete the task at the index
        assert api.num_tasks("Main") == 0  # test if the number of tasks is 0
    
    def test_logger(self):
        '''Test the logger'''

        test_debug = logger.log_debug("Test")  # log a debug message
        assert "Test" in test_debug and "DEBUG" in test_debug  # test if the message is in the log

        test_error = logger.log_error("Test")  # log an error message
        assert "Test" in test_error and "ERROR" in test_error  # test if the message is in the log

        test_info = logger.log_info("Test")  # log an info message
        assert "Test" in test_info and "INFO" in test_info  # test if the message is in the log

        test_warn = logger.log_warn("Test")  # log a warning message
        assert "Test" in test_warn and "WARN" in test_warn  # test if the message is in the log
    
    def test_xp(self):
        '''Test the internal XP system. TO-DO'''
        pass  # Placeholder for future tests