""" Prologue
 *  Module Name: api-tests.py
 *  Purpose: Unit Tests for the Taskwarrior API.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Mo Morgan
 *  Date: 3/10/2025
 *  Last Modified: 2/25/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from utils.task_api import register_api, TaskAPIImpl
register_api(TaskAPIImpl) # Order matters.

from utils.task_api import api

class TestClass:
    """Taskwarrior API tests"""
    def test_api_add_task(self):
        """Test Adding a basic task to the API"""
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

    def test_api_update_task(self):
        """Test updating a task in the API"""

        task_idx = api.num_tasks("Main") - 1
        assert task_idx != -1 # test that a task exists. If not, then the test method failed.

        task = api.task_at(task_idx, "Main")  # get the task at the index
        assert task is not None  # test that the task exists. If not, then the test method failed.annotations = task.get_annotations() # get the task annotations before updating, to confirm they remain the same.

        task.set("description", "New Description")  # set the description of the task
        api.update_task(task)  # update the task in the API
        
        t = api.task_at(task_idx, "Main")  # get the task at the index
        assert t is not None  # test that the task exists. If not, then the test method failed.
        assert t.get_description() == "New Description"  # test if the description is set
        assert t.get_annotations() == task.get_annotations() # test if the two task annotations are identical
    
    def test_api_delete_task(self):
        """Test deleting a task in the API"""
        task_idx = api.num_tasks("Main") - 1  # get the index of the last task
        assert task_idx != -1 # test that a task exists. If not, then the test method failed.

        api.delete_at(task_idx, "Main")  # delete the task at the index
        assert api.num_tasks("Main") == 0  # test if the number of tasks is 0