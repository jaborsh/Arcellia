from enum import Enum

from evennia.utils.utils import lazy_property
from typeclasses.mixins.items import ItemMixin
from typeclasses.objects import Object


class EquipmentType(Enum):
    """
    Defines the type of equipment.
    """

    AMULET = "amulet"
    BODY = "body"
    CLOAK = "cloak"
    FOOTWEAR = "footwear"
    HANDWEAR = "handwear"
    HEADWEAR = "headwear"
    RING = "ring"
    SHIELD = "shield"
    WEAPON = "weapon"


class Equipment(ItemMixin, Object):
    def at_object_creation(self):
        self.db.covering = []

    @property
    def equipment_type(self):
        return self.attributes.get("equipment_type", None)

    @equipment_type.setter
    def equipment_type(self, value: EquipmentType):
        self.db.equipment_type = value

    @property
    def covering(self):
        return self.attributes.get("covering", [])

    @covering.setter
    def covering(self, value: list):
        self.db.covering = value

    @property
    def display_name(self):
        return self.attributes.get("display_name", self.key)

    @display_name.setter
    def display_name(self, value: str):
        self.db.display_name = value

    @lazy_property
    def position(self):
        position_map = {
            EquipmentType.HEADWEAR: "worn on head",
            EquipmentType.AMULET: "worn around neck",
            EquipmentType.CLOAK: "worn on back",
            EquipmentType.BODY: "worn on body",
            EquipmentType.HANDWEAR: "worn on hands",
            EquipmentType.RING: "worn on finger",
            EquipmentType.FOOTWEAR: "worn on feet",
            EquipmentType.WEAPON: "wielding",
            EquipmentType.SHIELD: "holding",
        }
        return position_map.get(self.equipment_type, "on body")

    def at_drop(self, caller):
        caller.equipment.remove(self)

    def at_give(self, caller, target):
        caller.equipment.remove(self)
