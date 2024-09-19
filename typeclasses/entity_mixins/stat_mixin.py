from evennia.utils.utils import lazy_property

from handlers import traits
from world.characters import stats as char_stats


class StatMixin:
    def init_stats(self):
        # Attributes
        self.stats.add(
            "vigor", "Vigor", trait_type="counter", base=1, min=1, max=20
        )
        self.stats.add(
            "mind", "Mind", trait_type="counter", base=1, min=1, max=20
        )
        self.stats.add(
            "endurance",
            "Endurance",
            trait_type="counter",
            base=1,
            min=1,
            max=20,
        )
        self.stats.add(
            "strength", "Strength", trait_type="counter", base=1, min=1, max=20
        )
        self.stats.add(
            "dexterity",
            "Dexterity",
            trait_type="counter",
            base=1,
            min=1,
            max=20,
        )
        self.stats.add(
            "intelligence",
            "Intelligence",
            trait_type="counter",
            base=1,
            min=1,
            max=20,
        )
        self.stats.add(
            "faith", "Faith", trait_type="counter", base=1, min=1, max=20
        )
        self.stats.add(
            "arcane", "Arcane", trait_type="counter", base=1, min=1, max=20
        )
        self.stats.add(
            "charisma", "Charisma", trait_type="counter", base=1, min=1, max=20
        )

        self.stats.add(
            "health",
            "Health",
            trait_type="gauge",
            base=char_stats.HEALTH_LEVELS[1],
            min=0,
            max=char_stats.HEALTH_LEVELS[1],
        )
        self.stats.add(
            "mana",
            "Mana",
            trait_type="gauge",
            base=char_stats.MANA_LEVELS[1],
            min=0,
            max=char_stats.MANA_LEVELS[1],
        )
        self.stats.add(
            "stamina",
            "Stamina",
            trait_type="gauge",
            base=char_stats.STAMINA_LEVELS[1],
            min=0,
            max=char_stats.STAMINA_LEVELS[1],
        )

        # Misc.
        self.stats.add(
            "experience", "Experience", trait_type="counter", base=0, min=0
        )
        self.stats.add("wealth", "Wealth", trait_type="counter", base=0, min=0)
        self.stats.add(
            "weight",
            "Weight",
            trait_type="counter",
            base=0,
            min=0,
            max=char_stats.WEIGHT_LEVELS[1],
        )

    @lazy_property
    def stats(self):
        return traits.TraitHandler(self, db_attribute_key="stats")

    @property
    def vigor(self):
        return self.stats.get("vigor")

    @property
    def mind(self):
        return self.stats.get("mind")

    @property
    def endurance(self):
        return self.stats.get("endurance")

    @property
    def strength(self):
        return self.stats.get("strength")

    @property
    def dexterity(self):
        return self.stats.get("dexterity")

    @property
    def intelligence(self):
        return self.stats.get("intelligence")

    @property
    def faith(self):
        return self.stats.get("faith")

    @property
    def arcane(self):
        return self.stats.get("arcane")

    @property
    def charisma(self):
        return self.stats.get("charisma")

    @property
    def health(self):
        return self.stats.get("health")

    @property
    def mana(self):
        return self.stats.get("mana")

    @property
    def stamina(self):
        return self.stats.get("stamina")

    @property
    def experience(self):
        return self.stats.get("experience")

    @property
    def wealth(self):
        return self.stats.get("wealth")

    @property
    def weight(self):
        self.stats.get("weight").current = sum(
            [o.db.weight for o in self.contents]
        )
        return self.stats.get("weight")
