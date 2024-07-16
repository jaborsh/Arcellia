from evennia.utils.test_resources import EvenniaTest

from handlers.rolls import RollHandler
from world.features import racial as racial_feats


class TestRollHandler(EvenniaTest):
    def test_initializes_correctly_when_not_initialized(self):
        handler = RollHandler()
        self.assertTrue(hasattr(handler, "initialized"))
        self.assertTrue(handler.initialized)

    def test_sets_dice_pattern_correctly(self):
        handler = RollHandler()
        self.assertTrue(hasattr(handler, "dice_pattern"))
        self.assertEqual(handler.dice_pattern.pattern, r"(\d*)d(\d+)")

    # Handles cases where the RollHandler object is already initialized
    def test_handles_already_initialized(self):
        handler = RollHandler()
        handler.initialized = True
        handler.__init__()
        self.assertTrue(handler.initialized)

    # check returns True when roll meets or exceeds dc
    def test_check_returns_true_when_roll_meets_or_exceeds_dc(self):
        handler = RollHandler()
        result = handler.check("1d1", dc=0)
        self.assertTrue(result)

    # check returns False when roll does not meet dc
    def test_check_returns_false_when_roll_does_not_meet_dc(self):
        handler = RollHandler()
        result = handler.check("1d1", dc=20)
        self.assertFalse(result)

    # check raises ValueError when both advantage and disadvantage are True
    def test_check_raises_value_error_with_both_advantage_and_disadvantage(
        self,
    ):
        handler = RollHandler()
        with self.assertRaises(ValueError):
            handler.check("1d20", advantage=True, disadvantage=True)

    # Rolling a valid dice string like "2d6" returns a sum within the expected range
    def test_roll_valid_dice_string(self):
        roll_handler = RollHandler()
        result = roll_handler.roll("2d6")
        self.assertTrue(2 <= result <= 12)

    # Rolling with a stat modifier correctly adds the modifier to the total sum
    def test_roll_with_stat_modifier(self):
        roll_handler = RollHandler()
        result = roll_handler.roll("2d6", stat=14)
        self.assertTrue(4 <= result <= 14)

    # Rolling with a stat value less than 1 applies a -5 modifier
    def test_roll_stat_less_than_one_applies_negative_modifier(self):
        roll_handler = RollHandler()
        result = roll_handler.roll("2d6", stat=0)
        self.assertTrue(-3 <= result <= 7)

    # Returns correct modifier for stat values between 1 and 30
    def test_modifier_for_stat_values_between_1_and_30(self):
        obj = RollHandler()
        self.assertEqual(obj.get_modifier(10), 0)
        self.assertEqual(obj.get_modifier(15), 2)
        self.assertEqual(obj.get_modifier(20), 5)

    # Test HalflingLuck
    def test_halfling_luck_trait(self):
        # Create a RollHandler object
        roll_handler = RollHandler()

        # Create a Roller object with HalflingLuck buff
        self.char1.feats.add(racial_feats.HalflingLuck)

        # Define the roll parameters
        roll_str = "1d2"

        # Call the roll method with HalflingLuck trait
        result = roll_handler.roll(roll_str, roller=self.char1)

        # Assert the result
        self.assertEqual(result, 2)
