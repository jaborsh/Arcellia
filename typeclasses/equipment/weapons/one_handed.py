from .weapons import Weapon, WeaponVersatility


class Flail(Weapon):
    """
    A one-handed flail weapon.

    Attributes:
        versatility (WeaponVersatility): The versatility of the flail, set to WeaponVersatility.ONE_HANDED.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.ONE_HANDED


class Morningstar(Weapon):
    """
    A class representing a Morningstar weapon.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon, indicating it is a one-handed weapon.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.ONE_HANDED


class Rapier(Weapon):
    """
    A one-handed weapon with high versatility.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon, set to WeaponVersatility.ONE_HANDED.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.ONE_HANDED


class Scimitar(Weapon):
    """
    A one-handed weapon class representing a scimitar.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon,
            indicating that it can be wielded with one hand.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.ONE_HANDED


class Shortsword(Weapon):
    """
    A class representing a shortsword weapon.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon, indicating it can be used with one hand.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.ONE_HANDED


class WarPick(Weapon):
    """
    A one-handed war pick weapon.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon, indicating that it is a one-handed weapon.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.ONE_HANDED
