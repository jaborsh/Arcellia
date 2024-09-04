from evennia import create_object
from evennia.utils.test_resources import EvenniaCommandTest

from world.spells.spells import Spell

_TEST_SPELL = Spell()
_TEST_SPELL2 = Spell()


class TestCombatHandler(EvenniaCommandTest):
    def setUp(self):
        super().setUp()
        self.mob1 = create_object("typeclasses.mobs.Mob", key="Mob")
        self.mob2 = create_object("typeclasses.mobs.Mob", key="Mob2")

    def test_combat_default_initialization(self):
        self.assertEqual(self.room1.combat._data["combatants"], {})
        self.assertEqual(self.room1.combat._data["action_queue"], [])

    def test_adding_combatant_with_no_enemies(self):
        self.room1.combat.add_combat(self.char1)
        self.assertEqual(self.room1.combat._data["combatants"], {})
        self.assertEqual(self.room1.combat._data["action_queue"], [])

    def test_add_new_combatant_successfully(self):
        self.room1.combat.add_combat(self.char1, self.mob1)
        self.assertIn(self.char1, self.room1.combat._data["combatants"])
        self.assertIn(self.mob1, self.room1.combat._data["combatants"])
        self.assertIn(self.mob1, self.room1.combat._data["combatants"][self.char1])
        self.assertIn(self.char1, self.room1.combat._data["combatants"][self.mob1])

    def test_add_existing_combatant(self):
        self.room1.combat.add_combat(self.char1, self.mob1)
        self.room1.combat.add_combat(self.char1, self.mob1)
        self.assertEqual(self.room1.combat._data["combatants"][self.char1], [self.mob1])
        self.assertEqual(self.room1.combat._data["combatants"][self.mob1], [self.char1])
        self.assertEqual(len(self.room1.combat._data["combatants"]), 2)

    def test_adding_combatant_with_list_of_enemies(self):
        self.room1.combat.add_combat(self.char1, [self.mob1, self.mob2])
        self.assertEqual(
            self.room1.combat._data["combatants"][self.char1], [self.mob1, self.mob2]
        )
        self.assertEqual(len(self.room1.combat._data["combatants"]), 3)

    def test_removing_nonexistent_combatant(self):
        self.room1.combat.add_combat(self.char1, self.mob1)
        self.room1.combat.remove_combatant(self.char2)
        self.assertEqual(self.room1.combat._data["combatants"][self.char1], [self.mob1])
        self.assertEqual(self.room1.combat._data["combatants"][self.mob1], [self.char1])

    def test_removing_combatant_success(self):
        self.room1.combat.add_combat(self.char1, self.mob1)
        self.room1.combat.remove_combatant(self.char1)
        self.assertNotIn(self.char1, self.room1.combat._data["combatants"])
        self.assertNotIn(self.mob1, self.room1.combat._data["combatants"])

    def test_add_valid_action_to_queue(self):
        self.room1.combat.add_action(self.char1, {"action": _TEST_SPELL})
        self.assertIn(
            (self.char1, {"action": _TEST_SPELL}), self.room1.combat.action_queue
        )
        self.assertEqual(len(self.room1.combat.action_queue), 1)

    def test_retrieves_next_action_when_queue_not_empty(self):
        self.room1.combat.add_action(self.char1, {"action": _TEST_SPELL})
        self.room1.combat.add_action(self.char1, {"action": _TEST_SPELL2})
        self.assertEqual(
            self.room1.combat.get_next_action(), (self.char1, {"action": _TEST_SPELL})
        )
        self.assertEqual(len(self.room1.combat.action_queue), 1)
        self.assertEqual(
            self.room1.combat.get_next_action(), (self.char1, {"action": _TEST_SPELL2})
        )
        self.assertEqual(len(self.room1.combat.action_queue), 0)

    def test_retrieves_next_action_none_when_queue_empty(self):
        self.assertIsNone(self.room1.combat.get_next_action())

    def test_remove_actions_for_combatant(self):
        self.room1.combat.add_action(self.char1, {"action": _TEST_SPELL})
        self.room1.combat.add_action(self.char1, {"action": _TEST_SPELL2})
        self.room1.combat.remove_actions(self.char1)
        self.assertEqual(list(self.room1.combat.action_queue), [])

    def test_clear_actions(self):
        self.room1.combat.add_action(self.char1, {"action": _TEST_SPELL})
        self.room1.combat.add_action(self.char1, {"action": _TEST_SPELL2})
        self.room1.combat.clear_actions()
        self.assertEqual(list(self.room1.combat.action_queue), [])

    def test_execute_action(self):
        self.room1.combat.add_action(self.char1, {"action": _TEST_SPELL})
        self.room1.combat.execute_action()
        self.assertEqual(list(self.room1.combat.action_queue), [])

    def test_execute_action_no_action(self):
        self.room1.combat.execute_action()
        self.assertEqual(list(self.room1.combat.action_queue), [])
