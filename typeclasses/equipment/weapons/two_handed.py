from .weapons import Weapon, WeaponVersatility


# Martial Weapons
class Glaive(Weapon):
    """
    A two-handed weapon known as a glaive.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon,
            indicating that it is a two-handed weapon.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.TWO_HANDED


class Greataxe(Weapon):
    """
    A class representing a greataxe weapon.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon, set to `WeaponVersatility.TWO_HANDED`.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.TWO_HANDED


class Greatsword(Weapon):
    """
    A class representing a two-handed greatsword weapon.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon, set to WeaponVersatility.TWO_HANDED.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.TWO_HANDED


class Halberd(Weapon):
    """
    A class representing a halberd weapon.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon,
            indicating that it is a two-handed weapon.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.TWO_HANDED


class Maul(Weapon):
    """
    A two-handed weapon known as a Maul.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon,
            indicating that it is a two-handed weapon.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.TWO_HANDED


class Pike(Weapon):
    """
    A class representing a pike weapon.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon,
            indicating that it is a two-handed weapon.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.TWO_HANDED


# Simple Weapons
class Greatclub(Weapon):
    """
    A two-handed weapon known as a greatclub.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon,
            indicating that it is a two-handed weapon.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.TWO_HANDED


# Ranged
class Shortbow(Weapon):
    """
    A two-handed shortbow weapon.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon, set to `WeaponVersatility.TWO_HANDED`.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.TWO_HANDED
