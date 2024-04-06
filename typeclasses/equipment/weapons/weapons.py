from enum import Enum

from typeclasses.equipment.equipment import Equipment, EquipmentType


class WeaponVersatility(Enum):
    """
    Defines the versatility of a weapon.
    """

    ONE_HANDED = "one-handed"
    VERSATILE = "versatile"
    TWO_HANDED = "two-handed"


class Weapon(Equipment):
    """
    Represents a weapon in the game.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.equipment_type = EquipmentType.WEAPON

    @property
    def versatility(self):
        """
        Get the versatility of the weapon.

        Returns:
            WeaponVersatility: The versatility of the weapon.
        """
        return self.traits.get("versatility").value

    @versatility.setter
    def versatility(self, value: WeaponVersatility):
        """
        Set the versatility of the weapon.

        Args:
            value (WeaponVersatility): The versatility value to set.
        """
        self.traits.add("versatility", "Versatility", trait_type="trait", value=value)
