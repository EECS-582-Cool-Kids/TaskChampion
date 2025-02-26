"""
 *  Module Name: gui-tests.py
 *  Purpose: Unit Tests for the internal TaskChampion GUI objects.
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

import pytest
from components.GUI.task_champion_gui import TaskChampionGUITest
from components.GUI.task_champion_widget import TaskChampionWidget

class TestClass:
    @pytest.fixture(scope="session")
    def gui(self):
        gui = TaskChampionGUITest()
        yield gui

    def test_placeholder(self, gui : TaskChampionGUITest):
        ''''''