from copy import copy

from evennia.utils import dbserialize

from handlers.clothing.clothing_types import ClothingType
from typeclasses.equipment.equipment import EquipmentType

EQUIPMENT_DEFAULTS = {slot: None for slot in EquipmentType}

EQUIPMENT_TYPE_COVER = {
    EquipmentType.HEADWEAR: [
        ClothingType.HEADWEAR,
        ClothingType.EYEWEAR,
        ClothingType.EARRING,
    ],
    EquipmentType.ARMOR: [
        ClothingType.UNDERSHIRT,
        ClothingType.TOP,
        ClothingType.OUTERWEAR,
        ClothingType.FULLBODY,
        ClothingType.BELT,
        ClothingType.UNDERWEAR,
        ClothingType.BOTTOM,
        ClothingType.HOSIERY,
    ],
    EquipmentType.HANDWEAR: [
        ClothingType.WRISTWEAR,
        ClothingType.HANDWEAR,
        ClothingType.RING,
    ],
    EquipmentType.FOOTWEAR: [ClothingType.HOSIERY, ClothingType.FOOTWEAR],
}

EQUIPMENT_TYPE_ORDER = [
    EquipmentType.HEADWEAR,
    EquipmentType.AMULET,
    EquipmentType.ARMOR,
    EquipmentType.HANDWEAR,
    EquipmentType.RING,
    EquipmentType.FOOTWEAR,
    EquipmentType.WEAPON,
    EquipmentType.SHIELD,
]


class EquipmentHandler:
    """
    A class that handles equipment management for a game object.

    Attributes:
        equipment_defaults (dict): A dictionary containing the default equipment slots and their initial values.

    Methods:
        __init__(self, obj, db_attribute="equipment"): Initializes the EquipmentHandler instance.
        all(self): Returns a list of all equipped items.
        remove(self, item): Removes the specified item from the equipment.
        wear(self, item): Wears the specified item.
        reset(self): Resets the equipment to its default values.
    """

    def __init__(
        self,
        obj,
        db_attribute="equipment",
        db_category=None,
    ):
        self.obj = obj
        self._db_attribute = db_attribute
        self._db_category = db_category
        self._equipment = copy(EQUIPMENT_DEFAULTS)
        self._load()

    def _load(self):
        loaded_data = self.obj.attributes.get(
            self._db_attribute, copy(EQUIPMENT_DEFAULTS)
        )
        self._equipment = dbserialize.deserialize(loaded_data)

    def _save(self):
        self.obj.attributes.add(
            self._db_attribute, self._equipment, category=self._db_category
        )

    def _display_action_message(self, item, action):
        is_weapon = item.equipment_type == EquipmentType.WEAPON
        verb = (
            "wield"
            if is_weapon and action == "wear"
            else "shealth"
            if is_weapon
            else action
        )
        message = f"$You() $conj({verb}) $you(obj)."
        self.obj.location.msg_contents(
            message, from_obj=self.obj, mapping={"obj": item}
        )

    def _get_slot_contents(self, slot_type):
        contents = self._equipment[slot_type]
        if contents is None:
            return []

        return contents if isinstance(contents, list) else [contents]

    def _is_slot_available(self, item):
        slot_type = item.equipment_type

        if slot_type == EquipmentType.RING:
            return len(self._equipment(EquipmentType.RING) or []) < 2
        elif slot_type == EquipmentType.SHIELD:
            weapons = self._equipment[EquipmentType.WEAPON] or []
            shield = self._equipment[EquipmentType.SHIELD]
            return len(weapons) < 2 and not shield
        elif slot_type == EquipmentType.WEAPON:
            weapons = self._equipment[EquipmentType.WEAPON] or []
            shield = self._equipment[EquipmentType.SHIELD]
            return len(weapons) < (1 if shield else 2)

        return not self._equipment[slot_type]

    @property
    def weapons(self):
        return self._equipment[EquipmentType.WEAPON] or []

    def all(self):
        equipment = []
        for slot_type in EQUIPMENT_TYPE_ORDER:
            equipment.extend(self._get_slot_contents(slot_type))
        return [item for item in equipment if item]

    def remove(self, item):
        for slot_type, equipped in self._equipment.items():
            if isinstance(equipped, list) and item in equipped:
                equipped.remove(item)
                break
            elif equipped == item:
                self._equipment[slot_type] = None
                break

        for piece in item.covering:
            piece.covered_by.remove(self)
        item.covering = []

        if item.equipment_type in (EquipmentType.WEAPON, EquipmentType.SHIELD):
            weapons = self._equipment[EquipmentType.WEAPON]
            if weapons:
                self.obj.msg("You switch your weapon to use two hands.")

        self._save()
        self._display_action_message(item, "remove")

    def wear(self, item):
        """Wear/equip an item."""
        if item in self.all():
            verb = (
                "wielding"
                if item.equipment_type == EquipmentType.WEAPON
                else "wearing"
            )
            self.obj.msg(f"You are already {verb} that.")
            return

        if not self._is_slot_available(item):
            # Error messages handled in _is_slot_available
            return

        slot_type = item.equipment_type
        if slot_type in (EquipmentType.WEAPON, EquipmentType.RING):
            self._equipment[slot_type] = self._equipment[slot_type] or []
            self._equipment[slot_type].append(item)
        else:
            self._equipment[slot_type] = item

        self._save()
        self._display_action_message(item, "wear")

    def reset(self):
        """
        Resets the equipment to its default values.
        """
        self._equipment = copy(EQUIPMENT_DEFAULTS)
        self._save()
