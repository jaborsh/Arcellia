from evennia.utils.utils import lazy_property

from handlers import traits
from prototypes import spawner
from world.items.rarity import ItemRarity


class ItemMixin:
    @lazy_property
    def traits(self):
        return traits.TraitHandler(self, db_attribute_key="traits")

    def at_post_spawn(self):
        # Do not manually call since attributes are removed after initial run.
        price = self.attributes.get("price", 0)
        rarity = self.attributes.get("rarity", ItemRarity.COMMON)
        spawns = self.attributes.get("spawns", [])
        weight = self.attributes.get("weight", 0)

        self.traits.add("price", "Price", trait_type="static", base=price)
        self.traits.add("rarity", "Rarity", value=rarity)
        self.traits.add("spawns", "Spawns", value=spawns)
        self.traits.add("weight", "Weight", trait_type="static", base=weight)

        self.spawn_contents()

        self.attributes.remove("price")
        self.attributes.remove("rarity")
        self.attributes.remove("spawns")
        self.attributes.remove("weight")

    def spawn_contents(self):
        if self.traits.get("spawns").value:
            for spawn in self.traits.get("spawns").value:
                spawn["location"] = self
                spawn["home"] = self
                spawner.spawn(spawn)

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
        return self.traits.get("weight")

    @weight.setter
    def weight(self, value):
        if not (isinstance(value, int) or isinstance(value, float)):
            raise ValueError("Invalid weight value.")

        self.traits.weight.base = value
