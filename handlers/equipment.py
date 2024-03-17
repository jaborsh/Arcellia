from handlers.handler import Handler
from typeclasses.clothing import ClothingType
from typeclasses.equipment import EquipmentType

EQUIPMENT_TYPE_COVER = {
    EquipmentType.HEADWEAR: [
        ClothingType.HEADWEAR,
        ClothingType.EYEWEAR,
        ClothingType.EARRING,
    ],
    EquipmentType.AMULET: [],
    EquipmentType.CLOAK: [],
    EquipmentType.BODY: [
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
    EquipmentType.BODY,
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

    equipment_defaults = {
        EquipmentType.HEADWEAR: None,
        EquipmentType.AMULET: None,
        EquipmentType.CLOAK: None,
        EquipmentType.BODY: None,
        EquipmentType.HANDWEAR: None,
        EquipmentType.RING: None,
        EquipmentType.FOOTWEAR: None,
        EquipmentType.WEAPON: None,
        EquipmentType.SHIELD: None,
    }

    def __init__(self, obj, db_attribute="equipment"):
        """
        Initializes the EquipmentHandler instance.

        Args:
            obj (GameObject): The game object associated with the equipment handler.
            db_attribute (str, optional): The name of the attribute used to store the equipment data. Defaults to "equipment".
        """
        if not obj.attributes.get(db_attribute, None):
            obj.attributes.add(db_attribute, self.equipment_defaults.copy())

        self.data = obj.attributes.get(db_attribute)
        self.db_attribute = db_attribute
        self.obj = obj

    def all(self):
        """
        Returns a list of all equipped items.

        Returns:
            list: A list of equipped items.
        """
        equipment = [item for item in self.data.values() if item]
        equipment = sorted(
            equipment, key=lambda x: EQUIPMENT_TYPE_ORDER.index(x.equipment_type)
        )
        return equipment

    def remove(self, item):
        """
        Removes the specified item from the equipment.

        Args:
            item (Item): The item to be removed.
        """
        for equipment_type, equipment in self.data.items():
            if equipment == item:
                self.data[equipment_type] = None
                break

        for piece in item.covering:
            piece.covered_by.remove(self)

        item.covering = []

        self._save()
        message = f"$You() $conj(remove) {item.get_display_name(self.obj)}."
        self.obj.location.msg_contents(message, from_obj=self.obj)

    def wear(self, item):
        """
        Wears the specified item.

        Args:
            item (Item): The item to be worn.
        """
        equipment_type = item.equipment_type
        if self.data[equipment_type]:
            self.obj.msg("You are already wearing something in that slot.")
            return

        self.data[equipment_type] = item
        self._save()
        message = f"$You() $conj(wear) {item.get_display_name(self.obj)}."
        self.obj.location.msg_contents(message, from_obj=self.obj)

    def reset(self):
        """
        Resets the equipment to its default values.
        """
        self.data = self.equipment_defaults.copy()
        self._save()