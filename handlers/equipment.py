from copy import copy

from handlers.clothing.clothing_types import ClothingType
from handlers.handler import Handler
from typeclasses.equipment.equipment import EquipmentType

EQUIPMENT_DEFAULTS = {
    EquipmentType.HEADWEAR: None,
    EquipmentType.AMULET: None,
    EquipmentType.CLOAK: None,
    EquipmentType.ARMOR: None,
    EquipmentType.HANDWEAR: None,
    EquipmentType.RING: None,
    EquipmentType.FOOTWEAR: None,
    EquipmentType.WEAPON: None,
    EquipmentType.SHIELD: None,
}


EQUIPMENT_TYPE_COVER = {
    EquipmentType.HEADWEAR: [
        ClothingType.HEADWEAR,
        ClothingType.EYEWEAR,
        ClothingType.EARRING,
    ],
    EquipmentType.AMULET: [],
    EquipmentType.CLOAK: [],
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
    EquipmentType.RING: [],
    EquipmentType.FOOTWEAR: [ClothingType.HOSIERY, ClothingType.FOOTWEAR],
    EquipmentType.WEAPON: [],
    EquipmentType.SHIELD: [],
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


class EquipmentHandler(Handler):
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
        db_attribute_key,
        db_attribute_category=None,
        default_data=copy(EQUIPMENT_DEFAULTS),
    ):
        super().__init__(
            obj, db_attribute_key, db_attribute_category, default_data
        )

    @property
    def weapons(self):
        """
        Returns a list of equipped weapons.
        """
        return self._data[EquipmentType.WEAPON] or []

    @weapons.setter
    def weapons(self, value):
        """
        Sets the weapons for the equipment handler.

        Args:
            value (Any): The new value to set for the weapons.

        This method updates the internal data dictionary with the new value
        for the weapons and then saves the updated data.
        """
        self._data[EquipmentType.WEAPON] = value
        self._save()

    def all(self):
        """
        Returns a list of all equipped items.

        Returns:
            list: A list of equipped items.
        """
        equipment = [
            item
            for slot in self._data.values()
            for item in (slot if isinstance(slot, list) else [slot])
            if item
        ]
        equipment = sorted(
            equipment,
            key=lambda x: EQUIPMENT_TYPE_ORDER.index(x.equipment_type),
        )
        return equipment

    def remove(self, item):
        """
        Removes the specified item from the equipment.

        Args:
            item (Item): The item to be removed.
        """
        equipment_type = None
        for eq_type, equipment in self._data.items():
            if isinstance(equipment, list):
                if item in equipment:
                    equipment.remove(item)
                    equipment_type = eq_type
                    break
            elif equipment == item:
                self._data[eq_type] = None
                equipment_type = eq_type
                break

        for piece in item.covering:
            piece.covered_by.remove(self)
        item.covering = []

        if (
            equipment_type == EquipmentType.WEAPON
            or equipment_type == EquipmentType.SHIELD
        ):
            remaining_weapons = self._data[EquipmentType.WEAPON]
            if remaining_weapons:
                self.obj.msg("You switch your weapon to use two hands.")

        self._save()
        self._display_remove_message(item, equipment_type)

    def _display_remove_message(self, item, equipment_type):
        if equipment_type == EquipmentType.WEAPON:
            message = f"$You() $conj(sheath) {item.get_display_name(self.obj)}."
        else:
            message = f"$You() $conj(remove) {item.get_display_name(self.obj)}."
        self.obj.location.msg_contents(message, from_obj=self.obj)

    def _check_equipment_constraints(self, item):
        if self._data[item.equipment_type]:
            self.obj.msg("You are already wearing something there.")
            return False
        return True

    def _check_ring_constraints(self, item):
        if len(self._data[EquipmentType.RING]) >= 2:
            self.obj.msg("You are already wearing two rings.")
            return False
        return True

    def _check_shield_constraints(self, item):
        if self._data[EquipmentType.WEAPON]:
            if len(self._data[EquipmentType.WEAPON]) >= 2:
                self.obj.msg("You cannot wear a shield with two weapons.")
                return False

            self.obj.msg("You switch your weapon to a single hand.")
        return True

    def _check_weapon_constraints(self, item):
        if self._data[EquipmentType.WEAPON] is None:
            return True
        elif len(self._data[EquipmentType.WEAPON]) >= 2:
            self.obj.msg("You are already wielding two weapons.")
            return False
        elif (
            self._data[EquipmentType.SHIELD]
            and len(self._data[EquipmentType.WEAPON]) >= 1
        ):
            self.obj.msg("You cannot wield two weapons with a shield.")
            return False
        elif len(self._data[EquipmentType.WEAPON]) >= 1:
            self.obj.msg("You switch your weapon to a single hand.")
        return True

    def _display_wear_message(self, item, equipment_type):
        if equipment_type == EquipmentType.WEAPON:
            message = f"$You() $conj(wield) {item.get_display_name(self.obj)}."
        else:
            message = f"$You() $conj(wear) {item.get_display_name(self.obj)}."
        self.obj.location.msg_contents(message, from_obj=self.obj)

    def wear(self, item):
        equipment_type = item.equipment_type

        if item in self.all():
            self.obj.msg(
                "You are already {wearing} that.".format(
                    wearing="wearing"
                    if equipment_type != EquipmentType.WEAPON
                    else "wielding"
                )
            )
            return

        if equipment_type == EquipmentType.WEAPON:
            if not self._check_weapon_constraints(item):
                return

        elif equipment_type == EquipmentType.RING:
            if not self._check_ring_constraints(item):
                return
        elif equipment_type == EquipmentType.SHIELD:
            if not self._check_shield_constraints(item):
                return
        else:
            if not self._check_equipment_constraints(item):
                return

        if self._data[equipment_type] is None and equipment_type in (
            EquipmentType.WEAPON,
            EquipmentType.RING,
        ):
            self._data[equipment_type] = [item]
        elif isinstance(self._data[equipment_type], list):
            self._data[equipment_type].append(item)
        else:
            self._data[equipment_type] = item

        self._save()
        self._display_wear_message(item, equipment_type)

    def reset(self):
        """
        Resets the equipment to its default values.
        """
        self._data = copy(EQUIPMENT_DEFAULTS)
        self._save()
