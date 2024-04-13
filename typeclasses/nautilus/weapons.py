from typeclasses.equipment.weapons.weapons import Weapon, WeaponVersatility


class EmberwispBlade(Weapon):
    def at_object_creation(self):
        super().at_object_creation()
        self.versatility = WeaponVersatility.TWO_HANDED
