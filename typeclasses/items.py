from handlers import traits
from world.items.rarity import ItemRarity

from evennia.utils.utils import lazy_property
from typeclasses.objects import Object


class Item(Object):
    @lazy_property
    def traits(self):
        return traits.TraitHandler(self, db_attribute_key="traits")

    @property
    def price(self):
        return self.traits.get("price") or 0

    @price.setter
    def price(self, value):
        if not isinstance(value, int):
            raise ValueError("Invalid price value.")

        self.traits.add("price", value)

    @property
    def rarity(self):
        return self.traits.get("rarity") or ItemRarity.COMMON

    @rarity.setter
    def rarity(self, value):
        map = {
            "common": ItemRarity.COMMON,
            "uncommon": ItemRarity.UNCOMMON,
            "rare": ItemRarity.RARE,
            "very rare": ItemRarity.VERY_RARE,
            "legendary": ItemRarity.LEGENDARY,
            "quest": ItemRarity.QUEST,
        }

        if isinstance(value, str):
            value = map.get(value.lower())
        elif not isinstance(value, ItemRarity):
            raise ValueError("Invalid rarity value.")

        self.traits.add("rarity", value)

    @property
    def weight(self):
        return self.traits.get("weight") or 0

    @weight.setter
    def weight(self, value):
        if not (isinstance(value, int) or isinstance(value, float)):
            raise ValueError("Invalid weight value.")

        self.traits.add("weight", value)
