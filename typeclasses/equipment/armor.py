from enum import Enum

from .equipment import Equipment, EquipmentType


class ArmorCategory(Enum):
    """
    Defines the category of armor.
    """

    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"


class Armor(Equipment):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.equipment_type = EquipmentType.ARMOR

    @property
    def category(self):
        return self.traits.get("category")

    @category.setter
    def category(self, value: ArmorCategory):
        self.traits.add("category", "Category", trait_type="trait", value=value)
