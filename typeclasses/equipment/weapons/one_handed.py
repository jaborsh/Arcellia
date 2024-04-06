from .weapons import Weapon, WeaponVersatility


# Martial Weapons
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


# Simple Weapons
class Club(Weapon):
    """
    A one-handed club weapon.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon, indicating it is a one-handed weapon.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.ONE_HANDED


class Dagger(Weapon):
    """
    A one-handed dagger weapon.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon, indicating it is a one-handed weapon.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.ONE_HANDED


class Handaxe(Weapon):
    """
    A one-handed handaxe weapon.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon, indicating it is a one-handed weapon.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.ONE_HANDED


class Javelin(Weapon):
    """
    A one-handed javelin weapon.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon, indicating it is a one-handed weapon.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.ONE_HANDED


class LightHammer(Weapon):
    """
    A one-handed light hammer weapon.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon, indicating it is a one-handed weapon.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.ONE_HANDED


class Mace(Weapon):
    """
    A one-handed mace weapon.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon, indicating it is a one-handed weapon.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.ONE_HANDED


class Sickle(Weapon):
    """
    A one-handed sickle weapon.

    Attributes:
        versatility (WeaponVersatility): The versatility of the weapon, indicating it is a one-handed weapon.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.ONE_HANDED
