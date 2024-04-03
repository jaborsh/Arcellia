from enum import Enum

from .equipment import Equipment, EquipmentType


class WeaponVersatility(Enum):
    """
    Defines the versatility of a weapon.
    """

    ONE_HANDED = "one-handed"
    TWO_HANDED = "two-handed"


class Weapon(Equipment):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.equipment_type = EquipmentType.WEAPON

    @property
    def versatility(self):
        return self.traits.get("versatility")

    @versatility.setter
    def versatility(self, value: WeaponVersatility):
        self.traits.add("versatility", "Versatility", trait_type="trait", value=value)
