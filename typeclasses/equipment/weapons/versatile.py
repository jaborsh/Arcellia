from .weapons import Weapon, WeaponVersatility


class Battleaxe(Weapon):
    """
    A versatile battleaxe weapon.

    Inherits from the Weapon class and sets the versatility to VERSATILE.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.VERSATILE


class Longsword(Weapon):
    """
    A versatile longsword weapon.

    Inherits from the Weapon class and sets the versatility to VERSATILE.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.VERSATILE


class Trident(Weapon):
    """
    A versatile trident weapon.

    Inherits from the Weapon class and sets the versatility to VERSATILE.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.VERSATILE


class Warhammer(Weapon):
    """
    A versatile warhammer weapon.

    Inherits from the Weapon class and sets the versatility to VERSATILE.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.VERSATILE
