from unittest.mock import Mock, patch  # Add patch import

from evennia.utils.test_resources import EvenniaTest

from ..combat import CombatHandler


class MockWeapon:
    def __init__(self, damage, attack_msg):
        self.damage = damage
        self.db = Mock()
        self.db.primary_attack = attack_msg
        self.db.secondary_attack = attack_msg


class MockEquipment:
    def __init__(self, weapons=None):
        self.weapons = weapons or []


class MockCombatant:
    def __init__(self, name, location=None, health=100):
        self.key = name
        self.location = location
        self.health = health
        self.equipment = MockEquipment()

    def is_alive(self):
        return self.health > 0

    def at_damage(self, damage):
        self.health -= damage


class TestCombatHandler(EvenniaTest):
    def setUp(self):
        super().setUp()
        self.room = self.room1  # from EvenniaTest
        self.handler = CombatHandler(self.room)

        # Create test combatants
        self.fighter1 = MockCombatant("Fighter1", self.room)
        self.fighter2 = MockCombatant("Fighter2", self.room)
        self.fighter3 = MockCombatant("Fighter3", self.room)

        # Create test weapons
        self.sword = MockWeapon(10, "slashes with a sword")
        self.dagger = MockWeapon(5, "stabs with a dagger")

    def test_initialization(self):
        """Test basic handler initialization"""
        self.assertFalse(self.handler.is_fighting)
        self.assertEqual(len(self.handler.queue), 0)
        self.assertEqual(len(self.handler._data["combatants"]), 0)

    def test_add_combatant(self):
        """Test adding combatants to combat"""
        self.handler.add_combatant(self.fighter1, self.fighter2)

        # Check both fighters are in combat
        self.assertIn(self.fighter1, self.handler._data["combatants"])
        self.assertIn(self.fighter2, self.handler._data["combatants"])

        # Check they are enemies of each other
        self.assertIn(self.fighter2, self.handler.get_enemies(self.fighter1))
        self.assertIn(self.fighter1, self.handler.get_enemies(self.fighter2))

    def test_remove_combatant(self):
        """Test removing combatants from combat"""
        self.handler.add_combatant(
            self.fighter1, [self.fighter2, self.fighter3]
        )
        self.handler.remove_combatant(self.fighter1)

        # Check fighter1 is removed
        self.assertNotIn(self.fighter1, self.handler._data["combatants"])

        # Check fighter1 is removed from others' enemy lists
        self.assertNotIn(self.fighter1, self.handler.get_enemies(self.fighter2))
        self.assertNotIn(self.fighter1, self.handler.get_enemies(self.fighter3))

    @patch("evennia.utils.utils.delay", new=Mock())
    def test_combat_flow(self):
        """Test the combat turn sequence"""
        # Setup combat with weapons
        self.fighter1.equipment.weapons = [self.sword]
        self.fighter2.equipment.weapons = [self.dagger]

        self.handler.add_combatant(self.fighter1, self.fighter2)

        # Check combat started
        self.assertTrue(self.handler.is_fighting)
        self.assertEqual(len(self.handler.queue), 2)

        # Process first turn - this should trigger a delay call
        self.handler.process_next_turn()

        # Check damage was dealt
        self.assertTrue(self.fighter2.health < 100)

        # Verify turn sequence - both fighters should still be in queue
        self.assertEqual(len(self.handler.queue), 2)

    def test_combat_death(self):
        """Test combat ending when a fighter dies"""
        self.fighter1.equipment.weapons = [self.sword]
        self.fighter2.health = 5  # Will die in one hit

        self.handler.add_combatant(self.fighter1, self.fighter2)
        self.handler.process_next_turn()

        # Check fighter2 was removed after death
        self.assertNotIn(self.fighter2, self.handler._data["combatants"])
        self.assertFalse(self.fighter2.is_alive())

    def test_dual_wielding(self):
        """Test damage calculation with dual wielding"""
        self.fighter1.equipment.weapons = [self.sword, self.dagger]
        expected_damage = self.sword.damage + (self.dagger.damage * 0.5)

        self.handler.add_combatant(self.fighter1, self.fighter2)
        initial_health = self.fighter2.health

        self.handler.perform_attack(self.fighter1)
        actual_damage = initial_health - self.fighter2.health

        self.assertEqual(actual_damage, expected_damage)

    def test_invalid_combatant(self):
        """Test handling of invalid combatants"""
        # Test combatant not in location
        self.fighter1.location = None
        self.assertFalse(self.handler._valid_combatant(self.fighter1))

        # Test dead combatant
        self.fighter2.health = 0
        self.assertFalse(self.handler._valid_combatant(self.fighter2))

    def test_combat_state(self):
        """Test combat state management"""
        self.handler.add_combatant(self.fighter1, self.fighter2)
        self.assertTrue(self.handler.is_combat_active())

        self.handler.end_combat()
        self.assertFalse(self.handler.is_fighting)
        self.assertEqual(len(self.handler.queue), 0)

    @patch("evennia.utils.utils.delay", new=Mock())
    def test_add_combatant_mid_combat(self):
        """Test adding a new combatant after combat has started"""
        # Setup initial combat
        self.fighter1.equipment.weapons = [self.sword]
        self.fighter2.equipment.weapons = [self.dagger]
        self.fighter3.equipment.weapons = [
            self.sword
        ]  # Give fighter3 a weapon too

        # Start combat with two fighters
        self.handler.add_combatant(self.fighter1, self.fighter2)

        # Verify initial state
        self.assertTrue(self.handler.is_fighting)
        self.assertEqual(len(self.handler.queue), 2)

        # Add third fighter mid-combat
        self.handler.add_combatant(
            self.fighter3, [self.fighter1, self.fighter2]
        )

        # Verify fighter3 was added properly
        self.assertIn(self.fighter3, self.handler._data["combatants"])
        self.assertEqual(len(self.handler.queue), 3)

        # Verify enemy relationships
        self.assertIn(self.fighter1, self.handler.get_enemies(self.fighter3))
        self.assertIn(self.fighter2, self.handler.get_enemies(self.fighter3))
        self.assertIn(self.fighter3, self.handler.get_enemies(self.fighter1))
        self.assertIn(self.fighter3, self.handler.get_enemies(self.fighter2))
