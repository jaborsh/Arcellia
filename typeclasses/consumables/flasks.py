from evennia.utils.utils import lazy_property

from handlers import traits
from typeclasses.consumables.consumables import Consumable


class Flask(Consumable):
    def at_object_creation(self):
        super().at_object_creation()
        self.locks.add("drop:false()")
        self.traits.add(
            "capacity", "Capacity", trait_type="counter", base=2, min=0, max=15
        )
        self.traits.add(
            "level", "Level", trait_type="counter", base=1, min=1, max=15
        )

    @property
    def display_name(self):
        return (
            self.attributes.get("display_name", self.name)
            + " {"
            + f"{self.capacity.current}"
            + "}"
        )

    @lazy_property
    def traits(self):
        return traits.TraitHandler(self, db_attribute_key="traits")

    @property
    def capacity(self):
        return self.traits.capacity

    @property
    def level(self):
        return self.traits.level

    def at_pre_drink(self, drinker):
        if self.capacity.current <= 0:
            drinker.msg("The flask is empty!")
            return False
        return True

    def at_drink(self, drinker):
        drinker.location.msg_contents(
            "$You() $conj(drink) from $your() $you(flask).",
            from_obj=drinker,
            mapping={"flask": self},
        )
        self.capacity.current -= 1

    def fill(self, filler):
        self.capacity.current = self.capacity.base


class HealthFlask(Flask):
    restoration_table = {
        1: 250,
        2: 400,
        3: 525,
        4: 625,
        5: 700,
        6: 750,
        7: 775,
        8: 800,
        9: 825,
        10: 850,
        11: 875,
        12: 900,
        13: 925,
        14: 950,
        15: 975,
        16: 1000,
    }

    def at_drink(self, drinker):
        super().at_drink(drinker)
        drinker.health.current += self.restoration_table[self.level.current]


class ManaFlask(Flask):
    restoration_table = {
        1: 50,
        2: 65,
        3: 80,
        4: 95,
        5: 110,
        6: 125,
        7: 140,
        8: 155,
        9: 170,
        10: 185,
        11: 200,
        12: 210,
        13: 220,
        14: 230,
        15: 240,
        16: 250,
    }

    def at_drink(self, drinker):
        super().at_drink(drinker)
        drinker.mana.current += self.restoration_table[self.level.current]
