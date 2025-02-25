from utils.task_api import register_api, FakeTaskAPI
register_api(FakeTaskAPI) # Order matters.

from utils.task_api import api

class Tests:
    '''Taskwarrior API tests'''
    def test_api_add_task(self):
        '''Test Adding a basic task to the API'''
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
    
    def test_api_update_task(self):
        '''Test updating a task in the API'''

        api.clear_tasks()
        api.add_new_task(description="description")

        task_idx = api.num_tasks() - 1
        assert task_idx == 0 # test that a task exists. If not, then the test method failed.

        task = api.task_at(task_idx)
        assert task != None

        task.set("description", "New Description")
        api.update_task(task)
        
        t = api.task_at(task_idx)
        assert t != None
        assert t.get_description() == "New Description"
    
    def test_api_delete_task(self):
        '''Test deleting a task in the API'''
        api.clear_tasks()
        api.add_new_task(description="description")

        task_idx = api.num_tasks() - 1
        assert task_idx != -1 # test that a task exists. If not, then the test method failed.

        api.delete_at(task_idx)
        assert api.num_tasks() == 0