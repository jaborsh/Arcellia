from collections import deque
from unittest.mock import call, patch

from evennia import create_object
from evennia.utils.test_resources import EvenniaCommandTest
from handlers.combat import TurnState


class TestCombatHandler(EvenniaCommandTest):
    def setUp(self):
        super().setUp()
        self.mob = create_object("typeclasses.mobs.Mob", key="Mob")
        self.mob.dexterity.base = 11
        self.room1.combat.add_combatant(self.char1, self.mob)

    def test_combat_initialization(self):
        self.assertEqual(
            self.room1.combat.combatants,
            {
                self.char1: {"enemies": {self.mob}, "state": TurnState.WAITING},
                self.mob: {"enemies": {self.char1}, "state": TurnState.WAITING},
            },
        )
        self.assertEqual(self.room1.combat.turn_queue, deque([self.mob, self.char1]))

    @patch("builtins.print")
    def test_execute_combatant_turn(self, mock_print):
        self.room1.combat.execute_turn(self.char1)

        expected_calls = [call("Char attacks!")]

        mock_print.assert_has_calls(expected_calls)
        self.assertEqual(
            self.room1.combat.combatants[self.char1]["state"], TurnState.DONE
        )

    @patch("builtins.print")
    def test_combat_round(self, mock_print):
        self.room1.combat.start_round()

        expected_calls = [
            call("Mob attacks!"),
            call("Char attacks!"),
            call("The round has ended."),
        ]

        mock_print.assert_has_calls(expected_calls, any_order=False)

    def test_remove_combatant(self):
        self.room1.combat.remove_combatant(self.char1)
        self.assertNotIn(self.char1, self.room1.combat.combatants)
        self.assertNotIn(self.mob, self.room1.combat.combatants)
