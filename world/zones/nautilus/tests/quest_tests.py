from handlers.quests import QuestProgress

from evennia.utils.test_resources import EvenniaCommandTest, EvenniaTest
from world.nautilus.interactions.levers import CmdPullLever

from ..quest import NautilusObjective, NautilusQuest


class TestNautilusQuest(EvenniaTest):
    def test_add_quest(self):
        self.char1.quests.add(NautilusQuest)
        self.assertIsInstance(self.char1.quests.get("Nautilus"), NautilusQuest)

    def test_assess_body(self):
        self.char1.quests.add(NautilusQuest)
        self.char1.quests.set_objective(
            "Nautilus", NautilusObjective.ASSESS_BODY, "status", QuestProgress.COMPLETED
        )
        self.assertEqual(
            self.char1.quests.get("Nautilus").get_objective_status(
                NautilusObjective.ASSESS_BODY
            ),
            QuestProgress.COMPLETED,
        )


class TestNautilusLevers(EvenniaCommandTest):
    def test_free_enchantress(self):
        self.char1.quests.add(NautilusQuest)
        self.char1.quests.set_objective_status(
            "Nautilus", NautilusObjective.FREE_ENCHANTRESS, QuestProgress.IN_PROGRESS
        )
        self.call(
            CmdPullLever(),
            "left",
            "You pull the left lever and hear a loud clunk. Suddenly, the enchantress' cell door swings open!",
        )
        self.assertTrue(
            self.char1.quests.get("Nautilus").get_objective_status(
                NautilusObjective.FREE_ENCHANTRESS
            )
            == QuestProgress.COMPLETED
        )

    def test_kill_enchantress(self):
        self.char1.quests.add(NautilusQuest)
        self.char1.quests.get("Nautilus").set_objective_status(
            NautilusObjective.FREE_ENCHANTRESS, QuestProgress.IN_PROGRESS
        )
        self.call(
            CmdPullLever(),
            "right",
            "You pull the right lever and hear a loud clunk. Psionic energy radiates from the enchantress' cell and she disintegrates into thin air.",
        )
        self.assertTrue(
            self.char1.quests.get("Nautilus").get_objective_status(
                NautilusObjective.FREE_ENCHANTRESS
            )
            == QuestProgress.FAILED
        )
