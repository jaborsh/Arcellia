from enum import Enum

from evennia.utils.test_resources import EvenniaTest

from ..quests import Quest, QuestProgress


class TestDetail(Enum):
    TEST_DETAIL = "test detail"
    TEST_DETAIL2 = "test detail 2"


class TestObjective(Enum):
    TEST_OBJECTIVE = "test objective"
    TEST_HIDDEN_OBJECTIVE = "test hidden objective"


class TestQuest(Quest):
    key = "TestQuest"
    initial_details = {
        TestDetail.TEST_DETAIL: False,
        TestDetail.TEST_DETAIL2: False,
    }
    initial_objectives = {
        TestObjective.TEST_OBJECTIVE: {
            "name": "Test Objective",
            "description": "Test Description",
            "hidden": False,
            "status": QuestProgress.UNSTARTED,
        },
        TestObjective.TEST_HIDDEN_OBJECTIVE: {
            "name": "Test Hidden Objective",
            "description": "Test Hidden Description",
            "hidden": True,
            "status": QuestProgress.UNSTARTED,
        },
    }


class TestQuestHandler(EvenniaTest):
    def test_add_new_quest(self):
        self.char1.quests.add(TestQuest)
        self.assertIsInstance(self.char1.quests.get("TestQuest"), TestQuest)

    def test_add_detail(self):
        self.char1.quests.add(TestQuest)
        self.char1.quests.add_detail("TestQuest", TestDetail.TEST_DETAIL, True)
        added_detail = self.char1.quests.get_detail("TestQuest", TestDetail.TEST_DETAIL)
        self.assertEqual(added_detail, True)

    def test_add_details(self):
        self.char1.quests.add(TestQuest)
        self.char1.quests.add_details(
            "TestQuest", {TestDetail.TEST_DETAIL: True, TestDetail.TEST_DETAIL2: True}
        )
        added_details = self.char1.quests.get_details("TestQuest")
        self.assertEqual(
            added_details, {TestDetail.TEST_DETAIL: True, TestDetail.TEST_DETAIL2: True}
        )

    def test_set_objective(self):
        self.char1.quests.add(TestQuest)
        self.char1.quests.set_objective(
            "TestQuest", TestObjective.TEST_OBJECTIVE, "status", QuestProgress.COMPLETED
        )
        objective = self.char1.quests.get_objective(
            "TestQuest", TestObjective.TEST_OBJECTIVE
        )
        self.assertEqual(objective["status"], QuestProgress.COMPLETED)

    def test_update_objectives(self):
        self.char1.quests.add(TestQuest)
        self.char1.quests.update_objectives(
            "TestQuest",
            {
                TestObjective.TEST_OBJECTIVE: {"status": QuestProgress.COMPLETED},
                TestObjective.TEST_HIDDEN_OBJECTIVE: {
                    "status": QuestProgress.COMPLETED
                },
            },
        )
        objectives = self.char1.quests.get_objectives("TestQuest")
        self.assertEqual(
            objectives[TestObjective.TEST_OBJECTIVE]["status"], QuestProgress.COMPLETED
        )
        self.assertEqual(
            objectives[TestObjective.TEST_HIDDEN_OBJECTIVE]["status"],
            QuestProgress.COMPLETED,
        )

    def test_set_status(self):
        self.char1.quests.add(TestQuest)
        self.char1.quests.set_status("TestQuest", QuestProgress.COMPLETED)
        status = self.char1.quests.get_status("TestQuest")
        self.assertEqual(status, QuestProgress.COMPLETED)

    def test_remove_quest(self):
        self.char1.quests.add(TestQuest)
        self.assertEquals(len(self.char1.quests.all()), 1)
        self.char1.quests.remove("TestQuest")
        self.assertEquals(len(self.char1.quests.all()), 0)

    def test_clear_quests(self):
        self.char1.quests.add(TestQuest)
        self.assertEquals(len(self.char1.quests.all()), 1)
        self.char1.quests.clear()
        self.assertEquals(len(self.char1.quests.all()), 0)

    def test_quest_complete(self):
        self.char1.quests.add(TestQuest)
        self.char1.quests.update_objectives(
            "TestQuest",
            {
                TestObjective.TEST_OBJECTIVE: {"status": QuestProgress.COMPLETED},
                TestObjective.TEST_HIDDEN_OBJECTIVE: {
                    "status": QuestProgress.COMPLETED
                },
            },
        )
        self.char1.quests.get("TestQuest").is_complete()
        status = self.char1.quests.get_status("TestQuest")
        self.assertEqual(status, QuestProgress.COMPLETED)
