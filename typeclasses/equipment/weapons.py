from typeclasses.equipment.equipment import Equipment, EquipmentType


class Weapon(Equipment):
    """
    Represents a weapon in the game.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.attributes.add("equipment_type", EquipmentType.WEAPON)

    @property
    def damage(self):
        """
        Returns the damage dealt by the weapon.
        """
        return self.attributes.get("damage", 0)
