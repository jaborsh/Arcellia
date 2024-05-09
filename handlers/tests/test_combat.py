from collections import deque
from unittest.mock import call, patch

from evennia.utils.test_resources import EvenniaCommandTest
from handlers.combat import TurnState


class TestCombatHandler(EvenniaCommandTest):
    def setUp(self):
        super().setUp()
        self.char2.dexterity.mod = 1
        self.room1.combat.add_combatant(self.char1, self.char2)

    def test_combat_initialization(self):
        self.assertEqual(
            self.room1.combat.combatants,
            {
                self.char1: {"enemies": {self.char2}, "state": TurnState.WAITING},
                self.char2: {"enemies": {self.char1}, "state": TurnState.WAITING},
            },
        )
        self.assertEqual(self.room1.combat.turn_queue, deque([self.char2, self.char1]))

    def test_execute_combatant_turn(self):
        self.room1.combat.execute_turn(self.char1)
        self.assertEqual(
            self.room1.combat.combatants[self.char1]["state"], TurnState.DONE
        )

    @patch("builtins.print")
    def test_combat_round(self, mock_print):
        self.room1.combat.start_round()

        expected_calls = [
            call("Char2 attacks!"),
            call("Char attacks!"),
            call("The round has ended."),
        ]

        mock_print.assert_has_calls(expected_calls, any_order=False)

    def test_remove_combatant(self):
        self.room1.combat.remove_combatant(self.char1)
        self.assertNotIn(self.char1, self.room1.combat.combatants)
        self.assertNotIn(self.char2, self.room1.combat.combatants)
