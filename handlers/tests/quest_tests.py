from evennia.utils.test_resources import EvenniaTest

from ..quests import Quest, QuestProgress


class TestQuest(Quest):
    key = "TestQuest"
    initial_details = {
        "TestDetail": False,
        "TestDetail2": False,
    }
    initial_objectives = {
        "TestObjective": {
            "name": "Test Objective",
            "description": "Test Description",
            "hidden": False,
            "completed": False,
        },
        "TestHiddenObjective": {
            "name": "Test Hidden Objective",
            "description": "Test Hidden Description",
            "hidden": True,
            "completed": False,
        },
    }


class TestQuestHandler(EvenniaTest):
    def test_add_new_quest(self):
        self.char1.quests.add(TestQuest)
        self.assertIn("TestQuest", self.char1.quests.all())
        self.assertIsInstance(self.char1.quests.get("TestQuest"), Quest)

    def test_add_detail(self):
        self.char1.quests.add(TestQuest)
        self.char1.quests.add_detail("TestQuest", "TestDetail", True)
        added_detail = self.char1.quests.get_detail("TestQuest", "TestDetail")
        self.assertEqual(added_detail, True)

    def test_add_details(self):
        self.char1.quests.add(TestQuest)
        self.char1.quests.add_details(
            "TestQuest", {"TestDetail": True, "TestDetail2": True}
        )
        added_details = self.char1.quests.get_details("TestQuest")
        self.assertEqual(added_details, {"TestDetail": True, "TestDetail2": True})

    def test_set_objective(self):
        self.char1.quests.add(TestQuest)
        self.char1.quests.set_objective("TestQuest", "TestObjective", "completed", True)
        objective = self.char1.quests.get_objective("TestQuest", "TestObjective")
        self.assertEqual(objective["completed"], True)

    def test_update_objectives(self):
        self.char1.quests.add(TestQuest)
        self.char1.quests.update_objectives(
            "TestQuest",
            {
                "TestObjective": {"completed": True},
                "TestHiddenObjective": {"completed": True},
            },
        )
        objectives = self.char1.quests.get_objectives("TestQuest")
        self.assertEqual(objectives["TestObjective"]["completed"], True)
        self.assertEqual(objectives["TestHiddenObjective"]["completed"], True)

    def test_set_status(self):
        self.char1.quests.add(TestQuest)
        self.char1.quests.set_status("TestQuest", QuestProgress.COMPLETED)
        status = self.char1.quests.get_status("TestQuest")
        self.assertEqual(status, QuestProgress.COMPLETED)

    def test_remove_quest(self):
        self.char1.quests.add(TestQuest)
        self.assertIn("TestQuest", self.char1.quests.all())
        self.char1.quests.remove("TestQuest")
        self.assertNotIn("TestQuest", self.char1.quests.all())

    def test_clear_quests(self):
        self.char1.quests.add(TestQuest)
        self.assertIn("TestQuest", self.char1.quests.all())
        self.char1.quests.clear()
        self.assertEqual(self.char1.quests.all(), {})

    def test_quest_complete(self):
        self.char1.quests.add(TestQuest)
        self.char1.quests.update_objectives(
            "TestQuest",
            {
                "TestObjective": {"completed": True},
                "TestHiddenObjective": {"completed": True},
            },
        )
        self.char1.quests.get("TestQuest").is_complete()
        status = self.char1.quests.get_status("TestQuest")
        self.assertEqual(status, QuestProgress.COMPLETED)
