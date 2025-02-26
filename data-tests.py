"""
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

        api.clear_tasks()
        task : dict = api.add_new_task(
            description = "Test Description", 
            tags        = "A",
            priority    = "H",
            project     = "Test Project",
        ) 

        assert task["description"] == "Test Description" # test if the description is set
        assert "A" in task["tags"] # test if the tag is set
        assert task["priority"] == "H" # test if the priority is set
        assert task["project"] == "Test Project" # test if the project is set
    
    def test_fake_api_update_task(self):
        '''Test updating a task in the Fake API'''

        api.clear_tasks()
        api.add_new_task("Test Description")

        task_idx = api.num_tasks() - 1
        assert task_idx != -1 # test that a task exists. If not, then the test method failed.

        task = api.task_at(task_idx)
        assert task != None

        task.set("description", "New Description")
        api.update_task(task)
        
        t = api.task_at(task_idx)
        assert t != None
        assert t.get_description() == "New Description"
    
    def test_fake_api_delete_task(self):
        '''Test deleting a task in the Fake API'''

        api.clear_tasks()
        api.add_new_task("Test Description")

        task_idx = api.num_tasks() - 1
        assert task_idx != -1 # test that a task exists. If not, then the test method failed.

        api.delete_at(task_idx)
        assert api.num_tasks() == 0
    
    def test_logger(self):
        '''Test the logger'''

        test_debug = logger.log_debug("Test")
        assert "Test" in test_debug and "DEBUG" in test_debug

        test_error = logger.log_error("Test")
        assert "Test" in test_error and "ERROR" in test_error

        test_info = logger.log_info("Test")
        assert "Test" in test_info and "INFO" in test_info

        test_warn = logger.log_warn("Test")
        assert "Test" in test_warn and "WARN" in test_warn
    
    def test_xp(self):
        '''Test the internal XP system. TO-DO'''
        pass