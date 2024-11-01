from unittest.mock import patch

from evennia.utils import create
from evennia.utils.test_resources import BaseEvenniaTest, BaseEvenniaTestCase

from handlers.clothing import ClothingHandler
from handlers.config.clothing_config import ClothingConfig
from typeclasses.clothing import Clothing, ClothingType


class TestClothingConfig(BaseEvenniaTestCase):
    """Test the ClothingConfig constants and relationships"""

    def test_type_cover_consistency(self):
        """Test that all ClothingTypes are present in TYPE_COVER"""
        for clothing_type in ClothingType:
            self.assertIn(clothing_type, ClothingConfig.TYPE_COVER)

    def test_defaults_consistency(self):
        """Test that all ClothingTypes have default values"""
        for clothing_type in ClothingType:
            self.assertIn(clothing_type, ClothingConfig.DEFAULTS)

    def test_type_order_consistency(self):
        """Test that all ClothingTypes are in TYPE_ORDER"""
        for clothing_type in ClothingType:
            self.assertIn(clothing_type, ClothingConfig.TYPE_ORDER)


class TestClothingHandler(BaseEvenniaTest):
    """Test the ClothingHandler functionality"""

    def setUp(self):
        """Set up test fixtures"""
        super().setUp()

        # Create the handler on the test character
        self.handler = ClothingHandler(self.char1, "clothing")

        # Create test clothing items
        self.shirt = create.create_object(
            Clothing,
            key="shirt",
            location=self.char1,
        )
        self.shirt.clothing_type = ClothingType.TOP

        self.jacket = create.create_object(
            Clothing,
            key="jacket",
            location=self.char1,
        )
        self.jacket.clothing_type = ClothingType.OUTERWEAR

    def test_initialization(self):
        """Test handler initialization"""
        self.assertEqual(self.handler._data, ClothingConfig.DEFAULTS.copy())

    def test_can_wear(self):
        """Test can_wear method"""
        self.assertTrue(self.handler.can_wear(self.shirt))

        # Test non-clothing item
        self.assertFalse(self.handler.can_wear(self.obj1))

        # Test overall limit
        with patch.object(ClothingConfig, "OVERALL_LIMIT", 1):
            self.handler.wear(self.shirt)
            self.assertFalse(self.handler.can_wear(self.jacket))

    def test_wear(self):
        """Test wear method"""
        self.assertTrue(self.handler.wear(self.shirt))
        self.assertIn(self.shirt, self.handler.get(ClothingType.TOP))

        # Test coverage relationships
        self.handler.wear(self.jacket)
        self.assertIn(self.shirt, self.jacket.covering)
        self.assertIn(self.jacket, self.shirt.covered_by)

    def test_remove(self):
        """Test remove method"""
        self.handler.wear(self.shirt)
        self.handler.wear(self.jacket)

        self.assertTrue(self.handler.remove(self.jacket))
        self.assertNotIn(self.jacket, self.shirt.covered_by)
        self.assertEqual(self.jacket.covering, [])

        # Test removing non-worn item
        non_worn = create.create_object(
            Clothing, key="non_worn", location=self.char1
        )
        non_worn.clothing_type = ClothingType.TOP
        self.assertFalse(self.handler.remove(non_worn))

    def test_all(self):
        """Test all method"""
        self.handler.wear(self.shirt)
        self.handler.wear(self.jacket)

        all_clothes = self.handler.all()
        self.assertEqual(len(all_clothes), 2)

        # Test exclude_covered parameter
        visible_clothes = self.handler.all(exclude_covered=True)
        self.assertEqual(len(visible_clothes), 1)
        self.assertIn(self.jacket, visible_clothes)

    def test_reset(self):
        """Test reset method"""
        self.handler.wear(self.shirt)
        self.handler.wear(self.jacket)

        self.handler.reset()
        self.assertEqual(self.handler._data, ClothingConfig.DEFAULTS.copy())
        # alternatively, could use handler's default_data parameter:
        # self.assertEqual(self.handler._data, self.handler._default_data)
        self.assertEqual(len(self.handler.all()), 0)
