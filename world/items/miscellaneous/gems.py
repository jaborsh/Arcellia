from typeclasses.items import Item
from world.items.rarity import ItemRarity


class Onyx(Item):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.display_name = "|xOnyx|n"
        self.db.desc = "As rich as the velvety cloak of twilight, each facet captures a fragment of midnight, keeping it prisoner within its glossy, opaque prison."
        self.db.senses = {
            "feel": "Its smooth surface is cool to the touch, betraying no hint of the fervor with which the darkness within was born.",
            "smell": "The stone carries no scent, yet being near it recalls the clean, crisp air of a world shrouded in twilight.",
            "sound": "Holding it close, one might fancy hearing a faint echo, as if the onyx pulses with the heartbeat of the shadows.",
            "taste": "The presence of the onyx is like a breath of night air, flavorless and pure, yet reminiscent of the calm before a storm.",
        }
        self.price = 35
        self.rarity = ItemRarity.COMMON
        self.weight = 0.01
