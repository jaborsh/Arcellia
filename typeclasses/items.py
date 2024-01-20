from handlers import traits
from world.items.rarity import ItemRarity

from evennia.utils.utils import lazy_property
from typeclasses.objects import Object


class Item(Object):
    def at_object_creation(self):
        self.traits.add("price", "Price", trait_type="static", base=0)
        self.traits.add("rarity", "Rarity", trait_type="trait", value=ItemRarity.COMMON)
        self.traits.add("weight", "Weight", trait_type="static", base=0)

    @lazy_property
    def traits(self):
        return traits.TraitHandler(self, db_attribute_key="traits")

    @property
    def price(self):
        return self.traits.get("price")

    @price.setter
    def price(self, value):
        if not isinstance(value, int):
            raise ValueError("Invalid price value.")

        self.traits.price.base = value

    @property
    def rarity(self):
        return self.traits.get("rarity")

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

        self.traits.rarity.value = value

    @property
    def weight(self):
        return self.traits.weight

    @weight.setter
    def weight(self, value):
        if not (isinstance(value, int) or isinstance(value, float)):
            raise ValueError("Invalid weight value.")

        self.traits.weight.base = value
