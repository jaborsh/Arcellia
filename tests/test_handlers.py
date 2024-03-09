import unittest

from handlers.rolls import RollHandler


class TestRollHandler(unittest.TestCase):
    def setUp(self):
        self.obj = RollHandler()

    def testValueError(self):
        with self.assertRaises(ValueError):
            self.obj.roll("invalid_string")

    def test_roll_single_without_mod(self):
        result = self.obj.roll("1d6")
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 1)
        self.assertLessEqual(result, 6)

    def test_roll_single_with_mod(self):
        result = self.obj.roll("1d6", 15)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 3)
        self.assertLessEqual(result, 8)

    def test_roll_multiple_with_mod(self):
        result = self.obj.roll("3d6", 15)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 5)
        self.assertLessEqual(result, 20)

    def test_roll_multiple_without_mod(self):
        result = self.obj.roll("3d6")
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 3)
        self.assertLessEqual(result, 18)

    def test_roll_negative_inf(self):
        result = self.obj.roll("1d6", -99)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, -4)
        self.assertLessEqual(result, 1)

    def test_roll_positive_inf(self):
        result = self.obj.roll("1d6", 99)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 10)
        self.assertLessEqual(result, 16)

    def test_greater_than_or_equal_to_dc(self):
        result = self.obj.check("1d6", dc=5, stat=30)
        self.assertTrue(result)

    def test_less_than_dc(self):
        result = self.obj.check("1d6")
        self.assertFalse(result)
