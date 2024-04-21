from commands import general
from evennia.utils.test_resources import EvenniaCommandTest
from handlers.tests.quest_tests import TestQuest


class TestQuests(EvenniaCommandTest):
    def setUp(self):
        super().setUp()
        self.char1.quests.add(TestQuest)

    def test_quest_list(self):
        self.call(general.CmdQuests(), "")

    def test_quest_specific(self):
        self.call(general.CmdQuests(), "TestQuest")
