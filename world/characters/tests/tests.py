from evennia.utils.test_resources import EvenniaTest

from ..classes import ClsRegistry


class TestClsRegistry(EvenniaTest):
    def test_cls_registry(self):
        self.char1.db.cls = ClsRegistry.get("barbarian")
        self.assertEqual(self.char1.db.cls.cls, "barbarian")
        self.assertEqual(self.char1.db.cls.level, 1)
        self.assertEqual(self.char1.db.cls.hit_dice, 12)
