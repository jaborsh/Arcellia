from evennia import create_object
from evennia.utils.test_resources import EvenniaCommandTest


class TestCombatHandler(EvenniaCommandTest):
    def setUp(self):
        super().setUp()
        self.mob1 = create_object("typeclasses.mobs.Mob", key="Mob")
        self.mob2 = create_object("typeclasses.mobs.Mob", key="Mob2")

    def test_combat_default_initialization(self):
        self.assertEqual(self.room1.combat._data["combatants"], {})
        self.assertEqual(self.room1.combat._data["action_queue"], [])

    def test_adding_combatant_with_no_enemies(self):
        self.room1.combat.add_combatant(self.char1)
        self.assertEqual(self.room1.combat._data["combatants"], {})
        self.assertEqual(self.room1.combat._data["action_queue"], [])

    def test_add_new_combatant_successfully(self):
        self.room1.combat.add_combatant(self.char1, self.mob1)
        self.assertIn(self.char1, self.room1.combat._data["combatants"])
        self.assertIn(self.mob1, self.room1.combat._data["combatants"])
        self.assertIn(
            self.mob1, self.room1.combat._data["combatants"][self.char1]
        )
        self.assertIn(
            self.char1, self.room1.combat._data["combatants"][self.mob1]
        )

    def test_add_existing_combatant(self):
        self.room1.combat.add_combatant(self.char1, self.mob1)
        self.room1.combat.add_combatant(self.char1, self.mob1)
        self.assertEqual(
            self.room1.combat._data["combatants"][self.char1], [self.mob1]
        )
        self.assertEqual(
            self.room1.combat._data["combatants"][self.mob1], [self.char1]
        )
        self.assertEqual(len(self.room1.combat._data["combatants"]), 2)

    def test_adding_combatant_with_list_of_enemies(self):
        self.room1.combat.add_combatant(self.char1, [self.mob1, self.mob2])
        self.assertEqual(
            self.room1.combat._data["combatants"][self.char1],
            [self.mob1, self.mob2],
        )
        self.assertEqual(len(self.room1.combat._data["combatants"]), 3)

    def test_removing_nonexistent_combatant(self):
        self.room1.combat.add_combatant(self.char1, self.mob1)
        self.room1.combat.remove_combatant(self.char2)
        self.assertEqual(
            self.room1.combat._data["combatants"][self.char1], [self.mob1]
        )
        self.assertEqual(
            self.room1.combat._data["combatants"][self.mob1], [self.char1]
        )

    def test_removing_combatant_success(self):
        self.room1.combat.add_combatant(self.char1, self.mob1)
        self.room1.combat.remove_combatant(self.char1)
        self.assertNotIn(self.char1, self.room1.combat._data["combatants"])
        self.assertNotIn(self.mob1, self.room1.combat._data["combatants"])
