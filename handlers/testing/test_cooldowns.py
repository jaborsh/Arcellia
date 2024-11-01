from evennia.utils.test_resources import EvenniaTest
from mock import patch

from ..cooldowns import CooldownHandler


class TestCooldownHandler(EvenniaTest):
    """Test the CooldownHandler functionality."""

    def setUp(self):
        super().setUp()
        self.handler = CooldownHandler(self.char1, default_data={})

    @patch("time.time")
    def test_ready(self, mock_time):
        """Test cooldown ready state."""
        # Mock time to be consistent
        mock_time.return_value = 100.0

        # Test non-existent cooldown
        self.assertTrue(self.handler.ready("nonexistent"))

        # Test active cooldown
        self.handler.add("test", 10)
        self.assertFalse(self.handler.ready("test"))

        # Test expired cooldown
        mock_time.return_value = 111.0  # Advance time past cooldown
        self.assertTrue(self.handler.ready("test"))

    @patch("time.time")
    def test_time_left(self, mock_time):
        """Test time remaining calculations."""
        mock_time.return_value = 100.0

        # Test non-existent cooldown
        self.assertEqual(self.handler.time_left("nonexistent"), 0.0)

        # Test active cooldown
        self.handler.add("test", 10)
        self.assertEqual(self.handler.time_left("test", use_int=True), 10)

        # Test partially elapsed cooldown
        mock_time.return_value = 105.0
        self.assertEqual(self.handler.time_left("test", use_int=True), 5)

        # Test expired cooldown
        mock_time.return_value = 111.0
        self.assertEqual(self.handler.time_left("test"), 0.0)

    @patch("time.time")
    def test_add_and_set(self, mock_time):
        """Test adding/setting cooldowns."""
        mock_time.return_value = 100.0

        # Test basic add
        self.handler.add("test", 10)
        self.assertEqual(self.handler._data["test"], 110.0)

        # Test set alias
        self.handler.set("test2", 20)
        self.assertEqual(self.handler._data["test2"], 120.0)

        # Test overwriting existing cooldown
        self.handler.add("test", 30)
        self.assertEqual(self.handler._data["test"], 130.0)

    @patch("time.time")
    def test_extend(self, mock_time):
        """Test extending cooldowns."""
        mock_time.return_value = 100.0

        # Test extending non-existent cooldown
        self.handler.extend("test", 10)
        self.assertEqual(self.handler._data["test"], 110.0)

        # Test extending existing cooldown
        mock_time.return_value = 105.0
        self.handler.extend("test", 10)
        self.assertEqual(self.handler._data["test"], 120.0)

    @patch("time.time")
    def test_reset_and_clear(self, mock_time):
        """Test resetting individual and all cooldowns."""
        mock_time.return_value = 100.0

        # Setup multiple cooldowns
        self.handler.add("test1", 10)
        self.handler.add("test2", 20)

        # Test reset individual
        self.handler.reset("test1")
        self.assertNotIn("test1", self.handler._data)
        self.assertIn("test2", self.handler._data)

        # Test reset non-existent
        self.handler.reset("nonexistent")  # Should not raise error

        # Test clear all
        self.handler.clear()
        self.assertEqual(len(self.handler._data), 0)

    @patch("time.time")
    def test_cleanup(self, mock_time):
        """Test cleanup of expired cooldowns."""
        mock_time.return_value = 100.0

        # Setup cooldowns
        self.handler.add("active", 10)
        self.handler.add("expired", -10)  # Already expired

        # Run cleanup
        self.handler.cleanup()

        # Verify only active cooldown remains
        self.assertIn("active", self.handler._data)
        self.assertNotIn("expired", self.handler._data)

    def test_all(self):
        """Test listing all cooldowns."""
        self.handler.add("test1", 10)
        self.handler.add("test2", 20)

        cooldowns = self.handler.all()
        self.assertEqual(len(cooldowns), 2)
        self.assertIn("test1", cooldowns)
        self.assertIn("test2", cooldowns)
