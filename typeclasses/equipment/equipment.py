from enum import Enum

from evennia.utils.utils import lazy_property
from handlers import traits

from typeclasses.objects import Object


class EquipmentType(Enum):
    """
    Defines the type of equipment.
    """

    AMULET = "amulet"
    ARMOR = "armor"
    CLOAK = "cloak"
    FOOTWEAR = "footwear"
    HANDWEAR = "handwear"
    HEADWEAR = "headwear"
    RING = "ring"
    SHIELD = "shield"
    WEAPON = "weapon"


class Equipment(Object):
    """
    Represents an equipment item in the game.

    Attributes:
        db.covering (list): List of body parts covered by the equipment.
        db.equipment_type (EquipmentType): Type of the equipment.
        db.display_name (str): Display name of the equipment.

    Properties:
        equipment_type (EquipmentType): Type of the equipment.
        covering (list): List of body parts covered by the equipment.
        display_name (str): Display name of the equipment.
        position (str): Position where the equipment is worn or held.

    Methods:
        at_object_creation(): Called when the object is created.
        at_drop(caller): Called when the equipment is dropped by a character.
        at_give(caller, target): Called when the equipment is given by one character to another.
    """

    _content_types = (
        "equipment",
        "object",
    )

    def at_object_creation(self):
        self.db.covering = []

    @lazy_property
    def traits(self):
        return traits.TraitHandler(self, db_attribute_key="traits")

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
            EquipmentType.ARMOR: "worn on body",
            EquipmentType.HANDWEAR: "worn on hands",
            EquipmentType.RING: "worn on finger",
            EquipmentType.FOOTWEAR: "worn on feet",
            EquipmentType.WEAPON: "wielding",
            EquipmentType.SHIELD: "holding",
        }
        return position_map.get(self.equipment_type, "on body")

    def at_drop(self, caller):
        if self in caller.equipment.all():
            caller.equipment.remove(self)

    def at_give(self, caller, target):
        if self in caller.equipment.all():
            caller.equipment.remove(self)
